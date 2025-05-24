import json
from pathlib import Path

DATA_FILE = Path("data/progress.json")

class GameState:
    def __init__(self, score=0, total_guesses=0, streak=0, best_streak=0):
        self.score = score
        self.total_guesses = total_guesses
        self.streak = streak
        self.best_streak = best_streak
        self.wrong_count = 0
        self.game_over = False

    def record_guess(self, correct: bool):
        self.total_guesses += 1
        if correct:
            self.score += 1
            self.streak += 1
            if self.streak > self.best_streak:
                self.best_streak = self.streak
        else:
            self.streak = 0
            self.wrong_count += 1
            if self.wrong_count >= 6:
                self.game_over = True
                print("Game Over! Too many wrong guesses.")

    def reset(self):
        self.score = 0
        self.total_guesses = 0
        self.streak = 0
        self.best_streak = 0

    def get_accuracy(self) -> float:
        if self.total_guesses == 0:
            return 0.0
        return (self.score / self.total_guesses) * 100

    def to_dict(self):
        return {
            "score": self.score,
            "total_guesses": self.total_guesses,
            "best_streak": self.best_streak
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            score=data.get("score", 0),
            total_guesses=data.get("total_guesses", 0),
            best_streak=data.get("best_streak", 0)
        )

    def __repr__(self):
        return (f"Score: {self.score}, Total: {self.total_guesses}, "
                f"Streak: {self.streak}, Best: {self.best_streak}, "
                f"Accuracy: {self.get_accuracy():.1f}%")


# Load player profile from file or create new
def load_player(name: str) -> GameState:
    name = name.strip().lower()

    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text("{}")  # create empty JSON

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    if name in data:
        print(f"Loaded existing profile for {name}")
        return GameState.from_dict(data[name])
    else:
        print(f"Creating new profile for {name}")
        return GameState()


# Save player profile to file
def save_player(name: str, gamestate: GameState):
    name = name.strip().lower()
    # "wrong_count": self.wrong_count

    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text("{}")

    with open(DATA_FILE, "r") as f:
        data = json.load(f)

    data[name] = gamestate.to_dict()

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
