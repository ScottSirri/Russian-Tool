from googletrans import Translator

# Returns the translation of a Russian string or list of strings
def translate(query):
    translator = Translator()
    return translator.translate(query, src='ru')
