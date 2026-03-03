from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import speechAnalyzerRoute
from dotenv import load_dotenv

import os
load_dotenv()

app = FastAPI()
authorized_host = os.getenv("ALLOWED_HOSTS")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[authorized_host],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
app.include_router(speechAnalyzerRoute.router)


@app.get("/")
def root():
    return {"message": "Welcome to ABL Speech Analyzer API."}

