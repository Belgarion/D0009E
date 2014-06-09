# -*- coding: utf-8 -*-
from .pluginbase import PluginBase

import urllib.request, urllib.error, urllib.parse
import time
import re

class Tenta(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!tenta", self.handleTenta)
		bot.addHelp("tenta", "Usage: tenta <kurskod>")

	def handleTenta(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel, self.getTenta(" ".join(params)))

	def getTenta(self, course):
		try:
			url = "https://portal.student.ltu.se/tentapub/plokal.php?" \
				+ "villkor=+and+t_schema.kurs%%3D'%s'&sortering=1" % (course)
			f = urllib.request.urlopen(url)
			data = f.read()
			data = data.replace("&nbsp;", " ")
			data = data.replace("\n", "")
			data = data.replace("\r", "")
			data = data.replace("\t", "")

			#print data
			m = re.search('tabellen med tentorna b.rjar -->'
					+ '(.*?)<!-- tabellen med tentorna slutar', data)
			if m:
				tentor = m.group(1).replace("<tr", "\n<tr").replace("</td>","; ")
				tentor = re.sub(r'<.+?>', '', tentor)

				results = []
				header = ''
				for t in tentor.split('\n'):
					if t == '': continue
					t = t.split(";")
					if header == '':
						header = t
						continue

					line = ''
					for i, c in enumerate(t):
						line += "%s: %s, " % (header[i].strip(), c.strip())

					results.append(line)


				print(results)
				if len(results) > 2:
					return results[:1]+['And (%d) more ( %s )' % (len(results) - 1, url)]
				return results
			else:
				return "Error"
		except Exception as e:
			return e

mainclass = Tenta
