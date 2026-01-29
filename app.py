import streamlit as st
import os
import re
from datetime import datetime

# Konfiguration af siden
st.set_page_config(
    page_title="FileMaster Pro | Dark Mode",
    page_icon="🏗️",
    layout="centered"
)

# --- MODERN DARK THEME DESIGN ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
    /* Global Background */
    [data-testid="stAppViewContainer"] {
        background-color: #0f172a !important;
    }
    
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
    }

    * {
        font-family: 'Inter', sans-serif;
        color: #f8fafc !important;
    }

    /* Overskrifter */
    h1, .header-text {
        color: #f8fafc !important;
        font-weight: 800;
        font-size: 2.5rem;
        text-align: center;
        margin-bottom: 0px;
        padding-top: 40px;
        letter-spacing: -1px;
    }
    
    .subheader-text {
        color: #94a3b8 !important;
        text-align: center;
        margin-bottom: 40px;
        font-size: 1.1rem;
        font-weight: 400 !important;
    }

    /* Main Container / Card */
    .st-emotion-cache-1r6slb0, .main-card {
        background-color: #1e293b !important;
        padding: 40px !important;
        border-radius: 24px !important;
        box-shadow: 0 20px 50px rgba(0,0,0,0.3) !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
    }

    /* Input Felter styling */
    input, select, textarea, [data-baseweb="select"] {
        background-color: #0f172a !important;
        color: white !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }

    /* Labels */
    label, .stMarkdown p {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        margin-bottom: 8px !important;
    }

    /* Preview Boks - DARK STYLE */
    .preview-card {
        background-color: #0f172a;
        border: 2px dashed #38bdf8;
        border-radius: 16px;
        padding: 30px;
        margin: 30px 0;
        text-align: center;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.5);
    }
    
    .preview-label {
        font-size: 0.75rem !important;
        color: #38bdf8 !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 12px;
        font-weight: 700 !important;
    }
    
    .preview-filename {
        color: #f1f5f9 !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        word-break: break-all;
        font-family: 'Courier New', monospace;
    }

    /* Premium Button - GLOW EFFECT */
    div.stButton > button {
        background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%) !important;
        color: white !important;
        border: none !important;
        padding: 18px 30px !important;
        border-radius: 12px !important;
        font-weight: 800 !important;
        width: 100% !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.2) !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(56, 189, 248, 0.4) !important;
        filter: brightness(1.1);
    }

    /* File Uploader - DARK */
    [data-testid="stFileUploader"] section {
        border: 2px dashed #334155 !important;
        background-color: #0f172a !important;
        border-radius: 16px !important;
    }
    
    [data-testid="stFileUploader"] div {
        color: #94a3b8 !important;
    }
    
    /* Skjul Streamlit menu for renere look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

def sanitize_filename(text):
    """Sanerer input for at undgå ulovlige tegn."""
    if not text:
        return ""
    return re.sub(r'[\\/*?:"<>|]', "-", text)

def main():
    # Logo / Header
    st.markdown('<h1 class="header-text">FileMaster Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subheader-text">Professionel navngivning til byggebranchen</p>', unsafe_allow_html=True)

    # Main UI
    uploaded_file = st.file_uploader("Upload din fil her", type=None)

    if uploaded_file:
        file_name, file_extension = os.path.splitext(uploaded_file.name)
        default_date = datetime.now().date()

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Formular i mørke kolonner
        col1, col2 = st.columns(2)
        
        with col1:
            selected_date = st.date_input("🗓️ Vælg Dato", value=default_date)
            subject = st.text_input("📝 Emne (Subject)", placeholder="f.eks. SAT Protokol")
        
        with col2:
            categories = ["KONTRAKT", "DESIGN", "ADMIN", "VENT", "SCOPE", "KORRESPONDANCE"]
            category = st.selectbox("🏷️ Vælg Kategori", options=categories)
            detail = st.text_input("🔍 Specifikke detaljer", placeholder="f.eks. Version 20")

        # Navne-generering logik
        clean_subject = sanitize_filename(subject)
        clean_detail = sanitize_filename(detail)
        date_str = selected_date.strftime("%Y-%m-%d")
        
        parts = [date_str, category]
        if clean_subject: parts.append(clean_subject)
        if clean_detail: parts.append(clean_detail)
        
        new_filename = " - ".join(parts) + file_extension

        # Preview Boks (Dark Mode)
        st.markdown(f"""
            <div class="preview-card">
                <div class="preview-label">Standardiseret filnavn</div>
                <div class="preview-filename">{new_filename}</div>
            </div>
        """, unsafe_allow_html=True)

        # Download Knap med Glow
        st.download_button(
            label="Download omdøbt fil",
            data=uploaded_file.getvalue(),
            file_name=new_filename,
            mime=uploaded_file.type,
            use_container_width=True
        )
        
    else:
        # Hero / Empty State
        st.markdown("""
            <div style="text-align: center; border: 1px solid #334155; border-radius: 20px; padding: 60px; background-color: #1e293b;">
                <h3 style="color: #f8fafc; font-weight: 700;">Klar til at omdøbe?</h3>
                <p style="color: #94a3b8;">Upload en fil for at komme i gang med din byggesag.</p>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
