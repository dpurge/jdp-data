from io import StringIO

def get_word_forms(text, alphabet=""):

    start = 0
    for end in range(len(text)):
        if not text[start] in alphabet:
            start = end
        if text[end] in alphabet:
            continue
        if end > start:
            yield text[start:end]
            start = end
    if end > start:
        if text[end] in alphabet:
            yield text[start:]
        else:
            yield text[start:end]

def get_vocabulary(words):
    data = StringIO()
    for word in words:
        data.write(word)
        data.write("\n")
    return data.getvalue()