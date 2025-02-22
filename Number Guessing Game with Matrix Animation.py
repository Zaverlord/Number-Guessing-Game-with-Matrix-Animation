import tkinter as tk
import random
import time
import threading
from tkinter import Canvas
from ttkthemes import ThemedTk

# Generate a random number
random_number = random.randint(1, 100)
turns = 0

def check_guess(event=None):
    global turns
    try:
        user_guess = int(entry.get())
        turns += 1
        entry.delete(0, tk.END)  # Clear the entry field after guessing
        if user_guess == random_number:
            result_label.config(text=f"You won! It took you {turns} turns.", foreground="#00FF00")
            guess_button.config(state=tk.DISABLED)
            draw_face(canvas, smile=True)
        elif user_guess < random_number:
            result_label.config(text="Too low! Try a higher number.", foreground="#00FF00")
            draw_face(canvas, smile=False)
        else:
            result_label.config(text="Too high! Try a lower number.", foreground="#00FF00")
            draw_face(canvas, smile=False)
    except ValueError:
        result_label.config(text="Invalid input! Please enter a number.", foreground="#FF0000")
        entry.delete(0, tk.END)  # Clear invalid input

def reset_game():
    global random_number, turns
    random_number = random.randint(1, 100)
    turns = 0
    entry.delete(0, tk.END)
    result_label.config(text="Guess a number between 1 and 100.", foreground="#00FF00")
    guess_button.config(state=tk.NORMAL)
    canvas.delete("all")  # Clear animation
    threading.Thread(target=matrix_animation, args=(canvas, 500, 200), daemon=True).start()

def draw_face(canvas, smile):
    canvas.delete("all")
    width, height = 500, 200
    eye_offset = random.randint(15, 25)
    mouth_variation = random.randint(10, 20)
    
    canvas.create_oval(width//2-40, height//2-40, width//2+40, height//2+40, outline="#00FF00", width=2)
    canvas.create_oval(width//2-20-eye_offset, height//2-15, width//2-10-eye_offset, height//2-5, fill="#00FF00")
    canvas.create_oval(width//2+10+eye_offset, height//2-15, width//2+20+eye_offset, height//2-5, fill="#00FF00")
    if smile:
        canvas.create_arc(width//2-20-mouth_variation, height//2, width//2+20+mouth_variation, height//2+20, start=0, extent=-180, style=tk.ARC, outline="#00FF00", width=2)
    else:
        canvas.create_arc(width//2-20-mouth_variation, height//2+10, width//2+20+mouth_variation, height//2+30, start=0, extent=180, style=tk.ARC, outline="#00FF00", width=2)

def matrix_animation(canvas, width, height):
    symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    drops = [0] * (width // 10)
    while True:
        canvas.delete("all")
        for i in range(len(drops)):
            text = random.choice(symbols)
            x = i * 10
            y = drops[i] * 10
            canvas.create_text(x, y, text=text, fill="#00FF00", font=("Courier", 10))
            if y > height and random.random() > 0.975:
                drops[i] = 0
            drops[i] += 1
        time.sleep(0.1)
        canvas.update()

# Create main window with a modern theme
root = ThemedTk(theme="equilux")
root.title("Number Guessing Game")
root.geometry("500x500")
root.configure(bg="#000000")

# Matrix animation canvas
canvas = Canvas(root, width=500, height=200, bg="#000000", highlightthickness=0)
canvas.pack()
thr = threading.Thread(target=matrix_animation, args=(canvas, 500, 200), daemon=True)
thr.start()

# Widgets
frame = tk.Frame(root, bg="#000000")
frame.pack(pady=10)

label = tk.Label(frame, text="Enter a number between 1 and 100:", fg="#00FF00", bg="#000000", font=("Arial", 14, "bold"))
label.pack()

entry = tk.Entry(frame, font=("Arial", 14), justify="center", bg="#222222", fg="#00FF00", insertbackground="#00FF00")
entry.pack(pady=5)
entry.bind("<Return>", check_guess)

guess_button = tk.Button(frame, text="Guess", command=check_guess, bg="#111111", fg="#00FF00", font=("Arial", 12, "bold"))
guess_button.pack(pady=5)

reset_button = tk.Button(frame, text="Reset", command=reset_game, bg="#111111", fg="#00FF00", font=("Arial", 12, "bold"))
reset_button.pack(pady=5)

result_label = tk.Label(frame, text="Guess a number between 1 and 100.", fg="#00FF00", bg="#000000", font=("Arial", 12, "bold"))
result_label.pack(pady=5)

# Run the application
root.mainloop()
