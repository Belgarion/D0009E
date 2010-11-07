# -*- coding: utf-8 -*-
from pluginbase import PluginBase

import httplib

class Temp(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!temp", self.handleTemp)
		bot.registerCommand("!temperatur", self.handleTemp)
		bot.registerCommand("!temperature", self.handleTemp)
		bot.addHelp("temp", "Usage: !temp [city]")

	def handleTemp(self, bot, channel, params):
		temperature = -273.15

		if params:
			city = ""
			temperature = ""

			conn = httplib.HTTPConnection("wap.temperatur.nu")
			conn.request("GET", "/%s" % params[0])
			resp = conn.getresponse()
			data = resp.read()

			lines = data.split("\n")
			for line in lines:
				if "Temp:" in line:
					temperature, datetime, city = \
							[i.strip('</p>') for i in line.split('<p>')]
					break

			bot.sendMessage("PRIVMSG", channel,
					"Temperature in %s: %s" % (city, temperature))
			return

		conn = httplib.HTTPConnection("marge.campus.ltu.se")
		conn.request("GET", "/temp/")
		resp = conn.getresponse()
		data = resp.read()

		lines = data.split("\n")
		for line in lines:
			if "Current temperature" in line:
				temperature = ("%s" % (" ".join(line.split()[5:8])))
				break

		bot.sendMessage("PRIVMSG", channel, "Temperature: %s" %
				(temperature))

mainclass = Temp
