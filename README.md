AI-Powered Resume Analyzer and Candidate Shortlisting System

Problem Statement:
Recruiters often receive a large number of resumes for a single job opening. Manually evaluating each resume against the job description is time-consuming, inconsistent, and prone to bias. There is a need for an automated system that can intelligently compare resumes with job requirements, generate meaningful feedback, and rank candidates efficiently.

Approach:
The system analyzes resumes against a given job description using a combination of semantic similarity, keyword matching, skill-based evaluation, and AI-powered skill extraction.

1)Text Extraction
2)Resumes and job descriptions are parsed from PDF or text files using pdfplumber.
3)Preprocessing
4)Extracted text is cleaned to remove noise and normalize formatting.
5)Skill Extraction
6)Skills are extracted dynamically from the job description using a Groq-powered large language model. This allows the system to identify both technical and soft skills without relying on a fixed predefined list. A fallback rule-based method is used in case the API is unavailable to ensure reliability.
7)Semantic Matching
8)Sentence embeddings are generated using SentenceTransformers. Cosine similarity is used to measure contextual similarity between the resume and job description.
9)Keyword Matching
10)Token-level overlap between resume and job description is calculated to capture explicit keyword matches.
11)Skill Matching
12)The system checks whether required skills extracted from the job description are present in the resume using both exact and partial matching techniques.
13)Final Scoring
A weighted score is computed:
Semantic similarity: 60%
Keyword overlap: 20%
Skill match: 20%
14)AI Feedback
A Groq-powered AI model is used to generate recruiter-style feedback, highlighting strengths and weaknesses.
15)Bulk Resume Ranking
16)Multiple resumes can be uploaded and automatically ranked based on their match score, simulating real-world candidate shortlisting.

Architecture Description:
User Input (Resume / Multiple Resumes + Job Description)
↓
Text Extraction (PDF Parsing)
↓
Preprocessing (Cleaning + Validation)
↓
AI Skill Extraction (Groq LLM)
↓
Embedding Generation (SentenceTransformers)
↓
Similarity + Keyword + Skill Scoring
↓
Final Score Calculation
↓
AI Feedback Generation
↓
Single Result View / Ranked Candidate List

.Key Features:
.Semantic similarity using sentence embeddings
.Hybrid scoring system combining multiple evaluation methods
.AI-based dynamic skill extraction from job descriptions
.AI-generated recruiter feedback
.Bulk resume upload with ranked shortlisting
.Clean and interactive UI
.Robust error handling and validation
.Edge Case Handling
.The system includes safeguards to ensure reliability in real-world scenarios:
.Detects unreadable or corrupted PDFs and prevents invalid processing
.Handles empty inputs for both resumes and job descriptions
.Flags vague job descriptions with insufficient content
.Detects noisy or meaningless text inputs and avoids misleading scores
.Provides fallback behavior when API keys are missing
.Cleans AI-generated output to remove formatting artifacts such as stray markdown symbols

Setup Instructions
Clone the repository
git clone https://github.com/Tann18/Tann18-AI-Powered-Resume-Analyzer-Scorer
Navigate to the project folder
cd your-repo
Install dependencies
pip install -r requirements.txt
Create a .env file
Add your API key:
GROQ_API_KEY=your_api_key_here
Run the application
streamlit run app.py
Dependencies
streamlit
pdfplumber
spacy
sentence-transformers
scikit-learn
groq
python-dotenv

Screenshots:
<img width="1920" height="868" alt="image" src="https://github.com/user-attachments/assets/a19e58ba-d282-4d62-822f-99dca7850468" />
<img width="1920" height="870" alt="image" src="https://github.com/user-attachments/assets/3f352c57-bcfd-4e78-af15-44394b91db49" />
<img width="1920" height="872" alt="image" src="https://github.com/user-attachments/assets/9e41da82-4dac-4523-9547-920232fd9a52" />
<img width="1920" height="865" alt="image" src="https://github.com/user-attachments/assets/da2f3e9f-911a-4428-a407-9f8de65a94c1" />

Project Walkthrough (YouTube):
https://studio.youtube.com/video/VLkFUJDdjpQ/edit

Reflection:
This project was developed using a Python-based stack with Streamlit for the user interface and various machine learning libraries for text processing and similarity analysis. Python was chosen due to its strong ecosystem for natural language processing and ease of rapid prototyping. SentenceTransformers was used to generate embeddings, enabling semantic comparison beyond simple keyword matching.
One of the biggest improvements in the system was transitioning from rule-based skill extraction to AI-based skill extraction using a Groq-powered large language model. This allowed the system to dynamically identify relevant skills from job descriptions instead of relying on a fixed predefined list, improving flexibility and real-world applicability.
One of the biggest challenges encountered was ensuring that resume matching was meaningful and not based solely on keyword overlap. Initial approaches using basic text comparison produced inaccurate results, especially when similar concepts were expressed differently. This was addressed by incorporating embedding-based similarity using cosine distance, which significantly improved contextual understanding.
Another challenge was handling real-world variability in input data. Resumes often come in different formats, and some PDFs may not contain extractable text. Additionally, vague job descriptions or noisy inputs could lead to misleading results. To solve this, input validation and edge case handling were implemented to detect and manage such scenarios gracefully.
Balancing accuracy and performance was also an important consideration. While more advanced models could improve results, they would increase latency and complexity. A hybrid scoring system was chosen to maintain a balance between interpretability, efficiency, and effectiveness.
If more time were available, the system could be enhanced by integrating more advanced transformer-based models for deeper semantic understanding and by introducing a vector database for scalable similarity search. Additional improvements could include extracting skills from both resumes and job descriptions for more precise matching, improving UI visualization, and enabling export of ranked results for recruiter workflows.
