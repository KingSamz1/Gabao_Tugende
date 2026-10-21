# Gabao Tugende — Streamlit website (English / Français)
# Run: streamlit run app.py
# Optional AI summaries: set OPENAI_API_KEY in your environment and install openai.
# All prices below are the prices supplied by the site owner; confirm them before publishing.

import os
import html
import sqlite3
from datetime import datetime
from urllib.parse import quote

import streamlit as st

st.set_page_config(
    page_title="Gabao Tugende | Study in Uganda",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

WHATSAPP_NUMBER = "256793839816"
WHATSAPP_DISPLAY = "(+256) 793 839 816"
ADDRESS = "Wasajja Road, Nalumunye, Kampala, Uganda"

TEXT = {
    "English": {
        "nav_home": "Home", "nav_english": "English course", "nav_courses": "Study in Uganda",
        "nav_ads": "Advertisements", "nav_contact": "Contact",
        "tagline": "Your bridge to higher education in Uganda",
        "hero_title": "Study in Uganda. Prepare for your future.",
        "hero_text": "Gabao Tugende supports Gabonese and other French-speaking students as they prepare to study in Uganda. From English-language preparation and university applications to visa guidance, accommodation and student support, we help you plan each step.",
        "start": "Explore programmes", "contact_us": "Contact our team",
        "about_title": "Why study in Uganda?",
        "about_text": "Uganda offers an English-speaking learning environment, a growing higher-education sector and opportunities to experience East African culture. Studying in English can help students build language skills and prepare for careers in regional and international settings. Admission, visa approval and programme availability are determined by the relevant institutions and authorities.",
        "makerere_title": "Why consider Makerere University?",
        "makerere_text": "Makerere University is one of Uganda’s best-known public universities, with a long history of teaching, research and professional training. In the QS Sub-Saharan Africa Rankings 2026, Makerere was listed 16th in Sub-Saharan Africa. Ranking positions vary by publisher, methodology and year, so rankings should always be labelled with their source.",
        "rank_note": "Ranking reference: QS Sub-Saharan Africa Rankings 2026. This is a regional ranking, not a claim that Makerere is among the top 16 universities in all of Africa.",
        "services_title": "How Gabao Tugende can help",
        "services": ["English-language school application and admission letter", "Guidance with student visa application", "Furnished accommodation options near the school", "University application and admission process support", "Guidance on university fee payment procedures", "Student medical insurance certificate coordination", "Pre-arrival guidance and practical student support"],
        "english_title": "Your 1-Year Intensive English Programme",
        "screening_fee": "Student document screening, qualification translation and equivalence, application/submission and administrative operations",
        "why_other_universities": "Why consider Makerere, Busitema and Victoria University?",
        "busitema_text": "Busitema University is a public university with programmes in areas including engineering, technology, agriculture and applied sciences. Confirm the current programme, intake and entry requirements directly with the university.",
        "victoria_text": "Victoria University is a private university in Kampala offering programmes across several professional and academic fields. Confirm current programme availability, accreditation and fees directly with the university.",
        "english_intro": "Build your English step by step through four progressive levels—Beginner, Elementary, Intermediate and Advanced. The programme is designed to help non-English-speaking international students strengthen their academic English and prepare for an English-proficiency assessment before applying for further studies at Makerere University. Exam eligibility and required scores must be confirmed with the university and the relevant testing body.",
        "levels": ["Beginner", "Elementary", "Intermediate", "Advanced"],
        "year_fee": "Annual tuition fee", "once": "one-time fee", "per_year": "per year", "per_month": "per month",
        "enquire": "Enquire for price", "course_title": "What can you study at Uganda’s universities?",
        "course_intro": "Explore selected programmes at Makerere University, Busitema University and Victoria University. Programme availability, titles, durations, admission criteria and fees must be verified with the relevant university before payment or travel arrangements.",
        "fee": "Programme tuition per academic year (functional fees included, as provided)",
        "admission": "Admission fee + admission letter", "visa": "Visa fee", "insurance": "Student medical insurance certificate",
        "accommodation": "Accommodation options", "apartment": "One-bedroom furnished apartment",
        "private_room": "One-bedroom furnished private guest room in a house",
        "sharing_room": "One-bedroom furnished shared guest room in a house",
        "minimum": "Minimum advance rent", "monthly": "monthly",
        "summary": "Course overview, benefits & career opportunities", "benefit": "Potential benefits",
        "jobs": "Possible career pathways", "whatsapp": "Ask about this programme on WhatsApp",
        "disclaimer": "Career pathways are examples, not guaranteed employment outcomes. Admission, fees, insurance, visas and accommodation are subject to provider and government confirmation.",
        "ads_title": "Advertise with Gabao Tugende", "ads_text": "Current announcements and partner advertisements will appear here.",
        "upload_ad": "Upload a banner advertisement", "ad_caption": "Advertisement caption (optional)",
        "contact_title": "Contact Gabao Tugende", "phone": "Phone / WhatsApp", "address": "Address",
        "send_message": "Message us on WhatsApp", "footer": "Gabao Tugende • Student support and study-abroad guidance",
        "search": "Search programmes", "filter": "Filter by subject area", "all": "All subject areas",
        "no_results": "No programmes match your search.", "programme": "Programme",
        "duration": "Duration", "year": "years", "school_fee": "English school annual fee",
        "english_admission": "English school admission fee + letter", "levels_title": "Four learning levels",
        "ranking_source": "Read Makerere's ranking update", "rank_label": "QS Sub-Saharan Africa Rankings 2026",
    },
    "Français": {
        "nav_home": "Accueil", "nav_english": "Cours d’anglais", "nav_courses": "Étudier en Ouganda",
        "nav_ads": "Publicités", "nav_contact": "Contact",
        "tagline": "Votre passerelle vers les études supérieures en Ouganda",
        "hero_title": "Étudiez en Ouganda. Préparez votre avenir.",
        "hero_text": "Gabao Tugende accompagne les étudiants gabonais et les autres étudiants francophones dans leur projet d’études en Ouganda. De la préparation en anglais aux démarches universitaires, en passant par l’orientation pour le visa, le logement et l’accompagnement étudiant, nous vous aidons à organiser chaque étape.",
        "start": "Découvrir les programmes", "contact_us": "Contacter notre équipe",
        "about_title": "Pourquoi étudier en Ouganda ?",
        "about_text": "L’Ouganda offre un environnement d’apprentissage anglophone, un secteur de l’enseignement supérieur en développement et une expérience culturelle d’Afrique de l’Est. Étudier en anglais permet de renforcer ses compétences linguistiques et de se préparer à des parcours professionnels régionaux et internationaux. L’admission, le visa et la disponibilité des programmes dépendent des établissements et autorités compétents.",
        "makerere_title": "Pourquoi envisager Makerere University ?",
        "makerere_text": "Makerere University est l’une des universités publiques les plus connues d’Ouganda, avec une longue tradition d’enseignement, de recherche et de formation professionnelle. Dans le classement QS Sub-Saharan Africa 2026, Makerere figurait à la 16e place en Afrique subsaharienne. Les positions varient selon l’organisme, la méthodologie et l’année ; toute référence doit donc préciser sa source.",
        "rank_note": "Référence : classement QS Sub-Saharan Africa 2026. Il s’agit d’un classement régional et non d’une affirmation selon laquelle Makerere serait parmi les 16 meilleures universités de toute l’Afrique.",
        "services_title": "Comment Gabao Tugende peut vous accompagner",
        "services": ["Candidature à l’école d’anglais et lettre d’admission", "Orientation pour la demande de visa étudiant", "Options de logements meublés près de l’école", "Accompagnement dans les démarches d’admission universitaire", "Orientation concernant les procédures de paiement des frais universitaires", "Coordination du certificat d’assurance médicale étudiant", "Conseils pratiques avant le départ et accompagnement étudiant"],
        "english_title": "Votre programme intensif d’anglais sur 1 an",
        "screening_fee": "Examen des documents, traduction et équivalence des qualifications, préparation/soumission du dossier et opérations administratives",
        "why_other_universities": "Pourquoi envisager Makerere, Busitema et Victoria University ?",
        "busitema_text": "Busitema University est une université publique proposant notamment des formations en ingénierie, technologie, agriculture et sciences appliquées. Confirmez directement le programme, la rentrée et les conditions d’admission.",
        "victoria_text": "Victoria University est une université privée située à Kampala proposant des formations dans plusieurs domaines. Vérifiez directement la disponibilité des programmes, leur accréditation et les frais.",
        "english_intro": "Progressez étape par étape grâce à quatre niveaux : Débutant, Élémentaire, Intermédiaire et Avancé. Ce programme vise à aider les étudiants internationaux non anglophones à renforcer leur anglais académique et à se préparer à une évaluation de compétence linguistique avant de poursuivre leurs études à Makerere University. Les examens acceptés et les scores requis doivent être confirmés auprès de l’université et de l’organisme d’examen.",
        "levels": ["Débutant", "Élémentaire", "Intermédiaire", "Avancé"],
        "year_fee": "Frais annuels", "once": "frais uniques", "per_year": "par an", "per_month": "par mois",
        "enquire": "Demander le tarif", "course_title": "Que peut-on étudier à Makerere University ?",
        "course_intro": "Découvrez une sélection de programmes de premier cycle. Les intitulés, durées, conditions d’admission et frais doivent être vérifiés auprès de Makerere University avant tout paiement ou organisation de voyage.",
        "fee": "Frais annuels du programme (frais fonctionnels inclus, selon les informations fournies)",
        "admission": "Frais d’admission + lettre d’admission", "visa": "Frais de visa", "insurance": "Certificat d’assurance médicale étudiant",
        "accommodation": "Options de logement", "apartment": "Appartement meublé d’une chambre",
        "private_room": "Chambre d’hôtes privée meublée dans une maison",
        "sharing_room": "Chambre d’hôtes meublée partagée dans une maison",
        "minimum": "Location à payer d’avance au minimum", "monthly": "par mois",
        "summary": "Présentation, avantages et débouchés possibles", "benefit": "Avantages potentiels",
        "jobs": "Débouchés possibles", "whatsapp": "Poser une question sur WhatsApp",
        "disclaimer": "Les débouchés sont des exemples et ne garantissent pas un emploi. L’admission, les frais, l’assurance, le visa et le logement doivent être confirmés par les prestataires et autorités concernés.",
        "ads_title": "Faites votre publicité avec Gabao Tugende", "ads_text": "Les annonces et publicités de partenaires apparaîtront ici.",
        "upload_ad": "Téléverser une bannière publicitaire", "ad_caption": "Légende de la publicité (facultatif)",
        "contact_title": "Contacter Gabao Tugende", "phone": "Téléphone / WhatsApp", "address": "Adresse",
        "send_message": "Nous écrire sur WhatsApp", "footer": "Gabao Tugende • Accompagnement étudiant et orientation pour les études à l’étranger",
        "search": "Rechercher un programme", "filter": "Filtrer par domaine", "all": "Tous les domaines",
        "no_results": "Aucun programme ne correspond à votre recherche.", "programme": "Programme",
        "duration": "Durée", "year": "ans", "school_fee": "Frais annuels de l’école d’anglais",
        "english_admission": "Frais d’admission à l’école d’anglais + lettre", "levels_title": "Quatre niveaux d’apprentissage",
        "ranking_source": "Lire l’annonce de classement de Makerere", "rank_label": "Classement QS Afrique subsaharienne 2026",
    },
}

# All amounts are FCFA and are intentionally kept as supplied by the site owner.
COURSES = [
    {"name":"Bachelor of Medicine and Bachelor of Surgery", "fr":"Bachelor of Medicine and Bachelor of Surgery (médecine et chirurgie)", "years":5, "fee":1600000, "area":"Health", "area_fr":"Santé", "summary":"A demanding medical programme focused on human health, clinical reasoning, diagnosis and patient care. It can build a foundation for further clinical training, subject to licensing requirements.", "summary_fr":"Un programme exigeant consacré à la santé humaine, au raisonnement clinique, au diagnostic et aux soins. Il peut constituer une base pour une formation clinique complémentaire, sous réserve des conditions d’autorisation d’exercice.", "benefit":"Develops scientific knowledge, clinical thinking and patient-care skills.", "benefit_fr":"Développe les connaissances scientifiques, le raisonnement clinique et les compétences de prise en charge des patients.", "jobs":"Doctor after required training, internship and registration; clinical research or public-health pathways may require additional qualifications.", "jobs_fr":"Médecin après les formations, stages et inscriptions obligatoires ; la recherche clinique et la santé publique peuvent exiger des qualifications supplémentaires."},
    {"name":"Bachelor of Science in Petroleum Geoscience and Production", "fr":"Bachelor of Science in Petroleum Geoscience and Production", "years":4, "fee":1600000, "area":"Engineering & Energy", "area_fr":"Ingénierie et énergie", "summary":"Studies geology, subsurface resources and petroleum production systems, combining earth science with energy-sector methods.", "summary_fr":"Étudie la géologie, les ressources du sous-sol et les systèmes de production pétrolière, en associant les sciences de la Terre aux méthodes du secteur énergétique.", "benefit":"Builds analytical, fieldwork and technical problem-solving skills.", "benefit_fr":"Développe l’analyse, le travail de terrain et la résolution de problèmes techniques.", "jobs":"Potential roles in energy operations, geoscience support, production support, environmental monitoring or further research; opportunities depend on industry demand.", "jobs_fr":"Emplois possibles dans les opérations énergétiques, l’appui géoscientifique, la production, le suivi environnemental ou la recherche ; les débouchés dépendent du marché."},
    {"name":"Bachelor of Nursing Science", "fr":"Bachelor of Nursing Science (sciences infirmières)", "years":4, "fee":1600000, "area":"Health", "area_fr":"Santé", "summary":"Prepares students in nursing science, patient assessment, health promotion and evidence-informed care.", "summary_fr":"Forme aux sciences infirmières, à l’évaluation des patients, à la promotion de la santé et aux soins fondés sur les données probantes.", "benefit":"Combines health science, communication and practical care skills.", "benefit_fr":"Associe sciences de la santé, communication et compétences pratiques de soins.", "jobs":"Nurse after applicable registration; hospital, community health, education or research roles may require experience or further study.", "jobs_fr":"Infirmier/ère après l’inscription réglementaire ; des postes hospitaliers, communautaires, pédagogiques ou de recherche peuvent exiger de l’expérience ou des études complémentaires."},
    {"name":"Bachelor of Science in Forestry", "fr":"Bachelor of Science in Forestry (sciences forestières)", "years":4, "fee":1800000, "area":"Environment & Agriculture", "area_fr":"Environnement et agriculture", "summary":"Covers forest ecosystems, conservation, forest management and sustainable use of natural resources.", "summary_fr":"Aborde les écosystèmes forestiers, la conservation, la gestion des forêts et l’utilisation durable des ressources naturelles.", "benefit":"Supports environmental stewardship, field assessment and sustainable resource planning.", "benefit_fr":"Favorise la protection de l’environnement, les évaluations de terrain et la planification durable des ressources.", "jobs":"Forestry officer, conservation project assistant, restoration work, environmental assessment or research support.", "jobs_fr":"Agent forestier, assistant de projet de conservation, restauration écologique, évaluation environnementale ou appui à la recherche."},
    {"name":"Bachelor of Science in Civil Engineering", "fr":"Bachelor of Science in Civil Engineering (génie civil)", "years":4, "fee":1600000, "area":"Engineering & Energy", "area_fr":"Ingénierie et énergie", "summary":"Studies the planning, design and construction of infrastructure such as buildings, roads, water systems and bridges.", "summary_fr":"Étudie la planification, la conception et la construction d’infrastructures : bâtiments, routes, systèmes d’eau et ponts.", "benefit":"Develops quantitative analysis, design and project coordination skills.", "benefit_fr":"Développe l’analyse quantitative, la conception et la coordination de projets.", "jobs":"Graduate engineer, site or project assistant, infrastructure technician or design support; professional registration may be required.", "jobs_fr":"Ingénieur débutant, assistant de chantier ou de projet, technicien d’infrastructure ou assistant en conception ; une inscription professionnelle peut être requise."},
    {"name":"Bachelor of Arts in Economics", "fr":"Bachelor of Arts in Economics (économie)", "years":3, "fee":1400000, "area":"Business & Social Sciences", "area_fr":"Commerce et sciences sociales", "summary":"Explores markets, public policy, data, incentives and how households, businesses and governments make decisions.", "summary_fr":"Explore les marchés, les politiques publiques, les données, les incitations et les décisions des ménages, entreprises et gouvernements.", "benefit":"Strengthens quantitative reasoning, research and policy analysis.", "benefit_fr":"Renforce le raisonnement quantitatif, la recherche et l’analyse des politiques publiques.", "jobs":"Economic or research assistant, banking and finance support, data analyst trainee, policy or programme assistant.", "jobs_fr":"Assistant économiste ou de recherche, appui en banque et finance, analyste de données débutant, assistant en politiques ou programmes."},
    {"name":"Bachelor of Science in Agricultural Engineering", "fr":"Bachelor of Science in Agricultural Engineering (génie agricole)", "years":4, "fee":1600000, "area":"Environment & Agriculture", "area_fr":"Environnement et agriculture", "summary":"Applies engineering principles to agricultural machinery, irrigation, post-harvest systems and farm productivity.", "summary_fr":"Applique les principes de l’ingénierie aux machines agricoles, à l’irrigation, aux systèmes après récolte et à la productivité des exploitations.", "benefit":"Combines engineering design with food systems and practical agricultural challenges.", "benefit_fr":"Associe la conception technique aux systèmes alimentaires et aux défis agricoles concrets.", "jobs":"Agricultural equipment or irrigation support, farm systems, agri-processing, project implementation or technical sales.", "jobs_fr":"Appui en équipements agricoles ou irrigation, systèmes agricoles, agro-transformation, mise en œuvre de projets ou vente technique."},
    {"name":"Bachelor of Science in Bioprocessing Engineering", "fr":"Bachelor of Science in Bioprocessing Engineering (génie des bioprocédés)", "years":4, "fee":1800000, "area":"Engineering & Energy", "area_fr":"Ingénierie et énergie", "summary":"Combines engineering, biology and process design for the production and processing of biological materials and products.", "summary_fr":"Associe ingénierie, biologie et conception de procédés pour produire et transformer des matières et produits biologiques.", "benefit":"Builds process, quality, laboratory and production-system knowledge.", "benefit_fr":"Développe les connaissances en procédés, qualité, laboratoire et systèmes de production.", "jobs":"Process or production assistant, quality-control support, biomanufacturing, food or pharmaceutical processing, or research support.", "jobs_fr":"Assistant procédés ou production, contrôle qualité, biofabrication, transformation alimentaire ou pharmaceutique, ou appui à la recherche."},
    {"name":"Bachelor of Science in Biomedical Engineering", "fr":"Bachelor of Science in Biomedical Engineering (génie biomédical)", "years":4, "fee":1600000, "area":"Engineering & Energy", "area_fr":"Ingénierie et énergie", "summary":"Applies engineering and technology to medical equipment, healthcare systems and biomedical problem-solving.", "summary_fr":"Applique l’ingénierie et la technologie aux équipements médicaux, aux systèmes de santé et aux problèmes biomédicaux.", "benefit":"Connects technical engineering skills with healthcare technology.", "benefit_fr":"Relie les compétences techniques de l’ingénierie aux technologies de santé.", "jobs":"Medical equipment support, biomedical technician pathways, clinical engineering support, product service or research; role requirements vary.", "jobs_fr":"Maintenance d’équipements médicaux, parcours de technicien biomédical, appui en ingénierie clinique, service produit ou recherche ; les exigences varient selon le poste."},
    {"name":"Bachelor of Science in Mechanical Engineering", "fr":"Bachelor of Science in Mechanical Engineering (génie mécanique)", "years":4, "fee":1600000, "area":"Engineering & Energy", "area_fr":"Ingénierie et énergie", "summary":"Covers mechanical systems, design, materials, manufacturing, energy and maintenance principles.", "summary_fr":"Aborde les systèmes mécaniques, la conception, les matériaux, la fabrication, l’énergie et la maintenance.", "benefit":"Develops design, technical analysis and systems troubleshooting.", "benefit_fr":"Développe la conception, l’analyse technique et le diagnostic de systèmes.", "jobs":"Mechanical or maintenance engineer pathway, manufacturing, plant operations, technical sales or project support.", "jobs_fr":"Parcours d’ingénieur mécanique ou maintenance, fabrication, exploitation d’usine, vente technique ou appui aux projets."},
    {"name":"Bachelor of Science in Computer and Communication Engineering", "fr":"Bachelor of Science in Computer and Communication Engineering", "years":4, "fee":1600000, "area":"Computing & Technology", "area_fr":"Informatique et technologie", "summary":"Combines computer systems, electronics, networks and communications technologies.", "summary_fr":"Associe les systèmes informatiques, l’électronique, les réseaux et les technologies de communication.", "benefit":"Builds hardware-software understanding and technical problem-solving.", "benefit_fr":"Développe la compréhension matériel-logiciel et la résolution de problèmes techniques.", "jobs":"Network or systems support, telecoms, embedded systems, technical operations or further specialisation.", "jobs_fr":"Support réseau ou systèmes, télécommunications, systèmes embarqués, opérations techniques ou spécialisation."},
    {"name":"Bachelor of Commerce", "fr":"Bachelor of Commerce (commerce)", "years":3, "fee":1400000, "area":"Business & Social Sciences", "area_fr":"Commerce et sciences sociales", "summary":"Introduces accounting, finance, business operations, marketing and management principles.", "summary_fr":"Présente la comptabilité, la finance, les opérations commerciales, le marketing et les principes de gestion.", "benefit":"Provides a broad foundation for business and financial decision-making.", "benefit_fr":"Fournit une base générale pour la prise de décision commerciale et financière.", "jobs":"Accounts or finance assistant, sales, procurement, administration, banking support or entrepreneurship.", "jobs_fr":"Assistant comptable ou financier, vente, achats, administration, appui bancaire ou entrepreneuriat."},
    {"name":"Bachelor of Business Administration", "fr":"Bachelor of Business Administration (administration des affaires)", "years":3, "fee":1600000, "area":"Business & Social Sciences", "area_fr":"Commerce et sciences sociales", "summary":"Focuses on management, organisational behaviour, marketing, operations and business strategy.", "summary_fr":"Se concentre sur la gestion, le comportement organisationnel, le marketing, les opérations et la stratégie d’entreprise.", "benefit":"Develops communication, teamwork, planning and leadership foundations.", "benefit_fr":"Développe les bases de la communication, du travail d’équipe, de la planification et du leadership.", "jobs":"Administrative or operations assistant, sales coordinator, customer service, project support or business ownership.", "jobs_fr":"Assistant administratif ou opérations, coordinateur commercial, service client, appui projet ou création d’entreprise."},
    {"name":"Bachelor of Science in Computer Science", "fr":"Bachelor of Science in Computer Science (informatique)", "years":3, "fee":1600000, "area":"Computing & Technology", "area_fr":"Informatique et technologie", "summary":"Studies programming, algorithms, software concepts, data and computer systems.", "summary_fr":"Étudie la programmation, les algorithmes, les concepts logiciels, les données et les systèmes informatiques.", "benefit":"Builds logical reasoning, coding and computational problem-solving skills.", "benefit_fr":"Développe le raisonnement logique, le codage et la résolution de problèmes informatiques.", "jobs":"Junior software developer, QA tester, IT support, data support or further study in specialised computing.", "jobs_fr":"Développeur logiciel junior, testeur QA, support informatique, appui données ou études spécialisées complémentaires."},
    {"name":"Bachelor of Human Resource Management", "fr":"Bachelor of Human Resource Management (gestion des ressources humaines)", "years":3, "fee":1600000, "area":"Business & Social Sciences", "area_fr":"Commerce et sciences sociales", "summary":"Covers recruitment, employee development, workplace relations, performance and HR administration.", "summary_fr":"Aborde le recrutement, le développement des employés, les relations professionnelles, la performance et l’administration RH.", "benefit":"Builds people-management, communication and organisational skills.", "benefit_fr":"Développe les compétences de gestion des personnes, de communication et d’organisation.", "jobs":"HR assistant, recruitment coordinator, training administrator, payroll support or office administration.", "jobs_fr":"Assistant RH, coordinateur de recrutement, administration de formation, appui paie ou administration de bureau."},
    {"name":"Bachelor of Science in Software Engineering", "fr":"Bachelor of Science in Software Engineering (génie logiciel)", "years":4, "fee":1800000, "area":"Computing & Technology", "area_fr":"Informatique et technologie", "summary":"Focuses on designing, building, testing and maintaining software systems through structured engineering methods.", "summary_fr":"Se concentre sur la conception, la création, les tests et la maintenance de logiciels selon des méthodes d’ingénierie structurées.", "benefit":"Builds software design, testing, teamwork and project delivery skills.", "benefit_fr":"Développe la conception logicielle, les tests, le travail en équipe et la livraison de projets.", "jobs":"Software developer, QA engineer, application support, web or mobile development and systems analysis.", "jobs_fr":"Développeur logiciel, ingénieur QA, support applicatif, développement web ou mobile et analyse de systèmes."},
    {"name":"Bachelor of Travel and Tourism Management", "fr":"Bachelor of Travel and Tourism Management (gestion du tourisme et des voyages)", "years":3, "fee":1600000, "area":"Business & Social Sciences", "area_fr":"Commerce et sciences sociales", "summary":"Studies tourism operations, travel services, destination planning, hospitality and visitor experience.", "summary_fr":"Étudie les opérations touristiques, les services de voyage, la planification des destinations, l’hôtellerie et l’expérience des visiteurs.", "benefit":"Develops customer service, coordination, communication and destination knowledge.", "benefit_fr":"Développe le service client, la coordination, la communication et la connaissance des destinations.", "jobs":"Tour operations, travel consultancy, hospitality, destination marketing, events or guest services.", "jobs_fr":"Opérations touristiques, conseil voyage, hôtellerie, marketing de destination, événements ou accueil."},
    {"name":"Bachelor of Science in Systems and Technology", "fr":"Bachelor of Science in Systems and Technology", "years":3, "fee":1600000, "area":"Computing & Technology", "area_fr":"Informatique et technologie", "summary":"A technology-oriented degree that may cover information systems, digital tools and organisational technology.", "summary_fr":"Un diplôme orienté technologie pouvant couvrir les systèmes d’information, les outils numériques et la technologie organisationnelle.", "benefit":"Can connect digital systems knowledge with organisational needs; confirm the exact curriculum with the university.", "benefit_fr":"Peut relier les connaissances des systèmes numériques aux besoins des organisations ; confirmez le programme exact auprès de l’université.", "jobs":"IT or systems support, digital operations, business systems support or further study, depending on the official curriculum.", "jobs_fr":"Support informatique ou systèmes, opérations numériques, support des systèmes d’entreprise ou poursuite d’études selon le programme officiel."},
    {"name":"Bachelor of Laws", "fr":"Bachelor of Laws (droit)", "years":4, "fee":1600000, "area":"Business & Social Sciences", "area_fr":"Commerce et sciences sociales", "summary":"Introduces legal systems, legislation, legal reasoning and methods of interpreting legal materials.", "summary_fr":"Présente les systèmes juridiques, la législation, le raisonnement juridique et l’interprétation des textes.", "benefit":"Strengthens argumentation, research, writing and critical analysis.", "benefit_fr":"Renforce l’argumentation, la recherche, la rédaction et l’analyse critique.", "jobs":"Legal assistant, compliance support, policy research or further professional legal training; practising law requires jurisdiction-specific steps.", "jobs_fr":"Assistant juridique, conformité, recherche en politiques publiques ou formation juridique complémentaire ; l’exercice du droit exige des démarches propres à chaque juridiction."},
    {"name":"Bachelor of Biomedical Laboratory", "fr":"Bachelor of Biomedical Laboratory (laboratoire biomédical)", "years":3, "fee":1600000, "area":"Health", "area_fr":"Santé", "summary":"Focuses on laboratory methods used to support disease investigation, diagnostics and health research.", "summary_fr":"Se concentre sur les méthodes de laboratoire qui soutiennent l’étude des maladies, le diagnostic et la recherche en santé.", "benefit":"Develops laboratory practice, accuracy, safety and scientific reporting.", "benefit_fr":"Développe la pratique de laboratoire, la précision, la sécurité et la rédaction scientifique.", "jobs":"Laboratory assistant or technologist pathways subject to programme recognition, registration and employer requirements; research support.", "jobs_fr":"Parcours d’assistant ou technologue de laboratoire sous réserve de reconnaissance du diplôme, d’inscription et des exigences employeur ; appui à la recherche."},
    {"name":"Bachelor of Science in Mining Engineering","fr":"Bachelor of Science en génie minier","years":4,"fee":1200000,"uni":"Busitema University","area":"Engineering & Energy","area_fr":"Ingénierie et énergie","summary":"Studies mineral resources, mine planning, extraction, safety and responsible resource development.","summary_fr":"Étudie les ressources minérales, la planification minière, l’extraction, la sécurité et le développement responsable des ressources.","benefit":"Combines engineering, geology, safety and operational problem-solving.","benefit_fr":"Associe ingénierie, géologie, sécurité et résolution de problèmes opérationnels.","jobs":"Possible pathways include mining engineer trainee, mine-planning support, safety or operations support, subject to requirements.","jobs_fr":"Débouchés possibles : ingénieur minier débutant, appui à la planification, à la sécurité ou aux opérations, selon les exigences."},
    {"name":"Bachelor of Science in Marine Engineering","fr":"Bachelor of Science en génie maritime","years":4,"fee":1200000,"uni":"Busitema University","area":"Maritime","area_fr":"Maritime","summary":"Focuses on marine machinery, propulsion, vessel systems, maintenance and maritime technical operations.","summary_fr":"Porte sur les machines marines, la propulsion, les systèmes des navires, la maintenance et les opérations techniques maritimes.","benefit":"Develops mechanical and systems knowledge relevant to marine operations.","benefit_fr":"Développe les connaissances mécaniques et systémiques utiles aux opérations maritimes.","jobs":"Possible pathways in marine engineering support, vessel maintenance and technical services; sea-going roles may require certification.","jobs_fr":"Débouchés possibles en appui maritime, maintenance de navires et services techniques ; les fonctions en mer peuvent exiger une certification."},
    {"name":"Bachelor of Science in Meteorology","fr":"Bachelor of Science en météorologie","years":3,"fee":1200000,"uni":"Makerere University","area":"Climate & Environment","area_fr":"Climat et environnement","summary":"Studies weather systems, atmospheric science, forecasting and climate variability.","summary_fr":"Étudie les systèmes météorologiques, les sciences de l’atmosphère, les prévisions et la variabilité climatique.","benefit":"Builds data interpretation, forecasting and environmental analysis skills.","benefit_fr":"Développe l’interprétation des données, la prévision et l’analyse environnementale.","jobs":"Possible pathways in meteorological services, climate research, disaster-risk support, aviation weather or environmental monitoring.","jobs_fr":"Débouchés possibles dans les services météorologiques, la recherche climatique, la prévention des risques, la météo aéronautique ou le suivi environnemental."},
    {"name":"Bachelor of Science in Artificial Intelligence and Data Science","fr":"Bachelor of Science en intelligence artificielle et science des données","years":3,"fee":1500000,"uni":"Victoria University","area":"Computing & Technology","area_fr":"Informatique et technologie","summary":"Combines programming, statistics, data analysis and AI methods to develop data-driven solutions.","summary_fr":"Associe programmation, statistiques, analyse de données et méthodes d’IA pour développer des solutions fondées sur les données.","benefit":"Builds analytical, computational and data-interpretation skills.","benefit_fr":"Développe les compétences analytiques, informatiques et d’interprétation des données.","jobs":"Possible pathways include junior data analyst, AI project assistant, business intelligence support or software/data roles with experience.","jobs_fr":"Débouchés possibles : analyste de données débutant, assistant de projet IA, appui en intelligence d’affaires ou postes logiciels/données avec expérience."},
    {"name":"Diploma in Marine Engineering","fr":"Diplôme en génie maritime","years":2,"fee":900000,"uni":"Busitema University","area":"Maritime","area_fr":"Maritime","summary":"Introduces marine engines, machinery, vessel maintenance and practical maritime engineering systems.","summary_fr":"Présente les moteurs marins, les machines, la maintenance des navires et les systèmes pratiques du génie maritime.","benefit":"Offers practical technical foundations for further study or entry-level support roles.","benefit_fr":"Apporte des bases techniques pratiques pour poursuivre les études ou accéder à des fonctions d’appui.","jobs":"Possible pathways include marine maintenance technician training, workshop support and engine-room support subject to certification.","jobs_fr":"Débouchés possibles : formation de technicien de maintenance maritime, atelier et appui en salle des machines sous réserve de certification."},
    {"name":"Bachelor of Science in Environmental Science","fr":"Bachelor of Science en sciences de l’environnement","years":3,"fee":1200000,"uni":"Makerere University","area":"Climate & Environment","area_fr":"Climat et environnement","summary":"Examines ecosystems, pollution, environmental assessment, conservation and sustainable resource management.","summary_fr":"Étudie les écosystèmes, la pollution, l’évaluation environnementale, la conservation et la gestion durable des ressources.","benefit":"Builds field research, environmental monitoring and sustainability skills.","benefit_fr":"Développe la recherche de terrain, le suivi environnemental et les compétences en durabilité.","jobs":"Possible pathways in environmental monitoring, conservation, sustainability, impact-assessment support or research.","jobs_fr":"Débouchés possibles dans le suivi environnemental, la conservation, la durabilité, les études d’impact ou la recherche."},
    {"name":"Diploma in Nautical Science","fr":"Diplôme en sciences nautiques","years":2,"fee":900000,"uni":"Busitema University","area":"Maritime","area_fr":"Maritime","summary":"Introduces navigation, seamanship, maritime safety and vessel operations.","summary_fr":"Présente la navigation, les pratiques maritimes, la sécurité et les opérations des navires.","benefit":"Builds foundational maritime knowledge; sea-going work may require approved training and certification.","benefit_fr":"Apporte des connaissances maritimes fondamentales ; le travail en mer peut exiger une formation et une certification reconnues.","jobs":"Possible pathways in maritime operations support or further nautical qualifications, subject to certification.","jobs_fr":"Débouchés possibles dans l’appui aux opérations maritimes ou des qualifications nautiques complémentaires, sous réserve de certification."}
]

# Assign institution labels to the earlier programme list too.
for _course in COURSES:
    _course.setdefault("uni", "Makerere University")

ACCOMMODATION = [
    {"key":"apartment", "price":250000, "months":4},
    {"key":"private_room", "price":170000, "months":6},
    {"key":"sharing_room", "price":130000, "months":6},
]

def money(value):
    return f"{value:,}".replace(",", " ") + " FCFA"

def whatsapp_url(message):
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={quote(message)}"

def tr(key):
    return TEXT[st.session_state.language][key]

def show_accommodation():
    st.markdown(f"**{tr('accommodation')}**")
    for item in ACCOMMODATION:
        st.write(f"• {tr(item['key'])}: **{money(item['price'])}/{tr('per_month')}** — {tr('minimum')}: **{item['months']} {('months' if st.session_state.language == 'English' else 'mois')}**")

def course_dialog(course):
    @st.dialog(course["name"] if st.session_state.language == "English" else course["fr"], width="large")
    def _dialog():
        lang = st.session_state.language
        name = course["name"] if lang == "English" else course["fr"]
        summary = course["summary"] if lang == "English" else course["summary_fr"]
        benefit = course["benefit"] if lang == "English" else course["benefit_fr"]
        jobs = course["jobs"] if lang == "English" else course["jobs_fr"]
        st.subheader(tr("fee"))
        st.markdown(f"### {money(course['fee'])}")
        st.caption(f"{course.get('uni', 'Makerere University')} • {tr('duration')}: {course['years']} {tr('year')}")
        st.write(f"**{tr('admission')}:** {money(90000)} ({tr('once')})")
        st.write(f"**{tr('visa')}:** {money(90000)} ({tr('once')})")
        st.write(f"**{tr('insurance')}:** {money(300000)} ({tr('per_year')})")
        show_accommodation()
        st.divider()
        st.subheader(tr("summary"))
        st.write(summary)
        st.markdown(f"**{tr('benefit')}**")
        st.write(benefit)
        st.markdown(f"**{tr('jobs')}**")
        st.write(jobs)
        st.caption(tr("disclaimer"))
        msg = ("Hello Gabao Tugende, please tell me more about the " + name +
               ", fees, admission requirements and application process." if lang == "English" else
               "Bonjour Gabao Tugende, merci de m'en dire plus sur le programme " + name +
               ", les frais, les conditions d'admission et la procédure de candidature.")
        st.link_button(tr("whatsapp"), whatsapp_url(msg), type="primary", use_container_width=True)
    _dialog()


# Advertisement approval workflow. SQLite stores uploads until an admin approves them.
DB_PATH = os.environ.get("GABAO_DB_PATH", "gabao_tugende.db")

def get_admin_password():
    try:
        secret = st.secrets.get("ADMIN_PASSWORD", "")
    except Exception:
        secret = ""
    return secret or os.environ.get("ADMIN_PASSWORD", "")

def db_connect():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    conn.row_factory = sqlite3.Row
    return conn

def init_ad_db():
    with db_connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS advertisements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL, caption TEXT DEFAULT '',
                filename TEXT NOT NULL, mime_type TEXT NOT NULL,
                image_data BLOB NOT NULL, status TEXT NOT NULL DEFAULT 'pending',
                submitted_at TEXT NOT NULL, reviewed_at TEXT DEFAULT NULL
            )
        """)

def save_ad(title, caption, uploaded_file):
    with db_connect() as conn:
        conn.execute(
            """INSERT INTO advertisements
            (title, caption, filename, mime_type, image_data, status, submitted_at)
            VALUES (?, ?, ?, ?, ?, 'pending', ?)""",
            (title.strip(), caption.strip(), uploaded_file.name,
             uploaded_file.type or "application/octet-stream", uploaded_file.getvalue(),
             datetime.utcnow().isoformat(timespec="seconds") + "Z")
        )

def get_ads(status=None):
    with db_connect() as conn:
        if status:
            return conn.execute("SELECT * FROM advertisements WHERE status=? ORDER BY id DESC", (status,)).fetchall()
        return conn.execute("SELECT * FROM advertisements ORDER BY id DESC").fetchall()

def update_ad_status(ad_id, status):
    with db_connect() as conn:
        conn.execute("UPDATE advertisements SET status=?, reviewed_at=? WHERE id=?",
                     (status, datetime.utcnow().isoformat(timespec="seconds") + "Z", ad_id))

init_ad_db()

# Header and language selector
with st.sidebar:
    st.markdown("## 🎓 Gabao Tugende")
    st.session_state.setdefault("language", "English")
    st.selectbox("Language / Langue", ["English", "Français"], key="language")
    st.markdown("---")
    st.markdown("### " + tr("tagline"))
    st.caption("🇬🇦 Gabon  →  🇺🇬 Uganda")
    st.link_button(tr("send_message"), whatsapp_url("Hello Gabao Tugende, I would like information about studying in Uganda." if st.session_state.language == "English" else "Bonjour Gabao Tugende, je souhaite obtenir des informations sur les études en Ouganda."), use_container_width=True)

# Navigation
pages = [tr("nav_home"), tr("nav_english"), tr("nav_courses"), tr("nav_ads"), tr("nav_contact")]
page = st.radio("Navigate / Navigation", pages, horizontal=True, label_visibility="collapsed", key="page_nav")

with st.sidebar:
    st.markdown("---")
    admin_view = st.checkbox("🔐 Admin: ad approvals / Administration : validation des publicités", key="show_admin_panel")

if admin_view:
    st.title("Advertisement approval / Validation des publicités")
    password = get_admin_password()
    if not password:
        st.error("Admin password is not configured. Set ADMIN_PASSWORD in environment variables or .streamlit/secrets.toml.")
        st.code("# .streamlit/secrets.toml\nADMIN_PASSWORD = \"replace-with-a-long-unique-password\"")
        st.stop()
    entered = st.text_input("Admin password / Mot de passe administrateur", type="password")
    if entered != password:
        st.info("Enter the administrator password to continue." if st.session_state.language == "English" else "Saisissez le mot de passe administrateur pour continuer.")
        st.stop()
    st.success("Administrator authenticated / Administrateur authentifié")
    st.subheader("Homepage banner / Bannière de la page d’accueil")
    with st.form("homepage_banner_upload", clear_on_submit=True):
        banner_caption = st.text_input("Homepage banner caption / Légende de bannière")
        banner_file = st.file_uploader("Upload homepage banner / Téléverser une bannière d’accueil", type=["png", "jpg", "jpeg", "webp"], key="homepage_banner_admin")
        publish_banner = st.form_submit_button("Publish homepage banner / Publier la bannière")
    if publish_banner:
        if not banner_file:
            st.error("Please select an image." if st.session_state.language == "English" else "Veuillez choisir une image.")
        else:
            save_ad("HOMEPAGE BANNER: Gabao Tugende", banner_caption, banner_file)
            # Banner uploads from the authenticated admin are approved immediately.
            with sqlite3.connect(DB_PATH) as _conn:
                _conn.execute("UPDATE advertisements SET status='approved' WHERE title='HOMEPAGE BANNER: Gabao Tugende' AND status='pending'")
            st.success("Homepage banner published." if st.session_state.language == "English" else "Bannière d’accueil publiée.")
            st.rerun()
    pending = get_ads("pending")
    st.subheader("Pending advertisements / Publicités en attente")
    if not pending:
        st.info("No pending advertisements." if st.session_state.language == "English" else "Aucune publicité en attente.")
    for ad in pending:
        with st.container(border=True):
            st.markdown("**" + ad["title"] + "**")
            if ad["caption"]:
                st.write(ad["caption"])
            st.image(ad["image_data"], use_container_width=True)
            st.caption(f"{ad['filename']} · {ad['submitted_at']}")
            c1, c2 = st.columns(2)
            if c1.button("Approve / Approuver", key=f"approve_{ad['id']}", type="primary", use_container_width=True):
                update_ad_status(ad["id"], "approved")
                st.rerun()
            if c2.button("Reject / Refuser", key=f"reject_{ad['id']}", use_container_width=True):
                update_ad_status(ad["id"], "rejected")
                st.rerun()
    st.subheader("Reviewed advertisements / Publicités examinées")
    for ad in [a for a in get_ads() if a["status"] in ("approved", "rejected")]:
        with st.expander(f"{ad['title']} — {ad['status']}"):
            st.image(ad["image_data"], use_container_width=True)
            if ad["status"] == "approved":
                if st.button("Unpublish / Retirer", key=f"unpublish_{ad['id']}"):
                    update_ad_status(ad["id"], "rejected")
                    st.rerun()
            elif st.button("Return to pending / Remettre en attente", key=f"repending_{ad['id']}"):
                update_ad_status(ad["id"], "pending")
                st.rerun()
    st.stop()

if page == tr("nav_home"):
    st.markdown("# 🎓 Gabao Tugende")
    st.caption(tr("tagline"))
    home_banners = [a for a in get_ads("approved") if a["title"].startswith("HOMEPAGE BANNER:")]
    if home_banners:
        st.image(home_banners[0]["image_data"], caption=home_banners[0]["caption"] or home_banners[0]["title"].replace("HOMEPAGE BANNER:", "").strip(), use_container_width=True)
    left, right = st.columns([1.35, 1])
    with left:
        st.title(tr("hero_title"))
        st.write(tr("hero_text"))
        st.button(tr("start"), type="primary",
                  on_click=lambda: st.session_state.update(page_nav=tr("nav_courses")),
                  use_container_width=True)
        st.link_button(tr("contact_us"), whatsapp_url("Hello Gabao Tugende, I would like to speak to your team." if st.session_state.language == "English" else "Bonjour Gabao Tugende, je souhaite parler à votre équipe."))
    with right:
        st.image("https://images.unsplash.com/photo-1523050854058-8df90110c9f1?auto=format&fit=crop&w=1200&q=85", use_container_width=True, caption="A future built through education")
    st.divider()
    st.header(tr("about_title"))
    st.write(tr("about_text"))
    st.header(tr("makerere_title"))
    st.write(tr("makerere_text"))
    st.subheader("Busitema University")
    st.write(tr("busitema_text"))
    st.subheader("Victoria University")
    st.write(tr("victoria_text"))
    st.info(tr("rank_note"))
    st.link_button(tr("ranking_source"), "https://magazine.qs.com/qs-insights-magazine-38/qs-sub-saharan-african-rankings-2026")
    st.divider()
    st.header(tr("services_title"))
    cols = st.columns(2)
    for i, service in enumerate(tr("services")):
        cols[i % 2].markdown(f"✅ {service}")
    st.caption(tr("disclaimer"))

elif page == tr("nav_english"):
    st.title(tr("english_title"))
    st.write(tr("english_intro"))
    cols = st.columns(4)
    for i, level in enumerate(tr("levels")):
        with cols[i]:
            st.markdown(f"### {i+1}. {level}")
            st.progress((i+1) / 4)
    st.divider()
    st.subheader(tr("year_fee"))
    st.markdown(f"## {money(700000)}")
    st.write(f"**{tr('screening_fee')}:** {money(350000)} ({tr('once')})")
    st.write(f"**{tr('english_admission')}:** {money(90000)} ({tr('once')})")
    st.write(f"**{tr('visa')}:** {money(90000)} ({tr('once')})")
    st.write(f"**{tr('insurance')}:** {money(300000)} ({tr('per_year')})")
    show_accommodation()
    st.link_button(tr("enquire"), whatsapp_url("Hello Gabao Tugende, please tell me more about the 1-year intensive English programme, total fees and enrolment." if st.session_state.language == "English" else "Bonjour Gabao Tugende, merci de m'informer sur le programme intensif d'anglais d'un an, les frais totaux et l'inscription."), type="primary", use_container_width=True)
    st.caption(tr("disclaimer"))

elif page == tr("nav_courses"):
    st.title(tr("course_title"))
    st.write(tr("course_intro"))
    query = st.text_input(tr("search"), placeholder="Medicine, engineering, business…" if st.session_state.language == "English" else "Médecine, ingénierie, commerce…")
    areas = sorted(set(c["area"] if st.session_state.language == "English" else c["area_fr"] for c in COURSES))
    selected_area = st.selectbox(tr("filter"), [tr("all")] + areas)
    visible = []
    for c in COURSES:
        name = c["name"] if st.session_state.language == "English" else c["fr"]
        area = c["area"] if st.session_state.language == "English" else c["area_fr"]
        if query.lower() in name.lower() and (selected_area == tr("all") or selected_area == area):
            visible.append(c)
    if not visible:
        st.info(tr("no_results"))
    for start in range(0, len(visible), 2):
        row = st.columns(2)
        for col, course in zip(row, visible[start:start+2]):
            with col:
                name = course["name"] if st.session_state.language == "English" else course["fr"]
                summary = course["summary"] if st.session_state.language == "English" else course["summary_fr"]
                st.markdown("### " + name)
                st.caption(f"{course.get('uni', 'Makerere University')} • {tr('duration')}: {course['years']} {tr('year')} • {money(course['fee'])}/{tr('per_year')}")
                st.write(summary)
                if st.button(tr("enquire"), key=f"enquire_{course['name']}", use_container_width=True):
                    course_dialog(course)
    st.caption(tr("disclaimer"))

elif page == tr("nav_ads"):
    st.title(tr("ads_title"))
    st.write(tr("ads_text"))
    st.markdown("### " + ("Approved advertisements" if st.session_state.language == "English" else "Publicités approuvées"))
    approved_ads = [a for a in get_ads("approved") if not a["title"].startswith("HOMEPAGE BANNER:")]
    if not approved_ads:
        st.info("No approved advertisements yet." if st.session_state.language == "English" else "Aucune publicité approuvée pour le moment.")
    else:
        for ad in approved_ads:
            st.image(ad["image_data"], use_container_width=True, caption=ad["caption"] or ad["title"])
            st.markdown("**" + html.escape(ad["title"]) + "**")
    st.divider()
    st.markdown("### " + ("Submit an advertisement for review" if st.session_state.language == "English" else "Soumettre une publicité pour validation"))
    st.write("Submitted banners appear publicly only after administrator approval." if st.session_state.language == "English" else "Les bannières ne seront visibles publiquement qu'après validation par un administrateur.")
    with st.form("ad_submission_form", clear_on_submit=True):
        ad_title = st.text_input("Advertisement title / Titre de la publicité", max_chars=120)
        ad_caption = st.text_input(tr("ad_caption"), max_chars=250)
        uploaded_ad = st.file_uploader(tr("upload_ad"), type=["png", "jpg", "jpeg", "webp"], key="public_ad_upload")
        ad_submit = st.form_submit_button("Submit for approval / Soumettre pour validation", type="primary")
    if ad_submit:
        if not ad_title.strip():
            st.error("Please enter an advertisement title." if st.session_state.language == "English" else "Veuillez saisir un titre pour la publicité.")
        elif uploaded_ad is None:
            st.error("Please upload a banner image." if st.session_state.language == "English" else "Veuillez téléverser une image de bannière.")
        else:
            save_ad(ad_title, ad_caption, uploaded_ad)
            st.success("Advertisement submitted and is pending admin approval." if st.session_state.language == "English" else "Publicité envoyée et en attente de validation.")
    st.divider()
    st.markdown("### " + ("Advertise with Gabao Tugende" if st.session_state.language == "English" else "Faire de la publicité avec Gabao Tugende"))
    st.link_button(tr("send_message"), whatsapp_url("Hello, I would like to advertise on the Gabao Tugende website." if st.session_state.language == "English" else "Bonjour, je souhaite faire de la publicité sur le site Gabao Tugende."))

else:
    st.title(tr("contact_title"))
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**{tr('phone')}**")
        st.write(WHATSAPP_DISPLAY)
        st.markdown(f"**{tr('address')}**")
        st.write(ADDRESS)
        st.link_button(tr("send_message"), whatsapp_url("Hello Gabao Tugende, I would like more information." if st.session_state.language == "English" else "Bonjour Gabao Tugende, je souhaite obtenir plus d'informations."), type="primary", use_container_width=True)
    with c2:
        st.markdown("### " + ("Send an enquiry" if st.session_state.language == "English" else "Envoyer une demande"))
        with st.form("contact_form"):
            name = st.text_input("Full name / Nom complet")
            email = st.text_input("Email")
            country = st.text_input("Country / Pays", value="Gabon" if st.session_state.language == "Français" else "")
            interest = st.selectbox("I am interested in / Je suis intéressé(e) par", ["English course", "Medicine", "Engineering", "Business", "Other"] if st.session_state.language == "English" else ["Cours d’anglais", "Médecine", "Ingénierie", "Commerce", "Autre"])
            details = st.text_area("Message / Message")
            submitted = st.form_submit_button("Prepare WhatsApp enquiry / Préparer la demande WhatsApp")
        if submitted:
            msg = f"Name: {name}\nEmail: {email}\nCountry: {country}\nInterest: {interest}\nMessage: {details}"
            st.link_button("Open WhatsApp with your enquiry", whatsapp_url(msg), type="primary")

st.divider()
st.caption(tr("footer") + " | " + ADDRESS)
