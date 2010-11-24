# -*- coding: utf-8 -*-
from pluginbase import PluginBase

import httplib
import random

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

			try:
				conn = httplib.HTTPConnection("wap.temperatur.nu")
				conn.request("GET", "/%s" % params[0].lower().replace("å","a").
						replace("ä", "a").replace("ö", "o"))
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
			except Exception, e:
				bot.sendMessage("PRIVMSG", channel,
						"Error getting temperature in %s, but I'm guessing it's"
						" %s degrees Celcius" % (params[0], random.randint(-40,60)))
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
