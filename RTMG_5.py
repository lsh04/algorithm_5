# 수정내용
# test branch에 있는 파일과 머지 한 상태
# 330 line outline_color = get_outline_color() 추가
# 331 line (255,255,255) -> outline_color 로 수정, 너비 값 x위치 값 수정
# 448 line (255,255,255) -> outline_color 로 수정, 너비 값 x위치 값 수정
import subprocess
import sys

def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[package] = __import__(package)

install_and_import('pygame')
install_and_import('mutagen')

import pygame, math, time, os, random
from mutagen.mp3 import MP3
from design import get_outline_color
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
elapsed_time = 0
#=========================

# 노트 소환 함수==============================
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
Korean_font_rate = pygame.font.Font(os.path.join(Fpath, "DungGeunMo.ttf"), int(w / 23))
rate_text = ingame_font_rate.render(str(rate), False, (255, 255, 255))

# 음악 가져와서 재생==============================================================================
music_file = "songs/Fluffybunny - Great Means Not Good - 01 Divergence theorem.mp3"
pygame.mixer.music.load(music_file)

# 음악 파일 길이 측정
audio = MP3(music_file)
music_length = audio.info.length - 8 # 음악 안나오는 시간 6초 정도 뺸 값

# 음악 재생
pygame.mixer.music.play()

# 음악 끝났을 때 이벤트
pygame.mixer.music.set_endevent(pygame.USEREVENT)


#===========================================================================================

def sum_note(n):
    if elapsed_time < music_length:  # 음악이 나올때만 노트 생성되게 변경
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

worst_count = 0
bad_count = 0
good_count = 0
great_count = 0
perpect_count = 0
miss_count = 0

max_combo = 0

combo_time = Time + 1

main = True
ingame = True

# 게임 오버
game_over = False
# 게임 엔드
game_end = False

# 생명력=========================================

max_health = 100
current_health = max_health


# 판정 코드=======================================
rate_data = [0, 0, 0, 0]

def rating(n):
    global combo, miss_anim, last_combo, combo_effect, combo_effect2, combo_time, rate, current_health, game_over, game_end, music_length, worst_count, miss_count, bad_count, good_count, great_count, perpect_count, max_combo
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
        miss_count += 1       # miss 카운트 
        current_health -= 10  # 미스 시 생명력 감소
    elif rate == "WORST": 
        worst_count += 1     # worst 카운트   
        current_health -= 5  # worst 판정 시 생명력 감소 추가
    elif rate == "BAD": 
        bad_count += 1       # bad 카운트
        current_health -= 5  # BAD 판정 시 생명력 감소
    elif rate == "GOOD":
        good_count += 1      # good 카운트
        current_health += 1  # GOOD 판정 시 생명력 증가
    elif rate == "GREAT":
        great_count += 1      # great 카운트
        current_health += 3  # GREAT 판정 시 생명력 증가
    elif rate == "PERPECT":
        perpect_count += 1   # perpect 카운트
        current_health += 5  # PERFECT 판정 시 생명력 증가
    
    current_health = max(0, min(current_health, max_health))  # 생명력 범위 제한
    
    if current_health <= 0:
        game_over = True

   # 최대 콤보수 갱신
    if last_combo > max_combo:
     max_combo = combo


#================================================

while main:
    while ingame and not game_over and not game_end:

        elapsed_time = time.time() - gst
        if len(t1) > 0:
            rate_data[0] = t1[0][1] 
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
        combo_text = ingame_font_combo.render(str(combo), False, (255, 255, 255)) # 콤보 텍스트가 rate여서 안되었던 점

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
            if event.type == pygame.USEREVENT:
                game_end = True
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

# 플레이타임 ======================================================================
        elapsed_minutes = int(elapsed_time // 60)
        elapsed_seconds = int(elapsed_time % 60)
        timer_font = pygame.font.Font(os.path.join(Fpath, "ingame_font.ttf"), int(w / 40))
        timer_text = timer_font.render(f"{elapsed_minutes:02}:{elapsed_seconds:02}", False, (255, 255, 255))
        screen.blit(timer_text, (w - 500, 50))  # 타이머 위치

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

        outline_color = get_outline_color()
        pygame.draw.rect(screen, outline_color, (785 - w / 8, -int(w / 100), 431, h + int(w / 50)), int(w / 100)) #gear line
    # 음악 진행 상황 그리기=====================================================================================================================================

        bar_start = (640, 10)
        bar_end = (970, 10)
        bar_length = bar_end[0] - bar_start[0]

        # 색상 정의
        sky_blue = pygame.Color(135, 206, 235)

        progress = min(elapsed_time / music_length, 1)

        music_bar_width = bar_length * progress
        music_bar_height = 10
        music_bar_x = bar_start[0]
        music_bar_y = bar_start[1] - music_bar_height // 2

        # 진행 게이지 배경 (하얀색)
        pygame.draw.rect(screen, (255, 255, 255), (bar_start[0], music_bar_y, bar_length, music_bar_height), 2)
        # 현재 진행 게이지 (하늘색)
        pygame.draw.rect(screen, sky_blue, (music_bar_x, music_bar_y, music_bar_width, music_bar_height))
        # 현재 진행 게이지 채워가는 점
        dot_x = bar_start[0] + progress * bar_length
        dot_y = bar_start[1]
        pygame.draw.circle(screen, (255, 255, 255), (int(dot_x), dot_y), 10)


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
                miss_count += 1       # miss count
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
                miss_count += 1       # miss count
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
                miss_count += 1       # miss count
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
                miss_count += 1       # miss count
                current_health -= 10  # 미스 시 생명력 감소
                current_health = max(0, min(current_health, max_health))  # 생명력 범위 제한
                if current_health <= 0:
                    game_over = True
                t4.remove(tile_data)

    # 판정선===========================================================================================================================
        pygame.draw.rect(screen, (0, 0, 0), (w /2 - w / 8, (h / 12) * 9, w / 4, h / 2))
        pygame.draw.rect(screen, outline_color, (785 - w / 8, (h / 12) * 9, 431, h /2), int(h /100))
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
        miss_text.set_alpha(255 - (255 / 4) * miss_anim)    # 텍스트 투명도

        screen.blit(combo_text, (w / 2 - combo_text.get_width() / 2, (h / 12) * 4 - combo_text.get_height() / 2))
        screen.blit(rate_text, (w / 2 - rate_text.get_width() / 2, (h / 12) * 8 - rate_text.get_height() / 2))
        screen.blit(miss_text, (w / 2 - miss_text.get_width() / 2, (h / 12) * 4 - miss_text.get_height() / 2))

        pygame.display.flip()
        clock.tick(maxframe)

#게임오버=====================================================================================================================================
    if game_over:
        pygame.mixer.music.stop()
        screen.fill((0, 0, 0))
        game_over_font = pygame.font.Font(None, 90)
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (620, 50))

        score_font = pygame.font.Font(None, 72)
        score_text = score_font.render("MAX COMBO", True, (255, 255, 255))
        screen.blit(score_text, (180, 200))
        score_text = score_font.render(f"{int(max_combo)}", True , (255, 255, 255))
        screen.blit(score_text, (180, 300))

        music_font = pygame.font.Font('font/DungGeunMo.ttf', 50)
        score_text = score_font.render("SONG NAME", True, (255, 255, 255))
        screen.blit(score_text, (580, 200))
        score_text = music_font.render("1번 곡", True , (255, 255, 255))
        screen.blit(score_text, (580, 300))

        score_text = score_font.render("PLAY TIME", True, (255, 255, 255))
        screen.blit(score_text, (1150, 200))
        score_text = score_font.render(f"{elapsed_time:.2f}", True , (255, 255, 255))
        screen.blit(score_text, (1150, 300))

        score_text = score_font.render("PERPCDT", True, (255, 255, 255))
        screen.blit(score_text, (180, 400))
        score_text = score_font.render(f"{int(perpect_count)}", True , (255, 255, 255))
        screen.blit(score_text, (180, 500))

        score_text = score_font.render("GREAT", True, (255, 255, 255))
        screen.blit(score_text, (460, 400))
        score_text = score_font.render(f"{int(great_count)}", True , (255, 255, 255))
        screen.blit(score_text, (460, 500))

        score_text = score_font.render("GOOD", True, (255, 255, 255))
        screen.blit(score_text, (680, 400))
        score_text = score_font.render(f"{int(good_count)}", True , (255, 255, 255))
        screen.blit(score_text, (680, 500))

        score_text = score_font.render("BAD", True, (255, 255, 255))
        screen.blit(score_text, (880, 400))
        score_text = score_font.render(f"{int(bad_count)}", True , (255, 255, 255))
        screen.blit(score_text, (880, 500))

        score_text = score_font.render("WORST", True, (255, 255, 255))
        screen.blit(score_text, (1040, 400))
        score_text = score_font.render(f"{int(worst_count)}", True , (255, 255, 255))
        screen.blit(score_text, (1040, 500))

        score_text = score_font.render("MISS", True, (255, 255, 255))
        screen.blit(score_text, (1290, 400))
        score_text = score_font.render(f"{int(miss_count)}", True , (255, 255, 255))
        screen.blit(score_text, (1290, 500))


        pygame.display.flip()

        # 게임오버 후 10초 대기
        pygame.time.wait(10000)
        main = False
# 풀 콤보 엔딩=================================================================================================================================
    if miss_count == 0 and elapsed_time > music_length:
        screen.fill((0, 0, 0))
        game_over_font = pygame.font.Font(None, 90)
        game_over_text = game_over_font.render("FULL COMBO!!", True, (255, 255, 255))
        screen.blit(game_over_text, (620, 50))

        score_font = pygame.font.Font(None, 72)
        score_text = score_font.render("MAX COMBO", True, (255, 255, 255))
        screen.blit(score_text, (180, 200))
        score_text = score_font.render(f"{int(max_combo)}", True , (255, 255, 255))
        screen.blit(score_text, (180, 300))

        music_font = pygame.font.Font('font/DungGeunMo.ttf', 50)
        score_text = score_font.render("SONG NAME", True, (255, 255, 255))
        screen.blit(score_text, (580, 200))
        score_text = music_font.render("1번 곡", True , (255, 255, 255))
        screen.blit(score_text, (580, 300))

        score_text = score_font.render("PLAY TIME", True, (255, 255, 255))
        screen.blit(score_text, (1150, 200))
        score_text = score_font.render(f"{elapsed_time:.2f}", True , (255, 255, 255))
        screen.blit(score_text, (1150, 300))

        score_text = score_font.render("PERPCDT", True, (255, 255, 255))
        screen.blit(score_text, (180, 400))
        score_text = score_font.render(f"{int(perpect_count)}", True , (255, 255, 255))
        screen.blit(score_text, (180, 500))

        score_text = score_font.render("GREAT", True, (255, 255, 255))
        screen.blit(score_text, (460, 400))
        score_text = score_font.render(f"{int(great_count)}", True , (255, 255, 255))
        screen.blit(score_text, (460, 500))

        score_text = score_font.render("GOOD", True, (255, 255, 255))
        screen.blit(score_text, (680, 400))
        score_text = score_font.render(f"{int(good_count)}", True , (255, 255, 255))
        screen.blit(score_text, (680, 500))

        score_text = score_font.render("BAD", True, (255, 255, 255))
        screen.blit(score_text, (880, 400))
        score_text = score_font.render(f"{int(bad_count)}", True , (255, 255, 255))
        screen.blit(score_text, (880, 500))

        score_text = score_font.render("WORST", True, (255, 255, 255))
        screen.blit(score_text, (1040, 400))
        score_text = score_font.render(f"{int(worst_count)}", True , (255, 255, 255))
        screen.blit(score_text, (1040, 500))

        score_text = score_font.render("MISS", True, (255, 255, 255))
        screen.blit(score_text, (1290, 400))
        score_text = score_font.render(f"{int(miss_count)}", True , (255, 255, 255))
        screen.blit(score_text, (1290, 500))

        pygame.display.flip()

        # 게임엔딩 후 10초 대기
        pygame.time.wait(10000)
        main = False
# 게임 엔드=================================================================================================================================== 
    if game_end:
        screen.fill((0, 0, 0))
        game_over_font = pygame.font.Font(None, 90)
        game_over_text = game_over_font.render("GAME END", True, (255, 255, 255))
        screen.blit(game_over_text, (620, 50))

        score_font = pygame.font.Font(None, 72)
        score_text = score_font.render("MAX COMBO", True, (255, 255, 255))
        screen.blit(score_text, (180, 200))
        score_text = score_font.render(f"{int(max_combo)}", True , (255, 255, 255))
        screen.blit(score_text, (180, 300))

        music_font = pygame.font.Font('font/DungGeunMo.ttf', 50)
        score_text = score_font.render("SONG NAME", True, (255, 255, 255))
        screen.blit(score_text, (580, 200))
        score_text = music_font.render("1번 곡", True , (255, 255, 255))
        screen.blit(score_text, (580, 300))

        score_text = score_font.render("PLAY TIME", True, (255, 255, 255))
        screen.blit(score_text, (1150, 200))
        score_text = score_font.render(f"{elapsed_time:.2f}", True , (255, 255, 255))
        screen.blit(score_text, (1150, 300))

        score_text = score_font.render("PERPCDT", True, (255, 255, 255))
        screen.blit(score_text, (180, 400))
        score_text = score_font.render(f"{int(perpect_count)}", True , (255, 255, 255))
        screen.blit(score_text, (180, 500))

        score_text = score_font.render("GREAT", True, (255, 255, 255))
        screen.blit(score_text, (460, 400))
        score_text = score_font.render(f"{int(great_count)}", True , (255, 255, 255))
        screen.blit(score_text, (460, 500))

        score_text = score_font.render("GOOD", True, (255, 255, 255))
        screen.blit(score_text, (680, 400))
        score_text = score_font.render(f"{int(good_count)}", True , (255, 255, 255))
        screen.blit(score_text, (680, 500))

        score_text = score_font.render("BAD", True, (255, 255, 255))
        screen.blit(score_text, (880, 400))
        score_text = score_font.render(f"{int(bad_count)}", True , (255, 255, 255))
        screen.blit(score_text, (880, 500))

        score_text = score_font.render("WORST", True, (255, 255, 255))
        screen.blit(score_text, (1040, 400))
        score_text = score_font.render(f"{int(worst_count)}", True , (255, 255, 255))
        screen.blit(score_text, (1040, 500))

        score_text = score_font.render("MISS", True, (255, 255, 255))
        screen.blit(score_text, (1290, 400))
        score_text = score_font.render(f"{int(miss_count)}", True , (255, 255, 255))
        screen.blit(score_text, (1290, 500))

        pygame.display.flip()

        # 게임엔드 후 10초 대기
        pygame.time.wait(10000)
        main = False


