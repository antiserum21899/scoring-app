def team_input(num_of_teams = 4):
    teams = {}
    for i in range(num_of_teams):
        team = {}
        team_name = input("Please enter your team name: \n")
        team_members = input("Please enter your team members separated by a comma like so \n -- member1,member2,member3,member4,member5 -- \n")
        team_members.split(",")

        team["members"] = team_members
        team['rankings'] = []
        team['scores'] = []
        teams[team_name] = team 
    return teams

def singles_input(num_of_singles = 20):
    individuals = {}
    for i in range(num_of_singles):
        individual_name = input("Please enter your name: \n")
        individuals[individual_name] = {
            'rankings': [],
            'scores': []
        }
    return individuals

def events_selection():
    events = input("Please enter the events you would like to enter for separated by a comma like so \n -- event1,event2,event3,event4,event5 -- \n").split(",")
    print("Here are your selected events:")
    print(events)
    return events

def positioning(teams, individuals, events):
    choice_type = input("Which positions are you entering scores for? \n TEAM or INDIVIDUAL ")
    if choice_type.lower() == "team":
        print("----TEAMS----")
        for team in teams.keys():
            print(team)
    elif choice_type.lower() == "individual":
        print("----INDIVIDUALS----")
        for individual in individuals.keys():
            print(individual)
    
    participant = input("Please select a participant to enter scores for: \n")
    if participant in teams.keys():
        participant_holder = teams[participant]
    elif participant in individuals.keys():
        participant_holder = individuals[participant]
    else:
        print("Participant could not be found. Please enter a valid participant.")
        positioning()

    print("Available Events")
    for i in range(len(events)):
        print(i, events[i])

    ranking = input("Enter the positions for each event separated by a comma \n -- 1,2,3,4,5,6,7,8,9,10 -- \n").split(",")
    
    try:
        new_positions = [int(x) for x in ranking]
    except:
        print("One or more items in the string was not a number.")
        return positioning(teams, individuals, events)
    print("Your rankings:")
    print(ranking)

    scores = []
    if choice_type.lower() == "team":
        total_participants = len(teams.keys())
    elif choice_type.lower() == "individual":
        total_participants = len(individuals.keys())

    for position in new_positions:
        score = total_participants - position + 1
        scores.append(score)
    
    participant_holder["scores"] = scores
    participant_holder['rankings'] = new_positions

def show_scores(teams, individuals):
    print("----TEAM POINTS----")
    for team_name, team_dict in teams.items():
        print(team_name, team_dict['scores'])
    print("----INDIVIDUAL POINTS----")
    for individual_name, individual_dict in individuals.items():
        print(individual_name, individual_dict['scores'])

print("-----------------------------------------\nWelcome to the Tournament Scoring System\n-----------------------------------------")
print("Please select:\n[1] Data Entry\n[2] Exit")
selection = input("Please enter your choice: ")
if selection == "1":
    teams = team_input()
    singles = singles_input()
    events = events_selection()
    while True:
        print("Would you like to: \n[1] Enter Scores\n[2] Show Results\n[3] Exit")
        selection = input("Please enter your choice: ")
        if selection == "1":
            positioning(teams, singles, events)
        elif selection == "2":
            show_scores(teams, singles)
        elif selection == "3":
            print("This program is shutting down...")
            exit()
        else:
            print("You have entered an invalid choice. This program is shutting down...")
            exit()
elif selection == "2":
    print("This program is shutting down...")
    exit()
else:
    print("You have entered an invalid choice. This program is shutting down...")
    exit()
        