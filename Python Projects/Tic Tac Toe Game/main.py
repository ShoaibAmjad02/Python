import tkinter as tk
from tkinter import messagebox
import random

root = tk.Tk()
root.title("Tic Tac Toe Game")
root.geometry("360x420")
root.configure(bg="#FFFFFF")

buttons = []
user = "X"
computer = "O"

# ---------------- WIN CHECK ----------------
def check_winner(board):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]

    for a,b,c in wins:
        if board[a] == board[b] == board[c] != "":
            return board[a]
    return None


# ---------------- GET BOARD STATE ----------------
def get_board():
    return [btn["text"] for btn in buttons]


# ---------------- DISABLE BOARD ----------------
def disable():
    for b in buttons:
        b.config(state="disabled")


# ---------------- COMPUTER MOVE ----------------
def computer_move():
    board = get_board()

    empty = [i for i in range(9) if board[i] == ""]
    if not empty:
        return

    move = random.choice(empty)
    buttons[move].config(text=computer, fg="lime")

    winner = check_winner(get_board())
    if winner:
        messagebox.showinfo("Game Over", "💻 Computer Wins!")
        disable()
    elif "" not in get_board():
        messagebox.showinfo("Game Over", "🤝 Draw!")


# ---------------- USER CLICK ----------------
def click(i):
    if buttons[i]["text"] == "":
        buttons[i].config(text=user, fg="red")

        winner = check_winner(get_board())
        if winner:
            messagebox.showinfo("Game Over", "🎉 You Win!")
            disable()
            return
        elif "" not in get_board():
            messagebox.showinfo("Game Over", "🤝 Draw!")
            return

        root.after(300, computer_move)


# ---------------- RESET GAME ----------------
def reset():
    for b in buttons:
        b.config(text="", state="normal")


# ---------------- UI ----------------
title = tk.Label(root, text="User vs Computer", font=("Arial", 18, "bold"),
                 fg="white", bg="#1e1e2f")
title.pack(pady=10)

frame = tk.Frame(root, bg="#1e1e2f")
frame.pack()

for i in range(9):
    btn = tk.Button(
        frame,
        text="",
        font=("Arial", 20, "bold"),
        width=5,
        height=2,
        bg="#ffffff",
        fg="white",
        command=lambda i=i: click(i)
    )
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(btn)

reset_btn = tk.Button(
    root,
    text="Restart",
    font=("Arial", 14),
    bg="#ffcc00",
    command=reset
)
reset_btn.pack(pady=15)

root.mainloop()