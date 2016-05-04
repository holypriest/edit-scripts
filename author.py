#!/usr/bin/python
# -*- coding: utf-8 -*-

class Author:

	def __init__(self, info):
		self.name = info[0]
		self.gender = info[1]
		self.language = info[2]
		self.mail = info[3]

	def speaks_portuguese(self):
		if (self.language == 'pt'): return True
		else: return False
