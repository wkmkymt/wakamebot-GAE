#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy

from setting import CONSUMER

class Wakametter(object):
    def __init__(self, access_key, access_secret):
        self.auth = None
        self.api  = None
        self.me   = None

        self.auth = tweepy.OAuthHandler(CONSUMER["key"], CONSUMER["secret"])
        self.auth.set_access_token(access_key, access_secret)
        self.api = tweepy.API(self.auth)
        self.me = self.api.me()

    def tweet(self, post):
        self.api.update_status(post.encode("utf-8"))
