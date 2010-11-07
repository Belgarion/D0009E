# -*- coding: utf-8 -*-
from pluginbase import PluginBase

import urllib2
import time
import re

class Lunch(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!lunch", self.handleLunch)
		bot.addHelp("lunch", "Lunch @ STUK")

	def handleLunch(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel, self.getLunch(" ".join(params)))

	def getLunch(self, place = ""):
		tm = time.localtime()
		weekdays = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag",
			"Lördag", "Söndag"]
		wday = tm.tm_wday

		mday = tm.tm_mday
		if tm.tm_hour >= 13:
			wday += 1
			mday += 1

		dateString = "%s %s/%s" % (weekdays[wday % 7], mday, tm.tm_mon)

		try:
			f = urllib2.urlopen("http://stuk.nu/lunch.aspx?menuID=11")
			data = f.read()
			data = data.replace("&nbsp;", " ")
			data = data.replace("\r", "")
			data = data.replace("<BR>", "\n")
			f.close()
		except urllib2.HTTPExceptionl, e:
			return e

		buf = "Lunch @ Stuk: "

		found = 0
		for line in data.split("\n"):
			line = re.sub(r'<[^>]+>', "", line)
			if not line:
				continue

			if dateString in line:
				buf += "%s: " % (line.strip())
				found = 1
				continue

			if found > 0:
				buf += line
				if found < 2:
					buf += ", "
				found += 1

			if found > 2:
				break

		return buf

mainclass = Lunch
