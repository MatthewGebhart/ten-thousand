from ten_thousand.game_logic import GameLogic
from textwrap import dedent

currently_playing = True


def intro():
    print("Welcome to Ten Thousand")
    print("(y)es to play or (n)o to decline")
    choice = input("> ")

    if choice == "n":
        print("OK. Maybe another time")
        global currently_playing
        currently_playing = False
    else:
        print(f"Starting round 1")


def default_roller(num):
    return GameLogic.roll_dice(num)


def play(roller=default_roller):
    total_score = 0
    round_number = 1
    current_dice = []
    dice_roll = []
    round_score = 0

    while currently_playing:

        print(f"Rolling {6 - len(current_dice)} dice...")
        roll = roller(6 - len(current_dice))
        roll_str = ""
        roll_list = []
        for num in roll:
            roll_str += str(num) + " "
            roll_list.append(num)
        print(f"*** {roll_str}***")

        # Check for zero score - Zilch
        if GameLogic.calculate_score(tuple(roll_list)) == 0:
            print(dedent("""
            ****************************************
            **        Zilch!!! Round over         **
            ****************************************
            """))
            current_dice = []
            dice_roll = []
            round_score = 0
            round_number = round_number + 1
            print(f"Total score is {total_score} points")
            print(f"Starting round {round_number}")
        else:
            print("Enter dice to keep, or (q)uit:")

            keep = input("> ")
            if keep == "q":
                print(f"Thanks for playing. You earned {total_score} points")
                break
            # Check for cheaters - held dice were present in roll
            while GameLogic.validate_keepers(roll_list, [int(x) for x in keep]) is False:
                print("Cheater!!! Or possibly you made a typo. Try again")
                print(f"*** {roll_str}***")
                print("Enter dice to keep, or (q)uit:")
                keep = input("> ")
            for character in keep:
                current_dice.append(int(character))
                dice_roll.append(int(character))
            round_score += GameLogic.calculate_score(tuple(dice_roll))
            # if all dice are held it gives 6 new ones because of "hot dice"
            if len(current_dice) == 6:
                print("HOT DICE, you get to roll 6 new ones")
                current_dice = []
            print(f"You have {round_score} unbanked points and {6 - len(current_dice)} dice remaining")
            print(f"(r)oll again, (b)ank your points or (q)uit:")
            choice = input("> ")
            if choice == "b":
                print(f"You banked {round_score} points in round {round_number}")
                total_score += round_score
                print(f"Total score is {total_score} points")
                current_dice = []
                round_score = 0
                round_number = round_number + 1
                print(f"Starting round {round_number}")
            if choice == "q":
                print(f"Thanks for playing. You earned {total_score} points")
                break
            dice_roll = []



if __name__ == "__main__":
    rolls = []

    def mock_roller(num):
        return rolls.pop(0) if rolls else default_roller(num)

    intro()
    play(mock_roller)