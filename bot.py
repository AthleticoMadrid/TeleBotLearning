from emoji import emojize                                 #для иконок
from glob import glob                                     #для выборки картинок по названию              
import logging                                                                          #модуль сообщений об ошибках
from random import choice, randint                        #choice - выдаёт рандомную картинку
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters                #Updater(получает/передаёт сообщения), Handler(обработчик)

import settings

logging.basicConfig(filename="bot.log", level=logging.INFO)      #настройки логгинга(файл куда сохраняются ошибки и уровень важности сообщений)

PROXY = {'proxy_url': settings.PROXY_URL,
        'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):            #update(то что пришло от телеграмма), context(отдаёт команды боту от нас)
    print("Вызван /Start")
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Здравствуй, дорогой друг {context.user_data['emoji']} !")              #ответ от бота на команду /Start

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    text = update.message.text                     #текст от пользователя
    print(text)
    update.message.reply_text(f"{text} {context.user_data['emoji']}")                #ответ от бота на сообщение от пользователя

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

def guess_number(update, context):                  #игра в числа с ботом
    print(context.args)
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except(TypeError, ValueError):
            message = "Введите целое число" 
    else:
        message = "Введите число"                   #если аргумент - пустой
    update.message.reply_text(message)

def send_car_picture(update, context):
    car_photo_list = glob('images/car*.jp*g')                  #получаем список с картинками
    car_photo_filename = choice(car_photo_list)                  #выбираем из списка случайную
    chat_id = update.effective_chat.id                          #находим id пользователя
    context.bot.send_photo(chat_id=chat_id, photo=open(car_photo_filename, 'rb'))             #отправляем пользователю картинку

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher                   #диспетчер команд
    dp.add_handler(CommandHandler("Start", greet_user))             #к диспетчеру добавляется обработчик команд реагирующий на "Start" и вызывается функция greet_user
    dp.add_handler(CommandHandler("Guess", guess_number))           #игра в числа с ботом
    dp.add_handler(CommandHandler("car", send_car_picture))         #картинки с автомобилями
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))        #Filters.text - реагировать только на текстовые сообщения

    logging.info("Бот запустился")
    mybot.start_polling()                       #обращения бота за обновлениями
    mybot.idle()                                #бот будет работать пока сами его не остановим

if __name__ == "__main__":
    main()                  #вызов функции
