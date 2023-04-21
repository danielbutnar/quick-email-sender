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
import smtplib
import argparse
import os
import re
import spacy
import conceptnet_lite
import stanza
import openai
from langdetect import detect
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

script_directory = os.path.dirname(os.path.abspath(__file__))
conceptnet_db_path = os.path.join(script_directory, "conceptnet.db")
conceptnet_lite.connect(conceptnet_db_path)


nlp_en = spacy.load("en_core_web_sm")
nlp_de = spacy.load("de_core_news_sm")
stanza.download('ro')
stanza_nlp_ro = stanza.Pipeline('ro')




def generate_formal_text(text, nlp, language):
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





def generate_formal_text_gpt3(text, language):
    """
    Generates a more formal version of the input text using the GPT-3 language model.
    
    Args:
        text (str): The input text to be made more formal.
        language (str): The language code of the input text (e.g., "en" for English).

    Returns:
        str: The more formal version of the input text.
    """
    openai.api_key =  "your-api-key-here"

    language_name = {
        "en": "English",
        "de": "German",
        "ro": "Romanian"
    }.get(language, "English")

    prompt = f"Please rewrite in the following text in the language {language} in a more formal and sophisticated way, excluding greetings and closing phrases and making the text much longer, and also keep in mind this text is part of an email, after the greetings part, so rewrite it acordingly:\n\n{text}\n\nFormal version:"

    response = openai.Completion.create(
        #you can choose any enigne
        engine="text-davinci-003", 
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.8,
    )

    formal_text = response.choices[0].text.strip()

    return formal_text




def format_message(message, recipient_email):
    """
    Formats an email message by detecting its language, making it more formal, and adding a greeting and closing.

    Args:
        message (str): The email message to be formatted.
        recipient_email (str): The recipient's email address.

    Returns:
        str: The formatted email message with a greeting, more formal content, and a closing.
    """
    # Detect language
    language = detect(message)

    # Choose the appropriate language model
    if language == "en":
        nlp = nlp_en
    elif language == "de":
        nlp = nlp_de
    elif language == "ro":
        nlp = stanza_nlp_ro
    else:
        nlp = nlp_en  # Default to English

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
    formal_message = generate_formal_text_gpt3(message, language)


    # Insert the message into the professional template
    formatted_email = f"{template['greeting']}\n\n{formal_message}\n\n{template['closing']}"
    return formatted_email

# ... (rest of the code remains unchanged)
def send_email(sender_email, sender_password, recipient_emails, subject, message, attachment_path):
    """
    Sends an email to multiple recipients with an optional attachment.

    Args:
        sender_email (str): The sender's email address.
        sender_password (str): The sender's email password or app-specific password.
        recipient_emails (list): A list of recipient email addresses.
        subject (str): The email subject.
        message (str): The email message.
        attachment_path (str): The path to the file to be attached to the email (optional).

    Returns:
        None
    """
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, sender_password)

    for recipient_email in recipient_emails:
        formatted_message = format_message(message, recipient_email)

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
        server.sendmail(sender_email, recipient_email, email_body)


    server.quit()



def main():
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
    args = parser.parse_args()

    # Replace with your Gmail account email and password or app-specific password
    sender_email = "your_email@gmail.com"
    sender_password = "your_password"

    send_email(sender_email, sender_password, args.recipient_email, args.subject, args.message, args.attachment)


if __name__ == "__main__":
    main()
