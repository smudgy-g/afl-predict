from pandas import DataFrame

from elo import calculate_expected_result


def predict_win_probability(home_team: str, away_team: str, team_elos: DataFrame, home_elo_bonus: float) -> tuple[float | None, float | None]:
    """
    Predicts the win probability for the home team against the away team.

    This function retrieves the current Elo ratings for both teams and applies a
    home-field advantage bonus to the home team's rating before calculating
    the expected win probability.
    """
    home_team_row = team_elos[team_elos['team'] == home_team]
    away_team_row = team_elos[team_elos['team'] == away_team]

    if home_team_row.empty or away_team_row.empty:
        print(f"Error: Could not find one of the teams in the Elo table")
        return None, None

    home_elo = home_team_row['elo'].item() + home_elo_bonus
    away_elo = away_team_row['elo'].item()

    prob_a_wins, prob_b_wins = calculate_expected_result(home_elo, away_elo)
    return prob_a_wins, prob_b_wins