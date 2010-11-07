# -*- coding: utf-8 -*-
from pluginbase import PluginBase

import traceback
import random

class DieRoll(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!dieroll", self.handleDieRoll)
		bot.addHelp("dieroll",
			"Usage: <number of dice>d<number of sides of die>")

	def handleDieRoll(self, bot, channel, params):
		if len(params) >= 1:
			try:
				bot.sendMessage("PRIVMSG", channel, self.dieroll(params))
			except:
				traceback.print_exc()
				bot.sendMessage("PRIVMSG", channel,
					"dieroll: invalid arguments")
		else:
			bot.sendMessage("PRIVMSG", channel,
				"dieroll: invalid arguments")

	def dieroll(self, params):
		buf = ""
		params = map(str.upper, params)
		for param in params:
			dice, sides = param.split("D")
			mod = 0
			times = 0
			divide = 0
			if "+" in sides:
				sides, mod = sides.split("+")
				mod = int(mod)
			elif "-" in sides:
				sides, mod = sides.split("-")
				mod = int(mod)
				mod = -mod
			elif "*" in sides:
				sides, times = sides.split("*")
				times = int(times)
			elif "/" in sides:
				sides, divide = sides.split("/")
				divide = float(divide)

			dice = int(dice)
			sides = int(sides)

			buf +=  "%s [ " % (param)
			total = 0
			for i in xrange(dice):
				if len(buf) > 450:
					return buf

				n = random.randint(1, sides)
				total += n
				buf += "%d " % n

			if times != 0:
				buf += "] * %d = %d, " % (times, total*times)
			elif divide != 0:
				buf += "] / %g = %g, " % (divide, total/divide)
			else:
				buf += "]%s = %d, " % ( ((" - %s" % abs(mod)) if mod < 0 else
					(" + %s" % mod)) if mod != 0 else "", total+mod)

		return buf

mainclass = DieRoll
