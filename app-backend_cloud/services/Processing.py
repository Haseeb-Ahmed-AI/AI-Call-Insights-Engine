import librosa
import noisereduce as nr 
import soundfile as sf
import os
import datetime
import shutil
# from pydub import AudioSegment

DATASET_DIR = os.path.join(os.getcwd(), "Dataset", "sourceFiles")
OUTPUT_DIR = os.path.join(os.getcwd(), "Dataset", "processedFiles")

# **************** Processing Audio with Insights *****************
def preprocessing_audio(filename: str, file_path=None) -> str:
    if file_path == None:
        audio_path = os.path.join(DATASET_DIR, filename)
    else:
        audio_path = os.path.join(file_path, filename)
    
    try:
        y, sr = librosa.load(audio_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    y_reduced_noise = nr.reduce_noise(y=y, sr=sr)
    
    # Time Duration.
    minutes:int = int(librosa.get_duration(y=y, sr=sr) // 60)
    seconds:int = int(librosa.get_duration(y=y, sr=sr) % 60)
    timeDuration = str(round((float(f"{minutes}.{seconds}")), 2))
    
    # Creation-Time
    creationTime = os.path.getctime(audio_path)
    creation_time_readable = datetime.datetime.fromtimestamp(creationTime)
    time = creation_time_readable.time().replace(microsecond=0)
    date = creation_time_readable.date()
    creationTime = str(date) + " "+ str(time)
 
    # Final-audio.wav Path (temporary)
    # temp_wav_path = os.path.join(OUTPUT_DIR, "final_audio_temp.wav")
    # sf.write(temp_wav_path, y_reduced_noise, sr)

    # # Convert WAV to MP3 using pydub
    # output_mp3_path = os.path.join(OUTPUT_DIR, "final_audio.mp3")
    # audio_segment = AudioSegment.from_wav(temp_wav_path)
    # audio_segment.export(output_mp3_path, format="mp3")
    # os.remove(temp_wav_path)
    
    # Save file in ProcessFiles Folder
    ext = os.path.splitext(audio_path)[1]
    output_audio_path = os.path.join(OUTPUT_DIR, f"finalAudio{ext}")
    shutil.copy(audio_path, output_audio_path) 
    

    # Remove all files in this Directory
    for file in os.listdir(DATASET_DIR):
        file_path = os.path.join(DATASET_DIR, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error removing file {file_path}: {e}")
    
    return creationTime, timeDuration, output_audio_path
# ==================================================================


