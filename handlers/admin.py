import os
import signal
from datetime import datetime, timedelta

import requests
from telebot import types

from ParsingBot.func.api_functions import admin_request_get_all, admin_request_get
from ParsingBot.func.main_menu import bot
from ParsingBot.func.subsription import update_password, generate_password

trial_access_dict = {}

admin_ids = {767785629, 1498579619, 6718209568}


def is_admin(chat_id):
    return chat_id in admin_ids


def process_broadcast_text(text):
    user_ids = get_all_user_ids()
    for user_id in user_ids:
        try:
            # Отправляем сообщение с HTML разметкой
            bot.send_message(user_id, text, parse_mode='HTML')
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_id}: {str(e)}")


# Обработка выбора администратором
@bot.message_handler(func=lambda message: message.text == "Управление ботом")
def manage_bot(
        message):
    if is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "<b>Управление ботом:</b>\n"
                                          "<code>/broadcast</code> [text] - сообщение всем пользователям бота\n"
                                          "<code>/stopbot</code> - остановка бота\n"
                                          "<code>/print</code> [text] - вывод текста в консоль\n"
                                          "<code>/givesub</code> [id] [days] - выдача подписки\n"
                                          "<code>/sendmessage</code> [user_id] [message] - отправка сообщения"
                                          "конкретному пользователю\n"
                                          "<code>/sendtoactive</code> [message] - отправка пользователям с подпиской\n"
                                          "<code>/sendtoinactive</code> [message] - отправка пользователям без подписки",
                         parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, "Извините, у вас нет доступа к этой команде.", parse_mode='HTML')


# Обработка выбора администратором
@bot.message_handler(func=lambda message: message.text == "Просмотр статистики")
def manage_bot_stats(message):
    if is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "<b>Просмотр статистики:</b>\n"
                                          "<code>/infopromo</code> - статистика по промокодам\n"
                                          "<code>/statistics</code> - статистика по пользователям\n"
                                          "<code>/user_info</code> [user_id] - информация о конретном пользователе",
                         parse_mode='HTML')
    else:
        bot.send_message(message.chat.id, "Извините, у вас нет доступа к этой команде.", parse_mode='HTML')


# Обработка команды /admin
@bot.message_handler(commands=['admin'])
def admin_menu(message):
    if is_admin(message.from_user.id):
        markup = types.ReplyKeyboardMarkup(row_width=2)

        button1 = types.KeyboardButton("Управление ботом")
        button2 = types.KeyboardButton("Просмотр статистики")

        markup.add(button1, button2)

        bot.send_message(message.chat.id, "Меню администратора:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Извините, я вас не понял. Используйте команду /start")


@bot.message_handler(commands=['broadcast'])
def handle_broadcast_command(message):
    if is_admin(message.from_user.id):
        try:
            # Проверяем наличие параметра после команды /broadcast
            if len(message.text.split()) > 1:
                text = ' '.join(message.text.split()[1:])
                process_broadcast_text(text)
            else:
                bot.send_message(message.chat.id, f"Ошибка при обработке команды.\n"
                                                  f"после команды сразу вписывайте текст\n"
                                                  f"форматирование делать как в HTML")
        except Exception as e:
            print(f"Ошибка при обработке команды /broadcast: {str(e)}")
    else:
        bot.send_message(message.chat.id, "Извините, я вас не понял. Используйте команду /start")


def send_broadcast(text):
    user_ids = get_all_user_ids()
    for user_id in user_ids:
        try:
            bot.send_message(user_id, text)
        except Exception as e:
            print(f"Не удалось отправить сообщение пользователю {user_id}: {str(e)}")


def get_all_user_ids():
    try:
        user_ids = [user['chat_id'] for user in admin_request_get_all()]
        return user_ids
    except Exception as e:
        print(f"Ошибка при получении chat_id: {str(e)}")
        return []


@bot.message_handler(commands=['stopbot'])
def handle_stop_bot_command(message):
    if is_admin(message.from_user.id):
        bot.send_message(message.chat.id, "Остановка бота...")
        os.kill(os.getpid(), signal.SIGINT)
    else:
        bot.send_message(message.chat.id, "Извините, я вас не понял. Используйте команду /start")


@bot.message_handler(commands=['print'])
def handle_print_command(message):
    if is_admin(message.from_user.id):
        try:
            text_to_print = ' '.join(message.text.split()[1:])
            print(text_to_print)

            bot.send_message(message.chat.id, "Текст выведен в консоль.")
        except IndexError:
            bot.send_message(message.chat.id, "Укажите текст после команды /print.")
    else:
        bot.send_message(message.chat.id, "Извините, я вас не понял. Используйте команду /start")


@bot.message_handler(commands=['infopromo'])
def handle_infopromo_command(message):
    if is_admin(message.from_user.id):
        try:
            promo_stats = {}

            # Получаем список промокодов из API Django
            response = admin_request_get_all()
            for user in response:
                promo_code = user.get('promo_code')
                if promo_code != "Отсутствует":  # Исключаем промокод "Отсутствует"
                    if promo_code not in promo_stats:
                        promo_stats[promo_code] = {"Введено": 0, "Активных": 0}

                    # Получаем количество активных пользователей с промокодом из API Django
                    if user.get('subscription_status') == True:
                        promo_stats[promo_code]["Активных"] += 1

                    promo_stats[promo_code]["Введено"] += 1

            response_text = "<b>Статистика по промокодам:</b>\n\n"
            for promo_code, stats in promo_stats.items():
                response_text += f"<b>{promo_code}:</b>\n"
                response_text += f"├ Введено: {stats['Введено']} человек\n"
                response_text += f"└ Активных: {stats['Активных']} человек\n\n"

            bot.send_message(message.chat.id, response_text, parse_mode='HTML')
        except Exception as e:
            print(f"Ошибка при обработке команды /infopromo: {str(e)}")
    else:
        bot.send_message(message.chat.id, "Извините, я вас не понял. Используйте команду /start")



@bot.message_handler(commands=['givesub'])
def handle_grant_subscription_command(message):
    if is_admin(message.from_user.id):
        try:
            # Разбираем текст команды для получения user_id и длительности подписки
            command_parts = message.text.split()
            if len(command_parts) != 3:
                bot.send_message(message.chat.id, "Используйте команду следующим образом: /givesub [user_id] [days]")
                return

            user_id = int(command_parts[1])
            days = int(command_parts[2])

            if grant_subscription(user_id, days):
                bot.send_message(message.chat.id, f"Пользователю {user_id} предоставлена подписка на {days} дней.")
                user_password = generate_password()
                update_password(user_id, generate_password())
            else:
                bot.send_message(message.chat.id, f"Ошибка при предоставлении подписки для пользователя {user_id}.")

        except ValueError:
            bot.send_message(message.chat.id, "Некорректные параметры команды. Укажите user_id и количество дней.")
    else:
        bot.send_message(message.chat.id, "Извините, я вас не понял. Используйте команду /start")


def grant_subscription(user_id, days):
    credentials = {
        'app_password': 'ERZHNPAss12389!',
        'chat_id': '7777777'
    }
    try:
        user_info = admin_request_get(user_id)

        # Получаем текущую дату и время
        current_time = datetime.now()

        # Рассчитываем дату окончания подписки (добавляем указанное количество дней)
        end_time = current_time + timedelta(days=days)
        end_of_subscription = end_time.strftime('%Y-%m-%d %H:%M:%S')

        data = {'end_of_subscription': end_of_subscription, 'subscription_status': True}
        response = requests.patch(f'https://megaparsing.pythonanywhere.com/users/{user_info["id"]}/', json=data, params=credentials)

        return True
    except Exception as e:
        print(f"Ошибка при предоставлении подписки: {e}")
        return False
    finally:
        pass

@bot.message_handler(commands=['sendmessage'])
def send_message_to_user_command(message):
    if is_admin(message.from_user.id):
        try:
            # Проверяем, что после команды /sendmessage есть хотя бы два слова
            if len(message.text.split()) >= 3:
                user_id = int(message.text.split()[1])
                message_text = ' '.join(message.text.split()[2:])

                send_message_to_user(user_id, message_text)

                bot.send_message(message.chat.id, f"Сообщение отправлено пользователю {user_id}.")
            else:
                bot.send_message(message.chat.id,
                                 "Используйте команду следующим образом: /sendmessage [user_id] [message]")
        except ValueError:
            bot.send_message(message.chat.id, "Некорректные параметры команды. Укажите user_id и текст сообщения.")
    else:
        bot.send_message(message.chat.id, "Извините, я вас не понял. Используйте команду /start")


def send_message_to_user(user_id, message_text):
    try:
        bot.send_message(user_id, message_text)
    except Exception as e:
        print(f"Ошибка при отправке сообщения пользователю {user_id}: {str(e)}")


@bot.message_handler(commands=['sendtoactive'])
def send_message_to_active_users_command(message):
    if is_admin(message.from_user.id):
        try:
            # Разбираем текст команды для получения текста сообщения
            command_parts = message.text.split()
            if len(command_parts) != 2:
                bot.send_message(message.chat.id, "Используйте команду следующим образом: /sendtoactive [message]")
                return

            message_text = ' '.join(command_parts[1:])

            send_message_to_active_users(message_text)

            bot.send_message(message.chat.id, f"Сообщение отправлено только активным пользователям.")

        except Exception as e:
            print(f"Ошибка при отправке сообщения активным пользователям: {str(e)}")
    else:
        bot.send_message(message.chat.id, "Извините, я вас не понял. Используйте команду /start")


def send_message_to_active_users(message_text):
    active_users = []
    try:
        response = admin_request_get_all()
        for user in response:
            if user['subscription_status']:
                active_users.append(user['chat_id'])  # Добавляем chat_id напрямую, без вложенного списка
        for chat_id in active_users:
            bot.send_message(chat_id, message_text)  # Отправляем сообщение каждому активному пользователю
    except Exception as e:
        print(f"Ошибка при отправке сообщения активным пользователям: {str(e)}")



@bot.message_handler(commands=['sendtoinactive'])
def send_message_to_inactive_users_command(message):
    if is_admin(message.from_user.id):
        try:
            # Разбираем текст команды для получения текста сообщения
            command_parts = message.text.split()
            if len(command_parts) != 2:
                bot.send_message(message.chat.id, "Используйте команду следующим образом: /sendtoinactive [message]")
                return

            message_text = ' '.join(command_parts[1:])

            send_message_to_inactive_users(message_text)

            bot.send_message(message.chat.id, f"Сообщение отправлено только неактивным пользователям.")

        except Exception as e:
            print(f"Ошибка при отправке сообщения неактивным пользователям: {str(e)}")
    else:
        bot.send_message(message.chat.id, "Извините, я вас не понял. Используйте команду /start")


def send_message_to_inactive_users(message_text):
    try:
        response = admin_request_get_all()
        for user in response:
            if not user['subscription_status']:
                send_message_to_user(user['chat_id'], message_text)
    except Exception as e:
        print(f"Ошибка при отправке сообщения неактивным пользователям: {str(e)}")




@bot.message_handler(commands=['statistics'])
def handle_statistics_command(message):
    if is_admin(message.from_user.id):
        try:

            response = admin_request_get_all()

            total_users = len(response)
            active_subscribers = len([user for user in response if user['subscription_status']])
            promo_code_users = len([user for user in response if user['promo_code'] != 'Отсутствует'])
            promo_code_subscribers = len([user for user in response if user['promo_code'] != 'Отсутствует' and user['subscription_status']])
            no_promo_code_subscribers = len([user for user in response if user['promo_code'] == 'Отсутствует' and user['subscription_status']])

            response_text = "<b>Статистика по пользователям и подпискам:</b>\n\n"
            response_text += f"• Всего пользователей: {total_users}\n"
            response_text += f"• Активных подписчиков: {active_subscribers}\n"
            response_text += f"• Пользователей с введенными промокодами: {promo_code_users}\n"
            response_text += f"• Подписчиков с промокодами: {promo_code_subscribers}\n"
            response_text += f"• Подписчиков без промокодов: {no_promo_code_subscribers}\n"

            bot.send_message(message.chat.id, response_text, parse_mode='HTML')
        except Exception as e:
            print(f"Ошибка при обработке команды /statistics: {str(e)}")
    else:
        bot.send_message(message.chat.id, "Извините, у вас нет доступа к этой команде.")

