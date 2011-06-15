# -*- coding: utf-8 -*-
from pluginbase import PluginBase

import httplib
import random
import re

class Temp(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!temp", self.handleTemp)
		bot.registerCommand("!temperatur", self.handleTemp)
		bot.registerCommand("!temperature", self.handleTemp)
		bot.addHelp("temp", "Usage: !temp [location]")

	def handleTemp(self, bot, channel, params):
		temperature = -273.15

		if params:
			city = ""
			temperature = ""

			for f in [self.specialtemp, self.temperaturnu, \
					self.googleweather, self.errortemp]:
				if f(bot, channel, params):
					break
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

	def specialtemp(self, bot, channel, params):
		temp = None
		if params[0] == "special":
			temp = "Too hot"
		elif params[0] == "serverrum":
			conn = httplib.HTTPConnection("graphs.se")
			conn.request("GET", "/serverrum.txt")
			resp = conn.getresponse()
			data = resp.read()
			temp = data

		if temp:
			bot.sendMessage("PRIVMSG", channel,
					"Temperature in %s: %s" % (params[0], temp))
			return True

		return False

	def temperaturnu(self, bot, channel, params):
		return False
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
			return False

		return True

	def googleweather(self, bot, channel, params):
		city = ""
		temperature = ""
		humidity = ""

		try:
			conn = httplib.HTTPConnection("www.google.com")
			conn.request("GET", "/ig/api?weather=%s" % params[0])
			resp = conn.getresponse()
			data = resp.read()

			data = data.replace(">",">\n")
			lines = data.split("\n")
			for line in lines:
				m = re.match(r'\s*<city data="(.*)"/>', line)
				if m:
					city = m.groups(1)[0]

				m = re.match(r'\s*<temp_c data="(.*)"/>', line)
				if m:
					temperature = m.groups(1)[0]

				m = re.match(r'\s*<humidity data="(.*)"/>', line)
				if m:
					humidity = m.groups(1)[0]

			if not temperature or not city:
				raise ValueError

			bot.sendMessage("PRIVMSG", channel,
					"Temperature in %s: %s degrees Celsius, %s" % \
							(city, temperature, humidity))
		except Exception, e:
			return False

		return True

	def errortemp(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel,
				"Error getting temperature in %s, but I'm guessing it's"
				" %s degrees Celcius" % (params[0], random.randint(-40,60)))
		return True

mainclass = Temp
