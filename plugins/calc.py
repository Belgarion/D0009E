# -*- coding: utf-8 -*-
from .pluginbase import PluginBase

import math
import traceback

class Calc(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!calc", self.handleCalc)
		bot.addHelp("calc", "Usage: !calc <expression>")

	def handleCalc(self, bot, channel, params):
		if len(params) < 1:
			return "Usage: !calc <expression>"

		result = None
		try:
			expr = "".join(params)
			if ".__" in expr:
				result = "NEJ!"
			else:
				expr = expr.replace("__", "_DOUBLEUNDERSCORE_")
				result = self.calc(expr)
		except Exception as e:
			traceback.print_exc()
			result = "Error"
		bot.sendMessage("PRIVMSG", channel, str(result))

	def calc(self, expr):
		result = eval(expr, {"__builtins__":None},
			{"sin":math.sin, "cos":math.cos, "abs":abs, "e":math.e,
				"pi":math.pi, "log":math.log, "tan":math.tan, "factorial":math.factorial})
		return result

mainclass = Calc
