from movie_app import MovieApp
from storage_json import StorageJson

if __name__ == "__main__":
    # Initialize storage
    storage = StorageJson("movies.json")

    # Initialize movie app
    movie_app = MovieApp(storage)

    # Run the app
    movie_app.run()1