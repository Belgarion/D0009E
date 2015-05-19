# -*- encoding: utf-8 -*-

from .pluginbase import PluginBase

class AAO(PluginBase):
	def __init__(self, bot):
		bot.registerByteCommand("!åäö".encode(), self.utf8)
		bot.registerByteCommand(b"!\xe5\xe4\xf6", self.latin1)

	def utf8(self, bot, channel, params):
		bot.sendByteMessage(b"PRIVMSG", channel, b"UTF-8 :)")

	def latin1(self, bot, channel, params):
		bot.sendByteMessage(b"PRIVMSG", channel, b"Latin1 :(")

mainclass = AAO
