# -*- coding: utf-8 -*-
from pluginbase import PluginBase

import urllib2

class NextEp(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!nextep", self.handleNextEp)
		bot.addHelp("nextep", "Usage: !nextep <show>")

	def handleNextEp(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel, self.nextep("%20".join(params)))

	def nextep(self, show):
		try:
			f = urllib2.urlopen(
				"http://services.tvrage.com/tools/quickinfo.php?show=%s" % show)
			data = f.read()
			f.close()
		except urllib2.HTTPException, e:
			return e

		name = "Not found"
		nextep = "No info"
		for line in data.split("\n"):
			if "Show Name" in line:
				name = line.split("@")[1]
			if "Next Episode" in line:
				nextep = ", ".join(line.split("@")[1].split("^"))

		return "%s: Next episode: %s" % (name, nextep)

mainclass = NextEp
