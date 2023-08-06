
Cakemix is a Python library to open Office documents, automate the data analysis and making presentations

To install first time:
pip install cakemix

To upgrade:
pip install --upgrade cakemix


USAGE:

# importing cakemix.excel functions
from cakemix.excel import readExcel, get_column, plotBarData

# reading excel file. You can find this file in github: https://github.com/varlmes/python/blob/master/datatable_sample.xlsx
data=readExcel('C:\data\python\cakemix\datatable_sample.xlsx','Sheet1')

#showing the data
data

# getting the first column of data
result1=get_column(data,0)

# printing
result1[2:]

# getting the second column of data
result2=get_column(data,5)

# printing
result2[2:]

#plotting the data
plotBarData(result1[2:],(result2[2:]),'Salary','Name')


Example 2: from cakemix import list

from cakemix.list import *
out=findUniqueList([1,3,3,4,5,5,6])

Example 3: sending email

from cakemix.e_mail import sendEmail

For single recipient: 
	sendEmail('email@example.com','First email subject','Email body as how are you?') 
For multiple recipients: 
	sendEmail('email@example.com;email1@example.com','First email subject','Email body as how are you?') 
Requirements: You need to have Outlook installed on your computer and set for sending emails


Example 4: make sqlite database
	from db import makeDB
	makeDB('database.db')