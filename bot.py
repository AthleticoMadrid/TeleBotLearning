import logging                                                                          #модуль сообщений об ошибках
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters                #Updater(получает/передаёт сообщения), Handler(обработчик)

import settings

logging.basicConfig(filename="bot.log", level=logging.INFO)      #настройки логгинга(файл куда сохраняются ошибки и уровень важности сообщений)

PROXY = {'proxy_url': settings.PROXY_URL,
        'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):            #update(то что пришло от телеграмма), context(отдаёт команды боту от нас)
    print("Вызван /Start")
    update.message.reply_text("Здравствуй, дорогой друг!")              #ответ от бота на команду /Start

def talk_to_me(update, context):
    text = update.message.text                     #текст от пользователя
    print(text)
    update.message.reply_text(text)                #ответ от бота на сообщение от пользователя

def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher                   #диспетчер команд
    dp.add_handler(CommandHandler("Start", greet_user))             #к диспетчеру добавляется обработчик команд реагирующий на "Start" и вызывать функцию greet_user
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))        #Filters.text - реагировать только на текстовые сообщения

    logging.info("Бот запустился")
    mybot.start_polling()                       #обращения бота за обновлениями
    mybot.idle()                                #бот будет работать пока сами его не остановим

if __name__ == "__main__":
    main()                  #вызов функции
