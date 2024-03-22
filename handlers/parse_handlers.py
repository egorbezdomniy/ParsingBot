import io

import pandas as pd
import requests
from selenium import webdriver
from telebot import types

from ParsingBot.func.main_menu import bot
from ParsingBot.parse_functions.functions import more, parse
from ParsingBot.parse_functions.setup import headless_options


def create_fast_parse_keyboard():
    parsing_keyboard = types.InlineKeyboardMarkup(row_width=1)
    # Добавляем кнопки всегда
    parsing_keyboard.row(types.InlineKeyboardButton('<- Назад', callback_data='back'))

    return parsing_keyboard


def fast_parse_handler(call):
    with open('photo/parsing_your_link.jpg', 'rb') as photo:
        sent_message = bot.send_photo(call.message.chat.id, photo, caption="<b>Введите команду</b>:\n\n"
                                                                           "/parse {Ссылка} {минимальный процент кешбека} {Количество страниц каталога для парса\n\n"
                                                                           "Используйте ссылки только из каталога\n\n"
                                                                           "<b>Пример</b>:\n /parse https://megamarket.ru/catalog/igrovye-monitory/ 20 5",
                                      reply_markup=create_fast_parse_keyboard(), parse_mode='HTML')

def get_subscription_status(chat_id, message):
    try:
        credentials = {
            'app_password': 'ERZHNPAss12389!',
            'chat_id': '7777777'
        }

        response = requests.get('https://megaparsing.pythonanywhere.com/users/', params=credentials)
        if response.status_code == 200:
            data = response.json()
            for user in data:
                try:
                    if int(user.get('chat_id')) == chat_id:
                        return user['subscription_status']
                except:
                    pass
        else:
            bot.send_message(message.chat.id, "Ошибка При проверки статуса вашей подписки")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка При проверки статуса вашей подписки {e}")
@bot.message_handler(commands=['parse'])
def catalog_handler_func(message):
    user_id = message.chat.id
    subscription_status = get_subscription_status(user_id, message)

    if not subscription_status:
        bot.send_message(message.chat.id, "Вам необходимо приобрести подписку для использования этой функции. "
                                          "Используйте команду /start и перейдите в раздел 'Парсинг' для покупки.")
        return

    command_args = message.text.split()

    if len(command_args) < 3:
        bot.send_message(message.chat.id, "Ошибка: неправильно переданы аргументы")
        return

    url = command_args[1]
    bonus_percent = command_args[2] if len(command_args) > 2 else 0
    try:
        parse_pages = int(command_args[3] if len(command_args) > 3 else 5)
    except ValueError:
        bot.send_message(message.chat.id, 'Количество страниц должно быть числом')
        return

    try:
        int(bonus_percent)
    except ValueError:
        bot.send_message(message.chat.id, 'Процент кешбека должен быть числом')
        return

    if int(bonus_percent) > 110 or int(bonus_percent) < 0:
        bot.send_message(message.chat.id, "Ошибка: Такого кешбека не может быть")
        return

    bonus_percent = int(bonus_percent)

    if url.startswith('https://megamarket.ru/catalog/'):
        print(f'{message.from_user.username} Парсит {url} {parse_pages} страниц')
        try:
            bot.send_message(message.chat.id,
                             '(1/3) Подключаеся к сайту мегамаркет, это может занять до минуты, подождите...)')
            driver = webdriver.Chrome(options=headless_options())

            driver.set_window_size(1920, 1080)

            driver.get(url)

            bot.send_message(message.chat.id, '(2/3) Собираем и сортируем данные, подождите...')
            more(driver, pages=parse_pages)

            bot.send_message(message.chat.id, '(3/3) Создаем Эксель файл, подождите...')
            offers = parse(driver, needed_percent=int(bonus_percent))
            xl_file = create_excel_in_memory(sorted(offers, key=lambda x: x['bonus_percent']))
            # Предполагается, что `xl_file` является объектом BytesIO, возвращенным функцией create_excel_in_memory
            xl_file.seek(0)  # Перемещаем указатель в начало файла

            # Создаем объект InputFile для отправки через бота
            file_to_send = io.BytesIO(xl_file.read())
            file_to_send.name = 'Результаты Парса.xlsx'  # Имя файла, которое увидит пользователь

            # Отправляем файл
            bot.send_document(chat_id=message.chat.id, document=file_to_send)

            # После отправки файла можно очистить объект BytesIO, если это необходимо
            xl_file.close()
            back_button = types.InlineKeyboardButton('<- Назад', callback_data='back2')
            back_keyboard = types.InlineKeyboardMarkup().add(back_button)
            sent_message = bot.send_message(message.chat.id, 'Нажмите, чтобы вернуться к каталогу.',
                                            reply_markup=back_keyboard)
            print(f'{message.from_user.username} Пропарсил успешно {len(offers)} объявлений')
        except Exception as e:
            print(f"Произошла ошибка при выполнении парсинга: {str(e)}")
        finally:
            if 'driver' in locals():
                driver.quit()
    else:
        bot.send_message(message.chat.id, 'Ошибка, пример правильного использования:\n'
                                          '/parse {ссылка на категорию из каталога} {минимальный процент кешбека}')


def create_excel_in_memory(results):
    # Создаем DataFrame напрямую из списка словарей
    df = pd.DataFrame(results)

    # Создаем объект BytesIO для хранения файла Excel в памяти
    output = io.BytesIO()

    # Используем контекстный менеджер для работы с ExcelWriter
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Результаты', index=False, columns=['name', 'price', 'bonus_percent', 'bonus_amount'])

        workbook = writer.book
        worksheet = writer.sheets['Результаты']

        # Определяем форматы
        header_format = workbook.add_format({
            'bold': True,
            'font_name': 'Arial Black',
            'font_color': 'white',
            'bg_color': '#4F81BD',
            'align': 'center'
        })
        text_format = workbook.add_format({
            'bold': True,
            'font_name': 'Bahnschrift SemiBold',
            'align': 'center'
        })
        hyperlink_format = workbook.add_format({
            'align': 'center',
            'font_color': 'blue',
            'underline': True,
            'font_name': 'Bahnschrift SemiBold'
        })

        # Настраиваем ширину столбцов
        worksheet.set_column('A:A', 120, hyperlink_format)
        worksheet.set_column('B:D', 25, text_format)

        # Добавляем заголовки с использованием header_format
        headers = ['Название товара', 'Цена', 'Процент баллов', 'Количество баллов']
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)

        # Добавляем гиперссылки и данные
        for row_num, row in enumerate(df.itertuples(), start=1):
            worksheet.write_url(row_num, 0, row.url, string=row.name, cell_format=hyperlink_format)
            worksheet.write(row_num, 1, row.price, text_format)
            worksheet.write(row_num, 2, row.bonus_percent, text_format)
            worksheet.write(row_num, 3, row.bonus_amount, text_format)

    # После выхода из контекстного менеджера возвращаем данные файла из памяти
    output.seek(0)  # Перемещаем указатель в начало файла
    return output
