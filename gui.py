import tkinter as tk
import threading
import time
from game import TicTacToe
from player import GeniusComputerPlayer

def start_game():
    root = tk.Tk()
    root.title("Tic Tac Toe")
    root.geometry("420x550")
    root.resizable(False, False)
    ModeSelectScreen(root)
    root.mainloop()

class ModeSelectScreen:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root, bg="#e0f7fa")
        self.frame.pack(fill="both", expand=True)

        title = tk.Label(self.frame, text="Tic Tac Toe", font=('Helvetica', 24, 'bold'), bg="#e0f7fa", fg="#007acc")
        title.pack(pady=40)

        btn1 = tk.Button(self.frame, text="👥 Player vs Player", font=('Arial', 16), bg="#007acc", fg="white",
                         activebackground="#005a99", command=self.start_pvp)
        btn1.pack(pady=20, ipadx=10, ipady=5)

        btn2 = tk.Button(self.frame, text="🤖 Player vs Computer", font=('Arial', 16), bg="#007acc", fg="white",
                         activebackground="#005a99", command=self.start_pvc)
        btn2.pack(pady=10, ipadx=10, ipady=5)

    def start_pvp(self):
        self.frame.destroy()
        App(self.root, ai_mode=False)

    def start_pvc(self):
        self.frame.destroy()
        App(self.root, ai_mode=True)

class App:
    def __init__(self, root, ai_mode=False):
        self.root = root
        self.game = TicTacToe()
        self.ai_mode = ai_mode
        self.ai = GeniusComputerPlayer('O') if ai_mode else None
        self.current_letter = 'X'
        self.x_wins = 0
        self.o_wins = 0
        self.ties = 0
        self.buttons = []

        self.main_frame = tk.Frame(root, bg="#e0f7fa")
        self.main_frame.pack(expand=True)

        self.status_label = tk.Label(self.main_frame, text=f"{self.current_letter}'s Turn", font=('Helvetica', 18, 'bold'),
                                     bg="#e0f7fa", fg="#007acc")
        self.status_label.pack(pady=10)

        self.score_label = tk.Label(self.main_frame, text=self.get_score_text(), font=('Helvetica', 14),
                                    bg="#e0f7fa", fg="#333")
        self.score_label.pack(pady=5)

        self.board_frame = tk.Frame(self.main_frame, bg="#e0f7fa")
        self.board_frame.pack(pady=10)
        self.build_board()

        self.restart_button = tk.Button(self.main_frame, text="🔄 Restart Game", font=('Arial', 12, 'bold'),
                                        bg="#007acc", fg="white", activebackground="#005a99",
                                        activeforeground="white", relief="flat", padx=10, pady=5,
                                        command=self.restart_game)
        self.restart_button.pack(pady=15)

    def get_score_text(self):
        return f"❌ X: {self.x_wins}    🟢 O: {self.o_wins}    🤝 Ties: {self.ties}"

    def build_board(self):
        for i in range(9):
            button = tk.Button(self.board_frame, text=' ', font=('Helvetica', 24, 'bold'), width=5, height=2,
                               bg='white', fg='black', activebackground="#b2ebf2", relief="raised",
                               command=lambda i=i: self.make_move(i))
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(button)

    def make_move(self, i):
        if self.game.board[i] == ' ' and not self.game.current_winner:
            self.game.make_move(i, self.current_letter)
            color = 'red' if self.current_letter == 'X' else 'green'
            self.buttons[i].config(text=self.current_letter, fg=color)

            if self.game.current_winner:
                self.end_round(f"🎉 {self.current_letter} Wins!")
                if self.current_letter == 'X':
                    self.x_wins += 1
                else:
                    self.o_wins += 1
                self.highlight_winner()
                self.update_scoreboard()
                return

            if not self.game.empty_squares():
                self.end_round("🤝 It's a Tie!")
                self.ties += 1
                self.update_scoreboard()
                return

            self.current_letter = 'O' if self.current_letter == 'X' else 'X'
            self.status_label.config(text=f"{self.current_letter}'s Turn")

            if self.ai_mode and self.current_letter == 'O':
                self.root.after(300, self.computer_move)

    def computer_move(self):
        square = self.ai.get_move(self.game)
        self.make_move(square)

    def highlight_winner(self):
        win_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in win_combos:
            if all(self.game.board[i] == self.current_letter for i in combo):
                for i in combo:
                    self.buttons[i].config(bg="#a5d6a7" if self.current_letter == 'O' else "#ef9a9a")
                break

    def end_round(self, message):
        self.status_label.config(text=message)
        self.disable_buttons()

    def disable_buttons(self):
        for btn in self.buttons:
            btn.config(state='disabled')

    def restart_game(self):
        self.game = TicTacToe()
        self.current_letter = 'X'
        self.status_label.config(text=f"{self.current_letter}'s Turn")
        for btn in self.buttons:
            btn.config(text=' ', state='normal', bg='white')

    def update_scoreboard(self):
        self.score_label.config(text=self.get_score_text())
