# -*- coding: utf-8 -*-
from .pluginbase import PluginBase

import traceback
import time
import twitter

class TwitterReader(PluginBase):
	def __init__(self, bot):
		pass

	def handleNewConfig(self):
		self.lastTwitterCheck = float(self.getConfig("lastTwitterCheck", '0'))
		self.lastTwitterStatusTime = float(self.getConfig("lastTwitterStatusTime", '0'))
		self.twitterChannels = self.getConfig("channels", "").split()

	def on_tick(self, bot):
		if time.time() - self.lastTwitterCheck > 300:
			self.lastTwitterCheck = time.time()
			self.updateConfig("lastTwitterCheck", str(self.lastTwitterCheck))
			try:
				for channel in self.twitterChannels:
					self.handleTwitter(bot, channel, [])
			except:
				traceback.print_exc()

	def handleTwitter(self, bot, channel, params):
		api = twitter.Api()
		statuses = api.GetUserTimeline("baldos")
		if len(statuses) == 0:
			return

		msgs = ["@baldos: " + s.text.encode('utf8') for s in statuses if s.created_at_in_seconds > self.lastTwitterStatusTime][:2]
		msgs.reverse()
		self.lastTwitterStatusTime = statuses[0].created_at_in_seconds
		self.updateConfig("lastTwitterStatusTime", str(self.lastTwitterStatusTime))

		if len(msgs) > 0:
			bot.sendMessage("PRIVMSG", channel, msgs)


mainclass = TwitterReader

