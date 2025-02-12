from aiogram.fsm.state import State, StatesGroup


class Form(StatesGroup):
    name = State()
    age = State()
    weight = State()
    height = State()
    activity = State()
    city = State()
    calories_goal = State()


class Activity(StatesGroup):
    time_spent = State()


class Food(StatesGroup):
    products = State()
    selected_product = State()
    food_quantity = State()