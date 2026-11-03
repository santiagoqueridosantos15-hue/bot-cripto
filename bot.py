import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import telebot

# --- SERVIDOR WEB PARA O RENDER (PARA NÃO DAR TIMEOUT NA PORTA) ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Arranca o servidor web numa thread secundária em segundo plano
threading.Thread(target=run_server, daemon=True).start()
# -----------------------------------------------------------------

TOKEN = '9144206565:AAFom-n_h0VmwGzMaCJVq7jOsi81ZYg04jU'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🤖 Bot a funcionar!")
    @bot.message_handler(commands=['analisar'])
func def send_analysis(message):
    bot.reply_to(message, "🔍 A analisar o mercado...\n\n💎 SINAL: BTC/USD\nDireção: COMPRA (CALL)\nAssertividade: 92.2%")


# E o comando final para manter o bot a correr
bot.infinity_polling()

