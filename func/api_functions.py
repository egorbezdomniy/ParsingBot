import requests


def authenticated_get_request(credentials):
    try:
        response = requests.get('https://megaparsing.pythonanywhere.com/users', params=credentials)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return f"Ошибка: {response.status_code}"
    except Exception as e:
        return f"Ошибка при запросе: {e}"


def admin_request_get(chat_id):
    credentials = {
        'app_password': 'ERZHNPAss12389!',
        'chat_id': '7777777'
    }

    response = requests.get('https://megaparsing.pythonanywhere.com/users/', params=credentials)
    if response.status_code == 200:
        data = response.json()
        chat_id_str = str(chat_id)
        for item in data:
            if item['chat_id'].isdigit() and item['chat_id'] == chat_id_str:
                return item
    else:
        return f"Ошибка: {response.status_code}"

def admin_request_get_all():
    try:
        credentials = {
            'app_password': 'ERZHNPAss12389!',
            'chat_id': '7777777'
        }

        response = requests.get('https://megaparsing.pythonanywhere.com/users/', params=credentials)
        return response.json()
    except Exception as e:
        return f"Ошибка при запросе: {e}"


def admin_request_patch(data, chat_id):
    credentials = {
        'app_password': 'ERZHNPAss12389!',
        'chat_id': '7777777'
    }
    # Получаем список пользователей с сервера
    response = requests.get('https://megaparsing.pythonanywhere.com/users/', params=credentials)
    if response.status_code == 200:
        db_data = response.json()
        user_info = None
        for user in db_data:
            if str(user['chat_id']) == str(chat_id):
                user_info = user
                break
        if user_info:
            # Выполняем PATCH запрос для обновления данных пользователя
            patch_response = requests.patch(f'https://megaparsing.pythonanywhere.com/users/{user_info["id"]}/', json=data, params=credentials)
            if patch_response.status_code == 200:
                print("Значение успешно обновлено через API.")
            else:
                print(f"Произошла ошибка при обновлении значения через API. Код ошибки: {patch_response.status_code}")
        else:
            print("Пользователь не найден.")
    else:
        print(f"Ошибка при получении данных о пользователях. Код ошибки: {response.status_code}")
