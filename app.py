from flask import Flask, request, jsonify

from bot.ai_bot import AIBot
from services.waha import Waha


app = Flask(__name__)


@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    data = request.json

    if 'payload' in data and 'body' in data['payload']:
        chat_id = data['payload']['from']
        received_message = data['payload']['body']
        is_group = '@g.us' in chat_id

        if is_group:
            return jsonify({'status': 'success', 'message': 'Mensagem de grupo ignorada.'}), 200

        waha = Waha()
        ai_bot = AIBot()
        history_messages = waha.get_history_messages(
            chat_id=chat_id,
            limit=10,
        )
        response_message = ai_bot.invoke(
            history_messages=history_messages,
            question=received_message,
        )
        waha.send_message(
            chat_id=chat_id,
            message=response_message,
        )
        return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
