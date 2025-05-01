import streamlit as st
import requests
from langdetect import detect
from gtts import gTTS
from io import BytesIO

# --- Groq API config ---
GROQ_API_KEY = "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"
GROQ_MODEL = "llama3-8b-8192"

# --- Bilingual FAQ Content ---
faq_context = """
ENGLISH FAQ

1. What time is check-in? → Between 4 PM and 8 PM. A concierge agent will contact you via WhatsApp on arrival day.
2. Is there luggage storage? → Yes. €15 large, €7.50 cabin, €5 small. Book via WhatsApp: +33 6 66 41 52 23.
3. Early check-in? → Yes if available: €40 (6-13h), €25 (13-15h), free after 16h.
4. Late check-in? → €25 (20-23h), €50 (23-1h), €70 (1-6h). Free between 16h–20h.
5. Can I cancel? → Free until 5 days before arrival.
6. Shuttle to Disneyland? → No. Use public buses (€2–€3).
7. Modifying my booking? → Contact the booking platform. If booked directly, contact us.
8. Airport to Disney? → RER B from CDG to Châtelet, then RER A to Marne-la-Vallée.
9. Can I leave bags before/after check-in? → No, but we offer luggage storage.
10. Linen provided? → Yes. Sheets and towels included.
11. Essentials provided? → Yes. Coffee, tea, soap, dishwasher tabs.
12. Parties allowed? → No. Guests and events are not permitted.
13. Why is a deposit required? → To cover damage. It’s a temporary bank hold, released 7 days after checkout.

---

FAQ EN FRANÇAIS

1. 🕓 Check-in → entre 16h00 et 20h00. Agent via WhatsApp le jour d’arrivée.
2. 🧳 Bagagerie → Oui : 15 €, 7,50 €, 5 € selon taille. Réservation via WhatsApp : +33 6 66 41 52 23.
3. ⏱️ Enregistrement anticipé → Oui si dispo : 40 € (6–13h), 25 € (13–15h), gratuit après 16h.
4. 🌙 Check-in tardif → 25 € (20–23h), 50 € (23–1h), 70 € (1–6h).
5. ❌ Annulation → Gratuite jusqu’à 5 jours avant l’arrivée.
6. 🚍 Navette Disneyland → Non. Bus locaux à 2–3 €.
7. 🔄 Modifier réservation → Contactez la plateforme. Réservation directe = contactez-nous.
8. ✈️ Aéroport à Disney → RER B (CDG → Châtelet), puis RER A → Marne-la-Vallée.
9. 🧳 Laisser les bagages → Non. Utilisez notre service de bagagerie.
10. 🛏️ Linge de maison → Oui. Draps et serviettes fournis.
11. ☕ Produits essentiels → Café, thé, savon, pastilles.
12. 🚫 Fêtes/interdits → Non autorisées.
13. 💳 Caution → Empreinte bancaire temporaire, libérée après le départ.


📌 **Check-in / Check-out**
- Check-in: 4 PM–8 PM (gratuit).
- Late check-in: €25 (8–11 PM), €50 (11 PM–1 AM), €70 (1–6 AM).
- Early check-in if available: €40 (6–1 PM), €25 (1–3 PM), free after 4 PM.
- No luggage drop-off before/after check-in inside apartment. Use luggage service.

🧳 **Luggage Storage**
- Yes. Large: €15, Cabin: €7.50, Small: €5.
- Arrival: Pickup at apartment or Disney, drop-off after cleaning.
- Departure: Pickup at apartment, delivery near Disney.
- Book via WhatsApp: +33 6 66 41 52 23 (24h in advance).
- Alternative: Locker at 13 Cours de l’Elbe, 77700 SERRIS (not NC-managed).

🛏️ **What’s provided**
- Linen & towels included.
- Welcome kit: coffee, tea, soap, toilet paper, dishwasher/laundry tabs.

❌ **Not allowed**
- Parties or external guests are strictly forbidden.

💳 **Security Deposit**
- Required: A temporary bank hold, not debited.
- Sent by secure link 24h before arrival.
- Released 7 days after checkout if no damage.

🚍 **Transport**
- No shuttle to Disneyland. Use bus (2–3€) or RER: CDG → Châtelet (RER B) → Marne-la-Vallée (RER A).

🔄 **Booking & Cancellation**
- Modification: Via booking platform. If direct booking → contact us.
- Free cancellation up to 5 days before arrival. Otherwise, fees apply.

📫 **Contact**
- Address: 7, rue des Rougeriots, 77600 Chanteloup-en-Brie
- Email: contact@ncconciergerie.fr
- Phone: 0645392052
- Working hours: Mon–Sat: 9:00 AM – 8:00 PM


"""

# --- Function to call Groq
# --- Groq API call ---
def ask_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": GROQ_MODEL, "messages": [{"role": "user", "content": prompt}]}

    try:
        res = requests.post(url, headers=headers, json=payload)
        res.raise_for_status()
        data = res.json()
        if "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"]
        else:
            return "Erreur : aucune réponse retournée par l'API."
    except requests.exceptions.RequestException as e:
        return f"Erreur API : {e}"

# --- Text-to-Speech Function ---
def speak(text, lang):
    tts = gTTS(text=text, lang=lang)
    audio_bytes = BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

# --- Streamlit UI ---
st.set_page_config(page_title="NC FAQ Chatbot", page_icon="🤖")
st.title("🤖 NC Conciergerie – FAQ Chatbot")
st.markdown("Posez vos questions / Ask your questions (🇫🇷 / 🇬🇧)")

user_input = st.text_input("💬 Votre question ici / Type your question here:")

if user_input:
    lang_detected = detect(user_input)
    lang_tts = 'fr' if lang_detected == 'fr' else 'en'

    prompt = f"""
    You are a polite multilingual FAQ assistant for NC Conciergerie.

    User language: {lang_detected.upper()}
    FAQ knowledge base:
    {faq_context}

    User's question:
    {user_input}

    Respond in the user's language. Keep it short, friendly, and accurate.
    """

    answer = ask_groq(prompt)
    st.markdown(f"**🧠 Réponse / Answer:**\n\n{answer}")

    audio = speak(answer, lang_tts)
    st.audio(audio, format="audio/mp3", start_time=0)