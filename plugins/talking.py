#!/usr/bin/env python2
# -*- encoding: utf-8 -*-

# BOTNICK Lowe

from pluginbase import PluginBase

import random
import shutil
import time

class Talking(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!talk", self.talk)
		bot.registerQueryCommand("!listsentences", self.listSentences)
		bot.registerQueryCommand("!addsentence", self.addSentence)


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
		f = open("dict/dsso-1.44.txt")

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
		f = open(filename)
		for line in f.readlines():
			self.namn.append([line])
		f.close()

	def saveSentences(self, filename):
		shutil.move(filename, filename + ".old")

		f = open(filename, 'w')
		for i in self.sentences:
			print >>f, i
		f.close()

	def  loadSentences(self, filename):
		f = open(filename, 'r')
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

		sentence = random.choice(self.sentences)
		sentence = sentence.replace("%%ADJEKTIV%%", random.choice(self.adjektiv)[0])
		sentence = sentence.replace("%%ADJEKTIV5%%", adjektiv5)
		sentence = sentence.replace("%%NAMN%%", random.choice(self.namn)[0])
		sentence = sentence.replace("%%SUBSTANTIV%%", random.choice(self.substantiv)[0])

		substantiv5 = ""
		while not substantiv5 or substantiv5 == "!":
			substantiv5 = random.choice(self.substantiv)[5]

		sentence = sentence.replace("%%SUBSTANTIV5%%", substantiv5)
		sentence = sentence.replace("%%PRONOMEN%%", random.choice(self.pronomen)[0])
		sentence = sentence.replace("%%VERB%%", random.choice(self.verb)[1])
		sentence = sentence.replace("%%VERB3%%", random.choice(self.verb)[3])
		sentence = sentence.replace("%%VERB4%%", random.choice(self.verb)[4])
		sentence = sentence.replace("%%DEFINITION1%%", random.choice(self.definitions)[0])
		sentence = sentence.replace("%%NICK%%", random.choice(bot.channels[channel.upper()].names))

		return sentence

	def talk(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel, self.getSentence(bot, channel))

	def listSentences(self, bot, channel, params):
		for sentence in self.sentences:
			bot.sendMessage("PRIVMSG", channel, sentence)

	def addSentence(self, bot, channel, params):
		self.sentences.append(" ".join(params))
		self.saveSentences("sentences.txt")

	def on_tick(self, bot):
		hour = time.localtime().tm_hour
		if time.time() - bot.nextTalk > 0 and hour > 6 and hour <= 23:
			bot.nextTalk = time.time()  + random.randint(1800, 7200)
			chan = random.choice(bot.channels.keys())
			bot.sendMessage("PRIVMSG", chan, self.getSentence(bot, chan))


mainclass = Talking
