import telebot
from config import keys, TOKEN
from extensions import CurrencyConverter, ConvertionException


bot = telebot.TeleBot(TOKEN)

# bot.delete_webhook()


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):  # Можно ввести message: telebot.types.Message
    text = 'Для начала работы введите команду в следующем формате: \n <имя валюты, цену которой вы хотите узнать> ' \
           '<имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты> \n' \
           'Увидеть список всех доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неправильное количество параметров')

        values[2] = values[2].replace(',', ".")  # Замена запятой на точку для обработки <float>
        base, quote, amount = values
        total_base = CurrencyConverter.get_price(base, quote, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {round((total_base * float(amount)), 5)}'
        bot.send_message(message.chat.id, text)

bot.polling()
# bot.polling(none_stop=True)