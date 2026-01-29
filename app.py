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
    /* Stop Streamlit farve-styring og tving design */
    [data-testid="stAppViewContainer"] {
        background-color: #f1f3f6;
    }
    
    * {
        font-family: 'Inter', sans-serif;
    }

    /* Overskrifter og tekst farver - TVUNGET */
    h1, .header-text {
        color: #1a202c !important;
        font-weight: 800;
        font-size: 2.2rem;
        text-align: center;
        margin-bottom: 5px;
        padding-top: 20px;
    }
    
    .subheader-text {
        color: #4a5568 !important;
        text-align: center;
        margin-bottom: 30px;
        font-size: 1.1rem;
    }

    /* Container Box */
    .st-emotion-cache-1r6slb0, .main-card {
        background-color: white !important;
        padding: 40px !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important;
        color: #2d3748 !important;
    }

    /* Labels - TVUNGET SORT/GRÅ */
    label, p, span, .stMarkdown {
        color: #2d3748 !important;
        font-weight: 600 !important;
    }

    /* Preview Boks */
    .preview-card {
        background-color: #f8fafc;
        border: 2px dashed #3182ce;
        border-radius: 12px;
        padding: 25px;
        margin: 25px 0;
        text-align: center;
    }
    
    .preview-label {
        font-size: 0.75rem !important;
        color: #718096 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    
    .preview-filename {
        color: #2c5282 !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        word-break: break-all;
    }

    /* Knap */
    div.stButton > button {
        background: linear-gradient(135deg, #3182ce 0%, #2c5282 100%) !important;
        color: white !important;
        border: none !important;
        padding: 15px 30px !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        width: 100% !important;
        text-transform: uppercase;
    }

    /* File Uploader styling */
    [data-testid="stFileUploader"] section {
        border: 2px dashed #3182ce !important;
        background-color: #ebf8ff !important;
    }
    
    [data-testid="stFileUploader"] label {
        color: #2b6cb0 !important;
    }
    </style>
""", unsafe_allow_html=True)

def sanitize_filename(text):
    """Sanerer input for at undgå ulovlige tegn."""
    if not text:
        return ""
    return re.sub(r'[\\/*?:"<>|]', "-", text)

def main():
    # Header indpakket i HTML for at undgå markdown fejl
    st.markdown('<h1 class="header-text">FileMaster Pro</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subheader-text">Standardiseret navngivning til dine byggesager</p>', unsafe_allow_html=True)

    # Main UI
    uploaded_file = st.file_uploader("Træk og slip en fil her", type=None)

    if uploaded_file:
        file_name, file_extension = os.path.splitext(uploaded_file.name)
        default_date = datetime.now().date()

        st.markdown("<br>", unsafe_allow_html=True)
        
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
        # Tip tekst gemt hvis ingen fil er valgt
        st.markdown("""
            <div style="text-align: center; color: #718096; padding: 40px; font-style: italic;">
                Tip: Upload filen først for at se navne-generatoren.
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
