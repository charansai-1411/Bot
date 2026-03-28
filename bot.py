from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

app = FastAPI()

# ===== CONFIG (loaded from environment variables) =====
VERIFY_TOKEN = os.environ["VERIFY_TOKEN"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
PHONE_NUMBER_ID = os.environ["PHONE_NUMBER_ID"]
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# ==================

os.makedirs("images", exist_ok=True)

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


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

            reply = ask_gemini_text(text)
            send_whatsapp_message(sender, reply)

        # ---------- IMAGE ----------
        elif msg_type == "image":

            media_id = message["image"]["id"]
            caption = message["image"].get("caption", "What disease does this plant have? Identify the disease and suggest treatment.")

            send_whatsapp_message(sender, "📷 Image received. Analyzing with AI...")

            # Step 1: get image URL
            image_url = get_image_url(media_id)

            # Step 2: download image
            image_path = download_image(image_url, media_id)
            print("Saved image:", image_path)

            # Step 3: analyze with Gemini
            reply = ask_gemini_image(image_path, caption)
            send_whatsapp_message(sender, reply)

    except Exception as e:
        print("Error:", e)

    return {"status": "ok"}


# ===== GEMINI: TEXT =====
def ask_gemini_text(user_message):

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction="You are FarmersBot 🌱, a helpful agricultural assistant on WhatsApp. Answer questions about farming, crops, diseases, and agriculture. Keep responses concise and mobile-friendly (under 500 characters when possible). Use emojis to make responses engaging.",
            ),
        )
        return response.text

    except Exception as e:
        print("Gemini text error:", e)
        return "Sorry, I couldn't process your message right now. Please try again! 🌱"


# ===== GEMINI: IMAGE =====
def ask_gemini_image(image_path, prompt):

    try:
        # Upload image to Gemini
        uploaded_file = client.files.upload(file=image_path)

        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=[
                uploaded_file,
                prompt,
            ],
            config=types.GenerateContentConfig(
                system_instruction="You are FarmersBot 🌱, an expert agricultural AI on WhatsApp. When analyzing plant images: 1) Identify the plant/crop, 2) Detect any disease or pest, 3) Suggest treatment or remedies. Keep responses concise and mobile-friendly. Use emojis.",
            ),
        )
        return response.text

    except Exception as e:
        print("Gemini image error:", e)
        return "Sorry, I couldn't analyze the image right now. Please try again! 📷"


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