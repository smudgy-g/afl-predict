from pandas import DataFrame

from elo import calculate_expected_result


def predict_win_probability(team_a: str, team_b: str, team_elos: DataFrame, season_win_loss_averages: DataFrame) -> tuple[float | None, float | None]:
    """
    Predicts the winning probability of team A against team B.
    """
    print(season_win_loss_averages)
    team_a_row = team_elos[team_elos['team'] == team_a]
    team_b_row = team_elos[team_elos['team'] == team_b]

    if team_a_row.empty or team_b_row.empty:
        print(f"Error: Could not find one of the teams in the Elo table")
        return None, None

    elo_a = team_a_row['elo'].item()
    elo_b = team_b_row['elo'].item()

    prob_a_wins, prob_b_wins = calculate_expected_result(elo_a, elo_b)
    return prob_a_wins, prob_b_wins