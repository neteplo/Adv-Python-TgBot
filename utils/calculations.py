
def calculate_calories_norm(weight: int, height: int, age: int) -> int:
    '''
    Рассчитывает норму калорий по переданным весу, росту и возрасту
    '''
    calories_norm = 10 * weight + 6.25 * height - 5 * age + 200
    return int(calories_norm)

def calculate_water_norm(weight: int) -> int:
    '''
    Рассчитывает базовую норму воды в мл.
    '''
    return weight * 30


def calculate_calories_burned(activity_type: str, time_spend: int) -> int:
    '''
    Рассчитывает количество потраченных калорий по типу активности и времени
    '''

    calories_per_minute = {
        'gym': 7,        # Качалка: 7 ккал/мин
        'run': 10,       # Бег: 10 ккал/мин
        'cycle': 8,      # Велосипед: 8 ккал/мин
        'swim': 9,       # Плаванье: 9 ккал/мин
        'ping-pong': 5,  # Пинг-понг: 5 ккал/мин
        'squash': 12     # Сквош: 12 ккал/мин
    }

    return calories_per_minute.get(activity_type, 0) * time_spend