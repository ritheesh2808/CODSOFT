# Task 3: Movie Recommendation System

A content-based desktop movie recommendation system built using Python 3.12+, Pandas, NumPy, and Scikit-learn. It processes movie textual elements (genres, plot overviews, keywords, directors, and actors) using TF-IDF Vectorization and Cosine Similarity, delivering suggestions via a Tkinter dashboard.

---

## Overview

The Movie Recommendation System calculates textual similarity between a reference movie and the rest of the database. By combining plot overviews, keywords, genres, directors, and cast names, it builds a rich metadata profile for each film. Using Term Frequency-Inverse Document Frequency (TF-IDF) representation and Cosine Similarity calculations, the system rates how closely other movies match the user's selected title.

---

## Features

- **Self-Healing Dataset**: The application loads a sample dataset from `dataset/movies.csv`. If the CSV file is deleted or missing, the program automatically regenerates the dataset on startup.
- **Dynamic Search Auto-Suggestions**: A Listbox updates suggestions dynamically as the user types, ensuring rapid finding of titles.
- **Advanced Filtering**: Users can filter recommendations by genre (extracted dynamically from the dataset) and minimum average rating.
- **Match Similarity Percentage**: Each recommended movie card displays a computed match percentage (e.g. `95% Match`), showing how mathematically similar the film is.
- **Responsive Scrollable Layout**: Results are displayed as individual cards inside a canvas layout, complete with scrollbar support and cross-platform mouse wheel scroll bindings (active on hover).

---

## Technical Concept

1. **Feature Aggregation**: For each movie, the features are concatenated:
   $$\text{Combined Tag} = \text{genres} + \text{keywords} + \text{overview} + \text{director} + \text{cast}$$
   Names of directors and cast members have spaces removed (e.g. "Christopher Nolan" becomes "christophernolan") to ensure they are treated as distinct, unique tokens.
2. **Vectorization**: A `TfidfVectorizer` transforms the combined tags into numerical vectors, filtering out standard English stop words.
3. **Similarity**: The cosine similarity matrix is computed:
   $$\text{similarity}(A, B) = \cos(\theta) = \frac{A \cdot B}{\|A\| \|B\|}$$
   This results in scores ranging from $0$ (completely dissimilar) to $1$ (identical).

---

## Technologies Used

- **Python 3.12+**
- **Tkinter** (Python Desktop GUI package)
- **Pandas** (Data loading, cleanup, and queries)
- **NumPy** (Numerical calculations)
- **Scikit-learn** (TF-IDF Vectorization & Cosine Similarity)

---

## Folder Structure

```text
Task3_RecommendationSystem/
│
├── dataset/
│   └── movies.csv      # Sample movie dataset
│
├── assets/             # Graphical assets
├── screenshots/        # Application screenshots
├── app.py              # Main dashboard executable
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
3. **Python Libraries**:
   Install Python dependencies via `pip`:
   ```bash
   pip install -r requirements.txt
   ```

---

## Installation & Running

1. Clone or navigate to the project directory:
   ```bash
   cd Task3_RecommendationSystem
   ```
2. (Optional) Set up a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python3 app.py
   ```

---

## Usage Guide

1. **Selecting a Movie**: Start typing a title (e.g., "Inception") in the search box. The box below will filter matching options. Click on any item in the suggestion box to select it.
2. **Filtering**:
   - Select a genre from the **Select Genre** dropdown.
   - Slide the **Minimum Rating** scale to filter out lower-rated movies.
   - Spin the **Number of Suggestions** count to change how many card recommendations are displayed (between 3 and 15).
3. **Get Recommendations**: Click the button to calculate similarities and populate the scrollable panel with recommended movie cards.

---

## Screenshots

Below is a placeholder indicating where visual previews of the application interface are placed.

| Dashboard Search & Suggestions | Recommended Results |
|:---:|:---:|
| ![Main Interface](screenshots/recommender_main_placeholder.png) | ![Recommendations List](screenshots/recommender_results_placeholder.png) |

---

## Future Improvements

- Incorporate collaborative filtering (using user ratings matrices) if a larger database is integrated.
- Fetch live posters and ratings from public APIs (such as OMDb or TMDB) to display movie art.

---

## License

This project is licensed under the [MIT License](../LICENSE).

---

## Author

- **Ritheesh MG**
- GitHub: [ritheesh2808](https://github.com/ritheesh2808)
