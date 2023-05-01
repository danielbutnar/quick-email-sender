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
from my_module.common_imports import *
from my_module.utils import *

from my_module import TextProcessing, EmailHandler, utility_function_1
from my_module.email_handler import send_emails_concurrently

def main():
    """
    The main function for parsing command-line arguments and sending emails.

    Args:
        None

    Returns:
        None
    """
    pickle_directory, openai_api_key = utility_function_1()

    text_processing = TextProcessing(pickle_directory, openai_api_key)
    email_handler = EmailHandler(text_processing)

    
    parser = argparse.ArgumentParser(description="Send an email to multiple recipients.")
    parser.add_argument("recipient_email", nargs='+', help="Recipient email addresses separated by spaces.")
    parser.add_argument("subject", help="Email subject.")
    parser.add_argument("message", help="Email message.")
    parser.add_argument("-add", "--attachment", help="Path to the file to attach to the email.", default=None)
    parser.add_argument("-p", "--person", dest="ai_person", help="The type of AI person and context for rewriting the text (e.g., 'Employer-GPT').", default="Employer-GPT")
    parser.add_argument("-s", "--service", dest="service", help="The email service to use for sending the email (e.g., 'gmail', 'yahoo', 'outlook', 'hotmail', 'live', 'exchange', 'aol', 'zoho', 'mail', 'gmx', 'protonmail', 'icloud').", default="gmail")
    args = parser.parse_args()

    
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    
    try:
        print("main: calling send_emails_concurrently")
        send_emails_concurrently(email_handler, sender_email, sender_password, args.recipient_email, args.subject, args.message, args.attachment, args.ai_person, args.service)
    except Exception as e:
        logging.critical(f"Error sending email: {e}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send an email to multiple recipients.")
    parser.add_argument("recipient_email", nargs='+', help="Recipient email addresses separated by spaces.")
    parser.add_argument("subject", help="Email subject.")
    parser.add_argument("message", help="Email message.")
    parser.add_argument("-add", "--attachment", help="Path to the file to attach to the email.", default=None)
    parser.add_argument("-p", "--person", dest="ai_person", help="The type of AI person and context for rewriting the text (e.g., 'Employer-GPT').", default="Employer-GPT")
    parser.add_argument("-s", "--service", dest="service", help="The email service to use for sending the email (e.g., 'gmail', 'yahoo', 'outlook', 'hotmail', 'live', 'exchange', 'aol', 'zoho', 'mail', 'gmx', 'protonmail', 'icloud').", default="gmail")
    parser.add_argument("-help", action="store_true", help="Show this help message and exit.")
    args = parser.parse_args()

    if args.help:
        parser.print_help()
    else:
        main()
