# -*- coding: utf-8 -*-
from .pluginbase import PluginBase

import traceback

import urllib.request, urllib.error, urllib.parse
import re

import io
import struct
import html.parser
import string
import encodings
import encodings.idna

def simpleencode(str):
	out = ""
	validchars = string.ascii_letters + string.digits + '-._~:/?#[]@!$&\'()*+,;='
	for char in str:
		if char in validchars:
			out += char
		else:
			out += "%" + hex(ord(char))[2:]
	return out

class NoRedirection(urllib.request.HTTPErrorProcessor):
  def http_response(self, request, response):
    return response
  https_response = http_response

def getImageInfo(data):
    textData = str(data.decode('iso-8859-1'))
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
    elif ((size >= 24) and textData.startswith('\211PNG\r\n\032\n')
          and (textData[12:16] == 'IHDR')):
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[16:24])
        width = int(w)
        height = int(h)

    # Maybe this is for an older PNG version.
    elif (size >= 16) and textData.startswith('\211PNG\r\n\032\n'):
        # Check to see if we have the right content type
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[8:16])
        width = int(w)
        height = int(h)

    # handle JPEGs
    elif (size >= 2) and textData.startswith('\377\330'):
        content_type = 'image/jpeg'
        jpeg = io.StringIO(textData)
        jpeg.read(2)
        b = jpeg.read(1)
        try:
            while (b and ord(b) != 0xDA):
                while (ord(b) != 0xFF): b = jpeg.read(1)
                while (ord(b) == 0xFF): b = jpeg.read(1)
                if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                    jpeg.read(3)
                    h, w = struct.unpack(">HH", jpeg.read(4).encode('iso-8859-1'))
                    break
                else:
                    jpeg.read(int(struct.unpack(">H", jpeg.read(2).encode('iso-8859-1'))[0])-2)
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
		self.handleTitle(bot, channel, [url])

	def shortenURL(self, url):

		#This is stupid, but special case because reddit people are terrible
		if re.match("(http\:\/\/|https\:\/\/)?(www\.)?reddit\.com", url):
			try:
				return "http://redd.it/"+re.search("comments/(.+?)\/", url).groups(1)[0]
			except:
				pass

		if re.match("(http\:\/\/|https\:\/\/)?(www\.)?(redd\.it|öä.se)", url) and len(url) < 23:
			return url
		#End special case

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
		url = url.replace("Å","%C5")
		url = url.replace("Ä","%C4")
		url = url.replace("Ö","%D6")
		url = url.replace("å","%E5")
		url = url.replace("ä","%E4")
		url = url.replace("ö","%F6")

		#url = urllib.parse.urlencode(url)

		#Create String
		GETURL = APIURL + "/v3/shorten?"
		GETURL += self.apiKey + "&"
		GETURL += "longURL=" + url

		try:
			f = urllib.request.urlopen(GETURL)
			data = f.read().decode('iso-8859-1')
			shortUrl = re.findall("\"url\": \"(.*?)\"",data)[0].replace("\/","/")
			return shortUrl
		except:
			traceback.print_exc()
			return ""

	def getTitle(self, url):
		try:
			if url[0:7] != "http://" and url[0:8] != "https://" : url = "http://" + url
			shortUrl = self.shortenURL(url)[7:]
			proto, empty, host, *path = url.split("/")
			host_parts = host.split(".")
			host = ""
			for part in host_parts:
				part = encodings.idna.nameprep(part)
				part = encodings.idna.ToASCII(part)
				host = ((host + ".") if host else "") + part.decode('utf-8')
			url = proto + "//" + host + "/" + "/".join(path)
			print(url)

			headers = { 'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:24.0) Gecko/20100101 Firefox/24.0' }
			req = urllib.request.Request(url,None,headers)
			opener = urllib.request.build_opener(NoRedirection)
			f = opener.open(req)
			print("Code:", f.getcode())
			if f.getcode() >= 400:
				print(f.read(1024))
				return "Error: %s" % (f.getcode())
			location = f.getheader('Location')
			print("URL:",url)
			while location != None:
				print("Location: " + location)
				req=urllib.request.Request(simpleencode(location),None, headers)
				f.close()
				f = opener.open(req)
				print("Code:", f.getcode())
				if f.getcode() >= 400:
					print(f.read(1024))
					return "Error: %s" % (f.getcode())
				location = f.getheader('Location')
			rawData = f.read(1024000)
			data = ""
			try:
				data = rawData.decode('utf-8')
			except:
				data = rawData.decode('iso-8859-1')
			f.close()
		except urllib.error.HTTPError as e:
			return "Error: %s" % e

		m = re.search("<title>(.*?)</title>", data, re.DOTALL | re.IGNORECASE)
		if m:
			title = m.group(1)
			title = title.replace("\n", " ")
			title = title.strip()
			#title = title.replace("&amp;", "&")
			try:
				h = html.parser.HTMLParser()
				title = h.unescape(title)
			except:
				pass
			return "[ %s ] Title: %s" % (shortUrl,title)
		# check if image
		type, width, height = getImageInfo(rawData)
		if width != -1:
			return "[ %s ] Image: Type: %s, %sx%s" % (shortUrl, type, width, height)
		return "[ %s ] Title: Not Found" % (shortUrl)

mainclass = Title
