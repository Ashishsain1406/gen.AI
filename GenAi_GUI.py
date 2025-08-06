import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import time
import threading
from colorama import Fore, Style, init
import google.generativeai as genai
import sounddevice as sd
import queue
import json
import vosk

# Initialize colorama
init(autoreset=True)

# === Configure Gemini API ===
API_KEY = "AIzaSyBF9MpaY76QPhfo14iz7GYgGVqsJqY4e4A"  # <-- Replace with your actual key
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat()

# === Voice Input using Vosk ===
q = queue.Queue()
model_vosk = vosk.Model(lang="en-us")

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def listen_voice():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model_vosk, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "")

# === GUI Application ===
class GeminiApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gemini AI Chat")
        self.root.geometry("600x600")
        self.root.configure(bg="black")

        self.chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 12), bg="black", fg="white")
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.chat_area.config(state=tk.DISABLED)

        self.entry = tk.Entry(root, font=("Consolas", 12))
        self.entry.pack(fill=tk.X, padx=10, pady=5)
        self.entry.bind("<Return>", self.send_message)

        btn_frame = tk.Frame(root, bg="black")
        btn_frame.pack(pady=5)

        self.send_button = tk.Button(btn_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5)

        self.voice_button = tk.Button(btn_frame, text="🎙 Speak", command=self.voice_input)
        self.voice_button.pack(side=tk.LEFT, padx=5)

    def display_typing(self, speaker, text):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, f"{speaker}: ", ("bold",))
        for char in text:
            self.chat_area.insert(tk.END, char)
            self.chat_area.see(tk.END)
            self.root.update()
            time.sleep(0.02)
        self.chat_area.insert(tk.END, "\n\n")
        self.chat_area.config(state=tk.DISABLED)

    def send_message(self, event=None):
        user_input = self.entry.get()
        if not user_input.strip():
            return
        self.entry.delete(0, tk.END)
        threading.Thread(target=self.process_message, args=(user_input,), daemon=True).start()

    def process_message(self, user_input):
        self.display_typing("You", user_input)
        try:
            response = chat.send_message(user_input)
            reply = response.text
            self.display_typing("Gemini", reply)
        except Exception as e:
            self.display_typing("Error", str(e))

    def voice_input(self):
        self.display_typing("System", "Listening... Speak now.")
        try:
            text = listen_voice()
            if text:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, text)
                self.send_message()
            else:
                self.display_typing("System", "Sorry, I couldn't understand your voice.")
        except Exception as e:
            self.display_typing("Error", str(e))

# === Main ===
if __name__ == "__main__":
    root = tk.Tk()
    app = GeminiApp(root)
    root.mainloop()