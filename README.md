# 🎧 Tune Trainer by Yathansh Nagar

**Tune Trainer** is an interactive, music-based guessing game built in Python. It plays a 20-second audio snippet from your personal music collection and challenges you to guess either the song title, the artist, or the album. With built-in game modes like **Reverse** and **2.5x Speed**, animated spinning album covers, and a custom **hangman-style fail mechanic**, this game delivers a visually engaging and challenging experience.

---

## 🚀 Features

- 🎮 Multiple Game Modes: Normal, Reverse Playback, and 2.5x Speed
- 💿 Album Cover Reveal: Spins like a CD after your guess
- 🪜 Hangman-style Progression: 6 wrong guesses and you’re hanged!
- 📊 Performance Tracking: Accuracy, Streak, Score saved by name
- 🔁 Replayability: Tracks progress per player profile
- 🖼️ Supports `.mp3` music files and `.jpg`/`.png` cover art

---

## 🧱 Folder Structure

final_project/
├── music_data/ # The music folder: /Artist/Album/Song.mp3
│ └── ... # Each album has cover.jpg/png
├── hangman/ # Contains hangman_1.png to hangman_6.png
├── temp_snippets/ # Temporary .wav files created for playback
├── data/
│ └── progress.json # Auto-generated player stats
├── tune_trainer.py #  Main program (run this)
├── game_state.py # Player profile & stats logic
├── track.py # Track loading & metadata logic
├── requirements.txt # All dependencies listed here
└── README.md # You're reading it!
---

## 📦 Installation & Setup

### ✅ Requirements

- **Python 3.12.4**  
- **Windows 11** (tested and recommended)

### 📥 Dependencies

Install the required Python packages using:

```bash
pip install -r requirements.txt
```

Required packages:

pygame
pydub
pillow
ffmpeg

- Additional Notes
Ensure FFmpeg is installed and accessible in your system path (Environment Variable).

To download ffmpeg, visit "https://www.gyan.dev/ffmpeg/builds/"
Download the release build and add the "bin" foler to your system path.

- All songs must be in .mp3 format and stored in subfolders:
music_data/Artist/Album/Song.mp3

▶️ Running the Game

python tune_trainer.py
Follow the on-screen instructions to:

Enter your name

Select a game mode

Guess your way through 20-second snippets

Avoid being hanged!


🧑‍💻 Developer
Built by Yathansh Nagar for the COMP9001 Python Project Challenge.
SID - 540261626
Unikey - ynag0160