from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Groq API 配置
GROQ_API_KEY = "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"
GROQ_MODEL = "llama-3.1-70b"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    user_message = data['events'][0]['message']['text']

    # 調用 Groq LLM
    response = requests.post(
        'https://api.groq.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {GROQ_API_KEY}'},
        json={
            'model': GROQ_MODEL,
            'messages': [{'role': 'user', 'content': user_message}]
        }
    )

    llm_response = response.json()
    reply_message = llm_response['choices'][0]['message']['content']

    # 回覆 LINE 用戶
    reply_token = data['events'][0]['replyToken']
    reply_to_line(reply_token, reply_message)

    return jsonify({'status': 'success'})

def reply_to_line(reply_token, message):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'
    }
    payload = {
        'replyToken': reply_token,
        'messages': [{'type': 'text', 'text': message}]
    }
    requests.post('https://api.line.me/v2/bot/message/reply', headers=headers, json=payload)

if __name__ == '__main__':
    app.run()
