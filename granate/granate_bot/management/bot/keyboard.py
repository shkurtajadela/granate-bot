from typing import List
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


ikbb_start = InlineKeyboardButton(text='Начать ➡',
                                         callback_data='start')

ikbb_ask_question = InlineKeyboardButton(text='Вопрос',
                                         callback_data='ask_question')

ikbb_allow_notification = InlineKeyboardButton(text='Рассылки',
                                         callback_data='get_notification')

ikbb_info_opportunity = InlineKeyboardButton(text='Возможности',
                                         callback_data='info_opportunity')

ikbb_info_project = InlineKeyboardButton(text='О проекте',
                                         callback_data='info_project')

ikbb_notification_yes = InlineKeyboardButton(text='Да',
                                         callback_data='yes')

ikbb_notification_no = InlineKeyboardButton(text='Нет',
                                         callback_data='no')


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

def get_ikb_opportunity() -> InlineKeyboardMarkup:
    ikb_start = InlineKeyboardMarkup(row_width=1)
    ikb_start.add(ikbb_intern)
    return ikb_start
