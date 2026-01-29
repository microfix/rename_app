import streamlit as st
import os
import re
from datetime import datetime

# Konfiguration af siden
st.set_page_config(
    page_title="FileMaster Pro | Byggesag",
    page_icon="🏗️",
    layout="centered"
)

# --- PREMIUM DESIGN SYSTEM ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
    /* Global Styles */
    .stApp {
        background-color: #f1f3f6;
    }
    
    * {
        font-family: 'Inter', sans-serif;
    }

    /* Main Container */
    .main-container {
        background-color: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-top: 20px;
    }

    /* Header */
    .header-text {
        color: #1a202c;
        font-weight: 800;
        font-size: 2.2rem;
        margin-bottom: 5px;
        text-align: center;
    }
    
    .subheader-text {
        color: #718096;
        text-align: center;
        margin-bottom: 30px;
    }

    /* Input Labels */
    .stMarkdown p {
        font-weight: 600;
        color: #2d3748;
    }

    /* Preview Box */
    .preview-card {
        background-color: #f8fafc;
        border: 2px dashed #cbd5e0;
        border-radius: 12px;
        padding: 20px;
        margin: 25px 0;
        text-align: center;
    }
    
    .preview-label {
        font-size: 0.8rem;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
    }
    
    .preview-filename {
        color: #2b6cb0;
        font-size: 1.1rem;
        font-weight: 600;
        word-break: break-all;
    }

    /* Custom Button */
    div.stButton > button {
        background: linear-gradient(135deg, #3182ce 0%, #2c5282 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 10px;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(49, 130, 206, 0.4);
        background: linear-gradient(135deg, #4299e1 0%, #2b6cb0 100%);
    }

    /* File Uploader styling */
    .stFileUploader section {
        border-radius: 12px;
        border: 2px dashed #3182ce !important;
        background-color: #ebf8ff;
    }
    </style>
""", unsafe_allow_html=True)

def sanitize_filename(text):
    """Sanerer input for at undgå ulovlige tegn."""
    if not text:
        return ""
    # Erstat / \ : * ? " < > | med -
    return re.sub(r'[\\/*?:"<>|]', "-", text)

def main():
    # Header
    st.markdown('<h1 class="header-text">FileMaster Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subheader-text">Standardiseret navngivning til dine byggesager</p>', unsafe_allow_html=True)

    # Main Card
    with st.container():
        # 1. File Upload
        uploaded_file = st.file_uploader("Træk og slip en fil her", type=None)

        if uploaded_file:
            # Metadata logik
            file_name, file_extension = os.path.splitext(uploaded_file.name)
            default_date = datetime.now().date()

            st.markdown("---")
            
            # Formular i kolonner
            col1, col2 = st.columns(2)
            
            with col1:
                selected_date = st.date_input("🗓️ Dato", value=default_date)
                subject = st.text_input("📝 Emne (Subject)", placeholder="f.eks. SAT Protokol")
            
            with col2:
                categories = ["KONTRAKT", "DESIGN", "ADMIN", "VENT", "SCOPE", "KORRESPONDANCE"]
                category = st.selectbox("🏷️ Kategori", options=categories)
                detail = st.text_input("🔍 Detaljer (Detail)", placeholder="f.eks. Version 20")

            # Navne-generering
            clean_subject = sanitize_filename(subject)
            clean_detail = sanitize_filename(detail)
            date_str = selected_date.strftime("%Y-%m-%d")
            
            parts = [date_str, category]
            if clean_subject: parts.append(clean_subject)
            if clean_detail: parts.append(clean_detail)
            
            new_filename = " - ".join(parts) + file_extension

            # Preview Boks
            st.markdown(f"""
                <div class="preview-card">
                    <div class="preview-label">Nyt filnavn preview</div>
                    <div class="preview-filename">{new_filename}</div>
                </div>
            """, unsafe_allow_html=True)

            # Download Knap
            st.download_button(
                label="Omdøb og download fil",
                data=uploaded_file.getvalue(),
                file_name=new_filename,
                mime=uploaded_file.type,
                use_container_width=True
            )
            
        else:
            # Empty state
            st.markdown("""
                <div style="text-align: center; color: #a0aec0; padding: 40px;">
                    <p>Hurtigt tip: Upload filen først, derefter kan du redigere navnet.</p>
                </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
