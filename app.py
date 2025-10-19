from flask import Flask, request, jsonify
import telebot
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
bot = telebot.TeleBot(TOKEN)

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
        json_data = request.get_json()
        
        if 'message' in json_data and 'text' in json_data['message']:
            chat_id = json_data['message']['chat']['id']
            user_text = json_data['message']['text']
            
            # Responder "Hola mundo"
            bot.send_message(chat_id, "Hola mundo 👋")
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
        bot.remove_webhook()
        success = bot.set_webhook(url=webhook_url)
        
        return jsonify({
            "status": "success",
            "message": "✅ Webhook configurado",
            "webhook_url": webhook_url
        })
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Bot funcionando correctamente"})

@app.route('/test', methods=['GET'])
def test_bot():
    """Probar el bot enviando un mensaje"""
    try:
        bot.send_message('5217879590', '✅ Bot funcionando correctamente en Render!')
        return jsonify({"status": "success", "message": "Mensaje de prueba enviado"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
