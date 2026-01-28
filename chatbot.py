import re
from translator import translate_text

# mémoire du chatbot
conversation_memory = []

def chatbot_response(message, lang):
    global conversation_memory

    msg = message.lower()
    conversation_memory.append(message)

    # ----------- CALCUL ----------
    try:
        if re.search(r"\d+\s*[\+\-\*/]\s*\d+", msg):
            result = eval(msg)
            return f"🧮 Le résultat est : {result}"
    except:
        pass

    # ----------- SALUTATIONS ----------
    if any(w in msg for w in ["bonjour", "salut", "hello", "hi"]):
        return "👋 Bonjour ! Je suis prêt à t’aider."

    # ----------- IDENTITÉ ----------
    if "qui es tu" in msg or "tu es qui" in msg:
        return (
            "🤖 Je suis un chatbot intelligent développé dans "
            "une application de traduction multilingue."
        )

    # ----------- CAPACITÉS ----------
    if "que peux tu faire" in msg:
        return (
            "Je peux traduire, discuter, faire des calculs, "
            "me souvenir de la conversation et répondre intelligemment 🙂"
        )

    # ----------- MÉMOIRE ----------
    if "tu te souviens" in msg:
        if len(conversation_memory) > 1:
            return f"Oui 😊 Tu as déjà dit : « {conversation_memory[-2]} »"
        else:
            return "C’est le début de notre discussion 🙂"

    # ----------- QUESTIONS SIMPLES ----------
    if "comment tu vas" in msg:
        return "Je vais très bien 😄 merci ! Et toi ?"

    if "merci" in msg:
        return "Avec plaisir 🙌"

    # ----------- TRADUCTION INTELLIGENTE ----------
    if "traduis" in msg or "traduire" in msg:
        return translate_text(message, lang)

    # ----------- RÉPONSE CONTEXTUELLE ----------
    if len(conversation_memory) >= 2:
        last = conversation_memory[-2].lower()
        if "bonjour" in last:
            return "🙂 Tu veux traduire quelque chose ?"

    # ----------- PAR DÉFAUT ----------
    return (
        "🤖 Je comprends partiellement ta demande. "
        "Tu peux me parler, me demander un calcul ou une traduction."
    )
