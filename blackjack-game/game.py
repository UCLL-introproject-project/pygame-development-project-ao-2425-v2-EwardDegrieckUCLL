import copy
import random
import pygame

pygame.init()

# Variables
#   Game screen
size = width, height = 1200, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Blackjack - Introductieproject by Eward Degrieck")
fps = 60
timer = pygame.time.Clock()
bg_logo = ball = pygame.image.load("./blackjack-game/img/table_logo.png")
bg_logo.set_alpha(180)
#   Fonts
card_font = pygame.font.Font('./blackjack-game/fonts/FragmentMono-Regular.ttf', 52)
text_font = pygame.font.Font('./blackjack-game/fonts/Roboto-Regular.ttf', 44)
#   Colours
bg_color = (60, 125, 60)
red_color = (255, 0, 0)
black_color = (0, 0, 0)
white_color = (255, 255, 255)

cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
standard_deck_amount = 4

run_game = True
while run_game:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False

    screen.fill(bg_color)
    screen.blit(bg_logo, (180,250))
    pygame.display.flip()
pygame.quit()













all_cards = deck_amount * cards