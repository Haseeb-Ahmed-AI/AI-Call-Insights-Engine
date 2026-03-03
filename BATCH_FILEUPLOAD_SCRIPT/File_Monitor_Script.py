import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import asyncio

from openai import OpenAI
from sqlalchemy.orm import Session
from apscheduler.schedulers.blocking import BlockingScheduler  # Changed from BackgroundScheduler
import models
from database import engine, SessionLocal
from services.Processing import preprocessing_audio
from services import *

load_dotenv()
SOURCE_FOLDER_PATH = Path(os.getenv("SOURCE_FOLDER_PATH", ""))

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI()

models.Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        

async def upload_audio(InputfileName:str):
    db = next(get_db())
    global SOURCE_FOLDER_PATH
    
    filename = InputfileName
    fileExtension = InputfileName.split(".")[-1]

    print("Starting Analysis")
    creationTime, fileDuration, processedAudio = preprocessing_audio(filename, SOURCE_FOLDER_PATH)
    print("Processed Audio")
    
    transcript = transcribeAudio_gptTranscibeAPI(processedAudio, client, model=transcript_model)
    print("Audio Transcription (Done)")
     
    enhancedTranscript = transcriptEnchancer(transcript, client, prompt=transcript_enhancer_prompt, model=model)
    print("Transcription Enchanced (Done)")
    
    
    diarized_Transcript = diarization_audio(enhancedTranscript, client, prompt=transcript_diarization_prompt, model=model)
    enhanced_Diarized_Transcript = enhanced_diarization_audio(diarized_Transcript, client, prompt=enhanced_transcript_diarization_prompt, model=model)
    print(enhanced_Diarized_Transcript, end="\n\n")
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
        diarized_transcript = diarized_Transcript,
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
    
    return {"status": "success", "message": "File analyzed and Saved successfully", "filename": filename}




def monitor_files():
   
    global SOURCE_FOLDER_PATH
    
    allFiles_list = os.listdir(SOURCE_FOLDER_PATH)
    print("Checking files:", allFiles_list)
    
    db = next(get_db())
    try:
        db_table = models.Audio_Files_Records_Table
        processedFiles_list = db.query(db_table).all()
    except Exception as e:
        print("Error Fetching Data:", e)
        processedFiles_list = []
    finally:
        db.close()
    
    for file in allFiles_list:
        try:
            creationTime, timeDuration, output_path = preprocessing_audio(file.strip(), SOURCE_FOLDER_PATH)    
            print(file)
            
            is_file_already_processed = any(
                    db_file.filename == file and db_file.file_duration == timeDuration
                    for db_file in processedFiles_list
            )
            print(is_file_already_processed)
            
            if not is_file_already_processed:
                    print(f"Processing new file: {file}")
                    asyncio.run(upload_audio(InputfileName=file.strip()))
        except Exception as e:
            print(f"Error processing file {file}: {e}")

def main():
    
    scheduler = BlockingScheduler()
    scheduler.add_job(monitor_files, "interval", minutes=1)
    
    try:
        print("Scheduler started. Monitoring files every 10 minutes...")
        scheduler.start()
    except (KeyboardInterrupt):
        print("\nShutting down scheduler...")
        scheduler.shutdown()
        print("Scheduler stopped.")
        sys.exit(0)

if __name__ == "__main__":
    main()