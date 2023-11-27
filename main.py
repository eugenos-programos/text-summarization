import nltk
import en_core_web_sm
from app import QApplication, SummarizerApp
import sys


if __name__ == '__main__':
    nlp = en_core_web_sm.load()
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt')
    app = QApplication(sys.argv)
    summarizer_app = SummarizerApp()
    summarizer_app.show()
    sys.exit(app.exec_())
