import pygame, math, time, os, random

pygame.init()

w = 1600
h = w*(9/16)

screen = pygame.display.set_mode((w, h))

main = True
ingame = True

keys = [0, 0, 0, 0]  # 키 누름 감지 리스트
keyset = [0, 0, 0, 0] # 키 누름 감지 리스트

# 감속 코드가 프레임 최적화시키기에 작성한 프레임을 구하기 위한 코드
clock = pygame.time.Clock()
maxframe = 60
fps = 0
#===============================================================

# 노트 위치 계산 초시계====
gst = time.time()
Time = time.time() - gst
#=========================

# 노트 소환 함수==============================j
ty = 0      # 노트 y 
tst = Time  # 노트 소환 시간

t1 = []
t2 = []
t3 = []
t4 = []

# 글씨 폰트 가져오기========================================================================
Cpath = os.path.dirname(__file__)
Fpath = os.path.join("font")

rate= "PERPECT"

ingame_font_rate = pygame.font.Font(os.path.join(Fpath, "ingame_font.ttf"), int(w / 23))
rate_text = ingame_font_rate.render(str(rate), False, (255, 255, 255))
#===========================================================================================

def sum_note(n):
    ty = 0
    tst = Time + 2
    if n == 1:
        t1.append([ty, tst])
    if n == 2:
        t2.append([ty, tst])
    if n == 3:
        t3.append([ty, tst])
    if n == 4:
        t4.append([ty, tst])

speed = 2
notesumt = 0  # 노트 소환 위한 변수
a = 0
aa = 0

spin = 0
combo = 0
combo_effect = 0
combo_effect2 = 0
miss_anim = 0
last_combo = 0

combo_time = Time + 1
# 게임 오버

game_over = False

# 생명력=========================================

max_health = 100
current_health = max_health


# 판정 코드=======================================
rate_data = [0, 0, 0, 0]

def rating(n):
    global combo, miss_anim, last_combo, combo_effect, combo_effect2, combo_time, rate, current_health, game_over #수정됨
    if abs(Time - rate_data[n - 1]) < 2 and abs(Time - rate_data[n-1]) >= 0.7:
        last_combo = combo
        miss_anim = 1
        combo = 0
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "WORST"
    if abs(Time - rate_data[n - 1]) < 1 and abs(Time - rate_data[n-1]) >= 0.35:
        last_combo = combo
        miss_anim = 1
        combo = 0
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "BAD"
    if abs(Time - rate_data[n - 1]) < 0.35 and abs(Time - rate_data[n-1]) >= 0.07:
        combo += 1
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "GOOD"
    if abs(Time - rate_data[n - 1]) < 0.07 and abs(Time - rate_data[n-1]) >= 0.035:
        combo += 1
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "GREAT"
    if abs(Time - rate_data[n - 1]) < 0.035 and abs(Time - rate_data[n-1]) >= 0:
        combo += 1
        combo_effect = 0.2
        combo_time = Time + 1
        combo_effect2 = 1.3
        rate = "PERPECT"
# 생명력 조정
    if rate == "MISS":
        current_health -= 10  # 미스 시 생명력 감소
    elif rate == "BAD":
        current_health -= 5  # BAD 판정 시 생명력 감소
    elif rate == "GOOD":
        current_health += 1  # GOOD 판정 시 생명력 증가
    elif rate == "GREAT":
        current_health += 3  # GREAT 판정 시 생명력 증가
    elif rate == "PERPECT":
        current_health += 5  # PERFECT 판정 시 생명력 증가
    
    current_health = max(0, min(current_health, max_health))  # 생명력 범위 제한
    
    if current_health <= 0:
        game_over = True


#================================================
# 메인 게임 루프 수정

while main:
    while ingame and not game_over:

        if len(t1) > 0:
            rate_data[0] = t1[0][0]
        if len(t2) > 0:
            rate_data[1] = t2[0][1]
        if len(t3) > 0:
            rate_data[2] = t3[0][1]
        if len(t4) > 0:
            rate_data[3] = t4[0][1]

        if Time > 0.2 * notesumt:
            notesumt += 1
            while a == aa:
                a = random.randint(1, 4)
            sum_note(a)
            aa = a

        Time = time.time() - gst
        # 폰트==================================================================================================================================
        ingame_font_combo = pygame.font.Font(os.path.join(Fpath, "ingame_font.ttf"), int((w / 38) * combo_effect2))
        combo_text = ingame_font_combo.render(str(rate), False, (255, 255, 255))

        rate_text = ingame_font_rate.render(str(rate), False, (255, 255, 255))
        rate_text = pygame.transform.scale(rate_text, (int(w / 110 * len(rate) * combo_effect2), int((w / 58 * combo_effect * combo_effect2))))

        ingame_font_miss = pygame.font.Font(os.path.join(Fpath, "ingame_font.ttf"), int((w / 38 * miss_anim)))
        miss_text = ingame_font_miss.render(str(last_combo), False, (255, 0, 0))
        #============================================================================================================================================

        # 프레임==============
        fps = clock.get_fps()

        if fps == 0:
            fps = maxframe
        #=====================

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                # 키 입력 받는 함수============
                if event.key == pygame.K_d:
                    keyset[0] = 1
                    if len(t1) > 0:
                        if t1[0][0] > h / 3:
                         rating(1)
                         del t1[0]
                if event.key == pygame.K_f:
                    keyset[1] = 1
                    if len(t2) > 0:
                        if t2[0][0] > h / 3:
                         rating(2)
                         del t2[0]
                if event.key == pygame.K_j:
                    keyset[2] = 1
                    if len(t3) > 0:
                        if t3[0][0] > h / 3:
                         rating(3)
                         del t3[0]
                if event.key == pygame.K_k:
                    keyset[3] = 1
                    if len(t4) > 0:
                        if t4[0][0] > h / 3:
                         rating(4)
                         del t4[0]

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    keyset[0] = 0
                if event.key == pygame.K_f:
                    keyset[1] = 0
                if event.key == pygame.K_j:
                    keyset[2] = 0
                if event.key == pygame.K_k:
                    keyset[3] = 0
                #===============================

        screen.fill((0, 0, 0))
# 움직임 가감속(정확히는 감속)===========================================================
        keys[0] += (keyset[0] - keys[0]) / (3 * (maxframe / fps))
        keys[1] += (keyset[1] - keys[1]) / (3 * (maxframe / fps))
        keys[2] += (keyset[2] - keys[2]) / (3 * (maxframe / fps))
        keys[3] += (keyset[3] - keys[3]) / (3 * (maxframe / fps))

# 텍스트 움직임 정하는 코드=================================================================
        if Time > combo_time:
            combo_effect += (0 - combo_effect) / (7 * (maxframe / fps))
        if Time < combo_time:
            combo_effect += (1 - combo_effect) / (7 * (maxframe / fps))

        combo_effect2 += (2 - combo_effect2) / (7 * (maxframe / fps))

        miss_anim += (4 - miss_anim) / (14 * (maxframe / fps))
# 디자인================================================================================================================================

        pygame.draw.rect(screen, (0, 0, 0), (w /2 - w / 8, -int(w / 100), w / 4, h + int(w / 50))) #geat background

        for i in range(3):
            i += 1
            pygame.draw.rect(screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)), (w / 2 -w / 8 + w / 32 - (w / 32) * keys[0], (h / 12) * 9 - (h / 30) * keys[0] * i, w / 16 * keys[0], (h / 35) / i))
        for i in range(3):
            i += 1
            pygame.draw.rect(screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)), (w / 2 -w / 16 + w / 32 - (w / 32) * keys[1], (h / 12) * 9 - (h / 30) * keys[1] * i, w / 16 * keys[1], (h / 35) / i))
        for i in range(3):
            i += 1
            pygame.draw.rect(screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)), (w / 2 +w / 32 - (w / 32) * keys[2], (h / 12) * 9 - (h / 30) * keys[2] * i, w / 16 * keys[2] , (h / 35) / i))
        for i in range(3):
            i += 1
            pygame.draw.rect(screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)), (w / 2 +w / 16 + w / 32 - (w / 32) * keys[3], (h / 12) * 9 - (h / 30) * keys[3] * i, w / 16 * keys[3], (h / 35) / i))

        pygame.draw.rect(screen, (255, 255, 255), (w / 2 - w / 8, -int(w / 100), w / 4, h + int(w / 50)), int(w / 100)) #gear line
        
    # 생명력 게이지 그리기===========================================================================================
        health_bar_width = (w / 6) * (current_health / max_health)
        health_bar_height = h / 40
        health_bar_x = w / 50
        health_bar_y = h / 50

    # 배경 게이지 (빨간색)
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, w / 6, health_bar_height))
    # 현재 체력 게이지 (초록색)
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

# 게이지 테두리
        pygame.draw.rect(screen, (255, 255, 255), (health_bar_x, health_bar_y, w / 6, health_bar_height), 2)

        # note ========================================================================================================================
        for tile_data in t1:
            tile_data[0] = (h / 12) * 9 + (Time - tile_data[1]) * 350 * speed * (h / 900) # 렉걸려도 노트는 일정 속도로 내려오게 함
                    # 판정선 위치 기준 / (현재 - 노트 소환 시간) * 350 이동[시간 경과 될수록 이 차가 커져 노트가 내려가는데 2초를 더해줘서..6븐 참조]
            pygame.draw.rect(screen, (255, 255, 255), (w / 2 - w / 8, tile_data[0] - h / 100, w / 16, h / 50))
            if tile_data[0] > h - (h / 9):
                last_combo = combo
                miss_anim = 1
                combo = 0
                combo_effect = 0.2
                combo_time = Time + 1
                combo_effect2 = 1.3
                rate = "MISS"
                current_health -= 10  # 미스 시 생명력 감소
                current_health = max(0, min(current_health, max_health))  # 생명력 범위 제한
                if current_health <= 0:
                    game_over = True
                t1.remove(tile_data)

        for tile_data in t2:
            tile_data[0] = (h / 12) * 9 + (Time - tile_data[1]) * 350 * speed * (h / 900)
            pygame.draw.rect(screen, (255, 255, 255), (w / 2 - w / 16, tile_data[0] - h / 100, w / 16, h / 50))
            if tile_data[0] > h - (h / 9):
                last_combo = combo
                miss_anim = 1
                combo = 0
                combo_effect = 0.2
                combo_time = Time + 1
                combo_effect2 = 1.3
                rate = "MISS"
                current_health -= 10  # 미스 시 생명력 감소
                current_health = max(0, min(current_health, max_health))  # 생명력 범위 제한
                if current_health <= 0:
                    game_over = True
                t2.remove(tile_data) 

        for tile_data in t3:
            tile_data[0] = (h / 12) * 9 + (Time - tile_data[1]) * 350 * speed * (h / 900) 
            pygame.draw.rect(screen, (255, 255, 255), (w / 2, tile_data[0] - h / 100, w / 16, h / 50))
            if tile_data[0] > h - (h / 9):
                last_combo = combo
                miss_anim = 1
                combo = 0
                combo_effect = 0.2
                combo_time = Time + 1
                combo_effect2 = 1.3
                rate = "MISS"
                current_health -= 10  # 미스 시 생명력 감소
                current_health = max(0, min(current_health, max_health))  # 생명력 범위 제한
                if current_health <= 0:
                    game_over = True
                t3.remove(tile_data)

        for tile_data in t4:
            tile_data[0] = (h / 12) * 9 + (Time - tile_data[1]) * 350 * speed * (h / 900) 
            pygame.draw.rect(screen, (255, 255, 255), (w / 2 + w / 16, tile_data[0] - h / 100, w / 16, h / 50))
            if tile_data[0] > h - (h / 9):
                last_combo = combo
                miss_anim = 1
                combo = 0
                combo_effect = 0.2
                combo_time = Time + 1
                combo_effect2 = 1.3
                rate = "MISS"
                current_health -= 10  # 미스 시 생명력 감소
                current_health = max(0, min(current_health, max_health))  # 생명력 범위 제한
                if current_health <= 0:
                    game_over = True
                t4.remove(tile_data)

    # 판정선===========================================================================================================================
        pygame.draw.rect(screen, (0, 0, 0), (w /2 - w / 8, (h / 12) * 9, w / 4, h / 2))
        pygame.draw.rect(screen, (255, 255, 255), (w / 2 - w / 8, (h / 12) * 9, w / 4, h /2), int(h /100))
    #==================================================================================================================================

    # key ==============================================================================================================================
        pygame.draw.rect(screen, (255 - 100 * keys[0],255 - 100 * keys[0], 255 - 100 * keys[0]), (w / 2 - w / 9, (h / 24) * 19 + (h / 48) * keys[0], w / 27, h / 8), int(h / 150))
        pygame.draw.rect(screen, (255 - 100 * keys[3],255 - 100 * keys[3], 255 - 100 * keys[3]), (w / 2 + w / 13.5, (h / 24) * 19 + (h / 48) * keys[3], w / 27, h / 8), int(h / 150))

        pygame.draw.circle(screen, (150, 150, 150), (w / 2, (h / 24) * 21), (w / 20), int(h / 200))
        pygame.draw.line(screen, (150, 150, 150), (w / 2 - math.sin(spin) * 25 * (w / 1600), (h / 24) * 21 - math.cos(spin) * 25 * (w / 1600)), (w / 2 + math.sin(spin) * 25 * (w / 1600), (h / 24) * 21 + math.cos(spin) * 25 * (w / 1600)), int(w / 400))
        # spin += (speed / 20 * (maxframe / fps))
        spin = Time * -2

        pygame.draw.rect(screen, (255 - 100 * keys[1], 255 - 100 * keys[1], 255 - 100 * keys[1]), (w / 2 - w / 18, (h / 48) * 39 + (h / 48) * keys[1], w / 27, h / 8))
        pygame.draw.rect(screen, (0,0, 0), (w / 2 - w / 18, (h / 48) * 43 + (h / 48) * (keys[1] * 1.2), w / 27, h / 64), int(h / 150))
        pygame.draw.rect(screen, (50,50, 50), (w / 2 - w / 18, (h / 48) * 39 + (h / 48) * keys[1], w / 27, h / 8), int(h / 150))

        pygame.draw.rect(screen, (255 - 100 * keys[2], 255 - 100 * keys[2], 255 - 100 * keys[2]), (w / 2 + w / 58, (h / 48) * 39 + (h / 48) * keys[2], w / 27, h / 8))
        pygame.draw.rect(screen, (0,0, 0), (w / 2 + w / 58, (h / 48) * 43 + (h / 48) * (keys[2] * 1.2), w / 27, h / 64), int(h / 150))
        pygame.draw.rect(screen, (50,50, 50), (w / 2 + w / 58, (h / 48) * 39 + (h / 48) * keys[2], w / 27, h / 8), int(h / 150))
    #===================================================================================================================================
        miss_text.set_alpha(255 - (255 / 4) * miss_anim)

        #screen.blit(combo_text, (w / 2 - combo_text.get_width() / 2, (h / 12) * 4 - combo_text.get_height() / 2))
        screen.blit(rate_text, (w / 2 - rate_text.get_width() / 2, (h / 12) * 8 - rate_text.get_height() / 2))
        screen.blit(miss_text, (w / 2 - miss_text.get_width() / 2, (h / 12) * 4 - miss_text.get_height() / 2))

        pygame.display.flip()
        clock.tick(maxframe)
#게임오버=====================================================================================================================================
    if game_over:
        screen.fill((0, 0, 0))
        game_over_font = pygame.font.Font(None, 72)
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (w / 2 - game_over_text.get_width() / 2, h / 2 - game_over_text.get_height() / 2))
        pygame.display.flip()

        # 게임오버 후 3초 대기
        pygame.time.wait(3000)
        main = False  # 게임 종료