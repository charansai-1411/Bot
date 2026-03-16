from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

VERIFY_TOKEN = "FarmersBot"

ACCESS_TOKEN = "EAAMq6oZAHy4kBQzYdaPmHNZA4CdvYWuWisYnW4zGkmu4PG8RDyNLIhTM70IR3e6DlDxpid83gLvRThHy5oZBs7qEt5ETiuBNrea3QZCqicGc6volY3FCeZBZBMsAqtzhw9fOZCclgPOVPSSBjK8rLDZC0NXbRFWnJaQjs0R802hpZBZAUCcLIw2QZC50KolmVCGVZBmKX6sVpQ65WZCdW9EzdjFL82b05B6XV9jZCI1ZA0ZCzdflDWv41halwscHomP9XWbS8ocZBEo0q98YXYP51y7ZCVnaCP"
PHONE_NUMBER_ID = "1062500773611327"

# Create images folder
os.makedirs("images", exist_ok=True)


# Webhook verification
@app.get("/webhook")
async def verify(request: Request):

    params = request.query_params

    if params.get("hub.verify_token") == VERIFY_TOKEN:
        return int(params.get("hub.challenge"))

    return "Verification failed"


# Receive messages
@app.post("/webhook")
async def receive_message(request: Request):

    data = await request.json()

    print("Incoming:", data)

    try:
        value = data["entry"][0]["changes"][0]["value"]

        if "messages" not in value:
            return {"status": "ok"}

        message = value["messages"][0]
        sender = message["from"]
        msg_type = message["type"]

        # TEXT MESSAGE
        if msg_type == "text":
            text = message["text"]["body"]

            print("Text:", text)

            send_whatsapp_message(sender, f"You said: {text}")

        # IMAGE MESSAGE
        if msg_type == "image":

            media_id = message["image"]["id"]

            print("Image media id:", media_id)

            image_path = download_image(media_id)

            print("Saved image:", image_path)

            send_whatsapp_message(sender, "Image received 📷. Processing soon.")

    except Exception as e:
        print("Error:", e)

    return {"status": "ok"}


# Download image from WhatsApp servers
def download_image(media_id):

    url = f"https://graph.facebook.com/v19.0/{media_id}"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    # Get media URL
    response = requests.get(url, headers=headers).json()

    media_url = response["url"]

    # Download file
    image_response = requests.get(media_url, headers=headers)

    file_path = f"images/{media_id}.jpg"

    with open(file_path, "wb") as f:
        f.write(image_response.content)

    return file_path


# Send message back
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