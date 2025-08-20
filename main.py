from datetime import datetime
import pandas as pd

from config import WEIGHT
from elo import apply_mean_reversion, calculate_elo_bonus
from predict import predict_win_probability
from scraping import get_season_results
from stats import initialise_stats_table, update_stats_table


if __name__ == '__main__':
    current_year = datetime.now().year
    seasons = [current_year - i for i in range(0, 3)]
    seasons.reverse()

    seasons_data = get_season_results(seasons)
    all_season_df = pd.concat(seasons_data.values(), ignore_index=True)

    # Calculate overall home win percentage on the combined data
    home_win_count = (all_season_df['home_score'] > all_season_df['away_score']).sum()
    total_games = len(all_season_df)

    overall_home_win_percentage = home_win_count / total_games
    HOME_ELO_BONUS = calculate_elo_bonus(overall_home_win_percentage, weight=WEIGHT)
    print(f"Overall Home Win Percentage: {overall_home_win_percentage:.2%}")
    print(f"Calculated Home Elo Bonus: {HOME_ELO_BONUS:.2f} points")

    stats = initialise_stats_table(seasons_data)
    for year in sorted(seasons_data.keys()):
        print(f"Processing season: {year}")

        # Apply mean reversion to all PREVIOUS years
        if year > min(seasons_data.keys()):
            stats = apply_mean_reversion(stats)

        stats = update_stats_table(stats, seasons_data[year], HOME_ELO_BONUS)

    print(stats)
    home_team_name = 'Essendon'
    away_team_name = 'Western Bulldogs'

    home_prob, away_prob = predict_win_probability(home_team_name, away_team_name, stats, HOME_ELO_BONUS)
    if home_prob is not None:
        print(f"Prediction for {home_team_name} vs {away_team_name}:")
        print(f"  {home_team_name} wins: {home_prob:.2%}")
        print(f"  {away_team_name} wins: {away_prob:.2%}")
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
