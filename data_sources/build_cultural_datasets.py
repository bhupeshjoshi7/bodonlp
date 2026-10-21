"""
Build authentic Bodo phrases, proverbs (फाथास), and riddles (खानथि).
"""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "bodonlp" / "lexicon" / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# 1. Phrases
PHRASES = [
    {
        "bodo": "खुलुमबाय",
        "roman": "Khulumbai",
        "english": "Hello / Greetings",
        "hindi": "नमस्ते",
        "category": "greetings"
    },
    {
        "bodo": "मा खबर?",
        "roman": "Ma khobor?",
        "english": "How are you? (What is the news?)",
        "hindi": "क्या हाल है?",
        "category": "greetings"
    },
    {
        "bodo": "मोजां, नोंहा मा खबर?",
        "roman": "Mwjang, nwngha ma khobor?",
        "english": "Fine, how are you?",
        "hindi": "अच्छा हूँ, आपका क्या हाल है?",
        "category": "greetings"
    },
    {
        "bodo": "आं मोजाङैनो दं",
        "roman": "Ang mwjangwinw dwng",
        "english": "I am fine",
        "hindi": "मैं ठीक हूँ",
        "category": "greetings"
    },
    {
        "bodo": "नोंनि मुंआ मा?",
        "roman": "Nwngni munga ma?",
        "english": "What is your name?",
        "hindi": "तुम्हारा नाम क्या है?",
        "category": "introduction"
    },
    {
        "bodo": "आंनि मुंआ...",
        "roman": "Angni munga...",
        "english": "My name is...",
        "hindi": "मेरा नाम... है",
        "category": "introduction"
    },
    {
        "bodo": "नों मा खालामदों?",
        "roman": "Nwng ma khalamdwng?",
        "english": "What are you doing?",
        "hindi": "तुम क्या कर रहे हो?",
        "category": "conversation"
    },
    {
        "bodo": "आं हाबा मावदों",
        "roman": "Ang haba maowdwng",
        "english": "I am working",
        "hindi": "मैं काम कर रहा हूँ",
        "category": "conversation"
    },
    {
        "bodo": "नों बबेयाव थांगोन?",
        "roman": "Nwng bwbeyao thang-gwn?",
        "english": "Where will you go?",
        "hindi": "तुम कहाँ जाओगे?",
        "category": "travel"
    },
    {
        "bodo": "आं न'आव थांगोन",
        "roman": "Ang noao thang-gwn",
        "english": "I will go home",
        "hindi": "मैं घर जाऊंगा",
        "category": "travel"
    },
    {
        "bodo": "गोजोन फुंबिलि!",
        "roman": "Gwjwn fungbili!",
        "english": "Good morning!",
        "hindi": "शुभ प्रभात!",
        "category": "wishes"
    },
    {
        "bodo": "गोजोन सान!",
        "roman": "Gwjwn saan!",
        "english": "Good day / afternoon!",
        "hindi": "शुभ दोपहर!",
        "category": "wishes"
    },
    {
        "bodo": "गोजोन बेलासै!",
        "roman": "Gwjwn belase!",
        "english": "Good evening!",
        "hindi": "शुभ संध्या!",
        "category": "wishes"
    },
    {
        "bodo": "गोजोन हर!",
        "roman": "Gwjwn hor!",
        "english": "Good night!",
        "hindi": "शुभ रात्रि!",
        "category": "wishes"
    },
    {
        "bodo": "गोजोन्थों / साबायखर",
        "roman": "Gwjwnthwng / Sabai-khor",
        "english": "Thank you",
        "hindi": "धन्यवाद",
        "category": "polite"
    },
    {
        "bodo": "थाबाय दे!",
        "roman": "Thabai de!",
        "english": "Goodbye! (See you!)",
        "hindi": "अलविदा!",
        "category": "farewell"
    },
    {
        "bodo": "निमाहा बिनो थाबाय",
        "roman": "Nimaha binw thabai",
        "english": "I am sorry / Excuse me",
        "hindi": "माफ़ कीजिये",
        "category": "polite"
    },
    {
        "bodo": "नोंनि न'आ बबेयाव?",
        "roman": "Nwngni noa bwbeyao?",
        "english": "Where is your house?",
        "hindi": "तुम्हारा घर कहाँ है?",
        "category": "conversation"
    },
    {
        "bodo": "आं बर' राव रोंङा",
        "roman": "Ang Boro rao rwnga",
        "english": "I do not know Bodo language",
        "hindi": "मुझे बोडो भाषा नहीं आती",
        "category": "language"
    },
    {
        "bodo": "आं बर' राव सोलोंदों",
        "roman": "Ang Boro rao swlwngdwng",
        "english": "I am learning Bodo language",
        "hindi": "मैं बोडो भाषा सीख रहा हूँ",
        "category": "language"
    },
    {
        "bodo": "नों इंराजी राव बुंनो हागौना?",
        "roman": "Nwng Ingazi rao bungnw hagwna?",
        "english": "Can you speak English?",
        "hindi": "क्या आप अंग्रेजी बोल सकते हैं?",
        "category": "language"
    },
    {
        "bodo": "जाख्रायनाय जाबायना?",
        "roman": "Jakhrainai jabaina?",
        "english": "Have you eaten?",
        "hindi": "खाना खा लिया?",
        "category": "food"
    },
    {
        "bodo": "ओंखाम जाबाय",
        "roman": "Wngkham jabai",
        "english": "I have eaten rice/food",
        "hindi": "खाना खा लिया",
        "category": "food"
    },
    {
        "bodo": "दै लुबैदों",
        "roman": "Dwi lwbwidwng",
        "english": "I am thirsty (need water)",
        "hindi": "प्यास लगी है",
        "category": "food"
    },
    {
        "bodo": "बैसागुनि गोजोननाय जासिबाय",
        "roman": "Bwisaguni gwjwnnai jasibai",
        "english": "Happy Bwisagu festival!",
        "hindi": "बैसागु की शुभकामनाएँ!",
        "category": "festivals"
    }
]

# 2. Proverbs (फाथास / Bathra Sao)
PROVERBS = [
    {
        "bodo": "गावनि आफाखौ मान हो, गुबुननि आफाखौबो मान हो।",
        "roman": "Gaoni afakhou man ho, gubunni afakhoubo man ho.",
        "english": "Respect your own father, and respect others' father as well.",
        "meaning": "Treat all elders and people with equal reverence and honor.",
        "theme": "morality"
    },
    {
        "bodo": "हाथिखौ गोलोमफ्लांब्ला मानसिहा दावगानाय थाया।",
        "roman": "Hathikhou golomflangbla mansiha daoganai thaya.",
        "english": "If the elephant slips, a person stands no chance.",
        "meaning": "Even the mightiest can make mistakes; humility is necessary for all.",
        "theme": "wisdom"
    },
    {
        "bodo": "आफा गैयाब्ला न' गैया, आइ गैयाब्ला संनाय गैया।",
        "roman": "Afa gwyabla no gwaya, aai gwyabla swngnai gwaya.",
        "english": "Without father there is no household, without mother there is no hearth.",
        "meaning": "Both parents are essential pillars of a happy and prosperous home.",
        "theme": "family"
    },
    {
        "bodo": "सोरबा लोंनायनि दै, सोरबा बोहैनायनि दै।",
        "roman": "Swrba lwngnaini dwi, swrba bwhwinaini dwi.",
        "english": "For some it is drinking water, for others it is flood water.",
        "meaning": "One person's boon may be another person's tragedy; life is unequal.",
        "theme": "life"
    },
    {
        "bodo": "मोजां हाबाया मोजां फिथाइ लायो।",
        "roman": "Mwjang habaya mwjang fithai layo.",
        "english": "Good deeds bear good fruits.",
        "meaning": "As you sow, so shall you reap.",
        "theme": "karma"
    },
    {
        "bodo": "दैया दाउबाबो गोजों थायो, मानसिहा दुखु सह'बाबो गोजोन थायो।",
        "roman": "Dwiya daubabo gwjwng thayo, mansiha dukhu sohobabo gwjwn thayo.",
        "english": "Water remains clear even after stirring; a virtuous soul stays calm despite tribulations.",
        "meaning": "True inner peace is not disturbed by temporary adversity.",
        "theme": "resilience"
    },
    {
        "bodo": "सानसेनि सायाव गुबुन सानबो फैयो।",
        "roman": "Sanseni sayao gubun saanbo fwiyo.",
        "english": "After one day another day always arrives.",
        "meaning": "Hope never dies; dark times are followed by bright days.",
        "theme": "optimism"
    },
    {
        "bodo": "सिफुंनि सुरा गोरबोआव हाबथारो।",
        "roman": "Sifungni sura gwrboao habtharo.",
        "english": "The melody of the Sifung flute pierces right into the heart.",
        "meaning": "Pure art and music have the power to touch the deepest soul.",
        "theme": "culture"
    }
]

# 3. Riddles (खानथि / सोल')
RIDDLES = [
    {
        "question": "आं जाखाङोब्ला बारायलांगो, आं लोंखाङोब्ला थैयो। आं सोर?",
        "roman": "Ang jakhangobla barailango, ang lwngkhangobla thwiyo. Ang swr?",
        "english": "If I eat I grow, if I drink I die. Who am I?",
        "answer": "अर (Or / Fire)",
        "hint": "Element of nature"
    },
    {
        "question": "आं गाबनो हायो आथिं गैयाबालानो, आं बिरनो हायो गां गैयाबालानो। आं सोर?",
        "roman": "Ang gabnw hayo athing gwyabalano, ang birnw hayo gang gwyabalano. Ang swr?",
        "english": "I can weep without eyes, and I can fly without wings. Who am I?",
        "answer": "जोमैल' (Jwmoilw / Cloud)",
        "hint": "In the sky"
    },
    {
        "question": "खुलिब्ला न' गासै सिङाव, बन्द खालामब्ला लाथायाव। आं सोर?",
        "roman": "Khulibla no gaswi singao, bondo khalambla lathayao. Ang swr?",
        "english": "When opened it shelters the whole body, when closed it fits in the hand. Who am I?",
        "answer": "साथा (Satha / Umbrella)",
        "hint": "Everyday object"
    },
    {
        "question": "सानदुंआव दाउबायो, ओखायाव गोमोयो। आं सोर?",
        "roman": "Sandungao daubayo, okha-yao gwmwyo. Ang swr?",
        "english": "Accompanies you in the sunlight, disappears in the rain. Who am I?",
        "answer": "साया (Saya / Shadow)",
        "hint": "Always follows you"
    },
    {
        "question": "गावहा आथिं गंनै, जाबग्रा खुगा गंनै, बियो मानसिबो नङा जुनारबो नङा। बियो मा?",
        "roman": "Gaoha athing gwngnwi, jabgra khuga gwngnwi, biyw mansibo nonga junarbo nonga. Biyw ma?",
        "english": "It has two legs and two biting mouths, but it is neither human nor animal. What is it?",
        "answer": "खासि / खास्रि (Khasi / Scissors)",
        "hint": "Household cutting tool"
    }
]

def main():
    with open(DATA_DIR / "phrases.json", "w", encoding="utf-8") as f:
        json.dump(PHRASES, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(PHRASES)} phrases.")

    with open(DATA_DIR / "proverbs.json", "w", encoding="utf-8") as f:
        json.dump(PROVERBS, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(PROVERBS)} proverbs.")

    with open(DATA_DIR / "riddles.json", "w", encoding="utf-8") as f:
        json.dump(RIDDLES, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(RIDDLES)} riddles.")

if __name__ == "__main__":
    main()
