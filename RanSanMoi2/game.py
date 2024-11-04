import pygame
import time
import random

# Khởi tạo pygame
pygame.init()

# Định nghĩa màu sắc
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Kích thước màn hình
dis_width = 600
dis_height = 400

# Tạo màn hình chơi
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake game')

# Đồng hồ để điều khiển tốc độ trò chơi
clock = pygame.time.Clock()

# Kích thước mỗi khối rắn
snake_block = 20
snake_speed = 10

# Font chữ cho điểm số và thông báo
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Tải hình nền
background_image = pygame.image.load('images/background.png')  # Đường dẫn đến hình nền
background_image = pygame.transform.scale(background_image, (dis_width, dis_height))  # Kích thước hình nền

# Tải và scale hình ảnh cho đầu, thân rắn
snake_head_up = pygame.image.load('images/snake-top.png')
snake_head_up = pygame.transform.scale(snake_head_up, (snake_block, snake_block))

snake_head_down = pygame.image.load('images/snake-bot.png')
snake_head_down = pygame.transform.scale(snake_head_down, (snake_block, snake_block))

snake_head_left = pygame.image.load('images/snake-left.png')
snake_head_left = pygame.transform.scale(snake_head_left, (snake_block, snake_block))

snake_head_right = pygame.image.load('images/snake-right.png')
snake_head_right = pygame.transform.scale(snake_head_right, (snake_block, snake_block))

snake_body = pygame.image.load('images/snake-body.png')
snake_body = pygame.transform.scale(snake_body, (snake_block, snake_block))

# Tải hình thức ăn
food_image = pygame.image.load('images/food.png')  # Đường dẫn đến hình thức ăn
food_image = pygame.transform.scale(food_image, (snake_block, snake_block))  # Kích thước hình thức ăn

# Hàm hiển thị điểm số
def your_score(score):
    value = score_font.render("Score " + str(score), True, yellow)
    dis.blit(value, [0, 0])

# Vẽ đầu rắn
def draw_head(direction, position):
    if direction == "UP":
        dis.blit(snake_head_up, position)
    elif direction == "DOWN":
        dis.blit(snake_head_down, position)
    elif direction == "LEFT":
        dis.blit(snake_head_left, position)
    elif direction == "RIGHT":
        dis.blit(snake_head_right, position)

# Vẽ thân rắn
def draw_body(snake_list):
    for segment in snake_list:
        dis.blit(snake_body, (segment[0], segment[1]))

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1  # Khởi tạo độ dài rắn

    # Tọa độ thức ăn
    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

    direction = "RIGHT"  # Hướng ban đầu của rắn

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You die ! Press Q to end or C to play again", red)
            your_score(Length_of_snake - 1)
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
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    x1_change = -snake_block
                    y1_change = 0
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    x1_change = snake_block
                    y1_change = 0
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    y1_change = -snake_block
                    x1_change = 0
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    y1_change = snake_block
                    x1_change = 0
                    direction = "DOWN"

        # Kiểm tra va chạm với biên
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        # Vẽ hình nền
        dis.blit(background_image, (0, 0))

        # Vẽ thức ăn bằng hình ảnh mới
        dis.blit(food_image, (foodx, foody))

        # Cập nhật trạng thái của rắn
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Kiểm tra va chạm với chính mình
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        # Vẽ đầu và thân rắn
        draw_head(direction, snake_List[-1])
        draw_body(snake_List[:-1])  # Vẽ chỉ thân rắn (không vẽ đầu)

        your_score(Length_of_snake - 1)

        pygame.display.update()

        # Kiểm tra ăn thức ăn
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
