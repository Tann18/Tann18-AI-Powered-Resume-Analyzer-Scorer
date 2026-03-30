import streamlit as st
import pdfplumber
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from groq import Groq
import os
import re  # ADDED

# CONFIG
st.set_page_config(page_title="ResumeIQ", layout="wide")

# GLASS UI
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.header {
    font-size: 40px;
    font-weight: bold;
    color: white;
}
.glass {
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.1);
}
.tag {
    display: inline-block;
    padding: 8px 14px;
    margin: 6px;
    border-radius: 20px;
    background: linear-gradient(135deg, #00f2fe, #4facfe);
    color: black;
    font-weight: 500;
}
.section {
    font-size: 22px;
    font-weight: bold;
    margin-bottom: 10px;
    color: white;
}
.score {
    font-size: 32px;
    font-weight: bold;
    color: #00f2fe;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header"> ResumeIQ</div>', unsafe_allow_html=True)
st.write("AI-powered resume vs job description matcher")

# LOAD MODELS
nlp = spacy.load("en_core_web_sm")
embed_model = SentenceTransformer("paraphrase-MiniLM-L3-v2")

# SAFE API INIT
groq_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=groq_key) if groq_key else None

# ---------------- ADDED FUNCTIONS ---------------- #

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def is_garbage(text):
    words = text.split()
    if len(words) < 20:
        return True
    unique_ratio = len(set(words)) / (len(words) + 1)
    return unique_ratio < 0.3

# FUNCTIONS

def extract_text(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for p in pdf.pages:
                t = p.extract_text()
                if t:
                    text += t + " "
    except:
        return None

    text = clean_text(text)

    if not text:
        return None

    return text

def extract_skills(jd):
    jd = jd.lower()

    TECH = [
        "python","machine learning","deep learning","nlp",
        "sql","tensorflow","pytorch","aws","docker",
        "kubernetes","pandas","numpy","scikit-learn"
    ]

    SOFT = ["communication","teamwork","leadership"]

    tech_found = [t for t in TECH if t in jd]
    soft_found = [s for s in SOFT if s in jd]

    return {
        "Technical Skills": list(set(tech_found)),
        "Soft Skills": list(set(soft_found))
    }

# SCORING

def semantic_score(resume, jd):
    emb = embed_model.encode([resume, jd])
    return float(cosine_similarity([emb[0]], [emb[1]])[0][0])

def keyword_score(resume, jd):
    r = set(resume.lower().split())
    j = set(jd.lower().split())
    return len(r & j) / len(j) if j else 0

def skill_score(resume, skills):
    resume = resume.lower()
    all_skills = sum(skills.values(), [])

    if not all_skills:
        return 0

    score = 0
    for s in all_skills:
        if s in resume:
            score += 1
        elif any(w in resume for w in s.split()):
            score += 0.5

    return score / len(all_skills)

def final_score(resume, jd, skills):
    s1 = semantic_score(resume, jd)
    s2 = keyword_score(resume, jd)
    s3 = skill_score(resume, skills)

    return round((0.6*s1 + 0.2*s2 + 0.2*s3)*100, 2)

# AI FEEDBACK

def generate_feedback(resume, jd):

    if not groq_client:
        return "AI feedback unavailable (Missing API key)"

    prompt = f"""
You are a recruiter.

Return:

Strengths:
- ...
- ...

Weaknesses:
- ...
- ...

Resume:
{resume[:1200]}

JD:
{jd[:1200]}
"""
    try:
        res = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# INPUT

col1, col2 = st.columns(2)

with col1:
    resume_file = st.file_uploader(" Upload Resume", type="pdf")

with col2:
    jd_file = st.file_uploader(" Upload JD", type=["pdf","txt"])

# BULK UPLOAD (ADDED)
st.markdown("## Bulk Resume Upload (Shortlisting)")
bulk_files = st.file_uploader("Upload Multiple Resumes", type="pdf", accept_multiple_files=True)

# JD PROCESSING

jd_text = ""

if jd_file:
    if jd_file.type == "application/pdf":
        jd_text = extract_text(jd_file)
    else:
        jd_text = jd_file.read().decode("utf-8")

# ---------------- SINGLE ANALYSIS ---------------- #

if st.button(" Analyze Resume"):

    if not resume_file:
        st.error("Please upload a resume.")
        st.stop()

    if not jd_text:
        st.error("Invalid or empty job description.")
        st.stop()

    resume_text = extract_text(resume_file)

    if resume_text is None:
        st.error("Could not extract text from resume.")
        st.stop()

    if len(jd_text.split()) < 30:
        st.warning("Job description is too vague.")

    if is_garbage(resume_text):
        st.error("Resume content invalid.")
        st.stop()

    if is_garbage(jd_text):
        st.error("Job description invalid.")
        st.stop()

    skills = extract_skills(jd_text)
    score = final_score(resume_text, jd_text, skills)

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="section">Match Score</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="score">{score}%</div>', unsafe_allow_html=True)
    st.progress(score/100)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="section">Skills Breakdown</div>', unsafe_allow_html=True)

    for category, items in skills.items():
        if items:
            st.markdown(f"### {category}")
            row = ""
            for s in items:
                row += f"<span class='tag'>{s}</span>"
            st.markdown(row, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="section">AI Recruiter Analysis</div>', unsafe_allow_html=True)

    with st.spinner("Analyzing..."):
        feedback = generate_feedback(resume_text, jd_text)

    if "Strengths" in feedback:
        parts = feedback.split("Weaknesses")

        colA, colB = st.columns(2)

        with colA:
            st.markdown("### Strengths")
            st.write(parts[0].replace("Strengths:", "").strip())

        with colB:
            st.markdown("### Gaps")
            gaps = parts[1] if len(parts) > 1 else ""
            gaps = gaps.replace(":", "").replace("**", "").strip()
            st.write(gaps)
    else:
        st.write(feedback)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- BULK ANALYSIS ---------------- #

if st.button(" Bulk Analyze & Rank"):

    if not bulk_files:
        st.warning("Upload resumes")
        st.stop()

    if not jd_text:
        st.warning("Provide job description")
        st.stop()

    results = []

    for file in bulk_files:
        resume_text = extract_text(file)

        if resume_text is None or is_garbage(resume_text):
            continue

        skills = extract_skills(jd_text)
        score = final_score(resume_text, jd_text, skills)

        results.append({"name": file.name, "score": score})

    if not results:
        st.error("No valid resumes found.")
        st.stop()

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    st.markdown("## Ranked Shortlist")

    for i, r in enumerate(results, 1):
        st.markdown(f"**{i}. {r['name']} — {r['score']}%**")