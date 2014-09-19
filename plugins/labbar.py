# -*- coding: utf-8 -*-
from .pluginbase import PluginBase
import traceback
import os
import time
import math

class DictionaryDict:
	def __init__(self):
		self.dict = {}

	def insert(self, word, description):
		self.dict[word] = description
		return "Inserted \"%s\" into dictionary" % word

	def lookup(self, word):
		if word in self.dict:
			return "Description for %s: %s" % (word, self.dict[word])
		else:
			return "Word does not exist in dictionary"

	def delete(self, word):
		if word in self.dict:
			self.dict.pop(word)
			return "Removed \"%s\" from dictionary" % word
		else:
			return "Word does not exist in dictionary"

class PhonebookEntry:
	def __init__(self, name, number, alias = None):
		self.name = name
		self.number = number
		if not alias:
			self.alias = []
		else:
			self.alias = alias

class Phonebook:
	def __init__(self):
		self.phonebook = []
		self.quit = False
		self.commands = {'add':self.add, 'lookup':self.lookup,
				'alias':self.alias, 'change':self.change, 'help':self.help,
				'remove':self.remove}
		self.load("phonebook1")

	def handleCommand(self, bot, channel, params):
		command = params[0]
		params = params[1:]
		buffer = ""
		if command in self.commands:
			try:
				buffer = self.commands[command](*params)
				self.save("phonebook1")
			except:
				traceback.print_exc()
				buffer = "Phonebook: invalid input"

		if type(buffer) == type(""):
			bot.sendMessage("PRIVMSG", channel, buffer)
		elif type(buffer) == type([]):
			for i in buffer:
				bot.sendMessage("PRIVMSG", channel, i)

	def getEntries(self, name = None):
		entries = []
		for i in self.phonebook:
			if i.name.upper() == name.upper() or name.upper() in list(map(str.upper, i.alias)):
				entries.append(i)

		return entries

	def getEntryNumber(self, entries, number = None):
		if not number:
			return "Multiple matches for name, number required"
			return None

		entry = None
		for i in entries:
			if i.number == number:
				entry = i

		if not entry:
			return "Number not matching name"
			return None

		return entry

	def help(self):
		buf = []
		buf.append("Available commands:")
		buf.append(", ".join(list(self.commands.keys())))
		return buf

	def add(self, name = None, number = None):
		if not name or not number:
			return "Usage: add <name> <number>"

		for i in self.phonebook:
			if (i.name == name or name in i.alias) and i.number == number:
				return "Entry already exists"

		self.phonebook.append(PhonebookEntry(name, number))

	def lookup(self, name = None):
		if not name:
			return "Usage: lookup <name>"

		entries = self.getEntries(name)

		if len(entries) > 0:
			buf = []
			for entry in entries:
				buf.append(entry.number)
			return buf
		else:
			return "Name does not exist"

	def alias(self, name = None, newname = None, number = None):
		if not name or not newname:
			return "Usage: alias <name> <newname> [number]"

		entries = self.getEntries(name)
		if len(entries) > 1:
			entry = self.getEntryNumber(entries, number)
			if not entry:
				return
			if type(entry) == type(""):
				return entry

			if newname in entry.alias:
				return "Alias already exists for entry"

			entry.alias.append(newname)
		elif len(entries) > 0:
			entry = entries[0]

			if newname in entry.alias:
				return "Alias already exists for entry"

			entry.alias.append(newname)
		else:
			return "Name does not exist"

	def change(self, name = None, number = None, oldNumber = None):
		if not name or not number:
			return "Usage: change <name> <number> [oldNumber]"

		entries = self.getEntries(name)

		if len(entries) > 1:
			entry = self.getEntryNumber(entries, oldNumber)
			if not entry:
				return
			if type(entry) == type(""):
				return entry

			entry.number = number

		elif len(entries) > 0:
			entry = entries[0]
			entry.number = number

		else:
			return "Name does not exist"

	def remove(self, name = None, number = None):
		if not name:
			return "Usage: remove <name> [number]"

		entries = self.getEntries(name)

		if len(entries) > 1:
			entry = self.getEntryNumber(entries, number)
			if not entry:
				return
			if type(entry) == type(""):
				return entry

			self.phonebook.remove(entry)
		elif len(entries) > 0:
			entry = entries[0]
			self.phonebook.remove(entry)
		else:
			return "Name does not exist"

	def save(self, filename = None):
		if not filename:
			return "Usage: save <filename>"

		f = open(filename, "w")
		for i in self.phonebook:
			print("%s;%s;%s%s" % (i.number, i.name, ";".join(i.alias), ";" if len(i.alias) > 0 else ""), file=f)
		f.close()

	def load(self, filename = None):
		if not filename:
			return "Usage: load <filename>"

		if not os.path.isfile(filename):
			return "File does not exist"

		f = open(filename, "r")
		lines = f.readlines()

		self.phonebook = []
		for line in lines:
			parts = line.split(";")
			number = parts[0]
			name = parts[1]
			alias = [i for i in parts[2:] if i != '']
			self.phonebook.append(PhonebookEntry(name, number, alias))

		f.close()

class Labbar(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!solve", self.handleSolve)
		bot.registerCommand("!derivative", self.handleDerivative)
		bot.registerCommand("!bounce", self.handleBounce)
		bot.registerCommand("!tvarsumma", self.handleTvarsumma)
		bot.registerCommand("!sockerkaka", self.handleSockerkaka)
		bot.registerCommand("!kostnad", self.handleKostnad)

		bot.addHelp("solve", "Usage: !solve <f> <x0> <h>")
		bot.addHelp("sockerkaka", "Usage: !sockerkaka <number of persons>")
		bot.addHelp("kostnad", "Usage: !kostnad <P> <r> <a>")
		bot.addHelp("bounce", "Usage: !bounce <number>")
		bot.addHelp("tvarsumma", "Usage: !tvarsumma <number>")
		bot.addHelp("derivative", "Usage: !derivative <f> <x> <h>")

		try:
			self.phonebook = Phonebook()
			bot.registerCommand("!phonebook", self.phonebook.handleCommand)
			bot.addHelp("phonebook", "!phonebook help for more help")
		except:
			traceback.print_exc()

		try:
			self.dict = DictionaryDict()
			bot.registerCommand("!dictionary", self.handleDictionary)
			bot.addHelp("dictionary",
				"Usage: !dictionary {insert|lookup|delete} <word> [description]")
		except:
			traceback.print_exc()

	def handleSockerkaka(self, bot, channel, params):
		try:
			antal = int(params[0])
			lines = self.sockerkaka(antal)
			for line in lines:
				bot.sendMessage("PRIVMSG", channel, line)
		except:
			traceback.print_exc()
			bot.sendMessage("PRIVMSG", channel, "Sockerkaka: invalid arguments")

	def handleKostnad(self, bot, channel, params):
		try:
			P = float(params[0])
			r = float(params[1])
			a = float(params[2])
			bot.sendMessage("PRIVMSG", channel, self.kostnad(P, r, a))
		except:
			traceback.print_exc()
			bot.sendMessage("PRIVMSG", channel, "kostnad: invalid arguments")

	def handleBounce(self, bot, channel, params):
		try:
			n = int(params[0])
			bot.sendMessage("PRIVMSG", channel, self.bounce(n))
		except:
			traceback.print_exc()
			bot.sendMessage("PRIVMSG", channel, "bounce: invalid arguments")

	def handleTvarsumma(self, bot, channel, params):
		try:
			if params[0].lower() == "ling-ond":
				bot.sendMessage("PRIVMSG", channel, "0")
				return

			n = int(params[0])
			bot.sendMessage("PRIVMSG", channel, str(self.tvarsumma(n)))
		except:
			traceback.print_exc()
			bot.sendMessage("PRIVMSG", channel, "tvarsumma: invalid arguments")

	def handleDictionary(self, bot, channel, params):
		if len(params) >= 2:
			action = params[0]
			word = params[1]
			if action == "insert":
				if len(params) >= 3:
					description = " ".join(params[2:])
					bot.sendMessage("PRIVMSG", channel, self.dict.insert(word, description))
				else:
					bot.sendMessage("PRIVMSG", channel,
						"dictionary: too few argumets")
			elif action == "lookup":
				bot.sendMessage("PRIVMSG", channel, self.dict.lookup(word))
			elif action == "delete":
				bot.sendMessage("PRIVMSG", channel, self.dict.delete(word))

	def handleDerivative(self, bot, channel, params):
		if len(params) < 3:
			return "Usage: !derivative <f> <x> <h>"

		result = self.derivative("".join(params[0:-2]), params[-2], params[-1])
		bot.sendMessage("PRIVMSG", channel, str(result))

	def handleSolve(self, bot, channel, params):
		if len(params) < 3:
			return "Usage: !derivative <f> <x> <h>"

		result = self.solve("".join(params[0:-2]), params[-2], params[-1])
		bot.sendMessage("PRIVMSG", channel, str(result))


	def sockerkaka(self, antal):
		buf = "Sockerkaka: Ingredienser för %d personer:\n" \
		"* %d ägg\n" \
		"* %.2f dl strösocker\n" \
		"* %.2f tsk vaniljsocker\n" \
		"* %.2f tsk bakpulver\n" \
		"* %.2f g margarin eller smör\n" \
		"* %.2f dl vatten\n" \
		"* %.2f dl vetemjöl" % (antal, round((3.0/4)*antal), (3.0/4)*antal,
				(2.0/4)*antal, (2.0/4)*antal, (75.0/4)*antal,
				(1.0/4)*antal, (3.0/4)*antal)
		return buf.split("\n")

	def kostnad(self, P, r, a):
		k = P + (a+1)*P*r/2
		return "Den totala kostnaden efter %i år är %i kr." % (a, k)

	def bounce(self, n):
		buf = ""
		sign = n//abs(n)
		for i in range(-n, n+(1*sign), 1*sign):
			buf += "%d " % (abs(i)*sign)

		return buf

	def tvarsumma(self, n):
		return n%10 + self.tvarsumma(n/10) if n else 0

	def derivative(self, fStr, x, h):
		f = lambda x: eval(fStr, {"__builtins__":None},
			{"x":x, "sin":math.sin, "cos":math.cos, "abs":abs, "e":math.e,
				"pi":math.pi, "log":math.log, "tan":math.tan})
		x = float(x)
		h = float(h)

		return (1.0/(2.0*h))*(f(x+h) - f(x-h))

	def solve(self, fStr, x0, h):
		startTime = time.time()

		f = lambda x: eval(fStr, {"__builtins__":None},
			{"x":x, "sin":math.sin, "cos":math.cos, "abs":abs, "e":math.e,
				"pi":math.pi, "log":math.log, "tan":math.tan})

		h = float(h)
		x0 = float(x0)
		x1 = 0
		while abs(x1-x0) > h:
			if time.time() - startTime > 20.0:
				return """Solve taking too long to execute, aborting.""" \
						""" Current value: %d""" % (x0)

			x1 = x0
			x0 = x0 - f(x0)/self.derivative(fStr, x0, h)

		return x0

mainclass = Labbar
