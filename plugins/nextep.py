# -*- coding: utf-8 -*-
from .pluginbase import PluginBase

import urllib.request, urllib.error, urllib.parse

class NextEp(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!nextep", self.handleNextEp)
		bot.addHelp("nextep", "Usage: !nextep <show>")

	def handleNextEp(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel, self.nextep("%20".join(params)))

	def nextep(self, show):
		try:
			f = urllib.request.urlopen(
				"http://services.tvrage.com/tools/quickinfo.php?show=%s" % show)
			data = f.read()
			f.close()
		except urllib2.HTTPException as e:
			return e

		name = "Not found"
		year = "N/A"
		nextep = "N/A"
		lastep = "N/A"
		for line in data.split("\n"):
			if "Show Name" in line:
				name = line.split("@")[1]
			if "Premiered" in line:
                                year = line.split("@")[1]
			if "Next Episode" in line:
				nextep = ", ".join(line.split("@")[1].split("^"))
			if "Latest Episode" in line:
                                lastep = ", ".join(line.split("@")[1].split("^"))


		return "%s (%s) - Next episode: %s - Last episode: %s" % (name, year, nextep, lastep)

mainclass = NextEp
