#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Simple menu system class that I wrote.
Copyright (C) 2008-2013  James Shubin
Written by James Shubin <james@shubin.ca>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# HISTORY:
# - this code was written during _my_ personal time as a student.
# - my menu system was done with the `code and fix software engineering model'
# - i bet it's just as strong and bug free as anyone elses :P
# - on a serious note, it's really solid i think. check the nice features!
# - i hereby release it for use under the above AGPLv3 license.
# - please email me any patches, comments or feedback.

# CHANGELOG:
# v0.1: ??/??/???? initial code base (written around 2007)
# v0.2: 30/07/2009 fixed a small submenu bug, and added changelog

#TODO: wherever validation of an add_entry fails, we print error, raise exception and return false.
#	these are all listed here, but obviously they are superfluous, remove either print, raise or both.
import os
import sys
class menu_system:
	"""a simple menu system class"""

	def __init__(self, title='menu', prompt='$ '):
		"""the constructor"""
		self.prefix = ''	# sandwich the key
		self.postfix = ') '	# close the sandwich
		# 76 = 80 - (3 + 1)
		# max = default screen char width - (# menu item chars + 1 letter char + 1 end of line space)
		self.maxtextlen = 80 - (len(self.prefix) + len(self.postfix) + 1 + len(os.linesep))

		self.title = title	# the menu title
		self.prompt = prompt	# the menu prompt
		self.entries = []	# list of menu items

		self.myout = sys.stdout	# set these if you would like different
		self.myerr = sys.stderr # they need to have a write() method


	def add_entry(self, key, text, pos=None, sub=None):
		"""add entries to our menu:
		key is single A-Z, a-z letter choice, no duplicates
		text is text you want to display
		sub is None for regular function
		sub is lambda function or function for something to happen on press
		if the function returns true, then menu returns,
		otherwise it loops in menu
		sub is a built menu_system class if you want a sub menu to run and return next
		"""
		# validation
		if not(type(key) is str and type(text) is str):
			self.myerr.write('key and text parameters must be strings' + os.linesep)
			raise Exception('key and text parameters must be strings')
			return False

		if len(key) != 1 or len(text) > self.maxtextlen:
			self.myerr.write(('key must be one char, text must be max %d' % self.maxtextlen) + os.linesep)
			raise Exception('key must be one char, text must be max %d' % self.maxtextlen)
			return False

		if (ord(key) >= ord('A') and ord(key) <= ord('Z')) or (ord(key) >= ord('a') and ord(key) <= ord('z')):
			# check to avoid duplicate keys
			for x in self.entries:
				if x['key'] == key:
					self.myerr.write('key must be unique to this menu' + os.linesep)
					raise Exception('key must be unique to this menu')
					return False

			#TODO: we could add truncation of text if it's too long
			temp = {'key': key, 'text': text, 'sub': sub}
			if pos == None: pos = len(self.entries)	# append if pos is not specified
			self.entries.insert(pos, temp)		# inserts item at desired position
			return True	# happy

		else:
			self.myerr.write('bad key for menu entry' + os.linesep)
			raise Exception('bad key for menu entry')
			return False


	def run(self):
		"""runs the menu system, returns selected letter"""
		while True:

			sys.stdout.write(self.title + os.linesep) # print title
			for x in self.entries:
				sys.stdout.write(self.prefix + x['key'] + self.postfix + x['text'] + os.linesep)

			try: # do safe/smart prompt
				answer = '' # safe
				answer = raw_input(self.prompt)

			except EOFError: # user pressed ^D
				self.myerr.write('you pressed ^D' + os.linesep)
				return False

			except KeyboardInterrupt:
				self.myerr.write('you pressed ^C' + os.linesep)
				return False

			#self.myerr.write(('you pressed %s\n' % answer) + os.linesep) #DEBUG

			# validate answer
			if len(answer) != 1:
				self.myerr.write('invalid menu entry' + os.linesep)
				self.myerr.write(os.linesep)
				continue

			# look for answer
			found = False
			for x in self.entries:
				if x['key'] == answer:
					found = True
					if type(x['sub']) in [type(None)]:
						return x['key']

					elif type(x['sub']) in [type(lambda: True)]:
						# lambda functions that run each time
						# if they return true, you exit menu
						# if they return false, stay in menu
						if x['sub'](): return x['key']
						else: continue

					elif type(x['sub']) in [type(menu_system())]:
						# sub menu system
						self.myout.write(os.linesep)
						recurse = x['sub'].run()
						if not(type(recurse) is str): recurse = '0'
						return x['key'] + recurse

			if not(found):
				self.myerr.write('invalid menu entry' + os.linesep)
				self.myerr.write(os.linesep)
				continue

if __name__ == '__main__':

	# example 1
	def printfoo():
		print 'i am printing foo!'
		return False	# make it stay and loop

	sub = menu_system('sub menu', 'enter a letter> ')
	sub.add_entry('x', 'this is x')
	sub.add_entry('y', 'this is y')
	sub.add_entry('z', 'this is z')
	sub.add_entry('q', 'choose `q\' to quit')

	thing = menu_system('main menu\n---------', '\n$ ')
	thing.add_entry('a', 'this is letter a')
	thing.add_entry('b', 'be prepared!')
	thing.add_entry('c', 'the answer is always c (submenu!)', sub=sub)
	thing.add_entry('w', 'loop this menu', sub=lambda: False)
	thing.add_entry('E', 'escape this menu', sub=lambda: True)
	thing.add_entry('p', 'printfoo() and loop', sub=printfoo)
	thing.add_entry('q', 'choose `q\' to quit')

	print 'the chosen letter is: ' + str(thing.run())


	# example 2
	menua = menu_system('menu a: animals\n---------------')
	menua.add_entry('a', 'a is for alligator')
	menua.add_entry('b', 'b is for baboon')
	menua.add_entry('c', 'c is for cheetah')

	menub = menu_system('menu b: food\n------------')
	menub.add_entry('a', 'a is for apple')
	menub.add_entry('b', 'b is for banana')
	menub.add_entry('c', 'c is for carrot')

	menua.add_entry('x', 'goto food menu', sub=menub)
	menub.add_entry('x', 'goto animals menu', sub=menua)

	menua.add_entry('q', 'choose `q\' to quit')
	menub.add_entry('q', 'choose `q\' to quit')

	print 'the chosen letter is: ' + str(menua.run())

