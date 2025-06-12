import subprocess
import sys
import os

def run(cmd, env=None):
    print(f"➡️  {cmd}")
    subprocess.run(cmd, shell=True, check=True, env=env)

def main():
    # Step 1: Create conda environment
    run("conda create -y -n tasteNotWaste python=3.10")

    # Step 2: Install packages using subprocess calls with `conda run`
    # These calls run commands inside the created environment
    def conda_run(command):
        return f'conda run -n tasteNotWaste {command}'

    run(conda_run("conda install -y -c conda-forge ffmpeg numpy scipy portaudio"))
    run(conda_run("pip install pyaudio"))
    run(conda_run("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu"))
    run(conda_run("pip install openai-whisper streamlit spacy pyttsx3"))
    run(conda_run("python -m spacy download en_core_web_sm"))

    # Streamlit config (done outside environment as it’s user-specific)
    config_dir = os.path.expanduser("~/.streamlit")
    os.makedirs(config_dir, exist_ok=True)
    with open(os.path.join(config_dir, "config.toml"), "w") as f:
        f.write('[server]\nfileWatcherType = "none"\n')

    print("✅ Setup completed (Conda)")

if __name__ == "__main__":
    main()
