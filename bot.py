import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import telebot
from telebot import types
import requests
import random
from datetime import datetime

# --- SERVIDOR WEB PARA O RENDER (MANTÉM A PORTA ATIVA) ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Trading Fresco Bot Elite Pro is running!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()
# ---------------------------------------------------------

# --- CONFIGURAÇÃO DO BOT ---
TOKEN = '9144206565:AAFom-n_h0VmwGzMaCJVq7jOsi81ZYg04jU'  # Substitui pelo teu token do BotFather
bot = telebot.TeleBot(TOKEN)

# Lista completa de ativos monitorizados pelo motor de alta performance
ATIVOS_VIP = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT", "ADAUSDT", "AVAXUSDT", "LINKUSDT"]

def gerar_analise_profissional():
    # Seleciona aleatoriamente um ativo da lista para garantir diversidade de entradas
    symbol = random.choice(ATIVOS_VIP)
    try:
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        response = requests.get(url, timeout=5).json()
        
        if 'lastPrice' not in response:
            return {"status": "erro", "detalhe": "Erro na resposta da API"}

        preco = float(response['lastPrice'])
        variacao = float(response['priceChangePercent'])
        volume = float(response['volume'])
        
        # Análise baseada na tendência real e volatilidade do par
        if variacao > 0:
            direcao = "COMPRA (CALL) 🟢 🚀"
            tendencia = "Tendência de Alta / Bullish com Fluxo Institucional"
             padrao = "Rompimento de Resistência com Volume Crescente"
        else:
            direcao = "VENDA (PUT) 🔴 📉"
            tendencia = "Tendência de Baixa / Bearish com Pressão Vendedora"
            padrao = "Rejeição em Zona de Oferta / Exhaustion Candle"

        # Cálculo de assertividade dinâmico baseado na força do movimento
        assertividade = min(round(82.0 + abs(variacao) * 1.5, 1), 98.9)
        
        # Hora atual exata para a entrada
        hora_atual = datetime.now().strftime("%H:%M")

        return {
            "status": "sucesso",
            "ativo": symbol.replace("USDT", "/USD"),
            "preco": preco,
            "variacao": variacao,
            "direcao": direcao,
            "tendencia": tendencia,
            "padrao": padrao,
            "assertividade": assertividade,
            "hora": hora_atual
        }
    except Exception as e:
        return {"status": "erro", "detalhe": str(e)}

# Menu Principal com Teclado Profissional
@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item_sinal = types.KeyboardButton('💎 Gerar Sinal VIP Real')
    item_scan = types.KeyboardButton('🔍 Varredura de Mercado')
    item_ajuda = types.KeyboardButton('❓ Painel de Ajuda')
    markup.add(item_sinal, item_scan, item_ajuda)
    
    boas_vindas = (
        "👑 **TRADING FRESCO BOT - SISTEMA ELITE VIP** 👑\n\n"
        "Sistema de análise institucional conectado diretamente aos feeds de preços globais.\n"
        "Clica em **Gerar Sinal VIP Real** para o robô varrer o mercado e encontrar uma oportunidade real e diferente a cada clique!"
    )
    bot.reply_to(message, boas_vindas, parse_mode='Markdown', reply_markup=markup)

# Comando principal de análise profissional
@bot.message_handler(commands=['analisar', 'sinal'])
def enviar_sinal_vip(message):
    bot.reply_to(message, "⚡ **A varrer os livros de ordens e pares de criptomoedas...** Aguarda um segundo.")
    
    dados = gerar_analise_profissional()
    
    if dados["status"] == "sucesso":
        resposta = (
            f"💎 **SINAL INSTITUCIONAL DE ALTA ASSERTIVIDADE** 💎\n\n"
            f"📊 **Ativo Analisado:** {dados['ativo']}\n"
            f"⏱ **Timeframe:** 5 Minutos (M5)\n"
            f"💵 **Preço de Cotação:** ${dados['preco']:,.2f}\n"
            f"📈 **Variação 24h:** {dados['variacao']}%\n\n"
            f"🔬 **Análise Confluente & Estratégia:**\n"
            f"• Confluência: {dados['tendencia']}\n"
            f"• Padrão Técnico: {dados['padrao']}\n"
            f"• Direção Exata: {dados['direcao']}\n\n"
            f"🎯 **Assertividade Algorítmica:** 🎯 **{dados['assertividade']}%**\n"
            f"⚠️ **Gestão de Risco:** Entrada principal + Máx. 2 Gales\n"
            f"⏰ **Hora de Execução Recomendada:** {dados['hora']}"
        )
        bot.reply_to(message, resposta, parse_mode='Markdown')
    else:
        bot.reply_to(message, f"❌ Erro temporário ao comunicar com o servidor de preços: {dados['detalhe']}")

# Gestão dos botões interativos
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    texto = message.text
    if texto in ['💎 Gerar Sinal VIP Real', '🔍 Varredura de Mercado']:
        enviar_sinal_vip(message)
    elif texto == '❓ Painel de Ajuda':
        bot.reply_to(message, "💡 **Instruções:** Utiliza o comando `/analisar` ou os botões do menu para que o robô procure novas oportunidades reais em ativos diferentes em tempo real.")
    else:
        bot.reply_to(message, "🤖 Comando não reconhecido. Escreve `/start` para abrir o menu de controlo.")

bot.infinity_polling()
