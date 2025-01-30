import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Токен бота
TOKEN = "7831383998:AAGAfMis6FrWsaHSY37ojd1oHfbHbKz56ko"

# Создаем объект бота
bot = telebot.TeleBot(TOKEN)

# Вопросы и ответы
questions = [
    ("Какое слово вам ближе?", ["Арт", "Технологии", "Люди", "Анализ"]),
    ("Какое слово вам ближе?", ["Музыка", "Инженерия", "Психология", "Экономика"]),
    ("Какое слово вам ближе?", ["Рисование", "Программирование", "Помощь", "Исследования"]),
    ("Какое слово вам ближе?", ["Фотография", "Математика", "Общение", "Наука"]),
    ("Какое слово вам ближе?", ["Театр", "Роботы", "Дети", "Статистика"]),
]

# Категории
categories = {
    "Творческие профессии": 0,
    "Технические профессии": 0,
    "Гуманитарные профессии": 0,
    "Научные профессии": 0
}

# Словарь для ассоциаций
association_map = {
    "Арт": "Творческие профессии",
    "Технологии": "Технические профессии",
    "Люди": "Гуманитарные профессии",
    "Анализ": "Научные профессии",
    "Музыка": "Творческие профессии",
    "Инженерия": "Технические профессии",
    "Психология": "Гуманитарные профессии",
    "Экономика": "Научные профессии",
    "Рисование": "Творческие профессии",
    "Программирование": "Технические профессии",
    "Помощь": "Гуманитарные профессии",
    "Исследования": "Научные профессии",
    "Фотография": "Творческие профессии",
    "Математика": "Научные профессии",
    "Общение": "Гуманитарные профессии",
    "Наука": "Научные профессии",
    "Театр": "Творческие профессии",
    "Роботы": "Технические профессии",
    "Дети": "Гуманитарные профессии",
    "Статистика": "Научные профессии"
}

# Состояния
user_answers = {}


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создаем разметку с кнопкой
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Пройти тест", callback_data="start_test")
    markup.add(button)

    # Отправляем сообщение с кнопкой
    bot.send_message(message.chat.id, "Привет! Пройди ассоциативный тест и узнай свою профессию!", reply_markup=markup)


# Обработчик нажатия на кнопку
@bot.callback_query_handler(func=lambda call: call.data == "start_test")
def start_test(call):
    user_answers[call.message.chat.id] = []  # Сохраняем пустой список для пользователя
    ask_question(call.message.chat.id, 0)


# Функция для вывода вопроса
def ask_question(chat_id, question_index):
    if question_index < len(questions):
        question, options = questions[question_index]
        markup = InlineKeyboardMarkup()

        # Создаем кнопки для ответа
        for option in options:
            button = InlineKeyboardButton(option, callback_data=f"answer_{option}_{question_index}")
            markup.add(button)

        bot.send_message(chat_id, question, reply_markup=markup)
    else:
        # Подсчет баллов
        calculate_result(chat_id)


# Обработчик ответа
@bot.callback_query_handler(func=lambda call: call.data.startswith("answer_"))
def handle_answer(call):
    _, answer, question_index = call.data.split("_")
    question_index = int(question_index)

    # Сохраняем ответ пользователя
    user_answers[call.message.chat.id].append(answer)

    # Переходим к следующему вопросу
    ask_question(call.message.chat.id, question_index + 1)


# Функция для подсчета результата
def calculate_result(chat_id):
    answers = user_answers[chat_id]

    # Подсчитываем количество баллов для каждой категории
    for answer in answers:
        category = association_map[answer]
        categories[category] += 1

    # Определяем категорию с наибольшим количеством ответов
    result = max(categories, key=categories.get)

    # Отправляем результат пользователю
    bot.send_message(chat_id, f"Ваши результаты: {result}")

    # Добавляем ссылку, если результат - Творческие профессии
    if result == "Творческие профессии":
        bot.send_message(chat_id,
                         "Узнать больше и подобрать будующую профессию: https://go.redav.online/073da3bf6880a210?erid=LdtCKCJ1m&m=1")
    if result == "Технические профессии":
        bot.send_message(chat_id,
                         "Узнать больше и подобрать будующую профессию: https://go.redav.online/073da3bf6880a210?erid=LdtCKCJ1m&m=1")
    if result == "Гуманитарные профессии":
        bot.send_message(chat_id,
                         "Узнать больше и подобрать будующую профессию: https://go.redav.online/073da3bf6880a210?erid=LdtCKCJ1m&m=1")
    if result == "Научные профессии":
        bot.send_message(chat_id,
                         "Узнать больше и подобрать будующую профессию: https://go.redav.online/073da3bf6880a210?erid=LdtCKCJ1m&m=1")

    bot.send_message(chat_id, "Спасибо за участие в тесте!")

    # Сбрасываем данные пользователя
    user_answers[chat_id] = []
    reset_categories()


# Сброс категорий после завершения теста
def reset_categories():
    global categories
    categories = {
        "Творческие профессии": 0,
        "Технические профессии": 0,
        "Гуманитарные профессии": 0,
        "Научные профессии": 0
    }


# Запуск бота
if __name__ == "__main__":
    print("Бот запущен!")
    bot.infinity_polling()
