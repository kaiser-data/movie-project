# movie_app.py

from istorage import IStorage
import random
from termcolor import cprint
import re
import matplotlib.pyplot as plt
import numpy as np

class MovieApp:
    def __init__(self, storage: IStorage):
        """
        Initializes the MovieApp instance with a storage object.
        """
        self._storage = storage

    # -------------------------------------------------------------
    # 1. Utility Functions

    def _list_movies(self):
        """
        Lists all movies in the database.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("\nNo movies found.")
            return

        total_movies = len(movies)
        print(f"\n{total_movies} movies in total\n")
        for title, info in movies.items():
            print(f"{title} ({info['year']}): {info['rating']}")

    def _add_movie(self):
        """
        Adds a new movie to the database.
        """
        title = input("\nEnter new movie name: ").strip()
        try:
            self._validate_movie_name(title)
            year = int(input("Enter year: "))
            self._validate_year(year)
            rating = float(input("Enter rating (0-10): "))
            self._validate_rating(rating)
            poster = input("Enter poster URL: ").strip()

            self._storage.add_movie(title, year, rating, poster)
            cprint(f'\nMovie "{title}" successfully added.', "green")
        except ValueError as e:
            cprint(e, "red")

    def _delete_movie(self):
        """
        Deletes a movie from the database.
        """
        title = input("\nEnter movie name to delete: ").strip()
        try:
            self._storage.delete_movie(title)
            cprint(f'\nMovie "{title}" successfully deleted.', "green")
        except KeyError:
            cprint(f'\nMovie "{title}" does not exist!', "red")

    def _update_movie_rating(self):
        """
        Updates the rating of an existing movie.
        """
        title = input("\nEnter movie name to update: ").strip()
        movies = self._storage.list_movies()
        if title in movies:
            try:
                rating = float(input("Enter new rating (0-10): "))
                self._validate_rating(rating)
                self._storage.update_movie(title, rating)
                cprint(f'\nMovie "{title}" successfully updated.', "green")
            except ValueError as e:
                cprint(e, "red")
        else:
            cprint(f'\nMovie "{title}" does not exist!', "red")

    def _stats_movies(self):
        """
        Displays statistics about the movies in the database.
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

    def _random_movie(self):
        """
        Selects a random movie from the database.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("\nNo movies found.")
            return

        title, info = random.choice(list(movies.items()))
        print(f"\nYour random movie: {title} ({info['year']}), Rating: {info['rating']}")

    def _search_movies(self):
        """
        Searches for movies by partial name.
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

    def _sort_by_rating(self):
        """
        Sorts movies by rating in descending order.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("\nNo movies found.")
            return

        sorted_movies = sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True)
        print("\nMovies Sorted by Rating:")
        for title, info in sorted_movies:
            print(f"{title} ({info['year']}): {info['rating']}")

    def _sort_by_year(self):
        """
        Sorts movies by year in ascending or descending order.
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

    def _filter_movies(self):
        """
        Filters movies based on minimum rating and year range.
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

    def _create_histogram(self):
        """
        Creates a histogram of movie ratings and saves it as a PNG file.
        """


        movies = self._storage.list_movies()
        if not movies:
            cprint("\nNo movies available to create a histogram.", "red")
            return

        ratings = [info["rating"] for info in movies.values()]

        fig, ax = plt.subplots()
        ax.hist(
            ratings,
            bins=np.arange(0, 11, 1),
            color="gold",
            edgecolor="black",
            alpha=0.7,
            rwidth=0.8
        )
        ax.set_title("Rating Histogram for Movies", fontsize=18, fontweight="bold")
        ax.set_xlabel("Rating (0-10)", fontweight="bold")
        ax.set_ylabel("Number of Movies", fontweight="bold")
        ax.set_xticks(np.arange(0, 11, 1))

        file_name = "Rating_Histogram_Movies.png"
        fig.savefig(file_name)
        cprint(f"\nHistogram was successfully saved as '{file_name}'.", "green")

    # -------------------------------------------------------------
    # 2. Validation Functions

    def _validate_movie_name(self, name: str):
        """
        Validates the movie name.
        """
        if not name.strip():
            raise ValueError("Movie name must not be empty!")
        if not re.match(r"^[a-zA-Z0-9\s\-',.!?]+$", name):
            raise ValueError("Movie name contains invalid characters!")
        if name in self._storage.list_movies():
            raise ValueError(f"Movie '{name}' already exists!")

    def _validate_year(self, year: int):
        """
        Validates the movie year.
        """
        min_year = 1887
        current_year = datetime.now().year
        if not (min_year <= year <= current_year):
            raise ValueError(f"Year must be between {min_year} and {current_year}.")

    def _validate_rating(self, rating: float):
        """
        Validates the movie rating.
        """
        if not (0 <= rating <= 10):
            raise ValueError("Rating must be between 0 and 10.")

    # -------------------------------------------------------------
    # 3. Menu Logic

    def run(self):
        """
        Runs the movie application.
        """
        while True:
            print("\nMenu:")
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
            print("0. Exit")

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
            else:
                cprint("\nInvalid choice. Please try again.", "red")

            input("\nPress Enter to continue...")