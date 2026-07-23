# CodeAlpha_Task03
# 🎵 SonifyAI — Neural Music Generation System

<p align="center">
  <b>Generative AI Tool for Automatic Piano Composition using Deep LSTM Networks</b>
</p>

---

## 📌 Overview

**SonifyAI** is an end-to-end Deep Learning application designed to generate original piano music from MIDI datasets. Powered by Recurrent Neural Networks (specifically **LSTM** layers), the system learns sequential note/chord patterns, pitch dependencies, and timing dynamics to output brand-new musical tracks in real-time.

---

## ✨ Key Features

* 🧠 **Deep Recurrent Architecture:** Utilizes multi-layer **LSTM Networks** with Dropout regularization to prevent overfitting and capture long-term sequence dependencies.
* ⚡ **Interactive Cyberpunk UI:** Built with **Streamlit**, featuring custom controls for sequence parameters and real-time generation feedback.
* 🎛️ **Temperature & Sampling Control:** Fine-tune the "creativity" (entropy) of generated notes on the fly.
* 🎼 **MIDI Processing Pipeline:** Automatic conversion between raw `.mid` dataset files, note-integer mappings, and synthesized output streams using `music21`.
* 💾 **Automated Checkpointing:** Seamless training callback structure saving `.keras` model weights after every improvement epoch.
[ MIDI Files ] ➔ [ Data Loader (Notes/Chords) ] ➔ [ Sequence Preprocessing ]
│
[ Streamlit App ] 🎨 ◄── [ Saved .keras Model ] ◄── [ LSTM Model Training ]


1. **Extraction:** Parses raw MIDI data into single notes and multi-pitch chords.
2. **Encoding:** Maps note vocabulary to normalized numerical sequences.
3. **Training:** Learns predictive distributions over target notes using Categorical Crossentropy.
4. **Synthesis:** Samples note predictions sequentially based on temperature settings and writes to `output.mid`.

---

## 🛠️ Tech Stack

* **Language:** Python 3.11+
* **Deep Learning Framework:** TensorFlow / Keras
* **Audio & Musicology:** Music21, Mido, Pygame
* **Frontend Dashboard:** Streamlit
* **Data & Math Processing:** NumPy, Pickle

---

## 🚀 Quick Start Guide

### 1️⃣ Clone the Repository
```bash
git clone [https://github.com/YOUR-USERNAME/SonifyAI.git](https://github.com/YOUR-USERNAME/SonifyAI.git)
cd SonifyAI
2️⃣ Install Dependencies
Bash
pip install -r requirements.txt
3️⃣ Train the Model
Place your .mid dataset files inside the dataset/ directory and run:

Bash
python train.py
4️⃣ Launch the Application
Bash
streamlit run app.py
🎯 Project Highlights
Fast Inference: Optimized prediction loop for near-instant sequence generation during app usage.

Flexible Input: Supports loading custom models dynamically from the models/ folder.
---

## 🏗️ System Architecture & Workflow
