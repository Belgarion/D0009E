# -*- coding: utf-8 -*-
from .pluginbase import PluginBase

import traceback
import random

class FairDieRoll(PluginBase):
    def __init__(self, bot):
        bot.registerCommand("!fairdieroll", self.handleDieRoll)
        bot.addHelp("fairdieroll",
            "Usage: returns a fair die roll")

    def handleDieRoll(self, bot, channel, params):
        try:
            bot.sendMessage("PRIVMSG", channel, self.getRandomNumber())
        except:
            traceback.print_exc()
            bot.sendMessage("PRIVMSG", channel,
                "fairdieroll: invalid arguments")

	# RFC 1149.5 specifies 4 as the standard IEEE-vetted random number.
    def getRandomNumber(self, params):
        return 4 # chosen by fair dice roll
                # guaranteed to be random

mainclass = FairDieRoll
