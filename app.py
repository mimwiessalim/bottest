from flask import Flask, request
import telegram
import os
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# --- CONFIGURACIÓN ---
TOKEN = '7709737711:AAHCN8hgp27p_LSw9rLqjQhw6LffGd0swME'
CHAT_ID = '5217879590'
INTERVALO = 60 * 10  # cada 10 minutos

# Crear bot
bot = telegram.Bot(token=TOKEN)

@app.route('/')
def home():
    return "🤖 Bot de Telegram está funcionando correctamente!"

@app.route('/webhook', methods=['POST'])
def webhook():
    """Maneja los mensajes entrantes de Telegram"""
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        
        # Verificar si es un mensaje de texto
        if update.message and update.message.text:
            chat_id = update.message.chat.id
            text = update.message.text
            
            logger.info(f"Mensaje recibido: {text}")
            
            # Responder "Hola mundo" a cualquier mensaje
            bot.send_message(
                chat_id=chat_id,
                text="Hola mundo 👋"
            )
            
        return 'ok'
    
    except Exception as e:
        logger.error(f"Error en webhook: {e}")
        return 'error', 500

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Configura el webhook en Telegram"""
    try:
        # Obtener la URL base de Render
        webhook_url = f"https://{request.host}/webhook"
        
        # Configurar webhook
        success = bot.set_webhook(webhook_url)
        
        if success:
            return f"✅ Webhook configurado correctamente: {webhook_url}"
        else:
            return "❌ Error al configurar webhook"
    
    except Exception as e:
        return f"❌ Error: {e}"

@app.route('/health')
def health_check():
    return "✅ Bot saludable"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
