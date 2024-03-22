import requests

from ParsingBot.func.api_functions import admin_request_get_all
from ParsingBot.func.main_menu import bot
from ParsingBot.func.main_menu import last_message_ids, main_menu


@bot.message_handler(commands=['start'])
def handle_start(message):
    try:
        sent_message = bot.send_photo(message.chat.id, open('photo/dobro.jpg', 'rb'), reply_markup=main_menu)
        last_message_ids[message.chat.id] = sent_message.message_id
        user_exists = 0
        # Проверка существования записи для данного юзера
        response = admin_request_get_all()

        for user in response:
            try:
                if int(user.get('chat_id')) == message.chat.id:
                    user_exists = 1
            except:
                pass


        if not user_exists:
            data = {
                'username': message.chat.username if message.chat.username else message.chat.id,
                'chat_id': message.chat.id,
                'subscription_status': False,
                'promo_code': 'Отсутствует',
                'payment_url_1_month': None,
                'payment_url_3_month': None,
                'payment_url_1_year': None,
                'order_id_1_month': None,
                'order_id_3_month': None,
                'order_id_1_year': None,
                'end_of_subscription': None,
                'app_password': None,
            }
            credentials = {
                'app_password': 'ERZHNPAss12389!',
                'chat_id': '7777777'
            }
            response = requests.post('https://megaparsing.pythonanywhere.com/users/', json=data, params=credentials)
            if response.status_code == 201:
                print("Запись о новом пользователе успешно создана через API.")
            else:
                print("Произошла ошибка при создании записи о новом пользователе через API.")

    except Exception as e:
        print(f"Error in handle_start: {e}")
