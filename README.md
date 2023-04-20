# Quick Email Sender

A simple command-line tool for sending emails using a Gmail account. This tool enables you to send emails directly from your command line without opening your email client.

## Requirements

- Python 3.x
- A Gmail account with "Allow less secure apps" enabled or an app-specific password

## Setup

1. Clone the repository or download the `send_email.py` file to your local machine.
2. Open `send_email.py` in a text editor and replace the `sender_email` and `sender_password` variables with your Gmail account email and password or app-specific password.
3. Save the changes and close the text editor.

## Usage

Run the following command in your terminal or command prompt, replacing the recipient email, subject, and message with your desired values:

```sh
python send_email.py recipient@example.com "Your email subject" "Your email message"
