import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from transformers import MarianTokenizer, MarianMTModel
from sacremoses import MosesTokenizer, MosesDetokenizer

class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set window title and icon
        self.setWindowTitle("English to French Translator")
        self.setWindowIcon(QIcon('icon.ico'))
        self.setGeometry(300, 300, 800, 600)  # Set window geometry

        # Create central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)

        # Initialize UI components
        self.init_ui()
        self.show()  # Display the window

    def init_ui(self):
        # Input text area for English text
        self.input_text = QTextEdit(self)
        self.input_text.setPlaceholderText("Enter English text here")
        self.input_text.setStyleSheet("font-size: 16px; border: 2px solid #ccc; border-radius: 5px; padding: 10px;")
        self.input_text.setMinimumHeight(200)
        self.input_text.setAcceptRichText(False)
        self.central_layout.addWidget(self.input_text)

        # Translate button
        self.translate_button = QPushButton("Translate", self)
        self.translate_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-size: 18px; font-weight: bold; border-radius: 5px; padding: 10px 20px; } QPushButton:hover { background-color: #3e8e41; }")
        self.translate_button.clicked.connect(self.translate)
        self.central_layout.addWidget(self.translate_button, alignment=Qt.AlignCenter)

        # Output text area for translated French text
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("font-size: 16px; border: 2px solid #ccc; border-radius: 5px; padding: 10px;")
        self.output_text.setMinimumHeight(200)
        self.central_layout.addWidget(self.output_text)

        # Guidance label
        guidance_label = QLabel("Enter the English text above and view the French translation below.")
        guidance_label.setAlignment(Qt.AlignCenter)
        guidance_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")  # Updated styling
        self.central_layout.addWidget(guidance_label)

    def translate(self):
        # Translate function to handle translation process
        input_text = self.input_text.toPlainText()
        if input_text:
            try:
                # Tokenize input English text
                tokenizer = MosesTokenizer(lang='en')
                tokens = tokenizer.tokenize(input_text)
                detokenizer = MosesDetokenizer(lang='en')
                detokenized_text = detokenizer.detokenize(tokens)

                # Load pre-trained translation model
                model_name = "Helsinki-NLP/opus-mt-en-fr"
                model = MarianMTModel.from_pretrained(model_name)
                tokenizer = MarianTokenizer.from_pretrained(model_name)

                # Tokenize and encode detokenized text
                encoded_text = tokenizer(detokenized_text, return_tensors="pt")
                # Generate translation
                output = model.generate(**encoded_text)
                # Decode translated output
                translation = tokenizer.decode(output[0], skip_special_tokens=True)
                # Set translated text in output text area
                self.output_text.setPlainText(translation)
            except Exception as e:
                # If translation fails, display error message
                self.output_text.setPlainText("Translation failed. Please try again.")
                print(f"Translation error: {e}")

if __name__ == "__main__":
    # Create and run the application
    app = QApplication(sys.argv)
    window = TranslatorApp()
    sys.exit(app.exec_())
