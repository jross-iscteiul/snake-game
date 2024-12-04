from tkinter import *
import random

GAME_WIDTH = 1000
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


class Snake:
    def __init__(self):
        self.bodysize = BODY_PARTS
        self.coordinates = []
        self.squares = []
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        x = random.randint(0, int(GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]
        canvas.create_oval(x, y, (x + SPACE_SIZE), (y + SPACE_SIZE), fill=FOOD_COLOR, tag="food")


def next_turn(snake, food):
    x, y = snake.coordinates[0]
    match direction:
        case "up":
            y -= SPACE_SIZE
        case "down":
            y += SPACE_SIZE
        case "left":
            x -= SPACE_SIZE
        case "right":
            x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")

        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()

    snake.squares.insert(0, square)
    window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    match new_direction:
        case "left":
            if direction != "right":
                direction = new_direction
        case "right":
            if direction != "left":
                direction = new_direction
        case "up":
            if direction != "down":
                direction = new_direction
        case "down":
            if direction != "up":
                direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=('consolas', 70), text="GAME_OVER",
                       fill="red", tag="gameover")


window = Tk()
window.title("Snake Game")
window.resizable(False, False)
score = 0
direction = 'down'

# Create Score at the top

label = Label(window, text="Score:{}".format(score), font=('consolas', 40))
label.pack()

# Create canvas

canvas = Canvas(window, bg=BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
canvas.pack()

window.update()
# Centre on screen

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction("left"))
window.bind('<Right>', lambda event: change_direction("right"))
window.bind('<Up>', lambda event: change_direction("up"))
window.bind('<Down>', lambda event: change_direction("down"))
snake = Snake()
food = Food()
next_turn(snake, food)
window.mainloop()
