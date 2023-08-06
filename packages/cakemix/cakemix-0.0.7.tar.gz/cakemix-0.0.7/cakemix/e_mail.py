# -*- coding: utf-8 -*-

import win32com.client as win32
import datetime

now = datetime.datetime.now()

def sendEmail(mailTo,subject,body):
    '''Example: for single recipient: 
            sendEmail('email@example.com','First email subject','Email body as how are you?') 
        for multiple recipients: 
            sendEmail('email@example.com;email1@example.com','First email subject','Email body as how are you?') 
    You need to have Outlook installed on your computer and set for sending emails
    '''
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = mailTo
    mail.Subject = subject
    mail.Body = body
    #mail.HTMLBody = '''<html>'''

    #To attach a file to the email (optional):
    #attachment  = "e:\\data\python\\plot3.png"
    #mail.Attachments.Add(attachment)
    
    mail.Send()