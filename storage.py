users = {}


def update_user_data(user_id: int, data: dict):
    '''
    Сохраняет данные пользователя в глобальный словарь.
    Если пользователь уже существует, обновляет его данные.
    '''
    if user_id not in users:
        users[user_id] = {
            'weight': 0,
            'height': 0,
            'age': 0,
            'activity': 0,
            'city': '',
            'water_goal': 0,
            'calories_goal': 0,
            'water_logged': 0,
            'calories_logged': 0,
            'calories_burned': 0
        }
    users[user_id].update(data)


def get_user_data(user_id: int) -> dict:
    '''
    Возвращает данные пользователя по его ID.
    Если данные отсутствуют, возвращает пустой словарь.
    '''
    return users.get(user_id, {})