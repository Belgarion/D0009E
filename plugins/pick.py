# -*- coding: utf-8 -*-
from .pluginbase import PluginBase
import traceback
import random

class Names(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!pick", self.handlePick)
		bot.addHelp("pick", "Usage: !pick thingy1 || thingy2")

	def handlePick(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel,
				random.choice(" ".join(params).split("||")))

mainclass = Names
