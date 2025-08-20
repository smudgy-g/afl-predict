import pandas as pd

from config import WIN_POINTS, DRAW_POINTS, LOSS_POINTS, DEFAULT_ELO
from elo import update_elo


def initialise_stats_table(seasons_data: dict[int, pd.DataFrame]) -> pd.DataFrame:
    """
    Initializes a new DataFrame to store team statistics and Elo ratings.

    The table is populated with all unique team names found across the
    provided seasons and initializes their stats (Elo, wins, games played, etc.)
    to their default values.
    """
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


def update_stats_table(stats_table: pd.DataFrame, season_data: pd.DataFrame, home_elo_bonus: float) -> pd.DataFrame:
    """
    Updates team statistics and Elo ratings for all games in a season.

    This function iterates through each game in a given season, applies the home
    Elo bonus, updates the teams' Elo ratings, and increments their win/loss/draw
    and games played counts.
    """
    stats_copy = stats_table.copy()
    for _, row in season_data.iterrows():
        home_team = row['home_team']
        away_team = row['away_team']
        home_score = row['home_score']
        away_score = row['away_score']

        current_home_elo = stats_copy[stats_copy['team'] == home_team]['elo'].iloc[0]
        current_away_elo = stats_copy[stats_copy['team'] == away_team]['elo'].iloc[0]

        adjusted_home_elo = current_home_elo + home_elo_bonus

        result = 'H' if home_score > away_score else 'A'
        if home_score == away_score:
            result = 'D'

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

        new_home_elo, new_away_elo = update_elo(adjusted_home_elo, current_away_elo, result)
        stats_copy.loc[stats_copy['team'] == home_team, 'elo'] = new_home_elo
        stats_copy.loc[stats_copy['team'] == away_team, 'elo'] = new_away_elo

    return stats_copy