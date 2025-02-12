from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandObject
from textwrap import dedent

from states import Activity, Food
from storage import get_user_data, update_user_data
from keyboards.inline_keyboards import activity_type_kb, create_food_keyboard
from utils.calculations import calculate_calories_burned
from utils.food_search import search_food

router = Router()


# Обработчик команды /log_water
@router.message(Command('log_water'))
async def cmd_log_water(message: Message, command: CommandObject):
    try:
        water_amount = int(command.args)
    except TypeError:
        await message.answer('Пожалуйста, исполните команду вот так: /log_water <объем воды (мл)>')

    user_data = get_user_data(message.from_user.id)
    current_water = user_data.get('water_logged', 0) + water_amount
    update_user_data(message.from_user.id, {'water_logged': current_water})

    await message.answer(f'✅ Записано {water_amount} мл воды.\nВсего выпито: {current_water} мл.')


# Обработчик команды /log_workout
@router.message(Command('log_workout'))
async def cmd_log_workout(message: Message, command: CommandObject, state: FSMContext):
    try:
        time_spent = int(command.args)
    except TypeError:
        await message.answer('Пожалуйста, исполните команду вот так: /log_water <время активности (мин)>')

    await state.update_data(time_spent=time_spent)
    await message.answer('Выберите тип активности:', reply_markup=activity_type_kb)


# Обработчик выбора типа активности
@router.callback_query(F.data.in_({'gym', 'run', 'cycle', 'swim', 'ping-pong', 'squash'}))
async def process_activity_type(callback: CallbackQuery, state: FSMContext):
    activity_data = await state.get_data()
    time_spent = activity_data.get('time_spent', 0)

    # Рассчитываем дополнительные 200 мл за каждые 30 минут
    additional_water = (time_spent // 30) * 200

    # Рассчитываем сожженные калории в зависимости от типа активности
    activity_type = callback.data
    calories_burned = calculate_calories_burned(activity_type, time_spent)

    # Обновляем данные пользователя в глобальном словаре
    user_id = callback.from_user.id
    current_data = get_user_data(user_id)
    updated_data = {
        'calories_burned': current_data.get('calories_burned', 0) + calories_burned,
        'water_goal': current_data.get('water_goal', 0) + additional_water
    }
    update_user_data(user_id, updated_data)

    # Отправляем результат пользователю
    await callback.message.answer(
        f'✅ Активность записана!\n\n'
        f'🔥 Сожжено калорий: {calories_burned}\n'
        f'💧 Воды добавлено к цели: {additional_water} мл'
    )

    # Завершаем обработку callback
    await callback.answer()


# Обработчик команды /log_food
@router.message(Command('log_food'))
async def log_food(message: Message, command: CommandObject, state: FSMContext):
    # Получаем аргумент команды (название продукта)
    product_name = command.args

    # Ищем продукты через API
    products = search_food(product_name)
    if not products:
        await message.answer('Продукты не найдены. Попробуйте еще раз.')
        return

    # Сохраняем список продуктов в состоянии
    await state.set_state(Food.products)
    await state.update_data(products=products)

    # Создаем и отправляем inline-клавиатуру
    keyboard = create_food_keyboard(products)
    await message.answer("Выберите продукт:", reply_markup=keyboard)
    await state.set_state(Food.selected_product)


@router.callback_query(F.data.startswith('food_'))
async def process_food_selection(callback: CallbackQuery, state: FSMContext):
    # Извлекаем ID продукта из callback_data
    product_id = callback.data.split('_')[1]

    # Получаем список продуктов из состояния
    user_data = await state.get_data()
    products = user_data.get('products', [])

    # Находим выбранный продукт
    selected_product = next((p for p in products if p['id'] == product_id), None)
    if not selected_product:
        await callback.message.answer('Ошибка: продукт не найден.')
        await callback.answer()
        return

    # Сохраняем выбранный продукт в состоянии

    await state.update_data(selected_product=selected_product)

    # Запрашиваем количество продукта (в граммах)
    await callback.message.answer(f'Вы выбрали: {selected_product["name"]} ({selected_product["brand"]}, {selected_product["quantity"]})\n'
                                  f'Калорийность: {selected_product["calories"]} ккал/100г\n\n'
                                  f'Введите количество продукта в граммах:')

    await state.set_state(Food.food_quantity)
    await callback.answer()


@router.message(Food.food_quantity)
async def process_food_quantity(message: Message, state: FSMContext):
    try:
        quantity = float(message.text)  # Количество продукта в граммах
    except TypeError:
        await message.answer('Пожалуйста, введите число.\nПример: 150')
        return

    # Получаем выбранный продукт из состояния
    user_data = await state.get_data()
    selected_product = user_data.get('selected_product')

    # Рассчитываем калории
    calories_per_100g = selected_product.get('calories', 0)
    total_calories = (calories_per_100g * quantity) / 100

    # Обновляем данные пользователя в глобальном словаре
    user_id = message.from_user.id
    current_data = get_user_data(user_id)
    updated_data = {
        'calories_logged': current_data.get('calories_logged', 0) + total_calories
    }
    update_user_data(user_id, updated_data)

    # Отправляем результат пользователю
    await message.answer(
        f'✅ Продукт записан!\n\n'
        f'🍎 Продукт: {selected_product["name"]}\n'
        f'⚖️ Количество: {quantity} г\n'
        f'🔥 Калории: {total_calories:.2f} ккал'
    )

    # Очищаем состояние
    await state.clear()

