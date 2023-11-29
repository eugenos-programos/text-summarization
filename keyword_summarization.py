from nltk import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist


def generate_keyword_summary(text):
    sentences = sent_tokenize(text)

    words = [word.lower() for sentence in sentences for word in word_tokenize(sentence)]

    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word.isalnum() and word not in stop_words]
    word_freq = FreqDist(words)

    top_words = word_freq.most_common(10) 
    keyword_summary = {}
    for word, freq in top_words:
        current_dict = keyword_summary
        for part in word.split():
            current_dict = current_dict.setdefault(part, {})

    return keyword_summary

def get_summary(keyword_summary, indent=0) -> str:
    summary = ''
    for key, value in keyword_summary.items():
        summary += '  ' * indent + key + '\n'
        if isinstance(value, dict):
            get_summary(value, indent + 1)
    return summary
