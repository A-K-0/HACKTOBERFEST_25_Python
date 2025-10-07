from random import choice
from turtle import *
from freegames import floor
from freegames import vector as V   

# --- Maze Layout (1 = dot, 0 = wall, 2 = empty eaten) ---
ORIGINAL_TILES = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
tiles = list(ORIGINAL_TILES)

# --- Game State ---
state = {'score': 0, 'paused': False, 'game_started': False, 'game_over': False, 'win': False}
path = Turtle(visible=False)
writer = Turtle(visible=False)
score_writer = Turtle(visible=False)
message_writer = Turtle(visible=False)
pause_button_writer = Turtle(visible=False)
restart_button_writer = Turtle(visible=False)

aim = V(0, 0)
pacman = V(100, -80)
ghosts = []
desired_aim = V(0, 0)

# Shapes
pacman_shape = ((0,0),(10,5),(10,15),(5,20),(-5,20),(-10,15),(-10,5),(-5,0))
ghost_shape = ((-10,0),(-10,15),(-5,20),(5,20),(10,15),(10,0),(5,-5),(0,0),(-5,-5))

# Helpers
def square(x, y):
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()
    for _ in range(4):
        path.forward(20)
        path.left(90)
    path.end_fill()

def offset(point):
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    return int(x + y * 20)

def valid(point):
    index = offset(point)
    if tiles[index] == 0:
        return False
    index_check = offset(point + 19)
    if tiles[index_check] == 0:
        return False
    return point.x % 20 == 0 or point.y % 20 == 0

def world():
    bgcolor('black')
    path.color('blue')
    for index, tile in enumerate(tiles):
        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)
            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(3, 'white')

def draw_actors():
    clearstamps()
    penup()
    goto(pacman.x + 10, pacman.y + 10)
    shape("pacman")
    color("yellow")
    stamp()
    for point, _, col in ghosts:
        goto(point.x + 10, point.y + 10)
        shape("ghost")
        color(col)
        stamp()
    update()

# Pause
def toggle_pause(x=None, y=None):
    if state['game_over'] or not state['game_started'] or state['win']:
        return
    state['paused'] = not state['paused']
    if state['paused']:
        message_writer.goto(0, 40)
        message_writer.color("yellow")
        message_writer.write("PAUSED", align="center", font=("Comic Sans MS", 32, "bold"))
    else:
        message_writer.clear()
        game_loop()

# Ghost move counter
ghost_counter = 0

def game_loop():
    global ghost_counter
    if state['game_over'] or state['paused'] or not state['game_started'] or state['win']:
        return

    # Pacman move
    if valid(pacman + desired_aim):
        aim.x, aim.y = desired_aim.x, desired_aim.y
    if valid(pacman + aim):
        pacman.move(aim)

    # Eat dots
    index = offset(pacman)
    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        score_writer.clear()
        score_writer.write(f"Score: {state['score']}", align="center", font=("Comic Sans MS", 18, "normal"))
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        path.up()
        path.goto(x, y)
        path.color('blue')
        square(x, y)
        if 1 not in tiles:
            state['win'] = True
            flash_win_message()
            return

    # Ghosts move slower
    ghost_counter += 1
    if ghost_counter % 2 == 0:   # every second frame
        for point, course, _ in ghosts:
            options = [V(20,0), V(-20,0), V(0,20), V(0,-20)]
            reverse = course * -1
            valid_moves = [opt for opt in options if valid(point + opt) and opt != reverse]
            if not valid_moves:
                valid_moves = [opt for opt in options if valid(point + opt)]
            if valid_moves:
                if choice([True, False]):   # 50% random
                    best_move = choice(valid_moves)
                else:
                    best_move = course
                    min_dist = float('inf')
                    for move in valid_moves:
                        next_pos = point + move
                        dist = abs(pacman.x - next_pos.x) + abs(pacman.y - next_pos.y)
                        if dist < min_dist:
                            min_dist = dist
                            best_move = move
                course.x, course.y = best_move.x, best_move.y
            if valid(point + course):
                point.move(course)

    draw_actors()

    # Collision check (reduced radius)
    for point, _, __ in ghosts:
        if abs(pacman - point) < 10:
            state['game_over'] = True
            flash_game_over()
            return

    ontimer(lambda: game_loop(), 180)

def flash_game_over(show=True):
    if state['win'] or not state['game_over']:
        message_writer.clear()
        return
    if show:
        message_writer.goto(0, 40)
        message_writer.color("red")
        message_writer.write("GAME OVER", align="center", font=("Comic Sans MS", 32, "bold"))
    else:
        message_writer.clear()
    ontimer(lambda: flash_game_over(not show), 500)

def flash_win_message(show=True):
    if not state['win']:
        message_writer.clear()
        return
    if show:
        message_writer.goto(0, 40)
        message_writer.color("green")
        message_writer.write("YOU WIN!", align="center", font=("Comic Sans MS", 32, "bold"))
    else:
        message_writer.clear()
    ontimer(lambda: flash_win_message(not show), 500)

def change(x, y):
    desired_aim.x, desired_aim.y = x, y

def restart_game(x=None, y=None):
    global tiles, pacman, aim, desired_aim, ghosts, ghost_counter
    state['score'] = 0
    state['paused'] = False
    state['game_over'] = False
    state['win'] = False
    state['game_started'] = True
    ghost_counter = 0
    message_writer.clear()
    score_writer.clear()
    pacman = V(100, -80)
    aim = V(0, 0)
    desired_aim = V(0, 0)
    # Ghosts in corners
    start_positions = [(-180, 160), (180, 160), (-180, -160), (180, -160)]
    colors = ["red", "cyan", "pink", "orange"]
    ghosts = [[V(x, y), V(choice([-20, 20]), 0) if choice([True, False]) else V(0, choice([-20, 20])), c]
              for (x, y), c in zip(start_positions, colors)]
    tiles = list(ORIGINAL_TILES)
    path.clear()
    world()
    draw_actors()
    score_writer.write(f"Score: {state['score']}", align="center", font=("Comic Sans MS", 18, "normal"))
    game_loop()

def handle_click(x, y):
    if -30 < x < 130 and -255 < y < -225:
        toggle_pause()
    elif 140 < x < 240 and -255 < y < -225:
        restart_game()

# --- Setup ---
setup(440, 500, 370, 0)
hideturtle()
tracer(False)
register_shape("pacman", pacman_shape)
register_shape("ghost", ghost_shape)

writer.penup()
writer.goto(0, 200)
writer.color("yellow")
writer.write("PAC-MAN", align="center", font=("Comic Sans MS", 50, "bold"))

score_writer.penup()
score_writer.color("white")
score_writer.goto(-150, -240)

message_writer.penup()
pause_button_writer.penup()
pause_button_writer.color("white")
pause_button_writer.goto(80, -240)
pause_button_writer.write("Pause [P]", align="center", font=("Comic Sans MS", 14, "normal"))
restart_button_writer.penup()
restart_button_writer.color("white")
restart_button_writer.goto(190, -240)
restart_button_writer.write("Restart [R]", align="center", font=("Comic Sans MS", 14, "normal"))

listen()
onkey(lambda: change(20, 0), 'Right')
onkey(lambda: change(-20, 0), 'Left')
onkey(lambda: change(0, 20), 'Up')
onkey(lambda: change(0, -20), 'Down')
onkey(lambda: restart_game(), 'r')
onkey(lambda: toggle_pause(), 'p')

screen = getscreen()
screen.onclick(handle_click)

restart_game()
done()
