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
bot = telegram.Bot(token=TOKEN)

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
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        
        if update.message and update.message.text:
            chat_id = update.message.chat.id
            user_text = update.message.text
            
            # Responder "Hola mundo"
            bot.send_message(
                chat_id=chat_id,
                text="Hola mundo 👋"
            )
            logger.info(f"Respondí 'Hola mundo' a: {user_text}")
            
        return 'ok'
    
    except Exception as e:
        logger.error(f"Error en webhook: {e}")
        return 'error', 500

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Configurar webhook automáticamente"""
    try:
        webhook_url = f"{RENDER_URL}/webhook"
        success = bot.set_webhook(webhook_url)
        
        return jsonify({
            "status": "success" if success else "error",
            "message": "✅ Webhook configurado" if success else "❌ Error",
            "webhook_url": webhook_url
        })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Bot funcionando correctamente"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
