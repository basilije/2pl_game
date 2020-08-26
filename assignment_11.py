#! /usr/bin/python3

# Reaction Game
# Author: Vasilije Mehandzic (still no comments, sorry)

import tty
import sys
import termios
import time
import os
import random

def getKey():
	orig_settings = termios.tcgetattr(sys.stdin)
	tty.setcbreak(sys.stdin)	
	key = ''
	while key=='':
		key = sys.stdin.read(1)[0]
	return(key)

def clearScreen():
	os.system('clear')	
	
def ti(t):
	return time.time()-t

def keyDescription(kd):
	knd = []
	for kds in kd:
		if kds.upper() == "A":
			knd.append('*** A - Add/Remove players from the current game')	
		if kds.upper() == "C":
			knd.append('*** C - Display current players names and scores')	
		if kds.upper() == "T":
			knd.append('*** T - Display top ten players names and scores')	
		if kds.upper() == "S":
			knd.append('*** S - Start a round')	
		if kds.upper() == "E":
			knd.append('*** E - Exit the game')	
		if kds.upper() == "+":
			knd.append('*** + - Add a player')	
		if kds.upper() == "-":
			knd.append('*** - - Remove a player')	
		if kds.upper() == "L":
			knd.append('*** L - List players')	
		if kds.upper() == "ESC":
			knd.append('*** ESC - Step back')	
	return knd
	
def currentPlayers(score=False):
	to_return = []
	if score:
		for pl, sc in zip(current_players, current_scores):
			to_return.append((pl, sc))
	else:
		for pl in current_players:
			to_return.append((pl))
	return to_return

def currentPlayersAndScore():
	printnClear(" >>> currentPlayersAndScore", True)
	co, sp = 1, ' '
	for pl, sc in zip(current_players, current_scores):
		if co>9:
			sp = ''
		print(sp,co, '.', '{:.5f}'.format(sc), '  _________ ', pl)
		co += 1

def enterKeySequence():
	key, name = ' ', ''
	while (ord(key) != 10):
		key = getKey()
		if (ord(key) != 8):
			name += key
		else:
			if len(name) > 0:
				name = name[0:len(name)-1]
		print(name + "                             ", end='\r')
	return name

def printnClear(arg, clear = False):
	try:
		if clear:
			clearScreen()
		print(arg)
	except Exception as ex:
		print("Error printnClear ", ex.type(), ex.args)
		
def addPlayer():
	printnClear(" >>> addPlayer", True)
	printnClear("player name?")
	new_name = enterKeySequence()
	new_name = new_name[0:len(new_name)-1]
	current_players.append(new_name)
	current_scores.append(99.99999)
	printnClear(" just added")
	
def removePlayer():
	printnClear(" >>> removePlayer", True)
	co = 1
	for cp in current_players:
		print(co, cp)
		co += 1
	printnClear(" which one?", False)
	which_player = enterKeySequence()
	try:
		wp = int(which_player)
		if (wp <= len(current_players)) and (wp <= len(current_scores)):
			current_players.remove(current_players[wp-1])	
			current_scores.remove(current_scores[wp-1])	
			printnClear(" just deleted", False)
	except Exception as ex:
		print("Error removing player", ex.type(), ex.args)

def listPlayers():
	co = 1
	for cp, cs in zip(current_players, current_scores):
		print(co, cp, cs)
		co += 1	

def addRemovePlayers():
	printnClear(" >>> addRemovePlayers", True)
	key = ' '
	while ((ord(key) != 27) and (ord(key) != 10)):
		print()
		for kd in (keyDescription(['+', '-', 'l', 'ESC'])):
			print(kd)
		key = getKey()
		if key.upper()=="+":
			addPlayer()
		if key.upper()=="-":	
			removePlayer()	
		if key.upper()=="L":	
			listPlayers()	
	
def topTenPlayers():
	printnClear(' >>> topTenPlayers', True)
	try:
		all_ps = []
		all_players, all_scores = load()		
		for apla, asco in zip(all_players, all_scores):
			if (apla!='' and asco!=''):
				all_ps.append((apla, asco))
				
		top_ten = sorted(all_ps, key=lambda x : x[1])[:10]	
		print("__    ")
		co,sp = 1, ' '		
		for tt in top_ten:
			if co>9:
				sp = ''
			print(sp,co, '. {:.5f}'.format(float(tt[1])), '&:} ', '  _________ ', tt[0])
			co += 1		
		print("__    ")
	except Exception as ex:
		print("Error @ top ten ", ex.type(), ex.args)
			
def randSleep(sleep=1):
	return random.randint(1,1000)/1000

def startARound():
	printnClear(' >>> startARound', True)
	current_scores, co = [], 0
	for pl in current_players:
		clearScreen()
		printnClear('  <<prepare>> ' + str(pl))	
		wait()
		printnClear('  <<<<get>>>> ' + str(pl))
		time.sleep(randSleep())
		printnClear('  <<<set>>> ' + str(pl))
		time.sleep(randSleep())
		printnClear('  << ready>> ' + str(pl))
		time.sleep(randSleep(2))
		clearScreen()
		time.sleep(randSleep(2))
		ti=time.time()
		printnClear('    GO    ')
		key = getKey()
		sc = time.time() - ti
		printnClear("REACTION TIME: " + str(sc))
		current_scores.append(sc)
		wait()

def exitTheGame():
	printnClear(' >>> exitTheGame', True)
	time.sleep(1)

def fileToList(file_name):
	the_list = []
	if not(os.path.exists(file_name)):
		open(file_name, 'w+').close()		
	with open(file_name, 'r') as file_handle:
		for line in file_handle:			
			the_list.append(line[:-1])
	return the_list

def mainMenu(clear=True):
	if clear:
		clearScreen()
	for kd in keyDescription(["A", "C", "T", "S", "E"]):
		printnClear(kd)

def load():
	all_players, all_scores = [], []
	all_players = fileToList(players_file_name)
	all_scores = fileToList(scores_file_name)
	return all_players, all_scores

def save(players_file_name, scores_file_name, players, scores):		
	with open(players_file_name, 'w') as file_handle:
		for listitem in players:
			file_handle.write('%s\n' % listitem)
	with open(scores_file_name, 'w') as file_handle:
		for listitem in scores:
			file_handle.write('%s\n' % listitem)
	printnClear('just saved')
	
def wait(no_excuse_sleep=0):
	time.sleep(no_excuse_sleep)
	key, pr = ' ', ''
	while  ((ord(key) != 27) and (ord(key) != 10)):
		key = getKey()
		pr += '*'
		print(pr, end='\r')
	
printnClear("---------------")
players_file_name = 'players.txt'
scores_file_name = 'scores.txt'
all_players, all_scores = load()
printnClear(all_players)
printnClear(all_scores)
printnClear("---------------")
current_players = []
current_scores = []

key, tim = ' ', time.time()
while key.upper()!="E":
	mainMenu()
	key = getKey()
	if key.upper()=="A":
		addRemovePlayers()
		wait()
	if key.upper()=="C":
		currentPlayersAndScore()
		wait()
	if key.upper()=="T":
		topTenPlayers()
		wait()
	if key.upper()=="S":
		startARound()
		wait()
	
for pl, sc in zip(current_players, current_scores):
	all_players.append(pl)
	all_scores.append(sc)
	
save(players_file_name, scores_file_name, all_players, all_scores)
