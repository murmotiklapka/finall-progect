import telebot
from telebot import types
import os
from dotenv import load_dotenv
transports_ = {'Автомобиль' : 200,
               'Автобус' : 70,
               'Метро/поезд' : 40,
               'Самолёт' : 300
               }

transpords_0 = ['Автомобиль',
    'Автобус',
    'Метро/поезд',
    'Самолёт']

co2 = 0
load_dotenv()

bot = telebot.TeleBot(os.getenv("APITOKEN"))

@bot.message_handler(commands=['start'])
def start(message):
    text = (f'Приветствую, {message.from_user.first_name}!\n\n'
        'Могу помочь с определением примерного углеродного следа.')
    bot.send_message(message.chat.id, text)
    markup = types.InlineKeyboardMarkup()
    b = 0
    for i in transpords_0:
        button = types.InlineKeyboardButton(text=transpords_0[b],callback_data=transpords_0[b])
        markup.add(button)
        b += 1
    
    button_last = types.InlineKeyboardButton(text='Я закончил',callback_data='Я закончил')
    markup.add(button_last)
    bot.send_message(message.chat.id,'Выберите транспорт:',reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def calcul(call):
    try:
        bot.answer_callback_query(call.id)
    except:
        pass

    if call.data == 'Я закончил':
        stop(stop(call.message))
    else:
        msage = bot.send_message(call.message.chat.id,f'Сколько km вы передвигаетесь на {call.data} в месятс?')
        bot.register_next_step_handler(msage,get_km,call.data)
        return(call.data)

def get_km(message, transport):
    global co2
    km = int(message.text)
    km_1 = transports_[transport]
    co2 += km_1
    bot.send_message(message.chat.id,f'Жми другую кнопку снова')
    
def stop(message):
    last_num = co2 / 1000
    bot.send_message(message.chat.id,f'Ваш углеродный след: ~{last_num} kg в месятс!')
    bot.send_message(message.chat.id,f'Жми /start и запустишь снова')

bot.polling()
