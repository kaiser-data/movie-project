import json


def get_movies()-> dict:
    """
    Returns a dictionary of dictionaries that
    contains the movies information in the database.

    The function loads the information from the JSON
    file and returns the data. 

    {
      "Titanic": {
        "rating": 9,
        "year": 1999
      },
      "..." {
        ...
      },
    }
    """
    with open("movies_storage.json","r") as file:
        movies = json.load(file)

    return movies


def save_movies(movies:dict)->None:
    """
    Gets all your movies as an argument and saves them to the JSON file.
    """
    with open('movies_storage.json', 'w') as file:
        json.dump(movies, file, indent=4)
    

def add_movie(title: str, year: int, rating: float) -> None:
    """
    Adds a movie to the movies database.
    Loads the information from the JSON file, add the movie,
    and saves it. The function doesn't need to validate the input.
    """
    # Get the data from a JSON file
    movies = get_movies()
    #adds new movie to movies
    movies[title] = {"year": year, "rating" : rating }  
    # saves movies
    save_movies(movies)


def delete_movie(title: str) -> None:
    """
    Deletes a movie from the movies database.
    Loads the information from the JSON file, deletes the movie,
    and saves it. The function doesn't need to validate the input.
    """
    # Get the data from a JSON file
    movies = get_movies() 
    # deletes movie
    del movies[title]
    # saves movies dict
    save_movies(movies)


def update_movie(title: str, rating: float) -> None:
    """
    Updates a movie from the movies database.
    Loads the information from the JSON file, updates the movie,
    and saves it. The function doesn't need to validate the input.
    """
    movies = get_movies() 
    #updates rating
    movies[title]["rating"] = rating
    #saves movies dict
    save_movies(movies)
  