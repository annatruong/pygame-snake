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
instruction_font = pygame.font.SysFont('Arial', 35)

# Function to create start and game over screen
def display_start_end(window, title_txt, inst_text):
    window.fill(black)
    title = title_font.render(title_txt, True, white)
    title_rect = title.get_rect(center = (width_height // 2, width_height // 3))
    instruction = instruction_font.render(inst_text, True, white)
    instruction_rect = instruction.get_rect(center = (width_height // 2, width_height // 2))
    window.blit(title, title_rect)
    window.blit(instruction, instruction_rect)
    pygame.display.update()

# Function to draw grid
def draw_grid(window, rows, w):
    window.fill(black)
    x_grid = 0
    y_grid = 0
    for line in range(rows):
        x_grid += cell_width
        y_grid += cell_width
        pygame.draw.line(window, white, (x_grid, cell_width), (x_grid, w))
        pygame.draw.line(window, white, (0, y_grid), (w, y_grid))

# Set window
window = pygame.display.set_mode((width_height, width_height))
pygame.display.set_caption('Snake')
window.fill(black)
clock = pygame.time.Clock()

game_over = False
run = True

while run:

    if game_over == False:
        display_start_end(window,'SNAKE','PRESS ENTER TO START GAME')
    elif game_over == True:
        display_start_end(window,'GAME OVER','PRESS ENTER TO RESTART')

    pygame.display.update()

    start_key = pygame.key.get_pressed()
    if start_key[pygame.K_RETURN]:
        # Set/reset variables to start game
        game_over = False
        game = True
        body = []
        x = cell_width
        y = cell_width
        direction = 'right'
        x_food = random.randrange(cell_width, width_height - 5, cell_width)
        y_food = random.randrange(cell_width, width_height - 5, cell_width)
        # Add snake head
        body.append([x,y])

        while game:
            pygame.time.delay(150)
            clock.tick(50)
            draw_grid(window,rows,width_height)

            # Draw snake
            i = 0
            while i < len(body):
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
