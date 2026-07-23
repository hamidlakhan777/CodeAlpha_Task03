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
model_choice = st.sidebar.selectbox("Brain (Model)", available_models if available_models else ["No models found"])

seq_length = st.sidebar.slider("Sequence Length", min_value=50, max_value=500, value=100, step=10)
temperature = st.sidebar.slider("Creativity (Temperature)", min_value=0.1, max_value=2.0, value=1.0, step=0.1)

st.sidebar.markdown("---")
st.sidebar.info("Upload dataset, run `train.py` to get custom models.")

# Main content
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("#### Ready to synthesize?")
    if st.button("🚀 GENERATE MUSIC"):
        if not available_models:
            st.error("No trained models found! Please run train.py first.")
        else:
            with st.spinner("Synthesizing Audio..."):
                # Add pulsing visualizer while generating
                st.markdown("""
                <div class="soundwave-container">
                    <div class="bar"></div><div class="bar"></div>
                    <div class="bar"></div><div class="bar"></div>
                    <div class="bar"></div>
                </div>
                """, unsafe_allow_html=True)
                
                try:
                    # Generate the music
                    output_file = f"outputs/generated_{int(time.time())}.mid"
                    generate_music(model_choice, num_generate=seq_length, temperature=temperature)
                    
                    # Assuming generator always saves to outputs/output.mid currently, let's rename it
                    if os.path.exists('outputs/output.mid'):
                        os.rename('outputs/output.mid', output_file)
                    
                    st.session_state['last_generated'] = output_file
                    st.success("Sequence successfully generated!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Generation failed: {e}")

with col2:
    if 'last_generated' in st.session_state and os.path.exists(st.session_state['last_generated']):
        midi_file = st.session_state['last_generated']
        st.markdown("#### 🎧 Playback & Visualizer")
        
        midi_base64 = get_base64_of_file(midi_file)
        data_uri = f"data:audio/midi;base64,{midi_base64}"
        
        # HTML5 MIDI Player by Magenta
        player_html = f"""
        <script src="https://cdn.jsdelivr.net/combine/npm/tone@14.7.58,npm/@magenta/music@1.23.1/es6/core.js,npm/focus-visible@5,npm/html-midi-player@1.4.0"></script>
        
        <style>
            midi-player {{
                display: block;
                width: 100%;
                margin: 10px 0;
            }}
            midi-visualizer {{
                display: block;
                width: 100%;
                height: 300px;
                background-color: #1a1a2e;
                border: 2px solid #00f3ff;
                border-radius: 10px;
                box-shadow: 0 0 15px #00f3ff;
            }}
        </style>
        
        <midi-visualizer type="piano-roll" id="myVisualizer"></midi-visualizer>
        <midi-player
          src="{data_uri}"
          sound-font visualizer="#myVisualizer">
        </midi-player>
        """
        
        components.html(player_html, height=400)
        
        # Download button
        with open(midi_file, "rb") as f:
            st.download_button(
                label="💾 DOWNLOAD MIDI",
                data=f,
                file_name=os.path.basename(midi_file),
                mime="audio/midi"
            )
    else:
        st.info("Your synthesized tracks will appear here.")
