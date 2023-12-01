from langdetect import detect
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog, QMessageBox, QHBoxLayout
import os
from keyword_summarization import get_summary, generate_keyword_summary


class SummarizerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Text summarizer')

        self.text_edit = QTextEdit(self)
        self.result_label_se = QLabel(self)
        self.result_label_se.setWordWrap(True)

        self.result_label_ml = QLabel(self)
        self.result_label_ml.setWordWrap(True)

        self.result_label_keyword = QLabel(self)
        self.result_label_keyword.setWordWrap(True)

        load_button = QPushButton('Upload text', self)
        summarize_button = QPushButton('Summarize', self)
        help_button = QPushButton('Help', self)
        save_button_ml = QPushButton('Save NN result', self)
        save_button_se = QPushButton('Save SE result', self)
        save_button_keyword = QPushButton('Save keyword result', self)

        self.file_label = QLabel(f'<a href="None">Upload file for clickability</a>', self)
        self.file_label.setOpenExternalLinks(True)

        load_button.clicked.connect(self.load_text)
        summarize_button.clicked.connect(self.summarize_text)
        save_button_ml.clicked.connect(self.save_result_ml)
        save_button_se.clicked.connect(self.save_result_se)
        save_button_keyword.clicked.connect(self.save_result_keyword)
        help_button.clicked.connect(self.help)

        vbox = QVBoxLayout()
        vbox.addWidget(load_button)
        vbox.addWidget(self.file_label)
        vbox.addWidget(self.text_edit)
        vbox.addWidget(summarize_button)
        vbox.addWidget(self.result_label_se)
        vbox.addWidget(self.result_label_ml)
        vbox.addWidget(self.result_label_keyword)
        vbox.addWidget(save_button_se)
        vbox.addWidget(save_button_ml)
        vbox.addWidget(save_button_keyword)
        vbox.addWidget(help_button)

        self.setLayout(vbox)

    @staticmethod
    def create_file_link(file_path):
        absolute_path = os.path.abspath(file_path)
        file_link = f'file:///{absolute_path.replace(" ", "%20")}'
        return file_link

    @staticmethod
    def ml_summary_en(payload):
        import requests
        API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {"Authorization": "Bearer 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"}
        response_code = 404
        while response_code != 200:
            response = requests.post(API_URL, headers=headers, json=payload)
            response_code = response.status_code
        return response.json()
    
    @staticmethod
    def ml_summary_ru(payload):
        import requests
        API_URL = "https://api-inference.huggingface.co/models/csebuetnlp/mT5_multilingual_XLSum"
        headers = {"Authorization": "Bearer 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"}
        response_code = 404
        while response_code != 200:
            response = requests.post(API_URL, headers=headers, json=payload)
            response_code = response.status_code
        return response.json()

    def load_text(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open text document', filter='Text files (*.txt);;All Files (*)')

        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                self.file_label.setText(f'<a href="{self.create_file_link(file_path)}">{file_path}</a>')
                self.text_edit.setPlainText(text)

    def summarize_text(self):
        input_text = self.text_edit.toPlainText()

        if input_text:
            from sentence_extractor import TextRank4Sentences
            import nltk
            mod = TextRank4Sentences()
            mod.analyze(input_text, stop_words=nltk.corpus.stopwords.words('english'))

            result_text_se = mod.get_top_sentences(5)
            if detect(input_text) == 'en':
                result_text_ml = self.ml_summary_en({"inputs": input_text})[0]['summary_text']
            else:
                result_text_ml = self.ml_summary_ru({"inputs": input_text})[0]['summary_text']


            self.result_label_se.setText('.'.join(result_text_se))
            self.result_label_ml.setText(f"___________\n{result_text_ml}")
            self.result_label_keyword.setText(f"_________\n{get_summary(generate_keyword_summary(input_text))}")

    def save_result_se(self):
        result_text = self.result_label_se.text()

        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, 'Save result', filter='Text files (*.txt);;All Files (*)')

        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(result_text)

    def save_result_ml(self):
        result_text = self.result_label_ml.text()

        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, 'Save result', filter='Text files (*.txt);;All Files (*)')

        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(result_text)

    def save_result_keyword(self):
        result_text = self.result_label_keyword.text()

        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, 'Save result', filter='Text files (*.txt);;All Files (*)')

        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(result_text)

    def help(self):
        help_text = "This app is used for automatic text documents summarization. " \
                    "Steps:\n1. Upload text file.\n2. Click on 'summarize' for summarization.\n" \
                    "3. The result will be displayed in window where you can save it."

        QMessageBox.information(self, 'Help', help_text)
