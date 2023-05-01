# Professional Email Sender

This script allows you to send professional emails to multiple recipients, with an optional attachment. The emails are automatically formatted with a greeting, a more formal content, and a closing. The language of the email is detected, and appropriate language models are used to generate the more formal content, including OpenAI's GPT-3 for advanced text generation.

## Prerequisites

Before running the script, make sure you have the following Python libraries installed:

- `spacy`
- `stanza`
- `conceptnet_lite`
- `openai`
- `langdetect`

Also, ensure you have the language models downloaded for `spacy` and `stanza`.

## Installation

1. Clone the repository:

git clone https://github.com/yourusername/professional-email-sender.git

2. Change to the project directory:

cd professional-email-sender

3. Install the required packages:


3. Install the required packages:

pip install -r requirements.txt

4. Download the necessary language models:

python -m spacy download en_core_web_sm
python -m spacy download de_core_news_sm
python -m stanza.download('ro')

5. Set up OpenAI API Key:

To use GPT-3 for advanced text generation, make sure you have an API key for the OpenAI API. You can obtain one by signing up for OpenAI's GPT-3 service.

Edit the .env file and enter your actual API key:
openai.api_key = "your-api-key-here"

 Update the `sender_email` and `sender_password` variables with your Gmail account email and password or app-specific password.
 
 Update your pickle path with your actual path

## Usage


Run the script with the required arguments:

python send_email.py recipient@example.com "Subject" "Message"

You can also send emails to multiple recipients:

python send_email.py recipient1@example.com recipient2@example.com "Subject" "Message"

To include an attachment, use the `-add` or `--attachment` option:

python send_email.py recipient@example.com "Subject" "Message" -add "path/to/attachment"

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


