import telebot
from config import keys, TOKEN
from extensions import APIException, CriptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n <имя валюты> \
    <в какую валюту перевести> \
    <количество переводимой валюты>\n Увидеть список всех доступных валют /values '
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])  # Обработчик валюты с https://www.cryptocompare.com/cryptopian/api-keys
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')  # Получаем от пользователя <имя валюты> \<в какую валюту перевести> \<количество переводимой валюты> и разделяем пробелом

        if len(values) != 3:
            raise APIException('Не правильное количество параметров.')
        quote, base, amount = values
        total_base = CriptoConverter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()