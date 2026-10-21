"""
Linguistic, grammatical, and cultural constants for the Bodo language library.
"""

from enum import Enum


class Script(str, Enum):
    """Scripts officially and colloquially used for Bodo."""
    DEVANAGARI = "devanagari"  # Official script adopted in 1974
    LATIN = "latin"            # Romanized / phonetic script widely used online and historically
    ASSAMESE = "assamese"      # Historically used in 19th/20th century literature


class Dialect(str, Enum):
    """Regional varieties and dialects of the Bodo language."""
    WESTERN = "western"        # Western dialect (Kokrajhar, Chirang, Bongaigaon, Dhubri) - Standard Literary
    EASTERN = "eastern"        # Eastern dialect (Darrang, Udalguri, Sonitpur, Lakhimpur)
    SOUTHERN = "southern"      # Southern dialect (Kamrup, Goalpara, Meghalaya border)


class PartOfSpeech(str, Enum):
    """Grammatical parts of speech."""
    NOUN = "noun"
    PRONOUN = "pronoun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    POSTPOSITION = "postposition"
    CONJUNCTION = "conjunction"
    INTERJECTION = "interjection"
    PARTICLE = "particle"
    CLASSIFIER = "classifier"
    NUMBER = "number"


class Tense(str, Enum):
    """Grammatical tenses and aspects in Bodo."""
    PRESENT = "present"                    # Indefinite / Habitual (-o / -yo)
    PRESENT_CONTINUOUS = "present_continuous" # (-dwng / -दों)
    PAST = "past"                          # Perfective (-bai / -बाय) or Past Indefinite (-mwn / -मोन)
    PAST_CONTINUOUS = "past_continuous"    # (-dwngmwn / -दोंमोन)
    FUTURE = "future"                      # (-gwn / -गोन)
    FUTURE_CONTINUOUS = "future_continuous"# (-बाय थागोन)
    IMPERATIVE = "imperative"              # (-दो / -do)
    PROHIBITIVE = "prohibitive"            # (दा- / da-)


class Case(str, Enum):
    """Agglutinative case system markers in Bodo."""
    NOMINATIVE = "nominative"              # unmarked or -आ (-a)
    ACCUSATIVE = "accusative"              # -खौ (-khwo)
    INSTRUMENTAL = "instrumental"          # -जों (-jwng)
    DATIVE = "dative"                      # -नो (-nw)
    ABLATIVE = "ablative"                  # -निफ्राय (-nifrai)
    GENITIVE = "genitive"                  # -नि (-ni)
    LOCATIVE = "locative"                  # -आव (-ao)


# ISO Language Codes
ISO_639_3 = "brx"
ISO_639_NAME = "Bodo"
ISO_639_1 = "brx"
NLLB_CODE = "brx_Deva"
FLORES_CODE = "brx_Deva"
NATIVE_NAME = "बड़ो"
NATIVE_NAME_ALT = "बर'"

# Postposition / Case Markers Table
CASE_MARKERS = {
    Case.NOMINATIVE: {"marker": "", "alt": "आ", "roman": "a", "function": "Subject"},
    Case.ACCUSATIVE: {"marker": "खौ", "alt": "खौ", "roman": "khwo", "function": "Direct Object"},
    Case.INSTRUMENTAL: {"marker": "जों", "alt": "जों", "roman": "jwng", "function": "Instrument / With"},
    Case.DATIVE: {"marker": "नो", "alt": "नो", "roman": "nw", "function": "To / For (Recipient)"},
    Case.ABLATIVE: {"marker": "निफ्राय", "alt": "निफ्राय", "roman": "nifrai", "function": "From / Origin"},
    Case.GENITIVE: {"marker": "नि", "alt": "नि", "roman": "ni", "function": "Possessive / Of"},
    Case.LOCATIVE: {"marker": "आव", "alt": "याव", "roman": "ao", "function": "In / At / On"},
}

# Numeral Classifiers in Bodo (Distinctive feature of Sino-Tibetan / Bodo-Garo)
NUMERAL_CLASSIFIERS = {
    "sa": {"marker": "सा", "roman": "sa", "meaning": "For human beings", "examples": ["सासे मानसि (one person)", "सानै फिसा (two children)"]},
    "ma": {"marker": "मा", "roman": "ma", "meaning": "For animals, birds, insects", "examples": ["मासे सैमा (one dog)", "माब्रै दाव (four birds)"]},
    "gwng": {"marker": "गं", "roman": "gwng", "meaning": "For flat, curved, rigid objects, houses, utensils, instruments", "examples": ["गंसे न' (one house)", "गंनै थाला (two plates)"]},
    "dwng": {"marker": "दं", "roman": "dwng", "meaning": "For long, cylindrical, tall objects (trees, ropes, rivers)", "examples": ["दंसे बिफां (one tree)", "दंसे दुलि (one rope)"]},
    "thai": {"marker": "थाइ", "roman": "thai", "meaning": "For fruits, round objects, coins, spherical items", "examples": ["थाइसे थाइजौ (one mango)", "थाइथाम फिथाइ (three fruits)"]},
    "bisi": {"marker": "बिसि", "roman": "bisi", "meaning": "For thin, flat sheet-like objects (leaves, paper)", "examples": ["बिसिसे बिलाइ (one leaf)"]},
    "kholob": {"marker": "खोलोब", "roman": "kholob", "meaning": "For layers, volumes, books, pairs", "examples": ["खोलोबसे बिजाब (one book)"]},
    "gor": {"marker": "गर", "roman": "gor", "meaning": "For grains, beads, small spherical seeds", "examples": ["गरसे मैखुन (one bead)"]},
}

# Kinship Relationships in Bodo
KINSHIP = {
    "father": {"bodo": "आफा / बिफा", "roman": "Afa / Bifa", "hindi": "पिता"},
    "mother": {"bodo": "आइ / बिमा", "roman": "Aai / Bima", "hindi": "माता"},
    "elder_brother": {"bodo": "आदा", "roman": "Ada", "hindi": "बड़ा भाई"},
    "younger_brother": {"bodo": "फंबाय", "roman": "Fwngbai", "hindi": "छोटा भाई"},
    "elder_sister": {"bodo": "आब'", "roman": "Abo", "hindi": "बड़ी बहन"},
    "younger_sister": {"bodo": "बिननाव", "roman": "Binnao", "hindi": "छोटी बहन"},
    "grandfather_paternal": {"bodo": "आबौ", "roman": "Abou", "hindi": "दादा"},
    "grandmother_paternal": {"bodo": "आबै", "roman": "Abwi", "hindi": "दादी"},
    "grandfather_maternal": {"bodo": "आबौ", "roman": "Abou", "hindi": "नाना"},
    "grandmother_maternal": {"bodo": "आबै", "roman": "Abwi", "hindi": "नानी"},
    "son": {"bodo": "फिसाला", "roman": "Fisala", "hindi": "बेटा"},
    "daughter": {"bodo": "फिसाजो", "roman": "Fisajw", "hindi": "बेटी"},
    "husband": {"bodo": "हौवा / फिसाय", "roman": "Howa / Fisai", "hindi": "पति"},
    "wife": {"bodo": "हिनजाव / बिसि", "roman": "Hinjao / Bisi", "hindi": "पत्नी"},
    "uncle_elder": {"bodo": "आदै", "roman": "Adwi", "hindi": "ताऊ"},
    "uncle_younger": {"bodo": "आदै / खुरा", "roman": "Adwi / Khura", "hindi": "चाचा"},
    "aunt_elder": {"bodo": "आनै", "roman": "Anwi", "hindi": "ताई"},
    "aunt_younger": {"bodo": "आनै / मुरुमै", "roman": "Anwi / Murumwi", "hindi": "चाची"},
}

# Traditional Bodo Seasons (बोरो बोथोर / Boro Bothor)
SEASONS = {
    "spring": {"name_brx": "बैसाग बोथोर", "roman": "Bwisag Bothor", "english": "Spring", "description": "Season of blossoms, New Year, and Bwisagu festival"},
    "summer": {"name_brx": "दुंब्रु बोथोर", "roman": "Dumbru Bothor", "english": "Summer", "description": "Warm farming season"},
    "monsoon": {"name_brx": "ओखा बोथोर", "roman": "Okha Bothor", "english": "Monsoon / Rainy", "description": "Paddy transplantation season with monsoon showers"},
    "autumn": {"name_brx": "शिरि बोथोर", "roman": "Shiri Bothor", "english": "Autumn", "description": "Clear skies, blooming Kash reeds, Katrigasa festival"},
    "early_winter": {"name_brx": "गोजां बोथोर", "roman": "Gojang Bothor", "english": "Early Winter", "description": "Harvest season and harvest preparation"},
    "late_winter": {"name_brx": "साहा बोथोर", "roman": "Saha Bothor", "english": "Late Winter", "description": "Cool winter breeze and Domashi celebration"},
}

# Bodo Calendar Months (दान / Daan)
BODO_MONTHS = [
    {"index": 1, "bodo": "बैसाख", "roman": "Bwisakh", "gregorian": "April-May", "significance": "Start of New Year and Bwisagu"},
    {"index": 2, "bodo": "जेठ", "roman": "Jeth", "gregorian": "May-June", "significance": "Early summer agriculture"},
    {"index": 3, "bodo": "आहार", "roman": "Ahar", "gregorian": "June-July", "significance": "Beginning of monsoon cultivation"},
    {"index": 4, "bodo": "शाउन", "roman": "Shaon", "gregorian": "July-August", "significance": "Peak paddy sowing season"},
    {"index": 5, "bodo": "भाद्र", "roman": "Bhadro", "gregorian": "August-September", "significance": "Lush green valley season"},
    {"index": 6, "bodo": "आहिन", "roman": "Ahin", "gregorian": "September-October", "significance": "Autumn tranquility"},
    {"index": 7, "bodo": "खाथि", "roman": "Khati", "gregorian": "October-November", "significance": "Katrigasa earthen lamp celebration"},
    {"index": 8, "bodo": "आघोन", "roman": "Aghon", "gregorian": "November-December", "significance": "Golden paddy harvesting season"},
    {"index": 9, "bodo": "फुस", "roman": "Fus", "gregorian": "December-January", "significance": "Winter threshold and threshing fields"},
    {"index": 10, "bodo": "माघ", "roman": "Magh", "gregorian": "January-February", "significance": "Domashi (Magh harvest bonfires)"},
    {"index": 11, "bodo": "फागुन", "roman": "Fagun", "gregorian": "February-March", "significance": "Red silk-cotton blooms"},
    {"index": 12, "bodo": "सैथ", "roman": "Swith", "gregorian": "March-April", "significance": "Preparations for spring renewal"},
]

# Days of the Week in Bodo (सान / Saan)
DAYS_OF_WEEK = [
    {"day": 0, "bodo": "रबिबार", "roman": "Robibar", "english": "Sunday"},
    {"day": 1, "bodo": "समबार", "roman": "Sombar", "english": "Monday"},
    {"day": 2, "bodo": "मंगलबार", "roman": "Mongolbar", "english": "Tuesday"},
    {"day": 3, "bodo": "बुदबार", "roman": "Budbar", "english": "Wednesday"},
    {"day": 4, "bodo": "बिसथिबार", "roman": "Bisthibar", "english": "Thursday"},
    {"day": 5, "bodo": "सुखुरबार", "roman": "Sukhurbar", "english": "Friday"},
    {"day": 6, "bodo": "सुनिबार", "roman": "Sunibar", "english": "Saturday"},
]

# Prominent Bodo Clans / Ari / Surnames
BODO_CLANS = [
    {"surname": "Basumatary", "devanagari": "बसुमतारि", "clan": "Basumata-ari", "meaning": "Earth / Soil clan (descendants of Mother Earth)"},
    {"surname": "Brahma", "devanagari": "ब्रह्म", "clan": "Brahma-ari", "meaning": "Followers of Brahma Dharma founded by Gurudev Kalicharan Brahma"},
    {"surname": "Boro", "devanagari": "बर'", "clan": "Boro-ari", "meaning": "Core lineage bearing the indigenous ethnic denomination"},
    {"surname": "Narzary", "devanagari": "नारजारि", "clan": "Narzari", "meaning": "Jute cultivating lineage (from 'Narji' - dry jute leaves)"},
    {"surname": "Daimary", "devanagari": "दाइमरि", "clan": "Daimari", "meaning": "Riverine dwellers clan (from 'Dwi-ma' - big river)"},
    {"surname": "Swargiary", "devanagari": "स्वर्गियारि", "clan": "Swargiari", "meaning": "Priestly / celestial lineage associated with Bathou rituals"},
    {"surname": "Wary", "devanagari": "वारि", "clan": "Wari", "meaning": "Cotton / weaving heritage clan (from 'Wa' - bamboo or weaving thread)"},
    {"surname": "Goyary", "devanagari": "गयारि", "clan": "Goyari", "meaning": "Betel-nut planters lineage (from 'Goi' - areca nut)"},
    {"surname": "Ishwary", "devanagari": "ईश्वारि", "clan": "Iswari", "meaning": "Spiritual lineage dedicated to Ishwar / Bathoubwrai"},
    {"surname": "Mushahary", "devanagari": "मुसाहारि", "clan": "Mosahari", "meaning": "Tiger lineage (from 'Mosa' - tiger), legendary warriors"},
    {"surname": "Khaklary", "devanagari": "खाक्लारि", "clan": "Khakhlari", "meaning": "Traditional healers and herbal medicine custodians"},
    {"surname": "Hazowary", "devanagari": "हाजोवारि", "clan": "Hajowari", "meaning": "Highland / mountain dwellers clan (from 'Hajo' - hill/mountain)"},
]
