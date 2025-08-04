import google.generativeai as genai
from colorama import Fore, Style, init
import time

# Initialize colorama for colored terminal text
init(autoreset=True)

# Set up your Gemini API key
API_KEY = "AIzaSyCPFgvzO3z2k9DLqUxcGNe1HkA9Xcpx2z0"
genai.configure(api_key=API_KEY)

# Load Gemini model and start a chat session
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

# Typing effect for Gemini's reply
def type_print(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.02)
    print()

# Store the chat history (but don’t show it by default)
history = []

# Welcome message
print(Fore.CYAN + "Welcome to Gemini Chatbot!")
print(f"{Fore.LIGHTGREEN_EX}Type 'exit' to quit, '/help' for available commands.\n")

# Main chat loop
while True:
    user_input = input(Fore.YELLOW + "You: " + Style.RESET_ALL)

    if user_input.lower() == 'exit':
        break

    elif user_input.lower() == '/help':
        print(Fore.BLUE + "Available Commands:")
        print(" - exit: Quit the chat")
        print(" - /clear: Clear chat history")
        print(" - /history: Show all past messages\n")
        continue

    elif user_input.lower() == '/clear':
        history.clear()
        print(Fore.MAGENTA + "Chat history cleared.\n")
        continue

    elif user_input.lower() == '/history':
        print(Fore.CYAN + "\n--- Chat History ---")
        for speaker, message in history:
            color = Fore.YELLOW if speaker == "You" else Fore.GREEN
            print(color + f"{speaker}: {message}")
        print(Fore.CYAN + "--- End of History ---\n")
        continue

    # Send message to Gemini and store response
    response = chat.send_message(user_input)
    history.append(("You", user_input))
    history.append(("Gemini", response.text))

    # ✅ Only show the latest Gemini reply
    print(Fore.GREEN + "Gemini: ", end='')
    type_print(response.text)
    print(Fore.LIGHTBLACK_EX + "-" * 50)

# Save full chat log when the session ends
with open("chat_log.txt", "w", encoding='utf-8') as f:
    for speaker, message in history:
        f.write(f"{speaker}: {message}\n")

print(Fore.CYAN + "Chat saved to 'chat_log.txt'. Goodbye!")