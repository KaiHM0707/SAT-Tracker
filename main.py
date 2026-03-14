import json
import matplotlib.pyplot as plt

FILE = "scores.json"


def load_scores():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_scores(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_score():
    test_number = input("SAT Practice Test Number: ")
    
    try:
        score = int(input("Total Score: "))
    except:
        print("Invalid score. Please enter a number.")
        return

    data = load_scores()

    data.append({
        "test": test_number,
        "score": score
    })

    save_scores(data)

    print("Score saved!")


def show_scores():
    data = load_scores()

    if not data:
        print("No scores recorded yet.")
        return

    print("\nScore History")
    print("----------------")

    for entry in data:
        print(f"Test {entry['test']} → {entry['score']}")


def show_graph():
    data = load_scores()

    if not data:
        print("No scores to graph.")
        return

    tests = [entry["test"] for entry in data]
    scores = [entry["score"] for entry in data]

    plt.plot(tests, scores, marker="o")

    plt.title("SAT Score Progress")
    plt.xlabel("Practice Test")
    plt.ylabel("Score")

    plt.show()


def main():

    while True:

        print("\nSAT Analyzer")
        print("1. Add score")
        print("2. View scores")
        print("3. Show graph")
        print("4. Exit")

        choice = input("Select option: ")

        if choice == "1":
            add_score()

        elif choice == "2":
            show_scores()

        elif choice == "3":
            show_graph()

        elif choice == "4":
            print("Good luck on the SAT!")
            break

        else:
            print("Invalid option.")


main()