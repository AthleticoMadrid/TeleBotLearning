#файл с обработчиками
from glob import glob                                     #для выборки картинок по названию
from random import choice
from utils import get_smile, main_keyboard, play_random_numbers

def greet_user(update, context):            #update(то что пришло от телеграмма), context(отдаёт команды боту от нас)
    print("Вызван /Start")
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(
        f"Здравствуй, дорогой друг {context.user_data['emoji']} !",
        reply_markup=main_keyboard()
        )                                                       #ответ от бота на команду /Start

def talk_to_me(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)
    text = update.message.text                     #текст от пользователя
    print(text)
    update.message.reply_text(
        f"{text} {context.user_data['emoji']}", 
        reply_markup=main_keyboard()
        )                #ответ от бота на сообщение от пользователя

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
    update.message.reply_text(message, reply_markup=main_keyboard())

def send_car_picture(update, context):
    car_photo_list = glob('images/car*.jp*g')                  #получаем список с картинками
    car_photo_filename = choice(car_photo_list)                  #выбираем из списка случайную
    chat_id = update.effective_chat.id                          #находим id пользователя
    context.bot.send_photo(chat_id=chat_id, photo=open(car_photo_filename, 'rb'), reply_markup=main_keyboard())             #отправляем пользователю картинку

def user_coordinates(update, context):
    context.user_data['emoji'] = get_smile(context.user_data)   #получает бот
    coords = update.message.location                            #получает данные с координатами
    update.message.reply_text(
        f"Ваши координаты: {coords} {context.user_data['emoji']} !",
        reply_markup=main_keyboard()
    )                   #ответ от бота

