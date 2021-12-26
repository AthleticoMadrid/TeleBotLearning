import logging                                                                          #модуль сообщений об ошибках

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler                #Updater(получает/передаёт сообщения), Handler(обработчик)
from anketa import (anketa_start, anketa_name, anketa_rating, anketa_skip, anketa_comment, 
                anketa_dontknow)
from handlers import (greet_user, guess_number, send_car_picture, talk_to_me, 
                user_coordinates, check_user_photo)
import settings

logging.basicConfig(filename="bot.log", level=logging.INFO)      #настройки логгинга(файл куда сохраняются ошибки и уровень важности сообщений)

PROXY = {'proxy_url': settings.PROXY_URL,
        'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher                   #диспетчер команд
    
    anketa = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(Заполнить анкету)$'), anketa_start)],              #вход в диалог (анкету)
        states={
            "name": [MessageHandler(Filters.text, anketa_name)],
            "rating": [MessageHandler(Filters.regex('^(1|2|3|4|5)$'), anketa_rating)],
            "comment": [
                CommandHandler("Skip", anketa_skip),
                MessageHandler(Filters.text, anketa_comment)
            ]
        },                          #шаги (имя, рейтинг)
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, anketa_dontknow)
        ]                        #возврат в диалог (анкеты) при неверном ответе (а так же фото, видео, документе и локации)
    )
    dp.add_handler(anketa)
    dp.add_handler(CommandHandler("Start", greet_user))             #к диспетчеру добавляется обработчик команд реагирующий на "Start" и вызывается функция greet_user
    dp.add_handler(CommandHandler("Guess", guess_number))           #игра в числа с ботом
    dp.add_handler(CommandHandler("Car", send_car_picture))         #картинки с автомобилями
    dp.add_handler(MessageHandler(Filters.regex('^(Прислать автомобиль)$'), send_car_picture))      #реагирует на фразу: ^ -начало строки, () -фраза, $ -конец строки
    dp.add_handler(MessageHandler(Filters.photo, check_user_photo))                 #опознаватель объектов на фото
    dp.add_handler(MessageHandler(Filters.location, user_coordinates))              #отправка координат
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))        #Filters.text - реагирует только на текстовые сообщения

    logging.info("Бот запустился")
    mybot.start_polling()                       #обращения бота за обновлениями
    mybot.idle()                                #бот будет работать пока сами его не остановим

if __name__ == "__main__":
    main()                  #вызов функции
