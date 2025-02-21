import json
from isstorage import IStorage

class StorageJson(IStorage):
    """
    A concrete implementation of IStorage that uses JSON files for storage.
    """

    def __init__(self, file_path):
        """
        Initializes the StorageJson instance with the path to the JSON file.
        :param file_path: Path to the JSON file where movie data is stored.
        """
        self.file_path = file_path

    def list_movies(self):
        """
        Loads and returns the movies from the JSON file using UTF-8 encoding.
        :return: Dictionary of movies.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as fileobj:
                return json.load(fileobj)
        except FileNotFoundError:
            return {}

    def add_movie(self, title, year, rating, poster):
        """
        Adds a new movie to the JSON file with UTF-8 encoding.
        :param title: Title of the movie.
        :param year: Year the movie was released.
        :param rating: Rating of the movie.
        :param poster: URL of the movie's poster.
        """
        movies = self.list_movies()
        movies[title] = {
            "rating": rating,
            "year": year,
            "poster": poster
        }
        with open(self.file_path, 'w', encoding='utf-8') as fileobj:
            json.dump(movies, fileobj, indent=4, ensure_ascii=False)

    def delete_movie(self, title):
        """
        Deletes a movie from the JSON file with UTF-8 encoding.
        :param title: Title of the movie to delete.
        """
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            with open(self.file_path, 'w', encoding='utf-8') as fileobj:
                json.dump(movies, fileobj, indent=4, ensure_ascii=False)

    def update_movie(self, title, rating):
        """
        Updates the rating of a movie in the JSON file with UTF-8 encoding.
        :param title: Title of the movie to update.
        :param rating: New rating for the movie.
        """
        movies = self.list_movies()
        if title in movies:
            movies[title]['rating'] = rating
            with open(self.file_path, 'w', encoding='utf-8') as fileobj:
                json.dump(movies, fileobj, indent=4, ensure_ascii=False)