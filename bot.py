from fastapi import FastAPI, Request
import requests
import os

app = FastAPI()

# ===== CONFIG =====
VERIFY_TOKEN = "FarmersBot"

ACCESS_TOKEN = "EAAMq6oZAHy4kBRMDAZBVwZCYSQlhLBzljfFc31ZAhoHO0j3JzuYKTjLHprLMiGNO8RW00Qz6BTZC7HHE7cHT9Lf8Cde1Yaa3KFx0UhzyzZBfHU6BziEOtmj4vLOjdCFcqnuTFGnEAzV0aaZBVOCZCZC6lZBn1zFugPoZCsPfwvh0eIxJAR7ZBlMJyka81xVGROCdxTYvcodLw9sa8MMsGwtIUJ5WIwieJ0PoxIIb1AIKqeVx55jNW6JGuMZB62YJpi8Jbjf8DZAeZAcu5KxtsUmC47q8cQV"
PHONE_NUMBER_ID = "1006836429183653"

# 🔥 IMPORTANT: local AI server
AI_SERVICE_URL = "https://farmers-ai-1.onrender.com/predict"

# ==================

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

        if "messages" not in value:
            return {"status": "ok"}

        message = value["messages"][0]

        sender = message["from"]
        msg_type = message["type"]

        print("Sender:", sender)

        # ---------- TEXT ----------
        if msg_type == "text":

            text = message["text"]["body"]

            send_whatsapp_message(
                sender,
                f"{text}! Thanks for messaging FarmersBot 🌱"
            )

        # ---------- IMAGE ----------
        elif msg_type == "image":

            media_id = message["image"]["id"]

            send_whatsapp_message(sender, "📷 Image received. Analyzing...")

            # 🔥 STEP 1: get image URL properly
            image_url = get_image_url(media_id)

            # 🔥 STEP 2: download image
            image_path = download_image(image_url, media_id)

            print("Saved image:", image_path)

            # 🔥 STEP 3: call AI
            disease = call_ai_service(image_path)

            reply = f"🌿 Disease detected: {disease}"

            send_whatsapp_message(sender, reply)

    except Exception as e:
        print("Error:", e)

    return {"status": "ok"}


# ===== GET IMAGE URL =====
def get_image_url(media_id):

    url = f"https://graph.facebook.com/v19.0/{media_id}"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    return response.json()["url"]


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


# ===== CALL AI SERVICE =====
def call_ai_service(image_path):

    try:
        with open(image_path, "rb") as img:

            files = {"file": img}

            response = requests.post(AI_SERVICE_URL, files=files)

            result = response.json()

            return result.get("disease", "Unknown disease")

    except Exception as e:
        print("AI error:", e)
        return "Unable to analyze image"


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