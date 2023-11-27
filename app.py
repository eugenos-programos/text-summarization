import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog, QMessageBox, QHBoxLayout
import os
from transformers import pipeline


class SummarizerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Текстовый Рефератор')

        self.text_edit = QTextEdit(self)
        self.result_label_se = QLabel(self)
        self.result_label_se.setWordWrap(True)

        self.result_label_ml = QLabel(self)
        self.result_label_ml.setWordWrap(True)

        load_button = QPushButton('Загрузить текст', self)
        summarize_button = QPushButton('Реферировать', self)
        help_button = QPushButton('Помощь', self)
        save_button_ml = QPushButton('Сохранить результат МО', self)
        save_button_se = QPushButton('Сохранить результат SE', self)

        self.label = QLabel(f'<a href="None">Загрузите файл для кликабельности</a>', self)
        self.label.setOpenExternalLinks(True)

        load_button.clicked.connect(self.load_text)
        summarize_button.clicked.connect(self.summarize_text)
        save_button_ml.clicked.connect(self.save_result_ml)
        save_button_se.clicked.connect(self.save_result_se)
        help_button.clicked.connect(self.help)

        vbox = QVBoxLayout()
        vbox.addWidget(load_button)
        vbox.addWidget(self.label)
        vbox.addWidget(self.text_edit)
        vbox.addWidget(summarize_button)
        vbox.addWidget(self.result_label_se)
        vbox.addWidget(self.result_label_ml)
        vbox.addWidget(save_button_se)
        vbox.addWidget(save_button_ml)
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
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    
    @staticmethod
    def ml_summary_ru(payload):
        import requests
        API_URL = "https://api-inference.huggingface.co/models/csebuetnlp/mT5_multilingual_XLSum"
        headers = {"Authorization": "Bearer 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"}
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    def load_text(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Открыть текстовый документ', filter='Text files (*.txt);;All Files (*)')

        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                self.label.setText(f'<a href="{self.create_file_link(file_path)}">{file_path}</a>')
                self.text_edit.setPlainText(text)

    def summarize_text(self):
        input_text = self.text_edit.toPlainText()

        if input_text:
            from sentence_extractor import TextRank4Sentences
            import nltk
            mod = TextRank4Sentences()
            mod.analyze(input_text, stop_words=nltk.corpus.stopwords.words('english'))

            # Форматирование результатов
            result_text_se = mod.get_top_sentences(5)
            if 'a' in input_text or 'b' in input_text or 'c' in input_text:
                result_text_ml = self.ml_summary_en({"inputs": input_text})[0]['summary_text']
            else:
                result_text_ml = self.ml_summary_ru({"inputs": input_text})[0]['summary_text']

            self.result_label_se.setText('.'.join(result_text_se))
            self.result_label_ml.setText(f"___________\n{result_text_ml}")

    def save_result_se(self):
        result_text = self.result_label_se.text()

        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, 'Сохранить результат', filter='Text files (*.txt);;All Files (*)')

        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(result_text)

    def save_result_ml(self):
        result_text = self.result_label_ml.text()

        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, 'Сохранить результат', filter='Text files (*.txt);;All Files (*)')

        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(result_text)

    def help(self):
        help_text = "Данное приложение предназначено для автоматического реферирования текстовых документов. " \
                    "Шаги:\n1. Загрузите текстовый документ.\n2. Нажмите 'Реферировать' для получения реферата.\n" \
                    "3. Результат отобразится в окне, где вы можете сохранить его."

        QMessageBox.information(self, 'Help', help_text)

if __name__ == '__main__':
    import en_core_web_sm
    nlp = en_core_web_sm.load()
    import nltk
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt')
    app = QApplication(sys.argv)
    summarizer_app = SummarizerApp()
    summarizer_app.show()
    sys.exit(app.exec_())
