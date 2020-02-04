import decimal
import json
from datetime import datetime

import pytz

from models import db, User, Category, Cost
from telegram_bot import bot
import interface


def get_message_or_callback_query(request_data):
    try:
        return (request_data['message'], False)
    except KeyError:
        return (request_data['callback_query'], True)


def is_number(text):
    try:
        number = float(text)
    except ValueError:
        return False
    else:
        return True



def start(chat_id, user_fname):
    if not User.query.filter_by(id=chat_id).all():
        new_user = User(id=chat_id)
        default_categories = [
            Category(name=category_name, user=new_user) for category_name in interface.DEFAULT_CATEGORIES
        ]

        db.session.add(new_user)
        db.session.add_all(default_categories)
        db.session.commit()

    bot.send_message({
        'chat_id': chat_id,
        'text': f'\U0001F305 Добрый день, {user_fname}! {interface.START}'
    })
    show_main_menu(chat_id)


def help(chat_id):
    bot.send_message({
        'chat_id': chat_id,
        'text': interface.HELP
    })


def show_main_menu(chat_id, responce_text='', message_id=None):
    user = User.query.filter_by(id=chat_id).first()
    responce_text += f'\n\n{interface.CURRENT_BALANCE} {user.balance} {interface.RUBLE}'

    responce_data = {
        'chat_id': chat_id,
        'text': responce_text,
        'reply_markup': interface.MENU
    }

    if not message_id:
        bot.send_message(responce_data)
    else:
        responce_data['message_id'] = message_id
        bot.edit_message_text(responce_data)


def show_categories_menu(chat_id, message_id=None):
    user = User.query.filter_by(id=chat_id).first()
    responce_data = {
        'chat_id': chat_id,
        'text': f'{interface.CURRENT_BALANCE} {user.balance} {interface.RUBLE}',
        'reply_markup': interface.CATEGORIES_MENU
    }

    if not message_id:
        bot.send_message(responce_data)
    else:
        responce_data['message_id'] = message_id
        bot.edit_message_text(responce_data)


def add_category(chat_id):
    bot.send_message({
        'chat_id': chat_id,
        'text': interface.ADD_CATEGORY
    })


def delete_category(chat_id):
    user_categories = json.dumps({
        'keyboard': [
            [{'text': category.name}] for category in Category.query.filter_by(user_id=chat_id).all()
        ],
        'resize_keyboard': True,
        'one_time_keyboard': True
    })
    
    bot.send_message({
        'chat_id': chat_id,
        'text': interface.SELECT_DELETE_CATEGORY,
        'reply_markup': user_categories
    })



def update_categories(chat_id, category_name):
    category_name = ' '.join(category_name.split())
    categories = Category.query.filter_by(name=category_name, user_id=chat_id).all()
    
    if categories:
        category = categories.pop()

        for cost in Cost.query.filter_by(user_id=chat_id, category=category).all():
            db.session.delete(cost)

        db.session.delete(category)
        db.session.commit()

        show_main_menu(chat_id, interface.SUCCESS_DELETE_CATEGORY)
    else:
        show_main_menu(chat_id, interface.ERROR_DELETE_CATEGORY)


def save_category(chat_id, category_name):
    category_name = ' '.join(category_name.split())
    user = User.query.filter_by(id=chat_id).first()
    
    if not Category.query.filter_by(name=category_name, user=user).all():
        new_category = Category(name=category_name, user=user)
        db.session.add(new_category)
        db.session.commit()

        responce_text = interface.SUCCESS_ADD_CATEGORY

        show_main_menu(chat_id, responce_text)
    else:
        show_main_menu(chat_id, interface.ERROR_ADD_CATEGORY)


def select_category(chat_id):
    user_categories = json.dumps({
        'keyboard': [
            [{'text': category.name}] for category in Category.query.filter_by(user_id=chat_id).all()
        ],
        'resize_keyboard': True,
        'one_time_keyboard': True
    })

    bot.send_message({
        'chat_id': chat_id,
        'text': interface.SELECT_COST_CATEGORY,
        'reply_markup': user_categories
    })


def add_cost(chat_id):
    bot.send_message({
        'chat_id': chat_id,
        'text': interface.INPUT_PRICE_COST
    })


def save_cost(chat_id, cost_price, category_name):
    if is_number(cost_price):
        cost_price = float(cost_price)

        categories = Category.query.filter_by(name=category_name, user_id=chat_id).all()
        if categories:
            user = User.query.filter_by(id=chat_id).first()
            user.balance -= decimal.Decimal(cost_price)

            new_cost = Cost(
                user=user, 
                category=categories[0], 
                price=cost_price, 
                debit_date=datetime.now(tz=pytz.timezone('Asia/Yekaterinburg'))
            )   
            db.session.add(new_cost)
            db.session.commit()

            responce_text = interface.SUCCESS_ADD_СOST
            # responce_text += f'\n\nТекущий баланс: {user.balance} {interface.RUBLE}'

            show_main_menu(chat_id, responce_text)
        else:
            show_main_menu(chat_id, interface.ERROR_SELECT_CATEGORY)
    else:
        show_main_menu(chat_id, interface.IS_NOT_NUMBER)


def top_up_balance(chat_id):
    bot.send_message({
        'chat_id': chat_id,
        'text': interface.TOP_UP_BALANCE
    })


def save_balance(chat_id, amount):
    if is_number(amount):
        amount = float(amount)

        user = User.query.filter_by(id=chat_id).first()
        user.balance += decimal.Decimal(amount)

        db.session.commit()

        responce_text = interface.SUCCESS_TOP_UP_BALANCE

        show_main_menu(chat_id, responce_text)
    else:
        show_main_menu(chat_id, interface.IS_NOT_NUMBER)


def show_statistics_menu(chat_id, message_id=None):
    user = User.query.filter_by(id=chat_id).first()
    responce_data = {
        'chat_id': chat_id,
        'text': f'{interface.CURRENT_BALANCE} {user.balance} {interface.RUBLE}',
        'reply_markup': interface.STATISTICS_MENU
    }

    if not message_id:
        bot.send_message(responce_data)
    else:
        responce_data['message_id'] = message_id
        bot.edit_message_text(responce_data)


def show_statistics(chat_id, date=None):
    user = User.query.filter_by(id=chat_id).first()

    if not date:
        responce_text = '📈 Статистика за текущий месяц:\n\n'
        responce_text += f'{interface.CURRENT_BALANCE} {user.balance} {interface.RUBLE}\n'
        date = datetime.now(tz=pytz.timezone('Asia/Yekaterinburg')).date()
    else:
        error_responce_data = {
            'chat_id': chat_id,
            'text': interface.ERROR_STATISTICS_DATE
        }

        # date = '12/2019'.split()
        date = date.split('/')
        if len(date) != 2:
            bot.send_message(error_responce_data)
            return

        try:
            date = datetime(day=1, month=int(date[0]), year=int(date[1]))
        except (ValueError, TypeError):
            bot.send_message(error_responce_data)
            return

        responce_text = f'📈 Статистика за {date.month} месяц {date.year} года:\n\n'

    user_categories = Category.query.filter_by(user=user).all()

    categories_costs_price = {category.name: decimal.Decimal('0.00') for category in user_categories}
    total_costs_price = 0

    for cost in Cost.query.filter_by(user=user).all():
        is_same_month = cost.debit_date.year == date.year
        is_same_month *= cost.debit_date.month == date.month
        if is_same_month:
            price = cost.price
            categories_costs_price[cost.category.name] += price
            total_costs_price += price

    responce_text += f'💸 Сумма расходов: {total_costs_price} {interface.RUBLE}\n\n'
    for category, price in categories_costs_price.items():
        responce_text += f'{category} - {price} {interface.RUBLE}\n'

    bot.send_message({
        'chat_id': chat_id,
        'text': responce_text
    })

                    
def select_date(chat_id):
    total_dates = []
    for cost in Cost.query.filter_by(user_id=chat_id).all():
        date = f'{cost.debit_date.month}/{cost.debit_date.year}'
        if date not in total_dates:
            total_dates.append(date)

    bot.send_message({
        'chat_id': chat_id,
        'text': interface.SELECT_DATE,
        'reply_markup': json.dumps({
            'keyboard': [
                [{'text': date}] for date in total_dates
            ],
            'resize_keyboard': True,
            'one_time_keyboard': True
        })
    })
