Project Title
AI-Powered Resume Analyzer and Candidate Shortlisting System

Problem Statement
Recruiters often receive a large number of resumes for a single job opening. Manually evaluating each resume against the job description is time-consuming, inconsistent, and prone to bias. There is a need for an automated system that can intelligently compare resumes with job requirements, generate meaningful feedback, and rank candidates efficiently.

Approach
The system analyzes resumes against a given job description using a combination of semantic similarity, keyword matching, and skill-based evaluation.

Text Extraction
Resumes and job descriptions are parsed from PDF or text files using pdfplumber.
Preprocessing
Extracted text is cleaned to remove noise and normalize formatting.
Skill Extraction
Skills are extracted from the job description to represent employer requirements. These include both technical and soft skills.
Semantic Matching
Sentence embeddings are generated using SentenceTransformers. Cosine similarity is used to measure contextual similarity between the resume and job description.
Keyword Matching
Token-level overlap between resume and job description is calculated to capture explicit keyword matches.
Skill Matching
The system checks whether required skills from the job description are present in the resume.
Final Scoring
A weighted score is computed:
Semantic similarity: 60%
Keyword overlap: 20%
Skill match: 20%
AI Feedback
An AI model is used to generate recruiter-style feedback, highlighting strengths and weaknesses.
Bulk Resume Ranking
Multiple resumes can be uploaded and automatically ranked based on their match score, simulating real-world candidate shortlisting.

Architecture Description

User Input (Resume / Multiple Resumes + Job Description)
↓
Text Extraction (PDF Parsing)
↓
Preprocessing (Cleaning + Validation)
↓
Skill Extraction (from Job Description)
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

Key Features

Semantic similarity using sentence embeddings
Hybrid scoring system combining multiple evaluation methods
Skill extraction based on job requirements
AI-generated recruiter feedback
Bulk resume upload with ranked shortlisting
Clean and interactive UI
Robust error handling and validation

Edge Case Handling

The system includes safeguards to ensure reliability in real-world scenarios:

Detects unreadable or corrupted PDFs and prevents invalid processing
Handles empty inputs for both resumes and job descriptions
Flags vague job descriptions with insufficient content
Detects noisy or meaningless text inputs and avoids misleading scores
Provides fallback behavior when API keys are missing
Cleans AI-generated output to remove formatting artifacts such as stray markdown symbols

Setup Instructions

Clone the repository
git clone https://github.com/your-username/your-repo.git
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

Screenshots
<img width="1920" height="880" alt="image" src="https://github.com/user-attachments/assets/1f3d3933-5b28-493c-a676-cf817a1559f3" />
<img width="1920" height="873" alt="image" src="https://github.com/user-attachments/assets/40027a9b-5c45-408c-809b-ebd96516a973" />
<img width="1918" height="705" alt="image" src="https://github.com/user-attachments/assets/73d8cedc-cc3e-46ba-a1fd-67527f2bb549" />
<img width="1920" height="304" alt="image" src="https://github.com/user-attachments/assets/66fa4b3c-99fa-4af1-82a8-04b3ed0ed384" />



Reflection

This project was developed using a Python-based stack with Streamlit for the user interface and various machine learning libraries for text processing and similarity analysis. Python was chosen due to its strong ecosystem for natural language processing and ease of rapid prototyping. SentenceTransformers was used to generate embeddings, enabling semantic comparison beyond simple keyword matching.

One of the biggest challenges encountered was ensuring that resume matching was meaningful and not based solely on keyword overlap. Initial approaches using basic text comparison produced inaccurate results, especially when similar concepts were expressed differently. This was addressed by incorporating embedding-based similarity using cosine distance, which significantly improved contextual understanding.

Another challenge was handling real-world variability in input data. Resumes often come in different formats, and some PDFs may not contain extractable text. Additionally, vague job descriptions or noisy inputs could lead to misleading results. To solve this, input validation and edge case handling were implemented to detect and manage such scenarios gracefully.

Balancing accuracy and performance was also an important consideration. While more advanced models could improve results, they would increase latency and complexity. A hybrid scoring system was chosen to maintain a balance between interpretability, efficiency, and effectiveness.

If more time were available, the system could be enhanced by integrating transformer-based models such as BERT for deeper semantic understanding and by introducing a vector database for scalable similarity search. Additional improvements could include a more advanced skill gap analysis, better UI visualization, and exporting ranked results for recruiter workflows.

