from ParsingBot.func.main_menu import bot


# Обработчик неизвестных команд и сообщений
@bot.message_handler(func=lambda message: True)
def handle_unknown_command(message):
    if message.text:
        bot.send_message(message.chat.id, "Извините, я вас не понял. Используйте команду /start")
    else:
        # Если сообщение не текстовое, можно игнорировать
        pass

# Обработчик для стикеров (для дополнительной гибкости)
@bot.message_handler(content_types=['photo',
                                    'video',
                                    'sticker',
                                    'document',
                                    'audio',
                                    'voice',
                                    'video_note',
                                    'contact',
                                    'location',
                                    'animation',
                                    'poll',
                                    'venue',
                                    'dice',
                                    'new_chat_members',
                                    'left_chat_member',
                                    'new_chat_title',
                                    'new_chat_photo',
                                    'delete_chat_photo',
                                    'group_chat_created',
                                    'supergroup_chat_created',
                                    'channel_chat_created',
                                    'migrate_to_chat_id',
                                    'migrate_from_chat_id',
                                    'pinned_message',
                                    'invoice',
                                    'successful_payment',
                                    'connected_website'])
def handle_sticker(message):
    bot.send_message(message.chat.id, "Извините, я вас не понял. Используйте команду /start")