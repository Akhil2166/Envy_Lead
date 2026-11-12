import httpx
body = {"name": "Test Lead", "phone": "9999999999", "budget": "50 lakh", "location": "Madhapur", "intent": "buy", "status": "new"}
r = httpx.post("https://envylead-backend.vercel.app/api/leads", json=body, timeout=30)
print("STATUS:", r.status_code)
print("BODY:", r.text)
