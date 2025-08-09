import streamlit as st
import pandas as pd
import re
import random
import time
from pathlib import Path

APP_DIR = Path(__file__).parent
CSV_PATH = APP_DIR / "datasetFIFA.csv"          # put the CSV next to HarifS.py
IMG_PATH = APP_DIR / "football-rb.png"          # put the image next to HarifS.py

@st.cache_data
def load_csv(p: Path):
    for enc in ("utf-8", "cp1252"):
        try:
            return pd.read_csv(p, encoding=enc)
        except Exception:
            pass
    raise FileNotFoundError(f"Could not read: {p}")

# Load CSV
if CSV_PATH.exists():
    df = load_csv(CSV_PATH)
else:
    st.error(f"❌ CSV not found at: {CSV_PATH}")
    st.stop()

# Sidebar image
if IMG_PATH.exists():
    st.sidebar.image(str(IMG_PATH), use_container_width=True)
else:
    st.sidebar.warning(f"⚠️ Image not found at: {IMG_PATH}")

WC_2022_STATS = {
    "total matches": 64,
    "total goals": 172,
    "teams count": 32,
    "host country": "Qatar",
    "duration days": 29,
    "stadiums count": 8,
    "champion": "Argentina",
    "runner up": "France",
    "third place": "Croatia",
    "fourth place": "Morocco",
    "top scorers": {
        "kylian mbappé": 8,
        "lionel messi": 7,
        "julián álvarez": 4,
        "olivier giroud": 4,
        "cody gakpo": 3,
        "marcus rashford": 3,
        "richarlison": 3,
        "bukayo saka": 3,
        "álvaro morata": 3,
        "gonçalo ramos": 3,
        "enner valencia": 3
    },
    "individual awards": {
        "golden ball": "Lionel Messi",
        "golden glove": "Emiliano Martínez",
        "best young player": "Enzo Fernández"
    },
    "opening match": {
        "teams": ("Qatar", "Ecuador"),
        "result": "0-2",
        "scorer highlight": "Enner Valencia scored twice"
    },
    "final match": {
        "teams": ("Argentina", "France"),
        "score": "3-3",
        "result": "Argentina won on penalties"
    },
    "matches count external": {
        "argentina": 7,
        "france": 7,
        "croatia": 7,
        "morocco": 7,
        "brazil": 5,
        "england": 5,
        "netherlands": 5,
        "portugal": 5,
        "japan": 4,
        "south korea": 4,
        "switzerland": 4,
        "usa": 4,
        "germany": 3,
        "poland": 3,
        "serbia": 3,
        "senegal": 3,
        "cameroon": 3,
        "ecuador": 3,
        "tunisia": 3,
        "canada": 3,
        "mexico": 3,
        "ghana": 3,
        "wales": 3,
        "iran": 3,
        "saudi arabia": 3,
        "australia": 3,
        "costarica": 3,
        "qatar": 3,
        "belgium": 3,
        "uruguay": 3,
        "denmark": 3
    }
}
WC_2022_QA = {
    # 🏆 General Information
    "location": "Qatar, the first Arab country to host the tournament",
    "dates": "November 20 to December 18, 2022",
    "teams count": 32,
    "matches count": 64,
    "stadiums count": "8 stadiums, all in Qatar",
    "first match": "Qatar vs Ecuador (2-0 for Ecuador)",
    "champion": "Argentina",
    "runner up": "France",
    "third place": "Croatia",
    "argentina wins": "3 times: 1978, 1986, and 2022",
    
    # 👑 Individual Awards
    "golden ball": "Lionel Messi (Argentina)",
    "golden boot": "Kylian Mbappé (France) - 8 goals",
    "golden glove": "Emiliano Martínez (Argentina)",
    "best young player": "Enzo Fernández (Argentina)",
    "fair play": "England national team",
    
    # ⚽️ Matches and Results
    "total goals": "172 goals - record number",
    "highest scoring match": "France 4-3 Argentina (Final after extra time, Argentina won 4-2 on penalties)",
    "first goal": "Enner Valencia (Ecuador)",
    "last goal": "Kylian Mbappé in the final (hat-trick)",
    "penalty shootouts": "5 matches decided by penalty shootouts",
    
    # 🌍 Teams and Groups
    "groups count": "8 groups (A to H)",
    "arab knockout": "Morocco",
    "first arab semifinal": "Morocco",
    "arab teams count": "4 teams: Qatar, Saudi Arabia, Tunisia, Morocco",
    "surprise team": "Morocco national team",
    
    # 🇸🇦 Arab Teams
    "saudi argentina": "Saudi Arabia (2-1)",
    "morocco achievement": "Fourth place, after losing to France and Croatia",
    "tunisia group": "Eliminated in group stage despite beating France",
    "qatar wins": "No, eliminated from group stage without any wins",
    "tunisia goal": "Wahbi Khazri",
    
    # 🧠 Key Details
    "argentina coach": "Lionel Scaloni",
    "france coach": "Didier Deschamps",
    "messi goals": 7,
    "mbappe goals": 8,
    "argentina goals final": ["Lionel Messi (2 goals)", "Ángel Di María"],
    "france goals final": ["Kylian Mbappé (hat-trick)"],
    "penalty shootout final": "4-2 for Argentina",
    "first penalty final since 2006": True,
    "final referee": "Szymon Marciniak (Poland)",
    "teams beat champ runner": ["Saudi Arabia (beat Argentina)", "Tunisia (beat France)"],
    
    # 🎉 Notable Events
    "oldest player": "Milan Borjan (Canada) - born 1987",
    "youngest scorer": "Jude Bellingham (England) - 19 years old",
    "semi automated offside": "Yes, for the first time",
    "var used": "Yes",
    "highest scoring team": "France - 16 goals",
    "messi last world cup": "He said it was his last, but didn't officially retire after the tournament",
    "argentina penalties": "Twice: against Netherlands in quarterfinals and against France in final",
    "morocco spain": "0-0 draw, Morocco won 3-0 on penalties",
    "super hattrick": "No, highest was hat-trick (Mbappé)",
    "messi scored every round": "Yes, scored in group stage, round of 16, quarterfinals, semifinals, and final",
    
    # ⚽️ Teams and Matches (51-75)
    "argentina croatia": "Argentina 3-0",
    "croatia brazil scorers": "Neymar (Brazil) and Bruno Petković (Croatia)",
    "croatia brazil result": "4-2 on penalties after 1-1 draw",
    "morocco france": "France won 2-0",
    "france final appearances": "Twice (2018, 2022)",
    "england win": "No, eliminated in quarterfinals against France",
    "portugal switzerland": "Gonçalo Ramos (hat-trick)",
    "ronaldo switzerland": "No, he was on the bench",
    "germany group stage": "No, eliminated on goal difference",
    "group of death qualified": "Japan and Spain",
    "japan spain goal": "Ao Tanaka",
    "japan goal technology": "No, video technology showed the ball partially remained in play",
    "group stage surprise": "Japan",
    "saudi argentina first goal": "Saleh Al Shehri",
    "saudi argentina winning goal": "Salem Al Dawsari",
    "morocco wins": "3 wins in regulation time + 2 penalty shootout wins",
    "morocco belgium scorers": "Abdelhamid Sabiri and Zakaria Aboukhlal",
    "tunisia australia": "Australia won 1-0",
    "qatar senegal": "Senegal won 3-1",
    "african beat european": "Yes, like Morocco against Belgium and Spain",
    "senegal wins": "Twice (against Qatar and Ecuador)",
    "morocco top scorer": "Youssef En-Nesyri (2 goals)",
    "morocco portugal goal": "Youssef En-Nesyri",
    "brazil penalties": "Yes, against Croatia",
    "mbappe goals every round": "No, didn't score in semifinals",
    
    # 📊 Stats and Records (76-100)
    "messi goals": 7,
    "messi assists": 3,
    "most assists": "Antoine Griezmann (France) - 3 assists",
    "red cards": "Only 4 red cards",
    "first red card": "Goalkeeper Wayne Hennessey (Wales)",
    "penalties awarded": 23,
    "fastest goal": "Alphonso Davies (Canada) vs Croatia - 2nd minute",
    "thousandth goal": "Marcus Rashford (England)",
    "most goals conceded": "Costa Rica (11 goals)",
    "least goals conceded": "Morocco (only 1 goal conceded until semifinals)",
    "most goals scored": "France (16 goals)",
    "highest scoring group match": "England 6-2 Iran",
    "most draws": "United States (3 draws)",
    "best penalty saver": "Emiliano Martínez (Argentina)",
    "total goals record": "172 goals - broke 1998 and 2014 record (171 goals)",
    "highest possession": "Spain - 76% in some matches",
    "total attendance": "Over 3.4 million spectators",
    "average attendance": "Approximately 53,000 spectators per match",
    "highest attendance match": "Argentina vs Mexico - 88,966 spectators",
    "most minutes played": "Nikola Vlašić (Croatia) - over 720 minutes",
    "most world cup appearances player": "Lionel Messi - 26 World Cup matches",
    "players 5 world cups": "Messi, Ronaldo, goalkeeper Guillermo Ochoa, and others",
    "most goals by substitutes": "Portugal (4 goals by substitutes in one match)",
    "most penalty goals conceded": "Poland (against France and Argentina)",
    
    # 🧠 Additional Stats and Events (101-125)
    "only hattrick final": "Kylian Mbappé (France)",
    "other hattrick": "Gonçalo Ramos (Portugal vs Switzerland)",
    "biggest win": "England 6-2 Iran",
    "best defence until semifinal": "Morocco (conceded only 1 goal which was an own goal)",
    "own goal vs morocco": "Nayef Aguerd (against Canada)",
    "argentina matches": 7,
    "argentina goals": 15,
    "argentina penalties converted": "4 (3 scored by Messi)",
    "most penalty shootout wins": "Argentina - twice",
    "france vs african": "Yes, against Tunisia in group stage, lost 1-0",
    "ronaldo goal": "Yes, scored a penalty against Ghana",
    "most chances created": "France",
    "most shots": "Mbappé",
    "france goals": 16,
    "di maria final": "Yes, scored Argentina's second goal",
    "croatia third place goal": "Joško Gvardiol",
    "argentina losses": "Once (against Saudi Arabia)",
    "japan germany": "Japan won 2-1",
    "japan goals scorers": "Ritsu Dōan and Takuma Asano",
    "germany goal": "İlkay Gündoğan",
    "canada goal": "Alphonso Davies",
    "qatar points": "Zero - lost all matches",
    "most passes": "Rodri (Spain)",
    "croatia coach": "Zlatko Dalić",
    "croatia semifinals": "3 times (1998, 2018, 2022)",
    
    # 🏟️ Stadiums and Organization (126-150)
    "stadiums used": 8,
    "stadiums names": ["Lusail", "Al Bayt", "974", "Al Thumama", "Al Janoub", "Education City", "Ahmad bin Ali", "Khalifa International"],
    "final venue": "Lusail Stadium",
    "lusail capacity": "88,966 spectators",
    "semi automated offside used": "Yes",
    "smart ball tech": "Ball with internal sensor to precisely detect touch time",
    "final referee": "Szymon Marciniak (Poland)",
    "female referee": "Yes, like Stéphanie Frappart (first woman to referee men's World Cup match)",
    "referees count": "36 referees, 69 assistant referees, 24 VAR officials",
    "winter world cup": "Yes, in November/December instead of June/July",
    "last 32 teams": "Yes, 2026 will have 48 teams",
    "stadium 974 built": "Yes, from shipping containers - first temporary demountable stadium",
    "stoppage time goals": "Many goals - long stoppage time added in most matches",
    "official ball name": "Al Rihla by Adidas",
    "mascot name": "La'eeb",
    "official songs": ["Hayya Hayya (Better Together)", "Arhbo"],
    "global artists": "Yes, like Jungkook from BTS",
    "france wins": "Twice (1998, 2018)",
    "france final losses": "Twice (2006, 2022)",
    "morocco coach": "Walid Regragui",
    "morocco coach first": "Yes, appointed months before tournament",
    "controversial refereeing": "Yes, notably in Portugal vs Morocco match",
    "belgium group stage exit": "Yes",
    "croatia third place goals": ["Joško Gvardiol", "Mislav Oršić"],
    "asian beat european": "Yes: Japan beat Germany and Spain, Saudi Arabia beat Argentina"
}

FOLLOW_UP_QUESTIONS = {
    'goal': [
        "What's your favorite goal celebration from the tournament?",
        "Which player do you think scored the most beautiful goal?",
        "Do you remember any crucial late goals that changed matches?",
        "Which goal do you think was the most important of the tournament?"
    ],
    'result': [
        "What was the most surprising result for you?",
        "Which underdog performance impressed you the most?",
        "Do you think any team exceeded expectations?",
        "Which comeback victory was the most dramatic?"
    ],
    'tournament': [
        "What was your favorite moment of the World Cup?",
        "Which young player impressed you the most?",
        "How do you think the next World Cup will compare?",
        "Which team had the best tournament strategy?"
    ],
    'player': [
        "Who would you pick as player of the tournament?",
        "Which emerging star surprised you the most?",
        "Do you think any player deserved more recognition?",
        "Which player's performance was the most underrated?"
    ],
    'team': [
        "Which team had the best attacking play?",
        "What surprised you most about team performances?",
        "How do you rate the underdog teams' performances?",
        "Which team's defensive organization impressed you?"
    ],
    'general': [
        "What's your most memorable World Cup moment?",
        "Which stadium had the best atmosphere in your opinion?",
        "How do you think VAR affected the tournament?",
        "What was the biggest lesson from this World Cup?"
    ],
    
    "golden boot": [
        "Do you want to know how many goals Mbappé scored?",
        "Interested in who was second in the scoring chart?"
    ],
    "golden ball": [
        "Want to know Messi's stats during the tournament?",
        "Would you like details on his goals and assists?"
    ],
    "total goals": [
        "Do you want to know the average goals per match?",
        "Curious which match had the most goals?"
    ],
    "host country": [
        "Want to learn about Qatar's preparations?",
        "Interested in stadiums used during the event?"
    ],
    "champion": [
        "Want to know how Argentina reached the final?",
        "Interested in the final match scoreline?"
    ]
}

RESPONSES = {
    "golden boot": [
        "Mbappé secured the Golden Boot in Qatar 2022.",
        "Top scorer of 2022? It was Kylian Mbappé!"
    ],
    "golden ball": [
        "Messi was awarded the Golden Ball for his outstanding performance.",
        "No surprise – Messi was the best player in the tournament."
    ],
    "total goals": [
        "172 goals were netted during the tournament – a new record!",
        "The 2022 edition saw the highest goal tally ever: 172."
    ],
    "host country": [
        "Qatar made history as the first Arab country to host the World Cup.",
        "The desert heat? Yep – Qatar hosted the 2022 tournament."
    ],
    "champion": [
        "Argentina lifted the trophy after a dramatic final.",
        "La Albiceleste won their third World Cup title in 2022."
    ]
}

#___________________________________________________________________________
def clean_text(text):
    return text.lower().strip()

def extract_keywords(user_input: str):
    words = user_input.lower().replace("?", "").split()
    stop_words = {"is", "the", "what", "who", "when", "where", "how", "and", "or", "of", "a", "an", "in", "to", "for"}
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    return keywords

def search_in_qa(keywords, qa_data):
    # بحث دقيق: المفاتيح التي تحتوي كل الكلمات المفتاحية
    for key, answer in qa_data.items():
        key_lower = key.lower()
        if all(kw in key_lower for kw in keywords):
            return answer

    # بحث أقل دقة: المفاتيح التي تحتوي أي كلمة مفتاحية، لكن تحقق أقصى تطابق
    best_match = None
    best_match_count = 0
    for key, answer in qa_data.items():
        key_lower = key.lower()
        count = sum(1 for kw in keywords if kw in key_lower)
        if count > best_match_count:
            best_match = answer
            best_match_count = count

    if best_match_count > 0:
        return best_match

    return None


def search_in_stats(keywords, stats_data):
    for key, val in stats_data.items():
        if isinstance(val, dict):
            for subkey, subval in val.items():
                if any(kw in subkey.lower() for kw in keywords):
                    return f"{subkey.title()}: {subval}"
        else:
            if any(kw in key.lower() for kw in keywords):
                return f"{key.replace('_', ' ').title()}: {val}"
    return None


def search_in_dataset(keywords, df):
    df_combined = df.astype(str).apply(lambda row: ' '.join(row.values).lower(), axis=1)
    for i, row in enumerate(df_combined):
        if all(kw in row for kw in keywords):
            return df.iloc[i].to_dict()
    return None

def is_english(text):
    try:
        text.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        words = re.findall(r'\b\w+\b', text.lower())
        english_words = {"the", "and", "is", "in", "you", "what", "who", "when", "where", "how"}
        count_english = sum(1 for w in words if w in english_words)
        return count_english > 0

def is_external_topic(keywords):
    external_keywords = {"basketball", "tennis", "politics", "music", "movie", "weather", "news", "technology", "stock", "economy"}
    return any(kw in external_keywords for kw in keywords)

def random_choice(choices):
    return random.choice(choices) if choices else None

def get_follow_up(keywords):
    for kw in keywords:
        if kw in FOLLOW_UP_QUESTIONS:
            return random_choice(FOLLOW_UP_QUESTIONS[kw])
    return random_choice(FOLLOW_UP_QUESTIONS.get('general', []))

def get_random_response(keywords):
    for kw in keywords:
        if kw in RESPONSES:
            return random_choice(RESPONSES[kw])
    return None

def eliza_reply(user_input):
    msg = user_input.lower()

    if "hello" in msg or "hi" in msg:
        return "Hi there! How are you feeling today?"

    elif "how are you" in msg:
        return "I'm fine, What was your favorite moment of the World Cup?"

    elif "sad" in msg:
        return "I'm sorry you're feeling sad. Want to talk about it?"

    elif "world cup" in msg:
        return "The World Cup is a thrilling tournament! Any favorite team?"

    elif "bye" in msg or "exit" in msg:
        return "Goodbye! 👋 Take care."

    elif "thank" in msg:
        return "You're welcome!"

    else:
        return "Tell me more about that..."

def answer_QA(user_input, qa_data, stats_data, df):
    GENERIC_FALLBACK = "Tell me more about that..."

    # 1) Try ELIZA first
    eliza_resp = eliza_reply(user_input)
    if eliza_resp and eliza_resp != GENERIC_FALLBACK:
        return eliza_resp, None

    # 2) Otherwise, proceed with your sources
    keywords = extract_keywords(user_input)
    if not keywords:
        return ("Please enter more specific keywords.", get_follow_up(['general']))

    if not is_english(user_input):
        return ("Sorry, I only understand English and can respond only in English.", None)

    if is_external_topic(keywords):
        return ("That's an interesting topic! But I'm really an expert on the FIFA World Cup 2022. "
                "What would you like to know about the tournament?", None)

    answer = search_in_qa(keywords, qa_data)
    if not answer:
        answer = search_in_stats(keywords, stats_data)
    if not answer:
        answer = get_random_response(keywords)
    if not answer:
        answer = search_in_dataset(keywords, df)
        if answer:
            answer = "\n".join(f"{key}: {val}" for key, val in answer.items())

    # 3) Final fallback: ELIZA generic (or whatever it returns)
    if not answer:
        answer = eliza_reply(user_input)
        follow_up = None
    else:
        follow_up = get_follow_up(keywords)

    return answer, follow_up



# -----------------------------------------
# واجهة Streamlit مع المحادثة (معادلة للكود الثاني لكن مع دعم QA)

st.set_page_config(page_title="World Cup Bot (حريف)", page_icon="⚽️", layout="wide")

st.sidebar.title("About")
st.sidebar.info(
    f"This humain-powered chatbot helps to know about all World Cup 2022. "
    f"Simply chat with it and provide details about the World Cup 2022 — teams, winners, players or history!. "
)

st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
    height: 100vh;
    width: 100vw;
}
header, footer { visibility: hidden; }

.chat-message.user {
    background-color: white !important;
    color: black !important;
    border-radius: 0.8rem;
    padding: 0.5rem;
}
.chat-message.assistant {
    background-color: white !important;
    color: black !important;
    border-radius: 0.8rem;
    padding: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
# Welcome to World Cup Bot (حريف) ⚽️  
Discover World Cup history in 2022!
""")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! ⚽️ Ask me anything about the World Cup — teams, winners, players or history!"}
    ]

# عرض المحادثة السابقة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# إدخال المستخدم وجلب الرد
if user_input := st.chat_input("Type your message..."):

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking... ⚽"):
        time.sleep(2)
        answer, follow_up = answer_QA(user_input, WC_2022_QA, WC_2022_STATS, df)

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)

    if follow_up:
        st.session_state.messages.append({"role": "assistant", "content": follow_up})
        with st.chat_message("assistant"):
            st.markdown(follow_up)
