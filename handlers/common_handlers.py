from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from textwrap import dedent
from storage import get_user_data

router = Router()

# Обработчик команды /start
@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.reply(dedent('''
    Добро пожаловать! 🐸
    Я буду помогать тебе в поддержании здорового образа жизни.
    
    Краткий список того, что я умею:
    · Рассчитывать индивидуальную норму потребления воды и пищи
    · Вести учет физической активности и потребленных калорий
    
    Введите /help для получения подробного списка команд
    ''')
                        )


# Обработчик команды /help
@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.reply(dedent('''
    Доступные команды:
    /set_profile – Начните тут – настройка профиля пользователя:
    · Анкетирование пользователя с целью расчета индивидуальных норм
    /log_water – Логирование выпитой воды:
    · Сохраняет, сколько воды выпито
    · Показывает, сколько осталось до выполнения нормы
    /log_food – Логирование съеденной еды:
    · Сохраняет калорийность введенных продуктов
    /log_workout – Логирование физической активности
    · Фиксирует сожжённые в ходе активности калории
    · Учитывает расход воды на тренировке
    /check_progress – Показывает отчет:
    · Количестве потребленных калорий и воды
    · Количество воды и калорий оставшихся до выполнения индивидуальной нормы
    ''')
                        )


# Обработчик команды /check_progress
@router.message(Command('check_progress'))
async def end_survey(message: Message):

    user_data = get_user_data(message.from_user.id)

    summary_message = (dedent(f'''
        📊 Прогресс:
        Вода:
        - Выпито: {user_data.get('water_logged')} мл из {user_data.get('water_goal')} мл.
        - Осталось: {user_data.get('water_goal') - user_data.get('water_logged')} мл.
        
        Калории:
        - Потреблено: {user_data.get('calories_logged')} ккал из {user_data.get('calories_goal')} ккал.
        - Сожжено: {user_data.get('calories_burned')} ккал.
        - Баланс: {user_data.get('calories_goal') + user_data.get('calories_burned') - user_data.get('calories_logged')} ккал.
        ''')
                       )

    await message.answer(summary_message)


def setup_handlers(dp):
    dp.include_router(router)

