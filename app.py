from flask import Flask, request, jsonify

import request_processing
from config import USER_DB, PASSWORD_DB, HOST_DB, NAME_DB
from models import db


def create_app():
    app = Flask(__name__)
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{USER_DB}:{PASSWORD_DB}@{HOST_DB}/{NAME_DB}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app


app = create_app()

extra_options = {}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data, is_callback_query = request_processing.get_message_or_callback_query(request.json)
        
        if is_callback_query:
            chat_id, callback_data = data['message']['chat']['id'], data['data']
            message_id = data['message']['message_id']

            if callback_data == 'categories_menu':
                request_processing.show_categories_menu(chat_id, message_id)
            elif callback_data == 'add_category':
                request_processing.add_category(chat_id)
                extra_options[chat_id] = {
                    'last_command': 'add_category'
                }
            elif callback_data == 'delete_category':
                request_processing.delete_category(chat_id)
                extra_options[chat_id] = {
                    'last_command': 'delete_category'
                }
            elif callback_data == 'add_cost':
                request_processing.select_category(chat_id)
                extra_options[chat_id] = {
                    'last_command': 'select_category'
                }
            elif callback_data == 'top_up_balance':
                request_processing.top_up_balance(chat_id)
                extra_options[chat_id] = {
                    'last_command': 'top_up_balance'
                }
            elif callback_data == 'statistics_menu':
                request_processing.show_statistics_menu(chat_id, message_id)
            elif callback_data == 'back_to_menu':
                request_processing.show_main_menu(chat_id, message_id=message_id)
            elif callback_data == 'current_month_statistics':
                request_processing.show_statistics(chat_id)
            elif callback_data == 'some_month_statistics':
                request_processing.select_date(chat_id)
                extra_options[chat_id] = {
                    'last_command': 'select_date'
                }
        else:
            chat_id, message_text = data['chat']['id'], data['text'] 
            user_fname = data['from']['first_name']
            message_id = data['message_id']

            if message_text == '/start':
                # Приветствие пользователя и добавление его в базу данных
                request_processing.start(chat_id, user_fname)
                extra_options[chat_id] = {
                    'last_command': ''
                }
            elif message_text == '/menu':
                # Вывод главного меню
                if chat_id in extra_options:
                    del extra_options[chat_id]

                request_processing.show_main_menu(chat_id)
            elif message_text == '/add_category':
                # Вывод сообщения о добавлении новой категории
                request_processing.add_category(chat_id)
                extra_options[chat_id] = {
                    'last_command': 'add_category'
                }
            elif message_text == '/delete_category':
                # Вывод списка категорий для удаления одной из них
                request_processing.delete_category(chat_id)
                extra_options[chat_id] = {
                    'last_command': 'delete_category'
                }
            elif message_text == '/add_cost':
                # Вывод сообщения о добавлении новой категории
                request_processing.select_category(chat_id)
                extra_options[chat_id] = {
                    'last_command': 'select_category'
                }
            elif message_text == '/top_up_balance':
                # Пополнение баланса
                request_processing.top_up_balance(chat_id)
                extra_options[chat_id] = {
                    'last_command': 'top_up_balance'
                }
            elif message_text == '/statistics':
                # Вывод меню статистики
                if chat_id in extra_options:
                    del extra_options[chat_id]

                request_processing.show_statistics_menu(chat_id)
            elif chat_id in extra_options:
                # Обработка последних действий пользователя
                last_command = extra_options[chat_id]['last_command']

                if last_command == 'add_category':
                    request_processing.save_category(chat_id, message_text)   
                    del extra_options[chat_id]
                elif last_command == 'delete_category':
                    request_processing.update_categories(chat_id, message_text)
                    del extra_options[chat_id]
                elif last_command == 'select_category':
                    request_processing.add_cost(chat_id)
                    extra_options[chat_id] = {
                        'last_command': 'add_cost',
                        'category': message_text
                    }
                elif last_command == 'add_cost':
                    request_processing.save_cost(
                        chat_id, 
                        message_text, 
                        extra_options[chat_id]['category']
                    )
                    del extra_options[chat_id]
                elif last_command == 'top_up_balance':
                    request_processing.save_balance(chat_id, message_text)
                    del extra_options[chat_id]
                elif last_command == 'select_date':
                    request_processing.show_statistics(chat_id, message_text)
                    del extra_options[chat_id]
            else:
                request_processing.help(chat_id)
        return jsonify(data)
    return 'Telegram - @keeper_finance_bot'


if __name__ == '__main__':
    app.run()