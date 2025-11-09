# ------------------ SmartNotes AI App ------------------

!pip install streamlit pdfplumber google-generativeai --quiet

import streamlit as st
import pdfplumber
from io import StringIO
from textwrap import wrap
import google.generativeai as genai

# ----------- CONFIG -------------
API_KEY = "AIzaSyBjByrLrFQDC1EHCM1kpmf0zK32wl0qCEA"
genai.configure(api_key=API_KEY)

# ----------- PAGE SETTINGS -------------
st.set_page_config(page_title="SmartNotes AI", page_icon="🧠", layout="wide")

# ----------- THEME SELECTION -------------
theme = st.selectbox("Select Theme:", ["Warm Mode", "Dark Mode", "Neon Mode"])

if theme == "Dark Mode":
    bg_gradient = "linear-gradient(135deg,#1e1e2f,#2a2a3d)"
    text_color = "#f0f0f5"
    box_bg = "#2a2a3d"
    border_color = "#3c3c50"
    button_gradient = "linear-gradient(90deg,#4c6ef5,#15aabf)"
elif theme == "Neon Mode":
    bg_gradient = "linear-gradient(135deg,#0d0d0d,#1a1a1a)"
    text_color = "#00ffea"
    box_bg = "#1a1a1a"
    border_color = "#00ffea"
    button_gradient = "linear-gradient(90deg,#ff00ff,#00ffff)"
else:  # Warm Mode
    bg_gradient = "linear-gradient(135deg,#fdf4e6,#fff7dc)"
    text_color = "#1F2937"
    box_bg = "#ffffff"
    border_color = "#e5e7eb"
    button_gradient = "linear-gradient(90deg,#ff7f50,#ff6347)"

# ----------- DEVICE TYPE -------------
device_type = st.radio("Which device are you using?", ["Laptop/Desktop", "Mobile"], horizontal=True)
if device_type == "Mobile":
    textarea_height = 180
    font_size = "14px"
    padding_main = "10px"
else:
    textarea_height = 300
    font_size = "16px"
    padding_main = "20px"

# ----------- CSS STYLING -------------
css = f"""
<style>
.stApp {{
    background: {bg_gradient};
    font-family:'Inter',sans-serif;
    color:{text_color};
}}
.stTextArea textarea, .stFileUploader div, .stSelectbox div, .stRadio div {{
    border-radius:16px;
    background-color:{box_bg};
    border:1px solid {border_color};
    font-size:{font_size};
    padding:10px;
    color:{text_color} !important;
    box-shadow:none;
}}
.stRadio input[type=radio]:checked + label::before {{
    background-color:#ff6347;
}}
.stButton button {{
    background: {button_gradient};
    color:white;
    border:none;
    border-radius:16px;
    padding:0.8em 1.8em;
    font-weight:600;
    transition:0.3s;
}}
.stButton button:hover {{
    opacity:0.9; transform: scale(1.05);
}}
footer {{
    text-align:center;
    color:{text_color};
    margin-top:2em;
    font-size:13px;
}}
section.main {{padding:{padding_main};}}
</style>
"""
st.markdown(css, unsafe_allow_html=True)

# ----------- TITLE -------------
st.title("🧠 SmartNotes AI")
st.write("Paste text or upload PDFs to generate summaries, explanations, or quiz questions!")

# ----------- INPUT -------------
input_type = st.radio("Select input type:", ["Paste Text", "Upload PDF"])
text_input = ""
if input_type == "Paste Text":
    text_input = st.text_area("Paste your notes here:", height=textarea_height)
else:
    uploaded_file = st.file_uploader("Upload your PDF", type=["pdf"])
    if uploaded_file is not None:
        with pdfplumber.open(uploaded_file) as pdf:
            text_input = "\n".join(page.extract_text() or "" for page in pdf.pages)

# ----------- TASK SELECTION -------------
task = st.selectbox("Choose action:", ["Summarize Notes", "Explain Simply", "Generate Quiz"])

# ----------- GENERATE BUTTON -------------
if st.button("🚀 Generate"):
    if not text_input.strip():
        st.warning("Please enter some text first!")
    else:
        with st.spinner("Processing with AI..."):
            # Split text into chunks to avoid API errors
            max_chars = 2000
            chunks = wrap(text_input, max_chars)
            results = []
            for chunk in chunks:
                if task == "Summarize Notes":
                    prompt = "Summarize this text in clear bullet points:\n" + chunk
                elif task == "Explain Simply":
                    prompt = "Explain this text in simple language suitable for students:\n" + chunk
                else:
                    prompt = "Generate 5 quiz questions with answers based on this text:\n" + chunk
                response = genai.generate_text(model="text-bison-001", prompt=prompt)
                results.append(response.result)
            final_text = "\n".join(results)
            st.success("✅ Done!")
            st.markdown("### 🧾 Output:")
            st.write(final_text)
            output = StringIO(final_text)
            st.download_button("📥 Download Result", output.getvalue(), file_name="SmartNotes_Output.txt")

# ----------- FOOTER -------------
st.markdown("<footer>Made with 💜 by Aarav Katri</footer>", unsafe_allow_html=True)
