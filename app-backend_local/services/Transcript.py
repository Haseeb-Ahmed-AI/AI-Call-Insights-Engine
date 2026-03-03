import re           
import json
import os
import torch
import whisper
from . import Prompts
from dotenv import load_dotenv
load_dotenv()


print(torch.cuda.is_available())  
print(torch.cuda.device_count()) 
print(torch.cuda.get_device_name(0))  # Should print the GPU name (if available)

DEVICE = "cuda" if torch.cuda.is_available()  else "mps" if torch.backends.mps.is_available()  else "cpu"
print("GPU or CPU, Detected Device: ", DEVICE)

MODEL = whisper.load_model(os.getenv("MODEL"), DEVICE)
print("Model Installed")



#  ************** Whisper OpenAI API ****************
def transcribeAudio_whisperAPI(audio_filePath:str, client:any) -> str:
    with open(audio_filePath, "rb") as audio_file:
        try:
            transcript= client.audio.transcriptions.create(model="whisper-1", file=audio_file)
        except Exception as e:
            raise Exception(f"Error while Performing Transcript:  {e}")
    
    return  transcript.text
# ===================================================



#  ************** Whisper OpenAI Local ***************
def transcribeAudio_whisperLocal(audio_filePath:str) -> str:
    with open(audio_filePath, "rb") as audio_file:
        try:
            result = MODEL.transcribe(audio_filePath,
                          prompt="""Transcribe the following conversation between a customer and a company representative. The conversation might be in Urdu or English, you have to figure out. There will be some English words related to banking or any complain, such as 'Branch', 'Allied Bank Limited', 'ABL', 'Credit card', 'Debit card', 'Gold', 'Platinium', 'Transactions', 'Bank', 'Policy', 'Account' and other banking-related words. Donot convert english words into urdu, Show them as it is. Please ensure accurate transcription of both Urdu and English words in context.""",
                          temperature=0.2,       
                          beam_size=5,
                          compression_ratio_threshold=2,  
                          logprob_threshold=-1.0,                         
                          condition_on_previous_text=False,  # Make it False.
                          patience=2,      
                          no_speech_threshold=0.6, 
                          fp16=True,
                          without_timestamps=True,
                          initial_prompt=None,       
                          language='ur'
                          ) 
     
            transcript = result["text"] 
            print("Language: ", result["language"])
            return transcript 
        except Exception as e:
            print(f"Error while Performing Transcript:  {e}")
            return "Error while performing Transcript!"
# =====================================================


#  *********** GPT-4o Transcibe OpenAI API ************
def transcribeAudio_gptTranscibeAPI(audio_filePath:str, client:any, model:str) -> str:
    with open(audio_filePath, "rb") as audio_file:
        try:
            transcript= client.audio.transcriptions.create(model=model, file=audio_file,  prompt="Kindly Provide full Transcription, which should be very clear and accurate.")
        except Exception as e:
            raise Exception(f"Error while Performing Transcript:  {e}")
    
    return  transcript.text
#  ===================================================
 
    

#  ********* Transcript (RomanUrdu | English) **********
def transcriptEnchancer(transcript:str, client:any, prompt, model):
    response = client.chat.completions.create(
        # model="gpt-4.1",
        model=model,
        messages=[
            {"role": "system", "content": prompt},  
            {"role": "user", "content": transcript}
        ]
    )
    return str(response.choices[0].message.content)
# =======================================================



#  ************** Transcript Diarization *****************
def diarization_audio(transcript:str, client:any, prompt, model):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},  
            {"role": "user", "content": f"The is the Transcript, Diarized that Transcript and Provide me the Result.  {transcript}", }
        ],
        temperature=0.3
    )
    # content = response.choices[0].message.content
    try:
        formatted_dialogues = json.loads(response.choices[0].message.content)
        # Ensure it's a list of dicts with 'speaker' and 'text'
        if isinstance(formatted_dialogues, list) and all(isinstance(item, dict) and 'speaker' in item and 'text' in item for item in formatted_dialogues):
            return json.dumps(formatted_dialogues, indent=4)
    except Exception:
        pass
    # If not JSON, fallback to plain text formatting
    lines = []
    for item in response.choices[0].message.content.split('\n'):
        if ':' in item:
            speaker, text = item.split(':', 1)
            lines.append({'speaker': speaker.strip(), 'text': text.strip()})
    return json.dumps(lines, indent=4)
#  ========================================================



#  ************** Transcript Diarization *****************
def enhanced_diarization_audio(transcript:str, client:any, prompt, model):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},  
            {"role": "user", "content": f"I Provided you Labelized Transcript, enhance it and provide me its enhanced version: {transcript}" }
        ],
        temperature=0.3
    )
    
    
    # Try to parse the response as JSON (list of dicts with 'speaker' and 'text')
    try:
        formatted_dialogues = json.loads(response.choices[0].message.content)
        # Ensure it's a list of dicts with 'speaker' and 'text'
        if isinstance(formatted_dialogues, list) and all(isinstance(item, dict) and 'speaker' in item and 'text' in item for item in formatted_dialogues):
            return json.dumps(formatted_dialogues, indent=4)
    except Exception:
        pass
    # If not JSON, fallback to plain text formatting
    lines = []
    for item in response.choices[0].message.content.split('\n'):
        if ':' in item:
            speaker, text = item.split(':', 1)
            lines.append({'speaker': speaker.strip(), 'text': text.strip()})
    return json.dumps(lines, indent=4)
#  ========================================================



# ***************** Summarization *******************
def summarize_Transcript(transcript:str, client:any, prompt, model):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},        
            {"role": "user", "content": transcript} 
        ]
    )
    return str(response.choices[0].message.content)
# ===================================================



# ******************** Summary and Topic ********************
def processing_Summary_Topic(transcript:str, client:any, prompt, model):
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": transcript}         
        ]
    )   
    output = re.sub(r"^output:\s*", "", str(response.choices[0].message.content).strip("```\njson```").strip())
    data = json.loads(output)

    summary = data.get("summary", {})
    topic = data.get("topic", {})
    
    return str(summary), str(topic)
# ==========================================================