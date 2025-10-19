from flask import Flask, request, jsonify
import telegram
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
bot = telegram.Bot(token=TOKEN)

@app.route('/')
def home():
    return jsonify({
        "status": "active", 
        "message": "🤖 Bot de Telegram - Hola Mundo",
        "webhook_url": f"{RENDER_URL}/webhook",
        "endpoints": {
            "home": "/",
            "webhook": "/webhook", 
            "set_webhook": "/set_webhook",
            "health": "/health"
        }
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook para recibir mensajes de Telegram
    Responde "Hola mundo" a cualquier mensaje
    """
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        
        # Verificar si es un mensaje de texto
        if update.message and update.message.text:
            chat_id = update.message.chat.id
            user_text = update.message.text
            user_name = update.message.from_user.first_name
            
            logger.info(f"Mensaje de {user_name}: {user_text}")
            
            # Responder "Hola mundo" a cualquier mensaje
            bot.send_message(
                chat_id=chat_id,
                text="Hola mundo 👋"
            )
            
            logger.info(f"Respuesta 'Hola mundo' enviada a {user_name}")
            
        return 'ok'
    
    except Exception as e:
        logger.error(f"Error en webhook: {e}")
        return 'error', 500

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Configura el webhook en Telegram automáticamente"""
    try:
        webhook_url = f"{RENDER_URL}/webhook"
        
        # Configurar webhook
        success = bot.set_webhook(webhook_url)
        
        if success:
            logger.info(f"Webhook configurado: {webhook_url}")
            return jsonify({
                "status": "success",
                "message": "✅ Webhook configurado correctamente",
                "webhook_url": webhook_url
            })
        else:
            return jsonify({
                "status": "error", 
                "message": "❌ Error al configurar webhook"
            }), 500
    
    except Exception as e:
        logger.error(f"Error configurando webhook: {e}")
        return jsonify({
            "status": "error",
            "message": f"❌ Error: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint para verificar el estado del bot"""
    try:
        # Verificar que el bot esté funcionando
        bot_info = bot.get_me()
        
        return jsonify({
            "status": "healthy",
            "bot_username": bot_info.username,
            "bot_name": bot_info.first_name,
            "webhook_url": f"{RENDER_URL}/webhook"
        })
    
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500

@app.route('/test', methods=['GET'])
def test_message():
    """Endpoint para probar el envío de mensajes"""
    try:
        chat_id = '5217879590'  # Tu chat_id
        bot.send_message(
            chat_id=chat_id,
            text="🔧 Mensaje de prueba desde el bot desplegado en Render"
        )
        return jsonify({"status": "success", "message": "Mensaje de prueba enviado"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
