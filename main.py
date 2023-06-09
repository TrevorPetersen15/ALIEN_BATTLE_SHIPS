import pygame
import os
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH,HEIGHT = 1280,500
WIN=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("BATTLE SHIPS")
FPS=60
VEL=5

BORDER = pygame.Rect(WIDTH//2 -5 , 0, 10, HEIGHT)

SPACESHIP_SIZE=50,50
SPACESHIP_width,SPACESHIP_height=50,50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BULLET_HIT_SOUND=pygame.mixer.Sound(os.path.join("Assets","grenade+1.mp3"))
BULLET_FIRED=pygame.mixer.Sound(os.path.join("Assets","Gun+silencer.mp3"))
BULLET_VEL=7
MAX_BULLETS=3

HEALTH_FONT =pygame.font.SysFont("comicsans", 40, bold=False, italic=False)
ins_font =pygame.font.SysFont("comicsans", 20, bold=False, italic=False)

WINNER_FONT=pygame.font.SysFont("comicsans", 100, bold=True, italic=False)

YELLOW_SPACESHIP_IMAGE=pygame.image.load(os.path.join("Assets","spaceship_yellow.png"))
# YELLOW_SPACESHIP_IMAGE=pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_SIZE))
YELLOW_SPACESHIP_IMAGE=pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE,(SPACESHIP_SIZE)),90)
RED_SPACESHIP_IMAGE=pygame.image.load(os.path.join("Assets","spaceship_red.png"))
RED_SPACESHIP_IMAGE=pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE,(SPACESHIP_SIZE)),270)

YELLOW_HIT=pygame.USEREVENT+1
RED_HIT=pygame.USEREVENT+2
Space=pygame.transform.scale(pygame.image.load(os.path.join("Assets","space.png")),((WIDTH,HEIGHT)))

def draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health):
    WIN.blit(Space,(0,0))
    pygame.draw.rect(WIN,BLACK,BORDER)

    red_health_text= HEALTH_FONT.render("Health " + str(red_health),1, WHITE)
    yellow_health_text= HEALTH_FONT.render("Health " + str(yellow_health),1, WHITE)
    
    WIN.blit(red_health_text,(WIDTH//2+WIDTH//2//2-100, 10))
    WIN.blit(yellow_health_text,(WIDTH//2//2-100,10))



    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    WIN.blit(YELLOW_SPACESHIP_IMAGE,(yellow.x,yellow.y))
    WIN.blit(RED_SPACESHIP_IMAGE,(red.x,red.y))

    pygame.display.update()





def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height  < HEIGHT+5:  # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT +5:  # DOWN
        red.y += VEL

def draw_winner(text):
    
    draw_text=WINNER_FONT.render(text,1,WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)

def handle_bullet(yellow_bullets, red_bullets, yellow,red):
    for bullet in yellow_bullets:
        bullet.x+=BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x-=BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

def instructions(instruction):
    WIN.blit(Space,(0,0))
    draw_instruction=ins_font.render(instruction,1,WHITE)
    WIN.blit(draw_instruction, (WIDTH//2 - draw_instruction.get_width() //2, HEIGHT//2 - draw_instruction.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)##have delay done so it shows in how many seconds game will start

def main():
    begin='wasd for yellow space ship movement, left ctrl to shoot yellow // arrow keys to move red shaceship, right ctrl to shoot'
    instructions(begin)
    red=pygame.Rect(1230,300,SPACESHIP_width,SPACESHIP_height)
    yellow=pygame.Rect(0,300,SPACESHIP_width,SPACESHIP_height)
    clock=pygame.time.Clock()
    run=True
    red_bullets=[]
    yellow_bullets=[]
    red_health=10
    yellow_health=10
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRED.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRED.play()

            if event.type==RED_HIT:
                red_health-=1
                BULLET_HIT_SOUND.play()


            if event.type==YELLOW_HIT:
                yellow_health-=1
                BULLET_HIT_SOUND.play()

        winner_text=''
        if red_health<=0:
            winner_text= "YELLOW WINS!"

        if yellow_health<=0:
            winner_text= "RED WINS!"

        if winner_text!="":
            draw_winner(winner_text)
            break

        keys_pressed=pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullet(yellow_bullets, red_bullets, yellow,red)


        draw_window(red,yellow,red_bullets,yellow_bullets,red_health,yellow_health)


    main()

if __name__== "__main__":
    main()