import math
import numpy as np
import pandas as pd

from config import WEIGHT, K_FACTOR


def calculate_expected_result(elo_a: float, elo_b: float) -> tuple[float, float]:
    """
    Takes the Elo ratings of two teams and returns the probability of each team winning.
    Formula: E_A = 1 / (1 + 10((R_B − R_A)/400))
    :return: tuple[team_a: float, team_b: float]
    """
    team_a = 1 / (1 + math.pow(10, (elo_b - elo_a) / WEIGHT))
    team_b = 1 - team_a
    return team_a, team_b


def get_actual_result(result: str) -> float:
    """
    Gets the numerical interpretation of game outcome:
    1 for home team win, 0 for home team loss, 0.5 for a draw.
    """
    actual = 0

    if result == 'H':
        actual = 1
    elif result == 'D':
        actual = 0.5

    return actual


def update_elo(elo_home: float, elo_away: float, result: str) -> tuple[float, float]:
    """
    Updates the Elo ratings after a game.
    Formula: R_A′ = R_A + K(S_A − E_A)
    """
    expected_result, _ = calculate_expected_result(elo_home, elo_away)
    actual_result = get_actual_result(result)
    elo_change = K_FACTOR * (actual_result - expected_result)
    new_elo_home = elo_home + elo_change
    new_elo_away = elo_away - elo_change

    return np.round(new_elo_home, 3), np.round(new_elo_away, 3)


def apply_mean_reversion(season_data: pd.DataFrame, regression_factor: float = 0.2, mean_elo: float = 1500):
    """
    Applies the mean reversion to the Elo ratings at the end of each season to gradually pull
    back towards a league average.
    Formula: new_elo = (old_elo * (1 - regression_factor)) + (mean_elo * regression_factor)
    """
    season_data_copy = season_data.copy()
    season_data_copy['elo'] = (season_data_copy['elo'] * (1 - regression_factor)) + (mean_elo * regression_factor)

    return season_data_copy