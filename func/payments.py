from ParsingBot.bot_config import PHOTO_DIR

import os
import json

from telebot import types
from yookassa import Configuration, Payment

from ParsingBot.func.api_functions import admin_request_get
from ParsingBot.func.main_menu import bot, last_message_ids, delete_previous_message



def payment_func(value, description):
    Configuration.account_id = os.environ["YOOKASSA_SHOP_ID"]
    Configuration.secret_key = os.environ["YOOKASSA_SECRET_KEY"]
    payment = Payment.create({
        "amount": {
            "value": value,
            "currency": "RUB"
        },
        "payment_method_data": {
            "type": "bank_card"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": os.environ["YOOKASSA_RETURN_URL"]
        },
        "capture": True,
        "description": description
    })
    confirmation_url = payment.confirmation.confirmation_url
    payment_data = json.loads(payment.json())
    payment_id = payment_data['id']
    return json.loads(payment.json()), confirmation_url, payment_id
# Показывает варианты оплаты подписки.
def send_price_options(chat_id):
    try:
        user_info = admin_request_get(chat_id)

        payment_url_1_month, payment_url_3_month, payment_url_1_year = user_info['payment_url_1_month'], user_info['payment_url_3_month'], user_info['payment_url_1_year']

        price_options_keyboard = types.InlineKeyboardMarkup(row_width=2)

        price_options_keyboard.add(
            types.InlineKeyboardButton('1 месяц', callback_data='1_month', resize_keyboard=True,
                                       url=payment_url_1_month),
            types.InlineKeyboardButton('3 месяца', callback_data='3_month', resize_keyboard=True,
                                       url=payment_url_3_month),
            types.InlineKeyboardButton('1 год', callback_data='1_year', resize_keyboard=False, url=payment_url_1_year),
        types.InlineKeyboardButton("Проверить оплату", callback_data='check_payment', resize_keyboard=True)
        )
        price_options_keyboard.row(
            types.InlineKeyboardButton('<- Назад', callback_data='back_payment', resize_keyboard=True)
        )

        delete_previous_message(chat_id)

        with open(PHOTO_DIR / "price.jpg", 'rb') as photo:
            sent_message = bot.send_photo(chat_id, photo, reply_markup=price_options_keyboard)

        last_message_ids[chat_id] = sent_message.message_id

    except Exception as e:
        print(f"Error in send_price_options: {type(e).__name__}")

# отправляет меню с прайсом
def create_oplata_keyboard():
    oplata_keyboard = types.InlineKeyboardMarkup(row_width=1)

    oplata_keyboard.add(types.InlineKeyboardButton('Купить подписку', callback_data='method1'),
                        types.InlineKeyboardButton('Назад', callback_data='back'))

    return oplata_keyboard

