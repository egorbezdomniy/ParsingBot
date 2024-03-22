import secrets
import string
from datetime import datetime, timedelta

from yookassa import Payment

from ParsingBot.func.api_functions import admin_request_patch, admin_request_get
from ParsingBot.func.catalog_keyboard import create_parsing_keyboard
from ParsingBot.func.main_menu import delete_previous_message, bot, last_message_ids
from ParsingBot.func.payments import create_oplata_keyboard
from ParsingBot.func.payments import payment_func


def check_subscription_status(chat_id):
    user_info = admin_request_get(chat_id)
    print(user_info)
    subscription_info = [user_info['subscription_status'], user_info['end_of_subscription'],
                         user_info['payment_url_1_month'], user_info['payment_url_3_month'],
                         user_info['payment_url_1_year'], user_info['order_id_1_month'], user_info['order_id_3_month'],
                         user_info['order_id_1_year']]

    if subscription_info is not None:
        status, end_of_subscription, payment_url_1_month, payment_url_3_month, payment_url_1_year, order_id_1_month, order_id_3_month, order_id_1_year = subscription_info

        if status and end_of_subscription:
            end_date = datetime.strptime(end_of_subscription.replace('T', ' ').replace('Z', ''), '%Y-%m-%d %H:%M:%S')

            if end_date >= datetime.now():
                # Подписка активна
                delete_previous_message(chat_id)
                password = user_info['app_password']
                with open('photo/catalog.jpg', 'rb') as photo:
                    sent_message = bot.send_photo(chat_id, photo,
                                                  caption="<b><a href='https://drive.google.com/file/d/1JXrp9FRQOZTXdv1C9ZI-MzAlCey1Q2HK/view?usp=sharing'>"
                                                          "Скачать парсер</a></b> \n"

                                                          "<b><a href='https://www.youtube.com/@megamarketbot'>"
                                                          "Туториал по программе</a></b> \n\n"

                                                          f"<b>Логин:</b> {chat_id}\n"
                                                          f"<b>Пароль:</b> {password} ", parse_mode='HTML',
                                                  reply_markup=create_parsing_keyboard())

                last_message_ids[chat_id] = sent_message.message_id

            else:
                # Подписка истекла
                data = {'subscription_status': False}
                admin_request_patch(chat_id=chat_id, data=data)
                bot.send_message(chat_id, "Ваша подписка истекла. Теперь она неактивна.")
                with open('photo/oplata.jpg', 'rb') as photo:
                    sent_message = bot.send_photo(chat_id, photo, reply_markup=create_oplata_keyboard())

                last_message_ids[chat_id] = sent_message.message_id

        else:
            # Подписка неактивна
            delete_previous_message(chat_id)
            # Получаем информацию о промокоде пользователя из базы данных

            promocode_info = user_info['promo_code']
            promocode = promocode_info[0] if promocode_info else 'Отсутствует'

            promocode_discount = 0.9  # dobri skidka pon

            value_1_month = round(999 * promocode_discount) if promocode != 'Отсутствует' else 999
            description_1_month = "Месячная подписка на бота"
            payment_data_1_month, confirmation_url_1_month, payment_id_1_month = payment_func(value_1_month,
                                                                                              description_1_month)

            data = {'order_id_1_month': payment_id_1_month,
                    'payment_url_1_month': confirmation_url_1_month}
            admin_request_patch(chat_id=chat_id, data=data)

            value_3_month = round(1999 * promocode_discount) if promocode != 'Отсутствует' else 1999
            description_3_month = "Трехмесячная подписка на бота"
            payment_data_3_month, confirmation_url_3_month, payment_id_3_month = payment_func(value_3_month,
                                                                                              description_3_month)
            data = {'order_id_3_month': payment_id_3_month,
                    'payment_url_3_month': confirmation_url_3_month}
            admin_request_patch(chat_id=chat_id, data=data)

            value_1_year = round(3999 * promocode_discount) if promocode != 'Отсутствует' else 3999
            description_1_year = "Годовая подписка на бота"
            payment_data_1_year, confirmation_url_1_year, payment_id_1_year = payment_func(value_1_year,
                                                                                           description_1_year)
            data = {'order_id_1_year': payment_id_1_year,
                    'payment_url_1_year': confirmation_url_1_year}
            admin_request_patch(chat_id=chat_id, data=data)

            with open('photo/oplata.jpg', 'rb') as photo:
                sent_message = bot.send_photo(chat_id, photo, reply_markup=create_oplata_keyboard())

            last_message_ids[chat_id] = sent_message.message_id

    else:
        # Информация о подписке отсутствует
        bot.send_message(chat_id, 'Информация о подписке отсутствует.')


# данная фунция вызывается при нажати кнопки "парсинг", проверяет наличие подписки и в зависимости
# от этого отрабатывает различные варианты действий, а так же генерирует ссылки на оплату

# Функция для генерации случайного сложного пароля из 16 символов
def generate_password():
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(12))
    return password


# Функция для обновления пароля в базе данных
def update_password(chat_id, new_password):
    try:
        data = {'app_password': new_password}
        admin_request_patch(data=data, chat_id=chat_id)



    except Exception as e:
        print(f"Error in update_password: {e}")
    finally:
        print('Успешно обновлен пароль')


def check_subscription_payment(chat_id):
    try:
        user_info = admin_request_get(chat_id)
        row = (user_info['order_id_1_month'], user_info['order_id_3_month'], user_info['order_id_1_year'],
               user_info['end_of_subscription'])

        if row:
            # Различные длительности подписки в днях
            durations = [30, 90, 365]

            for i, order_id in enumerate(row[:-1]):  # Итерируемся по всем заказам, кроме end_of_subscription
                if order_id:
                    payment = Payment.find_one(order_id)

                    if payment and payment.status == "succeeded":
                        print(f"Payment for order_id {order_id} is successful.")
                        delete_previous_message(chat_id)
                        # Устанавливаем дату в зависимости от количества итераций
                        subscription_duration = durations[i]
                        end_of_subscription = datetime.now() + timedelta(days=subscription_duration)
                        print(end_of_subscription)

                        # Получаем информацию о промо-коде из базы данных
                        promo_code_row = [user_info['promo_code']]
                        promo_code = promo_code_row[0] if promo_code_row else "Отсутствует"

                        # Определяем стоимость подписки в соответствии с промо-кодом и итерацией
                        if promo_code == "Отсутствует":
                            prices = [999, 1999, 3999]
                        else:
                            prices = [899, 1799, 3599]

                        price = prices[i]

                        # Генерируем новый пароль
                        new_password = generate_password()

                        # Обновляем пароль в базе данных
                        update_password(chat_id, new_password)

                        # Обновляем статус и дату подписки
                        ########################################
                        data = {'subscription_status': True,
                                'end_of_subscription': end_of_subscription.strftime('%Y-%m-%d %H:%M:%S')}
                        admin_request_patch(chat_id=chat_id, data=data)

                        bot.send_message(chat_id,
                                         f"Оплата прошла успешно. Подписка активирована до {end_of_subscription.strftime('%Y-%m-%d')}.")
                        break
                    else:
                        print(f"Payment for order_id {order_id} has failed.")
                else:
                    bot.send_message(chat_id, "Нет активных заказов для проверки.")

    except Exception as e:
        print(f"Error in check_subscription_payment: {e}")
        bot.send_message(chat_id, "Произошла ошибка при проверке оплаты.")
