from fastapi import FastAPI, Request

app = FastAPI()

VERIFY_TOKEN = "FarmersBot"


@app.get("/webhook")
async def verify(request: Request):
    params = request.query_params

    if params.get("hub.verify_token") == VERIFY_TOKEN:
        return params.get("hub.challenge")

    return "Verification failed"


@app.post("/webhook")
async def receive_message(request: Request):
    data = await request.json()

    print("Incoming message:", data)

    return {"status": "received"}
