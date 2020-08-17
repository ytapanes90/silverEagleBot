#!/usr/bin/python

import telebot
import sqlite3
import json
import requests
import random


API_TOKEN = '1221828442:AAGl7rpmlUPiYe5qxb6xfBYb74sjY0cHkno'

bot = telebot.TeleBot(API_TOKEN)


def querydb(grupo):
    with sqlite3.connect("users.sqlite") as conn:
        cursorObj = conn.cursor()
        q = cursorObj.execute("SELECT id, alias FROM users WHERE grupo=%s" % grupo)
        users = q.fetchall()
        return users


users = []
headers=[
        'Bombeeeeero bombeeeeero echa agua echa agua que se quema que se quema abombochie bam bam',
        'Mayday mayday',
        'Co co, cohete a la vistaaaaaaaaaaa',
        'Pantera rosa llamando a pinguinos púrpura'
    ]


# Handle '/start'
@bot.message_handler(commands=['start'])
def start(message):
    started = True
    global started
    users = querydb(message.chat.id)
    print(users)
    bot.reply_to(message, "Iniciado")

# Handle '/stop'
@bot.message_handler(commands=['stop'])
def stop(message):
    started = False
    global started
    bot.reply_to(message, "Detenido")

# Handle '/status'
@bot.message_handler(commands=['status'])
def status(message):
    if started:
        bot.reply_to(message, "Iniciado")
    else:
        bot.reply_to(message, "Detenido")


# Handle '/all'
@bot.message_handler(commands=['all'])
def call_registers(message):
    if started:
        global users
        global headers
        alias = ""
        for user in users:
            alias+='@'+user[1]+'\n'
        head=random.randint(0,len(headers)-1)
        bot.send_message(message.chat.id, headers[head]+'\n'+alias)
    else:
        bot.reply_to(message, "Bot detenido")



# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if started:
        with sqlite3.connect("users.sqlite") as con:
            global users
            texto = message.text
            id_persona = message.from_user.id
            alias = message.from_user.username
            id_chat = message.chat.id

            cursorObj1 = con.cursor()
            change=False;
            user_found = False;
            for user in users:
                if str(id_persona) == user[0]:
                    user_found = True
                    if not(alias == user[1]):
                        cursorObj1.execute("UPDATE users SET alias='%s' WHERE id='%s'" % (alias,id_persona))
                        con.commit()
                        change = True

            if user_found == False:
                cursorObj1.execute("INSERT INTO users VALUES ('%s','%s','%s')" % (id_persona,alias,id_chat))
                con.commit()
                change = True

            if change:
                users=querydb(id_chat)

bot.polling()
