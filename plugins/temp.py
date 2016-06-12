# -*- coding: utf-8 -*-
from .pluginbase import PluginBase

import http.client
import random
import re
import json
import traceback
import urllib.parse

class Temp(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!temp", self.handleTemp)
		bot.registerCommand("!temperatur", self.handleTemp)
		bot.registerCommand("!temperature", self.handleTemp)
		bot.addHelp("temp", "Usage: !temp [location]")

	def handleNewConfig(self):
		self.apikey = self.getConfig("apikey")

	def handleTemp(self, bot, channel, params):
		temperature = -273.15

		if params:
			city = ""
			temperature = ""

			for f in [self.ludd, self.specialtemp, self.temperaturnu, \
					self.googleweather, self.errortemp]:
				if f(bot, channel, params):
					break
			return

		conn = http.client.HTTPSConnection("temp.campus.ltu.se")
		conn.request("GET", "/temp_outside.php")
		resp = conn.getresponse()
		data = resp.read().decode('utf-8')
		bot.sendMessage("PRIVMSG", channel, "Temperature: %s°C" % (data))

	def specialtemp(self, bot, channel, params):
		temp = None
		if params[0] == "special":
			temp = "Too hot"
		elif params[0] == "serverrum":
			conn = http.client.HTTPConnection("graphs.se")
			conn.request("GET", "/serverrum.txt")
			resp = conn.getresponse()
			data = resp.read().decode('utf-8')
			conn.close()
			temp = data

		if temp:
			bot.sendMessage("PRIVMSG", channel,
					"Temperature in %s: %s" % (params[0], temp))
			return True

		return False

	def temperaturnu(self, bot, channel, params):
		try:
			conn = http.client.HTTPConnection("wap.temperatur.nu")
			conn.request("GET", "/%s" % params[0].lower().replace("å","a").
					replace("ä", "a").replace("ö", "o"))
			resp = conn.getresponse()
			data = resp.read().decode('iso-8859-1')
			conn.close()

			lines = data.split("\n")
			for line in lines:
				if "Temp:" in line:
					temperature, datetime, city = \
							[i.strip('</p>') for i in line.split('<p>')]
					break
			else:
				print("Temperatur.nu no Temp: line found.")
				return False

			bot.sendMessage("PRIVMSG", channel,
					"Temperature in %s: %s" % (city, temperature))
		except Exception as e:
			traceback.print_exc()
			print("Temperaturnu failed")
			return False

		return True

	def googleweather(self, bot, channel, params):
		city = ""
		temperature = ""

		try:
			conn = http.client.HTTPConnection("api.openweathermap.org")
			conn.request("GET", "/data/2.5/weather?mode=json&units=metric&q=%s&APPID=%s" % (urllib.parse.quote(" ".join(params)), self.apikey))
			resp = conn.getresponse()
			data = resp.read().decode('utf-8')
			conn.close()

			print(data)
			decoded_openweathermap = json.loads(data)
			city = decoded_openweathermap['name']
			temperature = decoded_openweathermap['main']['temp']

			if city == '':
					city = decoded_openweathermap['sys']['country']

			if not temperature or not city:
				raise ValueError

			bot.sendMessage("PRIVMSG", channel,
					"Temperature in %s: %s degrees Celsius" % \
							(city, temperature))
		except Exception as e:
			traceback.print_exc()
			print("googleweather failed")
			return False

		return True

	def ludd(self, bot, channel, params):
		if params[0] == 'dh1':
			conn = http.client.HTTPSConnection("netmon.se")
			conn.request("GET", "/api/csv/16/ludd/temperature?name=dh1&interval=600")
			resp = conn.getresponse()
			data = resp.read().decode('utf-8')
			conn.close()
			temp = None
			header = None
			for line in data.split("\r\n"):
				if not header:
					header = line.split(",")
					continue
				t = line.split(",")
				if len(t)>1 and not t[1] == "NaN":
					temp = t[1]

			if temp:
				bot.sendMessage("PRIVMSG", channel,
						"Temperature in %s: %s" % (params[0], temp))
			else:
				bot.sendMessage("PRIVMSG", channel,
						"Unable to get temperature in %s", params[0])
			return True
		elif params[0] == 'dh2':
			conn = http.client.HTTPSConnection("netmon.se")
			conn.request("GET", "/api/csv/16/ludd/temperature?name=dh2&interval=600")
			resp = conn.getresponse()
			data = resp.read().decode('utf-8')
			conn.close()
			temp = None
			header = None
			for line in data.split("\r\n"):
				if not header:
					header = line.split(",")
					continue
				t = line.split(",")
				if len(t)>1 and not t[1] == "NaN":
					temp = t[1]

			if temp:
				bot.sendMessage("PRIVMSG", channel,
						"Temperature in %s: %s" % (params[0], temp))
			else:
				bot.sendMessage("PRIVMSG", channel,
						"Unable to get temperature in %s", params[0])
			return True
		elif params[0] == 'dh2-lc':
			conn = http.client.HTTPSConnection("netmon.se")
			conn.request("GET", "/api/csv/16/ludd/temperature?name=dh2lc&interval=600")
			resp = conn.getresponse()
			data = resp.read().decode('utf-8')
			conn.close()
			temp = None
			header = None
			for line in data.split("\r\n"):
				if not header:
					header = line.split(",")
					continue
				t = line.split(",")
				if len(t)>1 and not t[1] == "NaN":
					temp = t[1]

			if temp:
				bot.sendMessage("PRIVMSG", channel,
						"Temperature in %s: %s" % (params[0], temp))
			else:
				bot.sendMessage("PRIVMSG", channel,
						"Unable to get temperature in %s", params[0])
			return True
		return False

	def errortemp(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel,
				"Error getting temperature in %s, but I'm guessing it's"
				" %s degrees Celcius" % (" ".join(params), random.randint(-40,60)))
		return True

mainclass = Temp
