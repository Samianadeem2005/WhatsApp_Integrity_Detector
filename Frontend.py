import streamlit as st
import base64
import time


def run_ui():
    # ==========================================
    # 1. PAGE CONFIGURATION & SESSION STATE
    # ==========================================
    st.set_page_config(
        page_title="WhatsTrue - Confidence with Every Connection", 
        page_icon="💚", 
        layout="wide", 
        initial_sidebar_state="collapsed"
    )

    # PAGE ROUTING
    if "page" in st.query_params:
        current_page = st.query_params["page"]
    else:
        current_page = "home"

    if 'search_state' not in st.session_state:
        st.session_state.search_state = 'idle'

    def get_base64_video(path):
        try:
            with open(path, "rb") as file:
                return base64.b64encode(file.read()).decode()
        except:
            return None

    def get_base64_image(path):
        try:
            with open(path, "rb") as file:
                return base64.b64encode(file.read()).decode()
        except:
            return None

    # Yahan logo image ko base64 mein convert kar rahay hain
    logo_b64 = get_base64_image("Assets/Logo.png")
    bg_image_base64 = get_base64_image("Assets/bg.jpg")

    # ==========================================
    # 2. FULL PIXEL-PERFECT "ULTRA PRO" CSS STYLING
    # ==========================================
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">

    <style>
    /* Smooth Scrolling for the entire app */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        scroll-behavior: smooth !important;
    }

    /* Scroll Margin for anchor links to not hide behind fixed navbar */
    #protect, #business, #blog, #premium {
        scroll-margin-top: 110px;
    }

    header[data-testid="stHeader"] {display: none;}
    /* Added padding-top so content doesn't hide behind fixed navbar */
    .block-container {padding-top: 100px !important; padding-bottom: 0 !important; max-width: 100% !important; padding-left: 0 !important; padding-right: 0 !important;}

    /* Modern Soft Background */
    .stApp { 
        background-color: #f8fafc !important; 
        font-family: 'Nunito', sans-serif !important; 
    }

    /* --- WHATSTRUE HEADER (For Scanner Page) --- */
    .whatstrue-header {
        background-color: #ffffff;
        padding: 18px 40px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.03), 0 1px 2px rgba(15, 23, 42, 0.02);
        display: flex;
        align-items: center;
        gap: 10px;
        border-bottom: 1px solid #f1f5f9;
        cursor: pointer;
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 99999;
    }
    .whatstrue-logo {
        color: #0CD25F;
        font-weight: 900;
        font-size: 26px;
        letter-spacing: -1.2px;
    }
    .whatstrue-header img {
        height: 35px;
        mix-blend-mode: multiply; /* <-- Is se yahan bhi box khatam ho jayega */
    }

    /* --- Navbar Styling (Now Sticky/Fixed) --- */
    .navbar { 
        padding: 15px 40px; 
        background-color: rgba(255, 255, 255, 0.95); max-width: 100%; margin: 0 auto;
        display: flex; justify-content: space-between; align-items: center;
        backdrop-filter: blur(12px);
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 99999;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    /* --- Navbar Logo Alignment and Blend Mode --- */
    .navbar-logo { 
        display: flex; 
        align-items: center; 
    }
    .navbar-logo img { 
        height: 55px; 
        mix-blend-mode: multiply; /* <-- Is se white background transparent ho jayega */
    }

    .navbar-links { 
        display: flex; gap: 40px; font-weight: 800; font-size: 22px; 
        position: absolute; left: 50%; transform: translateX(-50%); 
    }
    .navbar-links a { text-decoration: none !important; color: #1e293b !important; transition: all 0.2s ease-in-out; }
    .navbar-links a:hover { color: #0CD25F !important; transform: translateY(-2px); }

    /* --- Hero Wrapper --- */
    .hero-wrapper {
        position: relative; width: 95%; max-width: 1350px; height: 560px;
        margin: 0px auto 20px auto; 
        border-radius: 30px; overflow: hidden;
        box-shadow: 0 20px 50px rgba(0,0,0,0.15);
    }
    .hero-video-bg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: 1; }
    .hero-overlay { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.3); z-index: 2; }
    .hero-content-overlay { 
        position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 3; 
        display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; 
    }
    .exact-hero-title { color: #ffffff !important; font-family: 'Nunito', sans-serif; font-size: 72px; font-weight: 800; line-height: 1.1; margin-bottom: 35px; letter-spacing: -1px;}

    .btn-green-exact {
        background-color: #0CD25F !important; color: white !important; font-family: 'Nunito', sans-serif !important;
        font-size: 18px !important; font-weight: 800 !important; padding: 18px 42px !important;
        border-radius: 100px !important; border: none !important; cursor: pointer !important; text-decoration: none !important; display: inline-block; 
        transition: all 0.3s ease !important; box-shadow: 0 10px 25px rgba(12, 210, 95, 0.4);
    }
    .btn-green-exact:hover { background-color: #0ab552 !important; transform: translateY(-4px) !important; box-shadow: 0 15px 35px rgba(12, 210, 95, 0.6); }

    /* =========================================
    PROTECT & DETECT SECTIONS
    ========================================= */
    .protect-section, .detect-section {
        max-width: 1200px;
        margin: 100px auto;
        padding: 0 40px;
        display: flex;
        align-items: center;
        gap: 60px;
        justify-content: space-between;
    }
    .protect-left, .detect-right {
        flex: 1;
        max-width: 500px;
    }
    .protect-right, .detect-left {
        flex: 1.2;
        display: flex;
    }
    .protect-right { justify-content: flex-end; }
    .detect-left { justify-content: flex-start; }

    .protect-right img, .detect-left img {
        max-width: 100%;
        height: auto;
    }
    .detect-left img {
        border-radius: 20px;
    }

    .section-subtitle {
        font-weight: 800;
        font-size: 16px;
        margin-bottom: 12px;
        font-family: 'Nunito', sans-serif;
    }
    .subtitle-pink { color: #F53F90; }
    .subtitle-green { color: #019D91; }

    .section-title {
        color: #1e293b;
        font-size: 52px;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 40px;
        font-family: 'Nunito', sans-serif;
        letter-spacing: -1px;
    }
    .feature-bullet {
        display: flex;
        align-items: flex-start;
        gap: 16px;
        margin-bottom: 24px;
    }
    .feature-bullet-icon {
        width: 48px;
        height: 48px;
        flex-shrink: 0;
    }
    .feature-bullet-text {
        font-size: 18px;
        font-weight: 500;
        color: #334155;
        font-family: 'Nunito', sans-serif;
        line-height: 1.5;
        margin-top: 10px;
    }
    .feature-bullet-text strong {
        color: #1e293b;
        font-weight: 800;
    }

    .btn-detect {
        background-color: #0CD25F !important; color: white !important; font-family: 'Nunito', sans-serif !important;
        font-size: 18px !important; font-weight: 800 !important; padding: 16px 36px !important;
        border-radius: 100px !important; border: none !important; cursor: pointer !important; text-decoration: none !important; display: inline-block; 
        transition: all 0.3s ease !important; box-shadow: 0 10px 25px rgba(12, 210, 95, 0.4);
        margin-top: 10px;
    }
    .btn-detect:hover { background-color: #0ab552 !important; transform: translateY(-4px) !important; box-shadow: 0 15px 35px rgba(12, 210, 95, 0.6); }

    @media (max-width: 900px) {
        .protect-section, .detect-section {
            flex-direction: column;
            text-align: left;
        }
        .protect-right, .detect-left {
            justify-content: center;
            margin-top: 30px;
        }
        .detect-section { flex-direction: column-reverse; } /* Keeps image at bottom on mobile */
    }

    /* =========================================
    NEW: TESTIMONIALS & TRUSTED SECTION
    ========================================= */
    .testimonial-wrapper {
        background-color: #0CD25F;
        border-radius: 40px;
        padding: 60px 40px 0px 40px;
        text-align: center;
        margin: 60px auto;
        max-width: 1200px;
        position: relative;
        overflow: hidden;
    }
    .testi-header { color: white; font-weight: 800; font-size: 16px; margin-bottom: 10px; font-family: 'Nunito', sans-serif;}
    .testi-title { color: #1e293b; font-size: 42px; font-weight: 900; margin-bottom: 50px; letter-spacing: -1px; font-family: 'Nunito', sans-serif;}
    .testi-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        position: relative;
        z-index: 2;
        margin-bottom: 50px;
    }
    .testi-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        text-align: left;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .testi-user { display: flex; align-items: center; gap: 15px; margin-bottom: 15px; }
    .testi-avatar { width: 50px; height: 50px; border-radius: 50%; object-fit: cover; }
    .testi-name { font-weight: 800; color: #1e293b; font-size: 16px; font-family: 'Nunito', sans-serif;}
    .testi-country { color: #94a3b8; font-size: 13px; font-weight: 600; font-family: 'Nunito', sans-serif;}
    .testi-text { color: #475569; font-size: 14px; font-weight: 600; line-height: 1.5; font-family: 'Nunito', sans-serif;}

    .testi-stats-title { color: #1e293b; font-size: 28px; font-weight: 800; margin-bottom: 30px; position: relative; z-index: 2; font-family: 'Nunito', sans-serif;}
    .testi-stats-grid {
        display: flex;
        justify-content: center;
        gap: 80px;
        position: relative;
        z-index: 2;
        margin-bottom: 20px;
    }
    .testi-stat-val { font-size: 64px; font-weight: 900; color: white; line-height: 1; font-family: 'Nunito', sans-serif;}
    .testi-stat-label { font-size: 12px; font-weight: 800; color: #1e293b; text-transform: uppercase; letter-spacing: 1px; margin-top: 10px; font-family: 'Nunito', sans-serif;}
    .globe-img { width: 100%; max-width: 1000px; margin: 0 auto; display: block; position: relative; z-index: 1; margin-top: -50px; }

    /* =========================================
    NEW: MARQUEE (TRUSTED BY)
    ========================================= */
    .trusted-container {
        max-width: 1200px;
        margin: 80px auto 40px auto;
        display: flex;
        align-items: center;
        overflow: hidden;
        padding: 0 40px;
    }
    .trusted-label {
        font-size: 18px;
        font-weight: 800;
        color: #1e293b;
        margin-right: 40px;
        white-space: nowrap;
        font-family: 'Nunito', sans-serif;
    }
    .marquee-wrapper {
        overflow: hidden;
        width: 100%;
        display: flex;
    }
    .marquee-track {
        display: flex;
        align-items: center;
        gap: 60px;
        animation: scroll-left 25s linear infinite;
        white-space: nowrap;
    }
    .marquee-logo { height: 45px; object-fit: contain; }

    @keyframes scroll-left { 
        0% { transform: translateX(0); } 
        100% { transform: translateX(-50%); } 
    }

    /* =========================================
    NEW: UNLOCK THE POWER (GRADIENT SAAS SECTION)
    ========================================= */
    .power-section {
        background: linear-gradient(135deg, #751AFF 0%, #0CD25F 100%);
        border-radius: 40px;
        padding: 60px 40px;
        text-align: center;
        max-width: 1200px;
        margin: 60px auto;
        color: white;
        font-family: 'Nunito', sans-serif;
    }
    .power-title { font-size: 42px; font-weight: 800; margin-bottom: 40px; letter-spacing: -1px; }
    .power-stats { display: flex; justify-content: center; align-items: center; gap: 40px; margin-bottom: 50px; }
    .power-stat-item { display: flex; align-items: center; gap: 10px; }
    .power-val { font-size: 42px; font-weight: 900; }
    .power-label { font-size: 14px; font-weight: 600; text-align: left; line-height: 1.2; }

    .power-cards {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: 20px;
        margin-bottom: 50px;
    }
    .power-card {
        background: white;
        border-radius: 20px;
        padding: 30px 15px;
        text-align: center;
        color: #1e293b;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .power-card:hover { transform: translateY(-5px); }
    .power-icon { font-size: 32px; margin-bottom: 15px; } /* Using Emojis for clean SVGs */
    .power-card-title { font-size: 15px; font-weight: 800; line-height: 1.3; }

    .btn-white {
        background-color: white !important; color: #0CD25F !important; font-family: 'Nunito', sans-serif !important;
        font-size: 16px !important; font-weight: 800 !important; padding: 16px 36px !important;
        border-radius: 100px !important; text-decoration: none !important; display: inline-block; 
        transition: all 0.3s ease !important;
    }
    .btn-white:hover { transform: translateY(-4px) !important; box-shadow: 0 10px 20px rgba(0,0,0,0.1); }

    @media (max-width: 900px) {
        .testi-grid { grid-template-columns: 1fr; } 
        .testi-stats-grid { flex-direction: column; gap: 30px; }
        .power-cards { grid-template-columns: repeat(2, 1fr); }
        .power-stats { flex-direction: column; gap: 20px; }
        .trusted-container { flex-direction: column; align-items: flex-start; gap: 20px; }
    }

    /* =========================================
    SCANNER PAGE CSS
    ========================================= */
    
    .scanner-page-title {
        font-size: 48px; font-weight: 900; text-align: center; 
        margin-top: 30px; margin-bottom: 50px; font-family: 'Nunito', sans-serif; letter-spacing: -1.5px;
        color: #0f172a; 
    }

    .custom-label { font-size: 18px; font-weight: 800; color: #1e293b !important; font-family: 'Nunito', sans-serif; margin-bottom: 2px; }
    .custom-sublabel { font-size: 13px; color: #64748b !important; font-weight: 600; font-family: 'Nunito', sans-serif; margin-bottom: 12px; }

    /* Force Pure White Background on Input Containers */
    div[data-baseweb="input"], 
    div[data-baseweb="textarea"],
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02) !important;
    }

    div[data-baseweb="select"], 
    div[data-baseweb="select"] > div, 
    div[data-baseweb="select"] * {
        cursor: pointer !important;
    }

    div[data-baseweb="input"] *, 
    div[data-baseweb="textarea"] *,
    div[data-baseweb="select"] * {
        background-color: transparent !important;
        color: #1e293b !important;
        -webkit-text-fill-color: #1e293b !important;
    }

    .stTextInput input, .stTextArea textarea {
        font-family: 'Nunito', sans-serif !important;
        font-size: 16px !important; 
        font-weight: 600 !important;
        padding: 14px 20px !important;
        outline: none !important;
        border: none !important;
        caret-color: #1e293b !important; 
    }
    .stTextArea textarea { padding: 20px !important; border-radius: 12px !important; }

    div[data-baseweb="input"]:focus-within, 
    div[data-baseweb="textarea"]:focus-within,
    div[data-baseweb="select"]:focus-within > div {
        border-color: #0CD25F !important;
        box-shadow: 0 0 0 4px rgba(12, 210, 95, 0.08) !important;
        background-color: #ffffff !important;
    }

    div[data-testid="InputInstructions"] { display: none !important; }

    /* Centered Glowing Initiate Button */
    button[kind="primary"] {
        background: linear-gradient(135deg, #0CD25F 0%, #059669 100%) !important; 
        color: white !important; border-radius: 100px !important; 
        padding: 14px 0 !important; font-size: 18px !important; font-weight: 800 !important;
        width: 100% !important; margin-top: 25px !important;
        box-shadow: 0 10px 25px rgba(12, 210, 95, 0.25) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important; border: none !important;
        letter-spacing: 0.5px; text-transform: uppercase; cursor: pointer !important;
    }
    button[kind="primary"]:hover { 
        transform: translateY(-3px) !important; 
        box-shadow: 0 15px 30px rgba(12, 210, 95, 0.35) !important; 
    }
    button[kind="primary"] * { color: white !important; }

    .detected-region { 
        font-size: 14px; font-weight: 800; margin-top: 16px; margin-bottom: 16px; 
        display: inline-flex; align-items: center; gap: 6px; 
        background: #f0fdf4; 
        color: #166534 !important; padding: 10px 20px; border-radius: 100px; 
        border: 1px solid #bbf7d0; box-shadow: 0 2px 8px rgba(74, 222, 128, 0.08);
    }

    /* Fancy Error Alert */
    .fancy-error {
        background: #fff1f2;
        border: 1px solid #fecdd3; border-left: 6px solid #e11d48;
        padding: 18px 22px; border-radius: 12px; margin-top: 20px;
        box-shadow: 0 4px 15px rgba(225, 29, 72, 0.05);
    }

    /* =========================================
    PREMIUM SCANNING INTERFACE STYLING
    ========================================= */
    
    .progress-box { 
        background-color: #ffffff !important; 
        border: 1px solid #e2e8f0 !important; 
        padding: 45px !important; 
        border-radius: 20px !important; 
        margin-top: 15px !important; 
        margin-bottom: 25px !important; 
        box-shadow: 0 10px 30px rgba(0,0,0,0.02) !important; 
        text-align: center !important; 
    }

    .progress-main-container {
        display: inline-flex !important; 
        align-items: center !important; 
        justify-content: center !important; 
        gap: 14px !important; 
        margin-bottom: 8px !important;
    }

    .progress-main-text { 
        font-size: 34px !important; 
        font-weight: 900 !important; 
        color: #0f172a !important; 
        -webkit-text-fill-color: #0f172a !important;
        letter-spacing: -0.5px !important; 
        margin: 0 !important;
    }

    .progress-sub-text { 
        font-size: 16px !important; 
        color: #64748b !important; 
        -webkit-text-fill-color: #64748b !important;
        font-weight: 600 !important; 
        margin-bottom: 35px !important; 
    }

    .steps-container { max-width: 460px !important; margin: 0 auto !important; text-align: left !important; }

    .step-item { 
        font-size: 18px !important; 
        color: #94a3b8 !important; 
        -webkit-text-fill-color: #94a3b8 !important;
        font-weight: 700 !important; 
        margin-bottom: 16px !important; 
        display: flex !important; 
        align-items: center !important; 
        gap: 14px !important; 
    }

    .step-item.active-step { color: #0f172a !important; -webkit-text-fill-color: #0f172a !important; }
    .step-item.done-step { color: #334155 !important; -webkit-text-fill-color: #334155 !important; }

    .icon-done { 
        font-size: 16px !important; display: flex !important; justify-content: center !important; align-items: center !important;
        width: 28px !important; height: 28px !important; border-radius: 50% !important; 
        background-color: #0CD25F !important; color: white !important;
        -webkit-text-fill-color: white !important; flex-shrink: 0 !important; font-weight: 900 !important;
    }

    .top-pulse-dot {
        width: 22px !important; height: 22px !important; border-radius: 50% !important; 
        background-color: #0CD25F !important; box-shadow: 0 0 0 0 rgba(12, 210, 95, 0.7) !important;
        animation: pulse-breathing 1.4s ease-in-out infinite !important; flex-shrink: 0 !important;
    }
    @keyframes pulse-breathing {
        0%   { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(12, 210, 95, 0.5); }
        70%  { transform: scale(1.15); box-shadow: 0 0 0 12px rgba(12, 210, 95, 0); }
        100% { transform: scale(0.9); box-shadow: 0 0 0 0 rgba(12, 210, 95, 0); }
    }

    .icon-spin-smooth {
        width: 28px !important; height: 28px !important; border-radius: 50% !important;
        border: 3px solid #e2e8f0 !important; border-top-color: #0CD25F !important;
        animation: spin-clockwise 0.8s linear infinite !important; flex-shrink: 0 !important;
    }
    @keyframes spin-clockwise { to { transform: rotate(360deg); } }

    .icon-wait { 
        width: 28px !important; height: 28px !important; border-radius: 50% !important; 
        border: 3px solid #cbd5e1 !important; flex-shrink: 0 !important; background-color: transparent !important;
    }

    /* =========================================
    ✨ DETAILED NUMBER INTELLIGENCE REPORT
    ========================================= */
    .intel-card {
        background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 30px;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.03); margin-bottom: 30px; font-family: 'Nunito', sans-serif;
    }
    .intel-header { display: flex; align-items: center; gap: 15px; margin-bottom: 25px; padding-bottom: 20px; border-bottom: 1px solid #f1f5f9; }
    .intel-header-icon { width: 45px; height: 45px; background: #eff6ff; color: #3b82f6; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size: 20px; }
    .intel-header-title { font-size: 24px; font-weight: 900; color: #0f172a; line-height: 1.2; }
    .intel-header-sub { font-size: 14px; font-weight: 600; color: #64748b; }

    .ai-rec-box { background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border-left: 6px solid #0CD25F; border-radius: 12px; padding: 20px; margin-bottom: 30px; }
    .ai-rec-box.spam-box { background: linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%); border-left-color: #e11d48; }
    .ai-rec-text { font-size: 15px; color: #0f172a; font-weight: 600; line-height: 1.6; }

    .info-row { display: flex; padding: 18px 0; border-bottom: 1px solid #f1f5f9; }
    .info-row:last-child { border-bottom: none; padding-bottom: 0; }
    .info-label { flex: 0 0 160px; font-size: 14px; font-weight: 700; color: #64748b; }
    .info-value { flex: 1; font-size: 15px; font-weight: 800; color: #1e293b; }
    .info-desc { font-size: 13px; font-weight: 600; color: #94a3b8; margin-top: 4px; line-height: 1.4; }

    .format-pills { display: flex; flex-wrap: wrap; gap: 8px; }
    .format-pill { background: #eff6ff; border: 1px solid #bfdbfe; color: #1e40af; padding: 5px 12px; border-radius: 8px; font-size: 13px; font-weight: 700; font-family: monospace; }

    /* Risk Slider Styles */
    .risk-slider-container { margin-top: 10px; position: relative; max-width: 400px; }
    .risk-track { width: 100%; height: 8px; border-radius: 100px; background: linear-gradient(90deg, #10b981 0%, #f59e0b 50%, #ef4444 100%); position: relative; }
    .risk-marker { position: absolute; top: -5px; width: 6px; height: 18px; background: #0f172a; border-radius: 10px; box-shadow: 0 0 4px rgba(0,0,0,0.3); }
    .risk-labels { display: flex; justify-content: space-between; margin-top: 8px; font-size: 12px; font-weight: 800; color: #64748b; max-width: 400px; }

    @media (max-width: 600px) { .info-row { flex-direction: column; gap: 8px; padding: 15px 0; } .info-label { flex: none; } }

    /* =========================================
    ✨ AI RECOMMENDATION & CALL TYPE GRID
    ========================================= */
    .call-type-box { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 30px; box-shadow: 0 4px 12px rgba(15, 23, 42, 0.02); margin-bottom: 30px; font-family: 'Nunito', sans-serif;}
    .call-type-header { font-size: 22px; font-weight: 800; color: #0f172a; margin-bottom: 5px; }
    .call-type-sub { font-size: 14px; color: #3b82f6; font-weight: 700; margin-bottom: 25px; cursor: pointer; transition: color 0.2s; }
    .call-type-sub:hover { color: #2563eb; text-decoration: underline; }
    .call-type-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; }
    .call-type-card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px; display: flex; flex-direction: column; gap: 8px; transition: all 0.2s ease; cursor: pointer; }
    .call-type-card:hover { border-color: #0CD25F; background: #ffffff; box-shadow: 0 6px 15px rgba(12, 210, 95, 0.1); transform: translateY(-3px); }
    .card-top { display: flex; align-items: center; gap: 12px; }
    .card-icon { font-size: 22px; }
    .card-title { font-size: 17px; font-weight: 800; color: #1e293b; }
    .card-desc { font-size: 13.5px; font-weight: 600; color: #64748b; line-height: 1.4; }

    @media (max-width: 768px) {
        .call-type-grid { grid-template-columns: 1fr; }
    }

    /* =========================================
    ✨ ELEGANT & COMPACT ACTION BUTTONS
    ========================================= */
    
    /* 1. DOWNLOAD BUTTON (Compact & Sleek) */
    div[data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #0CD25F 0%, #059669 100%) !important; 
        color: white !important; 
        font-family: 'Nunito', sans-serif !important;
        font-size: 16px !important; 
        font-weight: 800 !important; 
        padding: 14px 0 !important; 
        border-radius: 100px !important; 
        border: none !important; 
        cursor: pointer !important; 
        transition: all 0.3s ease !important; 
        box-shadow: 0 6px 15px rgba(12, 210, 95, 0.25) !important;
        width: 100% !important;
        letter-spacing: 0.5px;
    }
    div[data-testid="stDownloadButton"] button p {
        color: white !important;
        font-size: 16px !important; 
        font-weight: 800 !important; 
    }
    div[data-testid="stDownloadButton"] button:hover {
        transform: translateY(-2px) !important; 
        box-shadow: 0 10px 20px rgba(12, 210, 95, 0.4) !important; 
    }
    div[data-testid="stDownloadButton"] button:focus,
    div[data-testid="stDownloadButton"] button:active {
        outline: none !important;
        border: none !important;
    }

    /* 2. START NEW SEARCH BUTTON (Direct Streamlit Target - Nuclear Fix) */
    button[kind="secondary"] {
        background-color: #f1f5f9 !important; 
        border: none !important; 
        border-radius: 100px !important; 
        padding: 12px 0 !important; 
        cursor: pointer !important; 
        transition: all 0.3s ease !important; 
        width: 100% !important;
    }
    button[kind="secondary"] p {
        color: #64748b !important; 
        font-family: 'Nunito', sans-serif !important;
        font-size: 15px !important; 
        font-weight: 800 !important; 
        text-transform: uppercase !important;
        margin: 0 !important;
    }
    button[kind="secondary"]:hover {
        background-color: #e2e8f0 !important; 
        transform: translateY(-2px) !important; 
    }
    button[kind="secondary"]:hover p {
        color: #1e293b !important; 
    }
    button[kind="secondary"]:focus,
    button[kind="secondary"]:active {
        outline: none !important;
        box-shadow: none !important;
        background-color: #f1f5f9 !important;
    }
    button[kind="secondary"]:focus p {
        color: #64748b !important;
    }

    /* =========================================
    ✨ GLOBAL FOOTER CSS
    ========================================= */
    .global-footer {
        background-color: #262626;
        color: #ffffff;
        padding: 60px 40px 20px 40px;
        font-family: 'Nunito', sans-serif;
        position: relative;
        overflow: hidden;
        margin-top: 80px;
    }
    .footer-bg-logo {
        position: absolute;
        right: -80px;
        top: -40px;
        height: 400px;
        z-index: 0;
        pointer-events: none;
        opacity: 1;
    }
    .footer-content {
        max-width: 1400px;
        margin: 0 auto;
        position: relative;
        z-index: 1;
    }
    .footer-cta {
        margin-bottom: 60px;
    }
    .footer-cta h2 {
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 10px;
        letter-spacing: -1px;
    }
    .footer-cta h2 span { color: #0CD25F; }
    .footer-cta p { font-size: 15px; margin-bottom: 25px; color: #a1a1aa; font-weight: 600;}
    .footer-badges { display: flex; gap: 15px; }
    .footer-badges img { height: 40px; cursor: pointer; transition: transform 0.2s;}
    .footer-badges img:hover { transform: translateY(-2px); }

    .footer-middle {
        display: flex;
        justify-content: space-between;
        flex-wrap: wrap;
        margin-bottom: 40px;
        padding-bottom: 40px;
        border-bottom: 1px solid #3f3f46;
    }
    .footer-left { max-width: 250px; }
    .footer-lang { 
        background: #3f3f46; border-radius: 8px; padding: 10px 15px; 
        display: inline-flex; align-items: center; gap: 10px; cursor: pointer;
        font-size: 14px; font-weight: 700; margin-bottom: 25px; transition: background 0.2s;
    }
    .footer-lang:hover { background: #52525b; }
    .footer-powered { height: 22px; opacity: 0.8; }

    .footer-links-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 80px;
    }
    .footer-col-title { font-weight: 800; font-size: 15px; margin-bottom: 25px; color: #ffffff;}
    .footer-col-links { display: flex; flex-direction: column; gap: 16px; }
    .footer-col-links a { color: #a1a1aa; text-decoration: none; font-size: 13px; font-weight: 700; transition: color 0.2s;}
    .footer-col-links a:hover { color: #0CD25F; }

    .footer-bottom {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 13px;
        color: #a1a1aa;
        font-weight: 600;
    }
    .footer-bottom-links { display: flex; gap: 25px; align-items: center;}
    .footer-bottom-links a { color: #a1a1aa; text-decoration: none; transition: color 0.2s; }
    .footer-bottom-links a:hover { color: #ffffff; }
    .footer-social { display: flex; align-items: center; }
    .footer-social svg { width: 20px; height: 20px; fill: #a1a1aa; transition: fill 0.2s; cursor: pointer;}
    .footer-social svg:hover { fill: #ffffff; }

    @media (max-width: 900px) {
        .footer-middle { flex-direction: column; gap: 50px; }
        .footer-links-grid { grid-template-columns: repeat(2, 1fr); gap: 40px; }
        .footer-bottom { flex-direction: column; gap: 20px; text-align: center; }
        .footer-bg-logo { height: 250px; right: -80px; }
    }

    </style>
    """, unsafe_allow_html=True)

    if bg_image_base64:
        st.markdown(f"""
    <style>
    .stApp {{
        background-color: #f8fafc !important; 
        background-image: url("data:image/jpeg;base64,{bg_image_base64}") !important;
        background-repeat: repeat !important;
        background-size: 400px !important;
        background-attachment: fixed !important;
    }}
    </style>
    """, unsafe_allow_html=True)

    # ==========================================
    # 3. PAGE BODY ROUTING
    # ==========================================

    if current_page == "home":
        if logo_b64:
            st.markdown(f"""
    <div class="navbar">
        <div class="navbar-logo" style="display: flex; align-items: center;">
            <img src="data:image/png;base64,{logo_b64}" alt="WhatsTrue Icon" style="height: 45px;">
            <span style="color: #0CD25F; font-weight: 900; font-size: 28px; letter-spacing: -1px; margin-left: 8px; font-family: 'Nunito', sans-serif;">WhatsTrue</span>
        </div>
        <div class="navbar-links">
            <a href="#protect">Features</a>
            <a href="#premium">Premium</a>
            <a href="#business">Business ▾</a>
            <a href="#blog">Blog</a>
        </div>
    </div>
                """, unsafe_allow_html=True)

            video_path = "Assets/Whoscall_demo_en.mp4" 
            video_b64 = get_base64_video(video_path)

            if video_b64:
                st.markdown(f"""
        <div class="hero-wrapper">
            <div class="hero-overlay"></div>
            <div class="hero-content-overlay">
                 <div class="exact-hero-title">Confidence with<br>Every Connection</div>
                 <div class="hero-buttons">
                     <a href="?page=scanner" target="_self" class="btn-green-exact">Get Started</a>
            </div>
            </div>
        </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
        <div class="hero-wrapper" style="background: linear-gradient(135deg, #1e293b, #334155);">
            <div class="hero-overlay"></div>
            <div class="hero-content-overlay">
                <div class="exact-hero-title">Confidence with<br>Every Connection</div>
                <div class="hero-buttons">
                    <a href="?page=scanner" target="_self" class="btn-green-exact">Get Started</a>
                </div>
            </div>
        </div>
                """, unsafe_allow_html=True)

        # ==========================================
        # 🔥 PROTECT, DETECT, TESTIMONIALS & TRUSTED SECTIONS
        # ==========================================
        st.markdown("""
    <div class="protect-section" id="protect">
    <div class="protect-left">
    <div class="section-subtitle subtitle-pink">Protect</div>
    <div class="section-title">Stay in control by<br>knowing who's calling</div>

    <div class="feature-bullet">
    <div class="feature-bullet-icon">
    <svg viewBox="0 0 48 49" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M0 16.4067C0 7.57018 7.16344 0.406738 16 0.406738H32C40.8366 0.406738 48 7.57018 48 16.4067V32.4067C48 41.2433 40.8366 48.4067 32 48.4067H16C7.16344 48.4067 0 41.2433 0 32.4067V16.4067Z" fill="#FEE7F2"/>
    <g clip-path="url(#clip0_8928_972)">
    <rect x="13.833" y="24.0828" width="4.32789" height="11.2826" rx="2.16395" transform="rotate(-45 13.833 24.0828)" fill="#F53F90"/>
    <rect x="21.8193" y="32.0608" width="4.32789" height="16.9905" rx="2.16395" transform="rotate(-135 21.8193 32.0608)" fill="#F53F90"/>
    </g>
    <defs><clipPath id="clip0_8928_972"><rect width="20" height="20" fill="white" transform="translate(14 14.4067)"/></clipPath></defs>
    </svg>
    </div>
    <div class="feature-bullet-text">Caller ID in real time. No more “Who’s this?”</div>
    </div>

    <div class="feature-bullet">
    <div class="feature-bullet-icon">
    <svg viewBox="0 0 48 49" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M0 16.4067C0 7.57018 7.16344 0.406738 16 0.406738H32C40.8366 0.406738 48 7.57018 48 16.4067V32.4067C48 41.2433 40.8366 48.4067 32 48.4067H16C7.16344 48.4067 0 41.2433 0 32.4067V16.4067Z" fill="#FEE7F2"/>
    <g clip-path="url(#clip0_8928_972)">
    <rect x="13.833" y="24.0828" width="4.32789" height="11.2826" rx="2.16395" transform="rotate(-45 13.833 24.0828)" fill="#F53F90"/>
    <rect x="21.8193" y="32.0608" width="4.32789" height="16.9905" rx="2.16395" transform="rotate(-135 21.8193 32.0608)" fill="#F53F90"/>
    </g>
    <defs><clipPath id="clip0_8928_972"><rect width="20" height="20" fill="white" transform="translate(14 14.4067)"/></clipPath></defs>
    </svg>
    </div>
    <div class="feature-bullet-text">Spam & scam blockers that actually work.</div>
    </div>
    </div>
    <div class="protect-right">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/6912a4ec053c89b8e52ca846_img-home-protect.webp" alt="WhatsTrue Protect App Preview">
    </div>
    </div>

    <div class="detect-section" id="business">
    <div class="detect-left">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/6912b1a0a049a8c394bcb4b4_img-check.webp" alt="WhatsTrue AI Detection">
    </div>
    <div class="detect-right">
    <div class="section-subtitle subtitle-green">Detect</div>
    <div class="section-title">Check smarter, not<br>harder</div>

    <div class="feature-bullet">
    <div class="feature-bullet-icon">
    <svg viewBox="0 0 48 49" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M0 16.4067C0 7.57018 7.16344 0.406738 16 0.406738H32C40.8366 0.406738 48 7.57018 48 16.4067V32.4067C48 41.2433 40.8366 48.4067 32 48.4067H16C7.16344 48.4067 0 41.2433 0 32.4067V16.4067Z" fill="#D6FEF1"/><g clip-path="url(#clip0_det)"><rect x="13.833" y="24.0828" width="4.32789" height="11.2826" rx="2.16395" transform="rotate(-45 13.833 24.0828)" fill="#019D91"/><rect x="21.8193" y="32.0608" width="4.32789" height="16.9905" rx="2.16395" transform="rotate(-135 21.8193 32.0608)" fill="#019D91"/></g><defs><clipPath id="clip0_det"><rect width="20" height="20" fill="white" transform="translate(14 14.4067)"/></clipPath></defs></svg>
    </div>
    <div class="feature-bullet-text"><strong>Phone number</strong> - no more mystery calls or unwanted surprises.</div>
    </div>

    <div class="feature-bullet">
    <div class="feature-bullet-icon">
    <svg viewBox="0 0 48 49" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M0 16.4067C0 7.57018 7.16344 0.406738 16 0.406738H32C40.8366 0.406738 48 7.57018 48 16.4067V32.4067C48 41.2433 40.8366 48.4067 32 48.4067H16C7.16344 48.4067 0 41.2433 0 32.4067V16.4067Z" fill="#D6FEF1"/><g clip-path="url(#clip0_det)"><rect x="13.833" y="24.0828" width="4.32789" height="11.2826" rx="2.16395" transform="rotate(-45 13.833 24.0828)" fill="#019D91"/><rect x="21.8193" y="32.0608" width="4.32789" height="16.9905" rx="2.16395" transform="rotate(-135 21.8193 32.0608)" fill="#019D91"/></g><defs><clipPath id="clip0_det"><rect width="20" height="20" fill="white" transform="translate(14 14.4067)"/></clipPath></defs></svg>
    </div>
    <div class="feature-bullet-text"><strong>URL</strong> - Stop phishing scams before they hook you in.</div>
    </div>

    <div class="feature-bullet">
    <div class="feature-bullet-icon">
    <svg viewBox="0 0 48 49" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M0 16.4067C0 7.57018 7.16344 0.406738 16 0.406738H32C40.8366 0.406738 48 7.57018 48 16.4067V32.4067C48 41.2433 40.8366 48.4067 32 48.4067H16C7.16344 48.4067 0 41.2433 0 32.4067V16.4067Z" fill="#D6FEF1"/><g clip-path="url(#clip0_det)"><rect x="13.833" y="24.0828" width="4.32789" height="11.2826" rx="2.16395" transform="rotate(-45 13.833 24.0828)" fill="#019D91"/><rect x="21.8193" y="32.0608" width="4.32789" height="16.9905" rx="2.16395" transform="rotate(-135 21.8193 32.0608)" fill="#019D91"/></g><defs><clipPath id="clip0_det"><rect width="20" height="20" fill="white" transform="translate(14 14.4067)"/></clipPath></defs></svg>
    </div>
    <div class="feature-bullet-text"><strong>Screenshot</strong> - See beyond the surface in seconds!</div>
    </div>

    <a href="#" class="btn-detect">Try WhatsTrue AI !</a>
    </div>
    </div>

    <div class="power-section" id="premium">
    <div class="power-title">Unlock the power of WhatsTrue</div>

    <div class="power-stats">
    <div class="power-stat-item">
    <div class="power-val">5x</div>
    <div class="power-label">faster ID<br>load speed</div>
    </div>
    <div class="power-stat-item">
    <div class="power-val">45%</div>
    <div class="power-label">increase in<br>ID security</div>
    </div>
    <div class="power-stat-item">
    <div class="power-val">10x</div>
    <div class="power-label">peace<br>of mind</div>
    </div>
    </div>

    <div class="power-cards">
    <div class="power-card">
    <div class="power-icon">🔄</div>
    <div class="power-card-title">Auto update<br>Number Database</div>
    </div>
    <div class="power-card">
    <div class="power-icon">🛡️</div>
    <div class="power-card-title">Auto spam call<br>blocker</div>
    </div>
    <div class="power-card">
    <div class="power-icon">💬</div>
    <div class="power-card-title">SMS Assistant</div>
    </div>
    <div class="power-card">
    <div class="power-icon">🚫</div>
    <div class="power-card-title">AD-free</div>
    </div>
    <div class="power-card">
    <div class="power-icon">👥</div>
    <div class="power-card-title">Account sharing</div>
    </div>
    </div>

    <a href="#" class="btn-white">See premium plan ➔</a>
    </div>

    <div class="testimonial-wrapper" id="blog">
    <div class="testi-header">Trusted worldwide</div>
    <div class="testi-title">Don’t just take our word for it</div>

    <div class="testi-grid">
    <div class="testi-card">
    <div class="testi-user">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/6912b5796469a08ea70a00d5_img-avatarTh.webp" class="testi-avatar" alt="User">
    <div>
    <div class="testi-name">Nueng</div>
    <div class="testi-country">Thailand</div>
    </div>
    </div>
    <div class="testi-text">"Downloaded, it works and is really good. WhatsTrue helps to identify who is calling, especially scammers."</div>
    </div>

    <div class="testi-card">
    <div class="testi-user">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/6912b579525f2cb63c79be4e_img-avatarPH.webp" class="testi-avatar" alt="User">
    <div>
    <div class="testi-name">Jax Reyes</div>
    <div class="testi-country">Philippines</div>
    </div>
    </div>
    <div class="testi-text">"That's the best because the names of who's calling you is shown - if it's a telemarketer, if it's a scammer, or whoever it could be"</div>
    </div>

    <div class="testi-card">
    <div class="testi-user">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/6912b579686a76e70168c62b_img-avatarMy.webp" class="testi-avatar" alt="User">
    <div>
    <div class="testi-name">Muhammad Aziz</div>
    <div class="testi-country">Malaysia</div>
    </div>
    </div>
    <div class="testi-text">"Every time there's a suspicious number, WhatsTrue gives an early warning! Really awesome!"</div>
    </div>

    <div class="testi-card">
    <div class="testi-user">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/6912b579467f868689175f4a_img-avatarJp.webp" class="testi-avatar" alt="User">
    <div>
    <div class="testi-name">美三恵</div>
    <div class="testi-country">Japan</div>
    </div>
    </div>
    <div class="testi-text">"I used to ignore calls from unknown numbers. Now, with WhatsTrue, I can see who's calling and decide confidently whether to answer. It's a must-have app!"</div>
    </div>

    <div class="testi-card">
    <div class="testi-user">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/6912b57958c54419a02acf81_img-avatarKr.webp" class="testi-avatar" alt="User">
    <div>
    <div class="testi-name">이혜원</div>
    <div class="testi-country">South Korean</div>
    </div>
    </div>
    <div class="testi-text">"I love this app! It helps me identify voice phishing scams and has reliably caught scammers I've struggled with for ages. Highly recommend!"</div>
    </div>

    <div class="testi-card">
    <div class="testi-user">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/6912b579712f07aa84ba53bc_img-avatarBr.webp" class="testi-avatar" alt="User">
    <div>
    <div class="testi-name">Christian</div>
    <div class="testi-country">Brazil</div>
    </div>
    </div>
    <div class="testi-text">"Tired of spam calls? WhatsTrue identifies and blocks unknown numbers. Download it now on the App Store or Google Play!"</div>
    </div>
    </div>

    <div class="testi-stats-title">Trusted by millions and growing!</div>
    <div class="testi-stats-grid">
    <div>
    <div class="testi-stat-val">100K+</div>
    <div class="testi-stat-label">REPORT DATA</div>
    </div>
    <div>
    <div class="testi-stat-val">1M+</div>
    <div class="testi-stat-label">WHATSTRUE USERS</div>
    </div>
    </div>

    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/68871fc34336ef845314684e_mapTwEn.png" class="globe-img" alt="Globe Users">
    </div>

    <div class="trusted-container">
    <div class="trusted-label">Trusted By</div>
    <div class="marquee-wrapper">
    <div class="marquee-track">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/68871f546780c9ca9b996617_maxis.png" class="marquee-logo" alt="Maxis">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/68871f53ff3dcd6cc8ef5b34_hotlink.png" class="marquee-logo" alt="Hotlink">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/68871f53a1b4ee1854e7d189_hkt.png" class="marquee-logo" alt="HKT">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/68871f56b6ff099468d1c287_selangor.png" class="marquee-logo" alt="Selangor">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/68871f5458e5a5df0ffce368_ncsa.png" class="marquee-logo" alt="NCSA">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/68871f5662b247ca76139f83_true5G.png" class="marquee-logo" alt="True5G">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/68871f546780c9ca9b996617_maxis.png" class="marquee-logo" alt="Maxis">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/68871f53ff3dcd6cc8ef5b34_hotlink.png" class="marquee-logo" alt="Hotlink">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/68871f53a1b4ee1854e7d189_hkt.png" class="marquee-logo" alt="HKT">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/68871f56b6ff099468d1c287_selangor.png" class="marquee-logo" alt="Selangor">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/68871f5458e5a5df0ffce368_ncsa.png" class="marquee-logo" alt="NCSA">
    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/68871f5662b247ca76139f83_true5G.png" class="marquee-logo" alt="True5G">
    </div>
    </div>
    </div>
        """, unsafe_allow_html=True)

    elif current_page == "scanner":
        if logo_b64:
            st.markdown(f"""
            <div class="whatstrue-header" onclick="window.location.href='?page=home'">
                <div style="display: flex; align-items: center;">
                    <img src="data:image/png;base64,{logo_b64}" alt="WhatsTrue Icon" style="height: 35px; mix-blend-mode: multiply;">
                    <span style="color: #0CD25F; font-weight: 900; font-size: 24px; letter-spacing: -1px; margin-left: 8px; font-family: 'Nunito', sans-serif;">WhatsTrue</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.search_state == 'idle':
            st.markdown('<div style="max-width: 1200px; margin: 0 auto; padding: 0 40px; margin-top:50px;">', unsafe_allow_html=True)
            st.markdown('<div class="scanner-page-title">Is This WhatsApp Message Suspicious?</div>', unsafe_allow_html=True)

            col_left, col_right = st.columns([1, 1.1], gap="large")

            with col_left:
                st.markdown('<div class="custom-label">Enter WhatsApp Number</div>', unsafe_allow_html=True)
                st.markdown('<div class="custom-sublabel">Select country code and enter number</div>', unsafe_allow_html=True) 
                
                col_code, col_num = st.columns([1.6, 2.5]) 
                
                country_data = {
                    "Pakistan (+92)": {"region": "Pakistan", "length":[11], "code": "+92"},
                    "India (+91)": {"region": "India", "length":[11], "code": "+91"},
                    "United States (+1)": {"region": "United States / Canada", "length":[10], "code": "+1"},
                    "United Kingdom (+44)": {"region": "United Kingdom", "length":[10], "code": "+44"},
                    "U.A.E (+971)": {"region": "United Arab Emirates", "length":[9], "code": "+971"},
                    "Saudi Arabia (+966)": {"region": "Saudi Arabia", "length":[9], "code": "+966"},
                    "Australia (+61)": {"region": "Australia", "length":[9], "code": "+61"},
                    "Germany (+49)": {"region": "Germany", "length":[10], "code": "+49"},
                    "France (+33)": {"region": "France", "length":[9], "code": "+33"},
                    "Italy (+39)": {"region": "Italy", "length":[10], "code": "+39"},
                    "Spain (+34)": {"region": "Spain", "length":[9], "code": "+34"},
                    "Bahrain (+973)": {"region": "Bahrain", "length":[8], "code": "+973"},
                }
                
                with col_code:
                    selected_country_string = st.selectbox("Code", list(country_data.keys()), label_visibility="collapsed")
                    
                with col_num:
                    phone_number = st.text_input("Source", placeholder="E.g. 3146081201", label_visibility="collapsed")
                
                detected_region = country_data[selected_country_string]["region"]
                st.markdown(f'<div class="detected-region">📍 Detected Region: <span>{detected_region}</span></div>', unsafe_allow_html=True)
                
            with col_right:
                st.markdown('<div class="custom-label">Enter WhatsApp Message</div>', unsafe_allow_html=True)
                st.markdown('<div class="custom-sublabel">(Paste the exact message you received here)</div>', unsafe_allow_html=True)
                spam_text = st.text_area("Payload", placeholder="Paste the exact message you received...", height=155, label_visibility="collapsed")

            st.markdown("<br>", unsafe_allow_html=True) 
            error_placeholder = st.empty() 
            
            btn_col1, btn_col2, btn_col3 = st.columns([1, 1.2, 1]) 
            
            with btn_col2:
                if st.button("🚀 INITIATE SCAN", type="primary", use_container_width=True):
                    cleaned_number = ''.join(filter(str.isdigit, phone_number))
                    expected_lengths = country_data[selected_country_string]["length"]
                    
                    if not phone_number:
                        error_placeholder.markdown('''
                            <div class="fancy-error">
                                <span style="color: #be123c; font-size: 20px; font-weight: 900;">⚠️ Field is Empty!</span><br>
                                <span style="color: #4c1d95; font-size: 16px; font-weight: 700;">Please enter a phone number to scan.</span>
                            </div>
                        ''', unsafe_allow_html=True)
                    elif len(cleaned_number) not in expected_lengths:
                        len_str = " or ".join(map(str, expected_lengths))
                        error_placeholder.markdown(f'''
                            <div class="fancy-error">
                                <span style="color: #be123c; font-size: 20px; font-weight: 900;">🚨 Oops! Invalid Number Length.</span><br>
                                <span style="color: #881337; font-size: 16px; font-weight: 700;">For <b>{detected_region}</b>, standard numbers must be exactly <b>{len_str} digits</b> long.<br>
                                <span style="color: #f43f5e; font-weight: 800; font-size: 18px; display:block; margin-top:8px;">You entered: {len(cleaned_number)} digits</span></span>
                            </div>
                        ''', unsafe_allow_html=True)
                    else:
                        # Prediction yahan hogi
                        from src.mlproject.pipelines.prediction_pipeline import CustomData, PredictPipeline
                        
                        data = CustomData(
                        phone_number=phone_number.strip(),
                        message_text=spam_text.strip()
                        )
                        df = data.get_data_as_data_frame()
                        
                        pipeline = PredictPipeline()
                                                
                        # Result store karo session mein
                        result, confidence = pipeline.predict(df)
                        st.session_state.is_spam = bool(result[0] == 1)
                        st.session_state.confidence = confidence

                        if confidence <= 20:
                            st.session_state.risk_level = 1
                        elif confidence <= 40:
                            st.session_state.risk_level = 2
                        elif confidence <= 60:
                            st.session_state.risk_level = 3
                        elif confidence <= 80:
                            st.session_state.risk_level = 4
                        else:
                            st.session_state.risk_level = 5
                        
                        st.session_state.search_state = 'searching'
                        extracted_code = country_data[selected_country_string]["code"]
                        st.session_state.full_number = f"{extracted_code} {phone_number}"
                        st.session_state.detected_region = detected_region
                        st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        elif st.session_state.search_state in ['searching', 'done']:
            st.markdown('<div style="max-width: 1200px; margin: 0 auto; padding: 0 40px; margin-top:50px;">', unsafe_allow_html=True)
            target_num = st.session_state.get('full_number', '')
            
            st.markdown(f'''
                <div class="progress-box">
                    <div class="progress-main-container">
                        <div class="top-pulse-dot"></div>
                        <div class="progress-main-text">Searching for <span style="color:#0CD25F;">{target_num}</span></div>
                    </div>
                    <div class="progress-sub-text">Scanning 5.7M+ records in our database...<br><span style="color:#0CD25F; font-size: 14px; font-weight: 800;">About 20 seconds left...</span></div>
                    <div class="steps-container">
            ''', unsafe_allow_html=True)
            
            progress_placeholder = st.empty()
            
            steps = [
                "Number validated",
                "Checking carrier database",
                "Searching 5.7M+ records...",
                "Cross-referencing reports",
                "Compiling results"
            ]
            
            if st.session_state.search_state == 'searching':
                for i in range(len(steps) + 1):
                    html = ""
                    for j, step in enumerate(steps):
                        if j < i:
                            html += f'<div class="step-item done-step"><div class="icon-done">✓</div> {step}</div>'
                        elif j == i:
                            html += f'<div class="step-item active-step"><div class="icon-spin-smooth"></div> {step}</div>'
                        else:
                            html += f'<div class="step-item"><div class="icon-wait"></div> {step}</div>'
                    
                    progress_placeholder.markdown(html, unsafe_allow_html=True)
                    time.sleep(2.0) 
                    
                st.session_state.search_state = 'done'
                st.rerun()
                
            elif st.session_state.search_state == 'done':
                html = ""
                for step in steps:
                    html += f'<div class="step-item done-step"><div class="icon-done">✓</div> {step}</div>'
                progress_placeholder.markdown(html, unsafe_allow_html=True)
                st.markdown('</div></div>', unsafe_allow_html=True) 

                # SESSION STATE SE VARIABLES NIKALO
                target_num = st.session_state.get('full_number', '')
                detected_region = st.session_state.get('detected_region', 'Unknown Region')

                # --- YAHAN DOST BACKEND SE DATA LAYEGI ---
                # Session se actual prediction lo
                is_spam = st.session_state.get('is_spam', False)
                risk_level = st.session_state.get('risk_level', 1)
                confidence = st.session_state.get('confidence', 0.0)
                line_type = "Mobile Phone"
                
                # Formatting based on Backend response
                if risk_level >= 4:
                    spam_status_ui = "<span style='color: #e11d48;'>Yes (High Risk)</span>"
                    rec_bg = "linear-gradient(135deg, #fff1f2 0%, #ffe4e6 100%)"
                    rec_border = "#e11d48"
                    recommendation = f"This number ({target_num}) has been flagged as highly suspicious based on our recent network analysis. We strongly recommend that you do not click on any provided links, avoid sharing personal or financial information, and block this number immediately to ensure your safety."
                elif risk_level == 3:
                    spam_status_ui = "<span style='color: #e11d48;'>Yes (Moderate)</span>"
                    rec_bg = "linear-gradient(135deg, #fef3c7 0%, #fef9c3 100%)"
                    rec_border = "#f59e0b"
                    recommendation = f"This number ({target_num}) shows suspicious behavior and may be unsafe. Please be cautious, avoid clicking links, and verify the sender before responding."
                elif risk_level == 2:
                    spam_status_ui = "<span style='color: #2563eb;'>No</span>"
                    rec_bg = "linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)"
                    rec_border = "#2563eb"
                    recommendation = f"This number ({target_num}) currently appears low-risk, but use normal caution with unknown contacts and do not share sensitive information unnecessarily."
                else:
                    spam_status_ui = "<span style='color: #166534;'>NO (Safe)</span>"
                    rec_bg = "linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)"
                    rec_border = "#0CD25F"
                    recommendation = f"This number ({target_num}) appears safe based on our checks. You can proceed, but always remain careful with unfamiliar senders."
                
                # Calculate marker position percentage for CSS Slider (Risk 1=10%, 3=50%, 5=90%)
                marker_position = (risk_level / 5) * 100
                if marker_position > 95: marker_position = 95
                if marker_position < 5: marker_position = 5
                # -----------------------------------------

                st.markdown(f'''
    <div style="background: {rec_bg}; border-left: 6px solid {rec_border}; border-radius: 16px; padding: 24px; margin-bottom: 30px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); font-family: 'Nunito', sans-serif;">
    <div style="font-size: 24px; font-weight: 900; margin-bottom: 12px; color: #0f172a; display: flex; align-items: center; gap: 10px;">
    Is Spam: {spam_status_ui}
    </div>
    <div style="font-size: 16px; color: #334155; font-weight: 600; line-height: 1.6;">
    <strong style="color: #0f172a;">✨ AI Recommendation:</strong> {recommendation}
    </div>
    </div>

    <div class="intel-card">
    <div class="intel-header">
    <div class="intel-header-icon">📱</div>
    <div>
    <div class="intel-header-title">Number Intelligence</div>
    <div class="intel-header-sub">{target_num} • {detected_region}</div>
    </div>
    </div>

    <div class="info-row">
    <div class="info-label">Name</div>
    <div class="info-value">Unknown</div>
    </div>

    <div class="info-row">
    <div class="info-label">Country</div>
    <div class="info-value">{detected_region}</div>
    </div>

    <div class="info-row">
    <div class="info-label">Line Type</div>
    <div class="info-value">
    {line_type}
    <div class="info-desc">Mobile prefixes can identify the original issuing network, although portability may mean the active carrier is different today.</div>
    </div>
    </div>

    <div class="info-row">
    <div class="info-label">Location</div>
    <div class="info-value">
    {detected_region} Numbering Area
    <div class="info-desc">Estimated based on prefix.</div>
    </div>
    </div>

    <div class="info-row">
    <div class="info-label">Carrier</div>
    <div class="info-value">
    Unknown / Ported
    <div class="info-desc">Prefix-based carrier data can change after number portability.</div>
    </div>
    </div>

    <div class="info-row">
    <div class="info-label">Number Formats</div>
    <div class="info-value format-pills">
    <span class="format-pill">{target_num.replace(' ', '')}</span>
    <span class="format-pill">{target_num}</span>
    <span class="format-pill">{target_num.replace('+', '00')}</span>
    </div>
    </div>

    <div class="info-row">
    <div class="info-label">Risk Level</div>
    <div class="info-value" style="width: 100%;">
    <div style="font-size: 16px; font-weight: 800; margin-bottom: 8px;">Level {risk_level} / 5</div>
    <div class="risk-slider-container">
    <div class="risk-track"></div>
    <div class="risk-marker" style="left: calc({marker_position}% - 3px);"></div>
    </div>
    <div class="risk-labels">
    <span>Safe</span>
    <span>Moderate</span>
    <span>High Risk</span>
    </div>
    </div>
    </div>

    <div class="info-row">
    <div class="info-label">Threat Level</div>
    <div class="info-value">{confidence}%
    </div>
    </div>
    </div>

                ''', unsafe_allow_html=True)
                
                report_data = f"WhatsTrue Premium Report\nTarget Number: {target_num}\nRegion: {detected_region}\nRisk Level: {risk_level}/5\nIs Spam: {'Yes' if is_spam else 'No'}\nGenerated Date: 2026-05-25"
                
                dl_col1, dl_col2, dl_col3 = st.columns([1, 0.7, 1])
                with dl_col2:
                    st.download_button(
                        label="📥 DOWNLOAD FULL REPORT",
                        data=report_data,
                        file_name=f"whatstrue_report_{target_num.replace(' ','')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

            st.markdown('<br>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 0.7, 1])
            with col2:
                if st.button("← START NEW SEARCH", use_container_width=True):
                    st.session_state.search_state = 'idle'
                    st.rerun()
                
        st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # ✨ GLOBAL FOOTER (SHOWN ON EVERY PAGE)
    # ==========================================
    if logo_b64:
        st.markdown(f"""
    <div class="global-footer">
        <div class="footer-content">
            <div class="footer-cta">
                <h2>Free <span>download now</span></h2>
                <p>Take control of your personal identity today</p>
                <div class="footer-badges">
                    <a href="#"><img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/68872f785f9cd5849801c9a8_badge-apple.svg" alt="App Store"></a>
                    <a href="#"><img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/68872f7816d96d9d69031ebb_badge-google.svg" alt="Google Play"></a>
                </div>
            </div>
            <div class="footer-middle">
                <div class="footer-left">
                    <div style="display: flex; align-items: center; margin-bottom: 25px;">
                        <img src="data:image/png;base64,{logo_b64}" alt="WhatsTrue Icon" style="height: 35px; border-radius: 8px; object-fit: contain;">
                        <span style="color: #0CD25F; font-weight: 900; font-size: 26px; letter-spacing: -1px; margin-left: 8px; font-family: 'Nunito', sans-serif;">WhatsTrue</span>
                    </div>
                    <div class="footer-lang">
                        English 
                        <svg width="12" height="12" viewBox="0 0 24 25" fill="none"><path d="M16.2969 8.69922L12.0039 12.9922L7.71087 8.69922L6.29688 10.1132L12.0039 15.8202L17.7109 10.1132L16.2969 8.69922Z" fill="white"/></svg>
                    </div>
                    <br>
                    <img src="https://cdn.prod.website-files.com/6824b7a0497f20e292c20ff9/68872f78537d42e0f0d11915_powered%20by%20Gogolook.svg" class="footer-powered" alt="Powered by Gogolook">
                </div>
                <div class="footer-links-grid">
                    <div>
                        <div class="footer-col-title">WhatsTrue</div>
                        <div class="footer-col-links">
                            <a href="#">Features</a>
                            <a href="#">Premium</a>
                            <a href="#">Enterprise</a>
                            <a href="#">Mission</a>
                            <a href="#">Blog</a>
                            <a href="#">Redeem Code</a>
                        </div>
                    </div>
                    <div>
                        <div class="footer-col-title">Business</div>
                        <div class="footer-col-links">
                            <a href="#">Verified Business Number</a>
                            <a href="#">Watchmen</a>
                            <a href="#">Anti-Scam Intelligence</a>
                            <a href="#">Ads Partner</a>
                            <a href="#">Gifting</a>
                        </div>
                    </div>
                    <div>
                        <div class="footer-col-title">Company</div>
                        <div class="footer-col-links">
                            <a href="#">About Us</a>
                            <a href="#">Jobs</a>
                            <a href="#">Media kit</a>
                        </div>
                    </div>
                    <div>
                        <div class="footer-col-title">Services</div>
                        <div class="footer-col-links">
                            <a href="#">Technology</a>
                            <a href="#">FAQ</a>
                            <a href="#">Contact Us</a>
                            <a href="#">165 - Report System</a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="footer-bottom">
                <div class="footer-bottom-links">
                    <span>© 2026 Gogolook. All rights reserved.</span>
                    <a href="#">Privacy Policy</a>
                    <a href="#">Terms of Service</a>
                </div>
                <div class="footer-social">
                    <svg viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M20.5686 4.77345C21.5163 5.02692 22.2555 5.76903 22.5118 6.71673C23.1821 9.42042 23.1385 14.5321 22.5259 17.278C22.2724 18.2257 21.5303 18.965 20.5826 19.2213C17.9071 19.8831 5.92356 19.8015 3.40294 19.2213C2.45524 18.9678 1.71595 18.2257 1.45966 17.278C0.827391 14.7011 0.871044 9.25144 1.44558 6.73081C1.69905 5.78311 2.44116 5.04382 3.38886 4.78753C6.96561 4.0412 19.2956 4.282 20.5686 4.77345ZM9.86682 8.70227L15.6122 11.9974L9.86682 15.2925V8.70227Z"/></svg>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)