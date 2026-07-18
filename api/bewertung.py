from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS aktivieren, damit Anfragen von überall durchgehen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/bewertung")
async def receive_bewertung(request: Request):
    neue_bewertung = await request.json()
    
    # Logged die Bewertung direkt in Echtzeit ins Vercel-Dashboard
    print("NEUE BEWERTUNG ERHALTEN:", neue_bewertung)
    
    return {"status": "success"}