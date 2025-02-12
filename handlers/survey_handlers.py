from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from typing import Union

from states import Form
from keyboards.inline_keyboards import calories_fill_type_kb
from utils.calculations import calculate_calories_norm, calculate_water_norm
from storage import update_user_data

from textwrap import dedent

router = Router()


# Обработчик команды /set_profile – начало анкетирования
@router.message(Command('set_profile'))
async def cmd_set_profile(message: Message, state: FSMContext):
    await message.reply('Далее вам необходимо ответить на ряд вопросов:\nКак я могу к Вам обращаться?')
    await state.set_state(Form.name)


# Обработка возраста
@router.message(Form.name)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Сколько вам лет?')
    await state.set_state(Form.age)


# Обработка города
@router.message(Form.age)
async def process_age(message: Message, state: FSMContext):
    await state.update_data(age=int(message.text))
    await message.answer('В каком городе вы находитесь?')
    await state.set_state(Form.city)


# Обработка веса
@router.message(Form.city)
async def process_weight(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer('Введите ваш вес в кг:')
    await state.set_state(Form.weight)


# Обработка роста
@router.message(Form.weight)
async def process_height(message: Message, state: FSMContext):
    await state.update_data(weight=int(message.text))
    await message.answer('Введите ваш рост в см:')
    await state.set_state(Form.height)


# Обработка уровня активности
@router.message(Form.height)
async def process_activity(message: Message, state: FSMContext):
    await state.update_data(height=int(message.text))
    await message.answer('Сколько минут в день, в среднем, вы физически активны?')
    await state.set_state(Form.activity)


# Начало обработки нормы калорий
@router.message(Form.activity)
async def process_calories(message: Message, state: FSMContext):
    await state.update_data(activity=int(message.text))
    await message.answer('Как вы хотите задать свою норму калорий?',
                        reply_markup=calories_fill_type_kb)


# Настройка нормы в ручную
@router.callback_query(F.data == 'manual_calories')
async def process_manual_calories(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer('Введите вашу цель по калориям в день:')
    await state.set_state(Form.calories_goal)


# Автоматический расчет нормы
@router.callback_query(F.data == 'auto_calories')
async def process_auto_calories(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)
    user_data = await state.get_data()
    calories_goal = calculate_calories_norm(
        user_data.get('weight'),
        user_data.get('height'),
        user_data.get('age')
    )
    await state.set_state(Form.calories_goal)
    await state.update_data(calories_goal=calories_goal)
    await save_user_data(callback, state)


# Обработка введенной вручную нормы
@router.message(Form.calories_goal)
async def process_calories_input(message: Union[Message], state: FSMContext):
    await state.update_data(calories_goal=int(message.text))
    await save_user_data(message, state)


# Сохранение всех данных локально
async def save_user_data(event: Union[Message, CallbackQuery], state: FSMContext):
    state_user_data = await state.get_data()
    water_goal = calculate_water_norm(state_user_data.get('weight'))
    update_user_data(
        event.from_user.id, {
            **state_user_data,
            'water_goal': water_goal
        }
    )

    answer_text = dedent('''
    Спасибо за ответы!
    Теперь вы можете приступить к трекингу.
    Введите команду /help чтобы ознакомиться с доступными для отслеживания параметрами. 
    ''')

    if isinstance(event, Message):
        await event.answer(answer_text)
    else:
        await event.message.answer(answer_text)
    await state.clear()


def setup_handlers(dp):
    dp.include_router(router)
