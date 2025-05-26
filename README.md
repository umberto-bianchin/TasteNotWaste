# 🍽️ TasteNotWaste

A smart AI-powered recipe recommender that helps you minimize food waste by suggesting recipes based on your pantry contents, using voice input and NLP.

## Authors

* [@umberto-bianchin](https://www.https/github.com/umberto-bianchin)
* [@claudiadecarlo19](https://www.github.com/claudiadecarlo19)


---

## 💻 Mac Installation

```bash
conda create -n tasteNotWaste python=3.10
conda activate tasteNotWaste

conda install -c conda-forge ffmpeg numpy scipy python-sounddevice
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install openai-whisper streamlit spacy
python -m spacy download en_core_web_sm

# To avoid libomp conflict with Whisper + Torch
export KMP_DUPLICATE_LIB_OK=TRUE

# Disable Streamlit file watcher (optional but recommended)
mkdir -p ~/.streamlit
echo "[server]\nfileWatcherType = \"none\"" > ~/.streamlit/config.toml
```

## 🖥️ Windows Installation

```bash
conda create -n tasteNotWaste python=3.10
conda activate tasteNotWaste

conda install -c conda-forge ffmpeg numpy scipy python-sounddevice
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install openai-whisper streamlit spacy
python -m spacy download en_core_web_sm

# Disable Streamlit file watcher (optional but recommended)
mkdir -p ~/.streamlit
echo "[server]\nfileWatcherType = \"none\"" > ~/.streamlit/config.toml
```

## 🎧 Microphone Setup

To make sure the voice input works correctly, you need to **select the right audio input device** for your system.

Use the provided tool `mic_test.py` to detect and test microphones.

### 🧪 Step-by-Step: Test and Choose Microphone

1. Run the mic test script:
   ```bash
   python mic_test.py
    ```

2. It will list available input devices
3. Enter the device index when prompted. For example:
    ```bash
    Select device index to record from: 1
    Enter duration in seconds: 5
    ```
4. A short audio clip will be recorded and saved as test.wav.
5. The waveform will be plotted so you can visually confirm the mic is working.

### ✅ Set the Selected Device
Once you identify the correct device index, update the value in your app:
In audio.py
```bash
DEFAULT_DEVICE_INDEX = 1  # ← your working device
```

💡 If nothing records or waveform is flat:

- Try another input device
- Check OS mic permissions

##  Run the App
```bash
# Mac (with env var for OpenMP fix)
KMP_DUPLICATE_LIB_OK=TRUE streamlit run main.py

# or if already exported (Mac or Windows)
streamlit run main.py
```

---

## 🎤 Voice Mode (Speech-to-Recipe)

TasteNotWaste includes an optional voice interface that lets you speak your request instead of filling in the filters manually.

### 🗣️ What You Can Say

The app uses OpenAI Whisper (speech-to-text) + spaCy (text parsing), so phrasing must follow relatively standard formats. Here's what works well:

### ✅ Example Phrases

- "Suggest a recipe for **2 people** in **20 minutes**"
- "I want something with **chicken** and **rice**"
- "Find a dish for **4 persons** that excludes **onion** and **garlic**"
- "What can I cook for **3 people** in **30 minutes** with **zucchini**"
- "Give me a recipe without **tuna**"

You can combine:
- ⏱️ **Time** (e.g., “20 minutes”)
- 👥 **Portions** (e.g., “3 people”)
- ❤️ **Preferred ingredients** (e.g., “with chicken”)
- 🚫 **Unwanted ingredients** (e.g., “without onion”)

### ⚠️ Voice Tips

- Stick to basic vocabulary and phrasing
- Avoid long or vague sentences
- Speak clearly and wait for the "Recording..." signal

---

If the ingredient is not found in your pantry, it will be **skipped silently** and optionally listed in a warning.


## 🛠️ Manual Mode (No Microphone Needed)

Don't have a mic? No problem.

You can use **TasteNotWaste manually**:

- Set the number of portions via slider  
- Choose prep time with a simple range  
- Select your favorite and unwanted ingredients from dropdowns  
- Click **"Suggest recipes"** to get recommendations

The voice functionality is optional and enhances the experience — but everything works without it too!

