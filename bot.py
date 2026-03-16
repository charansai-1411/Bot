from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# ===== CONFIG =====
VERIFY_TOKEN = "FarmersBot"

ACCESS_TOKEN = "EAAMq6oZAHy4kBQzYdaPmHNZA4CdvYWuWisYnW4zGkmu4PG8RDyNLIhTM70IR3e6DlDxpid83gLvRThHy5oZBs7qEt5ETiuBNrea3QZCqicGc6volY3FCeZBZBMsAqtzhw9fOZCclgPOVPSSBjK8rLDZC0NXbRFWnJaQjs0R802hpZBZAUCcLIw2QZC50KolmVCGVZBmKX6sVpQ65WZCdW9EzdjFL82b05B6XV9jZCI1ZA0ZCzdflDWv41halwscHomP9XWbS8ocZBEo0q98YXYP51y7ZCVnaCP"
PHONE_NUMBER_ID = "1062500773611327"

# ==================

# create folder for images
os.makedirs("images", exist_ok=True)


# ===== WEBHOOK VERIFICATION =====
@app.get("/webhook")
async def verify(request: Request):

    params = request.query_params

    if params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(params.get("hub.challenge"))

    return "Verification failed"


# ===== RECEIVE MESSAGES =====
@app.post("/webhook")
async def receive_message(request: Request):

    data = await request.json()

    print("Incoming message:", data)

    try:

        value = data["entry"][0]["changes"][0]["value"]

        # ignore status updates
        if "messages" not in value:
            return {"status": "ok"}

        message = value["messages"][0]

        sender = message["from"]
        msg_type = message["type"]

        print("Sender:", sender)

        # ---------- TEXT MESSAGE ----------
        if msg_type == "text":

            text = message["text"]["body"]

            print("Text:", text)

            send_whatsapp_message(sender, f"{text}! Thanks for messaging FarmersBot. This Bot is created by Charan sai.")


        # ---------- IMAGE MESSAGE ----------
        if msg_type == "image":

            image_url = message["image"]["url"]
            media_id = message["image"]["id"]

            print("Image URL:", image_url)

            image_path = download_image(image_url, media_id)

            print("Saved image:", image_path)

            send_whatsapp_message(sender, "Image received 📷. Processing soon.")


    except Exception as e:
        print("Error:", e)

    return {"status": "ok"}


# ===== DOWNLOAD IMAGE =====
def download_image(image_url, media_id):

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    response = requests.get(image_url, headers=headers)

    file_path = f"images/{media_id}.jpg"

    with open(file_path, "wb") as f:
        f.write(response.content)

    return file_path


# ===== SEND MESSAGE =====
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