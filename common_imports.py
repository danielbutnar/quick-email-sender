import argparse
import os
import re
import smtplib
from concurrent.futures import ThreadPoolExecutor
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
import stanza
import spacy
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import openai
import nltk
from nltk.tokenize import word_tokenize
import langid
import conceptnet_lite
from dotenv import load_dotenv
import pickle
import logging
