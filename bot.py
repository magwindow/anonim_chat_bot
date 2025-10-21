import telebot
from telebot import types

from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    bot.send_message(message.chat.id, message.text)
    
    
bot.polling(none_stop=True)