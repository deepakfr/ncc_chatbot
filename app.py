import streamlit as st
import requests
from langdetect import detect

# --- Groq API config ---
GROQ_API_KEY = "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"
GROQ_MODEL = "mixtral-8x7b-32768"

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


Question FAQ 1 :

📍À quelle heure puis-je effectuer mon check-in ?

Réponse FAQ 1:

✅Les check-in sont possibles entre 16h00 et 20h00. 

Pour organiser votre arrivée, nous programmerons un agent NC  conciergerie qui se chargera de vous remettre les clés et de vous fournir toutes les informations nécessaires pour votre séjour.

Cette agent NC conciergerie vous contactera via WhatsApp le jour de votre arrivée pour finaliser les détails et organiser au mieux votre accueil. 

Assurez-vous d’avoir renseigné un numéro de téléphone valide, fonctionnant sur WhatsApp.

N’hésitez pas à nous indiquer votre heure d’arrivée prévue afin que nous puissions planifier votre check-in dans les meilleures conditions.


Question FAQ 1:

📍Proposez-vous un service de bagagerie ?

Réponse FAQ 2:

✅Oui, nous proposons un service de bagagerie. Voici ce que vous devez savoir :

Tarifs :
	•	Élément supérieur à la taille d’un bagage cabine : 15 €
	•	Élément égal à la taille d’un bagage cabine : 7,50 €
	•	Élément inférieur à la taille d’un bagage cabine : 5 €

Détails du service :
	•	Pour votre arrivée :
Nous récupérons vos bagages à votre arrivée (à votre appartement ou près de Disney) à l’heure convenue, puis les déposons dans votre appartement une fois le ménage terminé.
	•	Pour votre départ :
Nous récupérons vos bagages à votre appartement et les déposons à l’endroit de votre choix (dans la zone proche de Disney).

Veuillez noter que ce service est disponible uniquement dans la zone autour de votre appartement et non pour la région parisienne.

Réservation :

Pour bénéficier de ce service, merci de nous contacter 24 heures à l’avance via WhatsApp au +33 6 66 41 52 23, en précisant :
	•	Ce que nous devons garder (taille et nombre des bagages).
	•	Le lieu et l’heure de récupération des bagages.
	•	L’adresse et l’heure de dépôt des bagages.

Alternative :
Si vous préférez, une bagagerie automatique est disponible à cette adresse :
13 Cours de l’Elbe, 77700 SERRIS (service non géré par NC Conciergerie).

N’hésitez pas à nous contacter pour toute question ou pour organiser ce service.

L’équipe NC.



Question FAQ 3 :

📍Puis-je demander un enregistrement anticipé ?

Réponse FAQ 3:

✅Les enregistrements anticipés sont possibles, mais ils sont soumis à disponibilité et à des frais supplémentaires en fonction de l’horaire demandé.

Horaires et tarifs :

	•	Entre 06h00 et 13h00 : 40 €*

	•	Entre 13h00 et 15h00 : 25 €*

	•	Entre 16h00 et 20h00 : Gratuit

(Ces majorations dépendent de la confirmation de notre service de ménage et des horaires de départ des clients précédents.)

Le paiement pour l’enregistrement anticipé se fait directement lors de la remise des clés.

Décision et confirmation :

La possibilité d’un enregistrement anticipé sera confirmée 24 heures avant votre arrivée afin de prendre en compte les départs précédents et le temps nécessaire pour préparer l’appartement dans les meilleures conditions.

Si vous souhaitez demander un enregistrement anticipé, merci de nous contacter. Nous organiserons cela au mieux selon les disponibilités.

L’équipe NC.


Question FAQ 4:

📍Puis-je effectuer un check-in tardif ?

Réponse généralisée pour votre FAQ 4:

✅Oui, il est possible d’effectuer un check-in tardif, c’est-à-dire en dehors des horaires légaux de check-in qui se situent entre 16h00 et 20h00. 
Des frais supplémentaires s’appliquent en fonction de l’heure de votre arrivée.

Horaires et tarifs :
	•	Entre 16h00 et 20h00 : Gratuit
	•	Entre 20h00 et 23h00 : 25 €
	•	Entre 23h00 et 01h00 : 50 €
	•	Entre 01h00 et 06h00 : 70 €

Ces frais supplémentaires couvrent la disponibilité de notre agent d’accueil, qui se rendra sur place pour vous recevoir en toute tranquillité, quel que soit l’horaire tardif de votre arrivée.

Le paiement de ces frais sera effectué directement lors de la remise des clés.

Réservation :

Si vous prévoyez une arrivée tardive, merci de nous en informer à l’avance afin que nous puissions organiser votre accueil dans les meilleures conditions.

L’équipe NC.


Question FAQ 5 :

📍Quels sont les horaires de check-in et que se passe-t-il si je souhaite arriver en dehors de ces horaires ?

Réponse FAQ 5:

✅ Les horaires d’enregistrement (check-in) sont spécifiés dès le processus de réservation afin de garantir une information claire et précise.

Horaires standards :

	•	Les check-in s’effectuent entre 16h00 et 20h00.

	•	En dehors de ces horaires, des frais supplémentaires s’appliquent pour les arrivées tardives (voir notre FAQ dédiée au check-in avancée ou tardif pour les tarifs).

Un e-mail automatique vous est envoyé 10 minutes après la confirmation de votre réservation pour rappeler ces horaires et détailler les frais éventuels après 20h00.

En cas de retard de vol ou autre motif :

Même en cas de retard de vol ou d’autres circonstances imprévues, la majoration pour un enregistrement tardif reste applicable. Ces frais couvrent la disponibilité de notre agent, qui sera présent pour vous accueillir en toute tranquillité malgré l’heure tardive.

L’équipe NC.


Question FAQ 6 :

📍Proposez-vous un service de navette gratuite vers Disneyland ?

Réponse FAQ 6 :

✅ Notre offre ne comprend pas de navette gratuite vers Disneyland. Cependant, des bus locaux circulent régulièrement vers cette destination moyennant un tarif d’environ 2 à 3 euros par personne par trajet.

Astuce pratique :

Pour simplifier votre trajet, nous vous recommandons d’utiliser des applications de navigation telles que Google Maps, qui vous fourniront des indications détaillées et vous guideront jusqu’à votre destination en toute tranquillité.

Nous espérons que ces informations vous seront utiles pour organiser vos déplacements.

L’équipe NC.


Question FAQ 7:

📍Puis-je modifier ma réservation directement avec vous ?

Réponse FAQ 7:

✅ Pour toute modification de votre réservation (changements de dates, nombre de personnes, etc.), il est nécessaire de contacter d’abord le service client de la plateforme de réservation où vous avez effectué votre réservation.

Processus de modification :

Une fois votre demande de modification soumise à la plateforme, nous serons notifiés et nous pourrons procéder à la mise à jour de votre réservation sur notre plateforme, en vérifiant la faisabilité de votre demande.

Veuillez comprendre que nous ne pouvons pas effectuer de modifications directement sur votre réservation, car celle-ci a été générée via une plateforme tierce, si elle a été générée sur notre site Internet, veuillez nous contacter directement!

L’équipe NC.


Question FAQ 8:

📍Comment me rendre de l’aéroport Charles de Gaulle à la gare de  Disneyland ?

Réponse FAQ 8:

✅Pour vous rendre de l’aéroport Charles de Gaulle à la gare de Disneyland Paris, voici l’itinéraire à suivre :

	1.	Prenez le RER depuis l’aéroport Charles de Gaulle (CDG) :
	•	Depuis l’aéroport, suivez les indications pour rejoindre la station RER située à l’aéroport. Les lignes RER B et RER D desservent CDG.

	•	Prenez un train en direction de Paris car un changement est nécessaire à Châtelet - Les Halles.

	2.	Changement à la station Châtelet - Les Halles :

	•	Descendez du RER à Châtelet - Les Halles, une gare de correspondance importante pour plusieurs lignes de métro et de RER.
	
•	Suivez les panneaux indiquant Marne-la-Vallée / Parc Disneyland et prenez le RER A en direction de Disneyland Paris.

	3.	Arrivée à Marne-la-Vallée Chessy :
	•	Descendez à la gare de Marne-la-Vallée Chessy, la station située directement à l’entrée du parc Disneyland.

Ce trajet est simple et direct, et des informations complémentaires sont disponibles à chaque étape de votre voyage.

Nous espérons que ces indications vous seront utiles pour planifier votre arrivée à Disneyland Paris.

L’équipe NC.

Question FAQ 9:

📍Puis-je laisser mes bagages avant l’heure du check-in ?

Réponse FAQ 9:

✅ Par mesure de sécurité et pour garantir une bonne organisation, il n’est pas possible de laisser vos bagages avant l’heure du check-in. 

Cela concerne tous nos clients, car le logement est préparé après le départ des précédents hôtes et avant votre arrivée.

Service de bagagerie disponible :

Important à savoir :

Nous ne pouvons pas autoriser le dépôt de bagages dans le logement le matin ou l’après-midi avant votre arrivée. Cela est dû à l’intervention systématique d’un service de ménage externe qui nettoie et prépare le logement pour votre séjour. Ce service a lieu après chaque départ, à partir de 11h00

Afin d’éviter toute responsabilité, nous ne pouvons donc pas permettre de laisser des bagages avant votre heure d’arrivée.

Cependant, nous proposons un service de bagagerie si vous avez besoin de stocker vos affaires avant l’heure d’enregistrement.

L’équipe NC.


Question FAQ  10:

📍Le logement fournit-il du linge de maison ?

Réponse généralisée pour votre FAQ 10:

✅ Oui, le logement est entièrement équipé en linge de lit et de bain pour la durée de votre séjour, comprenant draps, serviettes et couvertures. 

Toutefois, si vous avez besoin de linge supplémentaire ou souhaitez le renouveler, vous devez nous en informer.

L’équipe NC.


Question FAQ 11:

📍Le logement est-il équipé en produits tels que café, thé ou autres articles de première nécessité ?

Réponse FAQ 11 :

✅ Le logement inclut un kit d’accueil comprenant des articles de première nécessité tels que quelques capsules de café, thé, rouleaux de papier toilette, et shampoing.

De plus, bien que cela ne soit pas spécifiquement mentionné dans notre annonce, nous avons également mis à votre disposition quelques consommables de dépannage pour faciliter votre arrivée, incluant :

	•	Liquide vaisselle
	•	4 pastilles pour le lave-vaisselle et la machine à laver
	•	Savon pour les mains
	•	4 capsules de café
	•	2 rouleaux de papier toilette

Cependant, il vous appartient de réajuster ces éléments et d’acheter des produits supplémentaires selon la durée de votre séjour et vos besoins.

L’équipe NC.

Question FAQ 11 :

📍Puis-je laisser mes bagages dans l’appartement après le check-out ?

Réponse généralisée pour votre FAQ 11:

✅ Nous regrettons de vous informer qu’il n’est pas possible de laisser vos bagages dans l’appartement après votre départ, car le service de ménage doit préparer l’appartement pour les clients suivants arrivant le même jour. 
Les départs doivent impérativement se faire au plus tard à 11h00 afin de permettre cette organisation.

Cependant, nous proposons un service de bagagerie qui vous permettra de profiter de votre journée sans être encombré par vos valises, en toute tranquillité.

L’équipe NC.

Question FAQ 12:

📍Est-il possible d’organiser un événement ou de recevoir des invités dans l’appartement ?

Réponse FAQ 12:

✅ Comme spécifié dans notre règlement intérieur, il est strictement interdit d’organiser des événements ou de faire venir des personnes extérieures dans l’appartement. 

Cette mesure est mise en place pour garantir le calme et le respect du voisinage.

En cas de non-respect de cette règle, nous nous réservons le droit de demander au client de quitter l’appartement. De plus, des nuisances sonores ou des comportements perturbateurs peuvent entraîner des dégradations et des conflits avec les voisins.

Nous vous invitons à respecter ces conditions pour assurer un séjour serein et agréable pour tous.

L’équipe NC.



Question FAQ 13:

📍Pourquoi dois-je fournir une caution, et comment fonctionne-t-elle ?

Réponse FAQ 13:

Le dépôt de caution est une procédure standard et obligatoire pour garantir la location de nos hébergements. Voici ce que vous devez savoir :

	1.	Pourquoi une caution ?
	•	La caution est une empreinte bancaire qui permet de couvrir d’éventuels dommages causés dans l’appartement ou le non-respect des conditions de location.
	•	Elle garantit que le logement sera restitué dans l’état initial, conforme à ce qui est prévu dans les conditions de réservation.


	2.	Important à savoir :
	•	La caution est distincte du paiement de la réservation. Ce sont deux transactions séparées.
	•	Sans finalisation du paiement de la caution, nous ne pourrons pas transmettre les informations nécessaires à la remise des clés, et l’accès à l’hébergement sera refusé.
	

3. Comment déposer la caution ?
	•	Procédure pour déposer la caution :
	a).	Cliquez sur le lien sécurisé que vous recevrez 24 heures avant votre arrivée.
	b).	Assurez-vous d’avoir une connexion Internet stable et une carte bancaire avec des plafonds suffisants pour effectuer l’opération. 
Si votre carte est limitée, vous pouvez utiliser une autre carte bancaire.

	•	Restitution de la caution :
	a) La caution est réalisée via une empreinte bancaire (aucun montant n’est débité immédiatement).
	b) Cette empreinte bancaire est automatiquement libérée 7 jours après votre départ, à condition que :
	*.	L’appartement soit rendu en parfait état.
	**.	Toutes les conditions de location soient respectées.

	 A NOTER: 
Comme il s’agit d’une empreinte bancaire, aucun débit ni crédit n’apparaîtra sur votre relevé bancaire. La somme est simplement bloquée temporairement par votre banque, puis libérée par la suite.

L’équipe NC.






14.  Why do I need to provide a security deposit, and how does it work?
14.1. Why a security deposit?

The security deposit is a bank hold to cover potential damages to the apartment or non-compliance with rental conditions.

It ensures that the accommodation will be returned in its initial state, as specified in the booking conditions.

14.2. Important to know:

The security deposit is separate from the booking payment. These are two separate transactions.
Without finalizing the security deposit payment, we cannot provide the necessary information for key handover, and access to the accommodation will be denied.
14.3. How to provide the security deposit?

Procedure to provide the security deposit:

Click on the secure link you will receive 24 hours before your arrival.
Ensure you have a stable internet connection and a bank card with sufficient limits to complete the transaction.
If your card is limited, you can use another bank card.
Refund of the security deposit:

The security deposit is made via a bank hold (no amount is immediately debited).

This bank hold is automatically released 7 days after your departure, provided that:

The apartment is returned in perfect condition.
All rental conditions are respected.
<strong>NOTE:</strong> Since it is a bank hold, no debit or credit will appear on your bank statement. The amount is temporarily blocked by your bank and then released.



15. Do you offer a free shuttle service to Disneyland?

Our offer does not include a free shuttle to Disneyland. However, local buses run regularly to this destination for a fee of approximately €2 to €3 per person per trip.

Practical Tip:

To simplify your journey, we recommend using navigation apps such as Google Maps, which will provide detailed directions and guide you to your destination in complete peace of mind.

16. Can I cancel my booking without fees if unforeseen circumstances arise?
We understand that unforeseen circumstances, such as health issues or other situations (canceled flights, etc.), may arise before your stay.

However, according to our booking policy, free cancellations must be made at least 5 days before the scheduled arrival date.

Cancellation Conditions:

Free cancellation: up to 5 days before arrival
Cancellation after 5 days: cancellation fees apply
We regret that we cannot deviate from this rule if the cancellation occurs after this period. In this case, the options to check would be to contact your personal or bank insurance to see if a compensation or refund solution can be found.


17. What are the check-in times, and what happens if I want to arrive outside these hours?
Check-in times are specified during the booking process to ensure clear and accurate information.

Standard Times:

Check-ins are between 4:00 PM and 8:00 PM
Outside these hours, additional fees apply for late arrivals
An automatic email is sent 10 minutes after your booking confirmation to remind you of these times and detail any potential fees after 8:00 PM.

In case of flight delays or other unforeseen circumstances:

Even in case of flight delays or other unforeseen circumstances, the surcharge for late check-in remains applicable. These fees cover the availability of our agent, who will be present to welcome you in complete peace of mind despite the late hour.


18. Can I do a late check-in?
Yes, it is possible to do a late check-in, i.e., outside the legal check-in hours between 4:00 PM and 8:00 PM. Additional fees apply depending on your arrival time.

Times and Rates:

Between 4:00 PM and 8:00 PM: Free
Between 8:00 PM and 11:00 PM: €25
Between 11:00 PM and 1:00 AM: €50
Between 1:00 AM and 6:00 AM: €70
These additional fees cover the availability of our welcome agent, who will be on-site to welcome you in complete peace of mind, regardless of your late arrival time.

Payment for these fees will be made directly during key handover.

19. Question Luggage Handler Services
Do you need information about our luggage service?

Response
Here's what you need to know!

Rates:
Item larger than carry-on size: €15
Item equal to carry-on size: €7.50
Item smaller than carry-on size: €5
Details:
Luggage service booking for your arrival: Our team collects your luggage at your apartment or near Disney at your preferred time and then delivers it to your apartment once cleaning is complete.
Luggage service booking for your departure: We collect your luggage from your apartment and deliver it to your chosen location near Disney at your preferred time.
Please note that we do not serve the Paris region. This service is exclusively available in the area around your apartment.

If you are interested in this service, please fill out this form.


20. Can I request an early check-in?
Early check-ins are possible but are subject to availability and additional fees depending on the requested time.

Times and Rates:

Between 6:00 AM and 1:00 PM: €40*
Between 1:00 PM and 3:00 PM: €25*
Between 4:00 PM and 8:00 PM: Free
*These surcharges depend on the confirmation of our cleaning service and the departure times of previous guests.

Payment for early check-in is made directly during key handover.

Decision and Confirmation:

The possibility of early check-in will be confirmed 24 hours before your arrival to account for previous departures and the time needed to prepare the apartment under the best conditions.


21. Do you offer luggage storage services?
Yes, we offer luggage storage services. Here's what you need to know:

Rates:

Item larger than carry-on size: €15
Item equal to carry-on size: €7.50
Item smaller than carry-on size: €5
Service Details:

For your arrival: We collect your luggage upon arrival (at your apartment or near Disney) at the agreed time and deliver it to your apartment once cleaning is complete.
For your departure: We collect your luggage from your apartment and deliver it to your chosen location (in the area near Disney).
Please note that this service is only available in the area around your apartment and not for the Paris region.

Booking:

To use this service, please contact us 24 hours in advance via WhatsApp at +33 6 66 41 52 23, specifying:

What we need to store (size and number of luggage)
The location and time for luggage collection
The address and time for luggage delivery
Alternative:

If you prefer, an automatic luggage storage service is available at this address: 13 Cours de l'Elbe, 77700 SERRIS (service not managed by NC Conciergerie).

21. What time can I check in?
Check-in is available between 4:00 PM and 8:00 PM.

To organize your arrival, we will schedule an NC conciergerie agent who will hand over the keys and provide all necessary information for your stay.

This NC conciergerie agent will contact you via WhatsApp on the day of your arrival to finalize details and organize your welcome.

Please ensure you have provided a valid phone number that works on WhatsApp.

Feel free to let us know your expected arrival time so we can plan your check-in under the best conditions.



Other information 
MEET US
7, rue des Rougeriots 

77600 Chanteloup-en-Brie

CONTACT US
contact@ncconciergerie.fr

0645392052

OUR HOURS
Monday - Friday: 9:00am - 8:00pm
Saturday: 9:00am - 8:00pm


"""

# --- Function to call Groq
def ask_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gemma-7b-it",  # Use the short version
        "messages": [
            {"role": "user", "content": "What time is check-in?"}
        ],
        "temperature": 0.5
    }

    try:
        res = requests.post(url, headers=headers, json=data)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]

    except requests.exceptions.RequestException as e:
        st.error(f"🚨 Network/API error: {e}")
        st.code(res.text)  # Show raw response for debugging
        return "Sorry, we couldn't process your request."



# --- Streamlit UI ---
st.set_page_config(page_title="NC FAQ Chatbot", page_icon="🤖")
st.title("🤖 NC Conciergerie – FAQ Chatbot")
st.markdown("Posez vos questions / Ask your questions (🇫🇷 / 🇬🇧)")

user_input = st.text_input("💬 Votre question ici / Type your question here:")

if user_input:
    lang = detect(user_input)
    prompt = f"""
You are a polite multilingual FAQ assistant for NC Conciergerie.

User language: {lang.upper()}
FAQ knowledge base:
{faq_context}

User's question:
{user_input}

Respond in the user's language. Keep it short, friendly, and accurate.
"""
    answer = ask_groq(prompt)
    st.markdown(f"**🧠 Réponse / Answer:**\n\n{answer}")
