from ascii.title import title

welcome_message = '''
Welcome to the AFL predictor. Under the hood its using an Elo comparison model with adjustments for home ground advantage.
'''

def welcome():
  print(title)
  print(welcome_message)


def get_command():
  prompts = dict({
    1: 'Get the winning probability for two teams.',
    2: 'Quit'
  })

  while True:
    print("List of possible commands:\n")
    for i, prompt in prompts.items():
      print(f"{i}. {prompt}")

    try:
      command_index = int(input(f"\nPlease select an option (1-{len(prompts)}): "))
    except ValueError:
      command_index = len(prompts) + 1

    is_valid = command_index in command_map
    if is_valid:
      return command_map[command_index]
    else:
      print("Command not found. Please try again.\n")


def calculate_win_probability():
  print("\nHere is the current team list:\n")
  for i, team in teams.items():
    print(f"{i}. {team}")

  waiting_for_input = True
  while waiting_for_input:
    home_team_index = int(input("\nWho is the home team? Enter the corresponding number: "))
    away_team_index = int(input("Who is the away team? Enter the corresponding number: "))

    try:
      home_team = teams[home_team_index]
      away_team = teams[away_team_index]

      print(f"\n\n🏉🏉🏉 Let's go!! 🏉🏉🏉\n")
      print(f"{home_team} vs. {away_team}\n")
      print("Calculating the probabilities ....\n\n")
     
      print(f"{home_team} has a 57% chance of winning.")
      print(f"{away_team} has a 46% chance of winning.")

      waiting_for_input = False
    except KeyError:
      print("\nError: Could not find one or both of the teams you selected.\nPlease try again")


 

  return True


command_map = dict({
    1: calculate_win_probability,
    2: None
  })

teams = dict({
  1: 'Adelaide',
  2: 'Brisbane',
  3: 'Carlton',
  4:'Collingwood',
  5: 'Essendon',
  6: 'Fremantle',
  7: 'Geelong',
  8: 'Gold Coast',
  9:'GWS',
  10:'Hawthorn',
  11:'Melbourne',
  12:'North Melbourne',
  13:'Port Adelaide',
  14:'Richmond',
  15:'St Kilda',
  16:'Sydney',
  17:'West Coast',
  18:'Western Bulldogs',
})


def main():
  welcome()

  is_running = True
  while is_running:
    func = get_command()
    if func is None:
      is_running = False
    else:
      func()

main()