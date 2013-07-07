# -*- coding: utf-8 -*-
from pluginbase import PluginBase

import urllib2
import re

class Title(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!title", self.handleTitle)
		bot.addHelp("title", "Usage: !title <url>")
		bot.registerCommand("!link", self.handleTitle)
		bot.addHelp("link", "Usage: !link <url>")
		bot.registerContentCommand("https?://", self.handleContentUrl)

	def handleNewConfig(self):
		self.apiKey = self.getConfig("apikey")

	def handleTitle(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel, self.getTitle("%20".join(params)))

	def handleContentUrl(self, bot, channel, content):
		m = re.search("(https?://[^\s]+)", content)
		url = m.group(0)
		print url
		self.handleTitle(bot, channel, [url])

	def shortenURL(self, url):
		APIURL = "https://api-ssl.bitly.com"

		#Encode url
		url = url.replace("!","%21")
		url = url.replace("#","%23")
		url = url.replace("$","%24")
		url = url.replace("&","%26")
		url = url.replace("'","%27")
		url = url.replace("(","%28")
		url = url.replace(")","%29")
		url = url.replace("*","%2A")
		url = url.replace("+","%2B")
		url = url.replace(",","%2C")
		url = url.replace("/","%2F")
		url = url.replace(":","%3A")
		url = url.replace(";","%3B")
		url = url.replace("=","%3D")
		url = url.replace("?","%3F")
		url = url.replace("@","%40")
		url = url.replace("[","%5B")
		url = url.replace("]","%5D")

		#Create String
		GETURL = APIURL + "/v3/shorten?"
		GETURL += self.apiKey + "&"
		GETURL += "longURL=" + url

		try:
			f = urllib2.urlopen(GETURL)
			shortUrl = re.findall("\"url\": \"(.*?)\"",f.read())[0].replace("\/","/")
			return shortUrl
		except:
			return ""

	def getTitle(self, url):
		try:
			if url[0:7] != "http://" and url[0:8] != "https://" : url = "http://" + url
			shortUrl = self.shortenURL(url)[7:]

			headers = { 'User-Agent' : 'Mozilla/5.0' }
			req = urllib2.Request(url,None,headers)
			f = urllib2.urlopen(req)
			data = f.read(10240) # title should be in first 10kB
			f.close()
		except urllib2.HTTPError, e:
			return "Error: %s" % e

		m = re.search("<title>(.*)</title>", data, re.DOTALL | re.IGNORECASE)
		if m:
			title = m.group(1)
			title = title.replace("\n", " ")
			return "[ %s ] Title: %s" % (shortUrl,title)
		return "[ %s ] Title: Not Found" % (shortUrl)

mainclass = Title
