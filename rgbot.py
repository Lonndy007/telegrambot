import telebot
from config import keys,TOKEN
from classswdwd import ConvertionException, CryptoConventer
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def repeat(message: telebot.types.Message):
   bot.send_message(message.chat.id,"привет   что бы конвертировать валюты напиши <переводимая валюта>,<в какую переводишь>,<сумму>,\n что бы узнать список доступных валют напиши /values")


@bot.message_handler(commands=["values"])
def repeat(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text,key))
    bot.reply_to(message,text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException("Не достаточно переменных")

        quote, base, amount = values
        total_base = CryptoConventer.convert(quote,base,amount)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")
    except  Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f"Цена {amount}  {quote} в {base} - {total_base}"
        bot.send_message(message.chat.id, text)



bot.polling(none_stop=True)