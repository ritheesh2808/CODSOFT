# CodSoft Artificial Intelligence Internship

Welcome to the official repository for my **CodSoft Artificial Intelligence Internship**. This repository houses three desktop-based AI projects built with Python 3.12+, Tkinter, and Scikit-learn, featuring dark themes and clean architectures.

---

## 👨‍💻 Intern Profile
- **Name**: Ritheesh MG
- **Domain**: Artificial Intelligence
- **Duration**: 25 June 2026 – 25 July 2026
- **Status**: Completed (3/3 Tasks)

---

## 📂 Repository Structure

```text
CODSOFT/
│
├── docs/                             # Documentation resources
├── LICENSE                           # MIT License file
├── README.md                         # Main repository landing page (this file)
│
├── Task1_Chatbot/
│   ├── assets/                       # Custom graphic resources
│   ├── screenshots/                  # Run captures
│   ├── chatbot.py                    # Main executable for Chatbot
│   ├── README.md                     # Chatbot documentation
│   └── requirements.txt              # Task requirements (Standard Library)
│
├── Task2_TicTacToeAI/
│   ├── assets/                       # Custom graphic resources
│   ├── screenshots/                  # Run captures
│   ├── main.py                       # Main GUI executable for Tic-Tac-Toe
│   ├── minimax.py                    # AI Minimax evaluation module
│   ├── README.md                     # Game documentation
│   └── requirements.txt              # Task requirements (Standard Library)
│
└── Task3_RecommendationSystem/
    ├── dataset/
    │   └── movies.csv                # Content-based dataset
    ├── assets/                       # Custom graphic resources
    ├── screenshots/                  # Run captures
    ├── app.py                        # Recommendation engine and GUI
    ├── README.md                     # System documentation
    └── requirements.txt              # Task requirements (pandas, numpy, scikit-learn)
```

---

## 🚀 Projects Overview

| Task | Title | Description | Key Tech Stack | Link |
| :---: | :--- | :--- | :--- | :---: |
| **01** | **Rule-Based Chatbot** | Desktop chatbot answering queries dynamically using case-insensitive keyword mappings, complete with scrolling logs and timestamps. | Python, Tkinter, Logging | [View Project](./Task1_Chatbot) |
| **02** | **Tic-Tac-Toe AI** | Unbeatable Tic-Tac-Toe AI built with the Minimax algorithm and Alpha-Beta pruning, with turn delays and scoring. | Python, Tkinter, Minimax | [View Project](./Task2_TicTacToeAI) |
| **03** | **Movie Recommendation** | A content-based recommender dashboard analyzing movie features with TF-IDF Vectorization and Cosine Similarity. | Pandas, NumPy, Scikit-learn, Tkinter | [View Project](./Task3_RecommendationSystem) |

---

## 🛠️ System Prerequisites & Installation

To run these desktop GUI applications, you need a Python environment and the `tkinter` package installed on your operating system.

### 1. Operating System Dependency (Linux/Kali Linux)
Tkinter is packaged separately on Debian-based distributions. Open a terminal and execute:
```bash
sudo apt-get update
sudo apt-get install -y python3-tk
```

### 2. Python Environment Setup
1. Clone this repository:
   ```bash
   git clone https://github.com/ritheesh2808/CODSOFT.git
   cd CODSOFT
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install package requirements for Task 3 (Task 1 and Task 2 rely solely on standard libraries):
   ```bash
   pip install -r Task3_RecommendationSystem/requirements.txt
   ```

---

## 💡 Recommended Git Commit Plan

To maintain a clean version history, here is the suggested commit sequence used during the development stages of this repository:

1. **Stage 1 (Initialization & Setup)**
   ```text
   feat: initialize repository structure and configure ignore patterns
   ```
2. **Stage 2 (Task 1: Chatbot)**
   ```text
   feat(chatbot): implement rule-based chatbot engine and dark theme GUI
   docs(chatbot): add requirements and README documentation for Task 1
   ```
3. **Stage 3 (Task 2: Tic-Tac-Toe AI)**
   ```text
   feat(tictactoe): implement minimax algorithm with alpha-beta pruning
   feat(tictactoe): build interactive grid interface and scoreboard tracker
   docs(tictactoe): add game requirements and README documentation for Task 2
   ```
4. **Stage 4 (Task 3: Movie Recommender)**
   ```text
   feat(recommender): create movies dataset and TF-IDF similarity model
   feat(recommender): design dashboard GUI with suggestions and filters
   docs(recommender): add package requirements and system README for Task 3
   ```
5. **Stage 5 (Root Update & Polishing)**
   ```text
   docs: update root README landing page and finalize internship goals
   ```

---

## 📈 Future Improvements

- Containerize applications using Docker and configure X11 forwarding to support remote GUI displays.
- Set up automated CI/CD checks (such as GitHub Actions running `flake8` and python tests).
- Integrate speech-to-text inputs into the Chatbot GUI.

---

## 📄 License

This repository is distributed under the [MIT License](./LICENSE).

---

## 👤 Author

- **Ritheesh MG**
- GitHub: [ritheesh2808](https://github.com/ritheesh2808)