import logging                                                                          #модуль сообщений об ошибках

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters                #Updater(получает/передаёт сообщения), Handler(обработчик)
from handlers import (greet_user, guess_number, send_car_picture, talk_to_me, 
                user_coordinates)
import settings

logging.basicConfig(filename="bot.log", level=logging.INFO)      #настройки логгинга(файл куда сохраняются ошибки и уровень важности сообщений)

PROXY = {'proxy_url': settings.PROXY_URL,
        'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher                   #диспетчер команд
    dp.add_handler(CommandHandler("Start", greet_user))             #к диспетчеру добавляется обработчик команд реагирующий на "Start" и вызывается функция greet_user
    dp.add_handler(CommandHandler("Guess", guess_number))           #игра в числа с ботом
    dp.add_handler(CommandHandler("Car", send_car_picture))         #картинки с автомобилями
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать автомобиль)$'), send_car_picture))      #реагирует на фразу: ^ -начало строки, () -фраза, $ -конец строки
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))              #отправка координат
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))        #Filters.text - реагирует только на текстовые сообщения

    logging.info("Бот запустился")
    mybot.start_polling()                       #обращения бота за обновлениями
    mybot.idle()                                #бот будет работать пока сами его не остановим

if __name__ == "__main__":
    main()                  #вызов функции
