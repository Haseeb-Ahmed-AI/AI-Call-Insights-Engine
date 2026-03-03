# ****************** Transcript Prompts *********************

transcript_WhisperLocal = """Transcribe the following conversation between a customer and a company representative. The conversation might be in Urdu or English, you have to figure out. There will be some words related to banking or any complain, such as 'اے بی ایل', 'الائیڈ بینک', 'کریڈٹ کارڈ', 'بینک', 'برانچ', 'پن', 'savings', 'لمیٹ', 'ensure', 'پالیسی', 'واٹس ایپ', 'انفارمیشن', 'کریڈینشلز', 'منتھ', 'پلاٹینم', 'گولڈ', 'سکس', 'مینجر, 'Policy' and other banking-related words. Donot convert english words into urdu, Show them as it is. Please ensure accurate transcription of both Urdu and English words in context."""



transcript_Enhancer = """"You are a Transcript Enhancer.

Task:
I will provide you with a conversation transcript.

Language Handling:
    ->  If the Transcript is in Urdu -> Convert into Roman Urdu (Urdu written in english).

Enhancement Rules:
1-  Donot include any additional sentence or word, just provide enhanced Transcript without any other word. 

2-  Remove all personal names and sensitive information, including PINs, passwords, usernames, dates of birth, TPINs, mother's name, father's name, home/work addresses, phone numbers, email addresses, CNIC/NIC numbers, bank account details, credit/debit card numbers, biometric data, customer IDs, and any other personally identifiable or confidential information.

3-  Always correct and retain the following words exactly as written:
    PIN, Allied Bank, CreditCard, DebitCard, Information, Platinum, ABL, Branch, Online Portal, Transaction, etc.

4-  Always spell Allied Bank Limited exactly as it is.

"""


transcript_Diarization = """
You are an Expert in Transcript Diarization / Labelization. Your task is to diarize transcript of a call between a *Company Representative* and a *Customer*. You always have to provide Diarized Transcript.

Do not assign personal names. Instead, use the tags "Company Representative" and "Customer". You have to figure out wisely which Transcript segment belongs to *Company Representative* and *Customer* respectively. 

Assign smaller segments to each speaker, one speaker might can have multiple segments as well. Further, *\n* in Transcript can help you in identifying the segments.

For your Hint:
    -> The *Company Representative* mostly initiates the conversation. Representative act as the information provider, explains products, or serve as the problem solver or help the customers.

    -> The *Customer* is usually the one who seeks information, asking for help with an issue, or asking about products and services.

Carefully analyze the context of each utterance and accurately segment the transcript using these two roles. 


Output Format(JSON): 
[
    {"speaker" : "...", "text" : "..."},
    {"speaker" : "Customer", "text" : "..."},
    ...
]

"""


enhanced_transcript_Diarization = """
You are an expert in enhancing diarized call transcripts between a Company Representative and a Customer.

Task:
- You will receive a diarized transcript (already labeled with speakers).
- Your job is to improve the clarity, accuracy, and readability of the transcript.
- Correct any labeling mistakes, fix grammar and spelling mistakes.
- Do not add, remove, or invent any content—just enhance what is present.

Guidelines:
- Do NOT include any personal names in the transcript.
- Always use only these speaker tags: "Company Representative" and "Customer".
- Retain important banking terms (e.g., PIN, TPIN, Allied Bank, CreditCard, DebitCard, Information, Platinum, ABL, Branch, Online Portal, Transaction, etc.) exactly as written.

- Output must be in JSON format as shown below, with each utterance as a separate object in the list.

Output Format (JSON):
[
    {"speaker": "Company Representative", "text": "..."},
    {"speaker": "Customer", "text": "..."},
    ...
]
"""
    


# ==================== Analysis Prompts ===================

analysis_Sentiments = """You are a sentiment analyzer model. Analyze the following text. Analyze it and provide the sentiment which are: [positive, negative, neutral] with their percentage. First, provide the sentiment with the highest percentage, followed by the second highest. Only provide the sentiment names and percentages in a dictionary/JSON format. No additional text or words.

Examples:

    Transcript: ایک کسٹمر اپنے کریڈٹ کارڈ کے بارے میں معلومات حاصل کر رہا تھا۔ بینک نمائندے نے دو طرح کے کریڈٹ کارڈز، گولڈ اور پلیٹینم کے بارے میں بتایا۔
    Sentiment: {'neutral': 80, 'positive': 15, 'negative': 5}

    Transcript: The update caused a lot of bugs, and it's been frustrating.
    Sentiment: {'negative': 85, 'neutral': 15, 'positive': 0}

Ensure the dictionary contains no extra text. Only output the dictionary to fit frontend needs. Thanks GPT."""
        


analysis_SentimentReason = """
You are an expert Sentiment Analyst.

Input:
   You will be provided with the full transcript of an audio call between two or more participants (typically a customer and a representative).

Your Task:
1. Carefully read and analyze the entire transcript.
2. Determine the **single dominant sentiment** expressed by the **customer at the end of the call**.
   (Choose from: **positive**, **neutral**, or **negative**)
3. Identify the **primary emotion** expressed by the customer based on the sentiment at the end of the call.
        emotions = ["happy", "sad", "angry", "fear", "surprise", "neutral", "frustrated", "disappointed", "confused", "hopefull", "impatient", "calm", "grateful", "relieved", "satisfied", "curious", "impressed", "annoyed", "excited"]
        
4. Provide a explanation (1-2 lines) of **why** this sentiment is dominant, based on the overall customer experience and interaction flow. Provide explanation in short and clear way.
5. Provide a explanation (1-2 lines) of **why** this emotion is dominant, based on the overall customer experience and interaction flow. Provide explanation in short and clear way.

Guidelines:
- Focus on the **overall outcome and customer emotional state by the end of the call**, not just isolated parts.
- Consider how the issue evolved, how well it was addressed, and how the customer **feels at the conclusion**.

Definitions:

➡️ **Positive**:
- The customer began with a query, concern, or even frustration, but by the end:
   - The issue was **fully resolved**.
   - Or the agent **guided the customer properly**, provided clear next steps or escalated appropriately, leading to **customer satisfaction** or **relief**.
   - The customer **felt heard, supported, and satisfied** even if the solution is pending but moving forward clearly.

➡️ **Neutral**:
- The issue was **partially addressed** or remains **unresolved**, and:
   - The agent made a **reasonable effort** (e.g., explained possible scenarios, escalated the case, gave next steps).
   - The customer expresses **uncertainty or mild dissatisfaction**, but not clear frustration or anger.
   - The overall tone is **informative but inconclusive**; the customer leaves with **doubts or ambiguity**, not strong emotions.

➡️ **Negative**:
- The customer remained or became **more frustrated, angry, or disappointed** during the call.
   - The tone of Agent is not coporative, friendly or supportive.
   - The issue was **not resolved**, and
   - The agent failed to provide **satisfactory guidance**, or the guidance was **confusing, insufficient, or dismissive**.
   - Escalation (if any) did not improve the situation, and the customer ended the call feeling **ignored, helpless, or upset**.

Output Format (JSON):

{
  "sentiment": "<positive | neutral | negative>",
  "emotion": "<happy | sad | angry | fear | surprise | neutral | frustrated | disappointed | confused | hopefull | impatient | calm | grateful | relieved | satisfied | curious | impressed | annoyed | excited>",
  "sentiment_reason": "<Brief 1-2 line explanation summarizing why this sentiment is dominant.>"
  "emotion_reason": "<Brief 1-2 line explanation summarizing why this emotion is dominant.>"
}
"""


analysis_Grouping = """
You are an Expert Prompt Analyzer.

Task:
You are provided with the transcript of a conversation between a customer and a bank representative.

Your job is to carefully read and analyze the conversation.

Objective:
Based on the content of the conversation, identify the single most relevant category from the predefined list provided below.

[myABL, Credit Card, Debit Card, Branch/ATM, chequebook, Phone-Banking, Asset Management, Transactions, Current Account, Saving Account, Other]

If the conversation is about multiple topics, choose the category that is most discussed or most important in the call.

Output Format (Json):
{
    "group": ""
}
"""

analysis_agent_customer_sentiment = """

You are an expert Sentiment Analyzer.

Input:
You will be provided with a transcript of a conversation where the speakers are already diarized and labeled as "Company Representative" and "Customer."

Task:
Analyze the conversation transcript.

Determine and assign the sentiment expressed by the "Company Representative" separately from the sentiment expressed by the "Customer."

Assess the transcript to capture the overall mood conveyed by each party.


Output Format (Json):
{
  "representative_sentiment": "<Sentiment for Representative in 2-3 words>",
  "customer_sentiment": "<Sentiment for Customer in 2-3 words>"
}

"""



def analysis_Emotions(sentiment) -> str:
    return f"""You are an emotion analyzer model. Analyze the following text. Analyze it and provide me the emotion. Emotion should be three of the following: [ happy, sad, angry, fear, surprise, neutral, frustrated ]. The Sentiment of the following Input Transcript is {sentiment}. Only provide name and percentage of each emotion just in dictionary form. No other text or word. 
                
    Here are some Examples:

        Transcript: The update caused a lot of bugs, and it's been frustrating. We lost a lot of time trying to fix the issues.
        Emotion: {{'frustrated': 80, 'angry': 15, 'neutral': 5}}

        Transcript: ایک کسٹمر اپنے کریڈٹ کارڈ کے بارے میں معلومات حاصل کر رہا تھا۔ بینک نمائندے نے دو طرح کے کریڈٹ کارڈز، گولڈ اور پلیٹینم کے بارے میں بتایا، جن میں فیس اور کم از کم تنخواہ کے تقاضے شامل ہیں۔ گولڈ کارڈ کی فیس 2500 روپے اور پلیٹینم کارڈ کی فیس 5000 روپے ہوتی ہے۔ کسٹمر کو بتایا گیا کہ پلیٹینم کارڈ کے لیے زیادہ فوائد ہیں اور اس کی حد زیادہ ہوتی ہے۔ نمائندے نے درخواست کے عمل اور تنخواہ کی ضروریات کو بھی واضح کیا۔
        Emotion: {{'neutral': 70, 'happy': 20, 'surprise': 10}}

        Transcript: I love the new features you added to the app! It's so much more user-friendly now, and my team is very happy.
        Emotion: {{'joy': 85, 'happy': 15, 'neutral': 0}}

        Transcript: The project deadline was pushed back, but I don’t mind. It gives me more time to work on it.
        Emotion: {{'neutral': 60, 'happy': 25, 'joy': 15}}
                
        Ensure the result dictionary does not contain any additional words like "json", "emotion" at the start. The format must be exact as this is needed for frontend use. Thanks GPT."""
        
        


analysis_Topic= "You need to find the topic of the following text. Extract the topic from the following text. Go through the Text and tell me about what is discussed in the text. Provide me the topic in 15-20 words or less. Language will be the same as the transcript provided to you, means if Urdu, then Topic will be in urdu, if english topic will be in English and simlar for other langauges."



analysis_Category = "You are a text categorizer. Categorize the following text. Categorize it and provide me the category. The category can be one of the following: [ Business, Education, Entertainment, Family, Friends, Health, Love, Politics, Religion, Science, Sports, Technology, Travel, Other, Complain, Query,Information, Customer Support, Finance, News, Relationship, Self-Improvement, Technology, Work ]. You can give me one to three categories. keep in mind no extra text. "



analysis_Sentiment_Emotion = """You are an advanced sentiment and emotion analyzer model. Analyze the following text and provide both the **sentiment** and **emotion** results.

1. **Sentiment Analysis**: Identify the sentiment [positive, negative, neutral] along with their percentages. Provide the highest percentage first, followed by the second highest. Only output the sentiment names and percentages in JSON format.

2. **Emotion Analysis**: Identify the primary emotions from the following list: [happy, joy, excited,  sad, angry, fear, surprise, neutral, frustrated]. Include the top three emotions with their percentages. Ensure the names and percentages are in JSON format.

For Examples:

    Transcript: The update caused a lot of bugs, and it's been frustrating.  
    Output: 
    {
        "sentiment": {"negative": 95, "neutral": 5, "positive": 0},
        "emotion": {"frustrated": 85, "angry": 10, "neutral": 5}
    }

    Transcript: ایک کسٹمر اپنے کریڈٹ کارڈ کے بارے میں معلومات حاصل کر رہا تھا۔ بینک نمائندے نے دو طرح کے کریڈٹ کارڈز، گولڈ اور پلیٹینم کے بارے میں بتایا۔  
    Output:
    {
        "sentiment": {"neutral": 80, "positive": 20, "negative": 0},
        "emotion": {"neutral": 80, "happy": 10, "surprise": 10}
    }

    Transcript: I love the new features you added to the app!  
    Output:
    {
        "sentiment": {"positive": 100, "neutral": 0, "negative": 0},
        "emotion": {"joy": 60, "happy": 40, "neutral": 0}
    }

Please ensure that the response strictly follows this JSON format:
{
    "sentiment": {},
    "emotion": {}
}
"""



summary_topic = """
You are a transcript summarizer and topic extractor with the following responsibilities:

Summarize the Transcript: Generate a well-structured summary that is comprehensive, logically correct. Ensure it covers all Relavent parts of conversation in 5-6 sentences,.
Donot Include Any Person Name and Focus on main purpose in Transcript.
Avoid using the word "summary" in the output.

Extract the Topic: Identify the core topic discussed in the transcript in 10-20 words or less, ensuring it matches the language of the input.
    
NOte: Output should be in JSON format, strickly follow that. Donot include word Output in Result, just provide Json Format.
Format Example:
```
{
    "summary": "",
    "topic": "",
}
```

The output should be clear, concise, and contextually accurate while preserving the essence of the original conversation
"""


customerSatisfaction_AgentAction = """
You are an expert in analyzing call transcripts between a Company Representative and a Customer. You will be provided with a diarized transcript of a conversation.

Your task is to analyze the interaction and extract the following two key insights:

---

1. **Customer Satisfaction Level (6-10 words):**  
Evaluate how the customer felt at the *end of the call*. Consider the following:
- Was their problem fully resolved or not?
- Was the agent helpful or dismissive?
- Did the customer express frustration, satisfaction, or confusion?
- Did the customer leave with a clear path to a solution?

Choose the **most appropriate** phrase from the list below or generate one that best fits in **6-10 words**:

**Customer Satisfaction Categories (Examples):**
- Problem resolved, customer satisfied with service  
- Issue partially resolved, customer seems uncertain  
- Problem unresolved, customer frustrated or angry  
- Customer satisfied with guidance received  
- Problem escalated, customer hopeful for resolution  
- Customer got clear steps, feels reassured  
- Confused and dissatisfied with outcome  
- Agent helpful, customer appreciated the effort  
- Customer dropped off unsatisfied  
- Call ended positively, customer thanked agent  

---

2. **Agent’s Line of Action (6-10 words):**  
Identify the specific actions taken by the Company Representative during the call. Consider:
- Did the agent provide a resolution?
- Was the issue escalated or transferred?
- Did the agent guide the customer effectively?

Choose the **most accurate** phrase from the list below or generate one that fits best in **6-10 words**:

**Agent Action Categories (Examples):**
- Fully resolved issue on call  
- Provided detailed instructions to fix issue  
- Escalated issue to another department  
- Promised callback or follow-up  
- Transferred call to specialist or support  
- Explained process, guided customer through steps  
- Couldn't resolve, advised next steps  
- Misunderstood issue, gave partial solution  
- Apologized, no concrete action taken  
- Requested more time/information to resolve  

---

**Output Format (JSON):**

{
    "customer_satisfaction": "<Choose or generate a phrase (6-10 words)>",
    "action_by_representative": "<Choose or generate a phrase (6-10 words)>"
}
"""





# ==================  Transcripts ==================
Test01_Transcript = " اسلام علیکم ملار فرمنکن سے میں نیمل بات کر رہی ہوں فاہمے کیا مدد کر سکتے ہو؟ نیمل وقار بات کر رہا ہوں کیسے ہوں؟ اللہم دلاللہ میں صحبہ وقار ٹھیک ہوں امید ہے آپ بھی خیریت سے ہوں گے جی اللہ کا شکر اچھا مجھے کچھ انفومیشن چاہیے کہ پہلے سے میں ٹیپن انٹر کر کے آیا ہوں ٹھیک ہے تو آپ کے پاس ریکارڈ آ رہا ہے ویسے ٹیپن تیپن میں دوبارہ ویریفائی کروائے دیں ویسے سینئیسین گنسٹاپ کا ریٹا آرہا ہے ویریفائی کر دیں گے نہیں میں انٹر کر کے آیا ہوں مجھے یہ پوچھنا ہے کہ ایبیل کریڈیٹ کارڈ کے بارے میں ایبیل کریڈیٹ کارڈ پروائیڈ کرتا ہے کریڈیٹ کارڈ کی سرویس بلکل لائٹ بن کے دو کریڈیٹ کارڈ ہیں میں آپ کو ان دونوں کے حوالے سے سروکار گائیڈ کر دیتی ہوں مدد جو سیٹنا کنفرم کی جائے گا اس کے ڈیفرنٹ کرائیٹیریز ہوتے ہیں ایک سیلوری پرسن کے لیے ہوتا ہے اور ایک بزنس پرسن کے لیے ہوتا ہے آپ کو کون سا کرائیٹیریز ہے سیلوری پرسن کے لیے پوچھنا چاہ رہے ہیں میں آپ کو کنفرم کر دیتے ہوں اگر آپ سیلوری پرسن کے لیے پوچھنا چاہ رہے ہیں تو اس کا جو الیجیبیٹی کرائیٹیریز اب اکار یہ ہے کہ آپ کا لائٹمنٹ کے ساتھ ریلیشیشپ ہونا چاہیے اور منیمم ہر مہنٹ آپ کے اکاؤنٹ میں سیلری 25,000 کی آنی چاہیے اور جو سکس مہنٹ ہوں گے ان سکس مہنٹ میں ہر مہینے آپ کے اکاؤنٹ میں ایک رقم لائٹمی آنی چاہیے یہ اس کا کرائٹیریہ ہے اس کے علاوہ کارڈ دو طرح کی ہیں رقم کتنی مطلب 25,000 کے رقم ہر مہینے اکاؤنٹ میں آنی چاہیے منیمم نہیں منیمم آنی چاہیے جو basic criteria ہے just basic criteria کو یہاں سے guide کیا جارہا ہے basic eligibility criteria یہ ہے اس کے علاوہ دو طرح کے card ہیں ایک gold ہے اور ایک platinum card ہے اگر gold card ہی بات کریں تو اس کی annual fee ہے 2500 plus FAT 2500 germatex annual fee ہے اور gold میں جو اکو limit ملتی ہے وہ ملتی ہے 30,000 سے لے کے 5,000,000 تر کی اس کے علاوہ دوسرا card ہے platinum کا ہے اس کی annual fee ہے 5000 germatex اور اس میں آپ کو limit ملتی ہے 3 واغ سے 2 ملین پر کے یہ limits ہیں اور gold card کا reversal criteria یہ ہے اگر 25000 سپنڈنگ کر لیتے ہیں 90 دنوں میں تو fee reverse ہو جاتی ہے platinum card میں اگر 25000 سپنڈنگ ہوتی ہے 90 days میں تو اس کی بھی fee reverse ہو جاتی ہے ٹھیک ہے اور دوسرا مجھے یہ بتائیے کہ اگر میں نے اس کو apply کرنا ہو تو کیا criteria ہے اگر apply کرنا ہو تو simply ہم یہاں سے آپ کی initial request لیتے ہیں initial request آپ 3 جگہوں سے بنوا سکتے ہیں برانچ کے ذریعے دے سکتے ہیں ہیلپ لنگ کے ذریعے دے سکتے ہیں اور اگر ورڈس ایپ سرویس استعمال کرتے ہیں تو ورڈس ایپ کے ذریعے بھی آپ انیشل ریکویسٹ فارورٹ کروا سکتے ہیں یہاں سے صرف انیشل ریکویسٹ فارورٹ ہوتی ہے جو کہ کریٹ کارٹ دپارٹمنٹ کے پاس جاتی ہے اگر تو آپ الیجیبل ہوں تو وہ پھر آپ کو خود کسٹمہ کو کانٹیکٹ کر کے فردو انفومیشن جو بھی ہے وہ لے لیتے ہیں ہم سے ٹھیک ہے کہ سٹی سے تعلق رکھتے ہیں. میں لاہور سے تعلق رکھتا ہوں. میری جو سلری سلری جو ہوتی ہے نا ڈپوزٹ وہ بھی ای ویل کے اکاونٹ کے اندر ہی ہوتی ہے. تو مجھے پردر تو اسی چیز کے ای ٹھینک وہ ضرورت نہیں ہوگی کسی ڈاکننڈ میں آنا چیز. جی اگر ہوئی بھی تو وہ تو ویسے بھی آپ کو ڈپارٹن خود کانٹیک کر لیتا ہے. کیونکہ ہم تو یہاں سے اگر ریکویسٹ آپ دیتے بھی ہیں تو صرف انیشل ریکویسٹ آگے فارورڈ ہوتی ہیں ہماری انکرے باقی جو بھی فالور پہلا جو بھی پروسیجر ہے وہ تک ویڈیو کارٹ دپارٹن والے اپنا خود کرتے ہیں چلے ٹھیک ہے میں تینکیو فور انفومیشن اگر مجھے ریکویسٹ ڈال لیں تو میں انشاءاللہ دوبارہ کال کر کے نا انیشل ریکویسٹ چکریہ چکریہ چکریہ کال فیڈلے کے جانے چانسر کروں گے لائف و بینکنگ کال کریں گے شکریہ لائف" 



Test02_Transcript = " اسلام علیکم لائکم میں کسی طور پر بھی بات کر رہی ہوں فرمائے آپ کی کیا مدد کر سکتی ہوں؟ بھائی لیکم علیکم اسلام جی میس میں نے ایک کریڈٹ کارڈ کی تھوڑی سے انفومیشن لینی تھی جی پلیج بتائے گا سر کیا جانا چاہ رہے ہیں آپ؟ جی مجھے آپ بتاتی ہیں کہ ایک کریڈٹ کارڈ میں کون کون سے پروڈکٹس ہیں دیئے ہم جبکہ ٹھیک ہے آپ اس سے پہلے کریڈٹ کارڈ استعمال کرتے ہیں سر الائیڈ بینک کا کوئی؟ نہیں الائیڈ بینک کا کوئی ٹھیک ہے میں آپ کو گائیڈ کرنا چاہوں گی پیشانک لمادر کے سر مخاطب کرنے کے لیے آپ کا نام جاننا چاہوں گی؟ تاہا ٹھیک ہے سر تاہا سر دو طرح کے کریڈٹ کارڈ ہوتے ہیں ٹھیک ہے الائیڈ بینک کا ہی آپ کا اکاؤنٹ ہے؟ جی الائیڈ بینک کا اکاؤنٹ ہے ٹھیک ہے سیلی پرسن ہے بزنس مین ہے؟ سیلی پرسن ٹھیک ہے سیلی آپ کی ریگولر اسی اکاؤنٹ میں آتی ہے الائیڈ بینک اکاؤنٹ میں؟ جی اسی اکاؤنٹ میں آتی ہے ٹھیک ہے میں آپ کو گائیڈ کرنا چاہوں گی کہ منیمم آپ کی جو سیلی ریکوائرڈ ہوتی ہے اس کے لیے ٹوئنٹی فائیو تھاؤزنٹ ہونے چاہیے سکس منت کا ریلیشن دیکھا جاتا ہے آپ کا بینک کے ساتھ ٹھیک ہے؟ ٹھیک ہے جی ریگولر اسی اکاؤنٹ میں آنی چاہیے کوئی ڈپ نہیں ہونا چاہیے دو طرح کے کریڈٹ کارڈ ہوتے ہیں ٹھیک ہے ایک گول کارڈ ہوتا ہے جس کی فیز ٹوئنٹی فائیو ہونڈر پلس ٹیکس ہوتی ہے ٹھیک ہے اگر آپ اس سے ٹوئنٹی فائیو تھاؤزنٹ کی سپینڈنگ ٹھری مانس میں کر لیتے ہیں تو وہ ویو اوف ہو جاتی ہے آپ کو ریورٹس ہو جاتی ہے ٹھیک ہے نہیں یہ جی اور اس کی لیمٹ تھا جی سوری ٹھیک ہے ٹھیک ہے ٹھیک ہے ٹھیک ہے ٹھیک ہے ٹھیک ہے جی اور آپ کی ایجی کس سے زیادہ ہونی چاہیے سکسٹی سے کم ہونی چاہیے اور سپیسیفک سیٹیز ہیں جن کے کسٹومر لے سکتے ہیں کس سیٹی سے بات کر رہے ہیں سر آپ ٹھیک ہے ایک منویس میں تین لاکھ سے دو ملین تک ہے جی جو پلیٹینم کارڈ ہے وہ تری لاکھ سے سٹارٹ ہوتی ہے اس کی لیمٹ اور ٹو ملین تک جاتی ہے ٹھیک ہے اور اس کے لیے کیا انکلیٹ ایریا شیلری کا سوری اس کے لیے کیا کہہ رہے ہیں آپ نے اس کا بتایا تھا نا کہ آپ کی ٹھائٹی ٹھالرن پلس ہونی چاہیے شیلری نہیں شیلری ریکوائرمنٹ بیسک جو دونوں کے لیے ہے وہ میں نے آپ کو پہلے گائیڈ کیا کہ ٹوئنٹی فائیو تھاؤزن منیمم ہونی چاہیے باقی میکسیمم جتنی بھی ہوتی مطلب الیجیبل ہونے کے لیے یہ لازمی ہے ریکوائرڈ ہے ٹھیک ہے کوئی اس کے لیے ریکوائرڈ نہیں ہوتا باقی سپیسیفک سیٹیز ہوتے ہیں جن کے کسٹمر لے سکتے ہیں کس سیٹیز سے سر آپ بات کریں آپ سطح بلکل آپ کریڈیٹ کارڈ اپلائی کر سکتے ہیں اپلائی کرنا چاہ رہے ہیں آپ آپ ہیلپ لائن سے بھی اپلائی کر سکتے ہیں آپ اپنے پیرنٹ برانڈ سے اپلائی کر لیں جہاں پہ آپ نے اکاؤنٹ اوپن کروایا اور ویٹس ایپ کے تروں بھی آپ اپلائی کر سکتے ہیں ویٹس ایپ بنکنگ اگر استعمال کرتے ہیں لائن بنک کی تو وہاں سے بھی اپلائی کر سکتے ہیں کچھ اور جانا چاہیں گے آپ سے نہیں ہوں شکریہ اس کے لیے بلنچ کر سکتے ہیں پنوالیجی کا کول ٹرانسفر کر رہی ہوں فیڈبیکس ایک جانب اپنے کیمٹر ایک ہر روح کیجئے گا لائی فرمینکیون کال کرنے کا شکریہ"


