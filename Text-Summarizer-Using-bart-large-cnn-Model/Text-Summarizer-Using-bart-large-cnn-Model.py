import sys
from transformers import pipeline, set_seed
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel, QSizePolicy
from PyQt5.QtGui import QIcon, QPalette, QColor, QFont
from PyQt5.QtCore import Qt


class SummarizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set window title
        self.setWindowTitle("Text Summarizer")
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
        # Input text area for the text to summarize
        self.input_text = QTextEdit(self)
        self.input_text.setPlaceholderText("Enter text to summarize here")
        self.input_text.setStyleSheet("font-size: 16px; border: 2px solid #ccc; border-radius: 5px; padding: 10px;")
        self.input_text.setMinimumHeight(200)
        self.input_text.setAcceptRichText(False)
        self.central_layout.addWidget(self.input_text)

        # Max words input
        self.max_words_label = QLabel("Maximum Words for Summary:", self)
        self.central_layout.addWidget(self.max_words_label)
        self.max_words_input = QTextEdit(self)
        self.max_words_input.setPlaceholderText("Enter max words")
        self.max_words_input.setStyleSheet("font-size: 16px; border: 2px solid #ccc; border-radius: 5px; padding: 10px;")
        self.central_layout.addWidget(self.max_words_input)

        # Summarize button
        self.summarize_button = QPushButton("Summarize", self)
        self.summarize_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-size: 18px; font-weight: bold; border-radius: 5px; padding: 10px 20px; } QPushButton:hover { background-color: #3e8e41; }")
        self.summarize_button.clicked.connect(self.summarize)
        self.central_layout.addWidget(self.summarize_button, alignment=Qt.AlignCenter)

        # Output text area for the summary
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("font-size: 16px; border: 2px solid #ccc; border-radius: 5px; padding: 10px;")
        self.output_text.setMinimumHeight(200)
        self.central_layout.addWidget(self.output_text)

    def summarize(self):
        # Summarize function to handle text summarization process
        input_text = self.input_text.toPlainText()
        max_words = int(self.max_words_input.toPlainText())
        if input_text and max_words > 0:
            try:
                # Load the pre-trained summarization model
                summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
                # Generate a summary of the text
                summary = summarizer(input_text, max_length=max_words, min_length=max_words//2, do_sample=False)[0]['summary_text']
                # Set the summary in the output text area
                self.output_text.setPlainText(summary)
            except Exception as e:
                # If summarization fails, display error message
                self.output_text.setPlainText("Summarization failed. Please try again.")
                print(f"Summarization error: {e}")

if __name__ == "__main__":
    # Create and run the application
    app = QApplication(sys.argv)
    window = SummarizerApp()
    sys.exit(app.exec_())
