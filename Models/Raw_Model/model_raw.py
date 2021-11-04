from Settings.setings import *


def sentence_tokenize(text):
    """
    take string input and return a list of sentences.
    use nltk.sentence_tokenize() to split the sentences.
    """
    return nltk.sentence_tokenize(text)


def word_tokenize(text):
    """
    return list of words
    """
    return nltk.word_tokenize(text)


def to_lower(text):
    """
    converted text to lower case as in, converting "Hello" to "hello" or "HELLO" to "hello".

    """
    return text.lower()


def auto_spell(text):
    """
    correct the spelling of the word.

    """
    spells = [spell(word) for word in (nltk.word_tokenize(text))]
    return " ".join(spells)


def remove_numbers(text):
    """
    take strings input and return a clean text without numbers.
    use regex to discard the numbers.
    """
    output = " ".join(c for c in text if not c.isdigit())
    return output


def remove_punctuation(text):
    return " ".join(c for c in text if c not in punctuation)


def remove_stop_words(text):
    """
    removes all the stop words like "is, the,a, etc"
    """
    stop_words = stopwords.words('swedish')
    return "".join([word for word in nltk.word_tokenize(text) if not word in stop_words])


def lemmatize(text):
    word_lemma = WordNetLemmatizer()
    lemmatized_word = [word_lemma.lemmatize(word) for word in nltk.word_tokenize(text)]
    return " ".join(lemmatized_word)


def pre_process(text):
    lower_text = to_lower(text)
    sentence_tokens = sentence_tokenize(lower_text)
    word_list = []
    for each_sent in sentence_tokens:
        lemmatized_sent = lemmatize(each_sent)
        clean_text_num = remove_numbers(lemmatized_sent)
        clean_text_punct = remove_punctuation(clean_text_num)
        clean_text_stop_w = remove_stop_words(clean_text_punct)
        word_tokens = word_tokenize(clean_text_stop_w)
        for i in word_tokens:
            word_list.append(i)
    return word_tokens
