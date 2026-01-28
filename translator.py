from deep_translator import GoogleTranslator
from langdetect import detect

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def translate_text(text, target_lang):
    return GoogleTranslator(source='auto', target=target_lang).translate(text)
