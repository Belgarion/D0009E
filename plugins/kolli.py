# -*- coding: utf-8 -*-
from .pluginbase import PluginBase

import http.client
import re

class Kolli(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!kolli", self.postenKolli)
		bot.registerCommand("!paket", self.postenKolli)
		bot.registerCommand("!posten", self.postenKolli)
		bot.addHelp("kolli", "Usage: !kolli [kolli-id]")

	def postenKolli(self, bot, channel, params):
		if len(params) < 1:
			bot.sendMessage("PRIVMSG", channel, "Something went wronk...")
			return

		conn = http.client.HTTPConnection("posten.se")
		conn.request("GET", "/tracktrace/TrackConsignments_do.jsp?trackntraceAction=saveSearch&consignmentId=%s" % params[0])
		resp = conn.getresponse()
		data = resp.read().decode('iso-8859-1')
		url = 'http://posten.se/tracktrace/TrackConsignments_do.jsp?trackntraceAction=saveSearch&consignmentId=%s' % params[0]

		search = re.search('(?ims)<dt>Fr&aring;n:</dt><dd>(.*?)</dd>.*?rightcol.*h2>.*<h3>(.*?)</h3>\s*?(.*?)(<br/>|<div).*?<dt>Vikt:</dt><dd>(.*?)</dd>', data)

		if search:
			sender = search.group(1)
			date = search.group(2)
			status = search.group(3)
			weight = search.group(5)

			if date and status:
				result = "%s fr\xe5n %s | %s: %s | %s" % (weight, sender, date, re.sub("<.+?>", "", status), url)
				bot.sendMessage("PRIVMSG", channel, result)
			else:
				bot.sendMessage("PRIVMSG", channel, "Something went wronk...")
		else:
			bot.sendMessage("PRIVMSG", channel, "No package for you!")

mainclass = Kolli
