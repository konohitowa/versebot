"""
VerseBot for reddit
By Matthieu Grieger
versebot.py
Copyright (c) 2015 Matthieu Grieger (MIT License)
"""

import sys
import re
import praw
from . import database
import logging
from . import books
import requests
from time import sleep
import time
from . import webparser
from . import verse
from .regex import find_verses, find_default_translations, find_subreddit_in_request
from .response import Response

class VerseBot:
    """ Main VerseBot class. """

    def __init__(self):
        """ Initializes a VerseBot object with supplied username and password. It is recommended that
        the username and password are stored in something like an environment variable for security
        reasons. """
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger("versebot")
        logging.getLogger("requests").setLevel(logging.WARNING)
        self.log.info("Connecting to database...")
        self.d = database.Database()
        self.d.connect(self.log,'versebot.db')  # Initialize connection to database.
        self.log.info("Successfully connected to database!")
        try:
            self.log.info("Connecting to reddit...")
            self.r = praw.Reddit(user_agent = ("VerseBot by /u/mgrieger, running as Catebot. GitHub: https://github.com/konohitowa/versebot"))
            self.r.login(self.d.username(), self.d.password())
        except Exception as err:
            self.log.critical("Exception: %s", err) 
            self.log.critical("Connection to reddit failed. Exiting...")
            exit(1)
        self.log.info("Successfully connected to reddit!")
        self.parser = webparser.WebParser()  # Initialize web parser with updated translation list.
        self.log.info("Updating translation list table...")
        self.d.update_translation_list(self.parser.translations)
        self.log.info("Translation list update successful!")
        #self.log.info("Cleaning old user translation entries...")
        #self.d.clean_user_translations()
        #self.log.info("User translation cleaning successful!")

    def main_loop(self):
        """ Main inbox searching loop for finding verse quotation requests. """
        self.log.info("Beginning to scan for new  messages...")

        processedComments = list()
        print('Beginning to scan comments...')
        # This loop runs every 30 seconds.
        while True:
            processedComments = self.d.comments()
            subreddit_handle = self.r.get_subreddit(self.d.subreddits())
            subreddit_comments = subreddit_handle.get_comments()
            try:
                for comment in subreddit_comments:
                    if comment.author.name != self.d.username() and comment.id not in processedComments:
                        lines = re.split('\n',comment.body)
                        body = ""
                        for line in lines:
                            if not re.match(r'^\s{,3}>', line):
                                body += line + '\n'
                        comment.body = body
                        self.respond_to_username_mention(comment)
                        try:
                            self.d.add_comment(comment_id=comment.id,utc_time=int(time.time()))
                            self.log.info(comment.id+","+comment.author.name)
                        except:
                            print("insert failed")
                            self.log.error("Database insert failed. %s " % str(sys.exc_info()[0]))
                            exit()
            
            except requests.exceptions.HTTPError:
                print("HTTPError")
                self.log.info("HTTP Error: waiting 5 minutes to retry: %s " % str(sys.exc_info()[0]))
                sleep(5*60 - timeToWait)
            sleep(30)

    def respond_to_username_mention(self, message):
        """ Responds to a username mention. This could either contain one or more valid
        Bible verse quotation requests, or it could simply be a username mention without
        any valid Bible verses. If there are valid Bible verses, VerseBot generates a
        response that contains the text from these quotations. Otherwise, the message is
        forwarded to the VerseBot admin for review. """

        verses = find_verses(message.body)
        if verses is not None:
            response = Response(message, self.parser)
            for v in verses:
                book_name = books.get_book(v[0])
                if book_name is not None:
                    v2 = verse.Verse(self.d, # Database
                        book_name,  # Book
                        v[1],  # Chapter
                        v[3],  # Translation
                        message.author,  # User
                        message.permalink[24:message.permalink.find("/", 24)],  # Subreddit
                        v[2])  # Verse
                    if not response.is_duplicate_verse(v2):
                        response.add_verse(v2)
            if len(response.verse_list) != 0:
                message_response = response.construct_message()
                if message_response is not None:
                    self.log.info("Replying to %s with verse quotations..." % message.author)
                    try:
                        message.reply(message_response)
#                        self.d.update_db_stats(response.verse_list)
#                        self.d.increment_comment_count()
                    except praw.errors.Forbidden as err:
                        # This message is unreachable.
                        pass
                    except praw.errors.APIException as err:
                        if err.error_type in ("TOO_OLD", "DELETED_LINK", "DELETED_COMMENT"):
                            self.log.warning("An error occurred while replying with error_type %s." % err.error_type)

    def respond_to_edit_request(self, message):
        """ Responds to an edit request. The bot will parse the body of the message, looking for verse
        quotations. These will replace the quotations that were placed in the original response to the
        user. Once the comment has been successfully edited, the bot then sends a message to the user
        letting them know that their verse quotations have been updated. """

        try:
            comment_url = message.body[1:message.body.find("}")]
            comment = self.r.get_submission(comment_url)
        except:
            try:
                message.reply("An error occurred while processing your edit request. "
                    "Please make sure that you do not modify the subject line of your message to %s."
                    % REDDIT_USERNAME)
            except requests.exceptions.ConnectionError:
                pass
            return

        if message.author == comment.author and comment:
            verses = find_verses(message.body)
            if verses is not None:
                for reply in comment.comments[0].replies:
                    if str(reply.author) == REDDIT_USERNAME:
                        try:
                            self.log.info("%s has requested a comment edit..." % comment.author)
                            link = reply.permalink[24:comment.permalink.find("/", 24)]
                            response = Response(message, self.parser, comment_url)
                            for verse in verses:
                                book_name = books.get_book(verse[0])
                                if book_name is not None:
                                    v = verse.Verse(book_name,  # Book
                                        verse[1],  # Chapter
                                        verse[3],  # Translation
                                        message.author,  # User
                                        link,  # Subreddit
                                        verse[2])  # Verse
                                    if not response.is_duplicate_verse(v):
                                        response.add_verse(v)
                            if len(response.verse_list) != 0:
                                message_response = ("*^This ^comment ^has ^been ^edited ^by ^%s.*\n\n" % message.author)
                                message_response += response.construct_message()
                                if message_response is not None:
                                    self.log.info("Editing %s's comment with updated verse quotations..." % message.author)
                                    self.d.remove_invalid_statistics(reply.body, link)
                                    reply.edit(message_response)
                                    self.d.update_db_stats(response.verse_list)
                                    try:
                                        message.reply("[Your triggered %s response](%s) has been successfully edited to reflect"
                                            " your updated quotations." % (REDDIT_USERNAME, comment_url))
                                    except requests.exceptions.ConnectionError:
                                        pass
                                    break
                        except:
                            raise
                            self.log.warning("Comment edit failed. Will try again later...")
                            break

    def respond_to_delete_request(self, message):
        """ Responds to a delete request. The bot will attempt to open the comment which has been requested
        to be deleted. If the submitter of the delete request matches the author of the comment that triggered
        the VerseBot response, the comment will be deleted. The bot will then send a message to the user letting
        them know that their verse quotation comment has been removed. """

        try:
            comment_url = message.body[1:message.body.find("}")]
            comment = self.r.get_submission(comment_url)
        except:
            try:
                message.reply("An error occurred while processing your deletion request. "
                    "Please make sure that you do not modify the subject line of your message to %s."
                    % REDDIT_USERNAME)
            except requests.exceptions.ConnectionError:
                pass
            return

        if message.author == comment.author and comment:
            for reply in comment.comments[0].replies:
                if str(reply.author) == REDDIT_USERNAME:
                    try:
                        self.log.info("%s has requested a comment deletion..." % comment.author)
                        link = reply.permalink[24:comment.permalink.find("/", 24)]
                        self.d.remove_invalid_statistics(reply.body, link)
                        self.d.decrement_comment_count()
                        reply.delete()
                        self.log.info("%s's comment has been deleted." % comment.author)
                        try:
                            message.reply("%s's response to [your comment](%s) has been deleted. "
                                "Sorry for any inconvenience!" % (REDDIT_USERNAME, comment_url))
                        except requests.exceptions.ConnectionError:
                            pass
                        break
                    except:
                        self.log.warning("Comment deletion failed. Will try again later...")

    def respond_to_user_translation_request(self, message):
        """ Responds to a user's default translation request. The bot will parse the message which contains the
        desired translations, and will check them against the database to make sure they are valid. If they are
        valid, the bot will respond with a confirmation message and add the defaults to the user_translations table.
        If not valid, the bot will respond with an error message. """

        ot_trans, nt_trans, deut_trans = find_default_translations(message.body)
        if None not in (ot_trans, nt_trans, deut_trans):
            if (self.d.is_valid_translation(ot_trans, "Old Testament")
                and self.d.is_valid_translation(nt_trans, "New Testament")
                and self.d.is_valid_translation(deut_trans, "Deuterocanon")):
                self.d.update_user_translation(str(message.author), ot_trans, nt_trans, deut_trans)
                self.log.info("Updated default translations for %s." % message.author)
                try:
                    message.reply("Your default translations have been updated successfully!")
                except requests.exceptions.ConnectionError:
                    pass
            else:
                try:
                    message.reply("One or more of your translation choices is invalid. Please review your choices"
                        " and try again.")
                except requests.exceptions.ConnectionError:
                    pass
        else:
            try:
                message.reply("Your default translation request does not match the required format. Please do not edit"
                    " the message after generating it from the website.")
            except requests.exceptions.ConnectionError:
                pass


    def respond_to_subreddit_translation_request(self, message):
        """ Responds to a subreddit's default translation request. The bot will parse the message which contains the
        desired translations, and will check them against the database to make sure they are valid. If they are
        valid, the bot will respond with a confirmation message and add the defaults to the subreddit_translations table.
        If not valid, the bot will respond with an error message. """

        subreddit = find_subreddit_in_request(message.body)
        try:
            if message.author in self.r.get_moderators(subreddit):
                ot_trans, nt_trans, deut_trans = find_default_translations(message.body)
                if None not in (ot_trans, nt_trans, deut_trans):
                    if (self.d.is_valid_translation(ot_trans, "Old Testament")
                        and self.d.is_valid_translation(nt_trans, "New Testament")
                        and self.d.is_valid_translation(deut_trans, "Deuterocanon")):
                        self.d.update_subreddit_translation(subreddit, ot_trans, nt_trans, deut_trans)
                        self.log.info("Updated default translations for /r/%s." % subreddit)
                        try:
                            self.r.send_message("/r/%s" % subreddit, "/r/%s Default Translation Change Confirmation" % subreddit,
                                "The default /u/%s translation for this subreddit has been changed by /u/%s to the following:\n\n"
                                "Old Testament: %s\nNew Testament: %s\nDeuterocanon: %s\n\nIf this is a mistake,"
                                " please [click here](http://matthieugrieger.com/versebot#subreddit-translation-default)"
                                " to submit a new request." % (REDDIT_USERNAME, str(message.author), ot_trans, nt_trans,
                                deut_trans))
                        except requests.exceptions.ConnectionError:
                            pass
                    else:
                        try:
                            message.reply("One or more of your translation choices is invalid. Please review your choices"
                            " and try again.")
                        except requests.exceptions.ConnectionError:
                            pass
                else:
                    try:
                        message.reply("Your default translation request does not match the required format. Please do not edit"
                        " the message after generating it from the website.")
                    except requests.exceptions.ConnectionError:
                        pass
        except requests.exceptions.HTTPError as err:
            if str(err) == "404 Client Error: Not Found":
                try:
                    message.reply("The subreddit you entered (/r/%s) does not exist or is private." % subreddit)
                except requests.exceptions.ConnectionError:
                    pass
        except praw.errors.RedirectException:
            try:
                message.reply("The subreddit you entered (/r/%s) does not exist or is private." % subreddit)
            except requests.exceptions.ConnectionError:
                pass
