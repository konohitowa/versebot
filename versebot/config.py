"""
VerseBot for reddit
By Matthieu Grieger
config.py
Copyright (c) 2015 Matthieu Grieger (MIT License)
"""

from os import environ
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

REDDIT_USERNAME = environ["REDDIT_USERNAME"]
REDDIT_PASSWORD = environ["REDDIT_PASSWORD"]
DATABASE_URL = environ["DATABASE_URL"]
LOG_LEVEL = INFO
MAXIMUM_MESSAGE_LENGTH = 6000
