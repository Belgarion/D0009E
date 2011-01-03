#!/usr/bin/env python2
# -*- encoding: utf-8 -*-

# BOTNICK Lowe

from pluginbase import PluginBase

import random
import shutil
import time
import codecs
import traceback

class Talking(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!talk", self.talk)
		bot.registerQueryCommand("!listsentences", self.listSentences)
		bot.registerQueryCommand("!addsentence", self.addSentence)
		bot.registerQueryCommand("!delsentence", self.delSentence)
		bot.registerQueryCommand("!repsentence", self.repSentence)
		self.substantiv = []
		self.pronomen = [["jag"], ["du"], ["vi"], ["ni"], ["man kanske"]]
		self.adjektiv = []
		self.verb  = []
		self.adverb = []
		self.prepositioner = []
		self.namn = []
		self.definitions = []

		self.loadWords()
		self.loadDict("dict/sagonamn", self.namn)

		"""self.sentences = ["Du är %%ADJEKTIV5%% än %%NAMN%%",
				"Ska %%PRONOMEN%% %%VERB%% en %%SUBSTANTIV%%?",
				"Hej %%NICK%% vill du med på lite %%SUBSTANTIV%%?",
				"Jo förresten %%NICK%%, visste du att i %%LAND%% så "
					"%%VERB4%% de %%SUBSTANTIV5%%",
				"har ni hört att det går ett rykte om att %%NICK%% har "
					"%%VERB3%%",
				"%%NICK%% det går ett rykte att du %%VERB%% %%SUBSTANTIV%% "
					"stämmer det?",
				"%%NICK%%: du är allt bra %%ADJEKTIV%% du :)",
				"%%NICK%%: du får sluta vara så jävla %%ADJEKTIV%%",
				"%%NICK%%: mja, lite %%ADJEKTIV%% kan du ju vara...",
				"Asså menar du inte %%SUBSTANTIV%% nu?",
				"Aah, du menar typ som %%SUBSTANTIV%%?",
				"Fan jag hatar %%SUBSTANTIV%%",
				"Asså jag orkar inte med mer %%SUBSTANTIV%%",
				"Jag har fått en massa spam om %%SUBSTANTIV5%%, "
					"ska jag ta illa upp?",
				"Äh, nu får det vara nog. Nu ska jag gå och %%VERB%%",
				"/away %%SUBSTANTIV%%",
				"Asså är inte det typ%%DEFINITION1%%"]"""
		self.sentences = []

		self.loadSentences("sentences.txt")


	def loadWords(self):
		f = codecs.open("dict/dsso-1.44.txt",'r','utf-8')

		for line in f.readlines():
			if line.split(":")[0] == "DEFINITION 1":
				self.definitions.append([line.split(":")[1].lower()])

			line.replace("\n","")
			line.replace("\r","")
			if ">" in line:
				wordType = line.split("<")[1].split(">")[0]
				word = line.split(">")[1].split(":")
				if wordType == "substantiv":
					self.substantiv.append(word)
				elif wordType == "adjektiv":
					self.adjektiv.append(word)
				elif wordType == "adverb":
					self.adverb.append(word)
				#elif wordType == "pronomen":
				#	self.pronomen.append(word)
				elif wordType == "verb":
					self.verb.append(word)
				elif wordType  == "egennamn":
					self.namn.append(word)
				elif wordType  == "preposition":
					self.prepositioner.append(word)

		f.close()

	def loadDict(self, filename, wordlist):
		f = codecs.open(filename, 'r', 'utf-8')
		for line in f.readlines():
			self.namn.append([line])
		f.close()

	def saveSentences(self, filename):
		shutil.move(filename, filename + ".old")

		f = codecs.open(filename, 'w', 'utf-8')
		for i in self.sentences:
			print >>f, i
		f.close()

	def  loadSentences(self, filename):
		f = codecs.open(filename, 'r', 'utf-8')
		for line in f.readlines():
			line = line.replace("\r", "")
			line = line.replace("\n", "")
			self.sentences.append(line)
		f.close()

	def getSentence(self, bot, channel):
		"""return "%s %s %s %s" % \
				(random.choice(self.pronomen)[0],
						random.choice(self.verb)[0],
						random.choice(self.substantiv)[0],
						random.choice(self.adverb)[0])"""

		adjektiv5 = ""
		while not adjektiv5 or adjektiv5 == "!":
			adjektiv5 = random.choice(self.adjektiv)[5]


		substitutes = {"%%ADJEKTIV%%":(self.adjektiv,0),
				"%%ADJEKTIV5%%":(self.adjektiv, 5),
				"%%NAMN%%":(self.namn, 0),
				"%%SUBSTANTIV%%":(self.substantiv, 0),
				"%%SUBSTANTIV5%%":(self.substantiv, 5),
				"%%PRONOMEN%%":(self.pronomen, 0),
				"%%VERB%%":(self.verb, 1),
				"%%VERB3%%":(self.verb, 3),
				"%%VERB4%%":(self.verb, 4),
				"%%DEFINITION1%%": (self.definitions, 0),
				"%%NICK%%": (bot.channels[channel.upper()].names, -1)}

		sentence = random.choice(self.sentences)
		for sub in substitutes:
			while sub in sentence:
				tup = substitutes[sub]
				word = ""
				while not word or word == "!":
					if tup[1] >= 0:
						word = random.choice(tup[0])[tup[1]]
					else:
						word = random.choice(tup[0])
				sentence = sentence.replace(sub, word, 1)

		return sentence.encode('latin1')

	def talk(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel, self.getSentence(bot, channel))

	def listSentences(self, bot, channel, params):
		for i, sentence in enumerate(self.sentences):
			bot.sendMessage("PRIVMSG", channel, str(i) + ": " + sentence.encode("latin1"))

	def addSentence(self, bot, channel, params):
		self.sentences.append(" ".join(params).decode("utf-8"))
		self.saveSentences("sentences.txt")

	def delSentence(self, bot, channel, params):
		try:
			self.sentences.pop(int(params[0]))
			self.saveSentences("sentences.txt")
			bot.sendMessage("PRIVMSG", channel, "Sentence deleted.")
		except:
			bot.sendMessage("PRIVMSG", channel, "Failed to delete sentence.")
	def repSentence(self, bot, channel, params):
		try:
			self.sentences[int(params[0])] = " ".join(params[1:]).decode("utf-8")
			self.saveSentences("sentences.txt")
			bot.sendMessage("PRIVMSG", channel, "Sentence replaced.")
		except:
			bot.sendMessage("PRIVMSG", channel, "Failed to replace sentence.")
			traceback.print_exc()
	def on_tick(self, bot):
		return
		hour = time.localtime().tm_hour
		if time.time() - bot.nextTalk > 0 and hour > 6 and hour <= 23:
			bot.nextTalk = time.time()  + random.randint(1800, 7200)
			chan = random.choice(bot.channels.keys())
			bot.sendMessage("PRIVMSG", chan, self.getSentence(bot, chan))


mainclass = Talking
