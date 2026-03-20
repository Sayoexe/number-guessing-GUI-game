import tkinter as tk
from tkinter import ttk
import random

class NumberGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Number Guessing Game")
        self.root.geometry("550x500")
        self.root.resizable(False, False)
        self.root.config(bg="#1e1e2f")

        # Game variables
        self.score = 0
        self.number = 0
        self.max_attempt = 0
        self.attempts = 0

        # -------- TITLE FRAME --------
        self.title_frame = tk.Frame(root, bg="#1e1e2f")
        self.title_frame.pack(pady=15)
        self.title_label = tk.Label(self.title_frame, text="NUMBER GUESSING GAME",
                                    font=("Comic Sans MS", 22, "bold"), fg="#f5f5f5", bg="#1e1e2f")
        self.title_label.pack()

        # -------- SCORE FRAME --------
        self.score_frame = tk.Frame(root, bg="#1e1e2f")
        self.score_frame.pack(pady=5)
        self.score_label = tk.Label(self.score_frame, text=f"Score: {self.score}",
                                    font=("Arial", 16, "bold"), fg="#00ff00", bg="#1e1e2f")
        self.score_label.pack()

        # -------- DIFFICULTY FRAME --------
        self.diff_frame = tk.Frame(root, bg="#1e1e2f")
        self.diff_frame.pack(pady=10)
        self.easy_button = tk.Button(self.diff_frame, text="EASY (1-50)", width=15, command=lambda: self.start_game('easy'),
                                     bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), activebackground="#45a049")
        self.easy_button.grid(row=0, column=0, padx=10)
        self.hard_button = tk.Button(self.diff_frame, text="HARD (1-100)", width=15, command=lambda: self.start_game('hard'),
                                     bg="#f44336", fg="white", font=("Arial", 12, "bold"), activebackground="#da190b")
        self.hard_button.grid(row=0, column=1, padx=10)

        # -------- FEEDBACK FRAME --------
        self.feedback_label = tk.Label(root, text="", font=("Arial", 14, "bold"), fg="#ffd700", bg="#1e1e2f")
        self.feedback_label.pack(pady=15)

        # -------- GUESS FRAME --------
        self.guess_frame = tk.Frame(root, bg="#1e1e2f")
        self.guess_entry = tk.Entry(self.guess_frame, font=("Arial", 14), width=10)
        self.guess_button = tk.Button(self.guess_frame, text="GUESS", command=self.make_guess, font=("Arial", 12, "bold"),
                                      bg="#2196F3", fg="white", width=10, activebackground="#0b7dda")

        # -------- ATTEMPTS FRAME --------
        self.attempt_label = tk.Label(root, text="", font=("Arial", 12), fg="#ff6347", bg="#1e1e2f")
        self.attempt_label.pack(pady=5)
        self.attempts_bar = ttk.Progressbar(root, length=350, maximum=100, mode='determinate')
        self.attempts_bar.pack(pady=10)

        # -------- ENDGAME FRAME --------
        self.endgame_frame = tk.Frame(root, bg="#1e1e2f")

    # ---------- START GAME ----------
    def start_game(self, level):
        if level == 'easy':
            self.number = random.randint(1, 50)
            self.max_attempt = 7
        else:
            self.number = random.randint(1, 100)
            self.max_attempt = 5

        self.attempts = 0
        self.feedback_label.config(text=f"Game started! You have {self.max_attempt} attempts.", fg="#ffd700")
        self.update_progress()

        self.guess_frame.pack(pady=10)
        self.guess_entry.grid(row=0, column=0, padx=5)
        self.guess_button.grid(row=0, column=1, padx=5)
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()

    # ---------- UPDATE PROGRESS BAR ----------
    def update_progress(self):
        percent = int((self.attempts / self.max_attempt) * 100)
        self.attempts_bar['value'] = percent
        self.attempt_label.config(text=f"Attempts Left: {self.max_attempt - self.attempts}")

    # ---------- MAKE GUESS ----------
    def make_guess(self):
        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            self.feedback_label.config(text="⚠️ Enter a valid number!", fg="#ff4500")
            return

        self.attempts += 1
        self.update_progress()

        if guess == self.number:
            self.score += 1
            self.score_label.config(text=f"Score: {self.score}")
            self.feedback_label.config(text=f"🎉 Correct! You guessed it in {self.attempts} attempts!", fg="#00ff00")
            self.end_game(win=True)
        elif abs(guess - self.number) <= 5:
            self.feedback_label.config(text="🔥 Very Close!", fg="#ffa500")
        elif guess > self.number:
            self.feedback_label.config(text="⬆️ Too HIGH!", fg="#ff6347")
        else:
            self.feedback_label.config(text="⬇️ Too LOW!", fg="#1e90ff")

        if self.attempts >= self.max_attempt and guess != self.number:
            self.feedback_label.config(text=f"💥 GAME OVER! The number was {self.number}", fg="#ff0000")
            self.end_game(win=False)

        self.guess_entry.delete(0, tk.END)

    # ---------- ENDGAME PANEL ----------
    def end_game(self, win):
        self.guess_frame.pack_forget()
        self.attempts_bar['value'] = 100 if not win else self.attempts_bar['value']
        self.endgame_frame.pack(pady=20)
        result_text = "🎉 YOU WON!" if win else "💥 YOU LOST!"
        self.result_label = tk.Label(self.endgame_frame, text=result_text, font=("Arial", 20, "bold"),
                                     fg="#00ff00" if win else "#ff4500", bg="#1e1e2f")
        self.result_label.pack(pady=10)
        self.final_score_label = tk.Label(self.endgame_frame, text=f"Final Score: {self.score}",
                                          font=("Arial", 16), fg="#ffd700", bg="#1e1e2f")
        self.final_score_label.pack(pady=5)
        self.play_again_btn = tk.Button(self.endgame_frame, text="Play Again", font=("Arial", 12, "bold"),
                                        bg="#4CAF50", fg="white", width=12, command=self.reset_game)
        self.play_again_btn.pack(pady=5)
        self.quit_btn = tk.Button(self.endgame_frame, text="Quit", font=("Arial", 12, "bold"),
                                  bg="#f44336", fg="white", width=12, command=self.root.destroy)
        self.quit_btn.pack(pady=5)

    # ---------- RESET GAME ----------
    def reset_game(self):
        self.endgame_frame.pack_forget()
        self.feedback_label.config(text="Choose a difficulty to start a new game.", fg="#ffd700")
        self.attempts_bar['value'] = 0
        self.guess_entry.delete(0, tk.END)
        self.guess_frame.pack_forget()


# ---------- RUN GAME ----------
root = tk.Tk()
game = NumberGuessingGame(root)
root.mainloop()