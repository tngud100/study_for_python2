from os import close
import pygame
import random

from pygame import time


pygame.init() # 초기화 (반드시 필요)

# 화면 크기 설정
screen_width = 480 # 가로 크기
screen_height = 680
screen = pygame.display.set_mode((screen_width, screen_height))


# 화면 타이틀 설정
pygame.display.set_caption("S_H_ Game") # 게임 이름

# FPS
clock = pygame.time.Clock()

# 배경 이미지 불러오기
background = pygame.image.load("C:/Users/82105/Desktop/pygame_basic/pygame_basic/background.png")

# 캐릭터(스프라이트) 불러오기
character = pygame.image.load("C:/Users/82105/Desktop\pygame_basic/pygame_basic/character.png")
character_size = character.get_rect().size # 이미지 크기를 구해옴
character_width = character_size[0] # 캐릭터의 가로 크기
character_height = character_size[1] # 캐릭터의 세로 크기
character_x_pos = (screen_width / 2) - character_width # 화면 가로의 절반 크기에 해당하는 곳에 위치
character_y_pos = screen_height - character_height # 화면 세로 크기 가장 아래에 해당하는 곳에 위치

# 이동할 좌표
to_x = 0
to_y = 0

# 이동 속도
character_speed = 0.5

# 적 enemy 캐릭터

enemy = pygame.image.load("C:/Users/82105/Desktop/pygame_basic/pygame_basic/enemy.png")
enemy_size = enemy.get_rect().size # 이미지 크기를 구해옴
enemy_width = enemy_size[0] # 적의 가로 크기
enemy_height = enemy_size[1] # 적의 세로 크기
enemy_x_pos = random.randint(1, screen_width - enemy_width) # 화면 가로의 절반 크기에 해당하는 곳에 위치
enemy_y_pos = 0 # 화면 세로 크기 가장 아래에 해당하는 곳에 위치

# 적이 이동 속도
enemy_speed = random.randint(10,20)

# 적의 이동 좌표
fall_y = 0
falled_y = screen_height - enemy_height

# 적이 땅에 떨어지기 까지의 시간
fall_time = pygame.time.get_ticks()
falled_time = 3

# 폰트 정의
game_font = pygame.font.Font(None, 40) # 폰트 객체 생성( 폰트, 크기)

# 총 시간
total_time = 50

# 시작 시간
start_ticks = pygame.time.get_ticks() # 시작 tick을 받아옴

# 이벤트 루프
running = True # 게임이 진행중인가?
while running:
    dt = clock.tick(60) # 게임화면의 초당 프레임 수 설정

    print(("fps : "+ str(clock.get_fps())))

    for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: # 창이 닫히는 이벤트가 발생하였는가?
            running = False # 게임이 진행중이 아님
        
        if event.type == pygame.KEYDOWN: # 키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT:
                to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                to_x += character_speed

            elif event.key == pygame.K_LEFT * pygame.K_RIGHT: # 키를 동시에 누름
                if event.type == pygame.KEYUP: # 방향키를 떼는 이벤트가 발생 했는가?
                    if event.key == pygame.K_LEFT: 
                        to_x += character_speed
                    elif event.key == pygame.K_RIGHT:
                        to_x -= character_speed
                    else:
                        to_x = 0

        if event.type == pygame.KEYUP: # 키를 뗐는지 확인
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                to_x = 0


    character_x_pos += to_x * dt
    enemy_y_pos += enemy_speed

    # 가로 경계값 처리
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    if enemy_y_pos > screen_height:
        enemy_y_pos = 0
        enemy_x_pos = random.randint(1, screen_width - enemy_width) # 화면 가로의 절반 크기에 해당하는 곳에 위치

    # 충돌 처리를 위한 rect 정보 없데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    # 충돌 체크
    if character_rect.colliderect(enemy_rect):
        print("fire")
        running = False

    screen.blit(background, (0, 0)) # 배경 그리기
        
    screen.blit(character, (character_x_pos, character_y_pos)) # 캐릭터 그리기

    screen.blit(enemy, (enemy_x_pos, enemy_y_pos)) # 적 그리기

    # 타이머 집어 넣기
    # 경과 시간 계산
    elasped_time = (pygame.time.get_ticks() - start_ticks) / 1000 
    # 경과 시간(ms)을 1000으로 나누어서 초(s) 단위로 표시

    timer = game_font.render(str(int(total_time - elasped_time)), True, (0, 0, 0))
    # 출력할 글자, True, 글자 색상
    screen.blit(timer, (10, 10))

    # 시간이 0이면 게임 종료
    if total_time - elasped_time <= 0 :
        print("Time Out")
        running = False

    pygame.display.update() # 게임화면을 다시 그리기!

pygame.time.delay(500)

# pygame 종료
pygame.quit()
