# -*- coding: utf-8 -*-
from pluginbase import PluginBase

import urllib2
import time
import re

class Lunch(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!lunch", self.handleLunch)
		bot.addHelp("lunch", "!lunch resturang (stuk,unik,centrum,husmans,aurorum,rawdeli,dazhong)")

	def handleLunch(self, bot, channel, params):
		msg = self.getLunch(" ".join(params))
		bot.sendMessage("PRIVMSG", channel, msg)

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
		elif place.lower() == "rawdeli":
			return self.getLunchRawDeli(day)
		elif place.lower() == "dazhong":
			return self.getLunchDazhong()

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
	def getLunchDazhong(self):
		return "Dazhong: Vi serverar åtta varmrätter, salladsbuffé och nybakat bröd varje dag. Kaffe med Friterade bananer och glass till efterrätt. 75:-"
	def getLunchUnik(self, day):
		week = ".."
		options = ""
		try:
			f = urllib2.urlopen("http://www.hittalunchen.se/Access/Meny.aspx?companyID=66&amp;css=unik&amp;showHeader=1")
			data = f.read()
			dagdish =  re.search("""<div class="day"><span class="name">"""+day+"""</span>(.*?)<div class="always">""",data,re.DOTALL | re.MULTILINE).groups(1)[0]
			week = re.search(""" <div class="lunchMenyHeader">Lunchmeny vecka (..)</div>""",data).groups(0)[0]
			dishName = re.findall("""<div class="title">(.*)</div>""",dagdish)
			dishPrice = re.findall("""<div class="price">(.*)</div>""",dagdish)
			for i in range(len(dishName)):
				options += "%s %s, " % (dishName[i],dishPrice[i])
			f.close()
		except:
			return "Error"

		return "Uni:k: %s %s: %s" % (day, week, options)

	def getLunchRawDeli(self, day):
		week = ".."
		options = ""
		try:
			f = urllib2.urlopen("http://www.hittalunchen.se/Access/Meny.aspx?companyID=82&amp;css=unik&amp;showHeader=1")
			data = f.read()
			dagdish =  re.search("""<div class="day"><span class="name">"""+day+"""</span>(.*?)<div class="always">""",data,re.DOTALL | re.MULTILINE).groups(1)[0]
			week = re.search(""" <div class="lunchMenyHeader">Lunchmeny vecka (..)</div>""",data).groups(0)[0]
			dishName = re.findall("""<div class="title">(.*)</div>""",dagdish)
			dishDesc = re.findall("""<div class="description">(.*)</div>""",dagdish)
			dishPrice = re.findall("""<div class="price">(.*)</div>""",dagdish)
			for i in range(len(dishName)):
				options += "\n-%s- %s %s" % (dishName[i],"\n"+dishDesc[i].replace("<br /> ","\n").replace(" <br />","\n").replace("<br />","\n"),dishPrice[i])
			f.close()
		except:
			return "Error"
		return ["Trasigt mycket output, klaga på yugge", "RAW DELI: %s v%s:" % (day, week)] + options.split("\n")

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
		week = ".."
		day = day.split(" ")[0] 
		try:
			f = urllib2.urlopen("http://www.amica.se/centrumrestaurangen")
			data = f.read()
			r = re.search("""<h2>Centrumrestaurangen LTU<br /></h2>(.*?)<p>&nbsp; &nbsp; <strong></strong></p>""",data,re.DOTALL | re.MULTILINE)
			rdata = r.groups(1)[0].replace("&aring;","å").replace("&amp;","&").replace("&auml;","ä").replace("&ouml;","ö")

			if day != "Fredag": rday = re.findall("""<h2>.*?"""+day+""".*?</h2>(.*?)<h2>""",rdata,re.DOTALL | re.MULTILINE)
			else: rday = re.findall("""<h2>.*?Fredag.*?</h2>(.*)""",rdata,re.DOTALL | re.MULTILINE)

			options = rday[0].replace("\r\n<p>","\n").replace("&nbsp;"," ").replace("&egrave;","é").replace("&eacute;","é").replace("<strong>","").replace("</strong>","").replace("</p>","").replace("\n \n","").replace("&ldquo;","\"").replace("&rdquo;","\"").replace("\n  ","\n").replace("\r\n","")
			week = re.findall("""Matsedel vecka (..)""",rdata)[0].replace("\r\n","")
			f.close()
		except:
			return "Error"

		return ["Massiv output, klaga på yugge",
			"Centrumresturangen: %s v.%s:" % (day, week)] + options.split("\n")

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
