# -*- coding: utf-8 -*-
from .pluginbase import PluginBase

import datetime

class Week(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!week", self.handleWeek)
		bot.registerCommand("!vecka", self.handleWeek)
		bot.addHelp("week", "Usage: !week")

	def handleWeek(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel, "Week: %s" %
				(datetime.datetime.now().strftime("%V")))

mainclass = Week
