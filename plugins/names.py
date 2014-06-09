# -*- coding: utf-8 -*-
from .pluginbase import PluginBase
import traceback
import random

class Names(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!names", self.handleNames)
		bot.registerCommand("!randnick", self.handleRandNick)

	def handleNames(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel,
				" ".join(bot.channels[channel.upper()].names))

	def handleRandNick(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel,
				random.choice(bot.channels[channel.upper()].names))

mainclass = Names
