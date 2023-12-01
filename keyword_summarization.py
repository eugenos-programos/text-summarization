from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import WordNetLemmatizer
from langdetect import detect
from nltk.stem.snowball import SnowballStemmer 


def generate_keyword_summary(text):
    lang = detect(text)
    sentences = sent_tokenize(text)

    words = [word.lower() for sentence in sentences for word in word_tokenize(sentence)]
    if lang != 'ru':
        lemmatizer = WordNetLemmatizer()
        words = [lemmatizer.lemmatize(word) for word in words]
    else:
        stemmer = SnowballStemmer("russian") 
        words = [stemmer.stem(word) for word in words]


    stop_words_eng = set(stopwords.words('english'))
    stop_words_russian = set(stopwords.words('russian'))
    words = [word for word in words if word.isalnum() and word not in stop_words_eng and word not in stop_words_russian and len(word) > 1]
    word_freq = FreqDist(words)
    print("word freq\n", word_freq.items())
    top_words = word_freq.most_common(10) 
    process_top_words = top_words.copy()
    for pair_1 in top_words:
        for pair_2 in top_words:
            if pair_1[0] != pair_2[0] and pair_1[0] in pair_2[0]:
                process_top_words.remove(pair_1)
    return process_top_words

def get_summary(keyword_summary: list[tuple[str, int]], indent=0) -> str:
    summary = ''
    for key, value in keyword_summary:
        summary += f" {key} - {value}\n"
        if isinstance(value, dict):
            get_summary(value, indent + 1)
    return summary
