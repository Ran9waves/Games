"""A tic-tac-toe game to test my skills with Python and undust my UI and graphic designer skills :) """

import tkinter as tk
from itertools import cycle
from tkinter import font
from typing import NamedTuple

class Player(NamedTuple): 
    label:str #stores the signs X and O
    color:str #stores the color of the player

class Move(NamedTuple):
    row: int
    col: int
    label: str =""

BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="blue"),
    Player(label="O", color="green"), ###stopped here. I need to continue on step 2
)

class TicTacToeGame(tk.Tk):
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo= []
        self._current_moves = []
        self._has_winner= False
        self._winning_combos= []
        self._setup_board()
    
    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()
    
    def _get_winning_combos(self):   #defines the possible winning combinations of the game
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def is_valid_move(self,move): #in case the game has not got a winner &/or the selected move hasn't already been played
        """Returns True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner #checks if the game has a winner or not
        return no_winner and move_was_not_played
    
    def process_move(self,move):
        """Process the current move and check if it's a win"""
        row, col = move.row, move.col #gets the .row and .col coordinates from the input move
        self._current_moves[row][col] = move # assings the input move to the item at [row][col] in the list of current move
        for combo in self._winning_combos: #starts a loop over the winning combinations
            results = set(
                self._current_moves[n][m].label
                for n, m in combo
            )
            is_win = (len(results) == 1) and ("" not in results) #checks if the move is a win or not
            if is_win:
                self._has_winner = True
                self.winner_combo = combo
                break
    
    def has_winner(self):
        """Return True if the game has a winner, and False otherwise"""
        return self._has_winner
    
    def is_tied(self):
        """Return True if the game is tied, and False otherwise.
        Basically it checks it with 2 conditions : all the possible moves have been played
        and the game has no winner
        """
        no_winner = not self._has_winner
        played_moves = (
            move.label for row in self._current_moves for move in row
        )
        return no_winner and all(played_moves)
    
    def toggle_player(self):
        """Return a toggled player, so that the game can go on"""
        self.current_player = next(self._players)
    
    def reset_game(self):
        """Reset the game state to play again"""
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row,col)
        self._has_winner = False
        self.winner_combo = []     

class TicTacToeBoard(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._game = game #adds the game logic
        self._create_menu()
        self._create_board_display() #adds the display to the gameboard
        self._create_board_grid() #adds the grid of cells to the gameboard
    
    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()
    
    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self) #holds the game's grid cells
        grid_frame.pack() #places the frame object on the main window
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.board_size):
                button= tk.Button(    #creates a button for each cell
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                self._cells[button]=(row,col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )
    
    def play(self, event):
        """Handle a player's move"""
        clicked_btn = event.widget #displays the button of the board grid
        row, col= self._cells[clicked_btn]
        move = Move(row,col,self._game.current_player.label)
        if self._game.is_valid_move(move): #checks if the player move is valid or not
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg,color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)

    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._game.current_player.label)
        clicked_btn.config(fg=self._game.current_player.color)
    
    def _update_display(self,msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")
    
    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(
            label="Play Again",
            command=self.reset_board
        )
        file_menu.add_separator
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def reset_board(self):
        """Reset the game's board to play again."""
        self._game.reset_game()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button(fg="black")

def main():
    """Create the game's board and run its main loop."""
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()

if __name__ == "__main__":
    main()



    
    