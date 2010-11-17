# -*- coding: utf-8 -*-
from pluginbase import PluginBase

import httplib
import time
import traceback

class Forecast(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!forecast", self.handleForecast)
		bot.addHelp("forecast", "Usage: !forecast")

	def on_tick(self, bot):
		hour = time.localtime().tm_hour
		if time.time() - bot.lastForecast > 7200 and \
				(hour == 5 or hour == 11 or hour == 17 or hour == 23):
			bot.lastForecast = time.time()
			try:
				self.handleForecast(bot, "#ltudata2010", [])
				self.handleForecast(bot, "#datasektionen", [])
			except:
				traceback.print_exc()

	def handleForecast(self, bot, channel, params):
		title = ""
		description = ""

		conn = httplib.HTTPConnection("www.yr.no")
		path = "/place/Sweden/Norrbotten/Lule%C3%A5/forecast.rss"
		conn.request("GET", path)
		resp = conn.getresponse()
		data = resp.read()

		lines = data.split("\n")
		lines = [i.strip("\r\n").strip() for i in lines]

		inItem = False
		for line in lines:
			if "<item>" in line:
				inItem = True
				continue

			if not inItem: continue

			if "<title>" in line:
				title = line
				title = title.replace("title>", "")
				title = title.replace("</", "")
				title = title.replace("<", "")
				continue

			if "<description>" in line:
				description = line
				description = description.replace("description>", "")
				description = description.replace("</", "")
				description = description.replace("<", "")
				continue

			if "</item>" in line:
				inItem = False
				break

		bot.sendMessage("PRIVMSG", channel, "Forecast: %s: %s" %
				(title, description))


mainclass = Forecast

