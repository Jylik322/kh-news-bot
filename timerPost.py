
from datetime import date, time
import newsbot
import parsing
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, messageentity, parsemode
from telegram.ext import  CallbackContext
def alarm(context:CallbackContext) -> None:
    job = context.job
    context.bot.send_message(job.context, text='Beep!')
def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True
def set_timer(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    try:
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('Sorry we can not go back to future!')
            return

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(alarm, due, context=chat_id, name=str(chat_id))

        text = 'Timer successfully set!'
        if job_removed:
            text += ' Old one was removed.'
        update.message.reply_text(text)
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')
def unset(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'Timer successfully cancelled!' if job_removed else 'You have no active timer.'
    update.message.reply_text(text)

def infoMain(context:CallbackContext) -> None:
    job = context.job
    heading = 'Главное'
    posts = parsing.parse()
    postsWithHeadings = []
    for post in posts:
            if post.post_Heading == heading:
                postsWithHeadings.append(post)
    for post in postsWithHeadings:
                context.bot.send_message(job.context,text='<a href="'+post.post_Link+'">'+post.post_Title+'</a>\n'+post.post_ShortDesc+'\n\n<i>'+post.post_Date+'</i>\n', 
                  parse_mode=telegram.ParseMode.HTML)

def infoCovid(context:CallbackContext) -> None:
    job = context.job
    heading = 'COVID'
    posts = parsing.parse()
    postsWithHeadings = []
    for post in posts:
            if post.post_Heading == heading:
                postsWithHeadings.append(post)
    for post in postsWithHeadings:
                context.bot.send_message(job.context,text='<a href="'+post.post_Link+'">'+post.post_Title+'</a>\n'+post.post_ShortDesc+'\n\n<i>'+post.post_Date+'</i>\n', 
                  parse_mode=telegram.ParseMode.HTML)

def infoEvents(context:CallbackContext) -> None:
    job = context.job
    heading = 'Мероприятия'
    posts = parsing.parse()
    postsWithHeadings = []
    for post in posts:
            if post.post_Heading == heading:
                postsWithHeadings.append(post)
    for post in postsWithHeadings:
                context.bot.send_message(job.context,text='<a href="'+post.post_Link+'">'+post.post_Title+'</a>\n'+post.post_ShortDesc+'\n\n<i>'+post.post_Date+'</i>\n', 
                  parse_mode=telegram.ParseMode.HTML)

def infoSociety(context:CallbackContext) -> None:
    job = context.job
    heading = 'Общество'
    posts = parsing.parse()
    postsWithHeadings = []
    for post in posts:
            if post.post_Heading == heading:
                postsWithHeadings.append(post)
    for post in postsWithHeadings:
                context.bot.send_message(job.context,text='<a href="'+post.post_Link+'">'+post.post_Title+'</a>\n'+post.post_ShortDesc+'\n\n<i>'+post.post_Date+'</i>\n', 
                  parse_mode=telegram.ParseMode.HTML)

def daily(update: Update, context: CallbackContext,heading) -> None:
    chat_id = update.callback_query.message.chat_id
    b = time(11, 00, 00)
    if(heading == 'Главное'):
        context.job_queue.run_daily(infoMain, b, context=chat_id, name=str(chat_id))
    if(heading == 'COVID'):
        context.job_queue.run_daily(infoCovid, b, context=chat_id, name=str(chat_id))
    if(heading == 'Мероприятия'):
        context.job_queue.run_daily(infoEvents, b, context=chat_id, name=str(chat_id))
    if(heading == 'Общество'):
        context.job_queue.run_daily(infoSociety, b, context=chat_id, name=str(chat_id))
    keyboard = newsbot.back_buttons()
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text('Теперь вы будете получать новости в 13:00 по Киеву. Тематика - '+heading,reply_markup=reply_markup)