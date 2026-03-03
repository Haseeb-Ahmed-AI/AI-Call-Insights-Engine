from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from openai import OpenAI
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from typing import Annotated
import zipfile
import shutil
import os
from services import *
from database import engine, SessionLocal
import models

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
router = APIRouter()
client = OpenAI()
models.Base.metadata.create_all(bind=engine)


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



# ********* ZIP FOLDER UPLOAD **********
@router.post("/api/upload-multiple-files")
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
@router.post("/api/upload-audio")
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
@router.post("/api/upload-and-analyze")
async def upload_audio(db: db_dependency, InputfileName = Form(...)):
        
    filename = InputfileName
    fileExtension = InputfileName.split(".")[-1]

    print("Starting Analysis")
    creationTime, fileDuration, processedAudio = preprocessing_audio(filename)
    print("Processed Audio")
    
    transcript = transcribeAudio_gptTranscibeAPI(processedAudio, client)
    print("Audio Transcription (Done)")
     
    enhancedTranscript = transcriptEnchancer(transcript, client)
    print("Transcription Enchanced (Done)")
    
    
    diarized_Transcript = diarization_audio(enhancedTranscript, client)
    enhanced_Diarized_Transcript = enhanced_diarization_audio(diarized_Transcript, client)
    # print(enhanced_Diarized_Transcript)
    print("Dialog-flow of Transcript (Done)")  
    

    # _ , emotion = analysis_Sentiments_Emotions(enhancedTranscript, client)
    # print("Sentiment, Emotion (Done)")
    
    grouping = grouping_analysis(enhancedTranscript, client)
    print("Grouping (Done)")
    
    representative_sentiment, customer_sentiment = agent_customer_sentiment_analysis(enhancedTranscript, client)
    print("Customer and Agent Sentiment (Done)")
    
    sentiment, sentiment_reason, emotion, emotion_reason= sentimentReasonAnalysis(enhancedTranscript, client)
    print("Sentiment with Reason and emotion (Done)")
    
    summary, topic = processing_Summary_Topic(enhancedTranscript, client)
    print("Topic/Query & Summary (Done)")
    
    
    customer_satisfaction, agent_lineof_action = satisfaction_action_analysis(diarized_Transcript, client)
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
@router.get("/api/all-records")
async def get_all_records(db: db_dependency):
    db_table = models.Speech_Analysis_Table
    try:
        data = db.query(db_table).all()
        return data
    except Exception as e:
        return {"status": "Error Fetching Data (404)", "message": str(e)}


# ===== Fetch Record by ID ======
@router.get("/api/record-by-id/{id}")
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
@router.delete("/api/delete-record-by-id/{id}")
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
@router.delete("/api/delete-record-by-id-Record-table/{id}")
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
