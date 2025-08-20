import os
from datetime import datetime
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pandas as pd


def get_html(page_url: str) -> str:
    """
    Open a web page and return its source code
    """
    request = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
    return urlopen(request).read()


def extract_win_loss_data(html_content: str, year: int) -> pd.DataFrame:
    """
    Extract the win/loss data from the html content into  a Pandas DataFrame
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    all_rows = soup.find_all('tr', class_=['darkcolor', 'lightcolor'])
    if not all_rows:
        print("Error: Data not found in page.")
        return pd.DataFrame()

    df = pd.DataFrame(columns=['date', 'home_team', 'away_team', 'home_score', 'away_score'])

    for row in all_rows:
        row_data = row.find_all('a')

        if len(row_data) < 3:
            continue

        try:
            match_date = row.find('td').get_text().strip()
            match_date = match_date.split(' ')
            match_date = datetime.strptime(f"{match_date[1]} {match_date[2]} {year}", '%d %b %Y')

            home = row_data[0].get_text().strip()
            away = row_data[1].get_text().strip()
            scores = row_data[2].get_text().strip().split('-')

            df.loc[len(df)] = [pd.to_datetime(match_date), home, away, pd.to_numeric(scores[0]), pd.to_numeric(scores[1])]
        except AttributeError as e:
            # Handle cases where find('a') might return None or text parsing fails
            print(f"Error parsing specific elements in row: {e}. Skipping row.")
            continue
        except ValueError as e:
            # Handle conversion errors (e.g., date format, int conversion)
            print(f"Data conversion error in row: {e}. Skipping row.")
            continue
        except IndexError as e:
            print(f"Index error (missing column) in row: {e}. Skipping row.")
            continue

    df.to_csv(f'data/{year}.csv', index=False)
    return df


def get_season_results(seasons: list[int], reload: bool = False) -> dict[int, pd.DataFrame]:
    '''
    Loop over each season and extract the win/loss data into a combined pandas dataframe
    '''
    all_seasons = dict()

    for season in seasons:
        season_data: pd.DataFrame
        file_path = f'data/{season}.csv'

        if reload and os.path.exists(file_path):
            print(f'Reload option selected. Deleting existing file for {season}...')
            os.remove(file_path)

        if os.path.exists(file_path):
            print(f'Reading data for season {season} from file...')
            season_data = pd.read_csv(file_path)
        else:
            print(f'Downloading data for season {season}...')
            url = f"https://www.footywire.com/afl/footy/ft_match_list?year={season}"
            html = get_html(url)
            season_data = extract_win_loss_data(html, season)

        if season_data.empty:
            print(f"No data parsed for season {season}. Skipping.")
            continue

        season_data['year'] = season
        all_seasons[season] = season_data
        print(f"Finished parsing data for season {season}\n")

    return all_seasons