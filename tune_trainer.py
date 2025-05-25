# from track import Track
# from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from pathlib import Path
from game_state import load_player, save_player
from track import Track
import random
import time
import pygame
from pydub import AudioSegment
import tempfile
import uuid
import os
import time
import atexit
import glob
from PIL import Image, ImageTk
from PIL import ImageDraw, ImageOps

# test_track = Track(Path("music_data/Maroon 5/Red Pill Blues (Deluxe)/Don't Wanna Know (feat. Kendrick Lamar).mp3"))
# print(test_track.get_display_name())  # "Yellow by Coldplay [Parachutes]"
# print(test_track.has_cover())         # True or False

# # from game_state import GameState

# # gs = GameState()
# # gs.record_guess(True)
# # gs.record_guess(False)
# # gs.record_guess(True)
# # gs.record_guess(True)
# # print(gs)
# # Score: 3, Total: 4, Streak: 2, Best: 2, Accuracy: 75.0%

# Global variables
current_player_name = None
current_game_state = None
current_correct_answer = None
pygame.mixer.init()
HANGMAN_IMAGES = [f"hangman/hangman_{i}.png" for i in range(1, 7)]
hangman_label = None


def circular_crop(img):
    """Returns a circular-cropped version of the PIL image."""
    size = img.size
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    result = ImageOps.fit(img, size, centering=(0.5, 0.5))
    result.putalpha(mask)
    return result


def load_tracks_from_folder(base_path: Path) -> list[Track]:
    """Scan music_data folder and return a list of Track objects."""
    all_tracks = []

    for mp3_file in base_path.rglob("*.mp3"):
        try:
            track = Track(mp3_file)
            all_tracks.append(track)
        except Exception as e:
            print(f"Error loading {mp3_file.name}: {e}")

    print(f"Loaded {len(all_tracks)} tracks.")
    return all_tracks

# if __name__ == "__main__":
#     music_folder = Path("music_data")
#     tracks = load_tracks_from_folder(music_folder)
    
#     for track in tracks:
#         print(track.get_display_name(), "— Cover found:", track.has_cover())

# from your_track_loader_file import load_tracks_from_folder  # Replace with correct import path

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
TITLE = "🎧 TuneTrainer by Yathansh Nagar"
current_player_name = None
current_game_state = None
tracks = load_tracks_from_folder(Path("music_data"))
TEMP_SNIPPET_DIR = Path("temp_snippets")
TEMP_SNIPPET_DIR.mkdir(exist_ok=True)

# Main app window
def create_main_window():
    root = tk.Tk()
    root.title(TITLE)
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.resizable(False, False)
    root.configure(bg="#5ecfe6")  # dark background for modern look

    # Hangman display frame (top-right)
    hangman_frame = tk.Frame(root, bg="#5ecfe6")
    hangman_frame.place(relx=0.85, rely=0.05)  # Top-right corner

    # Title label
    title_label = tk.Label(
        root,
        text=TITLE,
        font=("Helvetica", 28, "bold"),
        fg="white",
        bg="#5ecfe6",
        pady=30
    )
    title_label.grid(row=0, column=0, columnspan=3, sticky="n", padx=20)

    # Start Game button (animated later)
    start_button = ttk.Button(
        root,
        text="Start Game",
        # command=lambda: messagebox.showinfo("Start", "Game starting soon...")  # placeholder
        command=start_game_prompt
        # style="Accent.TButton"
    )
    start_button.grid(row=1, column=1, pady=80)

    # Rescan music folder button (bottom-left)
    rescan_button = ttk.Button(
        root,
        text="Rescan Music Folder",
        command=lambda: messagebox.showinfo("Rescan", "Rescanning...")  # placeholder
    )
    rescan_button.place(x=20, y=WINDOW_HEIGHT - 50)

    # Center alignment padding
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

    return root

def start_game_prompt():
    global current_player_name, current_game_state

    name = simpledialog.askstring("Enter Your Name", "What's your name?")
    if name:
        name = name.strip().lower()
        current_player_name = name
        current_game_state = load_player(name)

        # Placeholder message
        messagebox.showinfo(
            "Welcome!",
            f"Welcome back, {name}!\n"
            f"Score: {current_game_state.score}\n"
            f"Accuracy: {current_game_state.get_accuracy():.1f}%\n"
            f"Best streak: {current_game_state.best_streak}"
        )

        # NEXT: show mode selection screen
    else:
        messagebox.showwarning("No name", "Please enter a valid name.")

    clear_main_window(app)
    show_mode_selection(app)


def clear_main_window(root):
    for widget in root.winfo_children():
        widget.destroy()

def show_mode_selection(root):
    # Title
    title_label = tk.Label(
        root,
        text="Choose Your Mode",
        font=("Helvetica", 24, "bold"),
        fg="white",
        bg="#5ecfe6",
        pady=40
    )
    title_label.pack()

    # Normal Game Button
    normal_btn = ttk.Button(
        root,
        text="🎮 Normal Game",
        # command=lambda: messagebox.showinfo("Normal Mode", "Starting Normal Game...")
        command=lambda: start_game_round(root, mode="normal")
    )
    normal_btn.pack(pady=20, ipadx=20, ipady=10)

    # Boss Mode Button
    boss_btn = ttk.Button(
        root,
        text="🔥 Think You Can Beat This App?",
        command=lambda: show_boss_mode_options(root)
    )
    boss_btn.pack(pady=10, ipadx=20, ipady=10)


# def show_mode_selection(root):
#     # Title
#     title_label = tk.Label(
#         root,
#         text="Choose Your Mode",
#         font=("Helvetica", 24, "bold"),
#         fg="white",
#         bg="#1e1e1e",
#         pady=40
#     )
#     title_label.pack()

#     # Normal Game Button
#     normal_btn = ttk.Button(
#         root,
#         text="🎮 Normal Game",
#         command=lambda: messagebox.showinfo("Normal Mode", "Starting Normal Game...")
#     )
#     normal_btn.pack(pady=20, ipadx=20, ipady=10)

#     # Boss Mode Button
#     boss_btn = ttk.Button(
#         root,
#         text="🔥 Think You Can Beat This App?",
#         command=lambda: show_boss_mode_options(root)
#     )
#     boss_btn.pack(pady=10, ipadx=20, ipady=10)

def show_boss_mode_options(root):
    clear_main_window(root)

    title_label = tk.Label(
        root,
        text="Boss Mode Activated 💀 Choose Your Challenge:",
        font=("Helvetica", 20, "bold"),
        fg="#ff4c4c",
        bg="#5ecfe6",
        pady=30
    )
    title_label.pack()

    # 2.5x Speed Mode
    speed_btn = ttk.Button(
        root,
        text="▶️ 2.5x Speed Mode",
        # command=lambda: messagebox.showinfo("2.5x Mode", "Starting Fast Playback Mode...")
        command=lambda: start_game_round(root, mode="fast")
    )
    speed_btn.pack(pady=20, ipadx=20, ipady=10)

    # Reverse Mode
    reverse_btn = ttk.Button(
        root,
        text="🔁 Reverse Mode",
        # command=lambda: messagebox.showinfo("Reverse Mode", "Starting Backwards Mode...")
        command=lambda: start_game_round(root, mode="reverse")
    )
    reverse_btn.pack(pady=10, ipadx=20, ipady=10)

def start_game_round(root, mode="normal"):
    global current_correct_answer

    clear_main_window(root)

    # Pick 1 random track for this round
    # correct_track = random.choice(tracks)
    max_attempts = 5
    attempt = 0
    temp_file_to_clean = None

    while attempt < max_attempts:
        correct_track = random.choice(tracks)
        current_track = correct_track
        temp_file_to_clean = play_snippet_with_pydub(correct_track, mode=mode)
        if temp_file_to_clean:
            break  # success
        attempt += 1

    if not temp_file_to_clean:
        messagebox.showerror("Playback Error", "Failed to play a valid track after several attempts.")
        return

    # Pick a random question type
    question_type = random.choice(["title", "artist", "album"])

    # Get correct answer
    if question_type == "title":
        current_correct_answer = correct_track.title
        question_text = "Which song is this?"
        correct = correct_track.title
        distractors = random.sample([t.title for t in tracks if t.title != correct], 3)

    elif question_type == "artist":
        current_correct_answer = correct_track.artist
        question_text = "Who is the artist of this song?"
        correct = correct_track.artist
        distractors = random.sample([t.artist for t in tracks if t.artist != correct], 3)

    elif question_type == "album":
        current_correct_answer = correct_track.album
        question_text = "Which album is this song from?"
        correct = correct_track.album
        distractors = random.sample([t.album for t in tracks if t.album != correct], 3)

    # Shuffle choices
    options = distractors + [correct]
    random.shuffle(options)

    # Play snippet from random offset (max 20 seconds)
    snippet_duration = 20000  # 20 seconds
    # pygame.mixer.music.load(correct_track.filepath)
    # pygame.mixer.music.play()

    # Stop playback after 20 seconds
    root.after(snippet_duration * 1000, pygame.mixer.music.stop)

    # Display question
    question_label = tk.Label(
        root, text=question_text, font=("Helvetica", 18), fg="white", bg="#5ecfe6"
    )
    question_label.pack(pady=20)

    # Radio button choices
    selected = tk.StringVar()
    for opt in options:
        rb = tk.Radiobutton(
            root, text=opt, variable=selected, value=opt,
            font=("Helvetica", 14),
            bg="#5ecfe6", fg="white", selectcolor="#333333",
            activebackground="#5ecfe6", activeforeground="cyan"
        )
        rb.pack(anchor="w", padx=200, pady=5)

    # Feedback label
    feedback_label = tk.Label(root, text="", font=("Helvetica", 14), fg="white", bg="#5ecfe6")
    feedback_label.pack(pady=10)

    def submit_answer():
        global cover_label
        try:
            cover_label.destroy()  # remove previous cover if exists
        except:
            pass
        answer = selected.get()
        if not answer:
            feedback_label.config(text="Please select an option.", fg="yellow")
            return

        is_correct = (answer == current_correct_answer)
        if is_correct:
            feedback_label.config(
                text=f"✔️ Correct! The answer was: {current_correct_answer}",
                fg="lightgreen"
            )
        else:
            feedback_label.config(
                text=f"❌ Wrong. Correct was: {current_correct_answer}",
                fg="red"
            )

        # Show hangman image
        # Show hangman image if wrong
        global hangman_label
        if not is_correct:
            stage_index = min(current_game_state.wrong_count, 5)  # up to 6 stages
            img_path = HANGMAN_IMAGES[stage_index]
            img = Image.open(img_path).resize((120, 120))
            hangman_img = ImageTk.PhotoImage(img)

            # Remove previous image if exists
            if hangman_label:
                hangman_label.destroy()

            hangman_label = tk.Label(root, image=hangman_img, bg="#5ecfe6")
            hangman_label.image = hangman_img
            # hangman_label.pack()

            hangman_label.place(relx=0.85, rely=0.2)  # Top-right corner

            # Game over logic
            if current_game_state.wrong_count >= 6:
                feedback_label.config(
                    text="💀 You’ve been hanged! Game Over.",
                    fg="red"
                )
                submit_btn.config(state="disabled")

        # # Create visualizer canvas
        # visualizer_canvas = tk.Canvas(root, width=400, height=100, bg="#1e1e1e", highlightthickness=0)
        # visualizer_canvas.pack(pady=20)

        # bars = []
        # num_bars = 20
        # bar_width = 15
        # bar_spacing = 5

        # for i in range(num_bars):
        #     x0 = i * (bar_width + bar_spacing)
        #     bar = visualizer_canvas.create_rectangle(x0, 100, x0 + bar_width, 100, fill="cyan")
        #     bars.append(bar)    

        # Show album cover if exists
        if correct_track.has_cover():
            cover_path = correct_track.cover_path
            try:
                # img = Image.open(cover_path)
                # img = img.resize((200, 200))
                # cover_img = ImageTk.PhotoImage(img)

                original_img = Image.open(cover_path).resize((200, 200))
                original_img = circular_crop(original_img)

                # cover_label = tk.Label(root, image=cover_img, bg="#1e1e1e")
                # cover_label.image = cover_img  # prevent garbage collection
                # cover_label.pack(pady=10)
                # # Load and resize image
                # original_img = Image.open(cover_path).resize((200, 200))
                # rotated_img = original_img
                # cover_img = ImageTk.PhotoImage(rotated_img)

                # cover_label = tk.Label(root, image=cover_img, bg="#1e1e1e")
                # cover_label.image = cover_img
                # cover_label.pack(pady=10)
                # Create a label for rotating image
                cover_img = ImageTk.PhotoImage(original_img)
                cover_label = tk.Label(root, image=cover_img, bg="#5ecfe6")
                cover_label.image = cover_img
                cover_label.pack(pady=10)

                # Start spin animation
                def spin(degree=0):
                    rotated = original_img.rotate(degree)
                    tk_img = ImageTk.PhotoImage(rotated)
                    cover_label.configure(image=tk_img)
                    cover_label.image = tk_img
                    # Repeat after 100ms
                    cover_label.after(100, spin, (degree + 5) % 360)

                spin()  # start animation
            except Exception as e:
                print(f"Error loading cover: {e}")

        # Update and save stats
        current_game_state.record_guess(is_correct)
        if current_game_state.game_over:
            feedback_label.config(
                text="💀 You’ve been hanged! Game Over.",
                fg="red"
            )
            submit_btn.config(state="disabled")
            # next_button.config(state="disabled")
            return

        save_player(current_player_name, current_game_state)

        # Show stats bar
        stats_label = tk.Label(
            root,
            text=f"Score: {current_game_state.score} | "
                 f"Streak: {current_game_state.streak} | "
                 f"Accuracy: {current_game_state.get_accuracy():.1f}%",
            font=("Helvetica", 12),
            fg="white", bg="#5ecfe6"
        )
        stats_label.pack(pady=10)

        # Continue button
        next_button = ttk.Button(
            root,
            text="Next Round",
            command=lambda: start_game_round(root, mode)
        )
        next_button.pack(pady=20)

        # Disable Submit button
        submit_btn.config(state="disabled")

        # Animate visualizer bars
        # def animate_bars():
        #     for i, bar in enumerate(bars):
        #         height = random.randint(10, 100)
        #         visualizer_canvas.coords(bar, i * (bar_width + bar_spacing), 100 - height, i * (bar_width + bar_spacing) + bar_width, 100)
        #     visualizer_canvas.after(100, animate_bars)
        # animate_bars()

    submit_btn = ttk.Button(
        root,
        text="Submit Answer",
        command=submit_answer
    )
    submit_btn.pack(pady=20)

    # Clean up temp file after playback
    # pygame.mixer.music.stop()
    # if temp_file_to_clean and os.path.exists(temp_file_to_clean):
    #     os.remove(temp_file_to_clean)

    # def clean_up_temp_file():
    #     pygame.mixer.music.stop()
    #     if temp_file_to_clean and os.path.exists(temp_file_to_clean):
    #         os.remove(temp_file_to_clean)

# Delay cleanup by 21 seconds
    # root.after(21000, clean_up_temp_file)

# def play_snippet_with_pydub(track, duration=20):
#     """Play a random 20s snippet from an MP3 file using pydub + pygame."""
#     try:
#         song = AudioSegment.from_file(track.filepath)
#         print(f"Trying to load: {track.filepath}")

#         if len(song) < duration * 1000:
#             start_ms = 0
#         else:
#             start_ms = random.randint(0, len(song) - duration * 1000)

#         snippet = song[start_ms:start_ms + duration * 1000]

#         # Export to temp wav
#         temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
#         snippet.export(temp_wav.name, format="wav")

#         # Play with pygame
#         pygame.mixer.music.load(temp_wav.name)
#         pygame.mixer.music.play()

#         # Schedule stop after exact duration
#         return temp_wav.name  # return the temp file to delete it later
    
#     except Exception as e:
#         # print(f"Error playing {track.filepath.name}: {e}")
#         print(f"[SKIP] {track.filepath.name} — {e}")
#         return None

def play_snippet_with_pydub(track, duration=20, mode="normal"):
    """Play a random 20s snippet from an MP3 using pydub + pygame."""
    try:
        print(f"Trying to load: {track.filepath}")
        song = AudioSegment.from_file(str(track.filepath))

        if len(song) < duration * 1000:
            start_ms = 0
        else:
            start_ms = random.randint(0, len(song) - duration * 1000)

        print(f"Snippet: {track.title} | Length: {len(song)//1000}s | Start at: {start_ms//1000}s")
        print(f"Exported snippet from {start_ms} to {start_ms + duration * 1000} ms | Mode: {mode}")

        snippet = song[start_ms:start_ms + duration * 1000]

        # Apply mode-specific effects
        if mode == "reverse":
            snippet = snippet.reverse()
        elif mode == "fast":
            #snippet = snippet.speedup(playback_speed=2.5)
            snippet = snippet._spawn(
                snippet.raw_data,
                overrides={
                    "frame_rate": int(snippet.frame_rate * 2.5)
                }
            ).set_frame_rate(snippet.frame_rate)


        # Generate a unique .wav path
        temp_filename = TEMP_SNIPPET_DIR / f"{uuid.uuid4().hex}.wav"
        # snippet.export(temp_filename, format="wav").close()  # flush file

        # time.sleep(0.3)  # wait for file system to flush completely

        # pygame.mixer.music.stop()  # just in case
        # pygame.mixer.music.load(str(temp_filename))
        # pygame.mixer.music.play()

        snippet.export(temp_filename, format="wav").close()
        time.sleep(0.3)

        pygame.mixer.stop()
        sound = pygame.mixer.Sound(str(temp_filename))
        sound.play()

        return str(temp_filename)

        return str(temp_filename)
    except Exception as e:
        print(f"[SKIP] {track.filepath.name} — {e}")
        return None

def clean_temp_snippets_on_exit():
    for temp_file in TEMP_SNIPPET_DIR.glob("*.wav"):
        try:
            os.remove(temp_file)
        except Exception as e:
            print(f"Error cleaning {temp_file.name}: {e}")

atexit.register(clean_temp_snippets_on_exit)

if __name__ == "__main__":
    app = create_main_window()
    app.mainloop()

# from game_state import load_player, save_player

# gs = load_player("Yathansh")
# gs.record_guess(True)
# gs.record_guess(False)
# save_player("Yathansh", gs)
# print(gs)

