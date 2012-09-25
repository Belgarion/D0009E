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

	def handleTitle(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel, self.getTitle("%20".join(params)))
	def shortenURL(self, url):
		APIURL = "https://api-ssl.bitly.com"

		#Get APIKEY
		f = open("api.key","r")
		apiKey = f.read()
		f.close()

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
		GETURL += apiKey + "&"
		GETURL += "longURL=" + url

		try:
			f = urllib2.urlopen(GETURL)
			shortUrl = re.findall("\"url\": \"(.*?)\"",f.read())[0].replace("\/","/")
			return shortUrl
		except:
			return ""

	def getTitle(self, url):
		try:
			shortUrl = self.shortenURL(url)

			headers = { 'User-Agent' : 'Mozilla/5.0' }
			req = urllib2.Request(url,None,headers)
			f = urllib2.urlopen(req)
			data = f.read()
			f.close()
		except urllib2.HTTPError, e:
			return "Error: %s" % e

		m = re.search("<title>\n?(.*)\n?</title>", data)
		if m:
			return "[ %s ] Title: %s" % (shortUrl,m.group(1))
		return "Title not found"

mainclass = Title
