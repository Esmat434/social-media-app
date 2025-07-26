from langdetect import detect

def word_filtering(text):
    english_bad_words = {
        "fuck", "shit", "bitch", "asshole", "bastard",
        "dick", "crap", "piss", "slut", "whore",
        "spam", "ads", "scam", "suck", "jerk",
    }

    french_bad_words = {
        "merde", "putain", "salope", "connard", "enculé",
        "pute", "bordel", "chiant", "con", "pub",
        "arnaque", "spam",
    }

    spanish_bad_words = {
    "mierda", "puta", "gilipollas", "cabron", "coño",
    "hijo de puta", "joder", "estúpido", "imbécil",
    "anuncios", "spam", "fraude",
    }

    persian_bad_words = {
        "لعنتی", "حرامزاده", "کثافت", "خاک بر سرت", "مزخرف",
        "احمق", "نابغه", "گاو", "فاحشه", "جنده",
        "تبلیغات", "اسپم", "کلاه‌برداری", "کس‌شر", "عن",
    }

    arabic_bad_words = {
    "لعنة", "كلب", "حمار", "قذر", "زانية",
    "ابن الكلب", "تافه", "تباً", "تف", "محتال",
    "إعلانات", "احتيال", "بذاءة", "حقير", "زبالة",
    }

    BAD_WORDS = {
        "en": english_bad_words,
        "fr": french_bad_words,
        "es": spanish_bad_words,
        "fa": persian_bad_words,
        "ar": arabic_bad_words,
    }
    text = text.lower()
    lang = detect(text)
    if lang in BAD_WORDS:
        for word in BAD_WORDS[lang]:
            if word in text:
                return False
    
    return True