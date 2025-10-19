from flask import Flask, request, jsonify
import telegram
import os
import logging

# Configuración
app = Flask(__name__)
TOKEN = '7709737711:AAHCN8hgp27p_LSw9rLqjQhw6LffGd0swME'
RENDER_URL = 'https://bottest-2n1h.onrender.com'

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar bot
try:
    bot = telegram.Bot(token=TOKEN)
    logger.info("Bot inicializado correctamente")
except Exception as e:
    logger.error(f"Error inicializando bot: {e}")
    bot = None

@app.route('/')
def home():
    return jsonify({
        "status": "active", 
        "message": "🤖 Bot de Telegram - Hola Mundo",
        "webhook_url": f"{RENDER_URL}/webhook"
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook para recibir mensajes de Telegram"""
    try:
        if not bot:
            return 'Bot no inicializado', 500
            
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        
        if update.message and update.message.text:
            chat_id = update.message.chat.id
            user_text = update.message.text
            
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
        if not bot:
            return jsonify({"status": "error", "message": "Bot no inicializado"}), 500
            
        webhook_url = f"{RENDER_URL}/webhook"
        success = bot.set_webhook(webhook_url)
        
        if success:
            return jsonify({
                "status": "success",
                "message": "✅ Webhook configurado",
                "webhook_url": webhook_url
            })
        else:
            return jsonify({"status": "error", "message": "❌ Error al configurar webhook"}), 500
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"❌ Error: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        if bot:
            bot_info = bot.get_me()
            return jsonify({
                "status": "healthy",
                "bot_username": bot_info.username
            })
        else:
            return jsonify({"status": "unhealthy", "error": "Bot no inicializado"}), 500
    
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
