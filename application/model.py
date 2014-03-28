# -*- coding: utf-8 -*-

from google.appengine.ext import db

##############################################################################
#
# Data Models
#
##############################################################################

class Tweet(db.Model):
    text = db.StringProperty(multiline = True)
    date = db.DateTimeProperty(auto_now_add = True)
