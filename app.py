import streamlit as st
from translator import translate_text, detect_language
from chatbot import chatbot_response
from history import save_history, load_history
from audio_web import speak_web
import PyPDF2
import docx

st.set_page_config(
    page_title="Translator App",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Application de Traduction Multilingue")

languages = {
    "Français": "fr",
    "Anglais": "en",
    "Arabe": "ar",
    "Espagnol": "es",
    "Allemand": "de",
    "Italien": "it"
}

menu = st.sidebar.selectbox(
    "Menu",
    ["Traduction Texte", "Fichier", "Chatbot", "Historique"]
)

# =============================
# TRADUCTION TEXTE
# =============================
if menu == "Traduction Texte":
    text = st.text_area("Entrer le texte")
    target = st.selectbox("Langue cible", list(languages.keys()))

    if st.button("Traduire"):
        if text.strip():
            src = detect_language(text)
            result = translate_text(text, languages[target])

            st.success(result)
            audio = speak_web(result, languages[target])
            st.audio(audio)

            save_history(text, result, src, languages[target])
        else:
            st.warning("Veuillez entrer un texte.")

# =============================
# FICHIER
# =============================
elif menu == "Fichier":
    file = st.file_uploader("Importer fichier", type=["txt", "pdf", "docx"])
    target = st.selectbox("Langue cible", list(languages.keys()))

    if file:
        content = ""

        if file.type == "text/plain":
            content = file.read().decode("utf-8")

        elif file.type == "application/pdf":
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                content += page.extract_text() or ""

        elif file.type.endswith("wordprocessingml.document"):
            doc = docx.Document(file)
            for p in doc.paragraphs:
                content += p.text + "\n"

        translated = translate_text(content, languages[target])

        st.text_area("Texte traduit", translated, height=300)
        audio = speak_web(translated, languages[target])
        st.audio(audio)

        st.download_button(
            "Télécharger la traduction",
            translated,
            file_name="traduction.txt"
        )

# =============================
# CHATBOT
# =============================
elif menu == "Chatbot":
    msg = st.text_input("Votre message")
    target = st.selectbox("Langue", list(languages.keys()))

    if st.button("Envoyer"):
        if msg.strip():
            rep = chatbot_response(msg, languages[target])
            st.write("🤖 Bot :", rep)

            audio = speak_web(rep, languages[target])
            st.audio(audio)
        else:
            st.warning("Écris un message.")

# =============================
# HISTORIQUE
# =============================
elif menu == "Historique":
    hist = load_history()

    if not hist:
        st.info("Aucun historique.")
    else:
        for h in reversed(hist):
            st.markdown(f"**{h['date']}**")
            st.write("Original :", h["original"])
            st.write("Traduit :", h["translated"])
            st.markdown("---")
