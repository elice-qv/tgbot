import telebot
from telebot import types

# Устанавливаем токен бота
bot = telebot.TeleBot('6371805678:AAFCsmXTzKtwmb6ajM-kdVnujIF2wu1hzAc')

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = create_main_menu()
    bot.send_message(message.chat.id, "Добро пожаловать в магазин обуви и одежды Twelvestore!", reply_markup=user_markup)

# Обработчик кнопок главного меню
@bot.callback_query_handler(func=lambda call: call.data in ["shop", "calculator", "order", "conditions"])
def handle_menu_buttons(call):
    chat_id = call.message.chat.id
    if call.data == "shop":
        bot.send_message(chat_id, "Перейдите на наш сайт: https://twelvestore.ru")
    elif call.data == "calculator":
        send_calculator_menu(chat_id)
    elif call.data == "order":
        send_order_info(chat_id)
    elif call.data == "conditions":
        send_order_conditions(chat_id)

# Создание кнопок главного меню
def create_main_menu():
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton("🛍 Наш интернет-магазин", callback_data="shop"),
        types.InlineKeyboardButton("🧮 Калькулятор", callback_data="calculator"),
        types.InlineKeyboardButton("🛒 Оформить заказ", callback_data="order"),
        types.InlineKeyboardButton("📜 Условия заказа", callback_data="conditions"),
    ]
    markup.add(*buttons)
    return markup

# Отправка главного меню
def send_main_menu(chat_id):
    user_markup = create_main_menu()
    bot.send_message(chat_id, "Выберите действие:", reply_markup=user_markup)


# Обработчик кнопок калькулятора
@bot.callback_query_handler(func=lambda call: call.data in ["shoes", "clothing", "lingerie", "bags", "back_to_main"])
def handle_calculator_buttons(call):
    chat_id = call.message.chat.id
    if call.data == "back_to_main":
        user_markup = create_main_menu()
        bot.send_message(chat_id, "Выберите действие:", reply_markup=user_markup)
    else:
        category = call.data
        bot.send_message(chat_id, f"Введите цену в юанях:")
        bot.register_next_step_handler_by_chat_id(chat_id, handle_price_input, category)

# Обработчик ввода цены
def handle_price_input(message, category):
    chat_id = message.chat.id
    try:
        price_in_yuan = float(message.text)
        if category == "shoes":
            total_price = price_in_yuan * 14 + 0.1 * price_in_yuan + 2000
        elif category == "clothing":
            total_price = price_in_yuan * 14 + 0.1 * price_in_yuan + 1000
        elif category == "lingerie":
            total_price = price_in_yuan * 14 + 0.1 * price_in_yuan + 700
        elif category == "bags":
            total_price = price_in_yuan * 14 + 0.1 * price_in_yuan + 1800
        bot.send_message(chat_id, f"Итоговая цена: {total_price} руб.")
        send_calculator_menu(chat_id)
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите корректную цену.")

# Оформление заказа
def send_order_info(chat_id):
    bot.send_message(chat_id, "Введите ссылку на товар:")
    bot.register_next_step_handler_by_chat_id(chat_id, handle_order_link_input)

def handle_order_link_input(message):
    chat_id = message.chat.id
    order_link = message.text
    bot.send_message(chat_id, "Введите размер:")
    bot.register_next_step_handler_by_chat_id(chat_id, handle_order_size_input, order_link)

def handle_order_size_input(message, order_link):
    chat_id = message.chat.id
    size = message.text
    bot.send_message(chat_id, "Введите номер телефона:")
    bot.register_next_step_handler_by_chat_id(chat_id, handle_phone_number_input, order_link, size)

def handle_phone_number_input(message, order_link, size):
    chat_id = message.chat.id
    phone_number = message.text
    order_message = f"📦 Новый заказ!\nСсылка на товар: {order_link}\nРазмер: {size}\nНомер телефона: {phone_number}\n"
    order_message += f"Имя: {message.from_user.first_name}\nФамилия: {message.from_user.last_name}\nЛогин Телеграм: @{message.from_user.username}"
    bot.send_message(chat_id, "Спасибо за заказ! Мы получили его в обработку. С вами свяжется наш менеджер @fightisbigdeal.")
    send_main_menu(chat_id)
    # Отправляем уведомление администратору
    admin_chat_id = '2012133536'
    bot.send_message(admin_chat_id, order_message)

# Условия заказа
def send_order_conditions(chat_id):
    bot.send_message(chat_id, "Условия заказа с POIZON с помощью twelve store:\n"
                              "• Доставляем в среднем до 3х недель до нашего магазина\n"
                              "• Комиссия фиксированная 2000 рублей за весь заказ, можете заказать до 20 единиц товара, комиссия не меняется\n"
                              "• Формула расчета (цена в юанях * курс юаня +10% (страховка) + 2000(доставка до магазина)\n"
                              "• Мы можем отправить СДЭКом за ваш счет в любую точку, по Крыму можете воспользоваться доставкой курьером до двери, это бесплатно.\n"
                              "Если остались вопросы, пожалуйста не стесняйтесь, напишите нашему менеджеру @fightisbigdeal!\n"
                              "Найти инструкцию, как пользоваться POIZON можно найти на нашем сайте poizon.twelvestore.ru")

# Отправка меню калькулятора
def send_calculator_menu(chat_id):
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton("👟 Обувь", callback_data="shoes"),
        types.InlineKeyboardButton("👕 Одежда", callback_data="clothing"),
        types.InlineKeyboardButton("🩲 Белье и мелкие аксессуары", callback_data="lingerie"),
        types.InlineKeyboardButton("👜 Сумки и крупные аксессуары", callback_data="bags"),
        types.InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_main"),
    ]
    markup.add(*buttons)
    bot.send_message(chat_id, "Выберите категорию товара для расчета:", reply_markup=markup)

# Запускаем бота
bot.polling()
