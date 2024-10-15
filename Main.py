import pygame
import sys, os, random, time
from pygame.locals import*

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
startSpeed = 5
moveSpeed = startSpeed
maxSpeed = 10
score = 0
textFonts = ['comicsansms', 'arial']
textSize = 48
paused = False
enemyNum = -1

GAME_ROOT_FOLDER = os.path.dirname(__file__)
IMAGE_FOLDER = os.path.join(GAME_ROOT_FOLDER, "Images")

def GameOver() :
    # Game Over! 문구 표시
    fontGameOver = pygame.font.SysFont(textFonts, textSize)
    textGameOver = fontGameOver.render("Game Over!", True, RED)
    rectGameOver = textGameOver.get_rect()
    rectGameOver.center = (IMG_ROAD.get_width()//2, IMG_ROAD.get_height()//2)
    
    # 최종 점수 표시
    fontGameOver2 = pygame.font.SysFont(textFonts, textSize//2)
    textGameOver2 = fontGameOver.render("Score : " + str(score), True, RED)
    rectGameOver2 = textGameOver.get_rect()
    rectGameOver2.center = (IMG_ROAD.get_width()//2, IMG_ROAD.get_height()//2 + 80)
    
    screen.fill(BLACK)
    screen.blit(textGameOver, rectGameOver)
    screen.blit(textGameOver2, rectGameOver2)
    pygame.display.update()
    player.kill()
    enemy.kill()
    time.sleep(5)
    pygame.quit()
    sys.exit()
    

# 게임 시작
pygame.init()

clock = pygame.time.Clock()

clock.tick(60)

pygame.display.set_caption("Crazy Driver")

IMG_ROAD = pygame.image.load(os.path.join(IMAGE_FOLDER, "Road.png"))
IMG_PLAYER = pygame.image.load(os.path.join(IMAGE_FOLDER, "Player.png"))
IMG_ENEMIES = []
IMG_ENEMIES.append(pygame.image.load(os.path.join(IMAGE_FOLDER, "Enemy.png")))
IMG_ENEMIES.append(pygame.image.load(os.path.join(IMAGE_FOLDER, "Enemy2.png")))
IMG_ENEMIES.append(pygame.image.load(os.path.join(IMAGE_FOLDER, "Enemy3.png")))
IMG_ENEMIES.append(pygame.image.load(os.path.join(IMAGE_FOLDER, "IceCube.png")))


screen = pygame.display.set_mode(IMG_ROAD.get_size())

# 게임 객체 만들기
# 플레이어 초기 위치 계산
h = IMG_ROAD.get_width()//2
v = IMG_ROAD.get_height() - (IMG_PLAYER.get_height()//2)

# player 스프라이트 만들기
player = pygame.sprite.Sprite()
player.image = IMG_PLAYER
player.surf = pygame.Surface(IMG_PLAYER.get_size())
player.rect = player.surf.get_rect(center = (h, v))
    

# 메인 게임
while True :
    screen.blit(IMG_ROAD, (0,0))
    pygame.display.set_caption("Crazy Driver - Score " + str(score))
    # 플레이어 위치설정
    screen.blit(player.image, player.rect)
    
    # 적 존재 유무 확인
    if enemyNum == -1 :
        enemyNum = random.randrange(0,len(IMG_ENEMIES))
        
        # 적 초기 위치 계산
        hl = IMG_ENEMIES[enemyNum].get_width()//2
        hr = IMG_ROAD.get_width() - (IMG_ENEMIES[enemyNum].get_width()//2)
        h = random.randrange(hl,hr)
        v = 0
        
        # enemy 스프라이트 만들기
        enemy = pygame.sprite.Sprite()
        enemy.image = IMG_ENEMIES[enemyNum]
        enemy.surf = pygame.Surface(IMG_ENEMIES[enemyNum].get_size())
        enemy.rect = enemy.surf.get_rect(center = (h, v))
        
    keys = pygame.key.get_pressed()
    if paused :
        if not keys[K_SPACE] :
            moveSpeed = tempSpeed
            paused = False
    else :
        if keys[K_LEFT] and player.rect.left > 0 :
            player.rect.move_ip(-moveSpeed, 0)
            if player.rect.left < 0 :
                player.rect.left = 0
                
        if keys[K_RIGHT] and player.rect.right < IMG_ROAD.get_width() :
            player.rect.move_ip(moveSpeed, 0)
            if player.rect.right > IMG_ROAD.get_width() :
                player.rect.right = IMG_ROAD.get_width()
        
        if keys[K_SPACE] :
            tempSpeed = moveSpeed
            moveSpeed = 0
            paused = True
        
    # 적 위치설정    
    screen.blit(enemy.image, enemy.rect) 
    
    enemy.rect.move_ip(0,moveSpeed)
    
    if (enemy.rect.bottom > IMG_ROAD.get_height()) :
        enemy.kill() # enemy 객체 없애기
        enemyNum = -1 # 적 없음
        score += 1
        moveSpeed += 0.1
        if moveSpeed < maxSpeed :
            moveSpeed += 0.1
            
    # 충돌 확인   
    if enemyNum >= 0 and pygame.sprite.collide_rect(player, enemy) :
        # 얼음과 충돌
        if enemyNum == 3 : 
            # 얼음과 충돌하면 속도 원상복귀
            moveSpeed = startSpeed
        else :
            GameOver()
    
    for event in pygame.event.get() :
        if event.type == QUIT :
            pygame.quit()
            sys.exit()
            
    pygame.display.update()