# -*- coding: utf-8 -*-
from pluginbase import PluginBase

import traceback
import time
import twitter

class TwitterReader(PluginBase):
	def __init__(self, bot):
		pass

	def on_tick(self, bot):
		if time.time() - bot.lastTwitterCheck > 60:
			bot.lastTwitterCheck = time.time()
			try:
				self.handleTwitter(bot, "#brokenbrain", [])
			except:
				traceback.print_exc()

	def handleTwitter(self, bot, channel, params):
		api = twitter.Api()
		statuses = api.GetUserTimeline("baldos")
		if len(statuses) == 0:
			return

		msgs = ["@baldos: " + s.text for s in statuses if s.created_at_in_seconds > bot.lastTwitterStatusTime][:2]
		msgs.reverse()
		bot.lastTwitterStatusTime = statuses[0].created_at_in_seconds

		if len(msgs) > 0:
			bot.sendMessage("PRIVMSG", channel, msgs)


mainclass = TwitterReader

