from storage_json import StorageJson

storage = StorageJson('movies.json')
print(storage.list_movies())
storage.add_movie(...)
...