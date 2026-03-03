from fastapi import FastAPI, APIRouter, UploadFile, File, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from openai import OpenAI
from dotenv import load_dotenv
from typing import Annotated, AsyncGenerator
import zipfile
import shutil
import os
from services import *


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
router = APIRouter()
client = OpenAI()
models.Base.metadata.create_all(bind=engine)


# *********** Global Variables *************
transcript_enhancer_prompt = ""
transcript_diarization_prompt = ""
enhanced_transcript_diarization_prompt = ""
analysis_sentiment_reason_prompt = ""
analysis_grouping_prompt = ""
analysis_agent_customer_sentiment_prompt = ""
summary_topic_prompt = ""
customer_satisfaction_agent_action_prompt = ""
model = ""
transcript_model = ""
# ==========================================


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """ Runs on Server startup  """
    db = SessionLocal()
    db_table = models.Speech_Analysis_Parameters_Table
    
    global transcript_enhancer_prompt
    global transcript_diarization_prompt
    global enhanced_transcript_diarization_prompt
    global analysis_sentiment_reason_prompt
    global analysis_grouping_prompt
    global analysis_agent_customer_sentiment_prompt
    global summary_topic_prompt
    global customer_satisfaction_agent_action_prompt
    global model
    global transcript_model
    
    try:
        record = db.query(db_table).all()
        if record:
            last_record = record[-1]
            transcript_enhancer_prompt = last_record.transcript_enhancer_prompt
            transcript_diarization_prompt = last_record.transcript_diarization_prompt
            enhanced_transcript_diarization_prompt = last_record.enhanced_transcript_diarization_prompt
            analysis_sentiment_reason_prompt = last_record.analysis_sentiment_reason_prompt
            analysis_grouping_prompt = last_record.analysis_grouping_prompt
            analysis_agent_customer_sentiment_prompt = last_record.analysis_agent_customer_sentiment_prompt
            summary_topic_prompt = last_record.summary_topic_prompt
            customer_satisfaction_agent_action_prompt = last_record.customer_satisfaction_agent_action_prompt
            model = last_record.model
            transcript_model = last_record.transcript_model

        else:
            print("No records found in the Speech_Analysis_Parameters_Table.")
    except Exception as e:
        print(f"Error fetching data from Speech_Analysis_Parameters_Table: {str(e)}")
    finally:
        db.close()
    yield
    


app = FastAPI(lifespan=lifespan)
authorized_host = os.getenv("ALLOWED_HOSTS")

# Directory to store the audio files
DATASET_DIR = "Dataset/sourceFiles/"
UPLOAD_FOLDER = "./Dataset/uploaded_ZIP"
os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



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


# ********* ZIP FOLDER UPLOAD **********
@app.post("/api/upload-multiple-files")
async def upload_zip( file: UploadFile = File(...)):

    zip_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(zip_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Unzip files & store in DATASET_DIR
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(DATASET_DIR)

    # Get all mp3, flac and wav files from unzipped folder
    extracted_files = [f for f in os.listdir(DATASET_DIR) if f.endswith(('.mp3', '.wav', '.flac'))]
    
    return {"fileNamesList":extracted_files}
# =======================================

 
 
# ************ File Upload (MP3 WAV FLAC) ************
@app.post("/api/upload-audio")
async def upload_audio(file: UploadFile = File(...)):

    file_location = os.path.join(DATASET_DIR, file.filename)
    
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    return {"fileNamesList": [file.filename]}
# =====================================================



# **************** Analyze audio file *******************
@app.post("/api/upload-and-analyze")
async def upload_audio(db: db_dependency, InputfileName = Form(...)):
        
    filename = InputfileName
    fileExtension = InputfileName.split(".")[-1]

    print("Starting Analysis")
    creationTime, fileDuration, processedAudio = preprocessing_audio(filename)
    print("Processed Audio")
    
    # transcript = transcribeAudio_gptTranscibeAPI(processedAudio, client, model=transcript_model)
    transcript = transcribeAudio_whisperLocal(processedAudio)
    print("Audio Transcription (Done)")
     
    enhancedTranscript = transcriptEnchancer(transcript, client, prompt=transcript_enhancer_prompt, model=model)
    print("Transcription Enchanced (Done)")
    
    
    diarized_Transcript = diarization_audio(enhancedTranscript, client, prompt=transcript_diarization_prompt, model=model)
    enhanced_Diarized_Transcript = enhanced_diarization_audio(diarized_Transcript, client, prompt=enhanced_transcript_diarization_prompt, model=model)
    print("Dialog-flow of Transcript (Done)")  
    
    
    grouping = grouping_analysis(enhancedTranscript, client, prompt=analysis_grouping_prompt, model=model)
    print("Grouping (Done)")
    
    representative_sentiment, customer_sentiment = agent_customer_sentiment_analysis(enhancedTranscript, client, prompt=analysis_agent_customer_sentiment_prompt, model=model)
    print("Customer and Agent Sentiment (Done)")
    
    sentiment, sentiment_reason, emotion, emotion_reason= sentimentReasonAnalysis(enhancedTranscript, client, prompt=analysis_sentiment_reason_prompt, model=model)
    print("Sentiment with Reason and emotion (Done)")
    
    summary, topic = processing_Summary_Topic(enhancedTranscript, client, prompt=summary_topic_prompt, model=model)
    print("Topic/Query & Summary (Done)")
    
    
    customer_satisfaction, agent_lineof_action = satisfaction_action_analysis(diarized_Transcript, client, prompt=customer_satisfaction_agent_action_prompt, model=model)
    print("Customer Satisfaction, Agent Line of Action (Done)")
    

    print("\nStoring results in Database \n")
    db_analysis = models.Speech_Analysis_Table(
        filename = filename,
        file_extension = fileExtension,
        file_duration = fileDuration + " " + str(creationTime),
        transcript = transcript,
        enhanced_transcript = enhancedTranscript,
        diarized_transcript = enhanced_Diarized_Transcript,
        grouping = grouping,
        sentiment = sentiment,
        sentiment_reason = sentiment_reason,
        sentiment_summary = '',
        representative_sentiment = representative_sentiment,
        customer_sentiment = customer_sentiment,
        customer_satisfaction = customer_satisfaction,
        agent_lineof_action = agent_lineof_action,
        summary = summary,
        emotion = emotion,
        topic = topic,
        category = emotion_reason
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    return {"status": "success", "message": "File analyzed and Saved successfully", "filename": filename}
# ======================================================================


# ===== Fetch All Records ======
@app.get("/api/all-records")
async def get_all_records(db: db_dependency):
    db_table = models.Speech_Analysis_Table
    try:
        data = db.query(db_table).all()
        return data
    except Exception as e:
        return {"status": "Error Fetching Data (404)", "message": str(e)}


# ===== Fetch Record by ID ======
@app.get("/api/record-by-id/{id}")
async def get_record_by_id(id: str, db: db_dependency):
    id = int(id)
    db_table = models.Speech_Analysis_Table
    try:
        data = db.query(db_table).filter(db_table.id == id).first()
        if (data is None):
            return {"status": "Error", "message": "Data not found"}
        return data
    except Exception as e:
        return {"status": "Error", "message": str(e)}



# ===== Delete Record by ID ======
@app.delete("/api/delete-record-by-id/{id}")
async def delete_record_by_id(id: int, db: db_dependency):
    db_table = models.Speech_Analysis_Table
    try:
        data = db.query(db_table).filter(db_table.id == id).first()
        if not data:
            raise HTTPException(status_code=404, detail="Record not found")
        
        db.delete(data)
        db.commit()
        return {"status": "success", "message": "Data deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# ===== Delete Record by ID ======
@app.delete("/api/delete-record-by-id-Record-table/{id}")
async def delete_record_by_id_file_record(id: int, db: db_dependency):
    db_table = models.Audio_Files_Records_Table
    try:
        data = db.query(db_table).filter(db_table.id == id).first()
        if not data:
            raise HTTPException(status_code=404, detail="Record not found")
        
        db.delete(data)
        db.commit()
        return {"status": "success", "message": "Data deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
