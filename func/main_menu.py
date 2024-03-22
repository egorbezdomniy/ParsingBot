import os

import telebot
from dotenv import load_dotenv
from telebot import types

from ParsingBot.func.api_functions import admin_request_get
from ParsingBot.text_about_us import about_us_text

load_dotenv()
bot = telebot.TeleBot(os.getenv('token'))
last_message_ids = {}

# Клавиатура "Главное меню"
main_menu = types.InlineKeyboardMarkup(row_width=2)
main_menu.add(types.InlineKeyboardButton('Профиль', callback_data='profile'),
              types.InlineKeyboardButton('О нас', callback_data='about_us'),
              types.InlineKeyboardButton('Парсинг', callback_data='parsing'),
              types.InlineKeyboardButton('Помощь', callback_data='help'))
# Клавиатура "Назад"
back_button = types.InlineKeyboardMarkup(row_width=1)
back_button.add(types.InlineKeyboardButton('Назад', callback_data='back'))


def delete_previous_message(chat_id):
    if chat_id in last_message_ids and last_message_ids[chat_id] is not None:
        message_id_to_delete = last_message_ids[chat_id]
        try:
            bot.delete_message(chat_id, message_id_to_delete)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Ошибка удаления сообщения: {e}")


def send_profile_info(chat_id):
    # подключаемся и находим данные о пользователе через chat_id
    user_info = admin_request_get(chat_id)
    if user_info:
        username, subscription_status, promo_code, end_of_subscription = user_info['username'], \
            user_info['subscription_status'], user_info['promo_code'], user_info['end_of_subscription'],

        end_of_subscription_date = ''
        if subscription_status and end_of_subscription:
            date, time = end_of_subscription.split('T')
            year, month, day = date.split('-')
            end_of_subscription_date = f'{day}.{month}.{year}'
        if end_of_subscription_date:
            subscription_info = f"└ <b>Подписка:</b> Активна до <u>{end_of_subscription_date}</u>"
        else:
            subscription_info = f"└ <b>Подписка:</b> Отсутствует"

        profile_text = (
            f"<b>Ваша информация:</b>\n"
            f"├ <b>ID:</b> {chat_id}\n"
            f"├ <b>Username:</b> {username}\n"
            f"├ <b>Промокод:</b> {promo_code}\n"
            f"{subscription_info}"
        )

        profile_keyboard = types.InlineKeyboardMarkup(row_width=2)
        profile_keyboard.add(
            types.InlineKeyboardButton('Ввести промокод', callback_data='enter_promo'),
            types.InlineKeyboardButton('Назад', callback_data='back')
        )

        with open('photo/profile.jpg', 'rb') as photo:
            sent_message = bot.send_photo(chat_id, photo, caption=profile_text, reply_markup=profile_keyboard,
                                          parse_mode='HTML')

        if chat_id in last_message_ids:
            bot.delete_message(chat_id, last_message_ids[chat_id])

        last_message_ids[chat_id] = sent_message.message_id

    else:
        bot.send_message(chat_id, 'Информация о пользователе отсутствует.')


# "О нас"
def send_about_us_info(chat_id):
    with open('photo/about_us.jpg', 'rb') as photo:
        sent_message = bot.send_photo(chat_id, photo, caption=about_us_text, reply_markup=back_button,
                                      parse_mode='HTML')

    if chat_id in last_message_ids:
        bot.delete_message(chat_id, last_message_ids[chat_id])

    last_message_ids[chat_id] = sent_message.message_id


# "Помощь"
def send_help_info(chat_id):
    help_text = "<b>Краткая инструкция:</b> \n\n" \
                "1) Нажать парсинг \n" \
                "2) Оплатить тариф\n" \
                "3) Скачать и запустить программу\n" \
                "4) Произвести вход по данным с бота\n" \
                "5) Авторизоваться в настройках в МегаМаркете\n" \
                "6) Начать парсинг в главном меню \n\n" \
                "<b><a href='https://www.youtube.com/watch?v=E6wBDR0DBaE&t=7s'>Мануал по заработку</a></b>\n\n" \
                "<b>Техническая поддержка: <u>@drocheslaves</u></b>\n" \
                "По всем вопросам писать сюда"
    with open('photo/help.jpg', 'rb') as photo:
        sent_message = bot.send_photo(chat_id, photo, caption=help_text, reply_markup=back_button, parse_mode='HTML')

    if chat_id in last_message_ids:
        bot.delete_message(chat_id, last_message_ids[chat_id])

    last_message_ids[chat_id] = sent_message.message_id


def back_to_main_menu(chat_id):
    try:
        sent_message = bot.send_photo(chat_id, open('photo/dobro.jpg', 'rb'), reply_markup=main_menu)

        if chat_id in last_message_ids and last_message_ids[chat_id] is not None:
            bot.delete_message(chat_id, last_message_ids[chat_id])

        last_message_ids[chat_id] = sent_message.message_id

    except telebot.apihelper.ApiTelegramException as e:
        print(f"Error in back_to_main_menu: {e}")
