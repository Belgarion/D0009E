# -*- coding: utf-8 -*-
from pluginbase import PluginBase

import time

class Others(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!echo", self.handleEcho)
		bot.registerCommand("!ping", self.handlePing)
		bot.registerCommand("!time", self.handleTime)
		bot.registerCommand("!zzz", self.handleZZZ)
		bot.addHelp("echo", "Usage: !echo <arguments>")
		bot.addHelp("time", "Prints current time")
		bot.addHelp("!ping", "Pong")

	def handleEcho(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel, " ".join(params))

	def handleTime(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel, time.ctime())

	def handlePing(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel, "PONG")

	def handleZZZ(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel, "I'm a bot, I don't sleep!")

mainclass = Others
