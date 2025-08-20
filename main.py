from datetime import datetime
import pandas as pd
from pandas import DataFrame

from config import WIN_POINTS, DRAW_POINTS, LOSS_POINTS, DEFAULT_ELO
from elo import update_elo, apply_mean_reversion
from predict import predict_win_probability
from scraping import get_season_results
from stats import initialise_stats_table, update_stats_table


def create_season_averages(seasons_data: dict[int, pd.DataFrame]) -> dict[int, pd.DataFrame]:
    averages = dict()

    for key, value in seasons_data.items():
        df = pd.DataFrame(columns = ['location', 'wins', 'losses', 'draws', 'games', 'win_percentage'])

        df['location'] = ['home', 'away']
        df['wins'] = 0
        df['losses'] = 0
        df['draws'] = 0
        df['games'] = 0
        df['win_percentage'] = 0.0

        for index, row in value.iterrows():
            home_team_points = row['home_score']
            away_team_points = row['away_score']

            if home_team_points > away_team_points:
                df.loc[df['location'] == 'home', 'wins'] += 1
                df.loc[df['location'] == 'away', 'losses'] += 1
            elif away_team_points > home_team_points:
                df.loc[df['location'] == 'away', 'wins'] += 1
                df.loc[df['location'] == 'home', 'losses'] += 1
            else:
                df.loc[df['location'] == 'home', 'draws'] += 1
                df.loc[df['location'] == 'away', 'draws'] += 1

            df.loc[df['location'] == 'home', 'games'] += 1
            df.loc[df['location'] == 'away', 'games'] += 1

        home_win_percentage =  (df.loc[df['location'] == 'home', 'wins'] /
                           df.loc[df['location'] == 'home', 'games'].replace(0, 1))
        df.loc[df['location'] == 'home', 'win_percentage'] = home_win_percentage

        away_win_percentage = (df.loc[df['location'] == 'away', 'wins'] /
                               df.loc[df['location'] == 'away', 'games'].replace(0, 1))
        df.loc[df['location'] == 'away', 'win_percentage'] = away_win_percentage

        averages[key] = df

    return averages



if __name__ == '__main__':
    current_year = datetime.now().year
    seasons = [current_year - i for i in range(0, 3)]
    seasons.reverse()

    seasons_data = get_season_results(seasons)
    season_averages = create_season_averages(seasons_data)
    stats = initialise_stats_table(seasons_data)

    for year in sorted(seasons_data.keys()):
        print(f"Processing season: {year}")

        # Apply mean reversion to all PREVIOUS years
        if year > min(seasons_data.keys()):
            stats = apply_mean_reversion(stats)

        stats = update_stats_table(stats, seasons_data[year])

    print(stats.head())

    a, b = predict_win_probability('Essendon', 'Western Bulldogs', stats, season_averages[current_year])

    # print(a, b)


    #
    # all_games_dfs = []
    # for year in seasons:
    #     all_games_dfs.append(stats[year])
    #
    # all_games_dfs = pd.concat(all_games_dfs).sort_values(by='date').reset_index(drop=True)
    # print(all_games_dfs)

    # for item in season_averages.values():
    #     print(item)

    # apply a mean reversion for each season before concatenating
    # 0.2 to 0.4 regression factor
