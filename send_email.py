import smtplib
import argparse

def send_email(sender_email, sender_password, recipient_email, subject, message):
    # Create an SMTP connection
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Construct the email
    email_body = f"Subject: {subject}\n\n{message}"

    # Send the email
    server.sendmail(sender_email, recipient_email, email_body)
    server.quit()

def main():
    parser = argparse.ArgumentParser(description="Send an email")
    parser.add_argument("recipient_email", help="Recipient's email address")
    parser.add_argument("subject", help="Email subject")
    parser.add_argument("message", help="Email message")
    args = parser.parse_args()

    # Replace with your Gmail account email and password
    sender_email = "daniel.butnar@gmail.com"
    sender_password = "mlgooxieygudsxmr"

    send_email(sender_email, sender_password, args.recipient_email, args.subject, args.message)

if __name__ == "__main__":
    main()
