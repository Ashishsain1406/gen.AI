import google.generativeai as genai
from colorama import Fore, Style, init
import time
import speech_recognition as sr

# Initialize colorama
init(autoreset=True)

# Configure Gemini API
API_KEY = "AIzaSyD6IbGb60_BBafC_GrW2MYDtyJ9xFZMUD0"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

# Typing effect function
def type_print(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.02)
    print()

# Voice input function
def listen_to_mic():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(Fore.LIGHTBLUE_EX + "🎤 Listening... (speak now)")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(Fore.YELLOW + "You (voice): " + text)
        return text
    except sr.UnknownValueError:
        print(Fore.RED + "Sorry, I couldn’t understand. Try again.")
        return None
    except sr.RequestError:
        print(Fore.RED + "Could not request results; check internet.")
        return None

# Chat history
history = []

# Welcome message
print(Fore.CYAN + "🎯 Gemini Chatbot with Voice Input")
print("Type 'exit' to quit, press Enter to speak, or use /help\n")

# Main chat loop
while True:
    user_input = input(Fore.YELLOW + "You: " + Style.RESET_ALL)

    if user_input.strip() == "":
        user_input = listen_to_mic()
        if not user_input:
            continue

    if user_input.lower() == "exit":
        break

    elif user_input.lower() == "/help":
        print(Fore.BLUE + "\nAvailable Commands:")
        print(" - exit: Quit the chat")
        print(" - /clear: Clear chat history")
        print(" - /history: Show all past messages")
        print(" - [Press Enter]: Use mic to speak\n")
        continue

    elif user_input.lower() == "/clear":
        history.clear()
        print(Fore.MAGENTA + "Chat history cleared.\n")
        continue

    elif user_input.lower() == "/history":
        print(Fore.CYAN + "\n--- Chat History ---")
        for speaker, message in history:
            color = Fore.YELLOW if speaker == "You" else Fore.GREEN
            print(color + f"{speaker}: {message}")
        print(Fore.CYAN + "--- End of History ---\n")
        continue

    # Get Gemini response
    response = chat.send_message(user_input)
    history.append(("You", user_input))
    history.append(("Gemini", response.text))

    # Print only latest reply
    print(Fore.GREEN + "Gemini: ", end='')
    type_print(response.text)
    print(Fore.LIGHTBLACK_EX + "-" * 50)

# Save chat log
with open("chat_log.txt", "w", encoding="utf-8") as f:
    for speaker, message in history:
        f.write(f"{speaker}: {message}\n")

print(Fore.CYAN + "Chat saved to 'chat_log.txt'. Goodbye!")