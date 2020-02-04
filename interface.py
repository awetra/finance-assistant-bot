import json


BUTTONS_TEXT = {
    'CATEGORIES_MENU': '📚 Категории',
    'ADD_CATEGORY': '📗 Добавить категорию',
    'DELETE_CATEGORY': '📕 Удалить категорию',
    'ADD_COST': '📝 Добавить расходы',
    'TOP_UP_BALANCE': '💵 Пополнить баланс',
    'STATISTICS_MENU': '📊 Статистика',
    'CURRENT_MONTH_STATISTICS': '📂 Текущий месяц',
    'SOME_MONTH_STATISTICS': '📁 Другой месяц',
    'BACK_TO_MENU': '« Назад в меню'
}


MENU = json.dumps({
    'inline_keyboard': [
        [
            {
                'text': BUTTONS_TEXT['ADD_COST'],
                'callback_data': 'add_cost'
            },
            {
                'text': BUTTONS_TEXT['TOP_UP_BALANCE'],
                'callback_data': 'top_up_balance'
            }
        ],
        [{
            'text': BUTTONS_TEXT['CATEGORIES_MENU'],
            'callback_data': 'categories_menu'
        }],
        [{
            'text': BUTTONS_TEXT['STATISTICS_MENU'],
            'callback_data': 'statistics_menu'
        }],
    ]
})

CATEGORIES_MENU = json.dumps({
    'inline_keyboard': [
        [
            {
                'text': BUTTONS_TEXT['ADD_CATEGORY'],
                'callback_data': 'add_category'
            },
            {
                'text': BUTTONS_TEXT['DELETE_CATEGORY'],
                'callback_data': 'delete_category'
            }
        ],
        [{
            'text': BUTTONS_TEXT['BACK_TO_MENU'],
            'callback_data': 'back_to_menu'
        }]
    ]
})

STATISTICS_MENU = json.dumps({
    'inline_keyboard': [
        [
            {
                'text': BUTTONS_TEXT['CURRENT_MONTH_STATISTICS'],
                'callback_data': 'current_month_statistics'
            },
            {
                'text': BUTTONS_TEXT['SOME_MONTH_STATISTICS'],
                'callback_data': 'some_month_statistics'
            }
        ],
        [{
            'text': BUTTONS_TEXT['BACK_TO_MENU'],
            'callback_data': 'back_to_menu'
        }]
    ]
})


DEFAULT_CATEGORIES = [
    '🍳 Питание',
    '🛋 Дом',
    '🛀 Красота и гигиена',
    '📱 Интернет и сотовая связь',
    '🏠 Жильё',
    '🚌 Транспорт',
    '⚽️ Спорт',
    '🎳 Развлечения',
]


RUBLE = '\U000020BD'
CURRENT_BALANCE = '💰 Текущий баланс:'
IS_NOT_NUMBER = '🔥 Я думаю, что вы совершили опечатку... Может попробуете вновь?'

START = 'Вас приветствует @keeper_finance_bot!\n\n\
💸 С помощью данного бота вы сможете вести учёт финансов по необходимым для вас категориям.'


HELP = '⁉️ Список доступных команд:\n\n🕹 /menu - Главное меню\n📗 /add_category - Добавить новую категорию\n\
📕 /delete_category - Удалить категорию\n📝 /add_cost - Добавить новые расходы\n\
💵 /top_up_balance - Пополнить баланс\n📊 /statistics - Просмотр статистики'

ADD_CATEGORY = '📗 Введите название новой категории:'
SUCCESS_ADD_CATEGORY = '✨ Новая категория успешно добавлена!'
ERROR_ADD_CATEGORY = '🔥 Данная категория уже существует...'
SELECT_DELETE_CATEGORY = '🗂 Выберите одну из предложенных категорий, которую желаете удалить:'
SUCCESS_DELETE_CATEGORY = '✨ Категория успешно удалена!'
ERROR_DELETE_CATEGORY = '🔥 Необходимо выбрать существующую категорию из списка.'

SELECT_COST_CATEGORY = '🗂 Выберите одну из предложенных категорий для новых расходов:'
ERROR_SELECT_CATEGORY = '🔥 Необходимо выбрать существующую категорию из списка...\n\n\
Если вам нужна новая категория, вы можете добавить её - /add_category.'
INPUT_PRICE_COST = '📝 Введите сумму расходов:'
SUCCESS_ADD_СOST = '✨ Новые расходы успешно добавлены!'

TOP_UP_BALANCE = '💵 Введите сумму на пополнение баланса:'
SUCCESS_TOP_UP_BALANCE = '✨ Ваш баланс успешно пополнен!'

ERROR_STATISTICS_DATE = '🔥 Необходимо выбрать месяц из предложенного списка.'
SELECT_DATE = '🗂 Выберите из предложенного списка один месяц для просмотра вашей статистики:\n\n<b>Пример: 1/2020 - месяц/год</b>'