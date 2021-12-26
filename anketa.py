#файл для диалогов
from telegram import ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove            #ParseMode - позволяет форматировать данные
from telegram.ext import ConversationHandler                    #для завершения диалога
from utils import main_keyboard                     #основная клавиатура

def anketa_start(update, context):              #начало диалога
    update.message.reply_text(
        'Привет, как тебя зовут?', 
        reply_markup=ReplyKeyboardRemove()
    )
    return "name"                               #переход в шаги

def anketa_name(update, context):               #шаг №1. получим имя пользователя
    user_name = update.message.text             #введённое от пользователя
    if len(user_name.split()) < 2:              #если пользователь ввёл меньше 2х слов (не имя и фамилию)
        update.message.reply_text('Пожалуйста введите своё имя и фамилию')
        return "name"                           #если введено что-то неправильное то шаг начинается заново
    else:
        context.user_data["anketa"] = {"name": user_name}   #словарь с именем
        reply_keyboard = [['1', '2', '3', '4', '5']]      #оценка от пользователя
        update.message.reply_text(
            'Пожалуйста оцените нашего бота от 1 до 5',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)        #клавиатура (будет показана один раз (one_time))
        )
        return "rating"             #следующий шаг (рейтинг)

def anketa_rating(update, context):                         #рейтинг (оценка) бота
    context.user_data['anketa']['rating'] = int(update.message.text)
    update.message.reply_text('Напишите комментарий, или нажмите /skip, чтобы пропустить')
    return "comment"                  #следующий шаг (комментарий)

def anketa_comment(update, context):                    #комментарий от пользователя
    context.user_data['anketa']['comment'] = update.message.text                #записываем в комментарий текст от пользователя
    user_text = format_anketa(context.user_data['anketa'])
    update.message.reply_text(user_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)         #отправка текста пользователю в виде HTML и по окончанию вызов клавиатуры
    return ConversationHandler.END                      #диалог завершён

def anketa_skip(update, context):                       #пользователь пропускает комментарий
    user_text = format_anketa(context.user_data['anketa'])              #вывод никнейма и оценки
    update.message.reply_text(user_text, reply_markup=main_keyboard(), parse_mode=ParseMode.HTML)
    return ConversationHandler.END

def format_anketa(anketa):                              #вывод никнейма, оценки и комментария (если он есть)
    user_text = f"""<b>Имя фамилия</b>: {anketa['name']}
<b>Оценка</b>: {anketa['rating']}
"""
    if 'comment' in anketa:                 #если пользователь оставил комментарий
        user_text += f"\n<b>Комментарий</b>: {anketa['comment']}"
    return user_text

def anketa_dontknow(update, context):       #возврат к диалогу
    update.message.reply_text('Я вас не понимаю')