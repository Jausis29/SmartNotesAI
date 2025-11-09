import streamlit as st
import pdfplumber
from google.generativeai import TextGenerationClient

# ---------- CONFIG ----------
st.set_page_config(page_title="SmartNotes AI", layout="wide")

# Your Gemini API Key
API_KEY = "AIzaSyBjByrLrFQDC1EHCM1kpmf0zK32wl0qCEA"
client = TextGenerationClient(api_key=API_KEY)

# ---------- CUSTOM CSS ----------
st.markdown("""
<style>
/* Container padding and background */
main .block-container{
    padding: 2rem 3rem;
    background-color: #FFF8F0;
}

/* Rounded input boxes */
.stTextArea, .stTextInput, .stFileUploader {
    border-radius: 12px;
    border: 1px solid #DDD;
    padding: 10px;
    font-size: 16px;
}

/* Radio buttons styling */
[data-baseweb="radio"] label {
    display: flex;
    align-items: center;
    font-size: 16px;
    margin-bottom: 10px;
}
[data-baseweb="radio"] input[type="radio"]:checked + div > div {
    background-color: #FF6F61 !important;
    border-color: #FF6F61 !important;
}

/* Generate button */
.stButton>button {
    border-radius: 12px;
    padding: 10px 20px;
    background-color: #FF6F61;
    color: white;
    font-size: 16px;
    font-weight: bold;
}

/* Footer styling */
.footer {
    text-align: center;
    margin-top: 50px;
    font-size: 14px;
    color: #555;
}
</style>
""", unsafe_allow_html=True)

# ---------- THEME SELECTION ----------
theme = st.radio("Select Theme Mode:", ["Warm Mode", "Dark Mode", "Neon Mode"])
if theme == "Warm Mode":
    st.markdown("<style>body {background-color: #FFF8F0; color: #333;}</style>", unsafe_allow_html=True)
elif theme == "Dark Mode":
    st.markdown("<style>body {background-color: #121212; color: #EEE;}</style>", unsafe_allow_html=True)
elif theme == "Neon Mode":
    st.markdown("<style>body {background-color: #0A0A0A; color: #39FF14;}</style>", unsafe_allow_html=True)

# ---------- INPUT ----------
st.title("SmartNotes AI")
input_type = st.radio("Choose your input:", ["Paste Text", "Upload PDF"])
user_input = ""

if input_type == "Paste Text":
    user_input = st.text_area("Paste your text here:", height=200)
elif input_type == "Upload PDF":
    uploaded_file = st.file_uploader("Upload PDF file:", type=["pdf"])
    if uploaded_file is not None:
        with pdfplumber.open(uploaded_file) as pdf:
            text_pages = [page.extract_text() for page in pdf.pages]
            user_input = "\n".join(text_pages)

# ---------- GENERATE BUTTON ----------
if st.button("Generate Notes / Summary / Quiz"):
    if user_input.strip() == "":
        st.warning("Please provide text or upload a PDF first!")
    else:
        with st.spinner("Generating content with AI..."):
            response = client.generate_text(
                model="text-bison-001",
                prompt=f"Generate concise notes, summary, and quiz questions from this content:\n\n{user_input}",
                max_output_tokens=1024
            )
            st.subheader("Generated Notes / Summary / Quiz")
            st.write(response.text)

# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
Made with ❤️ by Aarav Katri
</div>
""", unsafe_allow_html=True)
