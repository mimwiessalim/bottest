from flask import Flask, request, jsonify
import telebot
import os
import logging
import requests

# Configuración
app = Flask(__name__)
TOKEN = '7709737711:AAHCN8hgp27p_LSw9rLqjQhw6LffGd0swME'
RENDER_URL = 'https://bottest-2n1h.onrender.com'

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar bot
bot = telebot.TeleBot(TOKEN)

# Almacén temporal de mensajes (para debugging)
message_log = []

@app.route('/')
def home():
    return jsonify({
        "status": "active", 
        "message": "🤖 Bot de Telegram - Hola Mundo",
        "webhook_url": f"{RENDER_URL}/webhook",
        "message_count": len(message_log)
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook para recibir mensajes de Telegram"""
    try:
        if request.is_json:
            update = request.get_json()
            logger.info(f"Update recibido: {update}")
            
            # Guardar para debugging
            message_log.append(update)
            
            # Procesar el mensaje
            if 'message' in update and 'text' in update['message']:
                chat_id = update['message']['chat']['id']
                user_text = update['message']['text']
                user_name = update['message']['from'].get('first_name', 'Usuario')
                
                logger.info(f"Mensaje de {user_name}: {user_text}")
                
                # Responder "Hola mundo"
                try:
                    bot.send_message(chat_id, "Hola mundo 👋")
                    logger.info(f"Respuesta enviada a {user_name}")
                except Exception as e:
                    logger.error(f"Error enviando mensaje: {e}")
            
            return 'ok'
        else:
            logger.error("Request no es JSON")
            return 'error: no json', 400
    
    except Exception as e:
        logger.error(f"Error en webhook: {e}")
        return 'error', 500

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Configurar webhook automáticamente"""
    try:
        webhook_url = f"{RENDER_URL}/webhook"
        
        # Eliminar webhook previo
        bot.remove_webhook()
        
        # Configurar nuevo webhook
        result = bot.set_webhook(url=webhook_url)
        
        # Verificar el webhook
        webhook_info = bot.get_webhook_info()
        
        logger.info(f"Webhook configurado: {webhook_url}")
        logger.info(f"Info webhook: {webhook_info}")
        
        return jsonify({
            "status": "success",
            "message": "✅ Webhook configurado",
            "webhook_url": webhook_url,
            "webhook_info": {
                "url": webhook_info.url,
                "has_custom_certificate": webhook_info.has_custom_certificate,
                "pending_update_count": webhook_info.pending_update_count
            }
        })
    
    except Exception as e:
        logger.error(f"Error configurando webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        # Verificar que el bot esté funcionando
        bot_info = bot.get_me()
        webhook_info = bot.get_webhook_info()
        
        return jsonify({
            "status": "healthy",
            "bot_username": bot_info.username,
            "webhook_url": webhook_info.url,
            "pending_updates": webhook_info.pending_update_count,
            "total_messages": len(message_log)
        })
    
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route('/debug', methods=['GET'])
def debug_info():
    """Endpoint de debugging"""
    return jsonify({
        "messages_received": message_log,
        "total_messages": len(message_log),
        "webhook_url": f"{RENDER_URL}/webhook"
    })

@app.route('/test', methods=['GET'])
def test_bot():
    """Probar el bot enviando un mensaje"""
    try:
        chat_id = '5217879590'  # Tu chat_id
        bot.send_message(chat_id, '✅ Bot funcionando correctamente en Render!')
        return jsonify({"status": "success", "message": "Mensaje de prueba enviado"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/remove_webhook', methods=['GET'])
def remove_webhook():
    """Eliminar webhook (para troubleshooting)"""
    try:
        result = bot.remove_webhook()
        return jsonify({"status": "success", "message": "Webhook eliminado"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
