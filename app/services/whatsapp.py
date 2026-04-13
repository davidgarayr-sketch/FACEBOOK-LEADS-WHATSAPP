import requests
from app.config import WHATSAPP_TOKEN, WHATSAPP_PHONE_ID

def send_whatsapp_message(to_number: str, message: str):
    url = f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "template",
        "template": {
            "name": "hello_world",
            "language": {
                "code": "en_US"
            }
        }
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"WhatsApp enviado a {to_number}: {response.status_code}")
    print(f"Respuesta WhatsApp: {response.text}")
    return response.json()
    #print(f"WhatsApp enviado a {to_number}: {response.status_code}")
    #return response.json()