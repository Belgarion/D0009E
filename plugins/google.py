# -*- coding: utf-8 -*-
from pluginbase import PluginBase

import urllib
from urllib import FancyURLopener
import random
import re

class UrlOpener(FancyURLopener):
	version = "D0009E/0.1"

class Google(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!google", self.handleGoogle)
		bot.addHelp("google", "Usage: !google search terms")

	def handleGoogle(self, bot, channel, params):
		url = "http://www.google.se/search?q=%s&ie=utf-8&oe=utf-8&rls=en" % \
				(urllib.quote_plus(" ".join(params)))

		try:
			file = UrlOpener().open(url)
		except IOError:
			bot.sendMessage("PRIVMSG", channel, "Error opening url.")
			return

		data = file.read(1024*1024)
		file.close()

		print data
		print "----"

		m = re.search('<h3 class="r"><a href="(.*?)".*?>(.*?)<\/a>', data)
		if m:
			print m.groups()
			title = re.sub('<.+?>', '', m.group(2))
			bot.sendMessage("PRIVMSG", channel, "%s [%s]" % (title, m.group(1)))
		else:
			bot.sendMessage("PRIVMSG", channel, url)

mainclass = Google
