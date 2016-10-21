# -*- coding: utf-8 -*-
from .pluginbase import PluginBase

import traceback
import random

class NewUser(PluginBase):
    def __init__(self, bot):
        bot.registerCommand("!newuser", self.handleNewUser)
        bot.addHelp("newuser",
            "Usage: returns link to registration")

    def handleNewUser(self, bot, channel, params):
        try:
            bot.sendMessage("PRIVMSG", channel, "New to LUDD? Register at https://vortex.ludd.ltu.se/register")
        except:
            traceback.print_exc()
            bot.sendMessage("PRIVMSG", channel,
                "newuser: invalid arguments")

mainclass = NewUser
