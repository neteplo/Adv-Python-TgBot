from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


calories_fill_type_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='⌨️Введу свою норму вручную', callback_data='manual_calories')],
        [InlineKeyboardButton(text='🤖Рассчитать норму автоматически', callback_data='auto_calories')]
    ],
    input_field_placeholder='Выберите способ расчета дневной нормы калорий:'
)


activity_type_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='🏋Качалка', callback_data='gym'),
         InlineKeyboardButton(text='🏃Бег', callback_data='run')],
        [InlineKeyboardButton(text='🚴Велосипед', callback_data='cycle'),
         InlineKeyboardButton(text='🏊Плаванье', callback_data='swim')],
        [InlineKeyboardButton(text='🏓Пинг-понг', callback_data='ping-pong'),
         InlineKeyboardButton(text='🎾Сквош', callback_data='squash')]
    ],
    input_field_placeholder='Выберите тип активности:'
)


def create_food_keyboard(products: list):
    '''
    Создает inline-клавиатуру для выбора продукта.
    '''
    keyboard = []
    for product in products:
        button_text = f"{product['name']} | {product['calories']} ккал на {product['quantity']}"
        keyboard.append([InlineKeyboardButton(text=button_text, callback_data=f"food_{product['id']}")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)