from .common_imports import *
from .utils import *
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
        smtp_server, smtp_port = self.get_smtp_settings(service.lower())

        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        try:
            server.login(sender_email, sender_password)
        except smtplib.SMTPAuthenticationError as e:
            logging.error(f"Error: Authentication failed - {e}")
            server.quit()
            return
        except Exception as e:
            logging.error(f"Error: Unable to login - {e}")
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
    """
    This function sends emails concurrently to multiple recipients using an EmailHandler instance, with optional attachment.

    Args:
    email_handler (EmailHandler): An instance of the EmailHandler class, responsible for handling and processing email-related tasks.
    sender_email (str): The email address of the sender.
    sender_password (str): The password for the sender's email account.
    recipient_emails (list): A list of email addresses to send the email to.
    subject (str): The subject of the email.
    message (str): The content of the email.
    attachment_path (str): The path to a file to be attached to the email (optional).
    ai_person (str): The name of the AI persona used for communication (optional).
    service (str): The email service provider to use for sending emails (e.g., 'gmail', 'yahoo', etc.).
    num_workers (int, optional): The number of worker threads for sending emails concurrently. Default is 10.

    This function divides the list of recipient email addresses into equal-sized chunks and sends emails to each chunk concurrently using a ThreadPoolExecutor. 
    It prints any errors that occur during the email sending process.
    """
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
    
