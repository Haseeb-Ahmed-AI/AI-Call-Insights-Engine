import re
from . import Prompts
import json


# ************** OPENAI-API-CALL-BLUEPRINT ****************
def openai_api_call(client:any, prompt:str, input:any, model:str = "gpt-4.1"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": input}         
        ]
    )   
    output = response.choices[0].message.content.strip()
    return str(output)
# =========================================================



# *************** Sentiment Analysis (Not-Used) ******************
def sentimentAnalysis(transcript:str, client:any, prompt, model):
    # prompt = Prompts.analysis_Sentiments
    
    response = openai_api_call(client, prompt, transcript, model)
    output = re.sub(r"^Sentiment:\s*", "", response)
    output = output.strip("```\njson```").strip()

    return str(output)
# =====================================================



# ***************** Sentiment and Emotions Analysis  *****************
def analysis_Sentiments_Emotions(transcript:str, client:any, prompt, model):
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": transcript}         
        ]
    )  
    data = json.loads(str(response.choices[0].message.content).strip("```json\n```").strip())

    sentiment = data.get("sentiment", '')
    emotion = data.get("emotion", '')

    return str(sentiment), str(emotion)
# ====================================================================



# ************ Sentiment with Reason Analysis **************
def sentimentReasonAnalysis(transcript: str, client: any, prompt, model):
    
    
    response = openai_api_call(client, prompt, transcript, model)
    response = response.strip("```\njson```").strip()
    print(response, type(response), sep=" ")
    data = json.loads(response)
    sentiment = data.get("sentiment", '')
    sentiment_reason = data.get("sentiment_reason", '')
    emotion= data.get("emotion", '')
    emotion_reason = data.get("emotion_reason", '')
    return sentiment, sentiment_reason, emotion, emotion_reason
# ==========================================================



# ************* Grouping Analysis ******************
def grouping_analysis(transcript: str, client: any, prompt, model):
    
    response = openai_api_call(client, prompt, transcript, model)
    response = response.strip("```\njson```").strip()
    print(response, type(response), sep=" ")
    
    data = json.loads(response)
    response = data.get("group", '')
    print(response)
    return str(response)
# ==================================================



# ***** Agent and Customer Sentiment Analysis ******
def agent_customer_sentiment_analysis(transcript: str, client: any, prompt, model):
    
    response = openai_api_call(client, prompt, transcript, model)
    response = response.strip("```\njson```").strip()
    
    data = json.loads(response)
    data = {k.lower(): v for k, v in data.items()}
    print(data)
    representative_sentiment = data.get("representative_sentiment", '')
    customer_sentiment = data.get("customer_sentiment", '')
    return representative_sentiment, customer_sentiment
# ===================================================





# ************* Categorize the Text ******************
def categorizeText(transcript:str, client:any, prompt, model):
    
    response = openai_api_call(client, prompt, transcript, model)
    return response
# ====================================================


# ************* At-End: Customer Satisfaction and Action by Agent ******************
def satisfaction_action_analysis(transcript:str, client:any, prompt, model):
    """Diarized Transcript, Customer Satisfaction and End Action by Agent"""
    
    response = openai_api_call(client, prompt, transcript, model)
    response = response.strip("```\njson```").strip()
    data = json.loads(response)
    
    data = {k.lower(): v for k, v in data.items()}
    customer_satisfaction = data.get("customer_satisfaction", '')
    action_by_representative = data.get("action_by_representative", '')
    
    return customer_satisfaction, action_by_representative
# ===================================================================================