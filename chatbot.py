import re
from translator import translate_text

def chatbot_response(message, lang):
    msg = message.lower()

    # calcul simple
    try:
        if re.search(r"\d+\s*[\+\-\*/]\s*\d+", msg):
            return f"Résultat : {eval(msg)}"
    except:
        pass

    if "bonjour" in msg or "salut" in msg:
        return "Bonjour 👋 Comment puis-je vous aider ?"

    if "qui es tu" in msg:
        return "Je suis un chatbot intégré à une application de traduction."

    if "merci" in msg:
        return "Avec plaisir 😊"

    return translate_text(message, lang)
