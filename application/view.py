#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webapp2
from webapp2_extras import sessions
from google.appengine.ext import db
from jinja2 import Environment, FileSystemLoader

import os
import binascii
from random import randint

from model import Tweet
from wakametter import Wakametter
from setting import *

##############################################################################
#
# Base Handler
#
##############################################################################

class BaseHandler(webapp2.RequestHandler):
    def render(self, template_file, template_values = {}):
        """ Render HTML of template file by Jinja2 """
        env = Environment(
            loader = FileSystemLoader(TEMPLATE_DIR, encoding = CHAR_SET),
            autoescape = False
            )
        template = env.get_template(template_file)
        html = template.render(template_values)

        self.response.write(html)

    def dispatch(self):
        self.session_store = sessions.get_store(request = self.request)

        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        backend = self.session_store.config.get("default_backend", "securecookie")
        return self.session_store.get_session(backend = backend)


##############################################################################
#
# Home View
#
##############################################################################

class HomeHandler(BaseHandler):
    def get(self):
        # Make new session when there is no session.
        if not self.session.get("user"):
            new_id = binascii.hexlify(os.urandom(8))
            me     = Wakametter(ACCESS["key"], ACCESS["secret"]).me
            
            self.session["user"] = {"id"  : new_id,
                                    "name": me.screen_name,
                                    "icon": me.profile_image_url
                                    }

        # Get User
        user = self.session.get("user")

        # Get texts of twitter-bot
        query = Tweet.all().order("-date")
        tweets = query.fetch(query.count())

        # Render
        template_values = { "user_name": user["name"],
                            "icon_src" : user["icon"],
                            "tweets"   : tweets
                            }
        self.render("home.html", template_values)


##############################################################################
#
# Add Bot Handler
#
##############################################################################

class AddBotHandler(BaseHandler):
    def post(self):
        # Save new text of twitter-bot
        new_tweet = Tweet(text = self.request.get("text"))
        new_tweet.put()

        self.redirect("/")


##############################################################################
#
# Remove Bot Handler
#
##############################################################################

class RemoveBotHandler(BaseHandler):
    def post(self):
        # Get selected texts
        tweet_ids = self.request.get("tweet", allow_multiple = True)

        # Delete text of twitter-bot from DataBase
        delete_tweets = []
        for id in tweet_ids:
            tweet = Tweet.get_by_id(int(id))
            delete_tweets.append(tweet)
        db.delete(delete_tweets)

        self.redirect("/")


##############################################################################
#
# Post Tweet Handler
#
##############################################################################
class PostTweetHandler(BaseHandler):
    def get(self):
        # Get text chosen randomly from DataBase
        query = Tweet.all()
        tweets = query.fetch(query.count())
        tweet = tweets[randint(0, query.count() - 1)]

        # Tweet the text
        wkm = Wakametter(ACCESS["key"], ACCESS["secret"])
        wkm.tweet(tweet.text)
            

##############################################################################
#
# Application
#
##############################################################################

handlers = [
    ("/", HomeHandler),
    ("/add", AddBotHandler),
    ("/remove", RemoveBotHandler),
    ("/post", PostTweetHandler),
    ]

config = { "webapp2_extras.sessions": SESSION_CONFIG }

app = webapp2.WSGIApplication(
    handlers,
    debug = True,
    config = config,
    )
