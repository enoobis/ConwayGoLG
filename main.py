import tkinter as tk
import numpy as np
import random

# Define the size of the grid
GRID_SIZE = 50

# Define the colors
BG_COLOR = "#0d1117"
CELL_COLOR = "#c9d1d9"

# Create a random initial grid
def create_grid():
    return np.random.choice([0, 1], size=(GRID_SIZE, GRID_SIZE), p=[0.7, 0.3])

# Update the grid according to the rules of the game
def update_grid(grid):
    new_grid = np.zeros_like(grid)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            # Count the number of neighbors
            neighbors = np.sum(grid[max(0, i-1):min(i+2, GRID_SIZE), max(0, j-1):min(j+2, GRID_SIZE)]) - grid[i, j]
            # Apply the rules
            if grid[i, j] == 1 and (neighbors == 2 or neighbors == 3):
                new_grid[i, j] = 1
            elif grid[i, j] == 0 and neighbors == 3:
                new_grid[i, j] = 1
    return new_grid

# Create the GUI
class GameOfLifeGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Conway's Game of Life Generator")
        self.master.configure(bg=BG_COLOR)
        self.grid = create_grid()
        self.cell_size = 10
        self.cells = []
        self.create_cells()
        self.running = False
        self.create_buttons()
    
    # Create the cells
    def create_cells(self):
        for i in range(GRID_SIZE):
            row = []
            for j in range(GRID_SIZE):
                cell = tk.Canvas(self.master, width=self.cell_size, height=self.cell_size, bg=BG_COLOR, highlightthickness=0)
                cell.grid(row=i, column=j)
                row.append(cell)
            self.cells.append(row)
        self.update_cells()
    
    # Update the cells
    def update_cells(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.grid[i, j] == 1:
                    self.cells[i][j].configure(bg=CELL_COLOR)
                else:
                    self.cells[i][j].configure(bg=BG_COLOR)
    
    # Toggle the running state
    def toggle_running(self):
        self.running = not self.running
        if self.running:
            self.run_button.configure(text="Stop", bg="#d73a49")
            self.run_step()
        else:
            self.run_button.configure(text="Run", bg="#2ea44f")
    
    # Run one step of the game
    def run_step(self):
        self.grid = update_grid(self.grid)
        self.update_cells()
        if self.running:
            self.master.after(100, self.run_step)
    
    # Reset the game
    def reset(self):
        self.grid = create_grid()
        self.update_cells()
    
    # Create the buttons
    def create_buttons(self):
        button_frame = tk.Frame(self.master, bg=BG_COLOR)
        button_frame.grid(row=GRID_SIZE, columnspan=GRID_SIZE, pady=10)
        self.run_button = tk.Button(button_frame, text="Run", bg="#2ea44f", fg="white", activebackground="#2ea44f", activeforeground="white", command=self.toggle_running)
        self.run_button.pack(side=tk.LEFT, padx=5)
        reset_button = tk.Button(button_frame, text="Reset", bg="#6f42c1", fg="white", activebackground="#6f42c1", activeforeground="white", command=self.reset)
        reset_button.pack(side=tk.LEFT, padx=5)

root = tk.Tk()
root.configure(bg=BG_COLOR)
gui = GameOfLifeGUI(root)
root.mainloop()