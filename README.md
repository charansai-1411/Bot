🚀 README.md 
# 🌱 FarmersBot — AI-Powered Crop Assistant on WhatsApp

FarmersBot is a simple WhatsApp-based AI assistant that helps farmers detect crop diseases and get guidance instantly.

No apps. No complexity. Just send a message on WhatsApp.

---

## 📸 What it does

- 📷 Send a crop image → Get disease detection
- 💬 Ask questions in text → Get farming guidance
- ⚡ Instant responses using AI
- 📱 Works directly on WhatsApp (no app required)

---

## 🧠 How it works

1. User sends image/text via WhatsApp  
2. WhatsApp Business API receives the message  
3. FastAPI backend processes the request  
4. Image/text is sent to Gemini AI  
5. AI analyzes and returns response  
6. Bot sends reply back to user  

---

## ⚙️ Tech Stack

- **WhatsApp API** → Meta Business Suite  
- **Backend** → FastAPI  
- **AI** → Gemini Vision (image + text understanding)  
- **Deployment** → Render  
- **Version Control** → GitHub  

---

## 🚀 Try it

📲 WhatsApp: +91 9515605026  

Send:
- A crop image 📸  
- OR a farming question 💬  

---

## 🛠️ Setup (Local Development)

### 1. Clone repo

```bash
git clone https://github.com/charansai-1411/Bot.git
cd Bot
2. Install dependencies
pip install -r requirements.txt
3. Add environment variables

Create .env file:

ACCESS_TOKEN=your_whatsapp_token
PHONE_NUMBER_ID=your_phone_id
VERIFY_TOKEN=your_verify_token
GEMINI_API_KEY=your_api_key
4. Run server
uvicorn bot:app --reload
🌐 Deployment

Deployed using Render

Start command:

python3 -m uvicorn bot:app --host 0.0.0.0 --port 10000
⚠️ Limitations
Not 100% accurate (AI-based predictions)
Works best with clear crop images
Currently limited to supported WhatsApp users (sandbox)
🚀 Future Improvements
🌐 Regional language support (Telugu, Hindi)
📈 Better accuracy with custom-trained models
🧩 More actionable farming advice
📊 Crop-specific recommendations
💡 Why this project?

Most farmers don’t use apps.
But they already use WhatsApp daily.

Instead of forcing new behavior, this project builds on what they already use.

🤝 Contributing

Open to ideas, improvements, and collaborations.

Feel free to fork and contribute!

📬 Contact

If you have feedback or ideas, reach out via LinkedIn or GitHub.

⭐ If you found this useful

Give it a star ⭐ — it helps a lot!
