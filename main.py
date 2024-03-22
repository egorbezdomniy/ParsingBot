import logging
import time

from ParsingBot.func.catalog_keyboard import change_password_callback
from ParsingBot.func.main_menu import bot
from ParsingBot.handlers.admin import handle_broadcast_command, handle_print_command, handle_stop_bot_command, \
    admin_menu
from ParsingBot.handlers.inline_buttons_handler import handle_buttons_func
from ParsingBot.handlers.parse_handlers import catalog_handler_func
from ParsingBot.handlers.promo_handler import handle_promo_input
from ParsingBot.handlers.start_handler import handle_start
from ParsingBot.handlers.unkown_command_handler import handle_unknown_command, handle_sticker

bot.add_message_handler(handle_start)
bot.add_callback_query_handler(handle_buttons_func)
bot.add_message_handler(handle_promo_input)
bot.add_message_handler(handle_unknown_command)
bot.add_message_handler(handle_broadcast_command)
bot.add_message_handler(handle_stop_bot_command)
bot.add_message_handler(handle_print_command)
bot.add_message_handler(admin_menu)
bot.add_callback_query_handler(change_password_callback)
bot.add_message_handler(handle_sticker)
bot.add_message_handler(catalog_handler_func)

if __name__ == '__main__':
    while True:
        try:
            print('Bot is alive')
            bot.polling(none_stop=True)
        except Exception as err:
            logging.error(err)
            time.sleep(5)
            print('Bot is dead')

