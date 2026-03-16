from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

VERIFY_TOKEN = "FarmersBot"
ACCESS_TOKEN = "YOUR_WHATSAPP_ACCESS_TOKEN"
PHONE_NUMBER_ID = "YOUR_PHONE_NUMBER_ID"


@app.get("/webhook")
async def verify(request: Request):
    params = request.query_params
    if params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(params.get("hub.challenge"))
    return "Verification failed"


@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()
    print("Incoming message:", data)

    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]
        sender = message["from"]
        text = message["text"]["body"]

        send_whatsapp_message(sender, f"You said: {text}")

    except:
        pass

    return {"status": "ok"}


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

    requests.post(url, headers=headers, json=payload)
