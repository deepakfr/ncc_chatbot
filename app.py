import streamlit as st
import requests
from langdetect import detect

# --- Groq API config ---
GROQ_API_KEY = "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"
GROQ_MODEL = "llama3-8b-8192"

# --- Compact JSON FAQ (25 Q&A) ---
faq_json = [
  {"id": 1, "question": "À quelle heure puis-je effectuer mon check-in ?", "answer": "Les check-in sont possibles entre 16h00 et 20h00. Un agent NC Conciergerie vous contactera via WhatsApp pour organiser votre arrivée. Assurez-vous d’avoir renseigné un numéro valide fonctionnant sur WhatsApp."},
  {"id": 2, "question": "Proposez-vous un service de bagagerie ?", "answer": "Oui, nous proposons un service de bagagerie avec des tarifs selon la taille : 15 € (grande), 7,50 € (moyenne), 5 € (petite). Service sur réservation via WhatsApp au +33 6 66 41 52 23, disponible uniquement autour de Disney."},
  {"id": 3, "question": "Puis-je demander un enregistrement anticipé ?", "answer": "Oui, selon disponibilité. Entre 6h et 13h : 40 €, entre 13h et 15h : 25 €. Gratuit entre 16h et 20h. Confirmation 24h avant l’arrivée."},
  {"id": 4, "question": "Puis-je effectuer un check-in tardif ?", "answer": "Oui. De 20h à 23h : 25 €, 23h à 1h : 50 €, 1h à 6h : 70 €. À régler sur place lors de la remise des clés."},
  {"id": 5, "question": "Que se passe-t-il si j’arrive en dehors des horaires de check-in ?", "answer": "Des frais s’appliquent selon l’heure. Un email automatique vous informe après votre réservation. Même en cas de retard de vol, les frais restent dus."},
  {"id": 6, "question": "Y a-t-il une navette gratuite vers Disneyland ?", "answer": "Non. Des bus locaux sont disponibles pour environ 2 à 3 € par trajet. Utilisez Google Maps pour vous orienter."},
  {"id": 7, "question": "Puis-je modifier ma réservation directement avec vous ?", "answer": "Non, les modifications doivent se faire via la plateforme de réservation. Si vous avez réservé sur notre site, contactez-nous directement."},
  {"id": 8, "question": "Comment aller de l’aéroport Charles de Gaulle à Disneyland ?", "answer": "Prenez le RER B vers Paris → changez à Châtelet-les-Halles → prenez le RER A vers Marne-la-Vallée Chessy (Disneyland)."},
  {"id": 9, "question": "Puis-je laisser mes bagages avant le check-in ?", "answer": "Non, pour des raisons de sécurité et d’organisation. Le service de ménage intervient après chaque départ. Utilisez notre service de bagagerie sur réservation."},
  {"id": 10, "question": "Le logement fournit-il du linge de maison ?", "answer": "Oui, linge de lit et serviettes sont inclus. Demandez si vous avez besoin de renouvellement."},
  {"id": 11, "question": "Y a-t-il des produits de base (café, savon, etc.) dans l’appartement ?", "answer": "Oui, un kit d’accueil est fourni : savon, liquide vaisselle, café, papier toilette, etc. À compléter selon vos besoins."},
  {"id": 12, "question": "Puis-je laisser mes bagages après le check-out ?", "answer": "Non, le ménage doit être fait avant les prochains clients. Un service de bagagerie est disponible sur demande."},
  {"id": 13, "question": "Puis-je organiser un événement ou recevoir des invités ?", "answer": "Non. Pour le respect du voisinage, les fêtes et invités extérieurs sont interdits. En cas d’infraction, expulsion possible."},
  {"id": 14, "question": "Pourquoi dois-je fournir une caution ?", "answer": "La caution couvre les dommages éventuels. Elle est prise par empreinte bancaire, non débitée, et libérée 7 jours après le départ si tout est conforme."},
  {"id": 15, "question": "What is the security deposit for?", "answer": "It ensures the apartment is returned in good condition. It is a bank hold, not an actual charge, released after 7 days."},
  {"id": 16, "question": "Can I cancel for free if something unexpected happens?", "answer": "Yes, but only if you cancel at least 5 days before arrival. After that, fees apply. Check with your insurance for potential refund."},
  {"id": 17, "question": "What are the check-in times and what if I’m late?", "answer": "Check-in: 4 PM – 8 PM. Late arrivals are subject to fees. You’ll receive an email with full details after booking."},
  {"id": 18, "question": "Can I do a late check-in?", "answer": "Yes. Between 8 PM and 11 PM: €25, 11 PM to 1 AM: €50, 1 AM to 6 AM: €70. To be paid at key handover."},
  {"id": 19, "question": "What is the luggage handler service?", "answer": "Pickup/delivery of luggage on arrival or departure near Disney. Costs depend on bag size. Reservation required via WhatsApp."},
  {"id": 20, "question": "Can I request an early check-in?", "answer": "Yes, subject to availability. 6–13h: €40, 13–15h: €25. Free from 16h. Confirmed 24h before arrival."},
  {"id": 21, "question": "Do you offer luggage storage services?", "answer": "Yes. Pickup and drop-off possible around Disney only. Reservation 24h in advance via WhatsApp."},
  {"id": 22, "question": "What time can I check in?", "answer": "Between 16h and 20h. You’ll be contacted via WhatsApp. Provide your estimated arrival time and valid number."},
  {"id": 23, "question": "What is your physical address?", "answer": "7, rue des Rougeriots, 77600 Chanteloup-en-Brie"},
  {"id": 24, "question": "What is your contact email?", "answer": "contact@ncconciergerie.fr"},
  {"id": 25, "question": "What are your opening hours?", "answer": "Monday to Saturday: 9:00am – 8:00pm"}
]

# --- Function to search FAQ ---
def search_faq(user_q):
    user_q_lower = user_q.lower()
    for entry in faq_json:
        if entry['question'].lower() in user_q_lower:
            return entry['answer']
    return None

# --- Streamlit UI ---
st.set_page_config(page_title="NC FAQ Chatbot", page_icon="🤖")
st.title("🤖 NC Conciergerie – FAQ Chatbot")
st.markdown("Posez vos questions / Ask your questions (🇫🇷 / 🇬🇧)")

user_input = st.text_input("💬 Votre question ici / Type your question here:")

if user_input:
    language = detect(user_input)
    faq_answer = search_faq(user_input)

    if faq_answer:
        st.markdown(f"**🧠 Réponse :**\n\n{faq_answer}")
    else:
        if language == "fr":
            st.warning("Désolé, je n'ai pas trouvé de réponse à votre question.")
        else:
            st.warning("Sorry, I couldn't find an answer to your question.")