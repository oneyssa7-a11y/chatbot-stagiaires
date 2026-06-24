#!/usr/bin/env python3
"""
Chatbot Stagiaires — Ridcha Data — version Streamlit
Le moteur de recherche (FAQ, normalisation, scoring IDF/Jaccard) est inchangé
par rapport au script console d'origine. Seule l'interface change.
"""

import re
import unicodedata
from collections import Counter
from math import log

import streamlit as st

# ---------------------------------------------------------------------------
# FAQ
# ---------------------------------------------------------------------------

FAQ = {
    # — Entreprise —
    "Que fait l'entreprise ?": (
        "Ridcha Data est une entreprise française de services informatiques "
        "spécialisée dans les solutions de données, Cloud DevOps, "
        "cybersécurité et transformation numérique."
    ),
    "Quels sont les services proposés par Ridcha Data ?": (
        "Nous aidons les entreprises avec leurs outils informatiques, "
        "leurs données et la sécurité de leurs systèmes."
    ),
    "Qui sont les clients de l'entreprise ?": (
        "Des entreprises dans les secteurs de la banque, des télécoms, "
        "de l'automobile, de l'énergie, du commerce et de la santé."
    ),
    "Depuis quand l'entreprise existe-t-elle ?": (
        "Ridcha Data a été créée en 2013."
    ),
    "Où sont situés les bureaux ?": (
        "Le siège est à Montigny-le-Bretonneux, en région parisienne."
    ),
    "Quels sont les  jours et les horaires d'ouverture ?": (
        "Le lundi, jeudi et vendredi de 9h à 18h, le mardi et le mercredi nous sommes en télétravail."
    ),

    # — Services & tech —
    "Qu'est-ce que le Cloud DevOps ?": (
        "C'est une façon de créer et gérer des applications plus rapidement "
        "grâce à internet."
    ),
    "Proposez-vous du développement web ?": (
        "Oui, nous créons des sites web adaptés aux besoins de nos clients."
    ),
    "Quels langages de programmation utilisez-vous ?": (
        "Nous utilisons différents langages selon les projets : "
        "Java, Python et JavaScript notamment."
    ),
    "Pouvez-vous créer une application sur mesure ?": (
        "Oui, nous créons des applications personnalisées selon les besoins "
        "de chaque client."
    ),
    "Proposez-vous des services de cybersécurité ?": (
        "Oui, nous aidons à protéger les systèmes informatiques et les données "
        "des entreprises."
    ),
    "Quels services cloud fournissez-vous ?": (
        "Nous aidons les entreprises à stocker, gérer et sécuriser leurs données "
        "en ligne."
    ),

    # — Cybersécurité —
    "Comment créer un mot de passe sécurisé ?": (
        "Utilisez un mot de passe long avec des lettres, des chiffres "
        "et des caractères spéciaux."
    ),
    "Comment reconnaître un email de phishing ?": (
        "Méfiez-vous des messages qui demandent des informations personnelles "
        "ou contiennent des liens suspects."
    ),
    "Que faire si je clique sur un lien suspect ?": (
        "Déconnectez-vous immédiatement d'internet, prévenez le support "
        "informatique et ne saisissez aucun identifiant ni mot de passe."
    ),
    "Pourquoi l'authentification à deux facteurs est-elle importante ?": (
        "Elle ajoute une couche de sécurité supplémentaire à votre compte."
    ),
    "Comment protéger mes données personnelles ?": (
        "Utilisez des mots de passe forts et ne partagez pas vos informations "
        "sensibles."
    ),

    # — Accueil & tuteur —
    "À qui dois-je m'adresser en arrivant ?": (
        "À votre tuteur ou responsable de stage."
    ),
    "Qui sera mon tuteur ?": (
        "La personne désignée pour vous accompagner pendant votre stage, "
        "probablement Madame Berriche, la responsable des ressources humaines."
    ),
    "Que vais-je faire pendant mon stage ?": (
        "Vous participerez à différentes missions comme la création d'un projet "
        "ou la découverte de l'entreprise. Votre référent sera Monsieur Chammam."
    ),
    "Où puis-je trouver les informations importantes ?": (
        "Auprès de votre tuteur ou sur les outils internes."
    ),
    "Comment contacter mon équipe ?": (
        "Par email, téléphone ou messagerie interne."
    ),
    "À qui remettre les documents administratifs ?": (
        "Au service RH ou à votre tuteur."
    ),

    # — Informatique & matériel —
    "wifi": (
        "Le mot de passe Wi-Fi est affiché dans la salle principale, "
        "à côté du premier bureau près de la porte."
    ),
    "Ai-je accès au Wi-Fi ?": (
        "Oui, les informations de connexion vous seront fournies à votre arrivée."
    ),
    "Comment me connecter à mon ordinateur ?": (
        "L'entreprise ne fournit pas d'ordinateur ; il faut apporter le vôtre "
        "ou celui de votre établissement scolaire."
    ),
    "Puis-je utiliser mon ordinateur personnel ?": (
        "Oui, c'est même fortement recommandé puisque l'entreprise ne fournit "
        "pas d'ordinateurs."
    ),
    "Que faire si mon ordinateur ne fonctionne plus ?": (
        "Contactez le support informatique."
    ),
    "Comment installer un logiciel ou une application ?": (
        "Demandez l'autorisation ou l'aide d'un support informatique."
    ),
    "Puis-je utiliser une clé USB personnelle ?": (
        "Cela dépend des règles de sécurité de l'entreprise ; renseignez-vous "
        "auprès de votre tuteur."
    ),
    "Que faire si j'oublie mon mot de passe ?": (
        "Si c'est le mot de passe du site Ridcha Data Academy, demandez un "
        "renouvellement par email à la responsable des ressources humaines."
    ),

    # — Travail & projets —
    "Puis-je travailler à distance ?": (
        "Selon les règles définies par votre responsable."
    ),
    "Est-ce que je vais participer à des projets réels ?": (
        "Non, tu ne participeras pas à un projet réel mais tu devras réaliser "
        "un projet personnel qui bénéficie à l'entreprise (site web, IA, etc.)."
    ),
    "Que faire si je termine une mission ?": (
        "Demandez une nouvelle tâche à votre tuteur."
    ),
    "Comment demander de l'aide ?": (
        "En contactant votre tuteur ou un collègue."
    ),
    "Comment signaler un problème ?": (
        "Prévenez votre responsable ou le support informatique."
    ),
    "Comment puis-je progresser rapidement ?": (
        "Soyez curieux, posez des questions, pratiquez, et utilisez l'IA "
        "pour vos recherches."
    ),
    "Comment réussir mon stage ?": (
        "Soyez sérieux, curieux et impliqué."
    ),

    # — Évaluation & rapport —
    "Est-ce que je dois rédiger un rapport de stage ?": (
        "Cela dépend uniquement de votre établissement scolaire."
    ),
    "Puis-je demander un retour sur mon travail ?": (
        "Oui, n'hésitez pas à en faire la demande régulièrement à votre tuteur."
    ),
    "Est-ce que le stage est évalué ?": (
        "Cela dépend de votre niveau : en troisième, votre tuteur remplira "
        "probablement une grille d'évaluation ; en seconde, vous ne devriez "
        "normalement pas être évalué."
    ),

    # — Vie pratique —
    "Où puis-je déjeuner ?": (
        "Dans les espaces prévus à cet effet ou à proximité des bureaux."
    ),
    "Y a-t-il une salle de pause ?": (
        "Oui, elle vous sera indiquée par votre tuteur de stage."
    ),
    "Comment déclarer une absence ?": (
        "Prévenez votre tuteur à l'avance."
    ),
    "Que faire en cas de retard ?": (
        "Informez votre responsable dès que possible."
    ),
    "Puis-je utiliser mon téléphone pendant le travail ?": (
        "Oui, de manière raisonnable."
    ),
    "Que dois-je retenir pour bien commencer mon stage ?": (
        "Soyez ponctuel, motivé, respectueux et n'hésitez pas à poser "
        "des questions."
    ),

    # — Définitions tech —
    "Explique-moi ce qu'est l'intelligence artificielle.": (
        "L'intelligence artificielle permet à un ordinateur d'effectuer certaines "
        "tâches normalement réalisées par un humain."
    ),
    "Qu'est-ce qu'un projet informatique ?": (
        "Une mission visant à créer ou améliorer une solution numérique."
    ),
    "Ça veut dire quoi Cloud ?": (
        "Ce sont des services informatiques accessibles via internet."
    ),
    "C'est quoi la cybersécurité ?": (
        "C'est la protection des systèmes et des données contre les attaques."
    ),
    "Ça veut dire quoi développement web ?": (
        "C'est la création de sites internet."
    ),
    "Ça veut dire quoi développement mobile ?": (
        "C'est la création d'applications pour smartphones."
    ),
    "C'est quoi Python ?": (
        "Un langage de programmation simple, lisible et très populaire."
    ),
    "C'est quoi Java ?": (
        "Un langage utilisé pour créer des applications robustes et portables."
    ),
    "C'est quoi JavaScript ?": (
        "Un langage principalement utilisé pour rendre les sites web interactifs."
    ),
    "C'est quoi SQL ?": (
        "Un langage pour interroger et gérer des bases de données relationnelles."
    ),
    "C'est quoi une API ?": (
        "Un contrat qui permet à deux applications de communiquer entre elles."
    ),
    "C'est quoi un serveur ?": (
        "Un ordinateur (ou service cloud) qui fournit des ressources "
        "à d'autres ordinateurs."
    ),

    # — Entreprise (nouvelles) —
    "Combien de personnes travaillent ici ?": (
        "L'entreprise compte plusieurs collaborateurs spécialisés "
        "dans différents domaines."
    ),
    "Quels sont les métiers présents dans l'entreprise ?": (
        "Développeur, consultant, chef de projet, ingénieur cloud, "
        "expert en cybersécurité et responsable en ressources humaines."
    ),
    "Comment fonctionne une journée de travail ici ?": (
        "Les équipes travaillent sur leurs projets, participent à des réunions "
        "et collaborent ensemble."
    ),
    "Quels sont les principaux clients de l'entreprise ?": (
        "Des entreprises de différents secteurs comme la banque, la santé, "
        "les télécommunications et l'industrie."
    ),
    "Comment l'entreprise gagne-t-elle de l'argent ?": (
        "En réalisant des prestations et des projets pour ses clients."
    ),

    # — Rapport de stage —
    "Qu'est-ce que je peux mettre dans mon rapport de stage ?": (
        "Parlez de l'entreprise, de vos missions et de ce que vous avez appris."
    ),
    "Quelles questions poser à mon tuteur pour mon rapport de stage ?": (
        "Voici des questions utiles à poser à votre tuteur :\n"
        "  - Pourquoi avez-vous choisi ce métier ?\n"
        "  - Qu'aimez-vous dans votre travail ?\n"
        "  - À quoi ressemble votre journée type ?\n"
        "  - Quel a été votre premier emploi ?\n"
        "  - Quel projet vous a le plus marqué ?\n"
        "  - Quel est le plus grand défi de votre métier ?\n"
        "  - Que faut-il faire pour réussir dans ce domaine ?\n"
        "  - Quel est votre parcours professionnel ?"
    ),

    # — Métiers & carrière —
    "Comment crée-t-on un site web ?": (
        "En utilisant des langages de programmation comme HTML, CSS et JavaScript, "
        "ainsi que des outils de développement adaptés."
    ),
    "Quel diplôme faut-il pour travailler ici ?": (
        "Cela dépend du métier visé."
    ),
    "Quels sont les métiers les plus recherchés dans ce domaine ?": (
        "Développeur, ingénieur cloud, expert cybersécurité et data analyst."
    ),
    "Comment devenir développeur ?": (
        "En suivant une formation en informatique (BTS, licence, école d'ingénieurs "
        "ou autodidacte avec de la pratique)."
    ),
    "Comment devenir chef de projet ?": (
        "Avec de l'expérience et des compétences en gestion d'équipe et de planning."
    ),
    "Quels sont les avantages du métier ?": (
        "Apprendre en permanence, innover et résoudre des problèmes concrets."
    ),
    "Quelles sont les difficultés du métier ?": (
        "S'adapter aux nouvelles technologies qui évoluent très rapidement."
    ),
    "Quelles compétences sont importantes pour exercer ce métier ?": (
        "La logique, la curiosité et le travail en équipe."
    ),
    "Quels langages de programmation faut-il apprendre ?": (
        "Python, JavaScript ou Java sont de bons choix pour débuter."
    ),

    # — Informatique générale —
    "Comment fonctionne Internet ?": (
        "Il relie des millions d'ordinateurs dans le monde grâce à des protocoles "
        "de communication standardisés."
    ),
    "Qu'est-ce qu'un virus informatique ?": (
        "Un programme malveillant qui peut endommager un ordinateur ou voler des données."
    ),
    "Comment protéger son ordinateur ?": (
        "En le mettant régulièrement à jour et en utilisant un antivirus."
    ),
    "Pourquoi les données sont-elles importantes ?": (
        "Elles permettent de stocker et d'utiliser des informations utiles "
        "pour prendre de meilleures décisions."
    ),

    # — Vie en stage (nouvelles) —
    "Puis-je poser des questions à tout moment ?": (
        "Oui, c'est même conseillé ! Poser des questions montre votre curiosité."
    ),
    "Que faire si je fais une erreur ?": (
        "Le signaler à votre tuteur et chercher une solution ensemble."
    ),
    "Comment bien s'intégrer dans une équipe ?": (
        "En étant poli, curieux et respectueux envers tous les membres."
    ),
}

# ---------------------------------------------------------------------------
# Normalisation
# ---------------------------------------------------------------------------

SYNONYMS = {
    "wi-fi":                     "wifi",
    "wi fi":                     "wifi",
    "se connecter":              "connexion",
    "mdp":                       "mot de passe",
    "motpasse":                  "mot de passe",
    "mot-de-passe":              "mot de passe",
    "responsable":               "tuteur",
    "rh":                        "ressources humaines",
    "ressources":                "ressources humaines",
    "ouverture":                 "horaires",
    "heures":                    "horaires",
    "cybersecurite":             "cybersecurite",
    "securite":                  "cybersecurite",
    "assistance":                "support",
    "evaluation":                "evaluation",
    "teletravail":               "distance",
    "developpement":             "developpement",
    "intelligence artificielle": "ia",
}

STOPWORDS = {
    "je", "tu", "il", "elle", "nous", "vous", "on",
    "a", "au", "aux", "du", "des", "en", "sur", "pour", "par",
    "de", "d", "le", "la", "les", "un", "une",
    "et", "ou", "est", "sont", "que", "quoi",
    "comment", "quand", "avec", "dans",
    "si", "se", "mon", "ma", "mes", "votre", "vos",
    "ton", "ta", "tes", "ce", "c", "ca",
}


def strip_accents(s):
    return "".join(
        ch for ch in unicodedata.normalize("NFD", s)
        if unicodedata.category(ch) != "Mn"
    )


def normalize(text):
    text = strip_accents(text.lower())
    text = text.replace("-", " ").replace("/", " ")
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    for src, dst in SYNONYMS.items():
        text = re.sub(r"\b" + re.escape(src) + r"\b", dst, text)

    tokens = []
    for w in text.split():
        if w in STOPWORDS:
            continue
        if len(w) > 4 and w.endswith("s"):
            w = w[:-1]
        tokens.append(w)

    return " ".join(tokens)

# ---------------------------------------------------------------------------
# Index & score hybride IDF + Jaccard
# ---------------------------------------------------------------------------

_FAQ_INDEX = [
    (key, frozenset(normalize(key).split()))
    for key in FAQ
]

_N = len(FAQ)
_df = Counter()
for _, toks in _FAQ_INDEX:
    _df.update(toks)


# Mots interrogatifs dont la correspondance influence le score
QUESTION_WORDS = {
    "comment", "pourquoi", "quand", "qui", "quoi", "quel", "quelle",
    "quels", "quelles", "combien", "ou", "puis", "peut", "faut", "faire",
    "devenir", "creer", "proteger", "fonctionne", "signaler",
}


def _idf(token):
    return log((_N + 1) / (_df.get(token, 0) + 1)) + 1.0


def _jaccard(a, b):
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _weighted_overlap(query, key_tokens):
    return sum(_idf(t) for t in query & key_tokens)


def _question_word(norm_text):
    for w in norm_text.split():
        if w in QUESTION_WORDS:
            return w
    return None


def _score(q_tokens, k_tokens, q_norm, k_norm):
    s  = _weighted_overlap(q_tokens, k_tokens) * 2.0
    s += _jaccard(q_tokens, k_tokens) * 5.0

    if k_norm and k_norm in q_norm:
        s += 4.0

    if k_tokens and k_tokens.issubset(q_tokens):
        s += 3.0

    q_qw = _question_word(q_norm)
    k_qw = _question_word(k_norm)
    if q_qw and k_qw and q_qw != k_qw:
        s -= 3.0

    extra_in_key = k_tokens - q_tokens
    s -= len(extra_in_key) * 0.3

    return s

# ---------------------------------------------------------------------------
# Recherche
# ---------------------------------------------------------------------------

MIN_SCORE       = 1.0
MAX_SUGGESTIONS = 3


def find_answers(question):
    q_norm   = normalize(question)
    q_tokens = frozenset(q_norm.split())
    if not q_tokens:
        return []

    results = [
        (_score(q_tokens, k_tokens, q_norm, normalize(key)), key)
        for key, k_tokens in _FAQ_INDEX
    ]
    results.sort(key=lambda x: -x[0])
    return results


def extract_keywords(raw):
    s = raw.strip().lower()
    s = re.sub(r"^(mots[- ]cl[ee]s|keywords)\s*:\s*", "", s)
    s = strip_accents(s)
    s = re.sub(r"[^\w\s]", " ", s)
    return [w for w in normalize(s).split() if w]

# ---------------------------------------------------------------------------
# Réponse principale
# ---------------------------------------------------------------------------

def ask(question):
    question = question.strip()
    if not question:
        return "Pose-moi une question !"

    if re.match(r"(mots[- ]cl[ee]s|keywords)\s*:", question.lower()):
        kws = extract_keywords(question)
        if not kws:
            return "Aucun mot-cle detecte. Exemple : mots-cles: wifi horaires tuteur"
        question = " ".join(kws)

    results = find_answers(question)
    if not results:
        return "Je n'ai pas compris la question. Essaie avec des mots-cles."

    best_score, best_key = results[0]

    if best_score >= MIN_SCORE:
        return FAQ[best_key]

    candidates = [k for sc, k in results[:MAX_SUGGESTIONS] if sc > 0]
    if not candidates:
        return (
            "Je n'ai pas trouve de reponse.\n\n"
            "Essaie : mots-cles: wifi horaires tuteur mot de passe stage."
        )

    lines = ["Je ne suis pas sur d'avoir compris. Vouliez-vous dire :\n"]
    for i, c in enumerate(candidates, 1):
        lines.append("{}. {}".format(i, c))
    lines.append("\nPrecise ta question ou utilise la syntaxe mots-cles.")
    return "\n".join(lines)


# ===========================================================================
# INTERFACE STREAMLIT
# (à partir d'ici : tout remplace l'ancienne boucle console input()/print())
# ===========================================================================

st.set_page_config(
    page_title="Chatbot Stagiaires — Ridcha Data",
    page_icon="🤖",
    layout="centered",
)

# --- Mémoire de session : historique des messages affichés dans le chat ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Mémoire de session : historique des questions (équivalent de `history`
#     dans la version console, utilisé par la commande "historique") ---
if "history" not in st.session_state:
    st.session_state.history = []


# --- Sidebar : aide + historique + reset (remplace les commandes texte) ---
with st.sidebar:
    st.header("🤖 Chatbot Stagiaires")
    st.caption("Ridcha Data")

    st.markdown("---")
    st.subheader("Exemples de mots-clés")
    st.markdown(
        "`wifi` · `mot de passe` · `tuteur` · `horaires` · `stage` · "
        "`cybersécurité` · `api` · `python` · `cloud` · `ordinateur`"
    )

    st.markdown("---")
    st.subheader("Historique des questions")
    if st.session_state.history:
        for i, q in enumerate(st.session_state.history, 1):
            st.markdown(f"{i}. {q}")
    else:
        st.caption("Aucune question posée pour l'instant.")

    st.markdown("---")
    if st.button("🗑️ Effacer la conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()


# --- Zone principale ---
st.title("🤖 Chatbot Stagiaires")
st.caption("Pose tes questions sur l'entreprise, le stage, la sécurité, etc.")

# Message d'accueil si la conversation est vide
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown(
            "Bonjour ! 👋 Je suis le chatbot stagiaires de **Ridcha Data**.\n\n"
            "Tu peux me poser une question en langage naturel "
            "(ex : *Quels sont les horaires ?*) ou utiliser la syntaxe "
            "`mots-cles: wifi tuteur stage`."
        )

# Affichage de l'historique de conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Saisie utilisateur
if prompt := st.chat_input("Écris ta question..."):
    # 1. Afficher et mémoriser le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.history.append(prompt)
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Générer et afficher la réponse du bot
    with st.chat_message("assistant"):
        with st.spinner("Réflexion..."):
            response = ask(prompt)
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # 3. Rafraîchir la sidebar (nouvel historique)
    st.rerun()
