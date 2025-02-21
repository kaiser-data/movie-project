Below is a `README.md` file for your movie database application. This document provides an overview of the project, instructions for setup and usage, and details about its features and architecture.

---

# Movie Database Application

## Table of Contents
1. [Overview](#overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Setup Instructions](#setup-instructions)
5. [Usage](#usage)
6. [Architecture](#architecture)
7. [Contributing](#contributing)
8. [License](#license)

---

## Overview

The **Movie Database Application** is a command-line tool designed to manage and analyze a collection of movies. It allows users to add, delete, update, and list movies, as well as perform various operations like generating statistics, sorting, filtering, and creating visualizations such as histograms. Additionally, it supports dynamic storage options (JSON or CSV) and integrates with the OMDb API for fetching movie data automatically.

---

## Features

- **Add Movie**: Add a new movie with its title, year, rating, and poster URL.
- **Delete Movie**: Remove a movie from the database by its title.
- **Update Movie Rating**: Update the rating of an existing movie.
- **List Movies**: Display all movies in the database with their year and rating.
- **Statistics**: Generate statistics such as average rating, median rating, best-rated movie, and worst-rated movie.
- **Random Movie**: Select a random movie from the database.
- **Search Movies**: Search for movies by partial name, including fuzzy matching for unmatched queries.
- **Sort Movies**: Sort movies by rating (descending) or release year (ascending/descending).
- **Filter Movies**: Filter movies based on minimum rating and a range of years.
- **Create Histogram**: Generate and save a histogram of movie ratings as a `.png` file.
- **Generate Website**: Dynamically generate an HTML website displaying the movies in a responsive grid layout.
- **OMDb API Integration**: Automatically fetch movie details (year, rating, and poster URL) using the OMDb API.

---

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.7 or higher
- Required libraries:
  - `requests`: For interacting with the OMDb API.
  - `matplotlib`: For generating histograms.
  - `jinja2`: For rendering the HTML template.
  - `python-dotenv`: For managing environment variables (e.g., OMDb API key).

You can install the required libraries using pip:

```bash
pip install requests matplotlib jinja2 python-dotenv
```

---

## Setup Instructions

1. **Clone the Repository**:
   Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/movie-database-app.git
   cd movie-database-app
   ```

2. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add your OMDb API key:

   ```
   OMDB_API_KEY=your_api_key_here
   ```

   You can obtain an API key by signing up at [OMDb API](http://www.omdbapi.com/apikey.aspx).

3. **Initialize Storage**:
   Choose a storage type (JSON or CSV) by modifying the `main.py` file. For example:

   - JSON storage:
     ```python
     storage = StorageJson("movies.json")
     ```

   - CSV storage:
     ```python
     storage = StorageCsv("movies.csv")
     ```

4. **Run the Application**:
   Execute the application using Python:

   ```bash
   python main.py
   ```

---

## Usage

Once the application is running, you will see a menu with the following options:

### Menu Options

```
Menu:
0. Exit
1. List Movies
2. Add Movie
3. Delete Movie
4. Update Movie Rating
5. Stats
6. Random Movie
7. Search Movie
8. Movies Sorted by Rating
9. Movies Sorted by Year
10. Filter Movies
11. Create Rating Histogram
12. Generate Website
```

### Example Commands

- **Add Movie**:
  Enter the movie title, and the application will fetch additional details (year, rating, poster URL) from the OMDb API.

- **Generate Website**:
  Select option `12` to create an interactive HTML website displaying all movies in a responsive grid layout. The website will be saved as `index.html`.

---

## Architecture

The application follows an Object-Oriented Programming (OOP) design pattern, ensuring modularity and extensibility:

1. **Interfaces**:
   - `IStorage`: An abstract interface defining the CRUD operations for movie storage.

2. **Storage Implementations**:
   - `StorageJson`: Implements the `IStorage` interface for JSON file storage.
   - `StorageCsv`: Implements the `IStorage` interface for CSV file storage.

3. **Core Logic**:
   - `MovieApp`: Encapsulates all application logic, including menu handling and movie operations.

4. **Template Rendering**:
   - Uses Jinja2 to dynamically generate the HTML website (`index.html`) based on the provided template (`_static/index_template.html`).

5. **Validation**:
   - Includes validation functions for movie names, years, and ratings to ensure data integrity.

---

## Contributing

 Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Submit a pull request detailing your changes.

Please adhere to the existing code style and include tests for any new functionality.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Sample Output

### Terminal Interaction

```
Menu:
0. Exit
1. List Movies
2. Add Movie
3. Delete Movie
4. Update Movie Rating
5. Stats
6. Random Movie
7. Search Movie
8. Movies Sorted by Rating
9. Movies Sorted by Year
10. Filter Movies
11. Create Rating Histogram
12. Generate Website

Enter choice (0-12): 1

5 movies in total
Titanic (1997): 9.0
Inception (2010): 8.8
The Matrix (1999): 8.7
The Godfather (1972): 9.2
The Shawshank Redemption (1994): 9.3
```

### Generated Website

The generated `index.html` file displays movies in a responsive grid layout, adapting to different screen sizes. Each movie card includes:
- Poster image
- Title
- Release year
