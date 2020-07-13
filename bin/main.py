import requests
import misc
import re
import csv
import sys
from antonidabotternovnik.lib.api import dog
from antonidabotternovnik.lib.api.wikipedia import main_wikipedia
from antonidabotternovnik.lib.parser import avito
sys.path.append("../lib/")
from open import *
import string
import json
from time import sleep
import detect


token = misc.token

global recent_update_id
last_update_id = 0

URL = 'https://api.telegram.org/bot' + token + '/'
# https://api.telegram.org/bot657957153:AAF6eMUmc8pnRnlpQfsRw6wCeSvMYsJNcyA/sendmessage?chat_id=364979656&text=hi

def get_updates():
    url = URL + 'getupdates'
   # print(url)
    r = requests.get(url)
    print(r.json())
    return  r.json()

def get_message():
    data = get_updates()
    last_object = data['result'][-1]
    current_update_id = last_object['update_id']
    global last_update_id
    if last_update_id != current_update_id:
        last_update_id = current_update_id
        chat_id =last_object['message']['chat']['id']
        message_text = last_object['message']['text']

        message = {'chat_id':chat_id,
                   'text':message_text}
        return  message
    return None


def send_message(chat_id,text ='Wait a second, please...'):
    url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id,text)
    requests.get(url)

def help():
    help = "/searchwikipedia -  поиск статьи в интернет-энциклопедии по заголовкам , а также выдача краткой информации по данному запросу\n"
    help +="/dog - выдача случайных фотографий собак\n"
    help +="/avito - выдача объявления по запросу с Авито из раздела ноутбуки по марке"
    return help

def avito_text(chat_id):
    send_message(chat_id, "Пожалуйста, введите модель ноутбука для поиска на Avito.")
    answer2 = None
    while answer2 == None:
        answer2 = get_message()
        if answer2 != None:
            chat_id = answer2['chat_id']
            text2 = answer2['text']
    avito.avito(text2)
    with open('avito.csv','r+') as f:
       a = f.read()
       if len(a) == 0:
           a = "Ошибка поиска! Эта модель может отсутствовать, попробуйте ввести запрос позже или выберите другую модель."
       print(a)
    send_message(chat_id,str(a))



def searchwikipedia(chat_id):
    send_message(chat_id, "Пожалуйста, введите запрос на поиск в Википедии.Запрос должен состоять из латинских букв.")
    answer2 = None
    while answer2 == None:
        answer2 = get_message()
        if answer2 != None:
            chat_id = answer2['chat_id']
            text2 = answer2['text']
    pat = '^[a-zA-Z{}]+$'.format(re.escape(string.punctuation))
    if bool(re.match(pat, text2)) == True:
        if text2:
            send_message(chat_id, main_wikipedia(text2.title()))
    else:
        send_message(chat_id, "Запрос должен состоять из латинских букв.")

def _main():

    while True:
        answer = get_message()
        if answer !=None:
            chat_id = answer['chat_id']
            text = answer['text']
            if text == '/start':
                send_message(chat_id, "Приве! Набери команду /help, чтобы узнать как  пользоваться ботом")
            if text == '/searchwikipedia':
                searchwikipedia(chat_id)
            if text == '/dog':
               dog.bots(chat_id)
            if text == '/avito':
                avito_text(chat_id)
            if text == '/help':
                send_message(chat_id, help())

        else :
            continue
        sleep(2)




if __name__ == '__main__':
    _main()

