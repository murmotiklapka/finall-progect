#импорты
import telebot
import random
import os

from telebot import types
from math import ceil
from dotenv import load_dotenv

#данные о углероде и массив всего
plants = {
    'Папоротник': 15,
    'Спатифиллум': 18,
    'Сансевиерия': 14,
    'Потос': 20,
    'Фикус': 35,
    'Хлорофитум': 12,
    'Алоэ вера': 10,
    'Монстера': 30
}

plants_ = [
    'Папоротник',
    'Спатифиллум',
    'Сансевиерия',
    'Потос',
    'Фикус',
    'Хлорофитум',
    'Алоэ вера',
    'Монстера'
]

transports_ = {
    'Автомобиль (бензин)': 13200,
    'SUV / джип': 18000,
    'Электромобиль': 3000,
    'Мотоцикл (спортивный)': 12600,
    'Скутер': 2400,
    'Автобус': 2800,
    'Электробус': 1200,
    'Метро': 2400,
    'Трамвай': 1050,
    'Троллейбус': 600,
    'Поезд': 2500,
    'Скоростной поезд': 3750,
    'Пассажирский самолёт': 225000,
    'Частный самолёт': 1600000,
    'Вертолёт': 132000,
    'Паром': 3600,
    'Круизный лайнер': 12000,
    'Яхта': 24500,
    'Грузовик': 56000,
    'Экскаватор': 6000
}

transpords_0 = [
    'Автомобиль (бензин)',
    'SUV / джип',
    'Электромобиль',
    'Мотоцикл (спортивный)',
    'Скутер',
    'Автобус',
    'Электробус',
    'Метро',
    'Трамвай',
    'Троллейбус',
    'Поезд',
    'Скоростной поезд',
    'Пассажирский самолёт',
    'Частный самолёт',
    'Вертолёт',
    'Паром',
    'Круизный лайнер',
    'Яхта',
    'Грузовик',
    'Экскаватор'
]

#устоновка переменных
co2_oll = 0
co2 = 0
achievementsses = []

load_dotenv()

bot = telebot.TeleBot(os.getenv("APITOKEN"))

#все функции бота
def error(message):
    bot.send_message(message.chat.id,'Произошла ошибка, попробуйте ещё раз нажав /start')
@bot.message_handler(commands=['start'])
def start(message):
    text = ('выберите ачивки(/achievements), топ 5 самых грязных и чистых транспортов(/top) или ростений(/top_plant) посчитать ваш углеродный след(/calculate), или как его убрать(/calculate_plants)')
    bot.send_message(message.chat.id, text)
    
@bot.message_handler(commands=['twitch'])
def twitch(message):
    bot.send_message(message.chat.id,f'ты нашёл пасхалку, она добавится в ачивки, если ты её не видел раньше!')
    if 'Пасхалка' not in achievementsses:
        achievementsses.append('Пасхалка')

@bot.message_handler(commands=['achievements'])
def achievements(message):
    bot.send_message(message.chat.id,f'{achievementsses}')

@bot.message_handler(commands=['calculate_plants'])
def calculate_plants(message):
    bot.send_message(message.chat.id,'Приветствую, могу помочь с определением примерного количества растений, которое надо посадить для нейтрализации вашего углеродного следа.')
    markup = types.InlineKeyboardMarkup()
    b = 0
    for i in plants_:
        button_ = types.InlineKeyboardButton(text=str(plants_[b]),callback_data='plant:' + str(plants_[b]))
        markup.add(button_)
        b += 1
    bot.send_message(message.chat.id,'Выберите растение:',reply_markup=markup) 

@bot.callback_query_handler(func=lambda call: call.data.startswith('plant:'))
def calcul_plant(call):
    try:
        bot.answer_callback_query(call.id)
        msage_ = bot.send_message(call.message.chat.id,f'Сколько вы создаёте углеродного следа в месяц (в граммах)?')
        bot.register_next_step_handler(msage_,get_plant,call.data.replace('plant:','',1))
    except Exception as error:
        print(error)
    return(call.data)

def get_plant(message, plant):
    global co2
    coal = int(message.text)
    km_1_ = coal / plants[plant]
    bot.send_message(message.chat.id,f'вам надо посадить ~{ceil(km_1_)}  {plant}, чтобы убрать ваш углеродный след!')
    bot.send_message(message.chat.id,f'нажми /start, чтобы начать сначала!')

@bot.message_handler(commands=['top'])
def top(message):
    top_bad = sorted(transports_.items(),key=lambda x: x[1],reverse=True)[:5]
    top_good = sorted(transports_.items(),key=lambda x: x[1])[:5]

    text = (f'Топ 5 самых грязных транспортов: {top_bad}\n\nТоп 5 самых чистых транспортов: {top_good}')
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['top_plant'])
def top_plant(message):
    top_bad_ = sorted(plants.items(),key=lambda x: x[1],reverse=True)[:5]
    top_good_ = sorted(plants.items(),key=lambda x: x[1])[:5]

    text = (f'Топ 5 самых плохих транспортов: {top_bad_}\n\nТоп 5 самых крутыч транспортов: {top_good_}')
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['calculate'])
def calculate(message):
    global co2
    co2 = 0
    text = ('Приветствую, могу помочь с определением примерного ~углеродного следа за час езды.')
    bot.send_message(message.chat.id, text)
    markup = types.InlineKeyboardMarkup()
    b = 0
    for i in transpords_0:
        button = types.InlineKeyboardButton(text=transpords_0[b],callback_data='transport:' + transpords_0[b])
        markup.add(button)
        b += 1
    
    button_last = types.InlineKeyboardButton(text='Я закончил',callback_data='transport:Я закончил')
    markup.add(button_last)
    bot.send_message(message.chat.id,'Выберите транспорт:',reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('transport:'))
def calcul(call):
    bot.answer_callback_query(call.id)
    transport = call.data.replace('transport:','',1)
    if transport == 'Я закончил':
        stop(call.message)
    else:
        msage = bot.send_message(call.message.chat.id,f'Сколько часов вы передвигаетесь на {transport} в месяц?')
        bot.register_next_step_handler(msage,get_km,transport)
        return(call.data)

def get_km(message, transport):
    global co2
    try:
        km = int(message.text)
        km_1 = transports_[transport]
        co2 += km_1 * km
        bot.send_message(message.chat.id,'выберите другой транспорт или нажмите кнопку "я закончил" для завершения расчета')
    except Exception as error:
        print(error)

def stop(message):
    global co2_oll
    random_plnt = random.choice(list(plants_))
    last_num = co2 / 1000
    bot.send_message(message.chat.id,f'Ваш углеродный след: ~{last_num} kg в месяц!')
    bot.send_message(message.chat.id,f'Вам надо посадить ~{ceil(last_num/plants[random_plnt])} {random_plnt}, чтобы убрать его!\n')
    bot.send_message(message.chat.id,'нажми /start, чтобы начать сначала!')
    co2_oll += last_num
    if co2_oll >= 1000000 and 'Миллионер углеродного следа' not in achievementsses:
        achievementsses.append('Миллионер углеродного следа')

#запуск бота
bot.polling()
