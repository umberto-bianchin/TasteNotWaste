# 🍽️ TasteNotWaste

A smart AI-powered recipe recommender that helps you minimize food waste by suggesting recipes based on your pantry contents, using voice input and NLP.

## Authors

* [@umberto-bianchin](https://www.github.com/umberto-bianchin)
* [@claudiadecarlo19](https://www.github.com/claudiadecarlo19)


---

## 📋 Requirements

Before running the application, make sure you have the following software and Python packages installed:

- **Python 3.10+**
- **ffmpeg**
- **numpy**
- **scipy**
- **portaudio**
- **pyaudio**
- **torch**, **torchvision**, **torchaudio** (CPU versions)
- **openai-whisper**
- **streamlit**
- **spacy**
- **pyttsx3**
- **spaCy model:** `en_core_web_sm`

---

## 📂 Installation Scripts
In the `scripts/` folder, you’ll find two helper scripts that automate the setup process:

- **`conda_install.py`**  
  A Python script that:
  1. Creates and activates a Conda environment named `tasteNotWaste` (Python 3.10).  
  2. Installs all required packages inside that environment (via `conda` and `pip`).  
  3. Downloads the spaCy model `en_core_web_sm`.  
  4. Creates/updates the Streamlit config to disable the file watcher.

  To run:
  ```bash
  cd scripts
  python conda_install.py
  ```

- **`normal_install.py`**  
  A Python script that:
  1. Verifies you’re on Python 3.10+.  
  2. Creates a virtual environment named `.venv`.  
  3. Installs all required packages inside `.venv` (via `pip`).  
  4. Downloads the spaCy model `en_core_web_sm`.  
  5. Creates/updates the Streamlit config to disable the file watcher.

  To run:
  ```bash
  cd scripts
  python normal_install.py
  ```

---

## 💻 Mac Installation with Conda

```bash
conda create -n tasteNotWaste python=3.10
conda activate tasteNotWaste

conda install -c conda-forge ffmpeg numpy scipy portaudio
pip install pyaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install openai-whisper streamlit spacy pyttsx3
python -m spacy download en_core_web_sm

# To avoid libomp conflict with Whisper + Torch
export KMP_DUPLICATE_LIB_OK=TRUE

# Disable Streamlit file watcher (optional but recommended)
mkdir -p ~/.streamlit
echo "[server]\nfileWatcherType = \"none\"" > ~/.streamlit/config.toml
```

## 🖥️ Windows Installation with Conda

```bash
conda create -n tasteNotWaste python=3.10
conda activate tasteNotWaste

conda install -c conda-forge ffmpeg numpy scipy portaudio
pip install pyaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install openai-whisper streamlit spacy pyttsx3
python -m spacy download en_core_web_sm

# Disable Streamlit file watcher (optional but recommended)
mkdir -p ~/.streamlit
echo "[server]\nfileWatcherType = \"none\"" > ~/.streamlit/config.toml
```

## 🚀 Running the App

Once you've created the virtual environment using one of the setup scripts (`setup_with_conda.py` or `setup_without_conda.py`), or after you installed all the needed packages, follow these steps to activate the environment and launch the app.

### ✅ 1. Activate the environment

#### Using `venv` (created by `normal_install.py`):

- **macOS / Linux:**
  ```bash
  source .venv/bin/activate
  ```

- **Windows (Command Prompt):**
  ```cmd
  .venv\Scripts\activate.bat
  ```

- **Windows (PowerShell):**
  ```powershell
  .venv\Scripts\Activate.ps1
  ```

#### Using Conda (created by `conda_install.py`):

```bash
conda activate tasteNotWaste
```

---

### ▶️ 2. Launch the app

From the root of the project, run:
```bash
streamlit run home.py
```

---

### ❌ Deactivate the environment (when you're done)

To deactivate the environment:

```bash
deactivate        # for venv
conda deactivate  # for conda
```

---
## 🎧 Microphone Setup

To make sure the voice input works correctly, use the provided tool `mic_test.py` to detect and test microphones.

### 🧪 Step-by-Step: Test Microphone

1. Run the mic test script:
   ```bash
   python mic_test.py
    ```
2. A short audio clip will be recorded and saved as test.wav.
5. Listen to the `test.wav` to confirm the mic is working.

💡 If nothing records or waveform is flat:

- Check OS mic permissions

---

## 🎤 Voice Mode (Speech-to-Recipe)

TasteNotWaste includes an optional voice interface that lets you speak your request instead of filling in the filters manually.

### 🗣️ What You Can Say

The app uses OpenAI Whisper (speech-to-text) + spaCy (text parsing), so phrasing must follow relatively standard formats. Here's what works well:

### ✅ Example Phrases

- "Suggest a recipe for **2 people** in **20 minutes**"
- "I want something with **pasta** and with **rice**"
- "Find a dish for **4 persons** with **onion** and no **garlic**"
- "What can I cook for **3 people** in **30 minutes** with **zucchini** that excludes **onion**?"
- "Give me a recipe without **tuna**"

You can combine:
- ⏱️ **Time** (e.g., “20 minutes”)
- 👥 **Portions** (e.g., “3 people”)
- 💸 **Buy ingredients** (e.g., "buy ingredients")
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
- Decide if you want to buy or not ingredients
- Select your favorite and unwanted ingredients from dropdowns  
- Click **"Suggest recipes"** to get recommendations

The voice functionality is optional and enhances the experience — but everything works without it too!

