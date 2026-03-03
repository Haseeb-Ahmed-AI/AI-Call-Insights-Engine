import torch
import whisper
import os


# Global Variables
print(torch.cuda.is_available())  
print(torch.cuda.device_count()) 
print(torch.cuda.get_device_name(0))  # Should print the GPU name (if available)

DEVICE = "cuda" if torch.cuda.is_available()  else "mps" if torch.backends.mps.is_available()  else "cpu"
print("GPU or CPU, Detected Device: ", DEVICE)

MODEL = whisper.load_model("turbo", DEVICE)
print("Model Installed")


audio_filePath = os.path.abspath('audio/Test01_Neutral.mp3')
print(audio_filePath)

# ************* Whisper Local Large ******************
def transcribeAudio_whisperLocal(audio_filePath:str) -> str:
    
    
    # How to provide Language into it?
    result = MODEL.transcribe(audio_filePath,
                          prompt="""Transcribe the following conversation between a customer and a company representative. The conversation might be in Urdu or English, you have to figure out. There will be some English words related to banking or any complain, such as 'اے بی ایل', 'الائیڈ بینک', 'کریڈٹ کارڈ', 'بینک', 'برانچ', 'پن', 'savings', 'لمیٹ', 'ensure', 'پالیسی', 'واٹس ایپ', 'انفارمیشن', 'کریڈینشلز', 'منتھ', 'پلاٹینم', 'گولڈ', 'سکس', 'مینجر, 'Policy' and other banking-related words. Donot convert english words into urdu, Show them as it is. Please ensure accurate transcription of both Urdu and English words in context.""",
                          temperature=0.2,       
                          beam_size=5,
                          compression_ratio_threshold=2,  
                          logprob_threshold=-1.0,
                          nospeech_threshold=0.6,
                          word_timestamps= True,             
                          suppress_silence=True,            
                          vad_filter= True,   
                          condition_on_previous_text=True,
                          patience=1,                       
                          repetition_penalty=1.5,
                          language='ur'
                          ) 
     
    transcript = result["text"] 
    print("Transcription: ", transcript)
    print("Language: ", result["language"])
    return transcript 


transcribeAudio_whisperLocal(audio_filePath)
# ===================================================