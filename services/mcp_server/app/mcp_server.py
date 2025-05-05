from fastapi import FastAPI, Request
import httpx

app = FastAPI()

API_URL = "http://python.com:5000"  # API container'ın iç network adresi

@app.post("/mcp")
async def mcp_proxy(request: Request):
    data = await request.json()
    # Burada LLM'den gelen payload'ı parse edebilirsin
    # Örneğin: {"action": "get_user", "user_id": 123}
    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, json=data)
        print(response.text)
        return response.json()