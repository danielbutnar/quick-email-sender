from .common_imports import * 
import logging 
from .utils import *
class TextProcessing:
    """
    The TextProcessing class provides methods for processing and classifying text, such as detecting spam or generating formal text.
    """
   
    def __init__(self, pickle_directory, openai_api_key):
        """
        Initialize the natural language processing models, spam classifier and word features.
        """
        self.pickle_directory = pickle_directory
        self.openai_api_key = openai_api_key
        self.nlp_en = spacy.load("en_core_web_sm")
        self.nlp_de = spacy.load("de_core_news_sm")
        stanza.download('ro')
        self.stanza_nlp_ro = stanza.Pipeline('ro')

        # Load the spam classifier from the pickle file
        with open(Path(self.pickle_directory) / "spam_classifier.pickle", "rb") as f:
            self.classifier = pickle.load(f)

        # Load the word features from the pickle file
        with open(Path(self.pickle_directory) / "word_features.pickle", "rb") as f:
            self.word_features = pickle.load(f)
        # Load the spam classifier from the pickle file
        with open(Path(self.pickle_directory) / "spam_classifier.pickle", "rb") as f:
            self.classifier = pickle.load(f)

        # Load the word features from the pickle file
        with open(Path(self.pickle_directory) / "word_features.pickle", "rb") as f:
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
            
            prompt = f"Please compose a formal email in the specified {language}, written as {ai_person}, addressed to an authority figure. The email should include a greeting, the following message, and a closing. Make sure to incorporate corporate speak into the rewritten message, strive to maintain the persona of the specified individual, and elaborate on the message to make it longer, while ensuring that it remains coherent and relevant.\n\nMessage:\n{message}\n\nEmail:"
            response = openai.Completion.create(
                engine=openai_engine,
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
        openai.api_key = self.openai_api_key

        language_name = {
            "en": "English",
            "de": "German",
            "ro": "Romanian"
        }.get(language, "English")
        print("Detected language:", language)
        prompt = (
    f"Please rewrite the following text in {language}, ensuring the use of a formal and sophisticated corporate style appropriate for a professional email, excluding greetings."
    " Pay close attention to the following:"
    "\n- Use language-specific style elements, phrases, or words common in corporate communications."
    "\n- Include idiomatic expressions or natural-sounding phrases in the target language."
    "\n- Maintain the desired level of formality and avoid informal language."
    "\n- Keep the message concise, avoiding unnecessary repetition."
    "\n- Preserve the core meaning of the original text, closely following its structure and content."
    "\n\nIf there are any ambiguous words or phrases, please consider the context and clarify the intended meaning in the rewritten text."
    " Additionally, ensure the output is grammatically accurate with correct spelling and punctuation."
    " If necessary, divide the text into smaller segments to focus on specific parts and improve the output quality."
    f"\n\nOriginal text:\n{text}\n\nFormal version:"
)


        response = openai.Completion.create(
            engine=engine,
            prompt=prompt,
            max_tokens=700,
            n=1,
            stop=None,
            temperature=0.8,
        )

        formal_text = response.choices[0].text.strip()

        return formal_text