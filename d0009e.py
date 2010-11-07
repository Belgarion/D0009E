#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import time
import threading
import traceback
import thread
import random
import sys
import re
import signal
import ConfigParser

class ChannelStats:
	def __init__(self):
		self.lastMessage = time.time()
		self.names = []

class Bot:
	def __init__(self):
		self.loadSettings()

		self.channels = {}
		for chan in self.chans:
			self.channels[chan] = ChannelStats()
		self.names_cur_channel = None

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.msg_re = re.compile('^(:([^ ]+))? *([^ ]+) +:?([^ ]*) *:?(.*)$')

		self.joined = False
		self.commands = []
		self.authorized_users = []

		self.loadPlugins()

	def loadPlugins(self):
		self.help = {}
		self.commands = {}
		self.plugins = []
		try:
			reload(__import__('plugins'))
			for i in __import__('plugins').__all__:
				plugin = __import__('plugins.%s' % i, fromlist=[None])
				reload(plugin)
				if "mainclass" in dir(plugin):
					print "Loading", i
					self.plugins.append(plugin.mainclass(self))
		except:
			traceback.print_exc()

	def loadSettings(self):
		self.config = ConfigParser.RawConfigParser()
		self.config.read('d0009e.cfg')

		self.irc_server = (self.config.get('connection', 'server'),
				self.config.getint('connection', 'port'))
		self.nick = self.config.get('connection', 'nick')
		self.chans = self.config.get('connection', 'channels').split()

		admins = self.config.get('users', 'admins')
		self.users = [tuple(i.split(":")) for i in admins.split()]

		self.lastForecast = self.config.getfloat('misc', 'lastForecast')

	def saveSettings(self):
		self.config.set('connection', 'channels', " ".join(self.chans))
		self.config.set('misc', 'lastForecast', str(self.lastForecast))

		admins = " ".join([":".join(i) for i in self.users])
		self.config.set('users', 'admins', admins)

		f = open("d0009e.cfg", "w")
		self.config.write(f)
		f.close()

	def run(self):
		self.running = True

		self.recvThread = RecvThread(self.sock)
		self.recvThread.start()

		self.connect()
		while self.running:
			try:
				self.handleCommands()
			except:
				traceback.print_exc()

			if self.joined:
				for plugin in self.plugins:
					try:
						plugin.on_tick(self)
					except:
						traceback.print_exc()

			time.sleep(0.1)

		self.sock.close()

	def quit(self):
		print "Saving settings"
		self.saveSettings()

		print "Quitting"
		self.sendMessage("QUIT", ":SIGINT")
		self.running = False

		self.recvThread.quit = True
		self.recvThread.join()

	def connect(self):
		self.joined = False
		self.sock.close()

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.recvThread.sock = self.sock

		self.sock.connect(self.irc_server)
		self.sendMessage('USER', '%s 8 *' % self.nick, 'Botten')
		self.sendMessage('NICK', self.nick)

	def registerCommand(self, command, func):
		self.commands[command] = func

	def addHelp(self, command, helpMessage):
		self.help[command] = helpMessage

	def sendMessage(self, action, target, message = ""):
		message = str(message)
		message = message.replace("\r", "")
		message = message.replace("\n", "")

		if len(message) >= 450:
			message = "Error: Message too long"

		if message:
			buf = "%s %s :%s\r\n" % (action, target, message)
		else:
			buf = "%s %s\r\n" % (action, target)

		print "[031m>>[0m", buf,
		while buf:
			sent = self.sock.send(buf)
			buf = buf[sent:]

	def handleCommands(self):
		while self.recvThread.commands != []:
			line = self.recvThread.commands.pop()
			print "[032m<<[0m", line

			m = self.msg_re.match(line)
			source, action, target, message = m.group(2, 3, 4, 5)

			command = message
			args = ""
			if " " in message:
				command = message.split()[0].lower()
				args = message.split()[1:]

			if action.upper() == "001" and not self.joined:
				for chan in self.chans:
					self.sendMessage("JOIN", chan)
				self.joined = True
			elif action.upper() == "PING":
				self.sendMessage("PONG", target)
			elif action.upper() == "ERROR":
				# Reconnect
				time.sleep(30)
				self.connect()
			elif action.upper() == "353": # begin names
				m = re.search('. ([^ ]+) :?(.+)$', message)

				if not m:
					continue

				channel, names = m.group(1, 2)
				if self.names_cur_channel != channel:
					self.channels[channel.upper()].names = []
					self.names_cur_channel = channel

				# Remove prefixes
				names = re.sub(r'[^0-9a-zA-Z\\^\[\]^_`{|} -]', '',  names)

				self.channels[channel.upper()].names.extend(names.split())

			elif action.upper() == "366": # end names
				self.names_cur_channel = None

			elif action.upper() == "PRIVMSG":
				if target.upper() == self.nick.upper():
					if message.upper() == "\001VERSION\001":
						nick = source.split("!")[0].lstrip(":")
						if nick[0] == ":": nick = nick[1:]
						self.sendMessage("NOTICE", nick,
							"\001VERSION Python\001")
					elif message.upper() == "\001TIME\001":
						nick = source.split("!")[0].lstrip(":")
						self.sendMessage("NOTICE", nick,
							"\001Time 13:37 - The time of leet\001")
					elif command.upper() == "AUTH":
						nick, userhost = source.split("!")

						if len(args) >= 2 and (args[0].lower(), args[1]) in self.users:
							self.authorized_users.append(source)

							self.sendMessage("NOTICE", nick,
									"You are now authenticated as %s" % (args[0]))
						else:
							self.sendMessage("NOTICE", nick,
									"Wrong username or password")
				elif target.upper() in self.channels:
					chanstats = self.channels[target.upper()]
					chanstats.lastMessage = time.time()

					if command.upper() == "!RELOAD":
						if not source in self.authorized_users:
							self.sendMessage("PRIVMSG", target,
									"reload: Access denied")
							continue

						print "Reloading"
						self.loadPlugins()
						self.sendMessage("PRIVMSG", target, "reload successful")
						continue

					try:
						if command in self.commands:
							thread.start_new_thread(self.commands[command],
								(self, target, args))
					except Exception, e:
						traceback.print_exc()
						self.sendMessage("PRIVMSG", target, "Error!!")

class RecvThread(threading.Thread):
	def __init__(self, sock):
		self.sock = sock
		self.quit = False
		self.commands = []
		threading.Thread.__init__(self)

	def run(self):
		buffer = ""
		self.sock.settimeout(5)
		while not self.quit:
			try:
				buffer += self.sock.recv(1024)
				commands = buffer.split("\r\n")[:-1]
				buffer = buffer[buffer.rfind("\r\n")+2:]
				for command in commands:
					self.addCommand(command)
			except socket.timeout:
				continue
			except Exception, e:
				traceback.print_exc()
				time.sleep(0.1)

	def addCommand(self, command):
		self.commands.append(command)

b = Bot()

def keyint(signum, frame):
	print "Received signal:", signum
	b.quit()

signal.signal(signal.SIGINT, keyint)

b.run()
