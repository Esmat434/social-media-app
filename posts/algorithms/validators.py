def word_filtering(text):
    BANNED_WORDS = {
    'fuck', 'add', 'ads', 'shit',
    }
    for word in BANNED_WORDS:
        if word in text:
            return False
    
    return True