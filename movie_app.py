# movie_app.py

from istorage import IStorage

class MovieApp:
    """
    The MovieApp class handles the main logic of the movie application.
    It interacts with the storage layer (IStorage) to perform operations like listing movies,
    adding movies, deleting movies, etc.
    """

    def __init__(self, storage: IStorage):
        """
        Initializes the MovieApp instance with a storage object.

        Args:
            storage (IStorage): An instance of a class that implements the IStorage interface.
        """
        self._storage = storage

    def _command_list_movies(self):
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

    def _command_add_movie(self):
        """
        Adds a new movie to the database.
        """
        title = input("\nEnter new movie name: ").strip()
        try:
            self._storage.add_movie(title, int(input("Year: ")), float(input("Rating: ")), input("Poster URL: "))
            print(f"\nMovie '{title}' successfully added.")
        except ValueError as e:
            print(f"\nError: {e}")

    def _command_delete_movie(self):
        """
        Deletes a movie from the database.
        """
        title = input("\nEnter movie name to delete: ").strip()
        try:
            self._storage.delete_movie(title)
            print(f"\nMovie '{title}' successfully deleted.")
        except KeyError:
            print(f"\nError: Movie '{title}' does not exist.")

    def _command_update_movie(self):
        """
        Updates the rating of a movie in the database.
        """
        title = input("\nEnter movie name to update: ").strip()
        try:
            new_rating = float(input("Enter new rating: "))
            self._storage.update_movie(title, new_rating)
            print(f"\nMovie '{title}' successfully updated.")
        except ValueError as e:
            print(f"\nError: {e}")
        except KeyError:
            print(f"\nError: Movie '{title}' does not exist.")

    def _command_movie_stats(self):
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

    def _command_random_movie(self):
        """
        Selects a random movie from the database.
        """
        movies = self._storage.list_movies()
        if not movies:
            print("\nNo movies found.")
            return

        title, info = random.choice(list(movies.items()))
        print(f"\nYour random movie: {title} ({info['year']}), Rating: {info['rating']}")

    def _command_search_movie(self):
        """
        Searches for a movie by name.
        """
        search_term = input("\nEnter part of the movie name: ").lower()
        results = [
            f"{title} ({info['year']}): {info['rating']}"
            for title, info in self._storage.list_movies().items()
            if search_term in title.lower()
        ]

        if results:
            print("\nSearch Results:")
            print("\n".join(results))
        else:
            print("\nNo matching movies found.")

    def _command_sort_by_rating(self):
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

    def _command_sort_by_year(self):
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

    def run(self):
        """
        Runs the movie application.
        Displays the menu and processes user commands.
        """
        while True:
            print("\nMenu:")
            print("1. List Movies")
            print("2. Add Movie")
            print("3. Delete Movie")
            print("4. Update Movie")
            print("5. Movie Stats")
            print("6. Random Movie")
            print("7. Search Movie")
            print("8. Sort by Rating")
            print("9. Sort by Year")
            print("0. Exit")

            choice = input("\nEnter choice: ").strip()

            if choice == "1":
                self._command_list_movies()
            elif choice == "2":
                self._command_add_movie()
            elif choice == "3":
                self._command_delete_movie()
            elif choice == "4":
                self._command_update_movie()
            elif choice == "5":
                self._command_movie_stats()
            elif choice == "6":
                self._command_random_movie()
            elif choice == "7":
                self._command_search_movie()
            elif choice == "8":
                self._command_sort_by_rating()
            elif choice == "9":
                self._command_sort_by_year()
            elif choice == "0":
                print("\nGoodbye!")
                break
            else:
                print("\nInvalid choice. Please try again.")