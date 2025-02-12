import requests


def search_food(product_name: str):
    '''
    Ищет продукты по названию через API OpenFoodFacts.
    Возвращает список из 5 продуктов.
    '''
    url = 'https://world.openfoodfacts.org/cgi/search.pl'
    params = {
        'search_terms': product_name,
        'search_simple': 1,
        'action': 'process',
        'json': 1,
        'page_size': 5  # Ограничиваем результат 5 продуктами
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверяем, что запрос успешен
        data = response.json()

        products = []
        for product in data.get('products', []):
            product_info = {
                'name': product.get('product_name', 'Неизвестно'),
                'calories': product.get('nutriments', {}).get('energy-kcal_100g', 0),
                'brand': product.get('brands', 'Неизвестно'),
                'quantity': product.get('quantity', '100 g'),
                'id': product.get('id')  # Уникальный ID продукта
            }
            products.append(product_info)
        if len(products) > 0:
            return products
        else:
            return None
    except Exception as e:
        print(f'Ошибка при запросе к API: {e}')