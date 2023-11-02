import sys
import PyPDF2
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QWidget

class PDFSummarizerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PDF Summarizer")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.text_edit = QTextEdit()
        self.layout.addWidget(self.text_edit)

        self.upload_button = QPushButton("Upload PDF")
        self.upload_button.clicked.connect(self.upload_pdf)
        self.layout.addWidget(self.upload_button)

        self.summarize_button = QPushButton("Summarize")
        self.summarize_button.clicked.connect(self.summarize)
        self.layout.addWidget(self.summarize_button)

        self.pdf_text = None

    def upload_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf);;All Files (*)", options=options)

        if file_name:
            with open(file_name, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                text = ''
                for page in pdf_reader.pages:
                    text += page.extract_text()
                from nlp_pipeline import clean_text
                self.pdf_text = """Large Language Models (LLMs) have achieved tremendous progress, yet they still
often struggle with challenging reasoning problems. Current approaches address
this challenge by sampling or searching detailed and low-level reasoning chains.
However, these methods are still limited in their exploration capabilities, making
it challenging for correct solutions to stand out in the huge solution space. In this
work, we unleash LLMs’ creative potential for exploring multiple diverse problem
solving strategies by framing an LLM as a hierarchical policy via in-context learn-
ing. This policy comprises of a visionary leader that proposes multiple diverse
high-level problem-solving tactics as hints, accompanied by a follower that exe-
cutes detailed problem-solving processes following each of the high-level instruc-
tion. The follower uses each of the leader’s directives as a guide and samples mul-
tiple reasoning chains to tackle the problem, generating a solution group for each
leader proposal. Additionally, we propose an effective and efficient tournament-
based approach to select among these explored solution groups to reach the fi-
nal answer. Our approach produces meaningful and inspiring hints, enhances
problem-solving strategy exploration, and improves the final answer accuracy on
challenging problems in the MATH dataset."""
                self.text_edit.setPlainText(self.pdf_text)

    def summarize(self):
        if self.pdf_text:
            # Add your summarization logic here
            # For this example, let's just show the first 500 characters as a summary
            from summarizer import Summarizer

            summarizer = Summarizer()

            # Выполнение суммаризации текста
            summary = summarizer.get_summary(self.pdf_text, "UNLEASHING THE CREATIVE MIND: LANGUAGE MODEL AS HIERARCHICAL POLICY FOR IMPROVED EXPLORATION ON CHALLENGING PROBLEM SOLVING")

            # Вывод суммаризированного текста

            from sentence_extractor import TextRank4Sentences

            mod = TextRank4Sentences()
            mod.analyze(self.pdf_text, stop_words=nltk.corpus.stopwords.words('english'))
            print(mod.get_top_sentences(5))

            summary = self.pdf_text[:500]
            self.text_edit.setPlainText(summary)

def main():
    app = QApplication(sys.argv)
    window = PDFSummarizerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    import en_core_web_sm
    nlp = en_core_web_sm.load()
    import nltk
    nltk.download('stopwords')
    nltk.download('wordnet')
    main()
