# -*- coding: utf-8 -*-
from pluginbase import PluginBase

import urllib2
import re

import StringIO
import struct
import HTMLParser

def getImageInfo(data):
    data = str(data)
    size = len(data)
    height = -1
    width = -1
    content_type = ''

    # handle GIFs
    if (size >= 10) and data[:6] in ('GIF87a', 'GIF89a'):
        # Check to see if content_type is correct
        content_type = 'image/gif'
        w, h = struct.unpack("<HH", data[6:10])
        width = int(w)
        height = int(h)

    # See PNG 2. Edition spec (http://www.w3.org/TR/PNG/)
    # Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
    # and finally the 4-byte width, height
    elif ((size >= 24) and data.startswith('\211PNG\r\n\032\n')
          and (data[12:16] == 'IHDR')):
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[16:24])
        width = int(w)
        height = int(h)

    # Maybe this is for an older PNG version.
    elif (size >= 16) and data.startswith('\211PNG\r\n\032\n'):
        # Check to see if we have the right content type
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[8:16])
        width = int(w)
        height = int(h)

    # handle JPEGs
    elif (size >= 2) and data.startswith('\377\330'):
        content_type = 'image/jpeg'
        jpeg = StringIO.StringIO(data)
        jpeg.read(2)
        b = jpeg.read(1)
        try:
            while (b and ord(b) != 0xDA):
                while (ord(b) != 0xFF): b = jpeg.read(1)
                while (ord(b) == 0xFF): b = jpeg.read(1)
                if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                    jpeg.read(3)
                    h, w = struct.unpack(">HH", jpeg.read(4))
                    break
                else:
                    jpeg.read(int(struct.unpack(">H", jpeg.read(2))[0])-2)
                b = jpeg.read(1)
            width = int(w)
            height = int(h)
        except struct.error:
            pass
        except ValueError:
            pass

    return content_type, width, height

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

			headers = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0' }
			req = urllib2.Request(url,None,headers)
			f = urllib2.urlopen(req)
			data = f.read(10240) # title should be in first 10kB
			f.close()
		except urllib2.HTTPError, e:
			return "Error: %s" % e

		m = re.search("<title>(.*?)</title>", data, re.DOTALL | re.IGNORECASE)
		if m:
			title = m.group(1)
			title = title.replace("\n", " ")
			title = title.strip()
			#title = title.replace("&amp;", "&")
			try:
				h = HTMLParser.HTMLParser()
				title = h.unescape(title).encode("utf-8")
			except:
				pass
			return "[ %s ] Title: %s" % (shortUrl,title)
		# check if image
		type, width, height = getImageInfo(data)
		if width != -1:
			return "[ %s ] Image: Type: %s, %sx%s" % (shortUrl, type, width, height)
		return "[ %s ] Title: Not Found" % (shortUrl)

mainclass = Title
