# Проект CarBot

CarBot - это бот для Telegram, который специализируется на отправке пользователю фото с автомобилем, а также умеющий считывать геолокацию где в данный момент находится пользователь

## Установка 

1. Клонируйте репозиторий с GitHub
2. Создайте виртуальное окружение
3. Установите зависимости `pip install -r requirements.txt`
4. Создайте файл `settings.py`
5. Впишите в settings.py переменные:
```
API_KEY = "API-ключ бота"
PROXY_URL = "Адрес прокси-сервера"
PROXY_USERNAME = "Логин на прокси-сервере"
PROXY_PASSWORD = "Пароль на прокси-сервере"
USER_EMOJI = [':koala:', ':tiger:', ':trollface:', ':relieved:', ':relaxed:']
```
6. Запустите бота командой `python bot.py`