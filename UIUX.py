# 29 line  변수와 32 line 주석 참고

# 수정 내용
# 28 line  "랭킹 보기" 추가
# 240 line 랭킹 UI와 뒤로가기 버튼 추가 (game state = 5) <- 여기에서 수정 하시면 돼요
# 편의성 수정: 각각의 뒤로가기 선택시 해당됐던 문구에 상호작용이 돼 있도록 수정
# ex) 게임 옵션 뒤로가기 선택을 눌렀을 때 메인 화면의 상호작용 키(빨간색) 이/가 무조건 곡 선택으로 되어있었음 다시 위아래 키를 눌러야 하는 번거로움 최소화
# 게임 설명에 진행바 관련 설명 추가
import pygame, os

# Pygame 초기화
pygame.init()

# 화면 크기 설정
w = 1600
h = int(w * (9 / 16))
screen = pygame.display.set_mode((w, h))

# 한글 폰트 설정
font_path = os.path.join("font", "DungGeunMo.ttf")

# 색상 정의
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (30, 144, 255)

# 메인 메뉴 항목 및 서브 메뉴 항목 설정
main_menu_items = ["리듬게임", "곡 선택", "게임 옵션", "게임 설명", "랭킹 보기","게임 종료"]
song_menu_items = ["곡1", "곡2", "뒤로가기"]

#게임 실행 파일
song_files = {
    "곡1": "RTMG_5",        # song_menu_tiems 에 있는 "곡1" 을 "음악"으로 수정 시
                            # song files 에 있는 "곡1" 도 "음악"으로 변경해야함, 꼭 뒤로가기 앞에 적을 것
    "곡2": "RTMG_3 copy",   # song files 에 있는  "RTMG_3"는 실행할 파일 적기
}                           # 테스트 해볼려고 '개인적으로' 곡2 누를시 RTMG_3_copy 파일로 가는걸 만들었습니다.

options_menu_items = ["테두리", "뒤로가기"]
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
    "연속 성공 시 콤보가 올라가며, 판정에 따라 perfect, great 등 시각적 효과가 추가됩니다.",
    "플레이 화면 중앙 상단에 현재 게임 진행 상황이 표시됩니다.",
    "우측 상단에 현재까지의 플레이 시간을 확인할 수 있습니다.",
    "초록색 바가 다 닳으면 게임오버입니다. (15번의 노트를 놓치면 게임 종료)",
]

# 현재 설명 페이지
current_description_page = 0

# design 에서의 함수 호출==========================================================================================
from design import hitbox_line_color, playtime_explain, count_effect_color, health_bar_explain, push_button_xoffset,combo_and_rate, update_outline_color,color_change, music_length

# 방향키에 따른 <> 색상 설정
left_bracket_active = False
right_bracket_active = False

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
            y_rendering = 400 + i * 100
            x_offset = 350
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

        outline_color_index = selected_effect[0]  # 테두리 색상을 선택한 값으로 업데이트
        update_outline_color(outline_color_index)  # 색상 업데이트
        color_change(x_offset)
        push_button_xoffset(x_offset)

# 게임 화면 (곡1~3 선택 후 진입)
    elif game_state == 3:
        selected_song = song_menu_items[selected_item]  # 선택한 곡 이름
        song_file = song_files.get(selected_song)  # 해당 곡에 맞는 파일 가져오기
        song_module = __import__(song_file)  # 모듈을 동적으로 불러오기
        song_module.run_game()  # 해당 모듈의 run_game 함수 실행


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
            
                if current_description_page in [0]:  # 0: D, F, J, K 키 안내
                    x_offset = 350
                    keys = [1,1,1,1]
                    count_effect_color(x_offset, keys)
                    hitbox_line_color(x_offset)
                    push_button_xoffset(x_offset)

                if current_description_page in [1]:  #1: 콤보 안내
                    x_offset = 350
                    keys = [0,0,0,0]
                    count_effect_color(x_offset, keys)
                    hitbox_line_color(x_offset)
                    push_button_xoffset(x_offset)
                    combo_and_rate(screen, x_offset, combo_value=15)                

                if current_description_page in [2]:  # 2: 진행바 표시
                    x_offset = 350
                    music_length(x_offset)


                if current_description_page in [3]:  # 3: 게임시간
                    a_offset = 350
                    z_offset = 50
                    playtime_explain(x_offset, z_offset)

                if current_description_page in [4]: # 4:게임오버
                    c_offset = 1000
                    d_offset = 400
                    e_offset = 100
                    health_bar_explain (c_offset, d_offset, e_offset)

                screen.blit(description_text, rect )
                y_offset += font.get_height()  # 한 줄씩 내려서 표시(줄바꿈 관련)

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

# 랭킹 보기 시스템 화면=================================================================================================
    elif game_state == 5:

            # 뒤로가기 버튼(현재 좌측 하단에 위치)
            back_text = font.render("뒤로가기", True, RED)
            back_rect = back_text.get_rect(topleft=(20, h - 100)) # topleft = 왼쪽을 기준으로, 20 = x 좌표 이동, h - 100 = 높이
            screen.blit(back_text, back_rect)
#===========================================================================================================================
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
                        game_state = 5
                    elif selected_item == 5:
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
                        song_selected = song_menu_items[selected_item]

            # 게임 옵션 화면(키)
            elif game_state == 2:
                if event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(options_menu_items)
                elif event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(options_menu_items)
                
                elif event.key == pygame.K_LEFT:
                    if selected_item < len(options_menu_items) - 1:                       
                        selected_effect[selected_item] = (selected_effect[selected_item] - 1) % 5
                        update_outline_color(selected_effect[selected_item])  # 색상 업데이트
                        left_bracket_active = True
                        right_bracket_active = False
                
                elif event.key == pygame.K_RIGHT:
                    if selected_item < len(options_menu_items) - 1:                        
                        selected_effect[selected_item] = (selected_effect[selected_item] + 1) % 5
                        update_outline_color(selected_effect[selected_item])  # 색상 업데이트
                        left_bracket_active = False
                        right_bracket_active = True
                
                elif event.key == pygame.K_RETURN:
                    if selected_item == len(options_menu_items) - 1:
                        game_state = 0
                        selected_item = 2

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
                            selected_item = 3

            # 랭킹 보기의 뒤로가기 키 설정 (Enter 누를 시 뒤로가기)
            elif game_state == 5:  # 현재 상태가 랭킹 보기 화면일 때
                if event.key == pygame.K_RETURN:  # Enter 키를 눌렀을 경우
                    game_state = 0  # 메인 화면으로 이동
                    selected_item = 4  # 선택된 아이템 초기화

    # 화면 업데이트
    pygame.display.flip()

# Pygame 종료
pygame.quit()