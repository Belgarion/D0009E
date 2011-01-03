# -*- encoding: utf-8 -*-

from pluginbase import PluginBase

import time
import datetime

class Xmas(PluginBase):
	def __init__(self, bot):
		bot.lastChristmasMsg = 0

	def on_tick(self, bot):
		tm = time.localtime()
		if tm.tm_mon != 12 or tm.tm_mday > 24:
			return

		hour = tm.tm_hour
		if time.time() - bot.lastChristmasMsg > 23*60*60 and hour == 00:
			bot.lastChristmasMsg = time.time()

			xmasTime = datetime.datetime(2010, 12, 24, 23, 59,59)
			nowTime = datetime.datetime.today()
			diff = xmasTime - nowTime

			for i in bot.plugins:
				if i.__class__.__name__ == "Talking":
					talking = i
					break

			for chan in bot.channels.keys():
				talking.talk(bot, chan, [])
				bot.sendMessage("PRIVMSG", chan,
						"och btw, det är %s dagar kvar till jul" % \
								(diff.days))


mainclass = Xmas
