import random
import pygame

pygame.init()

# Variables
#   Game screen
screen_size = (screen_width, screen_height) = (1000, 600)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Introductieproject - Blackjack by Eward Degrieck")
fps = 60
timer = pygame.time.Clock()
bg_logo = pygame.image.load("./blackjack-game/img/table_logo.png")
bg_logo.set_alpha(180)
#   Fonts
card_font = pygame.font.Font('./blackjack-game/fonts/FragmentMono-Regular.ttf', 36)
text_font = pygame.font.Font('./blackjack-game/fonts/Roboto-Regular.ttf', 42)
#   Colours
bg_color = (60, 125, 60)
red_color = (204, 35, 40)
black_color = (0, 0, 0)
white_color = (255, 255, 255)
#   Card images
heart_img = pygame.image.load('./blackjack-game/img/heart.png')
diamond_img = pygame.image.load('./blackjack-game/img/diamond.png')
club_img = pygame.image.load('./blackjack-game/img/club.png')
spade_img = pygame.image.load('./blackjack-game/img/spade.png')
back_of_card_img = pygame.image.load('./blackjack-game/img/back_of_card.png')
empty_card_img = pygame.image.load('./blackjack-game/img/empty_card.png')
#   Deck values
card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
card_symbols = ['heart', 'diamond', 'club', 'spade']
card_symbol_to_img = {'heart':heart_img, 'diamond':diamond_img, 'club':club_img, 'spade':spade_img}
single_deck = [
    (symbol, value) 
    for symbol in card_symbols 
    for value in card_values]
possible_deck_amounts = [4,10,16]
#   Booleans (can change during game loop)
game_active = False
deck_amount_i = 0
sound_on = True
start_new_hand = False
game_loop = False
show_restart_menu = False
show_starting_menu = True
show_game_menu = False
show_result_menu = True
hand_active = False
reveal_dealer = False
next_player_card = False
player_stands = False
totals_need_update = False
#   Game parameters (can change during game loop)
game_deck = []
player_hand = []
dealer_hand = []
totals = [0,0,0]
outcome = 0

# Functions
#   Draw game table and menus
def draw_table():
    screen.fill(bg_color)
    bg_logo_rect = bg_logo.get_rect()
    bg_logo_rect.center = screen.get_rect().center
    screen.blit(bg_logo, bg_logo_rect)

def draw_starting_menu():
    button_list = []
    base_position = (base_x, base_y) = 75, screen_height - 110
    if sound_on:
        button_list.append(draw_and_create_button('SOUND ON', base_position))
    else:
        button_list.append(draw_and_create_button('SOUND OFF', base_position))
    button_list.append(draw_and_create_button(f'DECKS: {get_deck_amount()}', ((base_x + 300), base_y)))
    button_list.append(draw_and_create_button('START', ((base_x + 600), base_y)))
    return button_list

def draw_restart_menu(result):
    button_list = []
    button_list.append(draw_and_create_button('DEAL HAND', (screen_width-350, 100)))
    # 1 => win, 2 => loss, 3 => tie, 4 => player bust
    if result == 0:
        string = 'Press DEAL HAND to start the game!'
    elif result == 1:
        string = 'Player wins! :-)'
    elif result == 2:
        string = 'Dealer wins... :-('
    elif result == 3:
        string = 'Tie!'
    elif result == 4:
        string = 'Player busted!'
    text = text_font.render(string, True, white_color)
    text_rect = text.get_rect()
    text_rect.midright = (screen_width-250, 50)
    screen.blit(text, text_rect)
    return button_list

def draw_game_menu():
    button_list = []
    button_list.append(draw_and_create_button('NEXT CARD', (screen_width-350, 100)))
    button_list.append(draw_and_create_button('STAND', (screen_width-350, 400)))
    return button_list

#   Draw cards to screen
def draw_card_back(position):
    screen.blit(back_of_card_img, position)

def draw_deck():
    base_x, base_y = (screen_width-200, 15)
    for i in range(5):
        draw_card_back((base_x+(i*8), base_y))    

def draw_card_face(card_tuple, position):
    screen.blit(empty_card_img, position)
    symbol, value = card_tuple
    x, y = position
    # draw card symbols
    symbol_img = card_symbol_to_img[symbol]
    screen.blit(symbol_img, (x+60, y+45))
    symbol_img_copy = symbol_img.copy()
    flipped_symbol = pygame.transform.flip(symbol_img_copy, True, True)
    screen.blit(flipped_symbol, (x+60, y+120))
    # draw card values
    if symbol in ['heart', 'diamond']:
        font_color = red_color
    else:
        font_color = black_color
    value_img = card_font.render(value, True, font_color)
    screen.blit(value_img, (x+18, y+15))
    value_img_copy = value_img.copy()
    flipped_value = pygame.transform.flip(value_img_copy, True, True)
    if value == '10':
        x_val_flip = x + 97
    else:
        x_val_flip = x + 110
    screen.blit(flipped_value, (x_val_flip, y+142))

def draw_dealer_cards(dealer_cards, hidden_card=False):
    base_x, base_y = (15, 10)
    for i in range(len(dealer_cards)):
        next_pos = (base_x + (i*78), base_y + (i*10))
        if hidden_card and i == 1:
            draw_card_back(next_pos)
        else:
            draw_card_face(dealer_cards[i], next_pos)

def draw_player_cards(player_cards):
    base_x, base_y = 15, screen_height-295
    for i in range(len(player_cards)):
        next_pos = (base_x + (i*78), base_y + (i*10))
        draw_card_face(player_cards[i], next_pos)

def draw_all_cards(player_cards, dealer_cards, reveal_dealer=False):
    draw_player_cards(player_cards)
    if reveal_dealer:
        draw_dealer_cards(dealer_cards)
    else:
        draw_dealer_cards(dealer_cards, hidden_card=True)

#   Draw scores and buttons
def draw_scores(player, dealer, reveal_dealer=False):
    player_score = calculate_score(player)
    dealer_score = calculate_score(dealer)
    player_text = card_font.render(f'Player: {player_score}', True, black_color)
    screen.blit(player_text, (35, screen_height-55))
    if reveal_dealer:
        dealer_text = card_font.render(f'Dealer: {dealer_score}', True, black_color)
    else:
        dealer_text = card_font.render('Dealer: ?', True, black_color)
    screen.blit(dealer_text, (35, 230))

def draw_and_create_button(text, position):
    button_rect = pygame.Rect(position, (250, 75))
    button = pygame.draw.rect(screen, white_color, button_rect, 0, 10)
    pygame.draw.rect(screen, black_color, button_rect, 3, 10)
    button_text = text_font.render(text, True, black_color)
    text_rect = button_text.get_rect()
    text_rect.center = button_rect.center
    screen.blit(button_text, text_rect.topleft)
    return button

def draw_totals(list):
    text = card_font.render(f'Win: {list[0]} - Loss: {list[1]} - Tie: {list[2]}', True, black_color)
    screen.blit(text, (415, screen_height-60))

#   Initiate game deck
def get_deck_amount():
    return possible_deck_amounts[deck_amount_i % 3]

def generate_and_shuffle_game_deck():
    game_deck =  get_deck_amount() * single_deck
    random.shuffle(game_deck)
    return game_deck

#   Deal cards
def deal_card(hand, deck):
    if len(deck) == 0:
        deck = generate_and_shuffle_game_deck()
    top_card = deck.pop()
    hand.append(top_card)
    return hand, deck

#   Calculate scores
def calculate_score(hand):
    hand_score = 0
    hand_values = [value for (_, value) in hand]
    aces_count = hand_values.count('A')
    for i in range(len(hand_values)):
        # for 2 -> 9 - just add number to total
        for j in range(8):
            if hand_values[i] == card_values[j]:
                hand_score += int(hand_values[i])
        # for 10 and face cards, add 10
        if hand_values[i] in ['10', 'J', 'Q', 'K']:
            hand_score += 10 
        # for aces start by adding 11, we'll check if need to reduce afterwards
        elif hand_values[i] == 'A':
            hand_score += 11
        # determine how many aces need to be 1 in order toget under 21
        while hand_score > 21 and aces_count > 0:
            aces_count -= 1
            hand_score -=10

    return hand_score

#   Endgame scenarios
def calculate_outcome(player, dealer):
    player_score = calculate_score(player)
    dealer_score = calculate_score(dealer)
    # 1 => win, 2 => loss, 3 => tie, 4 => player busted
    if player_score > 21:
        result = 4
    elif dealer_score < player_score <= 21 or dealer_score > 21:
        result = 1
    elif player_score < dealer_score <= 21:
        result = 2
    else:
        result = 3
    return result

def adjust_totals(result):
        if result == 4:
            totals[2] += 1
        else:
            totals[result-1] += 1

run_game = True
while run_game:
    # Draw new frame
    timer.tick(fps)
    draw_table()
    draw_deck()

    if not game_active:
        buttons = draw_starting_menu()
        show_starting_menu = True
    
    if game_active:
        draw_all_cards(player_hand, dealer_hand, reveal_dealer)
        draw_scores(player_hand, dealer_hand, reveal_dealer)
        draw_totals(totals)
        if hand_active:
            reveal_dealer = False
            if start_new_hand:
                dealer_hand = []
                player_hand = []
                for i in range(2):
                    player_hand, game_deck = deal_card(player_hand, game_deck)
                    dealer_hand, game_deck = deal_card(dealer_hand, game_deck)
            start_new_hand = False
            buttons = draw_game_menu()
            show_game_menu = True
            show_restart_menu = False
            if calculate_score(player_hand) >= 21:
                player_stands = True

            if next_player_card:
                player_hand, game_deck = deal_card(player_hand, game_deck)
                next_player_card = False
        else:
            buttons = draw_restart_menu(outcome)
            show_restart_menu = True

        if player_stands:
            hand_active = False
            show_restart_menu = True
            show_game_menu = False
            player_score = calculate_score(player_hand)
            if player_score <= 21:
                reveal_dealer = True
            while calculate_score(dealer_hand) < 17 and player_score <= 21:
                dealer_hand, game_deck = deal_card(dealer_hand, game_deck)
            outcome = calculate_outcome(player_hand, dealer_hand)
            buttons = draw_restart_menu(outcome)
            adjust_totals(outcome) 
            player_stands = False

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
        if event.type == pygame.MOUSEBUTTONUP:
            if show_starting_menu:
                if buttons[0].collidepoint(event.pos):
                    sound_on = not sound_on
                if buttons[1].collidepoint(event.pos):
                    deck_amount_i += 1
                if buttons[2].collidepoint(event.pos):
                    show_starting_menu = False
                    game_active = True

            if show_restart_menu:
                if buttons[0].collidepoint(event.pos):
                    hand_active = True
                    start_new_hand = True
            
            if show_game_menu:
                if buttons[0].collidepoint(event.pos):
                    next_player_card = True
                elif buttons[1].collidepoint(event.pos):
                    player_stands = True
                    hand_active = False
            
            if show_result_menu:
                pass
        
    pygame.display.flip()
pygame.quit()