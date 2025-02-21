from abc import ABC, abstractmethod

class IStorage(ABC):
    """
    An interface for storage implementations.
    Defines the required methods for interacting with movie data.
    """

    @abstractmethod
    def list_movies(self):
        """
        Returns a dictionary of dictionaries that contains the movies information in the database.
        """
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """
        Adds a movie to the movies database.
        """
        pass

    @abstractmethod
    def delete_movie(self, title):
        """
        Deletes a movie from the movies database.
        """
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """
        Updates a movie's rating in the movies database.
        """
        pass