#!/usr/bin/env python3
"""
Movie Recommendation System - GUI Application
CodSoft AI Internship - Task 3
Developer: Ritheesh MG

This application implements a content-based movie recommendation system.
It processes text attributes (genres, keywords, overview, director, cast) 
using TF-IDF Vectorization and Cosine Similarity, presenting results in a 
highly polished Tkinter desktop dashboard.
"""

import logging
import os
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Tuple, Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Relative paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
CSV_PATH = os.path.join(DATASET_DIR, "movies.csv")


class RecommendationEngine:
    """Handles dataset loading, TF-IDF vectorization, and similarity scores."""

    def __init__(self) -> None:
        self.df: pd.DataFrame = pd.DataFrame()
        self.similarity_matrix: np.ndarray = np.array([])
        self.genres_list: List[str] = []
        self._load_dataset()
        self._build_similarity_model()

    def _load_dataset(self) -> None:
        """Loads dataset from CSV, self-heals by writing defaults if missing."""
        if not os.path.exists(DATASET_DIR):
            os.makedirs(DATASET_DIR)

        if not os.path.exists(CSV_PATH):
            logging.warning("dataset/movies.csv not found. Re-generating default dataset...")
            self._write_default_csv()

        try:
            self.df = pd.read_csv(CSV_PATH)
            # Ensure proper types
            self.df['movie_id'] = self.df['movie_id'].astype(int)
            self.df['rating'] = self.df['rating'].astype(float)
            self.df['title'] = self.df['title'].astype(str)
            logging.info("Successfully loaded %d movies from CSV.", len(self.df))
        except Exception as e:
            logging.error("Failed to load CSV: %s. Loading memory fallback.", str(e))
            self._load_fallback_dataframe()

        # Extract unique genres dynamically
        all_genres = set()
        for genres_str in self.df['genres'].dropna():
            for g in genres_str.split(','):
                all_genres.add(g.strip())
        self.genres_list = ["All Genres"] + sorted(list(all_genres))

    def _write_default_csv(self) -> None:
        """Writes fallback dataset to disk if files are missing."""
        default_data = """movie_id,title,genres,keywords,overview,director,cast,rating
1,Inception,"Action,Adventure,Sci-Fi","dream,thief,subconscious,heist","A thief who steals corporate secrets through dream-sharing is tasked with planting an idea in a target's mind.","Christopher Nolan","Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page",8.8
2,Interstellar,"Adventure,Drama,Sci-Fi","space,wormhole,black hole,astronaut","A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.","Christopher Nolan","Matthew McConaughey, Anne Hathaway, Jessica Chastain",8.6
3,The Dark Knight,"Action,Crime,Drama","batman,joker,superhero,vigilante","When the menace known as the Joker wreaks havoc, Batman must accept one of the greatest tests of his ability.","Christopher Nolan","Christian Bale, Heath Ledger, Aaron Eckhart",9.0
4,The Matrix,"Action,Sci-Fi","virtual reality,simulation,hacker,rebellion","A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war.","Lana Wachowski, Lilly Wachowski","Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",8.7
5,Avatar,"Action,Adventure,Sci-Fi","alien,planet,colonization,marine","A paraplegic Marine dispatched to Pandora becomes torn between following orders and protecting this world.","James Cameron","Sam Worthington, Zoe Saldana, Sigourney Weaver",7.9
6,The Godfather,"Crime,Drama","mafia,family,crime syndicate,revenge","The aging patriarch of an organized crime dynasty transfers control of his empire to his reluctant son.","Francis Ford Coppola","Marlon Brando, Al Pacino, James Caan",9.2
7,Pulp Fiction,"Crime,Drama","hitman,boxer,heist,mobster","The lives of two mob hitmen, a boxer, a gangster, and his wife intertwine in tales of violence and redemption.","Quentin Tarantino","John Travolta, Uma Thurman, Samuel L. Jackson",8.9
8,Fight Club,"Drama,Thriller","insomnia,split personality,fight club,rebellion","An insomniac office worker and a soapmaker form an underground fight club that evolves into something more.","David Fincher","Brad Pitt, Edward Norton, Helena Bonham Carter",8.8
9,Forrest Gump,"Drama,Romance,Comedy","history,love,marathon,vietnam war","The presidency of JFK, Vietnam war, and other events unfold from the perspective of an Alabama man with an IQ of 75.","Robert Zemeckis","Tom Hanks, Robin Wright, Gary Sinise",8.8
10,The Shawshank Redemption,"Drama","prison,escape,friendship,redemption","Two imprisoned men bond over a number of years, finding solace and eventual redemption through common decency.","Frank Darabont","Tim Robbins, Morgan Freeman, Bob Gunton",9.3
11,The Lord of the Rings: The Fellowship of the Ring,"Adventure,Fantasy,Drama","ring,wizard,hobbit,middle earth","A meek Hobbit and eight companions set out on a journey to destroy the One Ring and save Middle-earth.","Peter Jackson","Elijah Wood, Ian McKellen, Orlando Bloom",8.8
12,Titanic,"Drama,Romance","shipwreck,iceberg,love story,historical","A seventeen-year-old aristocrat falls in love with a poor artist aboard the luxurious, ill-fated Titanic.","James Cameron","Leonardo DiCaprio, Kate Winslet, Billy Zane",7.9
13,Gladiator,"Action,Adventure,Drama","rome,gladiator,revenge,emperor","A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family.","Ridley Scott","Russell Crowe, Joaquin Phoenix, Connie Nielsen",8.5
14,Back to the Future,"Adventure,Comedy,Sci-Fi","time travel,delorean,1950s,inventor","A high school student is accidentally sent thirty years into the past in a time-traveling DeLorean.","Robert Zemeckis","Michael J. Fox, Christopher Lloyd, Lea Thompson",8.5
15,The Lion King,"Animation,Adventure,Drama","lion,king,uncle,africa","A young lion prince flees his kingdom after his father is murdered, only to learn the true meaning of responsibility.","Roger Allers, Rob Minkoff","Matthew Broderick, Jeremy Irons, James Earl Jones",8.5
16,Spirited Away,"Animation,Adventure,Fantasy","spirit,bathhouse,witch,dragon","A young girl wanders into a world ruled by gods, witches, and spirits where humans are changed into beasts.","Hayao Miyazaki","Rumi Hiiragi, Miyu Irino, Mari Natsuki",8.6
17,The Silence of the Lambs,"Crime,Drama,Thriller","serial killer,fbi,cannibal,psychological","A young F.B.I. cadet receives help from an incarcerated cannibal killer to catch another active serial killer.","Jonathan Demme","Jodie Foster, Anthony Hopkins, Scott Glenn",8.6
18,Jurassic Park,"Action,Adventure,Sci-Fi","dinosaurs,theme park,island,genetic","An island theme park populated by cloned dinosaurs suffers a power failure, letting the creatures run loose.","Steven Spielberg","Sam Neill, Laura Dern, Jeff Goldblum",8.2
19,Se7en,"Crime,Drama,Mystery","serial killer,detective,seven deadly sins","Two detectives hunt a serial killer who uses the seven deadly sins as his motives for gruesome murders.","David Fincher","Morgan Freeman, Brad Pitt, Kevin Spacey",8.6
20,The Prestige,"Drama,Mystery,Sci-Fi","magician,rivalry,obsession,illusion","After a tragic accident, two stage magicians engage in a battle to create the ultimate illusion.","Christopher Nolan","Hugh Jackman, Christian Bale, Scarlett Johansson",8.5
21,Django Unchained,"Drama,Western","slavery,bounty hunter,revenge,south","With the help of a German bounty hunter, a freed slave sets out to rescue his wife from a brutal plantation owner.","Quentin Tarantino","Jamie Foxx, Christoph Waltz, Leonardo DiCaprio",8.4
22,Whiplash,"Drama,Music","drummer,teacher,obsession,jazz","A promising young drummer enrolls at a cut-throat music conservatory where his dreams are mentored by an abusive teacher.","Damien Chazelle","Miles Teller, J.K. Simmons, Paul Reiser",8.5
23,La La Land,"Comedy,Drama,Music","musical,jazz,romance,hollywood","While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their dreams.","Damien Chazelle","Ryan Gosling, Emma Stone, John Legend",8.0
24,Parasite,"Drama,Thriller,Comedy","class conflict,family,deception,korea","Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.","Bong Joon Ho","Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong",8.6
25,Spider-Man: Into the Spider-Verse,"Animation,Action,Adventure","superhero,spider-man,multiverse,coming-of-age","Teen Miles Morales becomes the new Spider-Man of his universe, and must join with other Spider-heroes to stop a threat.","Bob Persichetti, Peter Ramsey","Shameik Moore, Jake Johnson, Hailee Steinfeld",8.4
26,The Departed,"Crime,Drama,Thriller","undercover,boston,mob,informant","An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in Boston.","Martin Scorsese","Leonardo DiCaprio, Matt Damon, Jack Nicholson",8.5
27,Goodfellas,"Biography,Crime,Drama","mafia,mobster,heist,true story","The story of Henry Hill and his life in the mob, covering his relationship with his wife and his partners.","Martin Scorsese","Robert De Niro, Ray Liotta, Joe Pesci",8.7
28,Avengers: Infinity War,"Action,Adventure,Sci-Fi","superhero,marvel,space,thanos","The Avengers and their allies must be willing to sacrifice all in an attempt to defeat the powerful Thanos.","Anthony Russo, Joe Russo","Robert Downey Jr., Chris Hemsworth, Mark Ruffalo",8.4
29,The Matrix Reloaded,"Action,Sci-Fi","virtual reality,simulation,hacker,sequel","Neo, Morpheus, and Trinity lead the fight against the machine army as Zion is threatened with destruction.","Lana Wachowski, Lilly Wachowski","Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",7.2
30,Shutter Island,"Mystery,Thriller","island,asylum,detective,psychological","In 1954, a U.S. Marshal investigates the disappearance of a murderer who escaped from a hospital for the criminally insane.","Martin Scorsese","Leonardo DiCaprio, Mark Ruffalo, Ben Kingsley",8.2
31,Eternal Sunshine of the Spotless Mind,"Drama,Romance,Sci-Fi","memory erasure,heartbreak,love,surreal","When their relationship turns sour, a couple undergoes a medical procedure to have each other erased from their memories.","Michel Gondry","Jim Carrey, Kate Winslet, Kirsten Dunst",8.3
32,WALL-E,"Animation,Adventure,Family","robot,space,earth,future","In the distant future, a small waste-collecting robot inadvertently embarks on a space journey that will decide the fate of mankind.","Andrew Stanton","Ben Burtt, Elissa Knight, Jeff Garlin",8.4
33,Ratatouille,"Animation,Adventure,Comedy","chef,rat,paris,cooking","A rat who can cook makes an unusual alliance with a young kitchen worker at a famous Paris restaurant.","Brad Bird, Jan Pinkava","Patton Oswalt, Ian Holm, Lou Romano",8.1
34,No Country for Old Men,"Crime,Drama,Thriller","drug money,hitman,sheriff,texas","Violence and mayhem ensue after a hunter stumbles upon a drug deal gone wrong and more than two million dollars in cash.","Ethan Coen, Joel Coen","Tommy Lee Jones, Javier Bardem, Josh Brolin",8.2
35,The Terminator,"Action,Sci-Fi","cyborg,future,time travel,assassin","A human soldier is sent from 2029 to 1984 to protect a woman whose unborn son will lead humanity in a war against machines.","James Cameron","Arnold Schwarzenegger, Linda Hamilton, Michael Biehn",8.0
36,Terminator 2: Judgment Day,"Action,Sci-Fi","cyborg,future,time travel,protector","A cyborg, identical to the one who failed to kill Sarah Connor, must now protect her ten-year-old son from a more advanced cyborg.","James Cameron","Arnold Schwarzenegger, Linda Hamilton, Edward Furlong",8.6
37,The Sixth Sense,"Drama,Mystery,Thriller","ghost,child,psychologist,twist","A psychological thriller about a young boy who communicates with spirits and the dispirited child psychologist who tries to help him.","M. Night Shyamalan","Bruce Willis, Haley Joel Osment, Toni Collette",8.1
38,The Usual Suspects,"Crime,Mystery,Thriller","lineup,heist,customs,verbal","A sole survivor tells of the twisty events leading up to a horrific gun battle on a boat, which began when five criminals met at a lineup.","Bryan Singer","Kevin Spacey, Gabriel Byrne, Chazz Palminteri",8.5
39,Toy Story,"Animation,Adventure,Comedy","toys,friendship,childhood,rivalry","A cowboy doll is profoundly threatened and jealous when a new spaceman action figure supplants him as top toy in a boy's room.","John Lasseter","Tom Hanks, Tim Allen, Don Rickles",8.3
40,Memento,"Mystery,Thriller","short-term memory,revenge,investigation,nonlinear","A man with short-term memory loss attempts to track down his wife's murderer using notes, photos, and tattoos.","Christopher Nolan","Guy Pearce, Carrie-Anne Moss, Joe Pantoliano",8.4"""
        try:
            with open(CSV_PATH, "w", encoding="utf-8") as f:
                f.write(default_data.strip())
            logging.info("Default dataset/movies.csv generated successfully.")
        except Exception as e:
            logging.error("Failed to write default CSV: %s", str(e))

    def _load_fallback_dataframe(self) -> None:
        """Loads a small hardcoded pandas dataframe if disk load fails completely."""
        fallback_list = [
            {
                "movie_id": 1, "title": "Inception", "genres": "Action,Adventure,Sci-Fi",
                "keywords": "dream,thief,subconscious", "overview": "A thief steals secrets through dreams.",
                "director": "Christopher Nolan", "cast": "Leonardo DiCaprio", "rating": 8.8
            },
            {
                "movie_id": 2, "title": "Interstellar", "genres": "Adventure,Drama,Sci-Fi",
                "keywords": "space,wormhole,black hole", "overview": "A team travels through a space wormhole.",
                "director": "Christopher Nolan", "cast": "Matthew McConaughey", "rating": 8.6
            },
            {
                "movie_id": 3, "title": "The Dark Knight", "genres": "Action,Crime,Drama",
                "keywords": "batman,joker", "overview": "Batman battles the chaotic Joker.",
                "director": "Christopher Nolan", "cast": "Christian Bale", "rating": 9.0
            }
        ]
        self.df = pd.DataFrame(fallback_list)

    def _build_similarity_model(self) -> None:
        """Vectorizes textual attributes and calculates Cosine Similarity."""
        # Combine structural textual variables into a single tag representation
        def combine_row_features(row: pd.Series) -> str:
            genres = str(row.get('genres', '')).replace(',', ' ').lower()
            keywords = str(row.get('keywords', '')).replace(',', ' ').lower()
            overview = str(row.get('overview', '')).lower()
            
            # Remove whitespace inside director and actor names so they act as distinct tokens
            director = str(row.get('director', '')).replace(' ', '').replace(',', ' ').lower()
            cast = str(row.get('cast', '')).replace(' ', '').replace(',', ' ').lower()
            
            return f"{genres} {keywords} {overview} {director} {cast}"

        self.df['combined_features'] = self.df.apply(combine_row_features, axis=1)

        # Apply TF-IDF Vectorizer
        tfidf = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf.fit_transform(self.df['combined_features'])

        # Compute Similarity Matrix
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        logging.info("Cosine similarity matrix built successfully. Shape: %s", str(self.similarity_matrix.shape))

    def get_recommendations(
        self,
        movie_title: str,
        min_rating: float = 0.0,
        genre_filter: str = "All Genres",
        top_n: int = 5
    ) -> List[Tuple[pd.Series, float]]:
        """
        Computes the top N recommendations similar to the input movie.
        
        Args:
            movie_title: Name of the reference movie.
            min_rating: Minimum acceptable average rating threshold.
            genre_filter: Specific genre required.
            top_n: Number of recommendations to retrieve.
            
        Returns:
            A list of tuples, each containing a Pandas Series (movie metadata) and similarity score.
        """
        # Find index of the movie title
        matches = self.df[self.df['title'].str.lower() == movie_title.lower().strip()]
        if matches.empty:
            logging.warning("No movie title matches found for '%s'", movie_title)
            return []

        idx = matches.index[0]

        # Get similarities for this movie index
        sim_scores = list(enumerate(self.similarity_matrix[idx]))

        # Sort descending based on similarity
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        recommendations: List[Tuple[pd.Series, float]] = []

        for i, score in sim_scores:
            # Skip the query movie itself
            if i == idx:
                continue

            movie_row = self.df.iloc[i]

            # Filter by minimum rating
            if float(movie_row['rating']) < min_rating:
                continue

            # Filter by genre
            if genre_filter != "All Genres":
                genres_arr = [g.strip().lower() for g in str(movie_row['genres']).split(',')]
                if genre_filter.lower() not in genres_arr:
                    continue

            recommendations.append((movie_row, score))

            if len(recommendations) >= top_n:
                break

        return recommendations


class MovieRecommenderGUI:
    """Manages the layout, search entry, suggestion lists, and card renderings."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Movie Recommendation Dashboard")
        self.root.geometry("850x650")
        self.root.minsize(800, 580)

        # Initialize Recommendation Engine
        self.engine = RecommendationEngine()

        # Visual Theme Definition (Catppuccin Mocha style)
        self.colors = {
            "bg": "#181825",          # Deep base
            "card_bg": "#1e1e2e",     # Surface card
            "input_bg": "#313244",    # Entry boxes
            "text": "#cdd6f4",        # Warm white text
            "subtext": "#a6adc8",     # Muted grey
            "highlight": "#cba6f7",   # Lavender accent
            "star_color": "#f9e2af",  # Pastel yellow/gold
            "green": "#a6e3a1",       # Pastel green (match score)
            "btn_bg": "#89b4fa",      # Light Blue
            "btn_fg": "#11111b",
            "btn_hover": "#b4befe"
        }

        # Apply root styling
        self.root.configure(bg=self.colors["bg"])

        # Configure ttk style mapping (specifically for Combobox dropdowns)
        self._setup_ttk_styles()

        self._create_widgets()
        self._load_all_movies_to_search()

    def _setup_ttk_styles(self) -> None:
        """Sets up custom styles for TTK widgets."""
        self.style = ttk.Style()
        self.style.theme_use("default")
        
        # Style Comboboxes
        self.style.configure(
            "TCombobox",
            fieldbackground=self.colors["input_bg"],
            background=self.colors["bg"],
            foreground=self.colors["text"],
            bordercolor=self.colors["input_bg"],
            arrowcolor=self.colors["text"]
        )
        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", self.colors["input_bg"])],
            foreground=[("readonly", self.colors["text"])]
        )

    def _create_widgets(self) -> None:
        """Constructs the sidebar filter dashboard and main recommendation list."""
        # Main layout panels
        self.sidebar = tk.Frame(self.root, bg=self.colors["card_bg"], width=300, bd=0)
        self.sidebar.pack(fill=tk.Y, side=tk.LEFT)
        self.sidebar.pack_propagate(False)

        # Border separator line
        sep = tk.Frame(self.root, bg=self.colors["input_bg"], width=1)
        sep.pack(fill=tk.Y, side=tk.LEFT)

        self.main_panel = tk.Frame(self.root, bg=self.colors["bg"])
        self.main_panel.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)

        self._build_sidebar_contents()
        self._build_main_panel_contents()

    def _build_sidebar_contents(self) -> None:
        """Builds all inputs and filters in the sidebar."""
        # Logo or Title branding
        logo_lbl = tk.Label(
            self.sidebar,
            text="🎬 MOVIE REC AI",
            font=("Helvetica", 14, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["highlight"]
        )
        logo_lbl.pack(anchor=tk.W, padx=20, pady=(25, 5))

        subtitle_lbl = tk.Label(
            self.sidebar,
            text="Content-Based Recommendation Engine",
            font=("Helvetica", 8),
            bg=self.colors["card_bg"],
            fg=self.colors["subtext"]
        )
        subtitle_lbl.pack(anchor=tk.W, padx=20, pady=(0, 20))

        # --- Search Box Header ---
        search_lbl = tk.Label(
            self.sidebar,
            text="Search Movie Title:",
            font=("Helvetica", 10, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["text"]
        )
        search_lbl.pack(anchor=tk.W, padx=20, pady=(10, 4))

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            self.sidebar,
            textvariable=self.search_var,
            font=("Helvetica", 10),
            bg=self.colors["input_bg"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            bd=0,
            highlightthickness=1,
            highlightbackground=self.colors["input_bg"],
            highlightcolor=self.colors["highlight"]
        )
        self.search_entry.pack(fill=tk.X, padx=20, ipady=6)
        self.search_entry.bind("<KeyRelease>", self._on_search_keyrelease)

        # Dynamic search recommendations dropdown Box
        self.suggestion_listbox = tk.Listbox(
            self.sidebar,
            bg=self.colors["input_bg"],
            fg=self.colors["text"],
            selectbackground=self.colors["highlight"],
            selectforeground=self.colors["card_bg"],
            bd=0,
            highlightthickness=0,
            height=5,
            font=("Helvetica", 9)
        )
        self.suggestion_listbox.pack(fill=tk.X, padx=20, pady=(2, 10))
        self.suggestion_listbox.bind("<<ListboxSelect>>", self._on_suggestion_select)

        # --- Filter Panel ---
        filters_title = tk.Label(
            self.sidebar,
            text="Filters & Hyperparameters",
            font=("Helvetica", 10, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["text"]
        )
        filters_title.pack(anchor=tk.W, padx=20, pady=(15, 8))

        # Genre combo filter
        genre_lbl = tk.Label(
            self.sidebar,
            text="Select Genre:",
            font=("Helvetica", 9),
            bg=self.colors["card_bg"],
            fg=self.colors["subtext"]
        )
        genre_lbl.pack(anchor=tk.W, padx=20, pady=(4, 2))

        self.genre_combo = ttk.Combobox(
            self.sidebar,
            values=self.engine.genres_list,
            state="readonly",
            font=("Helvetica", 9)
        )
        self.genre_combo.set("All Genres")
        self.genre_combo.pack(fill=tk.X, padx=20, pady=(0, 15))

        # Rating scale filter
        rating_lbl = tk.Label(
            self.sidebar,
            text="Minimum Rating:",
            font=("Helvetica", 9),
            bg=self.colors["card_bg"],
            fg=self.colors["subtext"]
        )
        rating_lbl.pack(anchor=tk.W, padx=20, pady=(4, 2))

        self.rating_scale = tk.Scale(
            self.sidebar,
            from_=0.0,
            to=10.0,
            resolution=0.1,
            orient=tk.HORIZONTAL,
            bg=self.colors["card_bg"],
            fg=self.colors["text"],
            activebackground=self.colors["highlight"],
            troughcolor=self.colors["input_bg"],
            highlightthickness=0,
            bd=0,
            font=("Helvetica", 9)
        )
        self.rating_scale.set(0.0)
        self.rating_scale.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Recommendation limit count spinner
        count_lbl = tk.Label(
            self.sidebar,
            text="Number of Suggestions:",
            font=("Helvetica", 9),
            bg=self.colors["card_bg"],
            fg=self.colors["subtext"]
        )
        count_lbl.pack(anchor=tk.W, padx=20, pady=(4, 2))

        self.count_spin = tk.Spinbox(
            self.sidebar,
            from_=3,
            to=15,
            increment=1,
            bg=self.colors["input_bg"],
            fg=self.colors["text"],
            bd=0,
            buttonbackground=self.colors["card_bg"],
            highlightthickness=0,
            font=("Helvetica", 9, "bold"),
            width=5
        )
        self.count_spin.pack(anchor=tk.W, padx=20, pady=(0, 25))

        # CTA Button
        self.recommend_btn = tk.Button(
            self.sidebar,
            text="Get Recommendations",
            font=("Helvetica", 10, "bold"),
            bg=self.colors["btn_bg"],
            fg=self.colors["btn_fg"],
            activebackground=self.colors["btn_hover"],
            activeforeground=self.colors["btn_fg"],
            bd=0,
            cursor="hand2",
            padx=10,
            pady=10,
            command=self.execute_recommendations
        )
        self.recommend_btn.pack(fill=tk.X, padx=20, side=tk.BOTTOM, pady=30)
        self.recommend_btn.bind("<Enter>", lambda e: self.recommend_btn.configure(bg=self.colors["btn_hover"]))
        self.recommend_btn.bind("<Leave>", lambda e: self.recommend_btn.configure(bg=self.colors["btn_bg"]))

    def _build_main_panel_contents(self) -> None:
        """Builds the display list for results."""
        # Top banner showing selected item details
        self.info_frame = tk.Frame(self.main_panel, bg=self.colors["card_bg"], padx=20, pady=15)
        self.info_frame.pack(fill=tk.X, side=tk.TOP, padx=20, pady=(20, 10))

        self.selected_title_lbl = tk.Label(
            self.info_frame,
            text="Search and select a movie to begin",
            font=("Helvetica", 12, "bold"),
            bg=self.colors["card_bg"],
            fg=self.colors["highlight"]
        )
        self.selected_title_lbl.pack(anchor=tk.W)

        self.selected_details_lbl = tk.Label(
            self.info_frame,
            text="",
            font=("Helvetica", 9, "italic"),
            bg=self.colors["card_bg"],
            fg=self.colors["subtext"],
            justify=tk.LEFT
        )
        self.selected_details_lbl.pack(anchor=tk.W, pady=2)

        self.selected_overview_lbl = tk.Label(
            self.info_frame,
            text="Our system generates similarity matrices based on director, actors, plot keywords, and genres to compute optimal recommendations.",
            font=("Helvetica", 9),
            bg=self.colors["card_bg"],
            fg=self.colors["text"],
            wraplength=480,
            justify=tk.LEFT
        )
        self.selected_overview_lbl.pack(anchor=tk.W, pady=(5, 0))

        # --- Recommendation List Header ---
        list_header = tk.Label(
            self.main_panel,
            text="Recommended Similar Movies",
            font=("Helvetica", 11, "bold"),
            bg=self.colors["bg"],
            fg=self.colors["text"]
        )
        list_header.pack(anchor=tk.W, padx=20, pady=(10, 5))

        # --- Scrollable Container Canvas ---
        self.scroll_container = tk.Frame(self.main_panel, bg=self.colors["bg"])
        self.scroll_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))

        self.canvas = tk.Canvas(self.scroll_container, bg=self.colors["bg"], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.scroll_container, orient=tk.VERTICAL, command=self.canvas.yview)
        
        self.scroll_frame = tk.Frame(self.canvas, bg=self.colors["bg"])
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
        self.scrollbar.pack(fill=tk.Y, side=tk.RIGHT)

        # Mousewheel scroll binding on hover
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)

    def _bind_mousewheel(self, event: Any) -> None:
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(-int(e.delta/120), "units"))
        self.canvas.bind_all("<Button-4>", lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda e: self.canvas.yview_scroll(1, "units"))

    def _unbind_mousewheel(self, event: Any) -> None:
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _load_all_movies_to_search(self) -> None:
        """Pulls list of movies from engine and puts them on search suggestion lists."""
        self.all_titles = self.engine.df['title'].tolist()
        self._update_suggestions("")

    def _update_suggestions(self, pattern: str) -> None:
        """Updates autocomplete items matching input characters."""
        self.suggestion_listbox.delete(0, tk.END)
        
        if pattern == "":
            filtered = self.all_titles[:15] # default suggestion items
        else:
            pattern_lower = pattern.lower()
            filtered = [t for t in self.all_titles if pattern_lower in t.lower()]

        for title in filtered:
            self.suggestion_listbox.insert(tk.END, title)

    def _on_search_keyrelease(self, event: Any) -> None:
        """Triggers updates on suggestions as user inputs titles."""
        pattern = self.search_var.get()
        self._update_suggestions(pattern)

    def _on_suggestion_select(self, event: Any) -> None:
        """Populates entry box and selected details when suggestion is clicked."""
        widget = event.widget
        indices = widget.curselection()
        if not indices:
            return
            
        selected_title = widget.get(indices[0])
        self.search_var.set(selected_title)
        
        # Populate selected movie header details
        matches = self.engine.df[self.engine.df['title'] == selected_title]
        if not matches.empty:
            row = matches.iloc[0]
            self.selected_title_lbl.configure(text=f"{row['title']}")
            
            detail_str = f"⭐ {row['rating']}  |  🎬 {row['genres']}  |  👤 Dir: {row['director']}"
            self.selected_details_lbl.configure(text=detail_str)
            
            self.selected_overview_lbl.configure(text=f"{row['overview']}", wraplength=480)
            logging.info("Selected movie updated to: %s", selected_title)

    def execute_recommendations(self) -> None:
        """Reads selections, processes recommendations, and displays results."""
        movie_title = self.search_var.get().strip()
        if not movie_title:
            messagebox.showwarning("Input Required", "Please type or select a movie title to get recommendations.")
            return

        # Check if movie title exists in dataset
        if not any(t.lower() == movie_title.lower() for t in self.all_titles):
            messagebox.showerror("Error", f"Could not find movie '{movie_title}' in database. Please check your spelling.")
            return

        min_rating = float(self.rating_scale.get())
        selected_genre = self.genre_combo.get()
        
        try:
            top_n = int(self.count_spin.get())
        except ValueError:
            top_n = 5

        logging.info("Calculating recommendations for '%s' (Min Rating: %.1f, Genre: %s, Count: %d)", 
                     movie_title, min_rating, selected_genre, top_n)

        # Get recommendations
        recommendations = self.engine.get_recommendations(
            movie_title,
            min_rating=min_rating,
            genre_filter=selected_genre,
            top_n=top_n
        )

        # Clear previous cards in the scroll frame
        for child in self.scroll_frame.winfo_children():
            child.destroy()

        if not recommendations:
            no_rec_lbl = tk.Label(
                self.scroll_frame,
                text="No matching recommendations found.\nTry lowering the rating scale filter or changing the genre constraint.",
                font=("Helvetica", 10, "italic"),
                bg=self.colors["bg"],
                fg=self.colors["subtext"],
                pady=40
            )
            no_rec_lbl.pack(fill=tk.BOTH, expand=True)
            return

        # Render new recommended cards
        for i, (row, score) in enumerate(recommendations):
            match_pct = int(score * 100)
            
            # Movie Card Frame
            card = tk.Frame(self.scroll_frame, bg=self.colors["card_bg"], padx=15, pady=12)
            card.pack(fill=tk.X, pady=6, ipady=4)
            card.pack_propagate(True)

            # Top Card Line: Title & Match Percentage
            header = tk.Frame(card, bg=self.colors["card_bg"])
            header.pack(fill=tk.X)

            title_lbl = tk.Label(
                header,
                text=f"{i+1}. {row['title']}",
                font=("Helvetica", 11, "bold"),
                bg=self.colors["card_bg"],
                fg=self.colors["highlight"]
            )
            title_lbl.pack(side=tk.LEFT)

            match_lbl = tk.Label(
                header,
                text=f"{match_pct}% Match",
                font=("Helvetica", 9, "bold"),
                bg=self.colors["card_bg"],
                fg=self.colors["green"]
            )
            match_lbl.pack(side=tk.RIGHT)

            # Middle Card Line: Rating and structural attributes
            attributes = tk.Frame(card, bg=self.colors["card_bg"])
            attributes.pack(fill=tk.X, pady=(2, 4))

            rating_lbl = tk.Label(
                attributes,
                text=f"⭐ {row['rating']}",
                font=("Helvetica", 9, "bold"),
                bg=self.colors["card_bg"],
                fg=self.colors["star_color"]
            )
            rating_lbl.pack(side=tk.LEFT, padx=(0, 10))

            genre_lbl = tk.Label(
                attributes,
                text=f"Genres: {row['genres']}",
                font=("Helvetica", 9, "italic"),
                bg=self.colors["card_bg"],
                fg=self.colors["subtext"]
            )
            genre_lbl.pack(side=tk.LEFT)

            director_lbl = tk.Label(
                attributes,
                text=f"Dir: {row['director']}",
                font=("Helvetica", 9),
                bg=self.colors["card_bg"],
                fg=self.colors["subtext"]
            )
            director_lbl.pack(side=tk.RIGHT)

            # Bottom Card Line: Overview
            overview_lbl = tk.Label(
                card,
                text=row['overview'],
                font=("Helvetica", 9),
                bg=self.colors["card_bg"],
                fg=self.colors["text"],
                wraplength=480,
                justify=tk.LEFT
            )
            overview_lbl.pack(anchor=tk.W, pady=(4, 0))

        # Reset scroll positioning to top
        self.canvas.yview_moveto(0)


def main() -> None:
    """Application entry point."""
    try:
        root = tk.Tk()
        app = MovieRecommenderGUI(root)
        root.mainloop()
    except Exception as e:
        logging.critical("Failed to launch Movie Recommender app: %s", str(e))
        messagebox.showerror("Fatal Error", f"Failed to start Movie Recommender:\n{str(e)}")


if __name__ == "__main__":
    main()
