import requests

def send_message(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("Сообщение отправлено успешно!")
    else:
        print(f"Ошибка при отправке сообщения: {response.text}")

if __name__ == "__main__":
    # Замените эти значения на ваши данные
    API_TOKEN = '7628020116:AAGxzTieGUSxkxg4N7wGQXVRe8X-zjmIvpA'
    CHAT_ID = '1566877581'            # ID чата, куда отправляем сообщение
    TEXT = 'Привет, мир!'                # Текст сообщения

    send_message(TOKEN, CHAT_ID, TEXT)