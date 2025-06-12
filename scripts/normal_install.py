import os
import subprocess
import sys
import venv
import platform

def run(cmd):
    print(f"➡️  {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def check_python_version():
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ is needed.")
        sys.exit(1)

def create_venv():
    print("🔧 Creating virtual environment in './.venv'")
    venv.create(".venv", with_pip=True)

def install_packages():
    is_windows = os.name == "nt"
    pip_path = os.path.join(".venv", "Scripts", "pip.exe") if is_windows else os.path.join(".venv", "bin", "pip")
    python_path = os.path.join(".venv", "Scripts", "python.exe") if is_windows else os.path.join(".venv", "bin", "python")

    run(f"{pip_path} install ffmpeg-python numpy scipy")

    if is_windows:
        run(f"{pip_path} install pipwin")
        run(f"{pip_path} install --upgrade setuptools wheel")  # Ensure build tools are OK
        run(f"{pip_path} uninstall -y pyaudio || true")
        run(f"{pip_path} install pyaudio || {pip_path} install pipwin && pipwin install pyaudio")
    elif platform.system() == "Darwin":
        run(f"brew install portaudio")
        run(f'export LDFLAGS="-L/opt/homebrew/lib" CPPFLAGS="-I/opt/homebrew/include" && {pip_path} install pyaudio')
    else:
        run(f"{pip_path} install pyaudio")

    run(f"{pip_path} install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu")
    run(f"{pip_path} install openai-whisper streamlit spacy pyttsx3")
    run(f"{python_path} -m spacy download en_core_web_sm")

    config_dir = os.path.expanduser("~/.streamlit") if not is_windows else os.path.expanduser("~\\.streamlit")
    os.makedirs(config_dir, exist_ok=True)
    with open(os.path.join(config_dir, "config.toml"), "w") as f:
        f.write('[server]\nfileWatcherType = "none"\n')

    print("✅ Setup completed")

def main():
    check_python_version()
    create_venv()
    install_packages()

if __name__ == "__main__":
    main()
