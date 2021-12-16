#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import subprocess
from data import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def main_menu_keyboard(): # Menu inicial
    keyboard = [[InlineKeyboardButton('Clasificación', callback_data='clasificacion')], [InlineKeyboardButton('Últimos partidos', callback_data='partidos')]]

    return InlineKeyboardMarkup(keyboard)

def main():
    updater = Updater(TOKEN, use_context=True)
    ud = updater.dispatcher
    ud.add_handler(CommandHandler('start', start))
    ud.add_handler(CallbackQueryHandler(menu_clasificacion, pattern='clasificacion'))
    ud.add_handler(CallbackQueryHandler(menu_partidos, pattern='partidos'))
    updater.start_polling()
    updater.idle()

def start(update, context):
    update.message.reply_text('Menú principal:', reply_markup=main_menu_keyboard())

def string_lista(string): # Paso de string a una lista
    sin_inicio = string.replace("[[", "")
    sin_inicio_fin = sin_inicio.replace("]]", "")
    li = list(sin_inicio_fin.split("], [")) # Como separo por ], [ elimino del inicio [[ y ]] del final

    if len(li) == 1: # Si el tamaño es 1 significa que lo tengo que separar por comas
        sin_comas = string.replace("'", "")
        li = list(sin_comas.split(", "))

    return li

def acento(string): # Cambio los acentos
    texto = string.replace('\\\\xc3\\\\xa1', 'á')
    texto = texto.replace('\\xc3\\xa1', 'á')
    texto = texto.replace('\\\\xc3\\\\xa9', 'é')
    texto = texto.replace('\\xc3\\xa9', 'é')

    return texto

def menu_clasificacion(update, context):
    query = update.callback_query

    try:
        f = open('/bot/ProyectoDAM/datos/clasificacion.json','r')
        consulta = f.read()
        f.close()
    except FileNotFoundError:
        print('Archivo no existe')
        exit()
    except PermissionError:
        print('No se tienen permisos para leer el archivo')
        exit()

    consulta = string_lista(consulta)
    respuesta = 'Liga BBVA 2021/22:\n\n'

    for x in consulta: # Recorro en la lista todos los equipos con los datos obtenidos de la web
        x = string_lista(x)
        respuesta += x[0] + ' - ' + acento(x[1]) + ': ' + x[2] + ' pts. en ' + x[4] + ' partidos, diferencia de goles: ' + x[3] + '.\n'
        
    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=respuesta, reply_markup=main_menu_keyboard())

def menu_partidos(update, context):
    query = update.callback_query

    try:
        f = open('/bot/ProyectoDAM/datos/resultados.json','r')
        consulta = f.read()
        f.close()
    except FileNotFoundError:
        print('Archivo no existe')
        exit()
    except PermissionError:
        print('No se tienen permisos para leer el archivo')
        exit()

    sin_inicio = consulta.replace("[", "")
    sin_inicio_fin = sin_inicio.replace("]", "")
    sin_comas = sin_inicio_fin.replace("'", "")
    li = list(sin_comas.split(", "))

    respuesta = 'Última jornada liga BBVA 2021/22:\n\n'

    for texto in li: # Recorro la lista de todos los partidos
        respuesta += acento(texto) + '\n'

    context.bot.edit_message_text(chat_id=query.message.chat_id, message_id=query.message.message_id, text=respuesta, reply_markup=main_menu_keyboard())

if __name__ == '__main__':
    main()
