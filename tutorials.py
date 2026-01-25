# Tutorial State Variables
tutorial_step = 0            # Integer: stores current tutorial stage
tutorial_completed = False   # Boolean: tracks if tutorial is finished

# tutorial content (can be expanded later)
tutorial_steps = [
    "Welcome to the Crypto Prediction App!",
    "This app predicts cryptocurrency trends using historical data.",
    "You can select different coins like BTC, ETH, or SOL.",
    "Predictions are based on machine learning models.",
    "You can view charts, predictions, and confidence levels.",
    "Tutorial complete! You're ready to use the app."
]

# tutorial functions

def show_step():
    """Displays the current tutorial step."""
    global tutorial_step
    print(f"\nStep {tutorial_step + 1}/{len(tutorial_steps)}")
    print(tutorial_steps[tutorial_step])


def next_step():
    """Allows user to progress to next step."""
    global tutorial_step, tutorial_completed

    if tutorial_step < len(tutorial_steps) - 1:
        tutorial_step += 1
        show_step()
    else:
        tutorial_completed = True
        print("\n Tutorial completed!")


def previous_step():
    """Returns user to previous step."""
    global tutorial_step

    if tutorial_step > 0:
        tutorial_step -= 1
        show_step()
    else:
        print("\n You are already at the beginning of the tutorial.")


def skip_tutorial():
    """Allows user to skip tutorial."""
    global tutorial_completed
    tutorial_completed = True
    print("\n Tutorial skipped. Redirecting to dashboard...")


def restart_tutorial():
    """Restarts tutorial from the beginning."""
    global tutorial_step, tutorial_completed
    tutorial_step = 0
    tutorial_completed = False
    print("\n Tutorial restarted.")
    show_step()


def exit_tutorial():
    """Exits tutorial mode and returns to dashboard."""
    print("\n Exiting tutorial. Returning to dashboard...")



#tutorial controller loop

def run_tutorial():
    """Main tutorial loop."""
    show_step()

    while not tutorial_completed:
        print("\nOptions:")
        print("1 - Next step")
        print("2 - Previous step")
        print("3 - Skip tutorial")
        print("4 - Restart tutorial")
        print("5 - Exit tutorial")

        choice = input("Choose an option: ")

        if choice == "1":
            next_step()
        elif choice == "2":
            previous_step()
        elif choice == "3":
            skip_tutorial()
        elif choice == "4":
            restart_tutorial()
        elif choice == "5":
            exit_tutorial()
            break
        else:
            print("Invalid option. Try again.")

# app entry point

if __name__ == "__main__":
    if not tutorial_completed:
        run_tutorial()
    else:
        print("Welcome back! Tutorial already completed.")
