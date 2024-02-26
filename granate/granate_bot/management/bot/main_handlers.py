from aiogram import types, Dispatcher
from .keyboard import *
from aiogram import Bot
from .states import *
from aiogram.dispatcher import FSMContext
# from .database import *
from granate_bot.models import User, Question
from dotenv import load_dotenv
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

load_dotenv('.env')
token = os.getenv("TOKEN_API")
bot = Bot(token)

async def cmd_start(msg: types.Message) -> None:
    new_text = 'Привет, я ....! Что хотите делать дальше'
    reply_markup = get_ikb_start()
    users = User.objects.filter(chat_id=msg.from_user.id)
    if len(users) == 0:
        new_user = User(chat_id=msg.from_user.id)
        new_user.save()
    await bot.send_message(chat_id=msg.from_user.id, text=new_text, reply_markup=reply_markup)
    await StartStatesGroup.choose_action.set()

async def callback_load_user_choice(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:    
        if callback.data == 'ask_question':
            new_text = 'Write your question'
            await bot.send_message(chat_id=callback.from_user.id, text=new_text)
            await AskQuestionStatesGroup.ask.set()
        elif callback.data == 'get_notification':
            new_text = 'Do you want to get special notification'
            reply_markup = get_ikb_notification()
            await bot.send_message(chat_id=callback.from_user.id, text=new_text, reply_markup=reply_markup)
            await NotifyStatesGroup.allow_notification.set() 
        elif callback.data == 'info_opportunity':
            new_text = 'возможномти:......\n Если хотите оставить заявку на стажировку, нажимаете кнопку'
            reply_markup = get_ikb_opportunity()
            await bot.send_message(chat_id=callback.from_user.id, text=new_text, reply_markup=reply_markup)
            await StartStatesGroup.start.set()
        elif callback.data == 'info_project':
            new_text = 'О проекте: https://www.figma.com/file/CxfaiElIpeYC86diKSZ9Lu/media-bot-Userflow?type=whiteboard&node-id=0-1'
            await bot.send_message(chat_id=callback.from_user.id, text=new_text)
            await StartStatesGroup.start.set() 

async def callback_load_notification(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:    
        if callback.data == 'yes':
            user = User.objects.get(chat_id=callback.from_user.id)
            user.get_notified = True
            user.save()
            new_text = 'Thank you! We will notify you for everything'
            await bot.send_message(chat_id=callback.from_user.id, text=new_text)
            await StartStatesGroup.start.set()
        elif callback.data == 'no':
            new_text = 'Привет, я ....! Что хотите делать дальше'
            reply_markup = get_ikb_start()
            await bot.send_message(chat_id=callback.from_user.id, text=new_text, reply_markup=reply_markup)
            await StartStatesGroup.start.set()

# отправить вопрос в группу "медиа" 
async def question_load(msg: types.Message) -> None:
    question = Question(chat_id=msg.from_user.id, question=msg.text)
    question.save()

    text = f"User with id {msg.from_user.id} sent the next question (question_id = {question.id}): \n"
    text += msg.text 
    await bot.send_message(chat_id="-1001764415837", text=text) # добавить id группа чтобы туда сообщение пришли
    new_text = 'Thank you! your question is send to our chat group, we are going to answer soon'
    await bot.send_message(chat_id=msg.from_id, text=new_text)

# /send_to_user chat_id question_id answer
async def send_to_user(msg: types.Message) -> None:
    admin = User.objects.get(chat_id=msg.from_user.id)
    if admin.admin:
        text = msg.text[14:]

        # get user_id
        first_space_index = text.index(' ')
        user_id = text[:first_space_index]

        # get question_id and answer
        snd_space = text[(first_space_index+1):].index(' ')
        question_id = text[(first_space_index+1):(snd_space+first_space_index+1)]
        text_to_send = text[first_space_index+snd_space+1:]
        question = Question.objects.filter(chat_id=user_id, id=question_id)
        if len(question) != 0:
            question[0].answered = True
            question[0].save()

            try:
                await bot.send_message(chat_id=user_id, text=text_to_send)
                await bot.send_message(chat_id=msg.from_user.id, text="Message was sent to user")
            except:
                user = User.objects.get(chat_id=user_id)
                if user:
                    user.delete()
                await bot.send_message(chat_id=msg.from_user.id, text="Message could not be send to user. Maybe he has blocked the bot")
        else:
            await bot.send_message(chat_id=msg.from_user.id, text="Message could not be send to user. Check user_id and question_id")

# /send_to_all - отправить рассылки всем пользователям 
async def send_to_all(msg: types.Message) -> None:
    admin = User.objects.get(chat_id=msg.from_user.id)
    
    if admin.admin:
        text = msg.text[13:]
        users = User.objects.all()
        for user in users:
            try:
                await bot.send_message(chat_id=user.chat_id, text=text)
            except:
                user.delete()
        await bot.send_message(chat_id=msg.from_user.id, text="Message was sent to everybody")

# /send_to_all - отправить рассылки подписанным пользователям 
async def send_to_all_on(msg: types.Message) -> None:
    admin = User.objects.get(chat_id=msg.from_user.id)

    if admin.admin:
        text = msg.text[16:]
        users = User.objects.filter(get_notified=True)
        for user in users:
            try:
                await bot.send_message(chat_id=user.chat_id, text=text)
            except:
                user.delete()
        await bot.send_message(chat_id=msg.from_user.id, text="Message was sent to everybody with notification on")
            

def register_commands(dp: Dispatcher) -> None:
    dp.register_message_handler(cmd_start, commands=['start'], state='*')
    dp.register_message_handler(send_to_user, commands=['send_to_user'], state='*')
    dp.register_message_handler(send_to_all, commands=['send_to_all'], state='*')
    dp.register_message_handler(send_to_all_on, commands=['send_to_all_on'], state='*')
    dp.register_callback_query_handler(callback_load_user_choice, state=StartStatesGroup.choose_action)
    dp.register_callback_query_handler(callback_load_notification, state=NotifyStatesGroup.allow_notification)
    dp.register_message_handler(question_load, state=AskQuestionStatesGroup.ask)

def register_handlers(dp: Dispatcher) -> None:
    register_commands(dp=dp)