# -*- coding: utf-8 -*-
from pluginbase import PluginBase

import urllib2
import time
import re

class Lunch(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!lunch", self.handleLunch)
		bot.addHelp("lunch", "!lunch resturang (stuk,unik,centrum,husmans,aurorum,rawdeli,dazhong)")

	def cleanHTML(self, text):
		# Finicky characters
		text = text.replace("&#233;", "é");
		text = text.replace("&#201;", "é");
		text = text.replace("&#229;", "å");
		text = text.replace("&#197;", "Å");
		text = text.replace("&#228;", "ä");
		text = text.replace("&#196;", "Ä");
		text = text.replace("&#246;", "ö");
		text = text.replace("&#214;", "Ö");

		# Other finicky characters
		text = text.replace("&nbsp;"," ")
		text = text.replace("&egrave;","é")
		text = text.replace("&eacute;","é")
		text = text.replace("\n \n","")
		text = text.replace("&ldquo;","\"")
		text = text.replace("&rdquo;","\"")
		text = text.replace("\n  ","\n")
		text = text.replace("\r\n","")


		# Markup
		text = re.sub("<br ?/?>", " ", text, re.IGNORECASE);
		text = re.sub("</?strong>","", text, re.IGNORECASE)
		text = re.sub("</?p>","", text, re.IGNORECASE)

		return text


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
			return self.getLunchTeknikensHus(day)
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

	def getHittaLunchen(self, companyID, day):
		print "Checking day " + day
		week = ".."
		options = ""
		try:
			f = urllib2.urlopen("http://www.hittalunchen.se/Access/Meny.aspx?companyID=%d&showHeader=1" % (companyID))
			data = f.read()
			week = re.search("""<div class="lunchMenyHeader">Lunchmeny vecka (\d+)</div>""",data).groups(0)[0]
			dagdish =  re.search("""<div class="day"><span class="name">"""+day+"""</span>(.*?)<div class="always">""",data,re.DOTALL | re.MULTILINE).groups(1)[0]
			dishName = re.findall("""<div class="title">(.*)</div>""",dagdish)
			dishPrice = re.findall("""<div class="price">(.*)</div>""",dagdish)
			for i in range(len(dishName)):
				options += "%s %s, " % (dishName[i],dishPrice[i])
			f.close()
		except Exception,e:
			# This happens when the day isn't on the menu, i.e. if you try !lunch at 14:00 on a friday.
			return "Stängt."
		return "%s v%s: %s" % (day, week, options)


	def getLunchUnik(self, day):
		return "Uni:k " + self.getHittaLunchen(66,day)

	def getLunchAurorum(self, day):
		return "Aurorum " + self.getHittaLunchen(5, day)

	# TODO: Fold this into getHittaLunchen (these dudes use the <description> field for 95% of their info.)
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

	def getLunchCentrum(self, day):
		week = ".."
		day = day.split(" ")[0] 
		try: 
			f = urllib2.urlopen("http://www.amica.se/centrumrestaurangen")
			data = f.read()
			meny = re.search("""<h2>Centrumrestaurangen LTU<br /></h2>(.*?)<div class="boxFoot">""",data,re.DOTALL | re.MULTILINE)
			menyData = meny.groups(1)[0].replace("&aring;","å").replace("&amp;","&").replace("&auml;","ä").replace("&ouml;","ö")

			if day != "Fredag": menyDay = re.findall("""<h2>.*?"""+day+""".*?</h2>(.*?)<h2>""",menyData,re.DOTALL | re.MULTILINE)
			else: menyDay = re.findall("""<h2>.*?Fredag.*?</h2>(.*)""",menyData,re.DOTALL | re.MULTILINE)

			dishes = menyDay[0]
			dishes = dishes.replace("\r\n<p>","\n")
			dishes = self.cleanHTML(dishes)

			week = re.findall("""Matsedel vecka (..)""",menyData)[0].replace("\r\n","")

			dishesParsed = re.findall("""([ a-zA-ZåäöÅÄÖ]*?:.*?:-)""",dishes,re.DOTALL | re.MULTILINE)
			out = ""
			last = 0
			for n,p in enumerate(dishesParsed):
				i = p.replace("\n","").replace("\t","").replace("   "," ").replace("   "," ").replace("  "," ")
				if len(i)+last > 90:
					i += "\n"
					last = 0
				else:
					last += len(i)
					if n != len(dishesParsed)-1: 
						i += " || "
				out += i
			f.close()
		except:
			return "Error"

		return ["[Centrumresturangen: %s v.%s] " % (day, week)] + out.split("\n")

	def getLunchTeknikensHus(self, day):
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

		m = re.search('<span class=PublicBreadcrumItem>Vecka (\d+)</span>', data)
		if m:
			week = m.group(1)

		daymap = {"måndag"  : "monday",
							"tisdag"  : "tuesday",
							"onsdag"  : "wednesday",
							"torsdag" : "thursday",
							"fredag"  : "friday"}
		if day.lower() in daymap.keys():
			engday = daymap[day.lower()]
		else:
			return "Teknikens Hus: Stängt."


		maincourse = "ERROR"
		pasta = "ERROR"
		salad = "ERROR"
		veggie = "ERROR"

		m = re.search('<span id="ctl00_MainContent_m_%s">(.*?)</span>' % engday, data.replace("\n",""))
		if m:
			maincourse = m.group(1)

		m = re.search('<span id="ctl00_MainContent_m_%s">(.*?)</span>' % "extra1", data.replace("\n",""))
		if m:
			pasta = m.group(1)

		m = re.search('<span id="ctl00_MainContent_m_%s">(.*?)</span>' % "extra2", data.replace("\n",""))
		if m:
			salad = m.group(1)

		m = re.search('<span id="ctl00_MainContent_m_%s">(.*?)</span>' % "extra3", data.replace("\n",""))
		if m:
			veggie = m.group(1)


		maincourse = self.cleanHTML(maincourse)
		pasta = self.cleanHTML(pasta)
		salad = self.cleanHTML(salad)
		veggie = self.cleanHTML(veggie)

		return [
							"Teknikens Hus: %s vecka %s:" % (day, week),
							"Huvudrätt: %s" % maincourse,
							"Pasta:  %s" % pasta,
							"Sallad: %s" % salad,
							"Veg:    %s" % veggie
					 ]


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
