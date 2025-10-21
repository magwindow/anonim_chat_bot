import telebot
from telebot import types

from config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🔍 Поиск собеседника')
    markup.add(item1)
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!  Добро пожаловать в анонимный чат бот. Нажми на кнопку "🔍 Поиск собеседника"'
                     .format(message.from_user), reply_markup=markup)
    
    
@bot.message_handler(commands=['menu'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('🔍 Поиск собеседника')
    markup.add(item1)
    bot.send_message(message.chat.id, '📋 Меню', reply_markup=markup)    


@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '🔍 Поиск собеседника':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('❌ Отменить поиск')
            markup.add(item1)
             
    
    
    
    
bot.polling(none_stop=True)