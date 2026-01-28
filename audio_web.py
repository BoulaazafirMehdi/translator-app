from gtts import gTTS
import tempfile

def speak_web(text, lang="fr"):
    tts = gTTS(text=text, lang=lang)
    file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(file.name)
    return file.name
