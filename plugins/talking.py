#!/usr/bin/env python2
# -*- encoding: utf-8 -*-

# BOTNICK Lowe

from .pluginbase import PluginBase
from .hyphenator import Hyphenator

import random
import shutil
import time
import codecs
import traceback


class Talking(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!talk", self.talk)
		bot.registerCommand("!mtalk", self.talk_markov)
		bot.registerCommand("!rykte", self.rykte)
		bot.registerCommand("!segway", self.segway)
		bot.registerCommand("!segue", self.segue)
		bot.registerCommand("!haiku", self.haiku)
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
		self.land = []
		self.yrke = []
		self.hyph = Hyphenator("dict/hyph_sv_SE.dic")

		self.loadWords()
		self.loadDict("dict/sagonamn", self.namn)

		self.sentences = []
		self.loadSentences("sentences.txt")

		self.loadMarkov("markov.txt", 2)

	def loadMarkov(self, filename, degrees=2):
		self.markov_cache = {}
		self.markov_degrees = degrees
		f = open(filename, errors='ignore')
		data = f.read().lower()
		f.close()
		self.markov_words = data.split()
		self.markov_word_size = len(self.markov_words)
		self.markov_generate_database(degrees)

	def markov_triples(self, degrees):
		if self.markov_word_size < degrees+1:
			return

		for i in range(self.markov_word_size - degrees):
			yield tuple(self.markov_words[i:i+degrees+1])

	def markov_generate_database(self, degrees):
		for words in self.markov_triples(degrees):
			key = tuple(words[:-1])
			if key in self.markov_cache:
				self.markov_cache[key].append(words[-1])
			else:
				self.markov_cache[key] = [words[-1]]

	def markov_generate_text(self, size=10):
		key = random.choice(list(self.markov_cache.keys()))
		gen_words = []
		for i in range(size):
			gen_words.append(key[0])
			key = list(key[1:]) + [random.choice(self.markov_cache[tuple(key)])]
		count = size
		while True:
			gen_words.append(key[0])
			print(key[0][-1])
			if key[0][-1] in ".'\",;:" or count > 25:
				break
			key = list(key[1:]) + [random.choice(self.markov_cache[tuple(key)])]
			count += 1
		return ' '.join(gen_words)

	def talk_markov(self, bot, channel, params):
		try:
			bot.sendMessage("PRIVMSG", channel, self.markov_generate_text())
		except:
			traceback.print_exc()

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

		f = codecs.open("dict/land.txt",'r','utf-8')
		landList = f.read().split(",")
		for l in landList:
			self.land.append(l)
		f.close()

		f = codecs.open("dict/yrke.txt",'r','utf-8')
		yrkeList = f.read().split(",")
		for l in yrkeList:
			self.yrke.append(l)
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
			print(i, file=f)
		f.close()

	def  loadSentences(self, filename):
		f = codecs.open(filename, 'r', 'utf-8')
		for line in f.readlines():
			line = line.replace("\r", "")
			line = line.replace("\n", "")
			self.sentences.append(line)
		f.close()

	def getSentence(self, bot, channel):
		sentence = random.choice(self.sentences)
		return self.subSentence(bot, channel, sentence)

	def subSentence(self, bot, channel, sentence):
		adjektiv5 = ""
		while not adjektiv5 or adjektiv5 == "!":
			adjektiv5 = random.choice(self.adjektiv)[5]


		substitutes = {"%%ADJEKTIV%%":(self.adjektiv,0),
				"%%ADJEKTIV%%":(self.adjektiv, 0),
				"%%ADJEKTIV1%%":(self.adjektiv, 1),
				"%%ADJEKTIV2%%":(self.adjektiv, 2),
				"%%ADJEKTIV3%%":(self.adjektiv, 3),
				"%%ADJEKTIV4%%":(self.adjektiv, 4),
				"%%ADJEKTIV5%%":(self.adjektiv, 5),
				"%%NAMN%%":(self.namn, 0),
				"%%SUBSTANTIV%%":(self.substantiv, 0),
				"%%SUBSTANTIV1%%":(self.substantiv, 1),
				"%%SUBSTANTIV2%%":(self.substantiv, 2),
				"%%SUBSTANTIV3%%":(self.substantiv, 3),
				"%%SUBSTANTIV4%%":(self.substantiv, 4),
				"%%SUBSTANTIV5%%":(self.substantiv, 5),
				"%%SUBSTANTIV6%%":(self.substantiv, 6),
				"%%SUBSTANTIV7%%":(self.substantiv, 7),
				"%%SUBSTANTIV8%%":(self.substantiv, 8),
				"%%PRONOMEN%%":(self.pronomen, 0),
				"%%VERB%%":(self.verb, 0),
				"%%VERB1%%":(self.verb, 1),
				"%%VERB2%%":(self.verb, 2),
				"%%VERB3%%":(self.verb, 3),
				"%%VERB4%%":(self.verb, 4),
				"%%ADVERB%%":(self.adverb, 0),
				"%%DEFINITION1%%": (self.definitions, 0),
				"%%LAND%%": (self.land, -1),
				"%%YRKE%%": (self.yrke, -1),
				"%%NICK%%": ([x.decode('utf-8') for x in bot.channels[channel.upper()].names], -1)}

		for sub in substitutes:
			while sub in sentence:
				tup = substitutes[sub]
				word = ""
				while not word or word == "!":
					if tup[1] >= 0:
						word = random.choice(tup[0])[tup[1]]
					else:
						word = random.choice(tup[0])
					if sub != "%%DEFINITION1%%":
						word = random.choice(word.split(", "))
				sentence = sentence.replace(sub, word, 1)

		return sentence

	def talk(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel, self.getSentence(bot, channel))

	def rykte(self, bot, channel, params):
		nick = "%%NICK%%"
		nick2 = "%%NICK%%"
		if len(params) > 1:
			nick = params[0].replace("_", " ")
			nick2 = params[1].replace("_", " ")
			bot.sendMessage("PRIVMSG", channel, self.subSentence(bot, channel,
				("Det går ett rykte i dataettan att %s har %%%%VERB3%%%% %s." % (nick, nick2))))
			return

		if len(params) > 0:
			nick = params[0].replace("_", " ")
		bot.sendMessage("PRIVMSG", channel, self.subSentence(bot, channel,
			("Det går ett rykte i dataettan att %s har %%%%VERB3%%%%." % (nick))))

	def segway(self, bot, channel, params):
		if random.randint(0,100) != 0: amne = random.choice(self.substantiv)[0]
		else:	amne = random.choice(self.land)
		outstr = "        _\n~~      /\n\n~~     / Nytt Ämne: "+amne+"\n~~ ___/\n   (o)"
		outlst = outstr.split("\n")
		bot.sendMessage("PRIVMSG", channel, outlst)

	def segue(self, bot, channel, params):
		if random.randint(0,100) != 0: o = random.choice(self.substantiv)[0]
		else:	o = random.choice(self.land) # 1% länder, bygger på statestik.
		lst  = ["Grabbar, vad tycker ni om "+o+"?","Så fruktansvärt tråkigt ämne, kan ni inte prata om "+o+" istället?","Så... angående "+o+"?"]
		bot.sendMessage("PRIVMSG", channel, random.choice(lst))

	def generateHaikuSentence(self, length, maxtries):
		sentence = []
		while length > 0 or maxtries > 0:
			wordtype = random.randint(0,99)
			if wordtype >= 0 and wordtype <25:
				o = random.choice(self.substantiv)[0]
			elif wordtype >= 25 and wordtype <50:
				o = random.choice(self.verb)[0]
			elif wordtype >= 50 and wordtype <75:
				o = random.choice(self.adjektiv)[0]
			elif wordtype >=75 and wordtype <99:
				o = random.choice(self.prepositioner)[0]
			hyphword = self.hyph.inserted(o)
			hyphlist = hyphword.split("-")
			syllableCount = len(hyphlist)
			if syllableCount <= length:
				sentence.append("".join(hyphlist))
				length-=syllableCount
			maxtries-=1
		random.shuffle(sentence)
		return " ".join(sentence)

	def haiku(self, bot, channel, params):
		out = []
		out.append("[Haiku]------------")
		out.append(self.generateHaikuSentence(5,50))
		out.append(self.generateHaikuSentence(7,50))
		out.append(self.generateHaikuSentence(5,50))
		out.append("-------------------")
		bot.sendMessage("PRIVMSG", channel, out)

	def listSentences(self, bot, channel, params):
		for i, sentence in enumerate(self.sentences):
			bot.sendMessage("PRIVMSG", channel, str(i) + ": " + sentence)

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
			chan = random.choice(list(bot.channels.keys()))
			bot.sendMessage("PRIVMSG", chan, self.getSentence(bot, chan))


mainclass = Talking
