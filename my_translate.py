from deep_translator import GoogleTranslator

# You've never seen a wrapper this thin.
# Returns the translation of a Russian string or list of strings
def translate(query):
    translation = GoogleTranslator(source='ru', target='en').translate(query)
    return translation
