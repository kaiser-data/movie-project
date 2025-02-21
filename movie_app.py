# movie_app.py
"""
Movie App module that provides functionality to manage a movie database.
This application allows users to add, delete, search and analyze movies
through a command-line interface, with data fetched from the OMDb API.
"""

from typing import Dict, List, Optional, Tuple, Any, Union
from datetime import datetime
import random
import os
import requests
from termcolor import cprint
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import numpy as np
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from isstorage import IStorage


class MovieApp:
    """
    A command-line application for managing a movie database.

    This class provides functionality to list, add, delete, search, and analyze
    movies. It also includes features for generating visualizations and a website
    based on the movie database.

    Attributes:
        _storage (IStorage): A storage interface for persisting movie data.
        omdb_api_key (str): API key for accessing the OMDb API.
    """

    def __init__(self, storage: IStorage) -> None:
        """
        Initialize the MovieApp with a storage backend.

        Args:
            storage (IStorage): A storage implementation that adheres to the IStorage interface
                                for persisting movie data.
        """
        self._storage = storage
        # Load the OMDb API key from the .env file
        load_dotenv()
        self.omdb_api_key = os.getenv("OMDB_API_KEY")

    # -------------------------------------------------------------
    # 1. Utility Functions

    def _list_movies(self) -> None:
        """
        Display all movies in the database with their release year and rating.

        If no movies are found, a message is displayed to inform the user.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("\nNo movies found.")
            return

        total_movies = len(movies)
        print(f"\n{total_movies} movies in total\n")
        for title, info in movies.items():
            print(f"{title} ({info['year']}): {info['rating']}")

    def _add_movie(self) -> None:
        """
        Add a new movie to the database by fetching data from the OMDb API.

        Prompts the user for a movie title, then retrieves the movie details
        using the OMDb API. If successful, adds the movie to the database.

        Exceptions:
            ValueError: If the movie data cannot be retrieved or processed.
        """
        title = input("\nEnter the movie title: ").strip()
        try:
            movie_data = self._fetch_movie_data(title)
            if movie_data:
                self._storage.add_movie(
                    movie_data["title"],
                    movie_data["year"],
                    movie_data["rating"],
                    movie_data["poster"]
                )
                cprint(f'\nMovie "{movie_data["title"]}" successfully added.', "green")
        except ValueError as e:
            cprint(str(e), "red")

    def _delete_movie(self) -> None:
        """
        Delete a movie from the database.

        Prompts the user for a movie title and removes it from the database if it exists.

        Exceptions:
            KeyError: If the movie does not exist in the database.
        """
        title = input("\nEnter movie name to delete: ").strip()
        try:
            self._storage.delete_movie(title)
            cprint(f'\nMovie "{title}" successfully deleted.', "green")
        except KeyError:
            cprint(f'\nMovie "{title}" does not exist!', "red")

    def _update_movie_rating(self) -> None:
        """
        Display a message indicating that updating movie ratings is disabled.

        Since movie data comes from the OMDb API, manual rating updates are not supported.
        """
        cprint("\nUpdating movie rating is disabled since data comes from the OMDb API.", "yellow")

    def _stats_movies(self) -> None:
        """
        Display statistical information about the movies in the database.

        Calculates and displays:
            - Average rating
            - Median rating
            - Best movie (highest rating)
            - Worst movie (lowest rating)

        If no movies are found, a message is displayed to inform the user.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("\nNo movies found.")
            return

        ratings = [info["rating"] for info in movies.values()]
        average_rating = sum(ratings) / len(ratings)
        median_rating = sorted(ratings)[len(ratings) // 2]
        best_movie = max(movies.items(), key=lambda x: x[1]["rating"])
        worst_movie = min(movies.items(), key=lambda x: x[1]["rating"])

        print(f"\nAverage Rating: {average_rating:.1f}")
        print(f"Median Rating: {median_rating:.1f}")
        print(f"Best Movie: {best_movie[0]} ({best_movie[1]['rating']:.1f})")
        print(f"Worst Movie: {worst_movie[0]} ({worst_movie[1]['rating']:.1f})")

    def _random_movie(self) -> None:
        """
        Select and display a random movie from the database.

        If no movies are found, a message is displayed to inform the user.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("\nNo movies found.")
            return

        title, info = random.choice(list(movies.items()))
        print(f"\nYour random movie: {title} ({info['year']}), Rating: {info['rating']}")

    def _search_movies(self) -> None:
        """
        Search for movies by partial name match.

        Prompts the user for a search term and displays all movies whose titles
        contain the search term (case-insensitive).
        """
        search_term = input("\nEnter part of the movie name: ").lower()
        movies = self._storage.list_movies()
        results = [
            f"{title} ({info['year']}): {info['rating']}"
            for title, info in movies.items()
            if search_term in title.lower()
        ]

        if results:
            print("\nSearch Results:")
            print("\n".join(results))
        else:
            print("\nNo matching movies found.")

    def _sort_by_rating(self) -> None:
        """
        Display all movies sorted by rating in descending order.

        If no movies are found, a message is displayed to inform the user.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("\nNo movies found.")
            return

        sorted_movies = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
        print("\nMovies Sorted by Rating:")
        for title, info in sorted_movies:
            print(f"{title} ({info['year']}): {info['rating']}")

    def _sort_by_year(self) -> None:
        """
        Display all movies sorted by release year.

        Prompts the user to choose between ascending or descending order.
        If no movies are found, a message is displayed to inform the user.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("\nNo movies found.")
            return

        order = input("\nSort by year (asc/desc): ").strip().lower()
        if order not in ["asc", "desc"]:
            print("\nInvalid sort order. Use 'asc' or 'desc'.")
            return

        sorted_movies = sorted(
            movies.items(),
            key=lambda x: x[1]["year"],
            reverse=(order == "desc")
        )
        print("\nMovies Sorted by Year:")
        for title, info in sorted_movies:
            print(f"{title} ({info['year']}): {info['rating']}")

    def _filter_movies(self) -> None:
        """
        Filter and display movies based on rating and year criteria.

        Prompts the user for:
            - Minimum rating threshold
            - Start year (inclusive)
            - End year (inclusive)

        Displays all movies that match the specified criteria.
        If no movies are found, a message is displayed to inform the user.

        Exceptions:
            ValueError: If the user enters non-numeric values for the filters.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("\nNo movies found.")
            return

        try:
            min_rating = float(input("Enter minimum rating (leave blank for no filter): ") or 0)
            start_year = int(input("Enter start year (leave blank for no filter): ") or 1887)
            end_year = int(input("Enter end year (leave blank for no filter): ") or datetime.now().year)

            filtered_movies = [
                f"{title} ({info['year']}): {info['rating']}"
                for title, info in movies.items()
                if info["rating"] >= min_rating and start_year <= info["year"] <= end_year
            ]

            if filtered_movies:
                print("\nFiltered Movies:")
                print("\n".join(filtered_movies))
            else:
                print("\nNo movies match the filter criteria.")
        except ValueError:
            cprint("\nInvalid input. Please enter valid numbers.", "red")

    def _fetch_movie_data(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Fetch movie data from the OMDb API.

        Args:
            title (str): The title of the movie to search for.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing movie details if found,
                                     None if the movie was not found or an error occurred.

        The returned dictionary contains the following keys:
            - title: The full movie title
            - year: The release year as an integer
            - rating: The IMDb rating as a float
            - poster: The URL to the movie poster image

        Raises:
            ValueError: If the API key is missing or the API returns an error.
        """
        if not self.omdb_api_key:
            raise ValueError("Error: OMDb API key not found. Please set it in the .env file.")

        try:
            url = f"http://www.omdbapi.com/?t={title}&apikey={self.omdb_api_key}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data.get("Response") == "False":
                cprint(f"Error: {data.get('Error', 'Movie not found')}", "red")
                return None

            movie_details = {
                "title": data.get("Title"),
                "year": int(data.get("Year", "0").split("–")[0].strip()),
                "rating": float(data.get("imdbRating", "0.0")),
                "poster": data.get("Poster", "")
            }
            return movie_details

        except requests.exceptions.RequestException as e:
            cprint(f"Error: Unable to connect to the OMDb API. Details: {e}", "red")
            return None

    def _create_histogram(self) -> None:
        """
        Create and save a histogram visualization of movie ratings.

        Generates a histogram of movie ratings using matplotlib and saves it as a PNG file.
        The histogram uses custom styling for better visual appeal.

        If no movies are found, a message is displayed to inform the user.
        """
        movies = self._storage.list_movies()
        if not movies:
            cprint("No movies available to create a histogram.", "red")
            return

        # Extract ratings
        ratings = [info["rating"] for info in movies.values()]

        # Create figure and axis with subplots
        fig, ax = plt.subplots()

        # Plotting and styling histogram
        ax.hist(
            ratings,
            bins=np.linspace(0, 10, 21),
            color="gold",
            edgecolor="black",
            hatch="//",
            rwidth=0.8,
            alpha=0.7
        )

        # Set title
        ax.set_title("Rating Histogram for Movies", fontsize=18, fontweight="bold")

        # Naming of x-axis and y-axis
        ax.set_xlabel("Rating (0-10)", fontweight="bold")
        ax.set_ylabel("Number of Movies", fontweight="bold")

        # Setting x-ticks
        ax.set_xticks(np.linspace(0, 10, 11))

        # Setting minor ticks
        minor_locator = AutoMinorLocator(2)  # 2 minor ticks per major tick
        ax.xaxis.set_minor_locator(minor_locator)

        # Grid for y-axis
        ax.grid(axis="y", alpha=0.75)

        # Define face color of graph
        fig.patch.set_facecolor("honeydew")

        # Save figure
        file_name = "Rating_Histogram_Movies.png"
        fig.savefig(file_name)
        cprint(f"\nHistogram was successfully saved as '{file_name}'.", "green")

    def _generate_website(self) -> None:
        """
        Generate an HTML website showcasing the movie database.

        Creates an HTML file with a responsive grid layout displaying all movies
        with their posters, titles, and release years. Uses Jinja2 templating
        to render the HTML from a template file.

        The template should be located in the '_static' directory with the name
        'index_template.html' and should contain placeholders for:
        - TEMPLATE_TITLE: Title of the webpage
        - TEMPLATE_MOVIE_GRID: HTML content for the movie grid

        If no movies are found, a message is displayed to inform the user.
        """
        # Get the list of movies from storage
        movies = self._storage.list_movies()
        if not movies:
            cprint("No movies available to generate a website.", "red")
            return

        # Prepare the movie grid HTML
        movie_grid_html = ""
        for title, info in movies.items():
            movie_card = f"""
                <div class="movie">
                    <img class="movie-poster" src="{info.get('poster', 'placeholder.jpg')}" alt="{title} poster">
                    <div class="movie-title">{title}</div>
                    <div class="movie-year">{info.get('year', 'Unknown')}</div>
                </div>
            """
            movie_grid_html += movie_card

        # Define the template environment
        env = Environment(loader=FileSystemLoader(searchpath="_static"))
        template = env.get_template("index_template.html")

        # Render the template with movie data
        rendered_html = template.render(
            TEMPLATE_TITLE="My Movie Database",  # Replace placeholder with actual title
            TEMPLATE_MOVIE_GRID=movie_grid_html  # Replace placeholder with movie grid
        )

        # Save the rendered HTML to a file
        output_file = "index.html"
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(rendered_html)

        cprint(f"Website was generated successfully as '{output_file}'.", "green")

    # -------------------------------------------------------------
    # 2. Menu Logic
    def run(self) -> None:
        """
        Run the movie application main loop.

        Displays a menu of options and processes user input until the user chooses to exit.
        Each menu option corresponds to a method that performs a specific operation.
        """
        while True:
            print("\nMenu:")
            print("0. Exit")
            print("1. List Movies")
            print("2. Add Movie")
            print("3. Delete Movie")
            print("4. Update Movie Rating")
            print("5. Stats")
            print("6. Random Movie")
            print("7. Search Movie")
            print("8. Sort by Rating")
            print("9. Sort by Year")
            print("10. Filter Movies")
            print("11. Create Rating Histogram")
            print("12. Generate Website")

            choice = input("\nEnter choice: ").strip()
            if choice == "0":
                print("\nGoodbye!")
                break
            elif choice == "1":
                self._list_movies()
            elif choice == "2":
                self._add_movie()
            elif choice == "3":
                self._delete_movie()
            elif choice == "4":
                self._update_movie_rating()
            elif choice == "5":
                self._stats_movies()
            elif choice == "6":
                self._random_movie()
            elif choice == "7":
                self._search_movies()
            elif choice == "8":
                self._sort_by_rating()
            elif choice == "9":
                self._sort_by_year()
            elif choice == "10":
                self._filter_movies()
            elif choice == "11":
                self._create_histogram()
            elif choice == "12":
                self._generate_website()
            else:
                cprint("\nInvalid choice. Please try again.", "red")

            input("\nPress Enter to continue...")