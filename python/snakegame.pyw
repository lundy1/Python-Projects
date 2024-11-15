import tkinter as tk
from tkinter import ttk
from random import choice

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.root.bind("<KeyPress>", self.on_key_press)
        self.board = tk.Canvas(root, width=400, height=400, bg="black")
        self.board.grid(row=0, column=0, padx=20, pady=20)
        self.snake = [(200, 200)]
        self.food = None
        self.food_id = None
        self.direction = "Right"
        self.new_direction = "Right"
        self.score = 0
        self.running = True
        self.init_game()

    def init_game(self):
        self.board.delete(tk.ALL)
        self.snake = [(200, 200)]
        self.direction = "Right"
        self.new_direction = "Right"
        self.score = 0
        self.running = True
        self.create_food()
        self.update_snake()
        self.root.after(100, self.move_snake)

    def create_food(self):
        while True:
            x, y = choice(range(20, 380, 20)), choice(range(20, 380, 20))
            if (x, y) not in self.snake:
                self.food = (x, y)
                if self.food_id:
                    self.board.delete(self.food_id)
                self.food_id = self.board.create_rectangle(x, y, x+20, y+20, fill="red", outline="red")
                break

    def update_snake(self):
        self.board.delete("snake")
        for x, y in self.snake:
            self.board.create_rectangle(x, y, x+20, y+20, fill="green", outline="green", tags="snake")

    def on_key_press(self, e):
        if e.keysym in ["Up", "Down", "Left", "Right"]:
            if (self.direction == "Up" and e.keysym != "Down") or \
               (self.direction == "Down" and e.keysym != "Up") or \
               (self.direction == "Left" and e.keysym != "Right") or \
               (self.direction == "Right" and e.keysym != "Left"):
                self.new_direction = e.keysym
        elif e.keysym == "r" and not self.running:
            self.init_game()

    def move_snake(self):
        if self.running:
            self.direction = self.new_direction
            x, y = self.snake[0]
            if self.direction == "Right":
                x += 20
            elif self.direction == "Left":
                x -= 20
            elif self.direction == "Up":
                y -= 20
            elif self.direction == "Down":
                y += 20
            new_head = (x, y)

            if x < 0 or x >= 400 or y < 0 or y >= 400 or new_head in self.snake:
                self.running = False
                self.game_over()
                return

            self.snake.insert(0, new_head)
            if new_head == self.food:
                self.score += 10
                self.create_food()
            else:
                self.snake.pop()

            self.update_snake()
            self.root.after(100, self.move_snake)

    def game_over(self):
        self.board.create_text(200, 200, text=f"Game Over\nScore: {self.score}\nPress 'R' to Restart", fill="white", font=("Arial", 20))

root = tk.Tk()
game = SnakeGame(root)
root.mainloop()
