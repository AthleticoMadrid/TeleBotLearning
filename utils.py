#файл с сервисными функциями
from emoji import emojize                                 #для иконок
from random import choice, randint                        #choice - выдаёт рандомную картинку
from telegram import ReplyKeyboardMarkup, KeyboardButton                  #клавиатура

import settings

def get_smile(user_data):
    if 'emoji' not in user_data:                                            #если в данных нет эмоджи:
        smile = choice(settings.USER_EMOJI)                                 #генерируем новый случайный смайлик из списка
        return emojize(smile, use_aliases=True)                             #возвращаем преобразованный :текст: из списка в иконку смайлика(aliase)
    return user_data['emoji']

def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)            #границы чисел откуда начинается генерирование
    if user_number > bot_number:
        message = f"Ваше число: {user_number}, моё число: {bot_number}, - вы выиграли"
    elif user_number == bot_number:
        message = f"Ваше число: {user_number}, моё число: {bot_number}, - ничья"
    else:
        message = f"Ваше число: {user_number}, моё число: {bot_number}, - вы проиграли"
    return message

def main_keyboard():
    return ReplyKeyboardMarkup([['Прислать автомобиль', KeyboardButton('Мои координаты', request_location=True)]])              #кнопки: Прислать автомобиль и Мои координаты
