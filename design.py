# UIUX.py 에 필요한 함수들을 저장한 곳, 게임 설명 및 옵션 관련 부분
import pygame, math, time, os

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
#게임옵션을 위한 위치값=========================
x_offset = 0
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
rate_text = ingame_font_rate.render(str(rate), False, (255, 255, 255))

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

#플레이타임(UIUx.py 게임 설명을 위한 함수 변환)=================================================================================
def playtime_explain (a_offset, z_offset):
        elapsed_minutes = int(elapsed_time // 60)
        elapsed_seconds = int(elapsed_time % 60)
        timer_font = pygame.font.Font(os.path.join(Fpath, "ingame_font.ttf"), int(w / 40 + z_offset))
        timer_text = timer_font.render(f"{elapsed_minutes:02}:{elapsed_seconds:02}", False, (255, 255, 255))
        screen.blit(timer_text, (w - 500, 50 + a_offset))  # 타이머 위치
# 판정선 (UIUX.py 게임 설명, 옵션 변경을 위한 함수 변환) =====================================================
def hitbox_line_color (x_offset):
    pygame.draw.rect(screen, (0, 0, 0),
                    (w /2 - w / 8 + x_offset, (h / 12) * 9, w / 4, h / 2))
    pygame.draw.rect(screen, (255, 255, 255),   # 옆 테두리
                    (w / 2 - w / 8 + x_offset, (h / 12) * 9, w / 4, h /2), int(h /100))

# 디자인 노트 입력시 나오는 이펙트(UIUX.py 게임 색상 및 옵션 변경을 위한 함수 변환)===========================================================================================
def count_effect_color (x_offset):
    pygame.draw.rect(screen, (0, 0, 0), (w /2 - w / 8 + x_offset, -int(w / 100), w / 4, h + int(w / 50))) #geat background

    for i in range(3):
        i += 1
        pygame.draw.rect(screen, (200 - ((200 / 7) * i),
                                    200 - ((200 / 7) * i),
                                    200 - ((200 / 7) * i)),
                            (w / 2 -w / 8 + w / 32 - (w / 32) * keys[0] + x_offset, (h / 12) * 9 - (h / 30) * keys[0] * i, w / 16 * keys[0], (h / 35) / i))
    for i in range(3):
        i += 1
        pygame.draw.rect(screen, (200 - ((200 / 7) * i),
                                    200 - ((200 / 7) * i),
                                    200 - ((200 / 7) * i)),
                            (w / 2 -w / 16 + w / 32 - (w / 32) * keys[1] + x_offset, (h / 12) * 9 - (h / 30) * keys[1] * i, w / 16 * keys[1], (h / 35) / i))
    for i in range(3):
        i += 1
        pygame.draw.rect(screen, (200 - ((200 / 7) * i),
                                    200 - ((200 / 7) * i),
                                    200 - ((200 / 7) * i)),
                            (w / 2 +w / 32 - (w / 32) * keys[2] + x_offset, (h / 12) * 9 - (h / 30) * keys[2] * i, w / 16 * keys[2] , (h / 35) / i))
    for i in range(3):
        i += 1
        pygame.draw.rect(screen, (200 - ((200 / 7) * i),
                                    200 - ((200 / 7) * i),
                                    200 - ((200 / 7) * i)),
                            (w / 2 +w / 16 + w / 32 - (w / 32) * keys[3] + x_offset,(h / 12) * 9 - (h / 30) * keys[3] * i, w / 16 * keys[3], (h / 35) / i))

    pygame.draw.rect(screen, (255, 255, 255), (w / 2 - w / 8 + x_offset, -int(w / 100), w / 4, h + int(w / 50)), int(w / 100)) #gear line 옆에 있는 라인

# 생명력=========================================
max_health = 100
current_health = max_health

# 생명력 게이지 바(UIUX.py 게임 설명을 및 위치 이동을 위한 함수 변환)===========================================================

def health_bar_explain (c_offset, d_offset, e_offset):
    health_bar_width = (w / 6) * (current_health / max_health)
    health_bar_height = h / 40
    health_bar_x = w / 50 + c_offset
    health_bar_y = h / 50 + d_offset

# 배경 게이지 (빨간색)
    pygame.draw.rect(screen, (255, 0, 0),
                        (health_bar_x, health_bar_y, w / 6 + e_offset, health_bar_height))
# 현재 체력 게이지 (초록색)
    pygame.draw.rect(screen, (0, 255, 0),
                        (health_bar_x, health_bar_y, health_bar_width, health_bar_height))

# 게이지 테두리
    pygame.draw.rect(screen, (255, 255, 255),
                        (health_bar_x, health_bar_y, w / 6 + e_offset, health_bar_height), 2)
    
# 누르는 발판 (게임 설명 및 위치 이동을 위한 함수 변환)===============================================================================
def push_button_xoffset(x_offset):
        pygame.draw.rect(screen, (255 - 100 * keys[0],255 - 100 * keys[0], # 첫 번째 발판의 누를 때 나오는 색
                                  255 - 100 * keys[0]),
                        (w / 2 - w / 9 + x_offset, (h / 24) * 19 + (h / 48) * keys[0], w / 27, h / 8), int(h / 150))
        
        pygame.draw.rect(screen, (255 - 100 * keys[3],  # 세 번째 발판의 누를 때 나오는 색
                                  255 - 100 * keys[3], 255 - 100 * keys[3]),
                        (w / 2 + w / 13.5 + x_offset, (h / 24) * 19 + (h / 48) * keys[3], w / 27, h / 8), int(h / 150))

        pygame.draw.circle(screen, (150, 150, 150),
                            (w / 2 + x_offset, (h / 24) * 21), (w / 20), int(h / 200))
        
        pygame.draw.line(screen, (150, 150, 150),
                        (w / 2 - math.sin(spin) * 25 * (w / 1600) + x_offset, (h / 24) * 21 - math.cos(spin) * 25 * (w / 1600)),
                        (w / 2 + math.sin(spin) * 25 * (w / 1600) + x_offset, (h / 24) * 21 + math.cos(spin) * 25 * (w / 1600)), int(w / 400))

        pygame.draw.rect(screen, (255 - 100 * keys[1], 255 - 100 * keys[1], # 두번째 발판의 배경, '흰' 색(테두리 아님)
                                  255 - 100 * keys[1]),
                        (w / 2 - w / 18 + x_offset, (h / 48) * 39 + (h / 48) * keys[1], w / 27, h / 8))
        pygame.draw.rect(screen, (0,0, 0),  # 두번째 발판의 배경에 두 줄이 그려진 '검은' 색 
                        (w / 2 - w / 18 + x_offset, (h / 48) * 43 + (h / 48) * (keys[1] * 1.2), w / 27, h / 64), int(h / 150))
        pygame.draw.rect(screen, (50,50, 50),   # 두번째 발판 테두리 (배경이 더 크다, 배경에다가 테두리를 입힌 느낌)
                        (w / 2 - w / 18 + x_offset, (h / 48) * 39 + (h / 48) * keys[1], w / 27, h / 8), int(h / 150))

        pygame.draw.rect(screen, (255 - 100 * keys[2],
                                  255 - 100 * keys[2], 255 - 100 * keys[2]),
                        (w / 2 + w / 58 + x_offset, (h / 48) * 39 + (h / 48) * keys[2], w / 27, h / 8))
        pygame.draw.rect(screen, (0,0, 0),
                        (w / 2 + w / 58 + x_offset, (h / 48) * 43 + (h / 48) * (keys[2] * 1.2), w / 27, h / 64), int(h / 150))
        pygame.draw.rect(screen, (50,50, 50),
                        (w / 2 + w / 58 + x_offset, (h / 48) * 39 + (h / 48) * keys[2], w / 27, h / 8), int(h / 150))

# 판정 코드=======================================
rate_data = [0, 0, 0, 0]

def rating(n):
    global combo, miss_anim, last_combo, combo_effect, combo_effect2, combo_time, rate, current_health
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