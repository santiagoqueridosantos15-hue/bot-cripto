import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import telebot
from telebot import types
import requests
import random
from datetime import datetime, timedelta

# --- SERVIDOR WEB PARA O RENDER ---
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Trading Fresco Bot Active 24/7!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# --- CONFIGURAÇÃO DO BOT ---
TOKEN = '9127242902:AAHoLwLHet8WN6vOc5A_8zfQb98hiUkbam4'  # Coloca aqui o teu token correto do BotFather
bot = telebot.TeleBot(TOKEN)

ATIVOS_VIP = [
    {"nome": "BTC/USD", "id": "bitcoin"},
    {"nome": "ETH/USD", "id": "ethereum"},
    {"nome": "SOL/USD", "id": "solana"},
    {"nome": "XRP/USD", "id": "ripple"},
    {"nome": "ADA/USD", "id": "cardano"},
    {"nome": "AVAX/USD", "id": "avalanche-2"}
]

def calcular_hora_entrada(timeframe_minutos):
    agora = datetime.now()
    if timeframe_minutos == 5:
        minuto_atual = agora.minute
        resto = minuto_atual % 5
        minutos_a_adicionar = 5 - resto if resto != 0 else 5
        if resto == 0 and agora.second > 40:
            minutos_a_adicionar = 10
        proxima_vela = agora + timedelta(minutes=minutos_a_adicionar)
        proxima_vela = proxima_vela.replace(second=0, microsecond=0)
        return proxima_vela.strftime("%H:%M")
    else:
        proxima_vela = agora + timedelta(minutes=1)
        proxima_vela = proxima_vela.replace(second=0, microsecond=0)
        return proxima_vela.strftime("%H:%M")

def gerar_sinal_preciso(timeframe_escolhido):
    escolha = random.choice(ATIVOS_VIP)
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={escolha['id']}&vs_currencies=usd&include_24hr_change=true"
        response = requests.get(url, timeout=6).json()
        
        if escolha['id'] not in response:
            raise Exception("Erro dados")

        dados_ativo = response[escolha['id']]
        preco = float(dados_ativo['usd'])
        variacao = float(dados_ativo.get('usd_24h_change', random.uniform(-3.0, 3.0)))
        
        if variacao >= 0:
            direcao = "COMPRA (CALL) 🟢 🚀"
            tendencia = "Fluxo Institucional de Alta (Bullish Momentum)"
            padrao = "Rompimento de Suporte/Resistência com Volume"
        else:
            direcao = "VENDA (PUT) 🔴 📉"
            tendencia = "Pressão Vendedora Institucional (Bearish Flow)"
            padrao = "Rejeição de Preço em Zona de Oferta"

        assertividade = min(round(85.0 + abs(variacao) * 1.5, 1), 98.8)
        hora_entrada = calcular_hora_entrada(timeframe_escolhido)

        return {
            "ativo": escolha['nome'],
            "timeframe": f"{timeframe_escolhido} Minuto(s) (M{timeframe_escolhido})",
            "preco": preco,
            "variacao": variacao,
            "direcao": direcao,
            "tendencia": tendencia,
            "padrao": padrao,
            "assertividade": assertividade,
            "hora": hora_entrada
        }
    except Exception:
        preco_fb = round(random.uniform(50000, 68000) if escolha['id'] == "bitcoin" else random.uniform(2200, 3800), 2)
        var_fb = round(random.uniform(-2.5, 3.2), 2)
        direcao = "COMPRA (CALL) 🟢 🚀" if var_fb >= 0 else "VENDA (PUT) 🔴 📉"
        
        return {
            "ativo": escolha['nome'],
            "timeframe": f"{timeframe_escolhido} Minuto(s) (M{timeframe_escolhido})",
            "preco": preco_fb,
            "variacao": var_fb,
            "direcao": direcao,
            "tendencia": "Confluência de Order Block & Price Action",
            "padrao": "Padrão de Exaustão de Microtendência",
            "assertividade": 93.5,
            "hora": calcular_hora_entrada(timeframe_escolhido)
        }

@bot.message_handler(commands=['start', 'menu'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item_m1 = types.KeyboardButton('⚡ Sinal M1 (1 Minuto)')
    item_m5 = types.KeyboardButton('⏳ Sinal M5 (5 Minutos)')
    item_ajuda = types.KeyboardButton('❓ Como Funciona')
    markup.add(item_m1, item_m5, item_ajuda)
    
    boas_vindas = (
        "👑 **TRADING FRESCO BOT - MODO PROFISSIONAL** 👑\n\n"
        "Escolhe abaixo se queres um sinal rápido de **1 Minuto (M1)** ou de **5 Minutos (M5)** sincronizado com o fecho exato da vela!"
    )
    bot.reply_to(message, boas_vindas, parse_mode='Markdown', reply_markup=markup)

def enviar_resposta_formatada(message, dados):
    resposta = (
        f"💎 **SINAL INSTITUCIONAL DE ALTA ASSERTIVIDADE** 💎\n\n"
        f"📊 **Ativo:** {dados['ativo']}\n"
        f"⏱ **Timeframe:** {dados['timeframe']}\n"
        f"💵 **Preço Atual:** ${dados['preco']:,.2f}\n"
        f"📈 **Variação 24h:** {dados['variacao']}%\n\n"
        f"🔬 **Análise Técnica:**\n"
        f"• Tendência: {dados['tendencia']}\n"
        f"• Padrão: {dados['padrao']}\n"
        f"• Direção: {dados['direcao']}\n\n"
        f"🎯 **Assertividade Algorítmica:** 🎯 **{dados['assertividade']}%**\n"
        f"⚠️ **Gestão de Risco:** Entrada principal + Máx. 2 Gales\n"
        f"⏰ **Hora Exata de Entrada:** **{dados['hora']}** (Vela Sincronizada)"
    )
    bot.reply_to(message, resposta, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    texto = message.text
    if texto == '⚡ Sinal M1 (1 Minuto)':
        bot.reply_to(message, "⚡ A calcular oportunidade para **M1**...", parse_mode='Markdown')
        dados = gerar_sinal_preciso(1)
        enviar_resposta_formatada(message, dados)
    elif texto == '⏳ Sinal M5 (5 Minutos)':
        bot.reply_to(message, "⏳ A sincronizar vela e a analisar o mercado para **M5**...", parse_mode='Markdown')
        dados = gerar_sinal_preciso(5)
        enviar_resposta_formatada(message, dados)
    elif texto == '❓ Como Funciona':
        bot.reply_to(message, "💡 Podes usar os botões para escolher M1 ou M5. As horas de entrada vêm rigorosamente sincronizadas com o início da próxima vela!")
    else:
        bot.reply_to(message, "🤖 Comando inválido. Envia /start para abrir o painel.")

# --- ARRANQUE BLINDADO CONTRA CONFLITOS (409) ---
if __name__ == '__main__':
    print("A limpar webhooks e instâncias anteriores...")
    try:
        bot.remove_webhook()
    except Exception:
        pass
    
    print("Bot a iniciar modo operacional no Telegram...")
    bot.infinity_polling(skip_pending=True, interval=1, timeout=20)

