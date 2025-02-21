import os
import sys
import re
import random
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from rapidfuzz import fuzz
from termcolor import cprint

import movie_storage

# 1. Utility Functions
# 2. Menu Functions
# 3. Main Function	
# -------------------------------------------------------------

# 1. Utility Functions
def list_movies() -> str:
    """
    Creates a string listing all movies with their year and rating.

    Returns:
        str: A string starting with the total number of movies, followed by each movie's title, year, and rating.
    """
    # Get the data from the JSON file
    movies = movie_storage.get_movies() 

    # Determine the total number of movies in the database
    total_movies = len(movies)

    # Create movie lines using list comprehension
    movie_lines = [f"{title} ({info['year']}): {info['rating']}" for title, info in movies.items()]

    # Join them together with a header
    movies_list_str = f"\n{total_movies} movies in total\n" + "\n".join(movie_lines)

    # Return the overview string
    return movies_list_str


def valid_movie_name(movie_name: str) -> None:
    """
    Validates the movie name.

    Args:
        movie_name (str): The name of the movie to validate.

    Raises:
        ValueError: If the movie name is empty, contains invalid characters, or already exists.
    """
    # checks if movie name is empty
    if not movie_name.strip():
        raise ValueError("Movie name must not be empty!")

    # checks if movie name is contains invalid chars
    if not re.match(r"^[a-zA-Z0-9\s\-',.!?]+$", movie_name):
        raise ValueError("Movie name contains invalid characters!")

    # Get the data from the JSON file
    movies = movie_storage.get_movies() 
    # checks if movie_name in movies
    if movie_name in movies.keys():
        raise ValueError(f"Movie '{movie_name}' already exists!")


def valid_year(year: str) -> None:
    """
    Validates the movie year.

    Args:
        year (str): The year input to validate.

    Raises:
        ValueError: If the year is not an integer or not within the valid range.
    """
    #defines year limits for user input
    min_year = 1887  # Oldest movie on IMDb: "Man Walking Around the Corner" (1887)
    current_year = datetime.now().year

    #check if user input for year is int
    try:
        year_int = int(year)
    except ValueError:
        raise ValueError("Invalid input: Please enter an integer as year.")

    #checks if year is in the limit range
    if not min_year <= year_int <= current_year:
        raise ValueError(f"Year must be between {min_year} and {current_year}.")


def valid_rating(rating: str) -> None:
    """
    Validates the movie rating.

    Args:
        rating (str): The rating input to validate.

    Raises:
        ValueError: If the rating is not a float between 0 and 10 with at most one decimal place.
    """
    # checks if user input rating can be tranformed to float value
    try:
        rating_float = float(rating)
    except ValueError:
        raise ValueError("Invalid input: Rating is not a float.")

    #checks if rating is in range
    if not 0 <= rating_float <= 10:
        raise ValueError("Rating must be between 0 and 10.")
    
    #checks if raing has only one decimal
    if not (rating_float * 10).is_integer():
        raise ValueError("Rating should have at most one decimal place.")

def add_movie() -> None:
    """
    Adds a new movie with its year and rating to the movies dictionary.

    Prompts the user for movie details, validates the inputs, and adds the movie to the storage.

    Raises:
        ValueError: If the movie already exists.
    """
    while True:
        # User input for new movie name
        new_movie_name = input("\nEnter new movie name: ")
        try:
            valid_movie_name(new_movie_name)
            break
        except ValueError as e:
            cprint(e, "red")

    while True:
        # User input for new movie year
        new_movie_year = input("\nEnter new movie year: ")
        try:
            valid_year(new_movie_year)
            break
        except ValueError as e:
            cprint(e, "red")
                
    new_movie_year = int(new_movie_year)        

    while True:
        # User input for new movie rating
        new_movie_rating = input("\nEnter new movie rating (0-10): ")
        try:
            valid_rating(new_movie_rating)
            break
        except ValueError as e:
            cprint(e, "red")
        
    new_movie_rating = float(new_movie_rating)

    # Add the movie and save the data to the JSON file
    try:
        movie_storage.add_movie(new_movie_name, new_movie_year, new_movie_rating)
        movie_storage.save_movies(movie_storage.get_movies())
        # Print confirmation of update
        cprint(f'\nMovie "{new_movie_name}" successfully added.', "green")
    except ValueError as e:
        # Handle case where movie already exists
        cprint(e, "red")


def delete_movie() -> None:
    """
    Deletes a movie with its rating from the movies dictionary.

    Prompts the user for the movie name to delete and removes it from the storage if it exists.
    """
    # User input for movie name to delete
    delete_movie_name = input("\nEnter movie name: ")

    # Attempt to delete the movie and print status
    try:
        movie_storage.delete_movie(delete_movie_name)    
        movie_storage.save_movies(movie_storage.get_movies())
        cprint(f'Movie "{delete_movie_name}" successfully deleted.', "green")
    except KeyError:
        cprint(f'Movie "{delete_movie_name}" does not exist!', "red")


def update_movie_rating() -> None:
    """
    Updates the rating of an existing movie.

    Prompts the user for the movie name and the new rating, then updates it in the storage.
    """
    # User input for movie name to update
    update_movie_name = input('\nEnter movie name: ')
    movies = movie_storage.get_movies()

    if update_movie_name in movies:
        while True:
            # User input for new rating
            update_rating = input("\nEnter new movie rating (0-10): ")
            try:
                valid_rating(update_rating)
                break
            except ValueError as e:
                cprint(e, "red")
    
        update_rating = float(update_rating)
        try:
            movie_storage.update_movie(update_movie_name, update_rating)
            cprint(f"Movie '{update_movie_name}' successfully updated.", "green")
        except KeyError:
            # This should not occur as we've already checked existence
            cprint(f"Movie '{update_movie_name}' does not exist!", "red")
    else:
        cprint(f"Movie '{update_movie_name}' doesn't exist!", "red")


def stats_movies() -> str:
    """
    Generates and returns statistics for the movies.

    Calculates average rating, median rating, best-rated movie, and worst-rated movie.

    Returns:
        str: A formatted string containing the statistics.
    """
    # Get the data from the JSON file
    movies = movie_storage.get_movies() 
    # Create a sorted list of movie ratings
    sorted_movies_ratings = sorted([info['rating'] for info in movies.values()])
    
    # Calculate mean average movie rating
    average_rating = sum(sorted_movies_ratings) / len(movies)

    # Calculate median average rating
    if len(movies) % 2 != 0:
       median_rating = sorted_movies_ratings[len(movies)//2]
    else:
        median_rating = ((sorted_movies_ratings[len(movies) // 2 - 1]
                        + sorted_movies_ratings[len(movies) // 2])
                        / 2)

    # Determine best rated movie
    best_movie = max(movies.items(), key=lambda x: x[1]["rating"])

    # Determine worst rated movie
    worst_movie = min(movies.items(), key=lambda x: x[1]["rating"])

    # Create string containing calculated statistic values above
    movies_stats_str = (
        f"\nAverage Rating: {average_rating:.1f}\n"
        f"Median Rating: {median_rating:.1f}\n"
        f"Best Movie: {best_movie[0]}, {best_movie[1]['rating']:.1f}\n"
        f"Worst Movie: {worst_movie[0]}, {worst_movie[1]['rating']:.1f}"
    )

    # Return string with statistic values
    return movies_stats_str

def random_movie() -> str:
    """
    Selects and returns a random movie from the movies dictionary.

    Returns:
        str: A formatted string containing a random movie title and its rating.
    """
    # Get the data from the JSON file
    movies = movie_storage.get_movies() 
    # Select a random movie using the random module
    random_movie_title = random.choice(list(movies.keys()))  # Changed variable name

    # Create string output with title and rating
    random_movie_str = (
        f"\nYour movie for tonight: {random_movie_title}"  # Use new variable name
        f" is rated {movies[random_movie_title]['rating']}."
    )

    # Return string output with title and rating
    return random_movie_str

def search_movies() -> str:
    """
    Searches for movies based on user input and returns matching results.

    If no direct matches are found, performs a fuzzy search to find similar titles.

    Returns:
        str: A string containing matching movie titles and their ratings.
    """
    # Get the data from the JSON file
    movies = movie_storage.get_movies() 
    # User input for search string
    search_str = input("\nEnter part of movie name: ").lower()

    # Creating output string with all matches
    search_result_str = ''

    for title in movies.keys():
        if search_str in title.lower():
            search_result_str += f"{title}, {movies[title]['rating']}\n"

    # If no result, use fuzzy search
    if search_result_str == '':
        search_result_str = fuzzy_search(movies, search_str)

    # Return string with all matches for user search
    return search_result_str

def fuzzy_search(movies: dict, search_str: str) -> str:
    """
    Returns movie titles similar to the search string using rapidfuzz.

    Args:
        movies (dict): A dictionary containing movie titles as keys and their info as values.
        search_str (str): The search string input by the user.

    Returns:
        str: A string containing similar movie titles and their ratings.
    """
    # Limit for fuzzy matching
    fuzz_limit = 70
    search_result_str = ''
    header_string = (
        f'The movie "{search_str}" does not exist.\n'
        f'Did you mean:\n'
    )
    # Loop through all words in titles to find similarity with rapidfuzz
    for title in movies.keys():
        for word in title.split():
            fuzz_ratio = fuzz.ratio(search_str, word.lower())
            if fuzz_ratio > fuzz_limit:
                search_result_str += f"{title}, {movies[title]['rating']}\n"
                break  # Avoid adding the same title multiple times

    if search_result_str != "":
        search_result_str = header_string + search_result_str

    return search_result_str


def movies_sorted_by_rating() -> str:
    """
    Outputs a string with titles and ratings sorted by rating.

    Returns:
        str: A string with all movies and ratings sorted from highest to lowest rating.
    """
    # Get the data from the JSON file
    movies = movie_storage.get_movies() 

    # Sort the dictionary by movie rating in descending order
    sorted_movies = dict(
        sorted(
            movies.items(),
            key=lambda kv: kv[1]["rating"],
            reverse=True
        )
    )
    # Create movie lines using list comprehension
    rating_sorted_movies_str = "\n".join(f"{title} ({info['year']}): {info['rating']}" for title, info in sorted_movies.items())

    # Return string output for sorted movies by rating
    return rating_sorted_movies_str


def movies_sorted_by_year() -> str:
    """
    Sorts the movies by their release year based on user preference.

    Prompts the user to choose whether they want the latest (newest) movies first or the earliest (oldest).
    Returns a formatted string listing all movies sorted by year.

    Returns:
        str: A string listing all movies sorted by year according to user preference.
    """
    while True:
        # Prompt user for sorting preference
        reverse_order = input("Do you want the latest (newest) movies first? (Y/N): ").strip().upper()
        if reverse_order in {"Y", "N"}:
            break
        print('Please enter "Y" or "N".') 

    # Get the data from the JSON file
    movies = movie_storage.get_movies() 

    if not movies:
        # Inform the user if there are no movies to sort
        return "\nNo movies available to sort by year."

    # Sorting dictionary by movie year
    sorted_movies = dict(
        sorted(
            movies.items(),
            key=lambda kv: kv[1]["year"],
            reverse=reverse_order == "Y"  # True for descending (latest first), False for ascending (earliest first)
        )
    )

    # Create movie lines using list comprehension
    year_sorted_movies_str = "\n".join(f"{title} ({info['year']}): {info['rating']}" for title, info in sorted_movies.items())

    # Return string output for sorted movies by year
    return year_sorted_movies_str


def filter_movies() -> str:
    """
    Filters movies based on minimum rating and a range of years.

    Prompts the user for minimum rating, start year, and end year to filter the movies.

    Returns:
        str: A string listing all movies that meet the filter criteria.
    """
    while True:
        filter_rating = input("Enter minimum rating (leave blank for no minimum rating): ").strip()
        if filter_rating != "":
            try:
                valid_rating(filter_rating)
                break
            except ValueError as e:
                cprint(e, "red")
                continue
        filter_rating = 0
        break

    filter_rating = float(filter_rating)
    while True:
        start_year = input("Enter start year (leave blank for no start year): ").strip()
        if start_year != '':
            try:
                valid_year(start_year)
                break
            except ValueError as e:
                cprint(e, "red")
                continue
        start_year = 1887
        break
    
    while True:
        end_year = input("Enter end year (leave blank for no end year): ").strip()
        if end_year != '':
            try:
                valid_year(end_year)  
                break
            except ValueError as e:
                cprint(e, "red")
                continue
        end_year = datetime.now().year
        break
    
    start_year = int(start_year)
    end_year = int(end_year)

    # Get the data from the JSON file
    movies = movie_storage.get_movies() 

    # Create movie lines with list comprehension
    filtered_movies_str = "\n".join(
        f"{title} ({info['year']}): {info['rating']}" 
        for title, info in movies.items() 
        if info['rating'] >= filter_rating and start_year <= info['year'] <= end_year
    )

    if not filtered_movies_str:
        return "\nNo movies match the filter criteria."

    filtered_movies_str = "Filtered Movies:\n" + filtered_movies_str

    return filtered_movies_str


def create_histogramm() -> None:
    """
    Creates a rating histogram using matplotlib for movie ratings and saves it as a .png file.
    """
    # Get the data from the JSON file
    movies = movie_storage.get_movies() 

    if not movies:
        cprint("No movies available to create a histogram.", "red")
        return

    # Extract ratings
    ratings = [movie['rating'] for movie in movies.values()]    

    # Create figure and axis with subplots
    fig, ax = plt.subplots()

    # Plotting and styling histogram
    ax.hist(
        ratings, hatch='//', color='gold', edgecolor="black",
        histtype='bar', rwidth=0.8, alpha=0.7, bins=np.linspace(0,10,21)
    )

    # Set title
    ax.set_title("Rating Histogram for Movies", fontweight="bold", fontsize=18)

    # Naming of x-axis and y-axis
    ax.set_xlabel("Rating between 0 - 10", fontweight="bold")
    ax.set_ylabel("Movie count", fontweight="bold")

    # Setting x-ticks
    ax.set_xticks(np.linspace(0,10,11))
    # Setting minor ticks
    minor_locator = AutoMinorLocator(2)  # 2 minor ticks per major tick
    ax.xaxis.set_minor_locator(minor_locator)
    # Grid for y-axis
    ax.grid(axis='y', alpha=0.75)
    # Define face color of graph
    fig.patch.set_facecolor('honeydew')

    # Save figure
    file_name = "Rating_Histogram_Movies.png"  # Added .png extension here
    cprint(save_figure(file_name, fig), "green")  # Removed extra whitespace

def save_figure(file_name: str, fig: plt.Figure) -> str:
    """
    Saves a matplotlib figure as a .png file.

    Args:
        file_name (str): The name under which the figure should be saved (including extension).
        fig (plt.Figure): The matplotlib figure to save.

    Returns:
        str: Confirmation message that the histogram was successfully saved.
    """
    if os.path.isfile(file_name):
        os.remove(file_name)
    fig.savefig(file_name)

    return f'Histogram was successfully saved as "{file_name}".'

# -------------------------------------------------------------

# 2. Menu Functions
def menu_list() -> str:
    """
    Creates the menu list and returns it as a string.

    Returns:
        str: A string representing the menu structure.
    """
    # Create string with menu options
    menu_str = (
            "\nMenu:"
            "\n0. Exit"
            "\n1. List movies"
            "\n2. Add movie"
            "\n3. Delete movie"
            "\n4. Update movie rating"
            "\n5. Stats"
            "\n6. Random movie"
            "\n7. Search movie"
            "\n8. Movies sorted by rating"
            "\n9. Movies sorted by year"
            "\n10. Filter movies"
            "\n11. Create Rating Histogram\n"
    )

    # Return string with menu options
    return menu_str


def menu_logic(user_choice: int, response_color: str = "white") -> None:
    """
    Executes the function corresponding to the user's menu choice.

    Args:
        user_choice (int): The menu option selected by the user.
        response_color (str, optional): The color for the response text. Defaults to "white".
    """
    # Responses for user input (0-11)
    if user_choice == 0:
        print("Bye!")
        sys.exit()
    elif user_choice == 1:
        cprint(list_movies(), response_color)
    elif user_choice == 2:
        add_movie()
    elif user_choice == 3:
        delete_movie()
    elif user_choice == 4:
        update_movie_rating()
    elif user_choice == 5:
        cprint(stats_movies(), response_color)
    elif user_choice == 6:
        cprint(random_movie(), response_color)
    elif user_choice == 7:
        cprint(search_movies(), response_color)
    elif user_choice == 8:
        cprint(movies_sorted_by_rating(), response_color)
    elif user_choice == 9:
        cprint(movies_sorted_by_year(), response_color) 
    elif user_choice == 10:
        cprint(filter_movies(), response_color)       
    elif user_choice == 11:
        create_histogramm()
    else:
        cprint("Invalid input. Please enter a number between 0 and 11.", "red")

# -------------------------------------------------------------

# 3. Main Function
def main() -> None:
    """
    The main function for the movie database application. It displays the menu,
    handles user input, and invokes corresponding functions.
    """
    menu_color = "light_blue"
    user_input_color = "light_magenta"
    response_color = "yellow"
    # Event loop for movie database program
    while True:
        # Print menu options on the terminal (0-11)
        cprint(menu_list(), menu_color)

        # User input to select function
        cprint("Enter choice (0-11): ", user_input_color)
        try:
            user_choice = int(input())
            menu_logic(user_choice, response_color)
        except ValueError:
            cprint("Invalid input. Please enter an integer between 0 and 11.", "red")

        # Ask user to continue to go back to menu options
        cprint("\nPress Enter to continue...", user_input_color)
        input()


if __name__ == "__main__":
    main()
