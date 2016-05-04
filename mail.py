#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders

user = "user"
pwd = "secret"
bcc = "someone@somewhere.com.br"

class Mail:

    def __init__(self, auth, ms):
        self.from_address = user + '@somewhere.com.br'
        self.to_address = auth.mail
        self.language = self.set_language(auth)
        self.subject = self.set_subject(ms)
        self.body = self.set_body(auth, ms)

    def set_language(self, auth):
        if (auth.speaks_portuguese()): return 'pt'
        else: return 'en'

    def set_opening(self, auth):
        if (self.language == 'pt'):
            return 'Prezado(a) Prof(a). ' + auth.name + ','
        else: return 'Dear Dr. ' + auth.name + ','

    def set_subject(self, ms):
        msid = ms.category + '-' + ms.number
        if (self.language == 'pt'): return '[Your Company] Seu manuscrito %s está disponível online' % (msid)
    else: return '[Your Company] Your manuscript %s is available online' % (msid)

    def set_body(self, auth, ms):
        if (self.language == 'pt'): text = open('message_pt.html', 'r')
        else: text = open('message_en.html')
        data = text.read()
        text.close()
        data = data.replace('#opn#', self.set_opening(auth))
        data = data.replace('#num#', ms.number)
        return unicode(data, 'utf-8')

    def send(self):
        msg = MIMEMultipart('alternative')
        msg['From'] = self.from_address
        msg['To'] = self.to_address
        msg['Subject'] = self.subject
        msg['Bcc'] = bcc
        msg['Reply-to'] = 'someone@somewhere.com.br'

        msg.attach(MIMEText(self.body.encode('utf-8'),
            'html', 'UTF-8'))

        mailServer = smtplib.SMTP('smtp.somewhere.com.br', 587)
        mailServer.ehlo()
        mailServer.starttls()
        mailServer.ehlo()
        mailServer.login(user, pwd)
        mailServer.sendmail(self.from_address, [self.to_address, bcc],
            msg.as_string())
        mailServer.close()
