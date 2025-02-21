from movie_app import MovieApp
from storage_json import StorageJson
from storage_csv import StorageCsv

# Uncomment the appropriate storage class based on the desired storage format
# storage = StorageCsv("movies.csv")
storage = StorageJson("movies.json")

# Instantiate the MovieApp class with the chosen storage object
# Type hint: `storage` is an instance of a class that implements the IStorage interface
movie_app: MovieApp = MovieApp(storage)

# Run the application by invoking the `run` method of the MovieApp instance
# This starts the interactive command-line interface for managing movies
movie_app.run()