import requests

def send_telegram_message(chat_id, message):
    bot_token = '7285772023:AAFHj3W6e-9ukh9u-lU2vNLOQom2rs1-NOc'  # Замените на ваш токен бота
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
    }
    response = requests.post(url, data=payload)
    
    # Проверка ответа от Telegram
    if response.status_code == 200:
        print("Сообщение отправлено успешно!")
    else:
        print(f"Ошибка при отправке сообщения: {response.status_code} {response.text}")
