# -*- coding: utf-8 -*-
from .pluginbase import PluginBase

import random
import time
import .talking

class QuietMessages(PluginBase):
	def __init__(self, bot):
		self.quiet_messages = \
			["It's awfully quiet around here.",
			"Is anyone there?", "The cake is a lie",
			"We're a lot alike, you and I. You tested me. I tested you. "\
				"You killed me, I... oh no, wait. I guess I haven't "\
				"killed you yet. Well... food for thought.",
			"Your entire life has been a mathematical error. "\
				"A mathematical error I'm about to correct.",
			"I see you.", "Hellooo!", "Who's there?", "Target lost...",
			"Hey, look at that thing! No, that other thing!",
			"He who controls the past commands the future, " \
				"He who commands the future, conquers the past.",
			"><(((('>",
			"The only reason there's such thing as mornings in the first place is to keep night and afternoon bumping into each other.",
			"The nice thing about repetitions is that you sort of know what to expect.",
			"Never trust a Game Master with a big smile.",
			"Gravity is a habit that is hard to shake off.",
			"To err is human... to really foul up requires the root password.",
			"Life would be so much easier if we only had the source code.",
			"Unix is user-friendly. It's just very selective about who its friends are.",
			"""\"Real men don't use backups, they post their stuff on a public ftp server and let the rest of the world make copies."  - Linus Torvalds""",
			"The nice thing about standards is that there are so many to choose from."
			]

	def on_tick(self, bot):
		self.sendQuietMessages(bot)

	def sendQuietMessages(self, bot):
		for channel, chanstats in bot.channels.items():
			if time.time() - chanstats.lastMessage > 24*60*60: # After 24 hours
				chanstats.lastMessage = time.time()
				try:
					bot.sendMessage("PRIVMSG",
							channel, random.choice(self.quiet_messages))
				except:
					traceback.print_exc()

mainclass = QuietMessages
