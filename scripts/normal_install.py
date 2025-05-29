import os
import subprocess
import sys
import venv

def run(cmd):
    print(f"➡️  {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def check_python_version():
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ è richiesto.")
        sys.exit(1)

def create_venv():
    print("🔧 Creo ambiente virtuale in './.venv'")
    venv.create(".venv", with_pip=True)

def install_packages():
    pip_path = os.path.join(".venv", "bin", "pip") if os.name != "nt" else os.path.join(".venv", "Scripts", "pip.exe")
    python_path = os.path.join(".venv", "bin", "python") if os.name != "nt" else os.path.join(".venv", "Scripts", "python.exe")

    run(f"{pip_path} install ffmpeg-python numpy scipy pyaudio")
    run(f"{pip_path} install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu")
    run(f"{pip_path} install openai-whisper streamlit spacy pyttsx3")
    run(f"{python_path} -m spacy download en_core_web_sm")

    config_dir = os.path.expanduser("~/.streamlit") if os.name != 'nt' else os.path.expanduser("~\\.streamlit")
    os.makedirs(config_dir, exist_ok=True)
    with open(os.path.join(config_dir, "config.toml"), "w") as f:
        f.write('[server]\nfileWatcherType = "none"\n')

    print("✅ Setup completato (senza Conda)")

def main():
    check_python_version()
    create_venv()
    install_packages()
    print("ℹ️ Usa '.venv/bin/streamlit run app.py' (o 'Scripts\\streamlit' su Windows) per avviare l’app.")

if __name__ == "__main__":
    main()
