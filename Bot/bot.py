from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()
VERIFY_TOKEN = "FarmersBot"

@app.get("/webhook")
async def verify(request: Request):
    params = request.query_params

    if params.get("hub.mode") == "subscribe" and params.get("hub.verify_token") == VERIFY_TOKEN:
        return PlainTextResponse(content=params.get("hub.challenge"))

    return PlainTextResponse(content="Verification failed", status_code=403)