import openai
import requests
import base64
import re
import tkinter as tk
from tkinter import simpledialog, messagebox, Text, Scrollbar

# It's recommended to fetch API keys from a secure location or environment variable.
# For the sake of this example, they are hardcoded.
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY_HERE'
GITHUB_TOKEN = 'YOUR_GITHUB_TOKEN_HERE'

openai.api_key = OPENAI_API_KEY

class GitHubRepoPlugin:
    # ... [rest of the GitHubRepoPlugin class as provided]

def chat_with_gpt(message, conversation_history="", temperature=0.7, max_tokens=150):
    plugin = GitHubRepoPlugin(GITHUB_TOKEN)
    
    # Check if the message is a URL
    if "github.com" in message:
        plugin_response = plugin.query(message)
        conversation_history += f"User: {message}\nAgent: {plugin_response}\n"
    
    # Pass the message (and any GitHub info) to OpenAI API
    conversation_payload = {
        "messages": [{"role": "user", "content": message}],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post("https://api.openai.com/v2/completions", headers=headers, json=conversation_payload)
        response_data = response.json()
        
        # Check for errors in the response
        if 'error' in response_data:
            return response_data['error']['message'], conversation_history
        
        assistant_response = response_data['choices'][0]['message']['content']
        conversation_history += f"Assistant: {assistant_response}\n"
        return assistant_response, conversation_history
    except Exception as e:
        return str(e), conversation_history

class ChatGPTGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("gitmaster GitHub Plugin")

        self.conversation_history = ""
        self.temperature = 0.7
        self.max_tokens = 300

        self.text_widget = Text(root, wrap=tk.WORD, state=tk.DISABLED)
        self.text_widget.pack(expand=1, fill=tk.BOTH, padx=10, pady=10)

        self.scrollbar = Scrollbar(root, command=self.text_widget.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_widget.config(yscrollcommand=self.scrollbar.set)

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', self.send_message)

        self.button = tk.Button(root, text="Send", command=self.send_message)
        self.button.pack(pady=10)

        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        self.settings_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Modify Agent", command=self.modify_agent)

    def send_message(self, event=None):
        user_message = self.entry.get()
        if user_message:
            response, self.conversation_history = chat_with_gpt(user_message, self.conversation_history, self.temperature, self.max_tokens)
            self.display_message(f"User: {user_message}\nAgent: {response}\n")
            self.entry.delete(0, tk.END)

    def display_message(self, message):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)

    def modify_agent(self):
        def apply_changes():
            self.temperature = temperature_slider.get()
            self.max_tokens = int(max_tokens_entry.get())
            modify_window.destroy()
            messagebox.showinfo("Info", f"Agent modified with temperature: {self.temperature} and max tokens: {self.max_tokens}")

        modify_window = tk.Toplevel(self.root)
        modify_window.title("Modify Agent Parameters")

        # Temperature
        temperature_label = tk.Label(modify_window, text="Temperature:")
        temperature_label.pack(pady=10)

        temperature_slider = tk.Scale(modify_window, from_=0.0, to=10.0, resolution=0.01, orient=tk.HORIZONTAL)
        temperature_slider.set(self.temperature)
        temperature_slider.pack(pady=10)

        # Max Tokens
        max_tokens_label = tk.Label(modify_window, text="Max Tokens:")
        max_tokens_label.pack(pady=10)

        max_tokens_entry = tk.Entry(modify_window)
        max_tokens_entry.insert(0, str(self.max_tokens))
        max_tokens_entry.pack(pady=10)

        apply_button = tk.Button(modify_window, text="Apply", command=apply_changes)
        apply_button.pack(pady=10)

root = tk.Tk()
gui = ChatGPTGUI(root)
root.mainloop()