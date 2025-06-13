# audio_utils.py
import pyaudio
import wave
import tempfile
import whisper
import spacy


nlp = spacy.load("en_core_web_sm")

def record_audio(duration=10, filename=None, samplerate=44100):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = samplerate

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    frames = []
    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    if filename is None:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        filename = tmp.name

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename

def transcribe_audio(path):
    model = whisper.load_model("small")
    result = model.transcribe(path, language="en")
    return result["text"].strip()

def extract_filters(text, ingredientsName):
    doc = nlp(text)
    portions, max_time = 1, 30
    preferred, unwanted = [], []
    ingredients_lower = [i.lower() for i in ingredientsName]
    buy_ingredients = True

    word_to_num = {
        "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
        "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
        "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
        "fifteen": 15, "twenty": 20, "thirty": 30, "forty": 40,
        "fifty": 50, "sixty": 60
    }

    text_lower = text.lower()

    if any(phrase in text_lower for phrase in [
        "buy ingredients", "include missing", "add missing", "need to buy", "go shopping"
    ]): buy_ingredients = True
    elif any(phrase in text_lower for phrase in [
        "don't buy", "do not buy", "no shopping", "avoid shopping", "skip buying"
    ]): buy_ingredients = False

    for i, token in enumerate(doc):
        if token.text.lower() in ["person", "people", "persons"] and i > 0:
            prev = doc[i - 1].text.lower()
            if prev.isdigit():
                portions = int(prev)
            elif prev in word_to_num:
                portions = word_to_num[prev]
        if token.text.lower() in ["minute", "minutes"] and i > 0:
            try: max_time = int(doc[i - 1].text)
            except: pass
        if token.text.lower() in ingredients_lower:
            prev = doc[i - 1].text.lower() if i > 0 else ""
            if prev in ["without", "no", "exclude", "excludes"]:
                unwanted.append(token.text)
            elif prev in ["with", "include", "has", "containing"]:
                preferred.append(token.text)

    return {
        "portions": portions,
        "max_time": max_time,
        "preferred": list(set(preferred)),
        "unwanted": list(set(unwanted)),
        "buy": buy_ingredients
    }

def resolve_ingredient_name(name, ing_map):
    name = name.lower()
    if name in ing_map:
        return ing_map[name]
    if name.endswith("es") and name[:-2] in ing_map:
        return ing_map[name[:-2]]
    if name.endswith("s") and name[:-1] in ing_map:
        return ing_map[name[:-1]]
    print(f"[SKIPPED] Ingredient '{name}' not found in pantry.")
    return None
    
