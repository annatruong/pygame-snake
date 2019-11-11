import pygame
import random
pygame.init()

# Window and grid variables
width_height = 500
rows = 20
cell_width = width_height // rows

# colour variables
purple = (76,0,156)
orange = (255,92,0)
white = (255,255,255)
black = (0,0,0)

# Font objects
title_font = pygame.font.SysFont('Arial', 100)
info_font = pygame.font.SysFont('Arial', 35)
score_font = pygame.font.SysFont('Arial', 25)

# Function to create start ascreen
def display_start_screen(window, title_txt, info_text):

    window.fill(black)
    title = title_font.render(title_txt, True, white)
    title_rect = title.get_rect(center = (width_height // 2, (width_height // 2)  - 50))
    info = info_font.render(info_text, True, white)
    info_rect = info.get_rect(center = (width_height // 2, (width_height // 2) + 25))
    window.blit(title, title_rect)
    window.blit(info, info_rect)
    pygame.display.update()

# Function to create game over screen
def display_end_screen(window, title_txt, info_text, total_score):

    window.fill(black)
    score_text = 'FINAL SCORE: ' + str(total_score)
    title = title_font.render(title_txt, True, white)
    title_rect = title.get_rect(center = (width_height // 2, (width_height // 2)  - 50))
    info = info_font.render(info_text, True, white)
    info_rect = info.get_rect(center = (width_height // 2, (width_height // 2) + 50))
    score = info_font.render(score_text, True, white)
    score_rect = score.get_rect(center = (width_height // 2, (width_height // 2) + 5))
    window.blit(title, title_rect)
    window.blit(info, info_rect)
    window.blit(score, score_rect)
    pygame.display.update()

# Function to draw grid
def draw_grid(window, rows, w):

    window.fill(black)
    x_grid = 0
    y_grid = 0
    score_txt = str(current_score)

    for line in range(rows):
        x_grid += cell_width
        y_grid += cell_width
        pygame.draw.line(window, white, (x_grid, cell_width), (x_grid, w))
        pygame.draw.line(window, white, (0, y_grid), (w, y_grid))

def display_score(window, w, current_score):
    score_txt = 'SCORE: ' + str(current_score)
    score = score_font.render(score_txt, True, white)
    window.blit(score, (5, 5))


# Set window
window = pygame.display.set_mode((width_height, width_height))
pygame.display.set_caption('Snake')
window.fill(black)
clock = pygame.time.Clock()

game_over = False
run = True
current_score = 0

while run:

    if game_over == False:
        display_start_screen(window,'SNAKE', 'PRESS ENTER TO START GAME')
    elif game_over == True:
        display_end_screen(window,'GAME OVER', 'PRESS ENTER TO RESTART', current_score)

    pygame.display.update()

    start_key = pygame.key.get_pressed()
    if start_key[pygame.K_RETURN]:
        # Set/reset variables to start game
        game_over = False
        game = True
        body = []
        x = cell_width
        y = cell_width
        current_score = 0
        direction = 'right'
        x_food = random.randrange(cell_width, width_height - 5, cell_width)
        y_food = random.randrange(cell_width, width_height - 5, cell_width)
        # Add snake head
        body.append([x,y])

        while game:
            pygame.time.delay(150)
            clock.tick(50)
            draw_grid(window, rows, width_height)
            display_score(window, width_height, current_score)

            # Draw snake
            i = 0
            while i < len(body):
                if i == 0:
                    eye_1 = (body[i][0] + (cell_width // 2), body[i][1] + 8)
                    eye_2 = (body[i][0] + (cell_width // 2), body[i][1] + 16)
                    if direction == 'up' or direction == 'down':
                        eye_1 = (body[i][0] + 8, body[i][1] + (cell_width // 2))
                        eye_2 = (body[i][0] + 16, body[i][1] + (cell_width // 2))
                    pygame.draw.rect(window, purple, (body[i][0]+1, body[i][1]+1, cell_width-1, cell_width-1))
                    pygame.draw.circle(window, black, eye_1, 3)
                    pygame.draw.circle(window, black, eye_2, 3)
                else:
                    pygame.draw.rect(window, purple, (body[i][0]+1, body[i][1]+1, cell_width-1, cell_width-1))
                i += 1

            # Draw food           
            pygame.draw.rect(window, orange, (x_food+1, y_food+1, cell_width-1, cell_width-1))
            food_cord = [x_food,y_food]

            # Check to make sure food is not in position of snake body
            if food_cord in body:
                x_food = random.randrange(cell_width, width_height - 5, cell_width)
                y_food = random.randrange(cell_width, width_height - 5, cell_width)
            pygame.display.update()

            # Check if food is eaten and extend snake body            
            if food_cord in body:
                x_food = random.randrange(cell_width, width_height - 5, cell_width)
                y_food = random.randrange(cell_width, width_height - 5, cell_width)
                body.append([x,y])
                current_score += 1
            
            # Update direction variable when key is pressed
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                if direction =='up' or direction == 'down':
                        direction = 'right'
            elif keys[pygame.K_LEFT]:
                if direction =='up' or direction == 'down':
                    direction = 'left'
            elif keys[pygame.K_UP]:
                if direction == 'left' or direction == 'right':
                        direction = 'up'
            elif keys[pygame.K_DOWN]:
                if direction == 'left' or direction == 'right':
                        direction = 'down'

            # Upate coordinates in body as snake moves
            j = len(body) - 2
            k = len(body) - 1
            while j >= 0:
                body[k][0] = body[j][0]
                body[k][1] = body[j][1]
                j -= 1
                k -= 1

            if direction == 'right':
                x += cell_width
                body[0][0] = x
                no_head = body[1:]
                if body[0][0] > 500 or body[0][1] > 500 or body[0][0] < 25 or body[0][1] < 25 or body[0] in no_head:
                    game = False
                    game_over = True
            elif direction == 'left':
                x -= cell_width
                body[0][0] = x
                no_head = body[1:]
                if body[0][0] > 500 or body[0][1] > 500 or body[0][0] < 0 or body[0][1] < 25 or body[0] in no_head:
                    game = False
                    game_over = True
            elif direction == 'up':
                y -= cell_width
                body[0][1] = y
                no_head = body[1:]
                if body[0][0] > 500 or body[0][1] > 500 or body[0][0] < 0 or body[0][1] < 25 or body[0] in no_head:
                    game = False
                    game_over = True
            elif direction == 'down':
                y += cell_width
                body[0][1] = y
                no_head = body[1:]
                if body[0][0] > 500 or body[0][1] > 500 or body[0][0] < 0 or body[0][1] < 25 or body[0] in no_head:
                    game = False
                    game_over = True

            # Terminate game if window is closed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    game = False
                    game_over = False
                    
    # Terminate game if window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
