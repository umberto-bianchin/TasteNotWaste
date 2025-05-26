# audio_utils.py

import tempfile
import numpy as np
import sounddevice as sd
import whisper
import spacy
from scipy.io.wavfile import write


nlp = spacy.load("en_core_web_sm")
DEFAULT_DEVICE_INDEX = 5

def record_audio(duration=10, samplerate=16000, device=DEFAULT_DEVICE_INDEX):
    sd.default.device = (device, None)
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    return recording.flatten()

def transcribe_audio(audio, samplerate=16000):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        write(f.name, samplerate, (audio * 32767).astype(np.int16))
        path = f.name
    model = whisper.load_model("small")
    result = model.transcribe(path, language="en")
    return result["text"].strip()

def extract_filters(text, ingredientsName):
    doc = nlp(text)
    portions, max_time = 1, 30
    preferred, unwanted = [], []
    ingredients_lower = [i.lower() for i in ingredientsName]
    buy_ingredients = False

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
    
