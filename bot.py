import telebot
from telebot import types

from database import Database
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
db = Database('users.db')

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🔍 Поиск собеседника')
    markup.add(item1)
    return markup

def stop_dialog():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('📢 Сказать свой профиль')
    item2 = types.KeyboardButton('/stop')
    markup.add(item1, item2)
    return markup

def stop_search():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('❌ Отменить поиск')
    markup.add(item1)
    return markup


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('👨 Я парень')
    item2 = types.KeyboardButton('👩 Я девушка')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!  Добро пожаловать в анонимный чат бот. Укажите свой пол:'
                     .format(message.from_user), reply_markup=markup)
    
    
@bot.message_handler(commands=['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🔍 Поиск собеседника')
    markup.add(item1)
    bot.send_message(message.chat.id, '📋 Меню', reply_markup=markup) 
    

@bot.message_handler(commands=['stop'])
def stop(message):
    chat_info = db.get_active_chat(message.chat.id)  
    if chat_info:
        db.delete_chat(chat_info[0])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('➡️ Следующий диалог')
        item2 = types.KeyboardButton('/menu')
        markup.add(item1, item2)
        bot.send_message(chat_info[1], 'Собеседник покинул чат', reply_markup=markup)
        bot.send_message(message.chat.id, 'Вы покинули чат', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Вы не в чате', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '🔍 Поиск собеседника' or message.text == '➡️ Следующий диалог':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('🔍 Парней')
            item2 = types.KeyboardButton('🔍 Девушек')
            item3 = types.KeyboardButton('🔴 Всех')
            markup.add(item1, item2, item3)
            bot.send_message(message.chat.id, 'Кого будем искать?', reply_markup=markup)
            
        
        elif message.text == '❌ Отменить поиск':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('🔍 Поиск собеседника')
            markup.add(item1)
            db.remove_queue(message.chat.id)
            bot.send_message(message.chat.id, '❌ Поиск остановлен', reply_markup=markup)
            
        
        elif message.text == '🔍 Парней':
            user_info = db.get_gender_chat('male')
            chat_two = user_info[0]
            if int(chat_two) != message.chat.id:
                if not db.create_chat(message.chat.id, chat_two):
                    db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                else:
                    bot.send_message(message.chat.id, '📣 Поиск завершен! Собеседник найден.\nЧтобы завершить чат нажмите /stop', reply_markup=stop_dialog())
                    bot.send_message(chat_two, '📣 Поиск завершен! Собеседник найден.\nЧтобы завершить чат нажмите /stop', reply_markup=stop_dialog())
            else:
                bot.send_message(message.chat.id, '🔎 Ищем парней....', reply_markup=stop_search())
        
        elif message.text == '🔍 Девушек':
            user_info = db.get_gender_chat('female')
            chat_two = user_info[0]
            if int(chat_two) != message.chat.id:
                if not db.create_chat(message.chat.id, chat_two):
                    db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                else:
                    bot.send_message(message.chat.id, '📣 Поиск завершен! Собеседник найден.\nЧтобы завершить чат нажмите /stop', reply_markup=stop_dialog())
                    bot.send_message(chat_two, '📣 Поиск завершен! Собеседник найден.\nЧтобы завершить чат нажмите /stop', reply_markup=stop_dialog())
            else:
                bot.send_message(message.chat.id, '🔎 Ищем девушек....', reply_markup=stop_search())
        
        elif message.text == '🔴 Всех':
            user_info = db.get_chat()
            chat_two = user_info[0]
            if not db.create_chat(message.chat.id, chat_two):
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '🔎 Ищем людей....', reply_markup=stop_search())
            else:
                bot.send_message(message.chat.id, '📣 Поиск завершен! Собеседник найден.\nЧтобы завершить чат нажмите /stop', reply_markup=stop_dialog())
                bot.send_message(chat_two, '📣 Поиск завершен! Собеседник найден.\nЧтобы завершить чат нажмите /stop', reply_markup=stop_dialog())
            
        
        elif message.text == '📢 Сказать свой профиль':
            chat_info = db.get_active_chat(message.chat.id)
            if chat_info:
                if message.from_user.username:
                    bot.send_message(chat_info[1], '@' + message.from_user.username)
                    bot.send_message(message.chat.id, '✅ Ваш профиль успешно отправлен')
                else:
                    bot.send_message(message.chat.id, '❌ У вас нет никнейма') 
            else:
                bot.send_message(message.chat.id, 'Вы не в чате')
        
        elif message.text == '👨 Я парень':
            if db.set_gender(message.chat.id, 'male'):
                bot.send_message(message.chat.id, '✅ Ваш пол успешно добавлен', reply_markup=main_menu())
            else:
                bot.send_message(message.chat.id, '📝 Ваш пол уже указан')   
                
        elif message.text == '👩 Я девушка':    
            if db.set_gender(message.chat.id, 'female'):
                bot.send_message(message.chat.id, '✅ Ваш пол успешно добавлен', reply_markup=main_menu())
            else:
                bot.send_message(message.chat.id, '📝 Ваш пол уже указан')
        
        else:
            if db.get_active_chat(message.chat.id):
                chat_info = db.get_active_chat(message.chat.id)
                bot.send_message(chat_info[1], message.text)
            else:
                bot.send_message(message.chat.id, 'Вы не в чате')
                

@bot.message_handler(content_types=['sticker'])
def bot_stickers(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info:
            bot.send_sticker(chat_info[1], message.sticker.file_id)
    else:
        bot.send_message(message.chat.id, 'Вы не в чате')
        

@bot.message_handler(content_types=['voice'])
def bot_voice(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info:
            bot.send_voice(chat_info[1], message.voice.file_id)
    else:
        bot.send_message(message.chat.id, 'Вы не в чате')
            
            

    
bot.polling(none_stop=True)