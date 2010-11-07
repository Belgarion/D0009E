# -*- coding: utf-8 -*-
from pluginbase import PluginBase

import urllib2
import re

class Title(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!title", self.handleTitle)
		bot.addHelp("title", "Usage: !title <url>")

	def handleTitle(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel, self.getTitle("%20".join(params)))

	def getTitle(self, url):
		try:
			f = urllib2.urlopen(url)
			data = f.read()
			f.close()
		except urllib2.HTTPException, e:
			return e

		m = re.search("<title>\n?(.*)\n?</title>", data)
		if m:
			return m.group(1)
		return "Title not found"

mainclass = Title
