from manuscript import Manuscript
from author import Author
from mail import Mail
import requests
from bs4 import BeautifulSoup
import re

def get_press():
    qn_html = requests.get('http://yourdomain.com.br')
    qn_text = qn_html.text
    soup = BeautifulSoup(qn_text, "lxml")
    links = soup.find_all(href=re.compile('nomeArquivo'))

    press = []
    for link in links:
        href = str(link.get('href'))
        match = re.search('(?<=nomeArquivo=)(\w+)', href)
        num = re.sub(r'[a-zA-Z-]', '', match.group(1))
        artcod = 'QN-' + num[0:4] + '-' + num[4:8]
        press.append(artcod)
    return set(press)

def get_sent(database):
    sent = []
    with open(database, 'r') as f:
        for num in f:
            sent.append(num.strip())
    return set(sent)

press = get_press() # get article # of articles in press
sent = get_sent('sent.txt') # get article # of sent e-mails
to_send = press.difference(sent) # difference of sets are the e-mails to send

infodb = {} # table of article # and e-mails
with open('list_mail.txt', 'r') as input_file:
    next(input_file)
    for line in input_file:
        line = line.strip()
        info = line.split('\t')
        infodb[info[0][0:12]] = (info[1], info[2], info[3])
for artcod in to_send:
    manuscript = Manuscript(artcod)
    if (infodb[artcod][2] == 'Brazil'): language = 'pt'
    else: language = 'en'
    auth_info = [infodb[artcod][0], 'n', language, infodb[artcod][1].lower()]
    author = Author(auth_info)
    mail = Mail(author, manuscript)
    mail.send()
    print '%s: e-mail enviado para %s' % (artcod, infodb[artcod][1].lower())
with open('sent.txt', 'a') as sent: # write in sent.txt the article # of sent
    for artcod in to_send:
        sent.write(artcod)
        sent.write('\n')
print 'Finished!'
