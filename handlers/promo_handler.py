from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from ParsingBot.func.main_menu import bot
from ParsingBot.func.promo_data import promo_list
from ParsingBot.func.promofunc import update_promo_code


@bot.message_handler(func=lambda message: message.text.startswith('/promo'))
def handle_promo_input(message):
    promo_code = message.text.replace('/promo', '').strip()

    if promo_code in promo_list:
        update_promo_code(message.chat.id, promo_code)
        success_message = f'Промокод "{promo_code}" успешно сохранен!\n' \
                          f'Теперь подписка стоит для Вас на 10% дешевле!'

        keyboard = InlineKeyboardMarkup()
        start_button = InlineKeyboardButton("Продолжить далее", callback_data='start_command')
        keyboard.row(start_button)

        bot.send_message(message.chat.id, success_message, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Неверный промокод. Попробуйте еще раз.')