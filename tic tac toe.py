import pygame
import sys
from pygame.locals import *
import random

def draw_text(surface, text, font, color, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != " ":
            return row[0]

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]

    return None

def is_full(board):
    for row in board:
        if " " in row:
            return False
    return True

def ai_move(board, difficulty):
    if difficulty == "Easy":
        empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == " "]
        return random.choice(empty_cells)
    elif difficulty == "Hard":
        # Simple strategy for hard mode (improvements can be made)
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "O"
                    if check_winner(board) == "O":
                        return row, col
                    board[row][col] = " "
        empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == " "]
        return random.choice(empty_cells)

def tic_tac_toe(mode, difficulty=None):
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        print_board(board)
        print(f"Player {current_player}'s turn.")

        if mode == "Computer" and current_player == "O":
            row, col = ai_move(board, difficulty)
        else:
            try:
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter column (0-2): "))
            except ValueError:
                print("Invalid input. Please enter numbers between 0 and 2.")
                continue

        if row < 0 or row > 2 or col < 0 or col > 2:
            print("Invalid position. Please enter numbers between 0 and 2.")
            continue

        if board[row][col] != " ":
            print("Cell already taken. Choose another.")
            continue

        board[row][col] = current_player

        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"Player {winner} wins!")
            break

        if is_full(board):
            print_board(board)
            print("It's a tie!")
            break

        current_player = "O" if current_player == "X" else "X"

def main_menu():
    pygame.init()

    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Tic Tac Toe")

    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 30)
    clock = pygame.time.Clock()

    while True:
        screen.fill((30, 30, 30))
        draw_text(screen, "Tic Tac Toe", font, (255, 255, 255), 300, 50)

        mx, my = pygame.mouse.get_pos()

        play_friend_button = pygame.Rect(200, 150, 200, 50)
        play_computer_button = pygame.Rect(200, 220, 200, 50)

        pygame.draw.rect(screen, (200, 0, 0) if play_friend_button.collidepoint((mx, my)) else (255, 0, 0), play_friend_button)
        pygame.draw.rect(screen, (0, 0, 200) if play_computer_button.collidepoint((mx, my)) else (0, 0, 255), play_computer_button)

        draw_text(screen, "Play with Friend", small_font, (255, 255, 255), play_friend_button.centerx, play_friend_button.centery)
        draw_text(screen, "Play with Computer", small_font, (255, 255, 255), play_computer_button.centerx, play_computer_button.centery)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if play_friend_button.collidepoint((mx, my)):
                    tic_tac_toe("Friend")
                if play_computer_button.collidepoint((mx, my)):
                    difficulty_menu()

        pygame.display.update()
        clock.tick(60)

def difficulty_menu():
    pygame.init()

    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Select Difficulty")

    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 30)
    clock = pygame.time.Clock()

    while True:
        screen.fill((30, 30, 30))
        draw_text(screen, "Select Difficulty", font, (255, 255, 255), 300, 50)

        mx, my = pygame.mouse.get_pos()

        easy_button = pygame.Rect(200, 150, 200, 50)
        hard_button = pygame.Rect(200, 220, 200, 50)

        pygame.draw.rect(screen, (200, 200, 0) if easy_button.collidepoint((mx, my)) else (255, 255, 0), easy_button)
        pygame.draw.rect(screen, (200, 0, 200) if hard_button.collidepoint((mx, my)) else (255, 0, 255), hard_button)

        draw_text(screen, "Easy", small_font, (0, 0, 0), easy_button.centerx, easy_button.centery)
        draw_text(screen, "Hard", small_font, (0, 0, 0), hard_button.centerx, hard_button.centery)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if easy_button.collidepoint((mx, my)):
                    tic_tac_toe("Computer", "Easy")
                if hard_button.collidepoint((mx, my)):
                    tic_tac_toe("Computer", "Hard")

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
