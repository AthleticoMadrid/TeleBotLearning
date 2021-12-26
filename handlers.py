#файл с обработчиками
from glob import glob                                     #для выборки картинок по названию
import os
from random import choice
from utils import get_smile, main_keyboard, play_random_numbers, has_object_on_image

def greet_user(update, context):            #update(то что пришло от бота), context(отдаёт команды боту от нас)
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

def check_user_photo(update, context):
    update.message.reply_text('Обрабатываем фото')              #сообщение пользователю
    os.makedirs('downloads', exist_ok=True)                     #создаётся папка 'downloads', если такой папки ещё нету
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)            #получаем id файла с фото
    file_name = os.path.join('downloads', f"{update.message.photo[-1].file_id}.jpg")        #сохранение файла(os.path.join - соединяет пути)
    photo_file.download(file_name)                      #скачиваем файл с указанного адреса
    update.message.reply_text('Файл сохранён')          #сообщение пользователю
    if has_object_on_image(file_name, 'car'):
        update.message.reply_text('Обнаружен автомобиль, сохраняю его в библиотеку')
        new_file_name = os.path.join('images', f'car_{photo_file.file_id}.jpg')
        os.rename(file_name, new_file_name)                 #переименовывает файл вместе с именем папки и перемещает его
    else:
        os.remove(file_name)                #удаляет файл
        update.message.reply_text('Тревога, автомобиль не обнаружен!')