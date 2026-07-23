import streamlit as st
import streamlit.components.v1 as components
import os
import base64
import time
from generator import generate_music
import glob

# Must be the first Streamlit command
st.set_page_config(page_title="SonifyAI - Music Generator", page_icon="🎵", layout="wide")

# Custom CSS for Cyberpunk / Neon Synthwave Theme
CYBERPUNK_CSS = """
<style>
/* Base Theme */
.stApp {
    background-color: #0d0f18;
    color: #e0e0e0;
    font-family: 'Inter', sans-serif;
}

/* Glowing text effects */
h1, h2, h3 {
    color: #00f3ff !important;
    text-shadow: 0 0 10px #00f3ff, 0 0 20px #00f3ff;
    font-weight: 700;
}

/* Sidebar Styling */
[data-testid="stSidebar"] {
    background-color: #1a1a2e;
    border-right: 2px solid #9d4edd;
    box-shadow: 5px 0 15px rgba(157, 78, 221, 0.4);
}

/* Buttons */
.stButton>button {
    background: linear-gradient(45deg, #9d4edd, #ff00ff);
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 24px;
    font-size: 16px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 2px;
    transition: all 0.3s ease;
    box-shadow: 0 0 10px #9d4edd, 0 0 20px #ff00ff;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px #00f3ff, 0 0 40px #00f3ff;
    color: #fff;
    border: none;
}

/* Sliders */
.stSlider div[data-baseweb="slider"] div {
    background-color: #00f3ff !important;
}

/* Loading Animation */
.stSpinner > div > div {
    border-top-color: #ff00ff !important;
    border-left-color: #00f3ff !important;
}

/* Custom Pulsing Soundwave for loading */
@keyframes pulse {
    0% { transform: scaleY(1); opacity: 0.5; }
    50% { transform: scaleY(2); opacity: 1; }
    100% { transform: scaleY(1); opacity: 0.5; }
}

.soundwave-container {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    height: 100px;
}

.bar {
    width: 10px;
    height: 30px;
    background-color: #00f3ff;
    border-radius: 5px;
    box-shadow: 0 0 10px #00f3ff;
    animation: pulse 1s infinite ease-in-out;
}
.bar:nth-child(1) { animation-delay: 0.1s; background-color: #00f3ff; }
.bar:nth-child(2) { animation-delay: 0.2s; background-color: #9d4edd; }
.bar:nth-child(3) { animation-delay: 0.3s; background-color: #ff00ff; }
.bar:nth-child(4) { animation-delay: 0.4s; background-color: #9d4edd; }
.bar:nth-child(5) { animation-delay: 0.5s; background-color: #00f3ff; }

/* Dataframe/Metrics Container */
div[data-testid="metric-container"] {
    background-color: rgba(26, 26, 46, 0.8);
    border: 1px solid #00f3ff;
    box-shadow: 0 0 10px rgba(0, 243, 255, 0.3);
    border-radius: 10px;
    padding: 10px;
}
</style>
"""

st.markdown(CYBERPUNK_CSS, unsafe_allow_html=True)

# Helper function to get base64 encoded MIDI
def get_base64_of_file(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# UI Layout
st.title("🎵 SonifyAI")
st.markdown("### Neural Music Generation in the Cyberpunk Era")
st.markdown("---")

# Sidebar Controls
st.sidebar.title("🎛️ Control Panel")

# Find available models
os.makedirs('models', exist_ok=True)
available_models = glob.glob("models/*.keras") + glob.glob("models/*.hdf5") + glob.glob("models/*.h5")

# Auto-download model from GitHub Release if no local model found
if not available_models:
    url = "https://github.com/hamidlakhan777/CodeAlpha_Task03/releases/download/v1.0/weights-improvement-05-4.3197-bigger.keras"
    dest = "models/weights-improvement-05-4.3197-bigger.keras"
    
    with st.sidebar.status("Downloading AI Model...", expanded=True) as status:
        try:
            import urllib.request
            urllib.request.urlretrieve(url, dest)
            status.update(label="Model Downloaded Successfully! 🎉", state="complete")
            available_models = glob.glob("models/*.keras") + glob.glob("models/*.hdf5") + glob.glob("models/*.h5")
        except Exception as e:
            status.update(label=f"Download failed: {e}", state="error")

model_choice = st.sidebar.selectbox("Brain (Model)", available_models if available_models else ["No models found"])
