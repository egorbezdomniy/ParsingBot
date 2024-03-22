from telebot import types

from ParsingBot.func.api_functions import admin_request_get, admin_request_patch
from ParsingBot.func.main_menu import bot


def create_parsing_keyboard():
    parsing_keyboard = types.InlineKeyboardMarkup(row_width=1)
    parsing_keyboard.add(types.InlineKeyboardButton('Назад', callback_data='back'))
    parsing_keyboard.add(types.InlineKeyboardButton('Сменить пароль', callback_data='change_password'))
    parsing_keyboard.add(types.InlineKeyboardButton('Быстрый парсинг', callback_data='fast_parse'))
    return parsing_keyboard


# Обработчик для кнопки "Сменить пароль"
@bot.callback_query_handler(func=lambda call: call.data == 'change_password')
def change_password_callback(query):

    bot.send_message(query.from_user.id, "Введите новый пароль:")
    bot.register_next_step_handler(query.message, process_new_password)


# Обработчик для получения нового пароля
def process_new_password(message):

    new_password = message.text
    chat_id = message.chat.id

    try:
        user_info = admin_request_get(chat_id)
        print(user_info)
        print(new_password)
        try:
            data = {'app_password': new_password}
            admin_request_patch(data=data, chat_id=chat_id)
        except Exception as e:
            print(f"Error in update_password: {e}")
    except Exception as e:
        print(f"Error in update_password: {e}")

    bot.send_message(chat_id, "Пароль успешно изменен.")