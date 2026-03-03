from fastapi import FastAPI, APIRouter, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from ldap3 import Server, Connection, ALL
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import and_
from database import engine, SessionLocal
import models
from openai import OpenAI
from dotenv import load_dotenv
from typing import Annotated

import os
from services import *


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
router = APIRouter()
client = OpenAI()
models.Base.metadata.create_all(bind=engine)






app = FastAPI()
authorized_host = os.getenv("ALLOWED_HOSTS")
LDAP_SERVER=os.getenv("LDAP_SERVER")
BASE_DN=os.getenv("BASE_DN")
DOMAIN=os.getenv("DOMAIN")




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)]


app.add_middleware(
    CORSMiddleware,
    allow_origins=[authorized_host],  
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
# app.include_router(speechAnalyzerRoute.router)


@app.get("/")
def root():
    return {"message": "Welcome to ABL Speech Analyzer API."}




# *************** Login Authentication ****************
@app.post("/api/login")
async def authenticate_users(db: db_dependency, username: str = Form(...), password: str = Form(...)):
    db_table = models.ABL_speech_analyzer_authenticated_users

    user_dn = f"{username}@{DOMAIN}"
    server = Server(LDAP_SERVER, get_info=ALL)
    
    try:
        conn = Connection(server, user=user_dn, password=password, auto_bind=True)
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials Provided.")

    # Search for user in the directory using sAMAccountName
    search_filter = f"(sAMAccountName={username})"
    conn.search(search_base=BASE_DN, search_filter=search_filter, attributes=["cn", "mail", "title", "department", "company", "mailnickname", "manager", "employeeid"])

    if not conn.entries:
        raise HTTPException(status_code=404, detail="User not found in directory")

    user = conn.entries[0]
    
    # userName = username
    # employeeId = 37640
    # fullName = "Hassan Mahmood"
    # email = "Hassan.Mahmood2@abl.com"
    
    userName = user.mailNickname.value
    employeeId = int(user.employeeID.value)
    fullName = user.cn.value
    email = user.mail.value
    
    try:
        data = db.query(db_table).filter(
            and_(
                db_table.employeeid == int(employeeId), 
                db_table.username == userName,
                db_table.fullname == fullName.lower(),
                db_table.email == email.lower()
            )
        ).first()
        
        if not data:
            raise HTTPException(status_code=404, detail="User not found. Unauthorized Access")
                    
        return {
            "username": data.username,
            "fullname": f"{data.fullname}".title(),
        }
    except HTTPException as e:
        # Re-raise HTTPExceptions (like 404) so FastAPI handles them correctly
        raise e
    except Exception as e:
        # Only catch and handle unexpected errors as 500
        raise HTTPException(status_code=500, detail="Internal Server Error")
        
# =======================================================================