import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
snake_color = (0, 255, 0)  # Green color for the snake
bonus_color = (255, 215, 0)  # Gold color for the bonus food

# Display dimensions
dis_width = 800
dis_height = 600

# Game display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

# Background music and image
pygame.mixer.music.load('background.mp3')
pygame.mixer.music.play(-1)
bg = pygame.image.load('background.jpg')
bg = pygame.transform.scale(bg, (dis_width, dis_height))

# Clock
clock = pygame.time.Clock()

# Snake block size and speed
snake_block = 10
snake_speed = {'easy': 10, 'medium': 20, 'hard': 30}
bonus_duration = {'easy': 15, 'medium': 10, 'hard': 5}

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def our_snake(snake_block, snake_List):
    for x in snake_List:
        pygame.draw.rect(dis, snake_color, [x[0], x[1], snake_block, snake_block])

def our_hurdles(hurdles):
    for hurdle in hurdles:
        pygame.draw.rect(dis, white, [hurdle[0], hurdle[1], snake_block, snake_block])

def show_score(score):
    value = score_font.render("Score: " + str(score), True, white)
    dis.blit(value, [dis_width - 200, 0])  # Display score at the top right

def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3 + y_displace])

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    score = 0
    food_count = 0

    # Food coordinates
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    # Bonus food coordinates
    bonus_foodx = -10
    bonus_foody = -10
    bonus_active = False
    bonus_start_time = 0

    # Hurdles
    hurdles = [
        (200, 200), (200, 210), (200, 220),
        (400, 400), (400, 410), (400, 420),
        (300, 100), (300, 110), (300, 120),
        (600, 200), (600, 210), (600, 220),
        (500,500),(510,500),(520,500),(500,510),(500,520),(500,530)
    ]

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red, -50)
            message(f"Your Score: {score}", black, 50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        x1 += x1_change
        y1 += y1_change

        # Implement tunnel effect
        if x1 >= dis_width:
            x1 = 0
        elif x1 < 0:
            x1 = dis_width - snake_block
        if y1 >= dis_height:
            y1 = 0
        elif y1 < 0:
            y1 = dis_height - snake_block

        dis.blit(bg, (0, 0))
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])

        if food_count >= 5 and not bonus_active:
            bonus_foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            bonus_foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            bonus_active = True
            bonus_start_time = time.time()
            food_count = 0  # Reset food count after bonus appears

        if bonus_active:
            pygame.draw.rect(dis, bonus_color, [bonus_foodx, bonus_foody, snake_block, snake_block])
            if time.time() - bonus_start_time > bonus_duration[difficulty]:
                bonus_active = False
                bonus_foodx = -10
                bonus_foody = -10

        our_hurdles(hurdles)
        our_snake(snake_block, snake_List)
        show_score(score)
        pygame.display.update()

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        for hurdle in hurdles:
            if hurdle[0] == x1 and hurdle[1] == y1:
                game_close = True

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score += 1
            food_count += 1

        if x1 == bonus_foodx and y1 == bonus_foody:
            score += 5
            bonus_active = False
            bonus_foodx = -10  # Hide the bonus food off the screen
            bonus_foody = -10  # Hide the bonus food off the screen

        clock.tick(snake_speed[difficulty])

    pygame.quit()
    quit()

# Main menu to choose difficulty
def main_menu():
    global difficulty
    main_menu_run = True
    while main_menu_run:
        dis.fill(blue)
        message("Welcome to Snake Game!", black, -100)
        message("Press 1 for Easy", black, -50)
        message("Press 2 for Medium", black, 0)
        message("Press 3 for Hard", black, 50)
        message("Press Q to Quit", black, 100)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu_run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = 'easy'
                    main_menu_run = False
                elif event.key == pygame.K_2:
                    difficulty = 'medium'
                    main_menu_run = False
                elif event.key == pygame.K_3:
                    difficulty = 'hard'
                    main_menu_run = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

if __name__ == "__main__":
    main_menu()
    gameLoop()
