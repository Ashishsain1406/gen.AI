# gen.AI
Gemini Command-Line Chatbot

🤖 Description

This is a simple command-line chatbot built using Google's Gemini API. It simulates a conversation with an AI assistant, with support for:

Typing effects for AI responses

Colored terminal output (via colorama)

Chat history management (/history, /clear)

Logging full chat session to a .txt file



---

🛠 Requirements

Install the required packages:

pip install google-generativeai colorama

If you want voice input (optional):

pip install SpeechRecognition pyaudio


---

🔑 Gemini API Key

You must have a Gemini API key from Google AI Studio.

Replace the following line with your own key:

API_KEY = "YOUR_API_KEY"


---

🚀 How to Run

python gemini_chatbot.py

You’ll see:

Welcome to Gemini Chatbot!
Type 'exit' to quit, '/help' for available commands.


---

🧠 Available Commands

Command	Description

/help	Show available commands
/clear	Clear the chat history
/history	View full chat history
exit	Exit the chatbot
/voice	(Optional) Speak to Gemini via mic



---

💾 Output

On exit, the chat is saved to a file:

chat_log.txt


---

📸 Screenshot

You: Hello!
Gemini: Hi there! How can I help you today?
--------------------------------------------------


---

🧑‍💻 Author

Made with ❤ by [Your Name
