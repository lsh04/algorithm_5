# 미완성 파일입니다.
# 기존의 RTMG_3을 쓰시면 되는데 RTMG_3코드의 디자인 관련된 부분에서 코드 변경이 있을 수 있습니다. (게임 플레이 영향 x)
# " DungGeunMo.ttf " 는 font 폴더 에다가 넣어 주세요. 나머지는 따로 넣을 필요 x
import pygame, os

# Pygame 초기화
pygame.init()

# 화면 크기 설정
w = 1600
h = int(w * (9 / 16))
screen = pygame.display.set_mode((w, h))

# 한글 폰트 설정
font_path = os.path.join("font", "DungGeunMo.ttf")
keys = [1, 1, 1, 1]
# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (30, 144, 255)
OUTLINE_COLORS = [
    (255, 255, 255),  # 효과 1 - 흰색
    (255, 0, 0),      # 효과 2 - 빨간색
    (0, 255, 0),      # 효과 3 - 녹색
    (0, 0, 255),      # 효과 4 - 파란색
    (255, 255, 0)     # 효과 5 - 노란색
]

# 메인 메뉴 항목 및 서브 메뉴 항목 설정
main_menu_items = ["리듬게임", "곡 선택", "게임 옵션", "게임 설명", "게임 종료"]
song_menu_items = ["곡1", "곡2", "곡3", "뒤로가기"]
options_menu_items = ["테두리", "효과음", "노트", "뒤로가기"]
description_items = ["뒤로가기"]
selected_item = 1
selected_effect = [0, 0, 0]  # 각 항목의 기본 선택 효과 (0~4 순환)

# 게임 상태 설정
game_state = 0
outline_color_index = selected_effect[0]  # 테두리 색상 인덱스
spin = 0
# 게임 설명 문구 리스트
game_description_texts = [
    "왼쪽부터 D, F, J, K 키로 노트를 입력할 수 있습니다.",
    "콤보를 연속으로 성공하면 콤보 숫자가 올라갑니다.",
    "게임을 시작한 후, 우측 상단에 현재까지의 플레이 시간을 확인할 수 있습니다.",
    "초록색 바가 다 닳으면 게임오버입니다. (15번의 노트를 놓치면 게임 종료)",
]

# 현재 설명 페이지
current_description_page = 0

# 테두리 사각형 위치와 크기 설정 (곡 선택 화면에서 가운데로 이동)
outline_rect = pygame.Rect(1000, 100, 300, 600)

# design 에서의 함수 호출==========================================================================================
from design import hitbox_line_color, playtime_explain, count_effect_color, health_bar_explain, push_button_xoffset

# 방향키에 따른 <> 색상 설정
left_bracket_active = False
right_bracket_active = False

# 테두리 색상 그리기 함수, 나중에 바꿀 예정
def draw_outline_color(screen, color_index, outline_rect):
    pygame.draw.rect(screen, OUTLINE_COLORS[color_index], outline_rect, 5)

# 줄바꿈(game_state 4)
def wrap_text(text, font, max_width):
    """
    주어진 너비에 맞춰 텍스트를 자동으로 줄 바꿈하여 반환하는 함수
    :param text: 표시할 텍스트
    :param font: 텍스트를 렌더링할 폰트 객체
    :param max_width: 텍스트가 차지할 수 있는 최대 너비
    :return: 줄 바꿈된 텍스트 리스트
    """
    lines = []
    words = text.split(' ')  # 텍스트를 단어 단위로 나눔
    current_line = words[0]  # 첫 번째 단어로 시작

    for word in words[1:]:
        # 현재 줄에 단어를 추가했을 때 너비가 max_width를 초과하면 줄 바꿈
        if font.size(current_line + ' ' + word)[0] <= max_width:
            current_line += ' ' + word
        else:
            lines.append(current_line)  # 현재 줄을 결과에 추가
            current_line = word  # 새로운 줄로 시작

    lines.append(current_line)  # 마지막 줄을 결과에 추가
    return lines

# 게임 루프
running = True
while running:
    # 화면 초기화
    screen.fill((0, 0, 0))

    spin += 0.05

    # 메인 메뉴 화면
    if game_state == 0:
        for i, item in enumerate(main_menu_items):
            if item == "리듬게임":
                font_size = 80
            else:
                font_size = 50
            font = pygame.font.Font(font_path, font_size)

            color = RED if i == selected_item else WHITE
            text = font.render(item, True, color)
            rect = text.get_rect(center=(w // 2, 150 + i * 100))
            screen.blit(text, rect)

    # 곡 선택 화면
    elif game_state == 1:
        for i, song in enumerate(song_menu_items):
            color = RED if i == selected_item else WHITE
            text = font.render(song, True, color)
            rect = text.get_rect(center=(w // 2, 150 + i * 100))
            screen.blit(text, rect)
  
    # 게임 옵션 화면
    elif game_state == 2:
        for i, option in enumerate(options_menu_items):
            # 텍스트 위치
            x_rendering = 400
            y_rendering = 150 + i * 100

            # 선택된 항목일 경우(꺽쇠, 방향키)
            if i < len(options_menu_items) - 1 and i == selected_item:
                left_bracket_color = RED if left_bracket_active else WHITE
                right_bracket_color = RED if right_bracket_active else WHITE
                left_bracket = font.render("<", True, left_bracket_color)
                option_text = font.render(f"{option} {selected_effect[i] + 1}", True, WHITE)
                right_bracket = font.render(">", True, right_bracket_color)

                # 텍스트 중앙 정렬
                option_width = option_text.get_width()

                # 꺾쇠 기호와 텍스트 위치 계산
                left_bracket_x = x_rendering - option_width // 2 - left_bracket.get_width() - 50
                right_bracket_x = x_rendering + option_width // 2 + 50

                # 텍스트 중앙 정렬
                option_text_x = x_rendering - option_width // 2

                # 텍스트와 꺾쇠 기호 렌더링
                screen.blit(left_bracket, (left_bracket_x, y_rendering))
                screen.blit(option_text, (option_text_x, y_rendering))
                screen.blit(right_bracket, (right_bracket_x, y_rendering))
            else:
                color = RED if i == len(options_menu_items) - 1 and i == selected_item else WHITE
                text = font.render(option, True, color)

                # 선택되지 않은 항목도 텍스트 중앙에 맞추기
                text_width = text.get_width()
                text_x = x_rendering - text_width // 2

                # 텍스트 렌더링
                screen.blit(text, (text_x, y_rendering))


        # 오른쪽 테두리 사각형 그리기 (게임 옵션에서 선택된 색상으로)
        outline_color_index = selected_effect[0]  # 테두리 색상을 선택한 값으로 업데이트
        draw_outline_color(screen, outline_color_index, outline_rect)

    # 게임 화면 (곡1~3 선택 후 진입), 일부 수정 예정
    elif game_state == 3:
        import RTMG_3
        RTMG_3.run_game()

    # 게임 설명 화면
    elif game_state == 4:
        for i, item in enumerate(main_menu_items):
            # 설명 페이지 텍스트 가져오기
            description = game_description_texts[current_description_page]
            # 자동 줄 바꿈 처리
            wrapped_lines = wrap_text(description, font, w - 1000)  # 화면 너비에서 여백을 뺀 너비

            # 텍스트 출력
            y_offset = h // 2 - len(wrapped_lines) * font.get_height() // 2  # 세로로 중앙 배치
            for line in wrapped_lines:
                description_text = font.render(line, True, WHITE)
                rect = description_text.get_rect(topleft=(200, y_offset)) # 왼쪽에 맞춰서 출력
            
                if current_description_page in [0, 1]:  # 0: D, F, J, K 키 안내 / 1: 콤보 안내
                    x_offset = 350
                    count_effect_color(x_offset)
                    hitbox_line_color(x_offset)
                    push_button_xoffset(x_offset)
                

                if current_description_page in [2]:  # 게임시간
                    a_offset = 350
                    z_offset = 50
                    playtime_explain(x_offset, z_offset)

                if current_description_page in [3]:  # 게임오버
                    c_offset = 1000
                    d_offset = 400
                    e_offset = 100
                    health_bar_explain (c_offset, d_offset, e_offset)

                screen.blit(description_text, rect )
                y_offset += font.get_height()  # 한 줄씩 내려서 표시

            # 좌우 키 설명
            left_bracket_color = RED if left_bracket_active else WHITE
            right_bracket_color = RED if right_bracket_active else WHITE

            # 텍스트 렌더링
            left_key_text = font.render("<", True, left_bracket_color)
            right_key_text = font.render(">", True, right_bracket_color)

            # 좌우 키 위치
            left_key_rect = left_key_text.get_rect(midleft=(50, h // 2))  # 화면 왼쪽 끝에서 50px 안쪽
            right_key_rect = right_key_text.get_rect(midright=(w - 50, h // 2))  # 화면 오른쪽 끝에서 50px 안쪽
            screen.blit(left_key_text, left_key_rect)
            screen.blit(right_key_text, right_key_rect)

            # 뒤로가기 버튼
            back_text = font.render("뒤로가기", True, RED if selected_item == len(description_items) else WHITE)
            back_rect = back_text.get_rect(topleft=(20, h - 100))
            screen.blit(back_text, back_rect)

    # 이벤트 처리(키입력 및 선택)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            
            # 메인 메뉴(키)
            if game_state == 0:
                if event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(main_menu_items)
                    if selected_item == 0:
                        selected_item = 1
                elif event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(main_menu_items)
                    if selected_item == 0:
                        selected_item = 4
                elif event.key == pygame.K_RETURN:
                    if selected_item == 1:
                        game_state = 1
                        selected_item = 0
                    elif selected_item == 2:
                        game_state = 2
                        selected_item = 0
                    elif selected_item == 3:
                        game_state = 4
                    elif selected_item == 4:
                        running = False

            # 곡 선택 화면(키)
            elif game_state == 1:
                if event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(song_menu_items)
                elif event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(song_menu_items)
                elif event.key == pygame.K_RETURN:
                    if selected_item == len(song_menu_items) - 1:
                        game_state = 0
                        selected_item = 1
                    else:
                        game_state = 3  # 곡 선택 시 게임 화면으로 이동
                        selected_item = 1

            # 게임 옵션 화면(키)
            elif game_state == 2:
                if event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(options_menu_items)
                elif event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(options_menu_items)
                elif event.key == pygame.K_LEFT:
                    if selected_item < len(options_menu_items) - 1:
                        left_bracket_active = True
                        right_bracket_active = False
                        selected_effect[selected_item] = (selected_effect[selected_item] - 1) % 5
                elif event.key == pygame.K_RIGHT:
                    if selected_item < len(options_menu_items) - 1:
                        left_bracket_active = False
                        right_bracket_active = True
                        selected_effect[selected_item] = (selected_effect[selected_item] + 1) % 5
                elif event.key == pygame.K_RETURN:
                    if selected_item == len(options_menu_items) - 1:
                        game_state = 0
                        selected_item = 1
                    else:
                        print(f"{options_menu_items[selected_item]} {selected_effect[selected_item] + 1} 활성화됨")

            # 게임 설명(키)
            elif game_state == 4:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        # 설명 항목에서 '뒤로가기'로 이동
                        selected_item = (selected_item + 1) % (len(description_items) + 1)
                    elif event.key == pygame.K_UP:
                        # '뒤로가기'에서 설명 항목으로 이동
                        selected_item = (selected_item - 1) % (len(description_items) + 1)
                    elif event.key == pygame.K_LEFT:  # 왼쪽 페이지 이동
                        left_bracket_active = True
                        right_bracket_active = False
                        current_description_page = (current_description_page - 1) % len(game_description_texts)
                    elif event.key == pygame.K_RIGHT:  # 오른쪽 페이지 이동
                        right_bracket_active = True
                        left_bracket_active = False
                        current_description_page = (current_description_page + 1) % len(game_description_texts)
                    elif event.key == pygame.K_RETURN:
                        if selected_item == len(description_items):  # '뒤로가기' 선택 시
                            game_state = 0  # 메인 화면으로 이동
                            selected_item = 1
                

    # 화면 업데이트
    pygame.display.flip()

# Pygame 종료
pygame.quit()
