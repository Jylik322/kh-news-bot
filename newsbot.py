import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, messageentity, parsemode
import telegram
from telegram.constants import PARSEMODE_HTML
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from telegram.message import Message
import parsing
import weather
import payment
reg_list = ["",""]
account = 0
condition = 0
chat_id = 0
check_strings = ["Your input is correct","Your input is empty","Parameter of command is not digit"]

def is_number(a):
    flag = False
    if a.isdigit():
        flag = True
    elif '.' in a:
        elements = a.split('.')
        if len(elements[1]) == 2:
            flag = True
    return flag

def check(string_in):
    n=0
    elements = string_in.split(' ')
    if not len(string_in) > 0:
        n=1
    elif not is_number(string_in):
        n=2
    return n
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
    reg_title = ["Показать последние новости","Показать текущую погоду"]
    reg_code = ["news","weather"]
    key_lst = []
    for i in range(len(reg_title)):
        key_lst.append(InlineKeyboardButton(reg_title[i], callback_data=reg_code[i]))
    kb = [key_lst]
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

def start(update: Update, context: CallbackContext) -> None:
    keyboard = key_buttons()
    reply_markup = InlineKeyboardMarkup(keyboard)
    keyboard2 = donate_button()
    reply2 = InlineKeyboardMarkup(keyboard2)
    update.message.reply_text('<b><i>Вы можете поддержать проект</i></b>', reply_markup=reply2,parse_mode=telegram.ParseMode.HTML)
    update.message.reply_text('<b><i>Добро пожаловать в бот KhNews!</i>\nТут вы можете посмотреть последние новости в Харькове, либо же просто посмотреть погоду</b>', reply_markup=reply_markup,parse_mode=telegram.ParseMode.HTML)

def ShowLastNews(update,context,head):
    posts = parsing.parse()
    postsWithHeadings = []
    for post in posts:
            if post.post_Heading == head:
                postsWithHeadings.append(post)
    for post in postsWithHeadings:
            if post == postsWithHeadings[len(postsWithHeadings)-1]:
                keyboard = back_buttons()
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.callback_query.message.edit_text(text='<a href="'+post.post_Link+'">'+post.post_Title+'</a>\n'+post.post_ShortDesc+'\n', 
                  parse_mode=telegram.ParseMode.HTML,reply_markup=reply_markup)
            else:
                update.callback_query.message.edit_text(text='<a href="'+post.post_Link+'">'+post.post_Title+'</a>\n'+post.post_ShortDesc+'\n', 
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
        file = r"C:\Users\jylik\Desktop\Python\images\back.jpg"
        update.callback_query.message.reply_photo(photo = open(file,'rb'))
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
    elif query.data == 'Covid':
        ShowLastNews(update,context,'COVID')
    elif query.data == 'Events':
        ShowLastNews(update,context,'Мероприятия')
    elif query.data == 'Society':
        ShowLastNews(update,context,'Общество')

def echo(update, context):
    global condition, account
    string_in = update.message.text
    if string_in == '/start':
        start()
    elif string_in == '/donate':
        payment.start_without_shipping_callback(update,context,update.message.chat_id)
    elif string_in == '/news':
        kb = heading_buttons()
        reply_markup = InlineKeyboardMarkup(kb)
        update.message.reply_text(text='<b>Выберите интересующую вас рубрику с <a href="http://innovations.kh.ua/khnews/">нашего сайта</a></b>',
                   parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup)
    elif string_in == '/weather':
         curWeather = weather.GetWeather()
         file = os.path.abspath(os.getcwd()+'\\images\\back.jpg')
         update.message.reply_photo(photo = open(file,'rb'))
         keyboard = back_buttons()
         reply_markup = InlineKeyboardMarkup(keyboard)
         update.message.reply_text(text="<b>"+curWeather.description+'\nТекущая температура: '+str(curWeather.temperature)+'°\nДавление: '+str(curWeather.pressure)+'\nВлажность: '+ str(curWeather.humidity)+'%</b>', parse_mode=telegram.ParseMode.HTML, reply_markup=reply_markup)

def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("<b>/start</b> - Начать работу с новостным ботом\n<b>/news</b> - Получить последние новости\n<b>/weather</b> - Показать текущую погоду\n<b>/help</b> - Показать доступные команды",parse_mode=telegram.ParseMode.HTML)

def main() -> None:
    """Run the bot."""
    updater = Updater("2041745489:AAGVbqTvRMRCrJX_O6tfnyGdouvxKHsx41s")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
