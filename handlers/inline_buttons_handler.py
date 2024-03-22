from ParsingBot.func.catalog_keyboard import create_parsing_keyboard
from ParsingBot.func.main_menu import bot, send_profile_info, send_about_us_info, send_help_info, back_to_main_menu, \
    last_message_ids
from ParsingBot.func.payments import send_price_options
from ParsingBot.func.promofunc import ask_for_promo
from ParsingBot.func.subsription import check_subscription_status, check_subscription_payment
from ParsingBot.handlers.parse_handlers import fast_parse_handler
from ParsingBot.handlers.start_handler import handle_start


@bot.callback_query_handler(func=lambda call: True)
def handle_buttons_func(call):
    if call.data == 'profile':
        send_profile_info(call.message.chat.id)
    elif call.data == 'about_us':
        send_about_us_info(call.message.chat.id)
    elif call.data == 'parsing':
        check_subscription_status(call.message.chat.id)
    elif call.data == 'help':
        send_help_info(call.message.chat.id)
    elif call.data == 'fast_parse':
        fast_parse_handler(call)
    elif call.data == 'start_command':
        handle_start(call.message)
    elif call.data == 'back':
        back_to_main_menu(call.message.chat.id)
    elif call.data == 'back_payment':
        back_to_main_menu(call.message.chat.id)
    elif call.data == 'check_payment':
        check_subscription_payment(call.message.chat.id)
    elif call.data == 'method1':
        send_price_options(call.message.chat.id)
    elif call.data == 'enter_promo':
        ask_for_promo(call.message.chat.id)
    elif call.data == 'back2':
            bot.delete_message(call.message.chat.id, call.message.message_id)
            with open('photo/catalog.jpg', 'rb') as photo:
                sent_message = bot.send_photo(call.message.chat.id, photo, reply_markup=create_parsing_keyboard())
            last_message_ids[call.message.chat.id] = sent_message.message_id
    elif call.data == 'back_current':
        chat_id = call.message.chat.id
        bot.delete_message(chat_id, call.message.message_id)


