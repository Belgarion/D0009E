# -*- encoding: utf-8 -*-

from pluginbase import PluginBase

class AAO(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!åäö", self.utf8)
		bot.registerCommand("!\xe5\xe4\xf6", self.latin1)

	def utf8(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel, "UTF-8 :)")

	def latin1(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel, "Latin1 :(")

mainclass = AAO
