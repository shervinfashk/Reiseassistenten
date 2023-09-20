from functions import menu, travel, decide

def main():
    print("Welcome! This CLI program tries to make your travel easier.")
    locations = travel()

    action = None
    while action != "break":
        decisions = menu()
        action = decide(decisions, locations)
        if action == "change":
            locations = travel()


main()
