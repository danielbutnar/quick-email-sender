# Professional Email Sender

This script allows you to send professionally formatted emails to multiple recipients, with optional attachments. The emails are automatically formatted with a greeting, a more formal content, and a closing. The language of the email is detected, and appropriate language models are used to generate the more formal content, including OpenAI's GPT-3 for advanced text generation.

## Prerequisites

Before running the script, make sure you have the following Python libraries installed:

- `spacy`
- `stanza`
- `conceptnet_lite`
- `openai`
- `langdetect`

Also, ensure you have the language models downloaded for `spacy` and `stanza`.

## Contribution

We would love for you to contribute to this project! Here's how you can get started:

1. Fork this repository to your own GitHub account.
2. Make your desired changes on a separate branch.
3. When you're ready, create a pull request so we can review your changes and merge them into the main branch.
4. Before you can start making changes, please ensure that you have the following prerequisites installed on your computer:



Also, make sure to download the necessary language models for spacy and stanza. If you need any help with the setup, don't hesitate to reach out to us!







## Installation

1. Clone the repository:

git clone https://github.com/yourusername/professional-email-sender.git

2. Change to the project directory:

cd professional-email-sender

3. Install the required packages:

pip install -r requirements.txt

4. Download the necessary language models:

python -m spacy download en_core_web_sm
python -m spacy download de_core_news_sm
python -m stanza.download('ro')
python -m spacy download fr_core_news_sm
python -m spacy download es_core_news_sm
python -m spacy download it_core_news_sm
python -m spacy download nl_core_news_sm
python -m spacy download pt_core_news_sm
python -m spacy download ru_core_news_sm
python -m spacy download sv_core_news_sm
python -m spacy download tr_core_news_sm
python -m spacy download zh_core_web_sm

5. Set up OpenAI API Key:

To use GPT-3 for advanced text generation, make sure you have an API key for the OpenAI API. You can obtain one by signing up for OpenAI's GPT-3 service.

Edit the `.env` file and enter your actual API key, email credentials, and pickle path:

OPENAI_API_KEY='your-api-key-here'
SENDER_EMAIL='your-email-here'
SENDER_PASSWORD='your-password-here'
PICKLE_DIRECTORY='your\path\to\pickle\dir'

## Usage

Run the script with the required arguments:


You can also send emails to multiple recipients:


python send_email.py recipient1@example.com recipient2@example.com "Subject" "Message"

To include an attachment, use the `-add` or `--attachment` option:

python send_email.py recipient@example.com "Subject" "Message" -add "path/to/attachment"

To customize the rewriting of the text, use the `-p` or `--person` option:

python send_email.py recipient@example.com "Subject" "Message" -p StudentGPT

Now, the program will rewrite the text from the perspective of a student.

To use a different email service, use the `-s` or `--service` option:

python send_email.py recipient@example.com "Subject" "Message" -s yahoo

## Creating a Command Alias (Windows)

To make it easier to use the script, you can create a command alias that allows you to call the program in the Command Prompt like this:
email recipient@example.com "Subject" "Message"

Follow these steps to set up a command alias for Windows:

1. Create a new text file in the `professional-email-sender` directory and name it `email.cmd`.

2. Open `email.cmd` in a text editor and add the following line:

@python "%~dp0\send_email.py" %*

This line tells the script to run `send_email.py` with the provided arguments when you use the `email` command.

3. Add the `professional-email-sender` directory to your system's `PATH` environment variable:

   a. Open the Start menu, right-click on "Computer" or "This PC", and select "Properties".
   
   b. Click on "Advanced system settings" on the left side.
   
   c. Click on the "Environment Variables" button near the bottom.
   
   d. Under "System variables", find the `Path` variable, select it, and click "Edit".
   
   e. Append the full path to the `professional-email-sender` directory to the end of the `Path` variable, separated by a semicolon. For example:

C:\Users\YourUsername\path\to\professional-email-sender

4. Save your changes, and restart any open Command Prompt windows. Now you can use the `email` command to send emails:

email recipient@example.com "Subject" "Message"
## Creating a Command Alias (macOS and Linux)

To make it easier to use the script, you can create a command alias that allows you to call the program in the terminal like this:

email recipient@example.com "Subject" "Message"

Follow these steps to set up a command alias for macOS and Linux:

1. Open a terminal window and navigate to your home directory by running:

cd ~

2. Open the `.bashrc` file (Linux) or `.bash_profile` file (macOS) with a text editor:

For Linux:
nano .bashrc

For macOS:
nano .bash_profile


3. Add the following line to the end of the file, replacing `/path/to/professional-email-sender` with the actual path to the project directory:

alias email='python3 /path/to/professional-email-sender/send_email.py'

4. Save the changes and exit the text editor.

5. Reload the configuration file by running:

For Linux:
source .bashrc

For macOS:
source .bash_profile

Now you can use the `email` command to send emails:

email recipient@example.com "Subject" "Message"
## License

This project is licensed under a Custom License. See the [LICENSE](LICENSE.txt) file for details.


