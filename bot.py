from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# ===== CONFIG =====
VERIFY_TOKEN = "FarmersBot"

ACCESS_TOKEN = "EAAMq6oZAHy4kBQ1CZCWbbwSct6fcHvenVbSMrI57ipnJPhqeBZBwkB2zToTuZAQOAM6gbeXa1ONYrUbtFZCzpOWlInedUt9ZCFr0N1AFqLV8MRgFhQDfrT6uHcWzA5bjhjQHjk80IlZB4reXZAlZAYqZBGkuxZBl6TwO9iayrZAA9Q5Dujj4bytAdb8DrMTajGch7CbBowPgFqdAu9ADGOorgRsH3LlsftSxGFXzZCg0okPnd4HgWlqgZCwYoTbZAk7qOcB4xawriNw2ts79MW0CZCQbvhUC"
PHONE_NUMBER_ID = "1062500773611327"

# ==================


# WEBHOOK VERIFICATION
@app.get("/webhook")
async def verify(request: Request):

    params = request.query_params

    mode = params.get("hub.mode")
    challenge = params.get("hub.challenge")
    token = params.get("hub.verify_token")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return int(challenge)

    return {"error": "Verification failed"}


# RECEIVE MESSAGES
@app.post("/webhook")
async def receive_message(request: Request):

    data = await request.json()

    print("Incoming message:", data)

    try:
        value = data["entry"][0]["changes"][0]["value"]

        if "messages" in value:

            message = value["messages"][0]

            sender = message["from"]

            if message["type"] == "text":
                text = message["text"]["body"]

                print("Sender:", sender)
                print("Text:", text)

                send_whatsapp_message(sender, f"You said: {text}")

    except Exception as e:
        print("Error:", e)

    return {"status": "ok"}


# SEND WHATSAPP MESSAGE
def send_whatsapp_message(to, text):

    url = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }

    response = requests.post(url, headers=headers, json=payload)

    print("Send response:", response.text)
