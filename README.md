# AFL Elo Predictor 🏉

This project is a command-line application that predicts the outcome of Australian Football League (AFL) matches using a historical Elo rating system. The model is built from scratch and includes key features like mean reversion and a home-field advantage adjustment to provide accurate and robust predictions.

## Features ✨

-   **Elo Rating System:** Calculates and updates team Elo ratings based on historical game results.
-   **Home-Field Advantage:** Adjusts team ratings for each game to account for the statistical advantage of playing at home. This bonus is a global value derived from historical league data.
-   **Mean Reversion:** Gradually pulls team ratings back towards a league average at the end of each season, ensuring ratings don't become permanently inflated or deflated over time.
-   **Data Scraping & Caching:** Scrapes match results from a reliable online source and caches the data locally as CSV files to prevent repeated downloads.
-   **Interactive CLI:** Provides a user-friendly command-line interface to:
    -   Predict the winning probability of any two teams.
    -   Display the current team Elo rankings.
    -   Reload the latest match data from the web.

## How to Run the Application 🚀

### Prerequisites

-   Python 3.6+
-   Git

### Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/smudgy-g/afl-predict
    cd afl-predict
    ```

2.  **Create a virtual environment** (recommended):

    ```bash
    python -m venv venv
    ```

    Activate the environment:

    -   **macOS/Linux:** `source venv/bin/activate`
    -   **Windows:** `.\venv\Scripts\activate`

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**

    ```bash
    python main.py
    ```

### Usage

Once the application starts, it will automatically scrape the necessary historical data (or load it from the cache) and calculate the Elo ratings. You will then be presented with a menu of options:

1.  **Predict a match:** Enter the corresponding numbers for the home and away teams to get the predicted winning probability.
2.  **Show stats table:** View the current Elo rankings and other team statistics.
3.  **Refresh data:** Force the application to download the latest data from the web, useful for getting up-to-date information for ongoing seasons.
4.  **Quit:** Exit the program.

## Credits 🙏

-   **Elo Rating System:** Elo rating system created with the help of William Leiss [Intro to Power Ratings: Ep 1 - Creating an ELO Rating System](https://www.youtube.com/watch?v=BzaS4Tb0fX4&t=1231s&ab_channel=WilliamLeiss).
-   **Data Source:** Match data is scraped from [Footywire.com](https://www.footywire.com/).
