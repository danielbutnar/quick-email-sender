Quick Email Sender


A simple command-line tool for sending emails using a Gmail account. This tool enables you to send emails directly from your command line without opening your email client.

Requirements


Python 3.x
A Gmail account with "Allow less secure apps" enabled or an app-specific password


Setup
Clone the repository or download the send_email.py file to your local machine.
Open send_email.py in a text editor and replace the sender_email and sender_password variables with your Gmail account email and password or app-specific password.
Save the changes and close the text editor.


Usage
Run the following command in your terminal or command prompt, replacing the recipient email, subject, and message with your desired values:
python send_email.py recipient@example.com "Your email subject" "Your email message"


Automation


Windows
Create a new text file named email.cmd in the same directory as send_email.py.

Open email.cmd in a text editor and add the following line:


@echo off
python path\to\send_email.py %*


Replace path\to\ with the full path to the send_email.py file.

Save the changes and close the text editor.

Add the directory containing email.cmd to your system's PATH environment variable:
a. Press Win + X and select "System".
b. Click "Advanced system settings" on the right side.
c. Click the "Environment Variables" button.
d. Under "System variables", find and select the "Path" variable, then click "Edit".
e. Click "New" and add the path to the directory containing email.cmd (e.g., C:\scripts\).
f. Click "OK" to close the dialogs and save the changes.

Now you can use the email command from any directory in your command prompt:
email recipient@example.com "Your email subject" "Your email message"


macOS and Linux


Make send_email.py executable by running the following command:


chmod +x /path/to/send_email.py


Replace /path/to/ with the full path to the send_email.py file.

Create a symbolic link to the script in a directory that's in your system's PATH, such as /usr/local/bin/:


sudo ln -s /path/to/send_email.py /usr/local/bin/email

Replace /path/to/ with the full path to the send_email.py file.

Now you can use the email command from any directory in your terminal:
email recipient@example.com "Your email subject" "Your email message"


Disclaimer
Please ensure that you follow the guidelines and policies of the email service provider you use. This script is provided for educational purposes, and the author is not responsible for any misuse or violation of terms of service.
