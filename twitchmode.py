#!/usr/bin/env python

# A simple tool, that will connect to twitch chat with the given oauth-key and 

# Imports
import socket
import re
import json
from pynput import keyboard

# Initializing global variables
settingsFile = "config.json"
debug = "True"

host = "irc.twitch.tv"
port = 6667
channel = ""
username = "" # Twitch account name for the user you want to send the messages as
oauth = "" # Twitch password token for the user you want to send the messages as

keyA = ""
keyB = ""
keyC = ""
keyD = ""
keyE = ""

default = json.dumps({
	"host": "irc.twitch.tv",
	"port": 6667,
	"joinchannel": "",
	"username": "",
	"oauth": "",
	"keyA":"Key.f1",
	"keyB":"Key.f2",
	"keyC":"Key.f3",
	"keyD":"Key.f4",
	"keyE":"Key.f5",
	"debug":"False"}
	, indent=4)

# Initializing socket for connecting to 
s = socket.socket()

# Reads the first line from the auth.ini file, placed in the working folder, and places the first line to the 
def checkSettings():
	try:
		with open(settingsFile) as json_data_file:
			data = json.load(json_data_file)
		
		global host
		global port
		global channel
		global username
		global oauth
		
		global keyA
		global keyB
		global keyC
		global keyD
		global keyE
		
		global debug
		
		host = data["host"]
		port = data["port"]
		channel = data["joinchannel"]
		username = data["username"]
		oauth = data["oauth"]
		
		keyA = data["keyA"]
		keyB = data["keyB"]
		keyC = data["keyC"]
		keyD = data["keyD"]
		keyE = data["keyE"]
		
		debug = data["debug"]
		
		print("Posting in channel: %s"%channel)
		print("as user: %s"%username)
		
	except:
		print("File %s does not exist!"%settingsFile)
		try:
			print("Creating configuration file...")
			
			f = open(settingsFile, "a")
			f.write(str(default))
			f.close()
			
			print("%s created!"%settingsFile)
			print("Go fill in your settings.")
			#with open("config2.json") as outfile:
			#json.dump(default, outfile)
		except:
			print("Failed to create %s"%settingsFile)
	
def connectIRC():
	s.connect((host, port))
	
	msg = "PASS " + oauth + "\r\n"
	s.send(msg.encode())
	
	msg = "NICK " + username + "\r\n"
	s.send(msg.encode())
	
	msg = "JOIN #" + channel + "\r\n"
	s.send(msg.encode())
	
def sendMessage(msg):
	#if msg != "False":
	sendThis = "PRIVMSG #" + channel +  " :" + msg + "\r\n"
	s.send(sendThis.encode())
	print("Sent message %s"%msg)

def checkKey(key):
	switcher = {
		keyA:"#A",
		keyB:"#B",
		keyC:"#C",
		keyD:"#D",
		keyE:"#E"
	}
	if switcher.get(key, "False") != "False":
		sendMessage(switcher.get(key, "False"))

def on_release(key):
	if debug == "True":
		print("{0}".format(key))
		if key == keyboard.Key.esc:
        # Stop listener
			return False
	else:
		checkKey("{0}".format(key))

		
# Announce the program
print("########## TwitchMode ##########")
# Check settings
checkSettings()

# Connect to Twitch chat
if debug != "True":						# Check if debugging
	if username != "" and oauth != "": 	# Check if username and oauth is set
		if channel != "":
			connectIRC()				# If these are set, call for connectIRC to connect to Twitch chat
		else:
			print ("Channel you want to join is not set!")
			print("Please set in in %s"%settingsFile)
	else:
		print("Username or user oauth token not set!")
		print("Please set them in %s"%settingsFile)
else:
	print("Debugging enabled! Not connecting...")
	print("Set value debug to \"False\" in %s to disable debugging"%settingsFile)
		
# Collect events until released
with keyboard.Listener(on_release=on_release) as listener:
    listener.join()

