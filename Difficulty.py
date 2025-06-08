difficulties = {
    "1": 0.2,
    "2": 0.1,
    "3": 0.05
}

class Difficults:

    def choose_difficulty(self):
        print("Choose Difficulty:")
        print("1 - Easy")
        print("2 - Normal")
        print("3 - Hard")
        while True:
            choice = input("Your choice: ")
            if choice in difficulties:
                return difficulties[choice]
            print("Invalid choice.")
