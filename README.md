# AI Call Insights Engine


## Workflow
<img width="4217" height="1877" alt="SpeechAnalyzer" src="https://github.com/user-attachments/assets/0528c546-1d01-4f58-bfc9-47a9c34c753d" />




## 🚀 Overview

This system helps organizations of all sizes improve customer experience
and operational efficiency by analyzing inbound and outbound calls
automatically. It provides:

-   High‑quality transcripts\
-   Speaker identification\
-   Sentiment & emotion analysis\
-   Customer satisfaction evaluation\
-   Agent performance insights\
-   Conversation summaries & topics

Its scalable architecture makes it ideal for startups, SMEs, and
enterprise‑level teams processing thousands of calls daily.

------------------------------------------------------------------------

## 📂 Core Features

### **1. Audio Upload & Processing**

-   Upload single audio files (`.mp3`, `.wav`, `.flac`)
-   Upload ZIP files containing multiple audio recordings
-   Automatic audio extraction and preprocessing

### **2. AI‑Powered Transcription**

-   Local Whisper model for accurate transcription
-   AI‑enhanced transcript cleanup for readability

### **3. Speaker Diarization**

-   Differentiates between agent and customer
-   Produces a structured conversational flow

### **4. Sentiment, Emotion & Reasoning**

-   Full sentiment breakdown
-   Emotion classification with reasoning
-   Agent vs customer sentiment comparison

### **5. Conversation Summary & Categorization**

-   Summaries of customer issues
-   Topic detection
-   Categorization and intent grouping

### **6. Customer Satisfaction & Agent Action Insights**

-   Automatically determines customer satisfaction
-   Suggests recommended actions for agents

### **7. Database Integration**

-   Stores all analysis results using SQLAlchemy ORM
-   Fetch, review, and delete past analyses
-   Stores dynamic prompt parameters for configurable behavior

------------------------------------------------------------------------

## 🏗️ Tech Stack

  Component           Technology
  ------------------- ----------------------------------
  Backend Framework   FastAPI
  Transcription       Whisper (Local)
  AI Processing       OpenAI GPT Models
  Database            SQLAlchemy with env‑based DB URL
  File Handling       ZIP extraction, audio storage
  Architecture        Modular, cloud‑ready, scalable

------------------------------------------------------------------------

## 📁 Project Structure

    project/
    │── main.py               # FastAPI app and analysis pipeline
    │── models.py             # Database ORM models
    │── database.py           # Database engine + session
    │── services/             # Audio & AI analysis (imported externally)
    │── Dataset/
    │   ├── sourceFiles/      # Audio files
    │   ├── uploaded_ZIP/     # ZIP uploads

------------------------------------------------------------------------

## 🔧 How It Works

1.  Audio file/ZIP is uploaded.
2.  Audio is preprocessed (cleaning, duration, format).
3.  Whisper generates transcription.
4.  GPT models enhance transcript and perform:
    -   Speaker diarization\
    -   Sentiment & emotional reasoning\
    -   Agent & customer sentiment separation\
    -   Summary + topic detection\
    -   Customer satisfaction scoring\
    -   Agent action recommendations\
5.  Data is stored in the database.
6.  Records can be retrieved or removed through API endpoints.

------------------------------------------------------------------------

## 🌍 Use Cases

### **• BPO & Call Center Quality Assurance**

Automate QA review, reduce manual auditing, and evaluate agent
performance.

### **• Customer Experience Improvement**

Measure sentiment trends and discover service gaps.

### **• Agent Coaching & Upskilling**

Provide targeted coaching recommendations based on real call
interactions.

### **• Scalable Enterprise Analytics**

Deploy across large teams with high call volumes.

### **• Small Business Automation**

Affordable automated QA without expanding staff.

------------------------------------------------------------------------

## 🛠️ Installation

1.  **Clone the repo**

``` bash
git clone https://github.com/yourusername/ai-call-insights-engine.git
cd ai-call-insights-engine
```

2.  **Install dependencies**

``` bash
pip install -r requirements.txt
```

3.  **Create `.env` file**

``` env
DATABASE_URL=your_database_url
OPENAI_API_KEY=your_openai_api_key
ALLOWED_HOSTS=*
```

4.  **Run the server**

``` bash
uvicorn main:app --reload
```

------------------------------------------------------------------------

## 📡 API Endpoints

### **Upload**

-   `POST /api/upload-audio`\
-   `POST /api/upload-multiple-files`

### **Analysis**

-   `POST /api/upload-and-analyze`

### **Database**

-   `GET /api/all-records`\
-   `GET /api/record-by-id/{id}`\
-   `DELETE /api/delete-record-by-id/{id}`

------------------------------------------------------------------------

## 📈 Scalability

The entire system is built with horizontal scalability in mind: -
Multiple workers can process calls in parallel - Databases handle large
datasets efficiently - Works on local servers or cloud platforms

------------------------------------------------------------------------

## 🤝 Contributing

Contributions are welcome. Fork the project and submit a pull request.


