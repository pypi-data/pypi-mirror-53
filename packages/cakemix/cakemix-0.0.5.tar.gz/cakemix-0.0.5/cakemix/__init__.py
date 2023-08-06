# -*- coding: utf-8 -*-
"""
cakemix
~~~~~

Cakemix is a Python library to make the business life easier. It uses standard Python libraries and simplifies opening/writing excel spreadsheets, 
comparing data in several spreadsheets, making ppt files, to reading pdf files.
It also has functions to automate the routine work like emailing, sending
reminders.

:copyright: © 2019 by Mesut Varlioglu, PhD.
:license: BSD, see LICENSE.rst for more details.
"""

#List classes
from .list import findUniqueList, findFilesDirectory, extractData

#Web classes
from .web import openURL, getLinks

#Excel classes
from .excel import readExcel, get_column, plotBarData, plotHistData, plotLineData, plotScatterData

#Flask GUI classes
from .flask_gui import *

#Email classes
from .e_mail import sendEmail

#Database classes
from .db import makeDB

#Spell classes
#from .spell import correction, candidates, known, edits1, edits2


name = "cakemix"
__version__ = '0.0.5'
