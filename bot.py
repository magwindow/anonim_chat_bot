import telebot
from telebot import types

from database import Database
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
db = Database('users.db')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🔍 Поиск собеседника')
    markup.add(item1)
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!  Добро пожаловать в анонимный чат бот. Нажми на кнопку:  🔍 Поиск собеседника'
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
        item1 = types.KeyboardButton('🔍 Поиск собеседника')
        markup.add(item1)
        bot.send_message(chat_info[1], 'Собеседник покинул чат', reply_markup=markup)
        bot.send_message(message.chat.id, 'Вы покинули чат', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Вы не в чате', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '🔍 Поиск собеседника':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('❌ Отменить поиск')
            markup.add(item1)
            
            chat_two = db.get_chat()
            
            if not db.create_chat(message.chat.id, chat_two):
                db.add_queue(message.chat.id)
                bot.send_message(message.chat.id, '🔎 Ищем людей....', reply_markup=markup)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('/stop')
                markup.add(item1)
                bot.send_message(message.chat.id, '📣 Поиск завершен! Собеседник найден.\nЧтобы завершить чат нажмите /stop', reply_markup=markup)
                bot.send_message(chat_two, '📣 Поиск завершен! Собеседник найден.\nЧтобы завершить чат нажмите /stop', reply_markup=markup)
        
        elif message.text == '❌ Отменить поиск':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('🔍 Поиск собеседника')
            markup.add(item1)
            
            db.remove_queue(message.chat.id)
            bot.send_message(message.chat.id, '❌ Поиск остановлен', reply_markup=markup)
        
        else:
            chat_info = db.get_active_chat(message.chat.id)
            bot.send_message(chat_info[1], message.text)
            
            

    
bot.polling(none_stop=True)