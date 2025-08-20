from datetime import datetime
import pandas as pd
from colorama import Fore, Style

from ascii.title import title
from config import WEIGHT
from elo import apply_mean_reversion, calculate_elo_bonus
from predict import predict_win_probability
from scraping import get_season_results
from stats import initialise_stats_table, update_stats_table


welcome_message = '''
Welcome to the AFL predictor. Under the hood it's using an Elo comparison model with adjustments for home ground advantage.
'''

def welcome():
    print(Fore.BLUE + Style.BRIGHT + title)
    print(Fore.CYAN + welcome_message + Style.RESET_ALL)


def get_command(command_map):
    prompts = dict({
        1: 'Get the winning probability for two teams',
        2: 'Show the current Elo stats table',
        3: 'Refresh the statistical data',
        4: 'Quit'
    })

    while True:
        print(Fore.CYAN + Style.BRIGHT + "List of possible commands:\n" + Style.RESET_ALL)
        for i, prompt in prompts.items():
            print(Fore.BLUE + f"{i}: " + Style.RESET_ALL + f"{prompt}")

        try:
            command_index = int(input(Fore.YELLOW + Style.BRIGHT + f"\nPlease select an option (1-{len(prompts)}): " + Style.RESET_ALL))
        except ValueError:
            command_index = len(prompts) + 1

        is_valid = command_index in command_map
        if is_valid:
            return command_map[command_index]
        else:
            print("Command not found. Please try again.\n")


def calculate_win_probability(final_stats_table, home_elo_bonus):
    # Retrieve the teams list from stats table, sorted alphabetically
    teams_list = sorted(final_stats_table['team'].unique())
    teams_dict = {i + 1: team for i, team in enumerate(teams_list)}

    print(Fore.CYAN + Style.BRIGHT + "\nHere is the current team list:\n" + Style.RESET_ALL)
    for i, team in teams_dict.items():
        print(Fore.BLUE + f"{i}: " + Style.RESET_ALL + f"{team}")

    waiting_for_input = True
    while waiting_for_input:
        try:
            home_team_index = int(input(Fore.YELLOW + "\nWho is the home team? Enter the corresponding number: " + Style.RESET_ALL))
            away_team_index = int(input(Fore.YELLOW + "Who is the away team? Enter the corresponding number: " + Style.RESET_ALL))

            home_team = teams_dict[home_team_index]
            away_team = teams_dict[away_team_index]

            print(f"\n\n{Fore.GREEN}🏉🏉🏉 Let's go!! 🏉🏉🏉{Style.RESET_ALL}\n")
            print(f"{Fore.MAGENTA}{home_team} vs. {away_team}{Style.RESET_ALL}\n")
            print("Calculating the probabilities ....\n\n")

            home_prob, away_prob = predict_win_probability(home_team, away_team, final_stats_table, home_elo_bonus)

            if home_prob is not None:
                print(f"{home_team} has a {home_prob:.2%} chance of winning.")
                print(f"{away_team} has a {away_prob:.2%} chance of winning.\n")
            
            waiting_for_input = False
        except KeyError:
            print(Fore.RED + "\nError: Could not find one or both of the teams you selected.\nPlease try again" + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "\nError: Invalid input. Please enter a number.\n" + Style.RESET_ALL)

    return True


def run_elo_model(seasons: list[int], reload_data=False) -> tuple[pd.DataFrame | None, float | None]:
    """
    Runs the full Elo model calculation pipeline.
    """
    seasons_data = get_season_results(seasons, reload=reload_data)
    
    # Handle the case where no data is returned
    if not seasons_data:
        print(Fore.RED + "Error: No season data was loaded. Cannot run the model." + Style.RESET_ALL)
        return None, None

    all_season_df = pd.concat(seasons_data.values(), ignore_index=True)
    home_win_count = (all_season_df['home_score'] > all_season_df['away_score']).sum()
    total_games = len(all_season_df)
    overall_home_win_percentage = home_win_count / total_games
    HOME_ELO_BONUS = calculate_elo_bonus(overall_home_win_percentage, weight=WEIGHT)
    
    stats = initialise_stats_table(seasons_data)
    for year in sorted(seasons_data.keys()):
        if year > min(seasons_data.keys()):
            stats = apply_mean_reversion(stats)
        stats = update_stats_table(stats, seasons_data[year], HOME_ELO_BONUS)
    
    final_stats_table = stats.sort_values(by='elo', ascending=False).reset_index(drop=True)

    return final_stats_table, HOME_ELO_BONUS


def main():
    welcome()

    # --- Run the Elo Calculation once at startup ---
    current_year = datetime.now().year
    seasons = [current_year - i for i in range(0, 3)]
    seasons.reverse()
   
    final_stats_table, HOME_ELO_BONUS = run_elo_model(seasons)
    
    # Handle the case of no data on startup
    if final_stats_table is None:
        print(Fore.RED + Style.BRIGHT + "Unable to load data. Exiting." + Style.RESET_ALL)
        return
    # --- End of Elo Calculation ---

    # --- Start the CLI loop ---
    def reload_data_and_recalculate():
        nonlocal final_stats_table, HOME_ELO_BONUS
        print(Fore.YELLOW + "Reloading data and recalculating Elo ratings..." + Style.RESET_ALL)
        final_stats_table, HOME_ELO_BONUS = run_elo_model(seasons, reload_data=True)
        print(Fore.GREEN + "Data refreshed and model recalculated." + Style.RESET_ALL)
        # Return True to keep the loop running
        return True

    command_map = {
        1: lambda: calculate_win_probability(final_stats_table, HOME_ELO_BONUS),
        2: lambda: print('\n', final_stats_table.to_markdown(), '\n'),
        3: reload_data_and_recalculate,
        4: None
    }
    
    is_running = True
    while is_running:
        func = get_command(command_map)
        if func is None:
            is_running = False
        else:
            func()

if __name__ == '__main__':
    main()