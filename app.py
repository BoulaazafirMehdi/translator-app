import streamlit as st
from translator import translate_text, detect_language
from history import save_history, load_history
from ocr import image_to_text
from chatbot import chatbot_response
from speech import voice_to_text
from audio_web import speak_web
from PIL import Image
import PyPDF2
import docx
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Traducteur Avancé",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CSS PERSONNALISÉ ----------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Variables globales */
    :root {
        --primary-color: #06B6D4;
        --secondary-color: #0891B2;
        --accent-color: #14B8A6;
        --bg-gradient: linear-gradient(135deg, #06B6D4 0%, #3B82F6 100%);
        --card-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Réinitialisation */
    .main {
        padding: 2rem 3rem;
        background: linear-gradient(to bottom right, #f8fafc, #f1f5f9);
    }
    
    /* Titre principal avec animation */
    h1 {
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem !important;
        margin-bottom: 0.5rem !important;
        animation: fadeInDown 0.8s ease-out;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Sous-titres */
    h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #1e293b !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar stylisée */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #06B6D4 0%, #3B82F6 100%);
        padding: 2rem 1rem;
    }
    
    .css-1d391kg .stSelectbox label, 
    [data-testid="stSidebar"] label {
        color: white !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }
    
    /* Cards avec effet glassmorphism */
    .stTextArea, .stTextInput, .stSelectbox {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: var(--card-shadow);
        transition: var(--transition);
    }
    
    .stTextArea:hover, .stTextInput:hover, .stSelectbox:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 50px rgba(0, 0, 0, 0.15);
    }
    
    /* Boutons modernes */
    .stButton > button {
        background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4);
        transition: var(--transition);
        cursor: pointer;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(6, 182, 212, 0.6);
        background: linear-gradient(135deg, #3B82F6 0%, #06B6D4 100%);
    }
    
    /* Messages de succès et info */
    .stSuccess {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 12px;
        padding: 1rem;
        border: none;
        font-family: 'Inter', sans-serif;
        animation: slideInRight 0.5s ease-out;
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    /* Conteneur de traduction */
    .translation-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: var(--card-shadow);
        margin: 1rem 0;
        border-left: 4px solid #06B6D4;
        animation: fadeIn 0.6s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* File uploader */
    .stFileUploader {
        background: white;
        border: 2px dashed #06B6D4;
        border-radius: 16px;
        padding: 2rem;
        transition: var(--transition);
    }
    
    .stFileUploader:hover {
        border-color: #3B82F6;
        background: rgba(6, 182, 212, 0.05);
    }
    
    /* Audio player */
    audio {
        width: 100%;
        border-radius: 12px;
        filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.1));
    }
    
    /* Historique */
    .history-item {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border-left: 3px solid #06B6D4;
        transition: var(--transition);
    }
    
    .history-item:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    /* Badges de langue */
    .lang-badge {
        display: inline-block;
        background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 100%);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0 0.25rem;
    }
    
    /* Divider stylisé */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, #06B6D4, transparent);
        margin: 2rem 0;
    }
    
    /* Sélecteurs de langue côte à côte */
    .language-selector {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin: 1rem 0;
    }
    
    /* Textarea amélioré */
    textarea {
        font-family: 'Inter', sans-serif !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
    }
    
    /* Badge de détection auto */
    .detected-lang {
        background: #f0fdf4;
        color: #166534;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-size: 0.9rem;
        font-weight: 500;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    /* Compteur de caractères */
    .char-counter {
        font-size: 0.85rem;
        color: #64748b;
        text-align: right;
        margin-top: 0.5rem;
    }
    
    /* Animation de chargement */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(6, 182, 212, 0.3);
        border-radius: 50%;
        border-top-color: #06B6D4;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# ---------------- TITRE AVEC SOUS-TITRE ----------------
st.markdown("""
    <h1>🌐 Traducteur Avancé</h1>
    <p style='font-family: Inter, sans-serif; font-size: 1.2rem; color: #64748b; margin-bottom: 2rem;'>
        Traduction instantanée • Multi-formats • Reconnaissance vocale & OCR
    </p>
""", unsafe_allow_html=True)

# ---------------- CONFIGURATION DES LANGUES ----------------
languages = {
    "🇫🇷 Français": "fr",
    "🇬🇧 Anglais": "en",
    "🇸🇦 Arabe": "ar",
    "🇪🇸 Espagnol": "es",
    "🇩🇪 Allemand": "de",
    "🇮🇹 Italien": "it",
    "🇵🇹 Portugais": "pt",
    "🇷🇺 Russe": "ru",
    "🇨🇳 Chinois": "zh-CN",
    "🇯🇵 Japonais": "ja",
    "🇰🇷 Coréen": "ko",
    "🇳🇱 Néerlandais": "nl",
    "🇹🇷 Turc": "tr",
    "🇵🇱 Polonais": "pl",
    "🇸🇪 Suédois": "sv"
}

# ---------------- MENU SIDEBAR MODERNE ----------------
st.sidebar.markdown("### 📋 Navigation")
menu = st.sidebar.selectbox(
    "Sélectionnez un mode",
    [
        "🔤 Traduction Texte",
        "🎤 Traduction Vocale",
        "🖼️ OCR - Image",
        "📄 Traduction Document",
        "🤖 Assistant Traduction",
        "📜 Historique"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ À propos")
st.sidebar.info("Application de traduction complète avec IA, OCR et reconnaissance vocale.")

# =========================
# 1️⃣ TRADUCTION TEXTE AVANCÉE
# =========================
if menu == "🔤 Traduction Texte":
    st.markdown("### ✍️ Traduction de Texte")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📝 Texte source")
        source_lang = st.selectbox(
            "Langue source",
            ["🔍 Détection automatique"] + list(languages.keys()),
            key="source_lang"
        )
        
        text = st.text_area(
            "Entrez votre texte",
            height=200,
            placeholder="Tapez ou collez votre texte ici...",
            key="source_text"
        )
        
        if text:
            char_count = len(text)
            st.markdown(f"<div class='char-counter'>{char_count} caractères</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🎯 Traduction")
        target = st.selectbox("Langue cible", list(languages.keys()), index=1, key="target_lang")
        
        if st.button("🚀 Traduire", use_container_width=True):
            if text:
                with st.spinner("Traduction en cours..."):
                    # Détection de langue
                    if source_lang == "🔍 Détection automatique":
                        detected = detect_language(text)
                        lang_name = [k for k, v in languages.items() if v == detected]
                        if lang_name:
                            st.markdown(
                                f"<div class='detected-lang'>✓ Langue détectée: {lang_name[0]}</div>",
                                unsafe_allow_html=True
                            )
                    else:
                        detected = languages[source_lang]
                    
                    # Traduction
                    result = translate_text(text, languages[target])
                    
                    # Affichage résultat
                    st.text_area(
                        "Résultat",
                        result,
                        height=200,
                        key="translation_result"
                    )
                    
                    # Sauvegarde historique
                    save_history(text, result, detected, languages[target])
                    
                    # Audio
                    st.markdown("#### 🔊 Écouter la traduction")
                    try:
                        audio = speak_web(result, languages[target])
                        st.audio(audio)
                    except Exception as e:
                        st.warning("Audio non disponible pour cette langue")
                    
                    # Boutons d'action
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.download_button(
                            "📥 Télécharger",
                            result,
                            file_name=f"traduction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            use_container_width=True
                        )
                    with col_b:
                        if st.button("🔄 Inverser les langues", use_container_width=True):
                            st.rerun()
            else:
                st.error("⚠️ Veuillez entrer du texte à traduire")

# =========================
# 2️⃣ TRADUCTION VOCALE
# =========================
elif menu == "🎤 Traduction Vocale":
    st.markdown("### 🎤 Traduction par Reconnaissance Vocale")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 🎙️ Parler")
        source_lang_voice = st.selectbox(
            "Langue parlée",
            list(languages.keys()),
            key="voice_source"
        )
        
        if st.button("🎤 Commencer l'enregistrement", use_container_width=True):
            with st.spinner("Écoute en cours..."):
                try:
                    # Conversion langue code pour reconnaissance vocale
                    lang_code = languages[source_lang_voice]
                    if lang_code == "en":
                        rec_code = "en-US"
                    elif lang_code == "fr":
                        rec_code = "fr-FR"
                    elif lang_code == "es":
                        rec_code = "es-ES"
                    elif lang_code == "de":
                        rec_code = "de-DE"
                    elif lang_code == "it":
                        rec_code = "it-IT"
                    elif lang_code == "ar":
                        rec_code = "ar-SA"
                    else:
                        rec_code = f"{lang_code}-{lang_code.upper()}"
                    
                    text = voice_to_text(rec_code)
                    st.session_state.voice_text = text
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'enregistrement: {str(e)}")
    
    with col2:
        st.markdown("#### 🎯 Traduction")
        target_voice = st.selectbox(
            "Langue cible",
            list(languages.keys()),
            index=1,
            key="voice_target"
        )
    
    # Affichage et traduction
    if 'voice_text' in st.session_state and st.session_state.voice_text:
        st.markdown("#### 📝 Texte reconnu")
        st.info(st.session_state.voice_text)
        
        if st.button("🚀 Traduire", use_container_width=True):
            with st.spinner("Traduction en cours..."):
                result = translate_text(st.session_state.voice_text, languages[target_voice])
                st.markdown("#### ✅ Traduction")
                st.success(result)
                
                # Audio de la traduction
                st.markdown("#### 🔊 Écouter")
                try:
                    audio = speak_web(result, languages[target_voice])
                    st.audio(audio)
                except:
                    st.warning("Audio non disponible")

# =========================
# 3️⃣ OCR IMAGE
# =========================
elif menu == "🖼️ OCR - Image":
    st.markdown("### 🖼️ Reconnaissance de Texte (OCR)")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📸 Image source")
        img = st.file_uploader(
            "Importer une image",
            type=["png", "jpg", "jpeg", "webp"],
            help="Formats supportés: PNG, JPG, JPEG, WEBP"
        )
        
        if img:
            image = Image.open(img)
            st.image(image, caption="Image téléchargée", use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Configuration")
        target_ocr = st.selectbox("Langue de traduction", list(languages.keys()), index=1)
    
    if img and st.button("🔍 Extraire et Traduire", use_container_width=True):
        with st.spinner("Analyse de l'image..."):
            try:
                # Extraction du texte
                text = image_to_text(image)
                
                if text:
                    st.markdown("#### 📝 Texte extrait")
                    st.text_area("Texte détecté", text, height=150)
                    
                    # Traduction
                    with st.spinner("Traduction..."):
                        translated = translate_text(text, languages[target_ocr])
                        
                        st.markdown("#### ✅ Traduction")
                        st.success(translated)
                        
                        # Audio
                        try:
                            audio = speak_web(translated, languages[target_ocr])
                            st.audio(audio)
                        except:
                            pass
                        
                        # Téléchargement
                        st.download_button(
                            "📥 Télécharger la traduction",
                            translated,
                            file_name="ocr_traduction.txt",
                            use_container_width=True
                        )
                else:
                    st.warning("⚠️ Aucun texte détecté dans l'image")
            except Exception as e:
                st.error(f"❌ Erreur lors de l'extraction: {str(e)}")

# =========================
# 4️⃣ TRADUCTION DOCUMENT
# =========================
elif menu == "📄 Traduction Document":
    st.markdown("### 📄 Traduction de Documents")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📂 Document source")
        file = st.file_uploader(
            "Importer un fichier",
            type=["txt", "pdf", "docx"],
            help="Formats supportés: TXT, PDF, DOCX"
        )
    
    with col2:
        st.markdown("#### 🎯 Configuration")
        target_doc = st.selectbox("Langue cible", list(languages.keys()), index=1)
    
    if file and st.button("📑 Traduire le document", use_container_width=True):
        with st.spinner("Lecture du document..."):
            content = ""
            
            try:
                # Extraction selon le type
                if file.type == "text/plain":
                    content = file.read().decode("utf-8")
                
                elif file.type == "application/pdf":
                    reader = PyPDF2.PdfReader(file)
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            content += page_text + "\n"
                
                elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    doc = docx.Document(file)
                    for paragraph in doc.paragraphs:
                        content += paragraph.text + "\n"
                
                if content:
                    st.markdown("#### 📄 Aperçu du contenu")
                    with st.expander("Voir le texte original"):
                        st.text_area("Contenu", content, height=200)
                    
                    # Traduction
                    with st.spinner("Traduction en cours..."):
                        translated = translate_text(content, languages[target_doc])
                        
                        st.markdown("#### ✅ Document traduit")
                        st.text_area("Traduction complète", translated, height=300)
                        
                        # Téléchargement
                        col_dl1, col_dl2 = st.columns(2)
                        with col_dl1:
                            st.download_button(
                                "📥 Télécharger TXT",
                                translated,
                                file_name=f"traduction_{file.name.split('.')[0]}.txt",
                                use_container_width=True
                            )
                        with col_dl2:
                            # Copier dans le presse-papiers (simulation)
                            st.button("📋 Copier", use_container_width=True)
                else:
                    st.error("❌ Impossible d'extraire le contenu du fichier")
            
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")

# =========================
# 5️⃣ ASSISTANT TRADUCTION (CHATBOT)
# =========================
elif menu == "🤖 Assistant Traduction":
    st.markdown("### 🤖 Assistant Intelligent de Traduction")
    
    # Initialisation de la conversation
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Configuration
    col_config1, col_config2 = st.columns(2)
    with col_config1:
        chat_lang = st.selectbox("Langue de conversation", list(languages.keys()), key="chat_lang")
    with col_config2:
        st.markdown("<div style='height: 47px;'></div>", unsafe_allow_html=True)
    
    # Affichage de l'historique
    st.markdown("#### 💬 Conversation")
    chat_container = st.container()
    
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                    <div style='background: #E0F2FE; padding: 1rem; border-radius: 12px; margin: 0.5rem 0;'>
                        👤 <strong>Vous:</strong> {msg['content']}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style='background: #DBEAFE; padding: 1rem; border-radius: 12px; margin: 0.5rem 0;'>
                        🤖 <strong>Assistant:</strong> {msg['content']}
                    </div>
                """, unsafe_allow_html=True)
    
    # Saisie du message
    col_msg, col_btn = st.columns([4, 1])
    with col_msg:
        msg = st.text_input(
            "Votre message",
            placeholder="Posez une question ou demandez une traduction...",
            key="chat_input",
            label_visibility="collapsed"
        )
    with col_btn:
        send_btn = st.button("📤 Envoyer", use_container_width=True)
    
    if send_btn and msg:
        # Ajouter le message de l'utilisateur
        st.session_state.messages.append({"role": "user", "content": msg})
        
        # Obtenir la réponse du chatbot
        with st.spinner("Réflexion..."):
            try:
                response = chatbot_response(msg, languages[chat_lang])
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"Désolé, une erreur s'est produite: {str(e)}"
                })
        
        st.rerun()
    
    # Bouton pour effacer la conversation
    if st.session_state.messages:
        if st.button("🗑️ Effacer la conversation"):
            st.session_state.messages = []
            st.rerun()

# =========================
# 6️⃣ HISTORIQUE MODERNE
# =========================
elif menu == "📜 Historique":
    st.markdown("### 📜 Historique des Traductions")
    
    history = load_history()
    
    if not history:
        st.info("📭 Aucune traduction dans l'historique")
    else:
        # Statistiques
        st.markdown("#### 📊 Statistiques")
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            st.metric("Total de traductions", len(history))
        with col_stat2:
            unique_langs = len(set([h.get('target_lang', '') for h in history]))
            st.metric("Langues utilisées", unique_langs)
        with col_stat3:
            total_chars = sum([len(h.get('original', '')) for h in history])
            st.metric("Caractères traduits", f"{total_chars:,}")
        
        st.markdown("---")
        
        # Filtres
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filter_lang = st.selectbox(
                "Filtrer par langue cible",
                ["Toutes"] + list(set([h.get('target_lang', 'N/A') for h in history]))
            )
        with col_f2:
            sort_order = st.selectbox("Trier par", ["Plus récent", "Plus ancien"])
        
        # Affichage de l'historique
        st.markdown("#### 📋 Traductions")
        
        filtered_history = history if filter_lang == "Toutes" else [
            h for h in history if h.get('target_lang') == filter_lang
        ]
        
        if sort_order == "Plus ancien":
            filtered_history = list(filtered_history)
        else:
            filtered_history = list(reversed(filtered_history))
        
        for idx, h in enumerate(filtered_history):
            with st.expander(
                f"🕒 {h.get('date', 'Date inconnue')} | "
                f"{h.get('source_lang', 'N/A')} → {h.get('target_lang', 'N/A')}"
            ):
                col_h1, col_h2 = st.columns(2)
                
                with col_h1:
                    st.markdown("**📝 Texte original**")
                    st.text_area(
                        "Original",
                        h.get('original', ''),
                        height=100,
                        key=f"orig_{idx}",
                        label_visibility="collapsed"
                    )
                
                with col_h2:
                    st.markdown("**✅ Traduction**")
                    st.text_area(
                        "Traduit",
                        h.get('translated', ''),
                        height=100,
                        key=f"trans_{idx}",
                        label_visibility="collapsed"
                    )
                
                # Boutons d'action
                col_a1, col_a2, col_a3 = st.columns(3)
                with col_a1:
                    st.download_button(
                        "📥 Télécharger",
                        h.get('translated', ''),
                        file_name=f"traduction_{idx}.txt",
                        key=f"dl_{idx}",
                        use_container_width=True
                    )
                with col_a2:
                    if st.button("🔄 Retraduire", key=f"retrans_{idx}", use_container_width=True):
                        st.info("Fonction à venir")
                with col_a3:
                    if st.button("🗑️ Supprimer", key=f"del_{idx}", use_container_width=True):
                        st.warning("Fonction de suppression à implémenter")
        
        # Bouton pour effacer tout l'historique
        st.markdown("---")
        if st.button("🗑️ Effacer tout l'historique", use_container_width=True):
            if st.button("⚠️ Confirmer la suppression"):
                st.info("Fonction de suppression globale à implémenter")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #64748b; padding: 2rem 0; font-family: Inter, sans-serif;'>
        <p>🌐 <strong>Traducteur Avancé</strong> | Propulsé par IA</p>
        <p style='font-size: 0.9rem;'>Traduction instantanée • Multi-formats • Reconnaissance vocale & OCR</p>
    </div>
""", unsafe_allow_html=True)