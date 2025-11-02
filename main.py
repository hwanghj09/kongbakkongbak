import pygame
import os
import time

# 초기화
pygame.init()
pygame.font.init()

# 화면 크기 및 색상 설정
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
RECT_WIDTH = 100
RECT_HEIGHT = 20
BACKGROUND_COLOR = (0, 0, 0)  # 배경 색상: 검은색
LINE_COLOR = (200, 200, 220)  # 텍스트 및 선 색상: 밝은 회색
PERFECT_COLOR = (0, 255, 100)  # Perfect 메시지 색상: 연한 초록색
GOOD_COLOR = (255, 200, 0)  # Good 메시지 색상: 주황색
TIME_COLOR = (200, 200, 220)  # 시간 텍스트 색상: 밝은 회색
BUTTON_COLOR = (50, 50, 70)  # 버튼 색상: 어두운 회색
BUTTON_HOVER_COLOR = (70, 70, 90)  # 버튼 호버 색상: 밝은 회색
# 화면 설정
score = {
    "perfect": 0,
    "good": 0,
    "bad": 0
}

f_score = 0
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("리듬 게임")
all_sprites = pygame.sprite.Group()
# 폰트 설정
font_size = 32
drum_sounds = [
    pygame.mixer.Sound('audio/drum1.ogg'),
    pygame.mixer.Sound('audio/drum2.ogg'),
    pygame.mixer.Sound('audio/drum3.ogg'),
    pygame.mixer.Sound('audio/drum4.ogg')
]
font = pygame.font.Font("font/NotoSansCJKkr-Regular.otf", font_size)
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((RECT_WIDTH, RECT_HEIGHT))
        self.image.fill(LINE_COLOR)
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def update(self):
        self.rect.y += 5  # 블록이 떨어지는 속도
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()  # 화면을 넘어가면 블록 제거
            score["bad"] += 1
def draw_text(text, font, color, surface, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)

def draw_background():
    screen.fill(BACKGROUND_COLOR)

def show_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

        draw_background()

        mouse_x, mouse_y = pygame.mouse.get_pos()

        # "게임 시작" 버튼
        if (SCREEN_WIDTH // 2 - 100 <= mouse_x <= SCREEN_WIDTH // 2 + 100 and 
            SCREEN_HEIGHT // 2 - 50 <= mouse_y <= SCREEN_HEIGHT // 2):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50))
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 50))
        draw_text("게임 시작", font, LINE_COLOR, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)
        
        # "나가기" 버튼
        if (SCREEN_WIDTH // 2 - 100 <= mouse_x <= SCREEN_WIDTH // 2 + 100 and 
            SCREEN_HEIGHT // 2 + 30 <= mouse_y <= SCREEN_HEIGHT // 2 + 80):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 30, 200, 50))
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 30, 200, 50))
        draw_text("나가기", font, LINE_COLOR, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)

        # "노래 만들기" 버튼
        if (SCREEN_WIDTH // 2 - 100 <= mouse_x <= SCREEN_WIDTH // 2 + 100 and 
            SCREEN_HEIGHT // 2 + 110 <= mouse_y <= SCREEN_HEIGHT // 2 + 160):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 110, 200, 50))
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 110, 200, 50))
        draw_text("노래 만들기", font, LINE_COLOR, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 140)
        
        if pygame.mouse.get_pressed()[0]:
            if (SCREEN_WIDTH // 2 - 100 <= mouse_x <= SCREEN_WIDTH // 2 + 100 and 
                SCREEN_HEIGHT // 2 - 50 <= mouse_y <= SCREEN_HEIGHT // 2):
                show_song_selection()
            elif (SCREEN_WIDTH // 2 - 100 <= mouse_x <= SCREEN_WIDTH // 2 + 100 and 
                  SCREEN_HEIGHT // 2 + 30 <= mouse_y <= SCREEN_HEIGHT // 2 + 80):
                pygame.quit()
                return
            elif (SCREEN_WIDTH // 2 - 100 <= mouse_x <= SCREEN_WIDTH // 2 + 100 and 
                  SCREEN_HEIGHT // 2 + 110 <= mouse_y <= SCREEN_HEIGHT // 2 + 160):
                create_new_song()

        pygame.display.flip()
        pygame.time.Clock().tick(30)

def show_song_selection():
    song_folder = 'song'
    song_files = [f for f in os.listdir(song_folder) if f.endswith('.ini')]
    if not song_files:
        song_files.append('사용 가능한 노래 없음')

    selected_song = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_RETURN and selected_song:
                    game_loop(selected_song)
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                for i, song_file in enumerate(song_files):
                    box_x = SCREEN_WIDTH // 2 - 150
                    box_y = 200 + i * 60 - 20
                    if (box_x <= mouse_x <= box_x + 300 and 
                        box_y <= mouse_y <= box_y + 50):
                        selected_song = song_file
                
                if selected_song:
                    start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 140, 200, 50)
                    if start_button_rect.collidepoint(mouse_x, mouse_y):
                        game_loop(selected_song)
                        return  
                
                back_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 50)
                if back_button_rect.collidepoint(mouse_x, mouse_y):
                    return

        draw_background()

        draw_text("노래 선택", font, LINE_COLOR, screen, SCREEN_WIDTH // 2, 100)

        y_offset = 200
        for i, song_file in enumerate(song_files):
            box_x = SCREEN_WIDTH // 2 - 150
            box_y = y_offset - 20
            if song_file == selected_song:
                pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (box_x, box_y, 300, 50))
            else:
                pygame.draw.rect(screen, BUTTON_COLOR, (box_x, box_y, 300, 50))
            draw_text(os.path.splitext(song_file)[0], font, LINE_COLOR, screen, SCREEN_WIDTH // 2, y_offset)
            y_offset += 60

        start_button_color = BUTTON_HOVER_COLOR if selected_song else BUTTON_COLOR
        pygame.draw.rect(screen, start_button_color, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 140, 200, 50))
        draw_text("게임 시작", font, LINE_COLOR, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 115)

        pygame.draw.rect(screen, BUTTON_COLOR, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 70, 200, 50))
        draw_text("메뉴로 돌아가기", font, LINE_COLOR, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 45)

        pygame.display.flip()
        pygame.time.Clock().tick(30)

def create_new_song():
    song_name = ""
    new_song_data = []
    recording = False
    start_time = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif not recording:
                    if event.key == pygame.K_RETURN:
                        recording = True
                        start_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_BACKSPACE:
                        song_name = song_name[:-1]
                    elif event.unicode.isalnum():
                        song_name += event.unicode
                else:
                    if event.key == pygame.K_RETURN:
                        recording = False
                        file_path = os.path.join('song', f"{song_name}.ini")
                        with open(file_path, 'w') as file:
                            file.write(f"MaxScore: {len(new_song_data) * 2}\n\n")
                            for time_ms, notes in new_song_data:
                                minutes = time_ms // 60000
                                seconds = (time_ms // 1000) % 60
                                milliseconds = time_ms % 1000
                                time_str = f"{minutes:02}:{seconds:02}:{milliseconds:03}"
                                file.write(f"{time_str} - {notes}\n")
                            file.write("END\n")
                        return
                    elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        current_time = pygame.time.get_ticks()
                        time_elapsed = current_time - start_time
                        if event.key == pygame.K_1:
                            note = "1000"
                        elif event.key == pygame.K_2:
                            note = "0100"
                        elif event.key == pygame.K_3:
                            note = "0010"
                        elif event.key == pygame.K_4:
                            note="0001"
                        new_song_data.append((time_elapsed, note))

        draw_background()
        draw_text("노래 제목:", font, LINE_COLOR, screen, SCREEN_WIDTH // 2, 200)
        draw_text(song_name, font, LINE_COLOR, screen, SCREEN_WIDTH // 2, 250)
        draw_text("1,2,3,4 버튼으로 노트를 추가하세요", font, LINE_COLOR, screen, SCREEN_WIDTH // 2, 300)

        if not recording:
            draw_text("엔터 키를 눌러 녹음을 시작하세요", font, LINE_COLOR, screen, SCREEN_WIDTH // 2, 350)
        else:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000
            draw_text(f"녹음 중: {elapsed_time:.2f}초", font, LINE_COLOR, screen, SCREEN_WIDTH // 2, 350)

        pygame.display.flip()
        pygame.time.Clock().tick(30)

def read_song_file(filename):
    with open(os.path.join('song', filename), 'r') as file:
        lines = file.readlines()
    
    max_score = int(lines[0].split(':')[1].strip())
    
    note_data = []
    for line in lines[2:]:
        if line.strip() == "END":
            break
        time, notes = line.strip().split(' - ')
        minutes, seconds, milliseconds = map(int, time.split(':'))
        time_ms = (minutes * 60 + seconds) * 1000 + milliseconds
        note_data.append((time_ms, notes))
    
    return max_score, note_data

def create_block(note_pattern):
    blocks = []
    for i, note in enumerate(note_pattern):
        if note == '1':
            block_x = i * (SCREEN_WIDTH // 4)
            new_block = Block(block_x, 0)
            all_sprites.add(new_block) 
            blocks.append(new_block)
    return blocks

def calculate_final_score():
    return (score["perfect"] * 2) + (score["good"] * 1) + (score["bad"] * -1)
def game_loop(song_file):
    all_sprites.empty()
    score = {"perfect": 0, "good": 0, "bad": 0}
    show_perfect_message = False
    show_good_message = False
    message_type = None
    message_start_time = 0

    max_score, note_data = read_song_file(song_file)
    note_index = 0

    # 노래 파일 로드 및 재생
    song_name = os.path.splitext(song_file)[0]
    pygame.mixer.music.load(f'song/{song_name}.ogg')
    pygame.mixer.music.play()
    start_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        current_time = pygame.time.get_ticks() - start_time

        # 노트 생성
        while note_index < len(note_data) and current_time >= note_data[note_index][0]:
            new_blocks = create_block(note_data[note_index][1])
            all_sprites.add(new_blocks)
            note_index += 1

        line_y_position = SCREEN_HEIGHT - (RECT_HEIGHT + 10)
        keys = pygame.key.get_pressed()
        if any(keys):
            closest_block = None
            closest_distance = float('inf')
            for block in all_sprites:
                distance = block.rect.bottom - line_y_position
                if distance < closest_distance and distance >= 0:
                    closest_distance = distance
                    closest_block = block

            if closest_block:
                column_index = closest_block.rect.x // (SCREEN_WIDTH // 4)

                if line_y_position <= closest_block.rect.top <= SCREEN_HEIGHT:
                    score['perfect'] += 1
                    show_perfect_message = True
                    message_type = 'perfect'
                    message_start_time = pygame.time.get_ticks()
                else:
                    score['good'] += 1
                    message_type = 'good'
                    show_good_message = True
                    message_start_time = pygame.time.get_ticks()
                
                if column_index >= 0 and column_index < len(drum_sounds):
                    drum_sounds[1].play()

                closest_block.kill()

        draw_background()

        line_width = SCREEN_WIDTH // 4
        for i in range(1, 4):
            pygame.draw.line(screen, LINE_COLOR, (i * line_width, 0), (i * line_width, SCREEN_HEIGHT), 2)

        pygame.draw.line(screen, LINE_COLOR, (0, line_y_position), (SCREEN_WIDTH, line_y_position), 2)

        all_sprites.update()
        all_sprites.draw(screen)
        draw_text(f"Perfect: {score['perfect']} Good: {score['good']} Bad: {score['bad']}", font, LINE_COLOR, screen, SCREEN_WIDTH // 2, 70)

        draw_text(f"Time: {current_time // 60000}:{(current_time // 1000) % 60:02d}", font, TIME_COLOR, screen, SCREEN_WIDTH // 2, 110)

        if show_perfect_message and message_type == 'perfect':
            draw_text("Perfect!", font, PERFECT_COLOR, screen, SCREEN_WIDTH // 2, 150)

        if show_good_message and message_type == 'good':
            draw_text("Good!", font, GOOD_COLOR, screen, SCREEN_WIDTH // 2, 150)

        current_time = pygame.time.get_ticks()
        if message_type and current_time - message_start_time > 500:
            show_perfect_message = False
            show_good_message = False
            message_type = None

        if note_index >= len(note_data) and not all_sprites:
            pygame.mixer.music.stop()  # 노래 정지
            final_score = calculate_final_score()
            draw_text(f"Final Score: {final_score}", font, LINE_COLOR, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            pygame.display.flip()
            pygame.time.delay(3000)
            return

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def main():
    while True:
        show_menu()

main()

pygame.quit()
