"""
A command-line script for sending professionally formatted emails to multiple recipients with optional attachments.

The script uses several natural language processing libraries and tools, such as spaCy, stanza, and GPT-3, to
detect the email's language, generate a more formal version of the input message, and apply an appropriate
greeting and closing based on the recipient's name and detected language. It also supports sending attachments
with the email.

Requirements:
- Python 3.9 or higher
- Libraries: smtplib, argparse, os, re, spacy, conceptnet_lite, stanza, openai, langdetect, email

Usage:
1. Replace the sender_email and sender_password variables in the main() function with your Gmail account email and
   password or app-specific password.
2. Run the script from the command line with the required arguments:
   recipient_email (one or more email addresses), subject, and message.
3. Optionally, provide an attachment file path using the -add or --attachment flag.

Example:
python send_email.py "recipient@example.com" "Email Subject" "Email message" --attachment "/path/to/attachment.txt"

Note: The script currently supports English, German, and Romanian languages.
"""
import argparse
import os
import re
import pickle
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
import langid

import conceptnet_lite

import nltk
import openai
import spacy
import stanza
import smtplib
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from langdetect import detect
from nltk.tokenize import word_tokenize
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is missing")
openai_engine = os.environ.get("OPENAI_ENGINE", "text-davinci-003")

nltk.download("punkt")
pickle_directory = os.getenv("PICKLE_DIRECTORY")
if not pickle_directory:
    raise ValueError("PICKLE_DIRECTORY environment variable is missing")



class TextProcessing:
    """
    The TextProcessing class provides methods for processing and classifying text, such as detecting spam or generating formal text.
    """
        
    def __init__(self):
        """
        Initialize the natural language processing models, spam classifier and word features.
        """
        self.nlp_en = spacy.load("en_core_web_sm")
        self.nlp_de = spacy.load("de_core_news_sm")
        stanza.download('ro')
        self.stanza_nlp_ro = stanza.Pipeline('ro')

        # Load the spam classifier from the pickle file
        with open(Path(pickle_directory) / "spam_classifier.pickle", "rb") as f:
            self.classifier = pickle.load(f)

        # Load the word features from the pickle file
        with open(Path(pickle_directory) / "word_features.pickle", "rb") as f:
            self.word_features = pickle.load(f)
        # Load the spam classifier from the pickle file
        with open(Path(pickle_directory) / "spam_classifier.pickle", "rb") as f:
            self.classifier = pickle.load(f)

        # Load the word features from the pickle file
        with open(Path(pickle_directory) / "word_features.pickle", "rb") as f:
            self.word_features = pickle.load(f)

    def find_features(self, message):
        """
        Finds the features of a message to be used for classification.
        
        Args:
            message (str): The message to find features for.
            
        Returns:
            dict: A dictionary of word features and their presence in the message.
        """
        words = set(message)
        features = {}
        for word in self.word_features:
            features[word] = (word in words)
        return features

    def classify_message(self, message):
        tokenized_message = word_tokenize(message)
        features = self.find_features(tokenized_message)
        result = self.classifier.classify(features)
        return result

    # ... (other functions)

    def is_spam_bert(self, email_content):
        model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        classification_pipeline = pipeline("text-classification", model=model, tokenizer=tokenizer)

        result = classification_pipeline(email_content)
        label = result[0]["label"]

        if label == "SPAM":
            return True
        else:
            return False
    def format_message(self, message, recipient_email, ai_person):
        """
        Formats an email message by detecting its language, making it more formal, and adding a greeting and closing.

        Args:
            message (str): The email message to be formatted.
            recipient_email (str): The recipient's email address.

        Returns:
            str: The formatted email message with a greeting, more formal content, and a closing.
        """
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is missing")

        openai_engine = os.environ.get("OPENAI_ENGINE", "text-davinci-003")


        # Detect language
        try:
            language = langid.classify(message)[0]
        except:
            language = input("Language not recognized. Please enter the language code (e.g., 'en' for English): ")

        supported_languages = ['en', 'de', 'ro', 'fr', 'es', 'it', 'nl', 'pt', 'ru', 'sv', 'tr', 'zh']
        if language in supported_languages:
            if language == "en":
                nlp = self.nlp_en
            elif language == "de":
                nlp = self.nlp_de
            elif language == "ro":
                nlp = self.stanza_nlp_ro

            # Extract the recipient's name from the email address
            name_match = re.match(r'([a-zA-Z]+)\.?([a-zA-Z]*)@', recipient_email)
            if name_match:
                recipient_name = name_match.group(1).capitalize()
                if name_match.group(2):
                    recipient_name += " " + name_match.group(2).capitalize()
            else:
                recipient_name = ""

            # Professional email templates
            templates = {
                "en": {
                    "greeting": f"Dear {recipient_name},",
                    "closing": "Best regards,\n\nDaniel"
                },
                "de": {
                    "greeting": f"Sehr geehrte{'' if recipient_name else 'r'} {recipient_name},",
                    "closing": "Mit freundlichen Grüßen,\n\nDaniel"
                },
                "ro": {
                    "greeting": f"Stimate {recipient_name},",
                    "closing": "Cu stimă,\n\nDaniel"
                }
            }

            template = templates.get(language, templates["en"])

            # Generate more formal text using GPT-3
            formal_message = self.generate_formal_text_gpt3(message, language, ai_person, openai_engine)

            # Insert the message into the professional template
        
            formatted_email = f"{template['greeting']}\n\n{formal_message}\n\n{template['closing']}"


        else:
            # For unsupported languages, use GPT-3 to generate the entire email, including greeting and closing
            prompt = f"Please write a formal email in {language} as an {ai_person} to an authority figure. The email should include a greeting, the following message, and a closing.\n\nMessage:\n{message}\n\nEmail:"
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=500,
                n=1,
                stop=None,
                temperature=0.8,
            )

            formatted_email = response.choices[0].text.strip()

        return formatted_email

    def is_spam_combined(self, email_content):
        """
        Checks if the given email content might be flagged as spam using both SpamAssassin and a pre-trained BERT model.

        Args:
            email_content (str): The email content to be checked for spam.

        Returns:
            bool: True if the email content might be flagged as spam, False otherwise.
        """
        bert_result = self.is_spam_bert(email_content)
        naive_bayes_result = self.classify_message(email_content) == "spam"

        return  bert_result or naive_bayes_result

    def generate_formal_text(self, text, nlp, language):
     """
     Generates a more formal version of the input text using ConceptNet and the provided language model.
    
     Args:
        text (str): The input text to be made more formal.
        nlp (spacy.lang or stanza.models): The language model for processing the input text.
        language (str): The language code of the input text (e.g., "en" for English).

     Returns:
        str: The more formal version of the input text.
     """
     if language == "ro":
        doc = nlp(text)
        tokens = [word for sent in doc.sentences for word in sent.words]
     else:
            doc = nlp(text)
            tokens = [token for token in doc]

            new_phrases = []

            for token in tokens:
                if language == "ro":
                    pos = token.upos
                    lemma = token.lemma
                else:
                    pos = token.pos_
                    lemma = token.lemma_

                if pos in ["NOUN", "VERB"]:
                    try:
                        concept = conceptnet_lite.Label.get(lemma, language).concepts[0]
                        related_concepts = [e.concept_to for e in concept.edges_out]
                        if related_concepts:
                            new_word = str(related_concepts[0].label).split('/')[3]
                            new_phrases.append(new_word)
                        else:
                            new_phrases.append(token.text)
                    except Exception as e:
                        new_phrases.append(token.text)
                else:
                    new_phrases.append(token.text)

            new_text = ' '.join(new_phrases).replace(" ,", ",").replace(" .", ".")

            return new_text


    def generate_formal_text_gpt3(self, text, language, ai_person, engine):
        """
        Generates a more formal version of the input text using the GPT-3 language model.
    
        Args:
            text (str): The input text to be made more formal.
            language (str): The language code of the input text (e.g., "en" for English).
            ai_person (str): The context of the AI persona (e.g., "assistant").
            engine (str): The GPT engine to use for generating text.

        Returns:
            str: The more formal version of the input text.
        """
        openai.api_key = openai_api_key

        language_name = {
            "en": "English",
            "de": "German",
            "ro": "Romanian"
        }.get(language, "English")
        print("Detected language:", language)
        prompt = f"Please rewrite the following text longer in {language}, taking into consideration the context of an {ai_person} writing to an authority figure. Enhance the formality and sophistication of the text while excluding greetings and closing phrases. Keep in mind that this text is part of the email body, following the greeting section.\n\nOriginal text:\n{text}\n\nFormal version:"

        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.8,
        )

        formal_text = response.choices[0].text.strip()

        return formal_text


    

class EmailHandler:
    """
    The EmailHandler class is responsible for handling email-related tasks, such as detecting the email service, getting SMTP settings, and sending emails.
    """
    def __init__(self, text_processing):
        """
        Initialize the EmailHandler class with the TextProcessing class instance and the Romanian language model.
        """
        
        self.text_processing = text_processing
        # stanza.download('ro')  # Download the Romanian language model if not already downloaded
        # self.stanza_nlp_ro = stanza.Pipeline('ro')  # Initialize the Romanian language model
    def get_smtp_settings(self, service):
        """
        Returns the SMTP server address and port number for the specified email service.

        Args:
            service (str): The email service provider (e.g., "gmail", "yahoo", "outlook").

        Returns:
            tuple: A tuple containing the SMTP server address (str) and port number (int).

        Raises:
            ValueError: If an invalid or unsupported email service is provided.
        """
        if service == "gmail":
            return "smtp.gmail.com", 465
        elif service == "yahoo":
            return "smtp.mail.yahoo.com", 465
        elif service == "outlook" or service == "hotmail" or service == "live":
            return "smtp.office365.com", 587
        elif service == "exchange":
            return "smtp.yourdomain.com", 587
        elif service == "aol":
            return "smtp.aol.com", 587
        elif service == "zoho":
            return "smtp.zoho.com", 587
        elif service == "mail" or service == "gmx":
            return "smtp.mail.com", 587
        elif service == "protonmail":
            return "smtp.protonmail.com", 587
        elif service == "icloud":
            return "smtp.mail.me.com", 587
        else:
            raise ValueError("Invalid email service provided.")
    

    def detect_email_service(self, sender_email):
        """
        Detects the email service based on the sender's email address.

        Args:
            sender_email (str): The sender's email address.

        Returns:
            str: The email service provider (e.g., "gmail", "yahoo", "outlook").
        """
        
        domain = sender_email.split("@")[-1]

        if "gmail" in domain:
            return "gmail"
        elif "yahoo" in domain:
            return "yahoo"
        elif "outlook" in domain or "hotmail" in domain or "live" in domain:
            return "outlook"
        elif "exchange" in domain:
            return "exchange"
        elif "aol" in domain:
            return "aol"
        elif "zoho" in domain:
            return "zoho"
        elif "mail" in domain or "gmx" in domain:
            return "mail"
        elif "protonmail" in domain:
            return "protonmail"
        elif "icloud" in domain or "me" in domain:
            return "icloud"
        else:
            return "unknown"

    def send_email(self, sender_email, sender_password, recipient_emails, subject, message, attachment_path, ai_person, service):
        """
        Sends an email to multiple recipients with an optional attachment.

        Args:
            sender_email (str): The sender's email address.
            sender_password (str): The sender's email password or app-specific password.
            recipient_emails (list): A list of recipient email addresses.
            subject (str): The email subject.
            message (str): The email message.
            attachment_path (str): The path to the file to be attached to the email (optional).
            ai_person (str): The name of the AI persona to use when formatting the message.
            service (str): The email service provider (default: "gmail").

        Returns:
            None
        """
        # Get the SMTP server and port using the new function
        print(f"send_email called for {recipient_emails[0]}")
        sender_password = os.getenv("SENDER_PASSWORD")
        smtp_server, smtp_port = self.get_smtp_settings(service.lower())

        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        try:
            server.login(sender_email, sender_password)
        except smtplib.SMTPAuthenticationError as e:
            print(f"Error: Authentication failed - {e}")
            server.quit()
            return
        except Exception as e:
            print(f"Error: Unable to login - {e}")
            server.quit()
            return

        for recipient_email in recipient_emails:
            formatted_message = self.text_processing.format_message(message, recipient_email, ai_person)
        

            if self.text_processing.is_spam_combined(formatted_message):
                print(f"Warning: Email to {recipient_email} might be flagged as spam. Skipping.")
                continue

            if attachment_path:
                msg = MIMEMultipart()
                msg['Subject'] = subject

                # Add the message body
                msg.attach(MIMEText(formatted_message, "plain"))

                # Add the attachment
                filename = os.path.basename(attachment_path)
                with open(attachment_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f"attachment; filename={filename}")
                    msg.attach(part)
                email_body = msg.as_string()
            else:
                email_body = f"Subject: {subject}\n\n{formatted_message}"

            email_body = email_body.encode("utf-8")
            try:
                server.sendmail(sender_email, recipient_email, email_body)
                print(f"Email sent to {recipient_email}")
            except Exception as e:
                print(f"Error sending email to {recipient_email}: {e}")

        server.quit()

def send_emails_concurrently(email_handler, sender_email, sender_password, recipient_emails, subject, message, attachment_path, ai_person, service, num_workers=10):
    # Divide the recipient_emails list into equal-sized chunks
    print("send_emails_concurrently called")
    chunk_size = len(recipient_emails) // num_workers + (len(recipient_emails) % num_workers > 0)
    email_chunks = [recipient_emails[i:i + chunk_size] for i in range(0, len(recipient_emails), chunk_size)]

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(email_handler.send_email, sender_email, sender_password, email_chunk, subject, message, attachment_path, ai_person, service) for email_chunk in email_chunks]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Error sending email: {e}")
    

def main():
    """
    The main function for parsing command-line arguments and sending emails.

    Args:
        None

    Returns:
        None
    """
    
    text_processing = TextProcessing()
    email_handler = EmailHandler(text_processing)

    """
    The main function for parsing command-line arguments and sending emails.

    Args:
        None

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="Send an email to multiple recipients.")
    parser.add_argument("recipient_email", nargs='+', help="Recipient email addresses separated by spaces.")
    parser.add_argument("subject", help="Email subject.")
    parser.add_argument("message", help="Email message.")
    parser.add_argument("-add", "--attachment", help="Path to the file to attach to the email.", default=None)
    parser.add_argument("-p", "--person", dest="ai_person", help="The type of AI person and context for rewriting the text (e.g., 'Employer-GPT').", default="Employer-GPT")
    parser.add_argument("-s", "--service", dest="service", help="The email service to use for sending the email (e.g., 'gmail', 'yahoo', 'outlook', 'hotmail', 'live', 'exchange', 'aol', 'zoho', 'mail', 'gmx', 'protonmail', 'icloud').", default="gmail")
    args = parser.parse_args()

    # Replace with your Gmail account email and password or app-specific password
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    
    try:
        print("main: calling send_emails_concurrently")
        send_emails_concurrently(email_handler, sender_email, sender_password, args.recipient_email, args.subject, args.message, args.attachment, args.ai_person, args.service)
    except Exception as e:
        print(f"Error sending email: {e}")

    # Detect the email service based on the sender's email address



if __name__ == "__main__":
    main()
