import csv
from isstorage import IStorage

class StorageCsv(IStorage):
    """
    A concrete implementation of IStorage that uses CSV files for storage.
    """

    def __init__(self, file_path):
        """
        Initializes the StorageCsv instance with the path to the CSV file.
        :param file_path: Path to the CSV file where movie data is stored.
        """
        self.file_path = file_path

    def list_movies(self):
        """
        Loads and returns the movies from the CSV file as a dictionary.
        Returns:
            dict: A dictionary of dictionaries containing movie information.
                  Example: {"Titanic": {"rating": 9.2, "year": 1997, "poster": "..."}}
        """
        movies = {}
        try:
            with open(self.file_path, mode='r', encoding='utf-8', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    title = row['title']
                    year = int(row['year'])
                    rating = float(row['rating'])
                    poster = row.get('poster', '')  # Optional field for poster URL
                    movies[title] = {
                        "rating": rating,
                        "year": year,
                        "poster": poster
                    }
        except FileNotFoundError:
            return {}
        return movies

    def add_movie(self, title, year, rating, poster=""):
        """
        Adds a new movie to the CSV file.
        :param title: Title of the movie.
        :param year: Year the movie was released.
        :param rating: Rating of the movie.
        :param poster: (Optional) URL of the movie's poster.
        """
        movies = self.list_movies()
        if title not in movies:
            movies[title] = {
                "rating": rating,
                "year": year,
                "poster": poster
            }

            # Write the updated data back to the CSV file
            fieldnames = ['title', 'year', 'rating', 'poster']
            with open(self.file_path, mode='w', encoding='utf-8', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for movie_title, movie_data in movies.items():
                    writer.writerow({
                        'title': movie_title,
                        'year': movie_data['year'],
                        'rating': movie_data['rating'],
                        'poster': movie_data['poster']
                    })

    def delete_movie(self, title):
        """
        Deletes a movie from the CSV file.
        :param title: Title of the movie to delete.
        """
        movies = self.list_movies()
        if title in movies:
            del movies[title]

            # Write the updated data back to the CSV file
            fieldnames = ['title', 'year', 'rating', 'poster']
            with open(self.file_path, mode='w', encoding='utf-8', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for movie_title, movie_data in movies.items():
                    writer.writerow({
                        'title': movie_title,
                        'year': movie_data['year'],
                        'rating': movie_data['rating'],
                        'poster': movie_data['poster']
                    })

    def update_movie(self, title, rating):
        """
        Updates the rating of a movie in the CSV file.
        :param title: Title of the movie to update.
        :param rating: New rating for the movie.
        """
        movies = self.list_movies()
        if title in movies:
            movies[title]['rating'] = rating

            # Write the updated data back to the CSV file
            fieldnames = ['title', 'year', 'rating', 'poster']
            with open(self.file_path, mode='w', encoding='utf-8', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for movie_title, movie_data in movies.items():
                    writer.writerow({
                        'title': movie_title,
                        'year': movie_data['year'],
                        'rating': movie_data['rating'],
                        'poster': movie_data['poster']
                    })