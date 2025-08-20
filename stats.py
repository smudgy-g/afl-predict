import pandas as pd
from pandas import DataFrame

from config import WIN_POINTS, DRAW_POINTS, LOSS_POINTS, DEFAULT_ELO
from elo import update_elo


def initialise_stats_table(seasons_data: dict[int, DataFrame]) -> DataFrame:
    all_teams = set()
    for _, df_season in seasons_data.items():
        all_teams.update(df_season['home_team'].unique())
        all_teams.update(df_season['away_team'].unique())
    team_names = sorted(list(all_teams))

    return pd.DataFrame({
        'team': team_names,
        'elo': DEFAULT_ELO,
        'points': 0,
        'wins': 0,
        'draws': 0,
        'losses': 0,
        'win_percentage': 0,
        'games_played': 0,
    })


def update_stats_table(stats_table: pd.DataFrame, season_data: pd.DataFrame) -> pd.DataFrame:
    season_home_win_percentage = season_data[season_data['location'] == 'home']['win_percentage'].iloc[0]
    season_away_win_percentage = season_data[season_data['location'] == 'away']['win_percentage'].iloc[0]
    season_win_average = (season_home_win_percentage + season_away_win_percentage) / 2

    home_advantage = season_home_win_percentage - season_win_average
    away_advantage = season_away_win_percentage - season_win_average

    stats_copy = stats_table.copy()
    for index, row in season_data.iterrows():
        home_team = row['home_team']
        away_team = row['away_team']
        home_score = row['home_score']
        away_score = row['away_score']

        current_home_elo = stats_copy[stats_copy['team'] == home_team]['elo'].iloc[0]
        current_away_elo = stats_copy[stats_copy['team'] == away_team]['elo'].iloc[0]

        result = 'H' if home_score > away_score else 'A'
        if home_score == away_score:
            result = 'D'

        stats_copy['date'] = pd.to_datetime(row['date'])

        stats_copy.loc[stats_copy['team'] == home_team, 'games_played'] += 1
        stats_copy.loc[stats_copy['team'] == away_team, 'games_played'] += 1

        if result == 'H':
            stats_copy.loc[stats_copy['team'] == home_team, 'points'] += WIN_POINTS
            stats_copy.loc[stats_copy['team'] == away_team, 'points'] += LOSS_POINTS

            stats_copy.loc[stats_copy['team'] == home_team, 'wins'] += 1
            stats_copy.loc[stats_copy['team'] == away_team, 'losses'] += 1

        elif result == 'A':
            stats_copy.loc[stats_copy['team'] == home_team, 'points'] += LOSS_POINTS
            stats_copy.loc[stats_copy['team'] == away_team, 'points'] += WIN_POINTS

            stats_copy.loc[stats_copy['team'] == home_team, 'losses'] += 1
            stats_copy.loc[stats_copy['team'] == away_team, 'wins'] += 1

        elif result == 'D':
            stats_copy.loc[stats_copy['team'] == home_team, 'points'] += DRAW_POINTS
            stats_copy.loc[stats_copy['team'] == away_team, 'points'] += DRAW_POINTS

            stats_copy.loc[stats_copy['team'] == home_team, 'draws'] += 1
            stats_copy.loc[stats_copy['team'] == away_team, 'draws'] += 1

        stats_copy['win_percentage'] = stats_copy['wins'] / stats_copy['games_played']
        home_win_percentage_diff = home_team['win_percentage'].iloc[0] - season_win_average
        away_win_percentage_diff = away_team['win_percentage'].iloc[0] - season_win_average

        new_home_elo, new_away_elo = update_elo(current_home_elo, current_away_elo, result)
        stats_copy.loc[stats_copy['team'] == home_team, 'elo'] = new_home_elo
        stats_copy.loc[stats_copy['team'] == away_team, 'elo'] = new_away_elo

    return stats_copy