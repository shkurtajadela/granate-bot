from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikbb_start = InlineKeyboardButton(text='Начать ➡',
                                         callback_data='start')

ikbb_ask_question = InlineKeyboardButton(text='ОСТАВИТЬ ВОПРОС',
                                         callback_data='ask_question')

ikbb_allow_notification = InlineKeyboardButton(text='ПОДПИСАТЬСЯ НА РАССЫЛКУ',
                                         callback_data='get_notification')

ikbb_info_opportunity = InlineKeyboardButton(text='АКТУАЛЬНЫЕ ВОЗМОЖНОСТИ',
                                         callback_data='info_opportunity')

ikbb_info_project = InlineKeyboardButton(text='О ПРОЕКТЕ',
                                         callback_data='info_project')


ikbb_notification_yes = InlineKeyboardButton(text='ЭТО МНЕ НАДО',
                                         callback_data='yes')

ikbb_notification_opp_yes = InlineKeyboardButton(text='ПОДПИСАТЬСЯ НА РАССЫЛКУ',
                                         callback_data='yes')

ikbb_notification_no = InlineKeyboardButton(text='НАЗАД В МЕНЮ',
                                         callback_data='no')

ikbb_opport_yes = InlineKeyboardButton(text='ХОЧУ!',
                                         callback_data='yes')


ikbb_question_yes = InlineKeyboardButton(text='КРУТО, ХОЧУ ЗАДАТЬ',
                                         callback_data='yes')

ikbb_question_no = InlineKeyboardButton(text='НАЗАД В МЕНЮ',
                                         callback_data='no')

ikbb_question_edit_no = InlineKeyboardButton(text='ВСЕ ОК, ОТПРАВЛЯЕМ',
                                         callback_data='yes')

ikbb_question_edit = InlineKeyboardButton(text='ХОЧУ ПЕПЕПИСАТЬ',
                                         callback_data='again')

ikbb_more_question = InlineKeyboardButton(text='ЗАДАТЬ ЕЩЕ ВОПРОС',
                                         callback_data='more')


ikbb_menu = InlineKeyboardButton(text='МЕНЮ',
                                         callback_data='menu')


ikbb_project = InlineKeyboardButton(text='КРУТО, СПАСИБО',
                                         callback_data='menu')


ikbb_intern = InlineKeyboardButton(text='Подать на стажировку',
                                         callback_data='internship', url="granate.space")


def get_ikb_start() -> InlineKeyboardMarkup:
    ikb_start = InlineKeyboardMarkup(row_width=1)
    ikb_start.add(ikbb_ask_question, ikbb_allow_notification, ikbb_info_opportunity, ikbb_info_project)
    return ikb_start

def get_ikb_notification() -> InlineKeyboardMarkup:
    ikb_start = InlineKeyboardMarkup(row_width=1)
    ikb_start.add(ikbb_notification_yes, ikbb_notification_no)
    return ikb_start

def get_ikb_notif_opp() -> InlineKeyboardMarkup:
    ikb_start = InlineKeyboardMarkup(row_width=1)
    ikb_start.add(ikbb_notification_opp_yes, ikbb_notification_no)
    return ikb_start

def get_ikb_menu() -> InlineKeyboardMarkup:
    ikb_start = InlineKeyboardMarkup(row_width=1)
    ikb_start.add(ikbb_menu)
    return ikb_start

def get_ikb_project() -> InlineKeyboardMarkup:
    ikb_start = InlineKeyboardMarkup(row_width=1)
    ikb_start.add(ikbb_project)
    return ikb_start

def get_ikb_opportunity() -> InlineKeyboardMarkup:
    ikb_start = InlineKeyboardMarkup(row_width=1)
    ikb_start.add(ikbb_opport_yes, ikbb_notification_no)
    return ikb_start

def get_ikb_question() -> InlineKeyboardMarkup:
    ikb_start = InlineKeyboardMarkup(row_width=1)
    ikb_start.add(ikbb_question_yes, ikbb_question_no)
    return ikb_start

def get_ikb_question_edit() -> InlineKeyboardMarkup:
    ikb_start = InlineKeyboardMarkup(row_width=1)
    ikb_start.add(ikbb_question_edit_no, ikbb_question_edit)
    return ikb_start

def get_ikb_question_more() -> InlineKeyboardMarkup:
    ikb_start = InlineKeyboardMarkup(row_width=1)
    ikb_start.add(ikbb_more_question, ikbb_menu)
    return ikb_start
