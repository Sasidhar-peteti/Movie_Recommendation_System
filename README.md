# Movie Recommendation System

This project is a Movie Recommendation System that recommends movies based on a given title or genre. The system uses Natural Language Processing (NLP) techniques to process movie overviews and genres to provide relevant recommendations.

## Features

- **Search by Title:** Enter a movie title to get a list of recommended movies similar to the entered title.
- **Search by Genre:** Enter a genre to get a list of movies within that genre.
- **Randomized Recommendations:** Every search by genre will provide a different set of movie recommendations.
- **Graphical User Interface (GUI):** Easy-to-use interface created with Tkinter.

## Requirements

- Python 3.6+
- pandas
- scikit-learn
- tkinter
- pillow

## Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/movierecommendationsystem.git
   cd movierecommendationsystem
   ```

2. **Install the required packages:**

   ```bash
   pip install pandas scikit-learn pillow
   ```

3. **Ensure you have the necessary files:**

   - `dataset.csv`: The dataset containing movie details.
   - `background.jpg`: The background image for the GUI.

4. **Run the application:**

   ```bash
   python movierecommendationsystem.py
   ```

## File Structure

- `movierecommendationsystem.py`: Main application file containing the logic for the recommendation system and the GUI.
- `dataset.csv`: CSV file containing movie data.
- `background.jpg`: Background image for the GUI.

## Usage

1. **Run the application:**

   ```bash
   python movierecommendationsystem.py
   ```

2. **Use the dropdown menu to select a search option:**
   - **Title:** Enter a movie title in the provided input field and click "Search" to get recommendations.
   - **Genre:** Enter a genre in the provided input field and click "Search" to get a list of movies within that genre.

3. **View Recommendations:**
   - Recommendations will be displayed below the search button with the text "Recommendations for You".
