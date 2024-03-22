from ParsingBot.func.api_functions import admin_request_patch
from ParsingBot.func.main_menu import bot, last_message_ids


def ask_for_promo(chat_id):
    bot.send_message(chat_id, 'Введите промокод:\n'
                              'Для ввода используйте команду /promo\n'
                              'Пример: /promo megamarket10')
    last_message_ids[chat_id] = last_message_ids.get(chat_id, None)


# обновление промокода в бд
def update_promo_code(chat_id, promo_code):
    data = {
        'promo_code': promo_code
    }
    admin_request_patch(data=data, chat_id=chat_id)