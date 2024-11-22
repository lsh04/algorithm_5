# UIUX.py 에 필요한 함수들을 저장한 곳, 게임 설명 및 옵션 관련 부분

# 수정 내용
# 119 line, 게임옵션 색상 변경함수, 옆 테두리 (255,255,255) -> outline_color 로 변경
# 게임 설명을 위한 진행바 함수 추가
import pygame, math, os

w = 1600
h = w*(9/16)

screen = pygame.display.set_mode((w, h))

keys = [0, 0, 0, 0]  # 키 누름 감지 리스트

# 노트 위치 계산 초시계====
elapsed_time = 0

#게임옵션을 위한 위치값======
x_offset = 0
#============
t1 = []
t2 = []
t3 = []
t4 = []

# 글씨 폰트 가져오기 플레이 타임 관련

Fpath = os.path.join("font")

spin = 0

# 색상 목록 정의================
OUTLINE_COLORS = [
    (255, 255, 255),  # 흰색
    (249, 29, 29),      # 빨간색
    (173, 248, 2),    # 녹색
    (30, 144, 255),   # 파란색
    (255, 215, 0)     # 노란색
]

# 테두리 색상 인덱스=================================
outline_color_index = 0  # 기본은 첫 번째 색상 (흰색)

# 색상 변경 함수=================================================================
def update_outline_color(new_index):
    global outline_color_index
    if 0 <= new_index < len(OUTLINE_COLORS):  # 유효한 색상 인덱스인지 체크
        outline_color_index = new_index

# 색상 반환 함수================================
def get_outline_color():
    return OUTLINE_COLORS[outline_color_index]

#플레이타임(UIUx.py 게임 설명을 위한 함수 변환)======================================================================
def playtime_explain (a_offset, z_offset):
        elapsed_minutes = int(elapsed_time // 60)
        elapsed_seconds = int(elapsed_time % 60)
        timer_font = pygame.font.Font(os.path.join(Fpath, "ingame_font.ttf"), int(w / 40 + z_offset))
        timer_text = timer_font.render(f"{elapsed_minutes:02}:{elapsed_seconds:02}", False, (255, 255, 255))
        screen.blit(timer_text, (w - 500, 50 + a_offset))  # 타이머 위치

# 판정선 (UIUX.py 게임 설명을 위한 함수 변환) =============================================
def hitbox_line_color (x_offset):
    pygame.draw.rect(screen, (0, 0, 0),
                    (785 - w / 8 + x_offset, (h / 12) * 9, 431, h / 2))
    pygame.draw.rect(screen, (255, 255, 255),   # 옆 테두리
                    (785 - w / 8 + x_offset, (h / 12) * 9, 431, h /2), int(h /100))

# 콤보 및 숫자 ( UIUX.py 게임 설명)====================================================================
def combo_and_rate(screen, x_offset, combo_value):
    rate = "PERFECT"  # 판정 텍스트
    
    # 폰트 설정
    ingame_font_rate = pygame.font.Font(os.path.join(Fpath, "ingame_font.ttf"), int(w / 30))
    ingame_font_combo = pygame.font.Font(os.path.join(Fpath, "ingame_font.ttf"), int(w / 20))
    
    # 콤보 텍스트 생성
    combo_text = ingame_font_combo.render(str(combo_value), True, (255, 255, 255))  # 흰색 텍스트
    combo_text_rect = combo_text.get_rect(center=(w / 2 + x_offset, (h / 12) * 4))  # 중앙 상단에 위치
    
    # 판정 텍스트 생성
    rate_text = ingame_font_rate.render(rate, True, (255, 255, 255))  # 흰색 텍스트
    rate_text_rect = rate_text.get_rect(center=(w / 2 + x_offset, (h / 12) * 8))  # 중앙 아래에 위치
    
    # 화면에 텍스트 그리기
    screen.blit(combo_text, combo_text_rect)  # 콤보 텍스트
    screen.blit(rate_text, rate_text_rect)    # 판정 텍스트

# 디자인 노트 입력시 나오는 이펙트(UIUX.py 게임 색상 및 설명을 위한 함수 변환)======================================================================
def count_effect_color (x_offset, keys):
    pygame.draw.rect(screen, (0, 0, 0), (w /2 - w / 8 + x_offset, -int(w / 100), w / 4, h + int(w / 50))) #geat background
    for i in range(3):
        i += 1
        pygame.draw.rect(screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)),
                            (w / 2 -w / 8 + w / 32 - (w / 32) * keys[0] + x_offset,
                            (h / 12) * 9 - (h / 30) * keys[0] * i, 100 * keys[0], (h / 35) / i))
    for i in range(3):
        i += 1
        pygame.draw.rect(screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)),
                            (w / 2 -w / 16 + w / 32 - (w / 32) * keys[1] +1 + x_offset,
                            (h / 12) * 9 - (h / 30) * keys[1] * i, 100 * keys[1],(h / 35) / i))
    for i in range(3):
        i += 1
        pygame.draw.rect(screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)),
                            (w / 2 +w / 32 - (w / 32) * keys[2] +2 + x_offset,
                            (h / 12) * 9 - (h / 30) * keys[2] * i, 100 * keys[2] , (h / 35) / i))
    for i in range(3):
        i += 1
        pygame.draw.rect(screen, (200 - ((200 / 7) * i), 200 - ((200 / 7) * i), 200 - ((200 / 7) * i)),
                            (w / 2 +w / 16 + w / 32 - (w / 32) * keys[3] +3 + x_offset,
                            (h / 12) * 9 - (h / 30) * keys[3] * i, 100 * keys[3], (h / 35) / i))

    pygame.draw.rect(screen, (255, 255, 255), (785 - w / 8 + x_offset, -int(w / 100), 431, h + int(w / 50)), int(w / 100)) #gear line 테두리선

# 게임옵션 색상 변경함수======================================================================================================================
def color_change(x_offset):
    outline_color = get_outline_color()
    pygame.draw.rect(screen, outline_color, (785 - w / 8 + x_offset, -int(w / 100), 431, h + int(w / 50)), int(w / 100)) #gear line 테두리선
    pygame.draw.rect(screen, (0, 0, 0), (785 - w / 8 + x_offset, (h / 12) * 9, 431, h / 2))
    pygame.draw.rect(screen, outline_color,(785 - w / 8 + x_offset, (h / 12) * 9, 431, h /2), int(h /100)) # 옆 테두리

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

        pygame.draw.circle(screen, (150, 150, 150), # 시계를 표현
                            (w / 2 + x_offset, (h / 24) * 21), (w / 20), int(h / 200)) 
        pygame.draw.line(screen, (150, 150, 150),
                        (w / 2 - math.sin(spin) * 25 * (w / 1600) + x_offset, (h / 24) * 21 - math.cos(spin) * 25 * (w / 1600)),
                        (w / 2 + math.sin(spin) * 25 * (w / 1600) + x_offset, (h / 24) * 21 + math.cos(spin) * 25 * (w / 1600)), int(w / 400))

        pygame.draw.rect(screen, (255 - 100 * keys[1], 255 - 100 * keys[1], 255 - 100 * keys[1]), # 두번째 발판의 배경, '흰' 색(테두리 아님)
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
        
            # 음악 진행 상황 그리기=====================================================================================================================================
def music_length(x_offset):
    bar_start = (640, 450)
    bar_end = (970, 450)
    bar_length = bar_end[0] - bar_start[0]

    # 색상 정의
    sky_blue = pygame.Color(135, 206, 235)

    # 진행 비율을 고정값으로 설정 (예: 0.5는 50% 진행)
    progress = 0.2  # 0.0에서 1.0 사이 값으로 설정

    # 진행 게이지 크기 및 위치 계산
    music_bar_width = bar_length * progress
    music_bar_height = 10
    music_bar_x = bar_start[0]
    music_bar_y = bar_start[1] - music_bar_height // 2

    # 진행 게이지 배경 (하얀색)
    pygame.draw.rect(screen, (255, 255, 255), (bar_start[0] + x_offset, music_bar_y, bar_length, music_bar_height), 2)
    # 현재 진행 게이지 (하늘색)
    pygame.draw.rect(screen, sky_blue, (music_bar_x + x_offset, music_bar_y, music_bar_width, music_bar_height))
    # 현재 진행 게이지 끝 점
    dot_x = bar_start[0] + progress * bar_length
    dot_y = bar_start[1]
    pygame.draw.circle(screen, (255, 255, 255), (int(dot_x) + x_offset, dot_y), 10)
