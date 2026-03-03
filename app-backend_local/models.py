from sqlalchemy import Column, Integer, String, Text
from database import Base

class Speech_Analysis_Table(Base):
    __tablename__ = 'abl_speech_analysis_table'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    filename = Column(String(255), index=True)
    file_extension = Column(String(255))
    file_duration = Column(String(255))
    transcript = Column(Text)
    enhanced_transcript = Column(Text)
    diarized_transcript = Column(Text)
    grouping = Column(String)
    sentiment = Column(String)
    sentiment_reason = Column(String)
    sentiment_summary = Column(Text)
    representative_sentiment = Column(String)
    customer_sentiment = Column(String)   
    customer_satisfaction = Column(Text)        # <=
    agent_lineof_action = Column(Text)          # <=                                                       
    summary = Column(Text)
    emotion = Column(String)
    topic = Column(String)
    category = Column(Text)
    
    
class Speech_Analysis_Parameters_Table(Base):
    __tablename__ = 'abl_speech_analysis_parameters_table'
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    transcript_enhancer_prompt = Column(Text)
    transcript_diarization_prompt = Column(Text)
    enhanced_transcript_diarization_prompt = Column(Text)
    analysis_sentiment_reason_prompt = Column(Text)
    analysis_grouping_prompt = Column(Text)
    analysis_agent_customer_sentiment_prompt = Column(Text)
    summary_topic_prompt = Column(Text)
    customer_satisfaction_agent_action_prompt = Column(Text)
    model=Column(String(255))
    transcript_model=Column(String(255))
    
    

    
    