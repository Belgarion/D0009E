# -*- coding: utf-8 -*-
from pluginbase import PluginBase

import urllib2
import time
import re

class Lunch(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!lunch", self.handleLunch)
		bot.addHelp("lunch", "Lunch @ STUK")

	def handleLunch(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel, self.getLunch(" ".join(params)))

	def getLunch(self, place = ""):
		tm = time.localtime()
		weekdays = ["Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag",
			"Lördag", "Söndag"]
		wday = tm.tm_wday

		mday = tm.tm_mday
		if tm.tm_hour >= 13:
			wday += 1
			mday += 1

		day = weekdays[wday % 7]
		dateString = "%s %s/%s" % (day, mday, tm.tm_mon)

		if place.lower() == "unik" or place.lower() == "uni:k":
			return self.getLunchUnik(day)
		elif place.lower() == "gästis":
			return self.getLunchGastis(day)
		elif place.lower() == "centrum":
			return self.getLunchCentrum(dateString)
		elif place.lower() == "teknikens hus" or place.lower() == "husmans":
			return self.getLunchTeknikensHus(dateString)
		elif place.lower() == "aurorum":
			return self.getLunchAurorum(day)

		try:
			f = urllib2.urlopen("http://www.stuk.nu/menyer/lunchmeny/")
			data = f.read()
			data = data.replace("&nbsp;", " ")
			data = data.replace("\r", "")
			data = data.replace("<BR>", "\n")
			f.close()
		except urllib2.HTTPExceptionl, e:
			return e

		buf = "Lunch @ Stuk: "

		found = 0
		for line in data.split("\n"):
			line = re.sub(r'<[^>]+>', "", line)
			if not line:
				continue

			if dateString in line:
				buf += "%s: " % (line.strip())
				found = 1
				continue

			if found > 0:
				buf += line
				found += 1
				break

		return buf

	def getLunchUnik(self, day):
		try:
			f = urllib2.urlopen("http://www.unikcafe.se/hem.html")
			data = f.read()
			data = data.replace("&nbsp;", " ")
			data = data.replace("&amp;", "&")
			data = data.replace("\r", "")
			f.close()
		except:
			return "Error"

		week = ".."

		m = re.search('Veckans lunch (.+?)<', data)
		if m:
			week = m.group(1)

		m = re.search('%s :</span>\s*<br />(.*?)</p>' % day.lower(), data.replace("\n",""))
		if m:
			options = m.group(1).replace("<br />", " || ").replace("    - ", "")
			options = re.sub('<.+?>', '', options)
		else:
			options = "Error"

		return "Uni:k: %s %s: %s" % (day, week, options)

	def getLunchAurorum(self, day):
		try:
			f = urllib2.urlopen("http://www.restaurangaurorum.se/page_lunch_utskr.aspx")
			data = f.read()
			data = data.replace("&nbsp;", " ")
			data = data.replace("&amp;", "&")
			data = data.replace("\r", "")
			f.close()
		except:
			return "Error"

		week = ".."

		m = re.search('Matsedel vecka (.+?) ', data)
		if m:
			week = m.group(1)

		m = re.search('%s</strong>(.*?)<strong>' % (day.replace("å","&aring;").replace("ö", "&ouml;")), data.replace("\n",""))
		if m:
			options = m.group(1).replace("<br />", " || ").replace("&ouml;", "ö").replace("&auml;", "ä").replace("&aring;", "å").replace("&eacute;", "é")
			print  re.search(r'<em>\s*<p>\s*(.+?)\s*</p>\s*</em>', options).groups()
			options = re.sub(r'<em>\s*<p>\s*(.+?)\s*</p>\s*</em>', r'|| \1:', options)
			options = re.sub(r'<.+?>', '', options)
			options = re.sub(r'\s+', ' ', options)
		else:
			options = "Error"

		return "Aurorum: %s v.%s: %s" % (day, week, options)

	def getLunchCentrum(self, day):
		try:
			f = urllib2.urlopen("http://www.amica.se/centrumrestaurangen")
			data = f.read()
			data = data.replace("&amp;", "&")
			data = data.replace("\r", "")
			data = data.replace("\n", "")
			f.close()
		except:
			return "Error"

		m = re.search('%s(.+?)<h2' % (day.replace("å","&aring;").replace("ö", "&ouml;")), data)
		if not m:
			return "Centrum: Error"

		options = m.group(1).replace("<strong>", "").replace("</strong>","")
		options = re.sub('</p><p>&nbsp;(.+?)<', "<", options)
		options = options.replace("</p><p>", " || ").replace("&nbsp;", " ").replace("  ", " ").replace("&ouml;", "ö").replace("&auml;", "ä").replace("&aring;", "å").replace("&eacute;", "é")
		options = re.sub('<.+?>', '', options)

		options = options.split(" || ")

		output = []
		output.append("Centrum: %s: " % (day))
		print output
		for option in options:
			if len(output[-1]) + len(option) > 440:
				output.append("Centrum: %s: " % (day))

			output[-1] = output[-1] + " " + option

		return output

	def getLunchTeknikensHus(self, day):
		return "Teknikens Hus: Not yet implemented"
		try:
			f = urllib2.urlopen("http://www.husmans.se/lunchmenyn/")
			data = f.read()
			data = data.replace("&nbsp;", " ")
			data = data.replace("&amp;", "&")
			data = data.replace("\r", "")
			f.close()
		except:
			return "Error"

		week = ".."

		m = re.search('Veckans lunch (.+?)<', data)
		if m:
			week = m.group(1)

		m = re.search('%s :</span> <br />(.*?)</p>' % day.lower(), data.replace("\n",""))
		if m:
			options = m.group(1).replace("<br />", " || ").replace("    - ", "")
			options = re.sub('<.+?>', '', options)
		else:
			options = "Error"

		return "Teknikens Hus: %s %s: %s" % (day, week, options)


	def getLunchGastis(self, day):
		try:
			f = urllib2.urlopen("http://www.kalix.nu/scripts/lunch.asp?uid=1103")
			data = f.read()
			data = data.replace("&nbsp;", " ")
			data = data.replace("&amp;", "&")
			data = data.replace("\r", "")
			data = data.replace("\n", "")
			f.close()
		except:
			return "Error"

		m = re.search('%s</span><br>(.*?)</td>' % day, data)
		if m:
			options = m.group(1)
			options = options.replace("<BR>", " || ")
			options = re.sub('<.+?>', '', options)
		else:
			options = "Error"

		return "Gästis: %s: %s" % (day, options)

mainclass = Lunch
