#!/usr/bin/python
# -*- coding: utf-8 -*-

from author import Author
from manuscript import Manuscript
import category
import subprocess
import os

class Letter:

	def __init__(self, auth, ms):
		self.number = ms.category + '-' + ms.number
		self.language = self.set_language(auth)
		self.category = self.set_category(ms)
		self.text = self.set_text(auth)

	def set_opening(self, auth):
		if (self.language == 'pt'):
			if (auth.gender == 'm'): return 'Prezado Prof. ' + auth.name + ','
			else: return 'Prezada Profª. ' + auth.name + ','
		else: return 'Dear Dr. ' + auth.name + ','

	def set_language(self, auth):
		if (auth.speaks_portuguese()): return 'pt'
		else: return 'en'

	def set_category(self, ms):
		if (self.language == 'pt'): return category.category_pt[ms.category]
		else: return category.category_en[ms.category]

	def set_text(self, auth):
		if (self.language == 'pt'): text = open('gpqn.tex', 'r')
		else: text = open('gpqn-en.tex')
		data = text.read()
		text.close()
		data = data.replace('#cat#', self.category)
		data = data.replace('#num#', self.number)
		data = data.replace('#opn#', self.set_opening(auth))
		return unicode(data, 'utf-8')

	def generate(self):
		newfile = 'GP ' + self.number + '.tex'
		output_file = open(newfile, 'w')
		output_file.write(self.text.encode('utf-8'))
		output_file.close()
		subprocess.call(['pdflatex', newfile])
