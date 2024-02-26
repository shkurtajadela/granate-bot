from aiogram.dispatcher.filters.state import StatesGroup, State


class StartStatesGroup(StatesGroup):
    start = State()
    choose_action = State()


class AskQuestionStatesGroup(StatesGroup):
    ask = State()
    notify_answ = State()

class NotifyStatesGroup(StatesGroup):
    allow_notification = State()

class OpportunityStatesGroup(StatesGroup):
    info_opportunity = State()

class AboutStatesGroup(StatesGroup):
    info_project = State()