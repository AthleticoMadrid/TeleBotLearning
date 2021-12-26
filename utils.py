#файл с сервисными функциями
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel                  #импорт CLARIFAI
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_pb2, status_code_pb2
from emoji import emojize                                 #для иконок
from pprint import PrettyPrinter                    #красивый вывод
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
    return ReplyKeyboardMarkup([
        ['Прислать автомобиль', KeyboardButton('Мои координаты', request_location=True), 'Заполнить анкету']
    ])              #кнопки: Прислать автомобиль и Мои координаты

def has_object_on_image(file_name, object_name):                 #нейросеть (распознавание объекта на картинке)
    channel = ClarifaiChannel.get_grpc_channel()                    #выбор канала
    app = service_pb2_grpc.V2Stub(channel)                          #создание приложения
    metadata = (('authorization', f'Key {settings.CLARIFAI_API_KEY}'),)         #кортеж с авторизацией и ключом

    with open(file_name, 'rb') as f:                        #открываем файл с картинкой (чтение в бинарном виде)
        file_data = f.read()                                #читаем его в переменную
        image = resources_pb2.Image(base64=file_data)       #переводит в формат base64 для Clarifai

    request = service_pb2.PostModelOutputsRequest(
        model_id='aaa03c23b3724a16a56b629203edc62c',         #базовая модель Clarifai
        inputs=[
            resources_pb2.Input(data=resources_pb2.Data(image=image))       #отправляем на сервер
        ])

    response = app.PostModelOutputs(request, metadata=metadata)             #получаем ответ от сервера Clarifai
    #print(response)
    return check_response_for_object(response, object_name)

def check_response_for_object(response, object_name):                   #функция проверки фото с авто
    if response.status.code == status_code_pb2.SUCCESS:
        for concept in response.outputs[0].data.concepts:
            if concept.name == object_name and concept.value >= 0.90:         #если найден концепт у которого имя (object_name) 'car' и уверенность >= 0.90
                return True
    else:
        print(f'Ошибка распознавания картинки {response.outputs[0].status.details}')

    return False

if __name__ == '__main__':
    pp = PrettyPrinter(indent=2)
    pp.pprint(has_object_on_image('images/car2.jpg', 'car'))                #если найден авто = True
    pp.pprint(has_object_on_image('images/not_car3.jpg', 'train'))          #если найден поезд = True
