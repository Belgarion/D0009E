# -*- coding: utf-8 -*-

class PluginBase():

	def __init__(self, bot):
		pass

	def on_privmsg(self, bot, nick, target, args):
		pass

	def on_tick(self, bot):
		pass

	def updateConfig(self, key, value):
		key = key.lower()
		if not "config" in dir(self):
			self.config = {}
		self.config[key] = value

	def setConfig(self, conf):
		if type(conf) == type({}):
			self.config = conf
			self.handleNewConfig()
		else:
			print("Unsupported config type", self, conf)

	def getConfigDict(self):
		if "config" in dir(self):
			return self.config
		else:
			return {}

	def getConfig(self, key, defaultValue = None):
		key = key.lower()
		if not "config" in dir(self):
			return defaultValue

		if key in self.config:
			return self.config[key]

		return defaultValue

	def handleNewConfig(self):
		pass
