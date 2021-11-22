from typing import Type
from requests.api import head
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, messageentity, parsemode
import telegram
from telegram import message
from telegram.bot import Bot
from telegram.constants import PARSEMODE_HTML
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from telegram.files.inputmedia import InputMedia, InputMediaPhoto
from telegram.message import Message
import parsing
import weather
import timerPost
import payment
import logging
reg_list = ["",""]
account = 0
condition = 0
check_strings = ["Your input is correct","Your input is empty","Parameter of command is not digit"]

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def donate_button():
    reg_title = ["Поддержать проект"]
    reg_code = ["donate"]
    key_lst = []
    for i in range(len(reg_title)):
        key_lst.append(InlineKeyboardButton(reg_title[i], callback_data=reg_code[i]))
    kb = [key_lst]
    return kb
def back_buttons():
    reg_title = ["Вернуться в главное меню"]
    reg_code = ["back"]
    key_lst = []
    for i in range(len(reg_title)):
        key_lst.append(InlineKeyboardButton(reg_title[i], callback_data=reg_code[i]))
    kb = [key_lst]
    return kb
def key_buttons():
    reg_title = ["Последние новости","Текущая погода","Подписка на новости"]
    reg_code = ["news","weather","subscribe"]
    key_lst = []
    for i in range(len(reg_title)):
        key_lst.append(InlineKeyboardButton(reg_title[i], callback_data=reg_code[i]))
    kb = [key_lst[0],key_lst[1]],[key_lst[2]]
    return kb
def heading_buttons():
    reg_title = ['Главное',
    'COVID',
    'События',
    'Общество']
    reg_code = ['Main','Covid','Events','Society']
    key_lst = []
    for i in range(len(reg_title)):
        key_lst.append(InlineKeyboardButton(reg_title[i], callback_data=reg_code[i]))
    kb = [key_lst]
    return kb
def headingTimer_buttons():
    reg_title = ['Главное',
    'COVID',
    'События',
    'Общество']
    reg_code = ['DailyMain','DailyCovid','DailyEvents','DailySociety']
    key_lst = []
    for i in range(len(reg_title)):
        key_lst.append(InlineKeyboardButton(reg_title[i], callback_data=reg_code[i]))
    kb = [key_lst]
    return kb
def start(update: Update, context: CallbackContext) -> None:
    keyboard = key_buttons()
    reply_markup = InlineKeyboardMarkup(keyboard)
    keyboard2 = donate_button()
    reply2 = InlineKeyboardMarkup(keyboard2)
    update.message.reply_text('<b><i>Вы можете поддержать проект</i></b>', reply_markup=reply2,parse_mode=telegram.ParseMode.HTML)
    update.message.reply_text('<b><i>Добро пожаловать в бот KhNews!</i>\nТут вы можете посмотреть последние новости в Харькове, либо же просто посмотреть погоду</b>', reply_markup=reply_markup,parse_mode=telegram.ParseMode.HTML)

def ShowLastNews(update:Update,context:CallbackContext,head):
    posts = parsing.parse()
    postsWithHeadings = []
    for post in posts:
            if post.post_Heading == head:
                postsWithHeadings.append(post)
    for post in postsWithHeadings:
            if post == postsWithHeadings[len(postsWithHeadings)-1]:
                keyboard = back_buttons()
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.callback_query.message.reply_text(text='<a href="'+post.post_Link+'">'+post.post_Title+'</a>\n'+post.post_ShortDesc+'\n\n<i>'+post.post_Date+'</i>\n', 
                  parse_mode=telegram.ParseMode.HTML,reply_markup=reply_markup)
            else:
                update.callback_query.message.reply_text(text='<a href="'+post.post_Link+'">'+post.post_Title+'</a>\n'+post.post_ShortDesc+'\n\n<i>'+post.post_Date+'</i>\n', 
                  parse_mode=telegram.ParseMode.HTML)
 
def button(update: Update, context: CallbackContext) -> None:
    global condition
    query = update.callback_query
    query.answer()
    print(query.data)
    if query.data == 'news':
        kb = heading_buttons()
        reply_markup = InlineKeyboardMarkup(kb)
        update.callback_query.message.edit_text(text='<b>Выберите интересующую вас рубрику с <a href="http://innovations.kh.ua/khnews/">нашего сайта</a></b>',
                   parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup)
                   
    if query.data == 'weather':
        curWeather = weather.GetWeather()
        update.callback_query.message.reply_photo('https://tvdownloaddw-a.akamaihd.net/stills/images/vdt_ru/2021/brus210408_001_kharkovbb_01v.jpg')
        keyboard = back_buttons()
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text(text="<b>"+curWeather.description+'\nТекущая температура: '+str(curWeather.temperature)+'°\nДавление: '+str(curWeather.pressure)+'\nВлажность: '+ str(curWeather.humidity)+'%</b>', parse_mode=telegram.ParseMode.HTML,reply_markup=reply_markup)

    if query.data == 'back':
        keyboard = key_buttons()
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text(text='<b>Вы вернулись в главное меню!</b>',
                  parse_mode=telegram.ParseMode.HTML,reply_markup=reply_markup)
    if query.data == 'donate':
        payment.start_without_shipping_callback(update,context,update.callback_query.message.chat_id)
    if query.data == 'Main':
        ShowLastNews(update,context,'Главное')
    if query.data == 'Covid':
        ShowLastNews(update,context,'COVID')
    if query.data == 'Events':
        ShowLastNews(update,context,'Мероприятия')
    if query.data == 'Society':
        ShowLastNews(update,context,'Общество')

    if(query.data == 'subscribe'):
        keyboard = headingTimer_buttons()
        reply = InlineKeyboardMarkup(keyboard)
        update.callback_query.message.reply_text('<b>Выбрать рубрику для подписки</b>', parse_mode=telegram.ParseMode.HTML,reply_markup=reply)

    if(query.data == 'DailyMain'):
        timerPost.daily(update,context,'Главное')
    if(query.data == 'DailyCovid'):
        timerPost.daily(update,context,'COVID')
    if(query.data == 'DailyEvents'):
        timerPost.daily(update,context,'Мероприятия')
    if(query.data == 'DailySociety'):
        timerPost.daily(update,context,'Общество')

def donate(update:Update,context:CallbackContext):
        payment.start_without_shipping_callback(update,context,update.message.chat_id)
def postNews(update:Update,context:CallbackContext):
        kb = heading_buttons()
        reply_markup = InlineKeyboardMarkup(kb)
        update.message.reply_text(text='<b>Выберите интересующую вас рубрику с <a href="http://innovations.kh.ua/khnews/">нашего сайта</a></b>',
                parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup)
def postWeahter(update:Update,context:CallbackContext):
         global photo
         curWeather = weather.GetWeather()
         photo = update.message.reply_photo('https://tvdownloaddw-a.akamaihd.net/stills/images/vdt_ru/2021/brus210408_001_kharkovbb_01v.jpg')
         keyboard = back_buttons()
         reply_markup = InlineKeyboardMarkup(keyboard)
         update.message.reply_text(text="<b>"+curWeather.description+'\nТекущая температура: '+str(curWeather.temperature)+'°\nДавление: '+str(curWeather.pressure)+'\nВлажность: '+ str(curWeather.humidity)+'%</b>', parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup)
def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("<b>/start</b> - Начать работу с новостным ботом\n<b>/news</b> - Получить последние новости\n<b>/weather</b> - Показать текущую погоду\n<b>/help</b> - Показать доступные команды",parse_mode=telegram.ParseMode.HTML)

def main() -> None:
    """Run the bot."""
    updater = Updater("2041745489:AAGVbqTvRMRCrJX_O6tfnyGdouvxKHsx41s")

    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(CommandHandler("set", timerPost.set_timer))
    updater.dispatcher.add_handler(CommandHandler("unset", timerPost.unset))
    updater.dispatcher.add_handler(CommandHandler("news", postNews))
    updater.dispatcher.add_handler(CommandHandler("weather", postWeahter))
    


    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
