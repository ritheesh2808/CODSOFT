# Task 1: Rule-Based Chatbot

A production-quality desktop chatbot application built using Python 3.12+ and Tkinter. This chatbot features a beautiful custom dark theme, message scrollability, Enter key bindings, message timestamps, a chat history clearing option, and robust rule-based parsing for 16+ conversational keywords and phrases.

---

## Overview

The Rule-Based Chatbot is a desktop-based virtual assistant designed to respond to predefined keywords and user inputs. It parses incoming messages case-insensitively and maps them to tailored answers. When a query doesn't match any criteria, the engine issues a friendly random fallback response, guiding the user back to supported commands.

---

## Features

- **Tkinter GUI with Custom Dark Theme**: Inspired by the modern Catppuccin Mocha palette, featuring soft-lit colors (Mint green, Lavender, and Slate) to reduce eye strain.
- **Scrollable Chat Log**: Powered by a read-only scrolled text widget to show messaging history seamlessly.
- **Enter Key Support**: Pressing the `Enter` key automatically triggers message dispatch.
- **Clear Chat button**: Allows users to wipe current conversations and reset to the greeting message.
- **Timestamps**: Messages are prepended with dynamic real-time system timestamps (`[HH:MM PM]`).
- **Flexible Pattern Matching**: Substring matching checks if queries contain greetings, request dates, time, facts, jokes, or project-specific details.

---

## Technologies Used

- **Python 3.12+**
- **Tkinter** (Standard Python GUI toolkit)
- **Logging** (Standard logging for capturing application runs and user prompts)
- **Datetime / Random** (Utility packages)

---

## Project Folder Structure

```text
Task1_Chatbot/
│
├── assets/             # Graphical assets
├── screenshots/        # Application screenshots
├── chatbot.py          # Main application executable
├── README.md           # Documentation (this file)
└── requirements.txt    # Package specifications
```

---

## Requirements

1. **Python 3.12+**
2. **Tkinter Library**:
   - On Windows/macOS, Tkinter is bundled with Python.
   - On Linux (Debian/Kali), you must install it using the system package manager:
     ```bash
     sudo apt-get update
     sudo apt-get install python3-tk
     ```

---

## Installation & Running

1. Clone or navigate to the project directory:
   ```bash
   cd Task1_Chatbot
   ```
2. (Optional) Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Run the application:
   ```bash
   python3 chatbot.py
   ```

---

## Usage Guide

- **Interacting**: Type messages into the bottom entry field and click **Send** or press **Enter**.
- **Supported Keywords**:
  - Greeting: `hello`, `hi`, `hey`
  - Farewell: `bye`
  - Appreciation: `thank you`
  - Menu List: `help`
  - Bot Identity: `who are you`, `what can you do`
  - Dynamic Info: `today's date`, `current time`
  - Content requests: `tell me a joke`, `tell me a fact`, `motivational quote`
  - Institutional Info: `codsoft`, `artificial intelligence`
  - Developer Info: `your developer` or `creator`
- **Clear Window**: Click the **Clear** button in the top-right corner to reset the chat view.

---

## Screenshots

Below is a placeholder indicating where visual previews of the application interface are placed.

| Chatbot Interface | Chat Settings & Rules |
|:---:|:---:|
| ![Main Chat Interface](screenshots/chatbot_main_placeholder.png) | ![Chat Helper Responses](screenshots/chatbot_rules_placeholder.png) |

---

## Future Improvements

- Add local file logging to save conversation history persistently.
- Integrate fuzzy matching using standard algorithms (like Levenshtein distance) to handle spelling typos in commands.
- Expand command configurations using an external JSON/YAML file.

---

## License

This project is licensed under the [MIT License](../LICENSE).

---

## Author

- **Ritheesh MG**
- GitHub: [ritheesh2808](https://github.com/ritheesh2808)
