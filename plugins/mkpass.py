# -*- coding: utf-8 -*-
from .pluginbase import PluginBase

import random
import string

class MkPass(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!mkpass", self.handleMkPass)
		bot.addHelp("mkpass", "Usage: !mkpass <number of characters>")

	def handleMkPass(self, bot, channel, params):
		pwlen = int(params[0])
		if pwlen > 256:
			bot.sendMessage("PRIVMSG", channel,
				"No one should need a password that long!")
			return

		pw = ""
		while pwlen > 0:
			if pwlen > 32:
				pw += "".join(random.sample(string.ascii_letters + string.digits, 32))
				pwlen -= 32
			else:
				pw += "".join(random.sample(string.ascii_letters + string.digits, pwlen))
				pwlen = 0

		bot.sendMessage("PRIVMSG", channel, pw)

mainclass = MkPass
