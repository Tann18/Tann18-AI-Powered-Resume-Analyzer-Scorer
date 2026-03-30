# Tann18-AI-Powered-Resume-Analyzer-Scorer

Problem Statement

Recruiters receive thousands of resumes and need a fast, unbiased way to evaluate candidates against job descriptions. Manual screening is time-consuming and inconsistent.

This project solves that by building an AI system that:

.Parses resumes
.Compares them with job descriptions
.Generates a match score and feedback

Approach
1.Extract text from resume (PDF parsing)
2.Clean and preprocess text
3.Compare with job description using NLP techniques
4.Compute similarity score
5.Generate improvement suggestions

Architecture

Simple Version (write this if no diagram):

User Input (Resume + JD)
        ↓
Text Extraction (PDF Parser)
        ↓
Preprocessing (Cleaning + Tokenization)
        ↓
Similarity Engine (TF-IDF / Embeddings)
        ↓
Score + Feedback Generator
        ↓
Output UI

Setup Instructions
Clone repo
git clone https://github.com/your-username/your-repo.git

Navigate
cd your-repo

Install dependencies
pip install -r requirements.txt

Run app
python app.py
Environment Variables

Create a .env file using:

OPENAI_API_KEY=your_key_here
HUGGINGFACE_API_KEY=your_key_here

<img width="1920" height="878" alt="image" src="https://github.com/user-attachments/assets/b54555d1-4d1a-408f-9e0b-79bcff50c192" />
<img width="1920" height="861" alt="image" src="https://github.com/user-attachments/assets/f7dfe04b-38f9-4031-be9d-e8684b4430f7" />

Dependencies

flask
numpy
pandas
scikit-learn
python-dotenv
PyPDF2

.env.example file
OPENAI_API_KEY=your_openai_api_key
HUGGINGFACE_API_KEY=your_huggingface_api_key

Reflection 
This project was built using a Python-based tech stack, primarily leveraging Flask for the backend and libraries such as scikit-learn and PyPDF2 for processing and analysis. I chose Python because of its strong ecosystem for machine learning and natural language processing, which made it efficient to implement similarity scoring and text analysis. Flask was selected for its simplicity and lightweight nature, allowing rapid prototyping and deployment without unnecessary complexity.

One of the biggest challenges I encountered was accurately comparing resumes with job descriptions in a meaningful way. Initially, simple keyword matching produced poor and inconsistent results, as it failed to capture contextual relevance. To address this, I implemented a more robust approach using TF-IDF vectorization and cosine similarity, which significantly improved the quality of matching. Additionally, handling different resume formats and ensuring reliable text extraction from PDFs required careful preprocessing and error handling.

Another challenge was balancing performance with accuracy. More advanced NLP models could have improved results further, but they also introduced latency and dependency complexity. I had to make trade-offs to ensure the system remained fast, responsive, and easy to run locally.

If I had more time, I would enhance the system by integrating transformer-based models such as BERT to improve semantic understanding. This would allow the system to better interpret nuanced skills and experiences rather than relying primarily on statistical similarity. I would also improve the user interface to make the feedback more interactive and visually appealing, as well as add features such as resume rewriting suggestions and job-specific optimization tips.

Overall, this project helped me understand the practical challenges of applying AI to real-world problems, particularly in terms of data variability, system design, and performance trade-offs. It reinforced the importance of choosing the right level of complexity for a given problem while maintaining scalability and usability.
