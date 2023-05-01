"""
This module provides a collection of utility classes and functions for text processing, email handling, and common imports.

It includes the following classes and functions:

Classes:

TextProcessing: A class containing various methods for processing and manipulating text.
EmailHandler: A class that provides functionality for handling and processing email-related tasks.
Functions:

utility_function_1: A general utility function for performing a specific task (e.g., data transformation, parsing, etc.)
common_imports: A collection of common and frequently used imports to be used across the application.
"""

from .text_processing import TextProcessing
from .email_handler import EmailHandler
from .utils import utility_function_1
from .common_imports import *

__all__ = ['TextProcessing', 'EmailHandler', 'utility_function_1', 'commun_imports']
