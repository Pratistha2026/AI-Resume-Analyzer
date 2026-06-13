import streamlit as st
import pdfplumber
import time

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<div class="particle-bg"></div>
<div class="glow-bg"></div>

<style>
.stApp {
    background: linear-gradient(135deg, #000000 0%, #070707 45%, #180000 100%);
    color: white;
}

/* Visible moving glowing particles */
.particle-bg {
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    background-image:
        radial-gradient(circle, rgba(255,0,0,1) 2px, transparent 5px),
        radial-gradient(circle, rgba(255,90,90,0.85) 3px, transparent 7px),
        radial-gradient(circle, rgba(180,0,0,0.65) 2px, transparent 6px);
    background-size: 80px 80px, 130px 130px, 190px 190px;
    animation: moveParticles 15s linear infinite;
    filter: drop-shadow(0 0 10px red);
    opacity: 0.95;
}

/* Soft moving glow */
.glow-bg {
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    background:
        radial-gradient(circle at 20% 30%, rgba(255,0,0,0.22), transparent 25%),
        radial-gradient(circle at 80% 20%, rgba(180,0,0,0.18), transparent 28%),
        radial-gradient(circle at 50% 80%, rgba(255,40,40,0.16), transparent 30%);
    animation: glowPulse 5s ease-in-out infinite alternate;
}

@keyframes moveParticles {
    0% {
        background-position: 0 0, 0 0, 0 0;
    }
    100% {
        background-position: 350px 350px, -300px 250px, 250px -350px;
    }
}

@keyframes glowPulse {
    from {
        opacity: 0.45;
        filter: blur(0px);
    }
    to {
        opacity: 0.95;
        filter: blur(3px);
    }
}

/* Keep all Streamlit content above background */
.block-container,
section[data-testid="stSidebar"],
header,
main,
[data-testid="stAppViewContainer"] > .main {
    position: relative;
    z-index: 1;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #100000, #000000);
    border-right: 2px solid #7a0000;
}

.main-title {
    text-align: center;
    font-size: 52px;
    font-weight: 900;
    color: #f4f4f4;
    letter-spacing: 2px;
    text-shadow:
        0 0 8px rgba(255,0,0,0.7),
        0 0 18px rgba(255,0,0,0.45),
        0 0 30px rgba(120,0,0,0.35);
}

.subtitle {
    text-align: center;
    color: #cfcfcf;
    font-size: 19px;
    margin-bottom: 15px;
}

.project-tag {
    text-align: center;
    color: #f5f5f5;
    font-size: 16px;
    background: rgba(120, 0, 0, 0.22);
    padding: 12px;
    border-radius: 30px;
    border: 1px solid #8b0000;
    box-shadow: 0 0 12px rgba(120,0,0,0.45);
    margin-bottom: 25px;
}

.section-line {
    height: 2px;
    background: linear-gradient(90deg, transparent, #7a0000, #c23b3b, transparent);
    margin: 26px 0;
}

.stTextArea textarea {
    background-color: rgba(10, 10, 10, 0.92) !important;
    color: #ffffff !important;
    border: 2px solid #7a0000 !important;
    border-radius: 16px !important;
    box-shadow: 0 0 10px rgba(120,0,0,0.45) !important;
}

.stFileUploader {
    background: rgba(20, 0, 0, 0.65);
    border: 2px dashed #7a0000;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 0 10px rgba(120,0,0,0.35);
}

h1, h2, h3, p, label, div {
    color: white;
}

.skill-chip {
    display: inline-block;
    padding: 8px 14px;
    margin: 6px;
    border-radius: 20px;
    background: rgba(120, 0, 0, 0.25);
    border: 1px solid #9b1c1c;
    color: white;
    box-shadow: 0 0 8px rgba(120,0,0,0.45);
}

.job-chip {
    display: inline-block;
    padding: 8px 14px;
    margin: 6px;
    border-radius: 20px;
    background: rgba(70, 70, 70, 0.25);
    border: 1px solid #b33a3a;
    color: white;
    box-shadow: 0 0 8px rgba(120,0,0,0.35);
}

.missing-chip {
    display: inline-block;
    padding: 8px 14px;
    margin: 6px;
    border-radius: 20px;
    background: rgba(170, 0, 0, 0.25);
    border: 1px solid #b00000;
    color: white;
    box-shadow: 0 0 8px rgba(170,0,0,0.45);
}

.example-box {
    background: rgba(100, 0, 0, 0.18);
    border-left: 5px solid #8b0000;
    padding: 12px;
    border-radius: 12px;
    box-shadow: 0 0 10px rgba(120,0,0,0.35);
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

skills = [
    "python",
    "c",
    "machine learning",
    "artificial intelligence",
    "ai",
    "sql",
    "data analytics",
    "excel",
    "cyber security",
    "java",
    "html",
    "css",
    "javascript",
    "git",
    "github",
    "power bi",
    "tableau"
]

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in skills:
        if skill in text:
            found_skills.append(skill)

    return found_skills

st.sidebar.title("🤖 Project Info")
st.sidebar.write("👩‍💻 Created by Pratistha Singh")
st.sidebar.write("🎓 B.Tech CSE (AI & ML)")
st.sidebar.write("📄 Project: AI Resume Analyzer")
st.sidebar.write("⚫ Theme: Black + Dark Red AI")

st.markdown('<div class="main-title">🤖 AI Resume Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Smart ATS Score Checker using Python, NLP and Streamlit</div>', unsafe_allow_html=True)
st.markdown('<div class="project-tag">📄 Upload Resume → 🧠 Extract Skills → 🎯 Match Job Description → 📊 Generate ATS Score</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "📤 Upload your Resume PDF",
    type=["pdf"]
)

st.markdown("""
<div class="example-box">
<b>📝 Example Job Description:</b><br>
Looking for an AI Engineer with Python, Machine Learning, Artificial Intelligence, SQL, Data Analytics, Excel and Cyber Security skills.
</div>
""", unsafe_allow_html=True)

job_description = st.text_area(
    "📝 Paste Job Description Here",
    placeholder="Paste job description here..."
)

if uploaded_file is not None:
    with st.spinner("🧠 Analyzing resume using AI..."):
        time.sleep(1)

    text = ""

    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)
    st.subheader("📑 Extracted Resume Text")
    st.text_area("Resume Text", text, height=250)

    resume_skills = extract_skills(text)
    job_skills = extract_skills(job_description)

    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✅ Resume Skills")
        if resume_skills:
            for skill in resume_skills:
                st.markdown(f'<span class="skill-chip">✅ {skill}</span>', unsafe_allow_html=True)
        else:
            st.info("No skills found.")

    with col2:
        st.subheader("🎯 Job Skills")
        if job_skills:
            for skill in job_skills:
                st.markdown(f'<span class="job-chip">🎯 {skill}</span>', unsafe_allow_html=True)
        else:
            st.warning("Paste a job description to detect skills.")

    missing_skills = list(set(job_skills) - set(resume_skills))

    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)
    st.subheader("❌ Missing Skills")

    if missing_skills:
        for skill in missing_skills:
            st.markdown(f'<span class="missing-chip">❌ {skill}</span>', unsafe_allow_html=True)
    else:
        st.success("🎉 No missing skills found!")

    if len(job_skills) > 0:
        ats_score = ((len(job_skills) - len(missing_skills)) / len(job_skills)) * 100
    else:
        ats_score = 0

    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)
    st.subheader("📊 ATS Score")

    st.progress(int(ats_score))

    if ats_score >= 80:
        st.success(f"🌟 Excellent ATS Score: {ats_score:.2f}%")
    elif ats_score >= 50:
        st.warning(f"⚠️ Average ATS Score: {ats_score:.2f}%")
    else:
        st.error(f"🚫 Low ATS Score: {ats_score:.2f}%")

    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)
    st.subheader("💡 Resume Improvement Suggestions")

    if missing_skills:
        for skill in missing_skills:
            st.warning(f"Improve your resume by adding or learning: {skill}")
    else:
        st.success("🎉 Great! Your resume matches the job description well.")