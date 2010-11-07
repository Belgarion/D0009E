# -*- coding: utf-8 -*-
from pluginbase import PluginBase

class Help(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!help", self.handleHelp)
		bot.addHelp("help", "Usasge: !help [command]")

	def handleHelp(self, bot, channel, params):
		if len(params) >= 1:
			if params[0] in bot.help:
				bot.sendMessage("PRIVMSG", channel, bot.help[params[0]])
			else:
				bot.sendMessage("PRIVMSG", channel, "No help for: %s" % params[0])
		else:
			bot.sendMessage("PRIVMSG", channel, ", ".join(bot.help.keys()))

mainclass = Help
