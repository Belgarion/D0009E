# -*- coding: utf-8 -*-
from pluginbase import PluginBase

import urllib2
import re

class Course(PluginBase):
	def __init__(self, bot):
		bot.registerCommand("!course", self.handleCourse)
		bot.registerCommand("!kurs", self.handleCourse)
		bot.addHelp("kurs", "Usage: !kurs <kurskod>")

	def handleCourse(self, bot, channel, params):
		bot.sendMessage("PRIVMSG", channel, self.getCourse("%20".join(params)))

	def getCourse(self, courseCode):
		courseCode = courseCode.upper()
		if len(courseCode) != 6:
			return "Invalid course code"

		try:
			url = "http://www.ltu.se/edu/course/%s/%s?ugglanCat=student" % (courseCode[:3], courseCode)
			f = urllib2.urlopen(url)
			data = f.read()
			f.close()
		except urllib2.HTTPError, e:
			return "Error: %s" % e.code

		m = re.search("<title>\n?(.*)\n?</title>", data)
		if m:
			return "%s : %s" % (m.group(1), url)
		return "Course not found"

mainclass = Course
