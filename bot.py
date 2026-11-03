import telebot

TOKEN = "9144206565:AAFom-n_h0VmwGzMaCJVq7jOsi81ZYg04jU"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot online e operacional, Zé!")

bot.infinity_polling()
