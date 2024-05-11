import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from transformers import pipeline

class QAApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Question Answering")  # Set window title
        self.setWindowIcon(QIcon('icon.ico'))  # Set window icon
        self.setGeometry(300, 300, 800, 600)  # Set window geometry

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout(self.central_widget)
        self.central_layout.setAlignment(Qt.AlignCenter)

        self.init_ui()  # Initialize UI elements
        self.show()  # Show the window

    def init_ui(self):
        # Label for passage input
        self.passage_label = QLabel("Enter your passage:")
        self.central_layout.addWidget(self.passage_label)

        # TextEdit widget for passage input
        self.passage_input = QTextEdit(self)
        self.passage_input.setPlaceholderText("Type your passage here")
        self.passage_input.setStyleSheet("font-size: 16px; border: 2px solid #ccc; border-radius: 5px; padding: 10px;")
        self.passage_input.setMinimumHeight(200)
        self.central_layout.addWidget(self.passage_input)

        # Label for question input
        self.question_label = QLabel("Enter your question:")
        self.central_layout.addWidget(self.question_label)

        # TextEdit widget for question input
        self.question_input = QTextEdit(self)
        self.question_input.setPlaceholderText("Type your question here")
        self.question_input.setStyleSheet("font-size: 16px; border: 2px solid #ccc; border-radius: 5px; padding: 10px;")
        self.question_input.setMinimumHeight(40)
        self.central_layout.addWidget(self.question_input)

        # Button to get the answer
        self.answer_button = QPushButton("Get Answer", self)
        self.answer_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-size: 18px; font-weight: bold; border-radius: 5px; padding: 10px 20px; } QPushButton:hover { background-color: #3e8e41; }")
        self.answer_button.clicked.connect(self.get_answer)  # Connect button click event to get_answer function
        self.central_layout.addWidget(self.answer_button, alignment=Qt.AlignCenter)

        # TextEdit widget to display the answer
        self.answer_output = QTextEdit(self)
        self.answer_output.setReadOnly(True)
        self.answer_output.setStyleSheet("font-size: 16px; border: 2px solid #ccc; border-radius: 5px; padding: 10px;")
        self.answer_output.setMinimumHeight(200)
        self.central_layout.addWidget(self.answer_output)

    def get_answer(self):
        # Retrieve passage and question input
        passage = self.passage_input.toPlainText()
        question = self.question_input.toPlainText()
        if passage and question:  # Check if both passage and question are provided
            try:
                # Load question-answering pipeline model
                qa_model = pipeline("question-answering", model="bert-large-uncased-whole-word-masking-finetuned-squad")
                # Get answer using the model
                answer = qa_model(question=question, context=passage, min_answer_len=50, max_answer_len=90)
                # Display the answer
                self.answer_output.setPlainText(answer['answer'])
            except Exception as e:
                # Display error message if failed to get answer
                self.answer_output.setPlainText(f"Failed to get answer: {e}")

if __name__ == "__main__":
    # Create QApplication instance
    app = QApplication(sys.argv)
    # Create QAApp instance
    window = QAApp()
    # Start the application event loop
    sys.exit(app.exec_())
