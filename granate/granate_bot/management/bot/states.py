from aiogram.dispatcher.filters.state import StatesGroup, State


class StartStatesGroup(StatesGroup):
    start = State()
    menu = State()
    choose_action = State()


class AskQuestionStatesGroup(StatesGroup):
    ask = State()
    write_question = State()
    edit_question = State()
    send_question = State()
    more_question = State()
    notify_answ = State()

class NotifyStatesGroup(StatesGroup):
    get_notification = State()
    allow_notification = State()

class OpportunityStatesGroup(StatesGroup):
    info_opportunity = State()

class AboutStatesGroup(StatesGroup):
    info_project = State()
