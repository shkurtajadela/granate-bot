from aiogram import types, Dispatcher
from .keyboard import *
from aiogram import Bot
from .states import *
from aiogram.dispatcher import FSMContext
from granate_bot.models import User, Question
from dotenv import load_dotenv
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'granate_bot.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

load_dotenv('.env')
token = os.getenv("TOKEN_API")
bot = Bot(token)

async def cmd_start(msg: types.Message, state: FSMContext) -> None:
    await start(msg.from_user.id)
    await StartStatesGroup.choose_action.set()

async def start(chat_id):
    new_text = '<i>По нажатию кнопки ты узнаешь о функции и после сможешь ее использовать</i>'
    reply_markup = get_ikb_start()
    users = User.objects.filter(chat_id=chat_id)
    if len(users) == 0:
        new_user = User(chat_id=chat_id)
        new_user.save()
    await bot.send_photo(chat_id=chat_id, caption=new_text, photo=open('/var/bot/granate-bot/granate/granate_bot/management/img/старт.png','rb'), reply_markup=reply_markup, parse_mode=types.ParseMode.HTML)


async def callback_menu(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await start(callback.from_user.id)
        await StartStatesGroup.choose_action.set()

async def callback_load_user_choice(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:    
        if callback.data == 'ask_question':
            new_text = '*вопрос поступает анонимно\n*старайся писать чётко и понятно, чтобы медиа-команда точно смогла на него ответить\n*вопросы могут быть на любые волнующие тебя темы'
            reply_markup = get_ikb_question()
            await bot.send_photo(chat_id=callback.from_user.id, caption=new_text, photo=open("/var/bot/granate-bot/granate/granate_bot/management/img/задай вопрос.png", 'rb'), reply_markup=reply_markup)
            await AskQuestionStatesGroup.write_question.set()
        elif callback.data == 'get_notification':
            new_text = 'Эта функция позволит тебе всегда быть в курсе всех событий и возможностей - мероприятия, полезности и подборки новостей\n\nБудь на связи с granate.space'
            reply_markup = get_ikb_notification()
            await bot.send_message(chat_id=callback.from_user.id, text=new_text, reply_markup=reply_markup)
            await NotifyStatesGroup.allow_notification.set() 
        elif callback.data == 'info_opportunity':
            new_text = 'Хочешь узнать, что есть для тебя сейчас?'
            reply_markup = get_ikb_opportunity()
            photo_path = '/var/bot/granate-bot/granate/granate_bot/management/img/возможности.png'
            await bot.send_photo(chat_id=callback.from_user.id, caption=new_text, photo=open(photo_path, 'rb'), reply_markup=reply_markup)
            await OpportunityStatesGroup.info_opportunity.set()
        elif callback.data == 'info_project':
            new_text = 'Узнать подробнее: granate.space'
            reply_markup = get_ikb_project()
            photo_path = '/var/bot/granate-bot/granate/granate_bot/management/img/о проекте.png'
            await bot.send_photo(chat_id=callback.from_user.id, caption=new_text, photo=open(photo_path, 'rb'), reply_markup=reply_markup)
            await StartStatesGroup.menu.set() 


async def callback_load_question(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.data == 'yes':
            new_text = 'Напишите ваш вопрос:'
            await bot.send_message(chat_id=callback.from_user.id, text=new_text)
            await AskQuestionStatesGroup.edit_question.set()
        elif callback.data == 'no':
            await start(callback.from_user.id)
            await StartStatesGroup.choose_action.set()

async def callback_load_opportunity(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.data == 'yes':
            new_text = '....отправка всех возможностей сообщением....\n\n'
            new_text += 'Чтобы своевременно узнавать о возможностях, можно подписаться на нашу рассылку'
            reply_markup = get_ikb_notif_opp()
            await bot.send_message(chat_id=callback.from_user.id, text=new_text, reply_markup=reply_markup)
            await NotifyStatesGroup.allow_notification.set()
        elif callback.data == 'no':
            await start(callback.from_user.id)
            await StartStatesGroup.choose_action.set()


async def callback_load_notification(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if callback.data == 'yes':
            user = User.objects.get(chat_id=callback.from_user.id)
            user.get_notified = True
            user.save()
            new_text = 'Спасибо за подписку!'
            reply_markup = get_ikb_menu()
            await bot.send_message(chat_id=callback.from_user.id, text=new_text, reply_markup=reply_markup)
            await StartStatesGroup.menu.set()
        elif callback.data == 'no':
            await start(callback.from_user.id)
            await StartStatesGroup.choose_action.set()

async def edit_question(msg: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['question'] = msg.text
        reply_markup = get_ikb_question_edit()
        new_text = f'Давай проверим, всё ли верно\n\n"{msg.text}"'
        await bot.send_message(chat_id=msg.from_id, text=new_text, reply_markup=reply_markup)
        await AskQuestionStatesGroup.send_question.set()

# отправить вопрос в группу "медиа" 
async def callback_question_send(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        if callback.data == 'again':
            new_text = 'Напишите ваш вопрос:'
            await bot.send_message(chat_id=callback.from_user.id, text=new_text)
            await AskQuestionStatesGroup.edit_question.set()
        elif callback.data == 'yes':
            question = Question(chat_id=callback.from_user.id, question=data['question'])
            question.save()
            text = f"User with id {callback.from_user.id} sent the next question (question_id = {question.id}): \n"
            text += data['question']
            reply_markup = get_ikb_question_more()
            #await bot.send_message(chat_id="-1001764415837", text=text) # добавить id группа чтобы туда сообщение пришли
            new_text = 'Спасибо большое за твой вопрос! Начинаем работать над ответом\nТы можешь задать несколько вопросов. Просто нажми "задать ещё вопрос"'
            await bot.send_message(chat_id=callback.from_user.id, text=new_text, reply_markup=reply_markup)
            await AskQuestionStatesGroup.more_question.set() 
        elif callback.data == 'menu':
            await start(callback.from_user.id)
            await StartStatesGroup.choose_action.set()

async def callback_more_question(callback: types.CallbackQuery, state: FSMContext) -> None:
    async with state.proxy() as data:
        if callback.data == 'more':
            new_text = 'Напишите ваш вопрос:'
            await bot.send_message(chat_id=callback.from_user.id, text=new_text)
            await AskQuestionStatesGroup.edit_question.set()
        elif callback.data == 'menu':
            await start(callback.from_user.id)
            await StartStatesGroup.choose_action.set()

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
    dp.register_message_handler(cmd_start, commands=['start'], state=['*', StartStatesGroup.start])
    dp.register_message_handler(send_to_user, commands=['send_to_user'], state='*')
    dp.register_message_handler(send_to_all, commands=['send_to_all'], state='*')
    dp.register_message_handler(send_to_all_on, commands=['send_to_all_on'], state='*')
    dp.register_callback_query_handler(callback_load_user_choice, state=StartStatesGroup.choose_action)
    dp.register_callback_query_handler(callback_load_notification, state=NotifyStatesGroup.allow_notification)
    dp.register_callback_query_handler(callback_question_send, state=AskQuestionStatesGroup.send_question)
    dp.register_message_handler(edit_question, state=AskQuestionStatesGroup.edit_question)
    dp.register_callback_query_handler(callback_load_question, state=AskQuestionStatesGroup.write_question)
    dp.register_callback_query_handler(callback_more_question, state=AskQuestionStatesGroup.more_question)
    dp.register_callback_query_handler(callback_menu, state=StartStatesGroup.menu)
    dp.register_callback_query_handler(callback_load_opportunity, state=OpportunityStatesGroup.info_opportunity)

def register_handlers(dp: Dispatcher) -> None:
    register_commands(dp=dp)
