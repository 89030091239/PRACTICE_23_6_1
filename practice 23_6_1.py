import telebot  # Импортируем библиотеку telebot, которая позволяет взаимодействовать с Telegram API.
from config import keys,   # Импортируем словарь ключей и токен бота из файла config.py.
from extensions import APIException, \
    CriptoConverter  # Импортируем классы APIException и CriptoConverter из файла extensions.py.

bot = telebot.TeleBot(TOKEN)  # Создаем экземпляр бота с помощью токена, полученного от BotFather


@bot.message_handler(commands=['start',
                               'help'])  # Создаем обработчик сообщений с командами "/start" и "/help", который будет выводить инструкции по использованию бота.
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n <имя валюты> \
    <в какую валюту конвертировать> \
    <количество конвертируемой валюты>\n Увидеть список всех доступных валют /values '
    bot.reply_to(message, text)


@bot.message_handler(
    commands=['values'])  # Создаем обработчик сообщения, который будет выводить список всех доступных валют.
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])  # Обработчик валюты с https://www.cryptocompare.com/cryptopian/api-keys
def get_price(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')  # Получаем от пользователя <имя валюты> \<в какую валюту перевести> \<количество переводимой валюты> и разделяем пробелом, применяем метод lower() к тексту сообщения

        if len(values) != 3:
            raise APIException('Не правильное количество введенных данных! \
            \nВведите через пробел три параметра: <имя валюты> \
    <в какую валюту конвертировать> \
    <количество конвертируемой валюты>')
        quote, base, amount = values
        total_base = CriptoConverter.get_price(quote, base, amount)  # Получаем данные с помощью метода get_price() класса CriptoConverter, передавая ему название валюты, в которую нужно конвертировать, и количество конвертируемой валюты
    except APIException as e:  # Если происходит исключение APIException, выводим соответствующее сообщение пользователю
        bot.reply_to(message, f'Ошибка пользователя! \n{e}')
    except Exception as e:  # Если происходит любое другое исключение, выводим соответствующее сообщение пользователю.
        bot.reply_to(message, f'Не удалось обработать команду! \nПричина: {e}')
    else:  # Если все прошло успешно, формируем ответное сообщение и отправляем его пользователю
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
