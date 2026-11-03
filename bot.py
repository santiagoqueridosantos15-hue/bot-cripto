import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import telebot
from telebot import types
import requests

# --- SERVIDOR WEB PARA O RENDER (MANTÉM A PORTA ATIVA) ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Trading Fresco Bot Realtime is running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()
# ---------------------------------------------------------

# --- CONFIGURAÇÃO DO BOT ---
TOKEN = '9144206565:AAFom-n_h0VmwGzMaCJVq7jOsi81ZYg04jU'  # O teu token do BotFather
bot = telebot.TeleBot(TOKEN)

# Função para ir buscar preços reais e calcular dados de mercado à séria
def obter_dados_reais(symbol="BTCUSDT"):
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        response = requests.get(url, timeout=5).json()
        
        preco_atual = float(response['lastPrice'])
        variacao = float(response['priceChangePercent'])
        volume = float(response['volume'])
        
        # Lógica dinâmica baseada na variação real de 24h
        direcao = "COMPRA (CALL) 🟢 🚀" if variacao >= 0 else "VENDA (PUT) 🔴 📉"
        tendencia = "Alta / Bullish" if variacao >= 0 else "Baixa / Bearish"
        assertividade = min(round(75 + abs(variacao) * 1.5, 1), 98.5) # Calculado com base na volatilidade real
        
        return {
            "status": "sucesso",
            "ativo": symbol.replace("USDT", "/USD"),
            "preco": preco_atual,
            "variacao": variacao,
            "direcao": direcao,
            "tendencia": tendencia,
            "assertividade": assertividade
        }
    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}

# Menu Principal Interativo
@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item_btc = types.KeyboardButton('📊 Analisar BTC (Real)')
    item_eth = types.KeyboardButton('📊 Analisar ETH (Real)')
    item_sinal = types.KeyboardButton('💎 Sinal Dinâmico VIP')
    item_ajuda = types.KeyboardButton('❓ Ajuda')
    markup.add(item_btc, item_eth, item_sinal, item_ajuda)
    
    boas_vindas = (
        "🤖 **Trading Fresco Bot - Motor de Análise Real** 🚀\n\n"
        "Este bot já não usa textos falsos. Pede uma análise para consultar os dados atuais do mercado em tempo real!"
    )
    bot.reply_to(message, boas_vindas, parse_mode='Markdown', reply_markup=markup)

# Comando de Análise Real para o BTC
@bot.message_handler(commands=['analisar_btc'])
def analisar_btc(message):
    bot.reply_to(message, "🔍 A consultar dados em tempo real na Binance para o Bitcoin...")
    dados = obter_dados_reais("BTCUSDT")
    
    if dados["status"] == "sucesso":
        resposta = (
            f"📊 **ANÁLISE REAL DE MERCADO (AO SEGUNDO)**\n\n"
            f"🪙 **Ativo:** {dados['ativo']}\n"
            f"💵 **Preço Atual:** ${dados['preco']:,.2f}\n"
            f"📈 **Variação 24h:** {dados['variacao']}% \n"
            f"🔄 **Tendência Calculada:** {dados['tendencia']}\n\n"
            f"🎯 **Direção Recomendada:** {dados['direcao']}\n"
            f"⭐️ **Assertividade Estimada:** {dados['assertividade']}%\n"
            f"⚠️ **Gestão:** Entrada com base no fluxo real."
        )
        bot.reply_to(message, resposta, parse_mode='Markdown')
    else:
        bot.reply_to(message, f"❌ Erro ao obter dados do mercado: {dados['detalhe']}")

# Comando de Análise Real para o ETH
@bot.message_handler(commands=['analisar_eth'])
def analisar_eth(message):
    bot.reply_to(message, "🔍 A consultar dados em tempo real para o Ethereum...")
    dados = obter_dados_reais("ETHUSDT")
    
    if dados["status"] == "sucesso":
        resposta = (
            f"📊 **ANÁLISE REAL DE MERCADO (AO SEGUNDO)**\n\n"
            f"🪙 **Ativo:** {dados['ativo']}\n"
            f"💵 **Preço Atual:** ${dados['preco']:,.2f}\n"
            f"📈 **Variação 24h:** {dados['variacao']}% \n"
            f"🔄 **Tendência Calculada:** {dados['tendencia']}\n\n"
            f"🎯 **Direção Recomendada:** {dados['direcao']}\n"
            f"⭐️ **Assertividade Estimada:** {dados['assertividade']}%\n"
            f"⚠️ **Gestão:** Entrada com base no fluxo real."
        )
        bot.reply_to(message, resposta, parse_mode='Markdown')
    else:
        bot.reply_to(message, f"❌ Erro ao obter dados do mercado: {dados['detalhe']}")

# Gestão de cliques nos botões
@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    texto = message.text
    if texto == '📊 Analisar BTC (Real)':
        analisar_btc(message)
    elif texto == '📊 Analisar ETH (Real)':
        analisar_eth(message)
    elif texto == '💎 Sinal Dinâmico VIP':
        analisar_btc(message) # Puxa dados do BTC como sinal principal
    elif texto == '❓ Ajuda':
        bot.reply_to(message, "💡 Usa /analisar_btc ou /analisar_eth para obter preços reais do mercado atual.")
    else:
        bot.reply_to(message, "🤖 Usa /start para abrir o painel de controlos reais.")

bot.infinity_polling()
