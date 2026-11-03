import telebot

TOKEN = "9144206565:AAGqIGGf1RqwiITOb8dIQC7_TR1AMEpxrRE"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Bot online e operacional, Zé!")

bot.infinity_polling()
