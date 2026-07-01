#!/usr/bin/env python3
"""
Rule-Based Chatbot Application
CodSoft AI Internship - Task 1
Developer: Ritheesh MG

This application implements a desktop chatbot using Tkinter with a modern dark theme.
It maps predefined user inputs to rules and provides appropriate, formatted responses.
"""

import logging
import random
import tkinter as tk
from datetime import datetime
from tkinter import scrolledtext, messagebox
from typing import Dict, List, Callable

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ]
)


class ChatbotEngine:
    """Handles the rule-based response generation logic."""

    def __init__(self) -> None:
        # Predefined responses for greeting rules
        self.greetings: List[str] = [
            "Hello! I am your AI assistant. How can I help you today?",
            "Hi there! How can I assist you?",
            "Hey! Great to see you. What can I do for you today?"
        ]

        # Developer info
        self.developer_info: str = (
            "I was developed by the talented Ritheesh MG for the CodSoft AI Internship.\n"
            "GitHub Portfolio: https://github.com/ritheesh2808"
        )

        # CodSoft info
        self.codsoft_info: str = (
            "CodSoft is an IT service and IT consulting company providing internships, "
            "mentorship, and hands-on project experience in domains like Artificial Intelligence, "
            "Web Development, and Android Development."
        )

        # AI info
        self.ai_info: str = (
            "Artificial Intelligence (AI) refers to the simulation of human intelligence "
            "in machines that are programmed to think and learn like humans. It includes "
            "subfields like Machine Learning, Deep Learning, Natural Language Processing, "
            "and Computer Vision."
        )

        # Jokes list
        self.jokes: List[str] = [
            "Why do programmers wear glasses? Because they can't C#!",
            "Why did the computer go to the doctor? Because it had a virus!",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
            "What is a programmer's favorite hangout place? Foo Bar!",
            "Why do computers crash? Because they get tired of your bugs!"
        ]

        # Facts list
        self.facts: List[str] = [
            "Honey never spoils. You could theoretically eat 3,000-year-old honey!",
            "Bananas are berries, but strawberries aren't!",
            "The first computer bug was an actual real moth found trapped in a relay by Grace Hopper in 1947.",
            "Wombat poop is cube-shaped, which stops it from rolling away!",
            "A day on Venus is longer than a year on Venus."
        ]

        # Motivational quotes
        self.quotes: List[str] = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "It always seems impossible until it's done. - Nelson Mandela",
            "Your limitation—it's only your imagination. - Unknown"
        ]

        # Fallback responses for unknown queries
        self.fallbacks: List[str] = [
            "I'm not sure I understand that. Can you try rephrasing?",
            "I don't have a rule for that yet! Type 'help' to see what I can do.",
            "Hmm, that's a bit outside my expertise. Ask me something else, or type 'help'.",
            "I couldn't quite grasp that. Feel free to ask about CodSoft, AI, or request a joke!"
        ]

    def get_response(self, user_query: str) -> str:
        """Processes the input query and returns a matching rule response."""
        query = user_query.lower().strip()
        logging.info("Processing query: '%s'", query)

        # Rule matching logic using substring analysis
        if any(greet in query for greet in ["hello", "hi", "hey"]):
            return random.choice(self.greetings)

        elif "bye" in query or "goodbye" in query:
            return "Goodbye! Have a wonderful day ahead. Feel free to chat again anytime!"

        elif "thank" in query:
            return "You're very welcome! I'm happy to help."

        elif "help" in query:
            return (
                "Here are the things you can ask me:\n"
                "• Greetings ('hello', 'hi', 'hey')\n"
                "• Farewell ('bye')\n"
                "• Identity ('who are you', 'what can you do')\n"
                "• Fun ('tell me a joke', 'tell me a fact')\n"
                "• Inspiration ('motivational quote')\n"
                "• Date & Time ('today's date', 'current time')\n"
                "• Information ('codsoft', 'artificial intelligence')\n"
                "• Creator ('your developer')"
            )

        elif "who are you" in query:
            return (
                "I am a Rule-Based Chatbot assistant created to demonstrate basic "
                "decision-making patterns using Python and Tkinter."
            )

        elif "what can you do" in query:
            return (
                "I can answer predefined queries, display the current date/time, tell you jokes, "
                "share interesting facts, provide motivational quotes, and tell you about AI and CodSoft!"
            )

        elif "joke" in query:
            return random.choice(self.jokes)

        elif "fact" in query:
            return random.choice(self.facts)

        elif "quote" in query or "motivation" in query:
            return random.choice(self.quotes)

        elif "date" in query:
            today = datetime.now().strftime("%A, %B %d, %Y")
            return f"Today's date is: {today}"

        elif "time" in query:
            now = datetime.now().strftime("%I:%M:%S %p")
            return f"The current time is: {now}"

        elif "developer" in query or "creator" in query or "ritheesh" in query:
            return self.developer_info

        elif "codsoft" in query:
            return self.codsoft_info

        elif "artificial intelligence" in query or "ai" in query:
            # Prevent short words like "said" triggering AI info
            words = query.split()
            if "ai" in words or "artificial" in words or "intelligence" in words or "what is ai" in query:
                return self.ai_info

        # Fallback response for unmatched query
        return random.choice(self.fallbacks)


class ChatbotGUI:
    """Manages the visual presentation and interactions of the chatbot."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("CodSoft AI Chatbot")
        self.root.geometry("480x600")
        self.root.resizable(False, False)

        # Initialize the response engine
        self.engine = ChatbotEngine()

        # Modern Dark Color Palette (Catppuccin Mocha themed)
        self.colors = {
            "bg": "#181825",          # Dark base background
            "header_bg": "#11111b",   # Darker header bar
            "input_bg": "#313244",    # Medium dark for text boxes
            "text": "#cdd6f4",        # Soft white for primary text
            "subtext": "#a6adc8",     # Muted gray-blue
            "user_bubble": "#cba6f7", # Light purple for user message text
            "bot_bubble": "#a6e3a1",  # Mint green for bot message text
            "system_text": "#f5e0dc", # Peach for logs/clean notifications
            "button_bg": "#89b4fa",   # Pastel blue for CTA buttons
            "button_fg": "#11111b",   # Contrast dark text for button
            "button_hover": "#b4befe" # Lighter blue-purple for hover
        }

        # Apply root background
        self.root.configure(bg=self.colors["bg"])

        self._create_widgets()
        self._setup_bindings()
        self._welcome_message()

    def _create_widgets(self) -> None:
        """Constructs the application layout."""
        # --- Header Section ---
        header = tk.Frame(self.root, bg=self.colors["header_bg"], height=70, bd=0)
        header.pack(fill=tk.X, side=tk.TOP)
        header.pack_propagate(False)

        title_label = tk.Label(
            header,
            text="CodSoft AI Assistant",
            font=("Helvetica", 14, "bold"),
            bg=self.colors["header_bg"],
            fg=self.colors["text"]
        )
        title_label.pack(anchor=tk.W, padx=20, pady=(12, 2))

        subtitle_label = tk.Label(
            header,
            text="Rule-Based Chatbot • Developed by Ritheesh MG",
            font=("Helvetica", 9),
            bg=self.colors["header_bg"],
            fg=self.colors["subtext"]
        )
        subtitle_label.pack(anchor=tk.W, padx=20)

        # --- Chat Display Area (Scrollable) ---
        chat_frame = tk.Frame(self.root, bg=self.colors["bg"])
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(15, 10))

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Helvetica", 10),
            bg=self.colors["bg"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            bd=0,
            highlightthickness=0,
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        # Make read-only by default
        self.chat_display.configure(state=tk.DISABLED)

        # Configure custom text tags for formatting
        self.chat_display.tag_configure("timestamp", foreground=self.colors["subtext"], font=("Helvetica", 8))
        self.chat_display.tag_configure("user", foreground=self.colors["user_bubble"], font=("Helvetica", 10, "bold"))
        self.chat_display.tag_configure("bot", foreground=self.colors["bot_bubble"], font=("Helvetica", 10, "bold"))
        self.chat_display.tag_configure("system", foreground=self.colors["system_text"], font=("Helvetica", 9, "italic"))
        self.chat_display.tag_configure("text_normal", foreground=self.colors["text"])
        self.chat_display.tag_configure("text_indent", lmargin1=15, lmargin2=15)

        # --- Input Section ---
        input_frame = tk.Frame(self.root, bg=self.colors["bg"])
        input_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=15, pady=(5, 15))

        self.entry_box = tk.Entry(
            input_frame,
            font=("Helvetica", 11),
            bg=self.colors["input_bg"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            bd=0,
            highlightthickness=1,
            highlightbackground=self.colors["input_bg"],
            highlightcolor=self.colors["button_bg"]
        )
        self.entry_box.pack(fill=tk.X, side=tk.LEFT, expand=True, ipady=8, padx=(0, 10))
        self.entry_box.focus_set()

        # Send Button
        self.send_button = tk.Button(
            input_frame,
            text="Send",
            font=("Helvetica", 10, "bold"),
            bg=self.colors["button_bg"],
            fg=self.colors["button_fg"],
            activebackground=self.colors["button_hover"],
            activeforeground=self.colors["button_fg"],
            bd=0,
            cursor="hand2",
            padx=15,
            command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT, ipady=6)

        # Hover effects for Send Button
        self.send_button.bind("<Enter>", lambda e: self.send_button.configure(bg=self.colors["button_hover"]))
        self.send_button.bind("<Leave>", lambda e: self.send_button.configure(bg=self.colors["button_bg"]))

        # --- Top Menu / Controls ---
        # Add a tiny top bar option to clear chat
        clear_button = tk.Button(
            header,
            text="Clear",
            font=("Helvetica", 8, "bold"),
            bg=self.colors["input_bg"],
            fg=self.colors["text"],
            activebackground=self.colors["bg"],
            activeforeground=self.colors["text"],
            bd=0,
            cursor="hand2",
            padx=10,
            command=self.clear_chat
        )
        clear_button.place(x=410, y=20)

    def _setup_bindings(self) -> None:
        """Binds input events."""
        self.entry_box.bind("<Return>", lambda event: self.send_message())

    def _welcome_message(self) -> None:
        """Inserts initial greetings into the display."""
        time_str = datetime.now().strftime("%I:%M %p")
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[{time_str}] ", "timestamp")
        self.chat_display.insert(tk.END, "System: ", "system")
        self.chat_display.insert(tk.END, "Welcome to the Chatbot! Type 'help' to see available commands.\n\n", "text_normal")
        self.chat_display.configure(state=tk.DISABLED)

    def send_message(self) -> None:
        """Extracts user text, generates response, and updates the display."""
        user_text = self.entry_box.get().strip()
        if not user_text:
            return

        # Clear entry box immediately
        self.entry_box.delete(0, tk.END)

        # Show user message
        time_str = datetime.now().strftime("%I:%M %p")
        self.chat_display.configure(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[{time_str}] ", "timestamp")
        self.chat_display.insert(tk.END, "You: ", "user")
        self.chat_display.insert(tk.END, f"{user_text}\n", "text_normal")

        # Get bot response
        try:
            bot_response = self.engine.get_response(user_text)
        except Exception as e:
            logging.error("Error generating response: %s", str(e))
            bot_response = "Oops! An internal error occurred. Please try again."

        # Show bot message
        self.chat_display.insert(tk.END, f"[{time_str}] ", "timestamp")
        self.chat_display.insert(tk.END, "Bot: ", "bot")
        self.chat_display.insert(tk.END, f"{bot_response}\n\n", "text_normal")

        # Autoscroll to bottom
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.yview(tk.END)

    def clear_chat(self) -> None:
        """Wipes the conversation log after confirmation."""
        if messagebox.askyesno("Clear Chat", "Are you sure you want to clear the conversation?"):
            self.chat_display.configure(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.configure(state=tk.DISABLED)
            self._welcome_message()
            logging.info("Chat screen cleared.")


def main() -> None:
    """Application entry point."""
    try:
        root = tk.Tk()
        app = ChatbotGUI(root)
        root.mainloop()
    except Exception as e:
        logging.critical("Failed to start application: %s", str(e))
        messagebox.showerror("Fatal Error", f"Failed to start chatbot application:\n{str(e)}")


if __name__ == "__main__":
    main()
