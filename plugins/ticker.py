# -*- coding: utf-8 -*-
# This 'Fulhack' is made by ElectricMan, hello@electricman.se
from pluginbase import PluginBase

import httplib
import json

class Ticker(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!ticker", self.handleTicker)
		bot.registerCommand("!btc", self.handleBTC)
		bot.registerCommand("!ltc", self.handleLTC)

		bot.addHelp("ticker", "Displays current exchange rates for Bitcoin and Litecoin from BTC-e")
		bot.addHelp("btc", "Displays current Bitcoin exchange rate from BTC-e")
		bot.addHelp("ltc", "Displays current Litecoin exchange rate from BTC-e")

	def handleTicker(self, bot, channel, params):
		try:
			conn = httplib.HTTPSConnection("btc-e.com")
			conn.request("GET", "/api/2/btc_usd/ticker")
			resp = conn.getresponse()
			data_btc = resp.read()

			decoded_btc_usd = json.loads(data_btc)
			btc_usd = round(decoded_btc_usd['ticker']['last'], 2)

			conn = httplib.HTTPSConnection("btc-e.com")
			conn.request("GET", "/api/2/ltc_usd/ticker")
			resp = conn.getresponse()
			data_ltc = resp.read()

			decoded_ltc_usd = json.loads(data_ltc)
			ltc_usd = round(decoded_ltc_usd['ticker']['last'], 2)

			bot.sendMessage("PRIVMSG", channel,	"LTC: %s USD -  BTC: %s USD" % (ltc_usd, btc_usd))

		except:
			bot.sendMessage("PRIVMSG", channel, "Something went wrong...")

	def handleBTC(self, bot, channel, params):
		try:
			conn = httplib.HTTPSConnection("btc-e.com")
			conn.request("GET", "/api/2/btc_usd/ticker")
			resp = conn.getresponse()
			data_btc = resp.read()

			decoded_btc_usd = json.loads(data_btc)

			btc_usd = round(decoded_btc_usd['ticker']['last'], 2)
			btc_usd_low = round(decoded_btc_usd['ticker']['low'], 2)
			btc_usd_high = round(decoded_btc_usd['ticker']['high'], 2)
			btc_usd_avg = round(decoded_btc_usd['ticker']['avg'], 2)

			bot.sendMessage("PRIVMSG", channel,	"BTC/USD: Last %s USD, High %s USD, Low %s USD, Average %s USD" % (btc_usd, btc_usd_high, btc_usd_low, btc_usd_avg))

		except:
			bot.sendMessage("PRIVMSG", channel, "BTC is going to tha moooooon! (No, something went wrong...)")

	def handleLTC(self, bot, channel, params):
		try:
			conn = httplib.HTTPSConnection("btc-e.com")
			conn.request("GET", "/api/2/ltc_usd/ticker")
			resp = conn.getresponse()
			data_ltc = resp.read()

			decoded_ltc_usd = json.loads(data_ltc)

			ltc_usd = round(decoded_ltc_usd['ticker']['last'], 2)
			ltc_usd_low = round(decoded_ltc_usd['ticker']['low'], 2)
			ltc_usd_high = round(decoded_ltc_usd['ticker']['high'], 2)
			ltc_usd_avg = round(decoded_ltc_usd['ticker']['avg'], 2)

			bot.sendMessage("PRIVMSG", channel,	"LTC/USD: Last %s USD, High %s USD, Low %s USD, Average %s USD" % (ltc_usd, ltc_usd_high, ltc_usd_low, ltc_usd_avg))

		except:
			bot.sendMessage("PRIVMSG", channel, "LTC is going to tha moooooon! (No, something went wrong...)")

mainclass = Ticker