import sys  # Importing the sys module for system-specific parameters and functions
from PyQt5.QtWidgets import (  # Importing necessary classes from PyQt5 module for GUI application
    QApplication,
    QMainWindow,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
)
from PyQt5.QtGui import QIcon, QFont  # Importing QIcon and QFont classes from PyQt5.QtGui module
from PyQt5.QtCore import Qt  # Importing Qt class from PyQt5.QtCore module
from transformers import pipeline, set_seed  # Importing pipeline and set_seed functions from transformers module
from sacremoses import MosesTokenizer, MosesDetokenizer  # Importing MosesTokenizer and MosesDetokenizer classes from sacremoses module

# Defining a class for the GPT Chat application, inheriting from QMainWindow
class GPTChatApp(QMainWindow):
    def __init__(self):
        super().__init__()  # Calling the superclass constructor
        self.setWindowTitle("GPT Chat")  # Setting window title
        self.setWindowIcon(QIcon('icon.ico'))  # Setting window icon
        self.setGeometry(300, 300, 800, 600)  # Set window geometry

        # Creating a central widget and setting it as the central widget for the main window
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_layout = QVBoxLayout(self.central_widget)  # Creating a vertical box layout
        self.central_layout.setAlignment(Qt.AlignCenter)  # Aligning widgets to the center

        self.init_ui()  # Initializing the user interface
        self.show()  # Displaying the main window

    # Method to initialize the user interface
    def init_ui(self):
        # Adding a label for the prompt
        self.prompt_label = QLabel("Enter your prompt:")
        self.central_layout.addWidget(self.prompt_label)

        # Adding a text input field for entering the prompt
        self.prompt_input = QTextEdit(self)
        self.prompt_input.setPlaceholderText("Type your prompt here")
        self.prompt_input.setStyleSheet("font-size: 16px; border: 2px solid #ccc; border-radius: 5px; padding: 10px;")
        self.prompt_input.setMinimumHeight(200)
        self.central_layout.addWidget(self.prompt_input)

        # Adding a label for max tokens
        self.max_length_label = QLabel("Max Tokens:")
        self.central_layout.addWidget(self.max_length_label)

        # Adding a text input field for entering the max tokens
        self.max_length_input = QTextEdit(self)
        self.max_length_input.setPlaceholderText("Enter max tokens")
        self.max_length_input.setStyleSheet("font-size: 16px; border: 2px solid #ccc; border-radius: 5px; padding: 10px;")
        self.max_length_input.setMinimumHeight(40)
        self.central_layout.addWidget(self.max_length_input)

        # Adding a button for generating the answer
        self.generate_button = QPushButton("Generate Answer", self)
        self.generate_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-size: 18px; font-weight: bold; border-radius: 5px; padding: 10px 20px; } QPushButton:hover { background-color: #3e8e41; }")
        self.generate_button.clicked.connect(self.generate_answer)  # Connecting button click event to generate_answer method
        self.central_layout.addWidget(self.generate_button, alignment=Qt.AlignCenter)

        # Adding a text output field for displaying the generated answer
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("font-size: 16px; border: 2px solid #ccc; border-radius: 5px; padding: 10px;")
        self.output_text.setMinimumHeight(200)
        self.central_layout.addWidget(self.output_text)

    # Method to generate the answer based on the user prompt
    def generate_answer(self):
        prompt = self.prompt_input.toPlainText()  # Getting the prompt text from the input field
        max_tokens = int(self.max_length_input.toPlainText()) if self.max_length_input.toPlainText() else None  # Getting the max tokens value
        if prompt:  # Checking if the prompt is not empty
            try:
                set_seed(42)  # Setting the random seed for reproducibility
                generator = pipeline('text-generation', model='gpt2-xl')  # Creating a text generation pipeline with GPT-2 XL model
                generated_text = generator(prompt, max_length=max_tokens, num_return_sequences=1)[0]['generated_text']  # Generating text based on the prompt
                self.output_text.setPlainText(generated_text)  # Displaying the generated text in the output field
            except Exception as e:  # Handling exceptions
                self.output_text.setPlainText(f"Generation failed: {e}")  # Displaying error message if generation fails

# Entry point of the program
if __name__ == "__main__":
    app = QApplication(sys.argv)  # Creating a PyQt application instance
    window = GPTChatApp()  # Creating an instance of GPTChatApp
    sys.exit(app.exec_())  # Executing the application
