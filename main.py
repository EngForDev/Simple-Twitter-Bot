#!/usr/bin/env python
#! -*- coding: utf-8 -*-

from appengine_twitter import AppEngineTwitter
from basehandler import BaseHandler, h
import twitter
 
# twitter.Api.__init__ method for override.
def twitter_api_init_gae(self,
                       username=None,
                       password=None,
                       input_encoding=None,
                       request_headers=None):
   import urllib2
   from twitter import Api
   self._cache = None

   self._urllib = urllib2
   self._cache_timeout = Api.DEFAULT_CACHE_TIMEOUT
   self._InitializeRequestHeaders(request_headers)
   self._InitializeUserAgent()
   self._InitializeDefaultParameters()
   self._input_encoding = input_encoding
   self.SetCredentials(username, password)

def run(name, pswd, search_term):
   gae_twitter = AppEngineTwitter(name, pswd)
   results = gae_twitter.search(search_term.encode('utf8'), {'rpp': 20})
   api = twitter.Api(username=bot_username, password=bot_password)

   # Get most corrently tweeted tweet
   status = api.GetUserTimeline()
   
   for s in status:
      if s.text.startswith("RT"):
         recent_tweet = s.text
         break
      else:
         print "The following tweet would be posted by hand, so skipped it."
         print "Tweet: " + s.text.encode('utf8')
         print
      
   print "Recent Tweet: "+recent_tweet.encode('utf8')
   print

   # Search Most Recent Tweet
   results.reverse()
   flag_enable = 0
   for i,result in enumerate(results):
      rt = "RT @" + result['from_user']  + " " + result['text']
      rt_len = len(rt)
      if flag_enable and result['from_user'] != bot_username and rt_len<MAX_LEN:
         """
         Retweet and exit
         """
         print "Re-tweet: "+rt.encode('utf8')
         print "Re-tweet Result: " + str(gae_twitter.update(rt.encode('utf8')))
         exit()
               
      if recent_tweet == rt:
         flag_enable = 1

   if flag_enable:
      print "There are no tweet found that I should tweet."
      exit()
      
   print "There are no tweets recently tweeted, so tweet the oldest tweet."
   result = results[0]
   rt = "RT @" + result['from_user']  + " " + result['text']
   rt_len = len(rt)
   print "Re-tweet: "+rt.encode('utf8')
   print "Re-tweet Result: " + str(gae_twitter.update(rt.encode('utf8')))
   exit()
   
# overriding API __init__
twitter.Api.__init__ = twitter_api_init_gae

# User Setting and Run Twitter Bot
bot_username = 'CafeMiyamaBot'
bot_password = '???'
br = "<br>"
MAX_LEN = 140
search_term = u'Cafe Miyama'
run(bot_username, bot_password, search_term)