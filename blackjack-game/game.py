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
bg_logo = pygame.image.load("blackjack-game/img/table_logo.png")
bg_logo.set_alpha(180)
#   Fonts
card_font = pygame.font.Font('blackjack-game/fonts/FragmentMono-Regular.ttf', 36)
text_font = pygame.font.Font('blackjack-game/fonts/Roboto-Regular.ttf', 42)
big_text_font = pygame.font.Font('blackjack-game/fonts/Roboto-Regular.ttf', 50)
#   Colours
bg_color = (60, 125, 60)
red_color = (205, 35, 40)
black_color = (0, 0, 0)
white_color = (255, 255, 255)
#   Card images
heart_img = pygame.image.load('./blackjack-game/img/heart.png')
diamond_img = pygame.image.load('./blackjack-game/img/diamond.png')
club_img = pygame.image.load('./blackjack-game/img/club.png')
spade_img = pygame.image.load('./blackjack-game/img/spade.png')
back_of_card_img = pygame.image.load('./blackjack-game/img/back_of_card.png')
empty_card_img = pygame.image.load('./blackjack-game/img/empty_card.png')
#   Button images
sound_on_img = pygame.image.load('./blackjack-game/img/sound_on.png')
sound_off_img = pygame.image.load('./blackjack-game/img/sound_off.png')
cash_out_img = pygame.image.load('./blackjack-game/img/cash_out.png')
#   Sounds
deal_card_sfx = pygame.mixer.Sound('./blackjack-game/sound/deal_card.mp3')
reveal_dealer_sfx = pygame.mixer.Sound('./blackjack-game/sound/reveal_dealer.mp3')
cash_out_sfx = pygame.mixer.Sound('./blackjack-game/sound/cash_out.mp3')
win_sfx = pygame.mixer.Sound('./blackjack-game/sound/win.mp3')
lose_sfx = pygame.mixer.Sound('./blackjack-game/sound/lose.mp3')
tie_sfx = pygame.mixer.Sound('./blackjack-game/sound/tie.mp3')
#   Deck values
card_values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
card_symbols = ['heart', 'diamond', 'club', 'spade']
card_symbol_to_img = {'heart':heart_img, 'diamond':diamond_img, 'club':club_img, 'spade':spade_img}
single_deck = [
    (symbol, value) 
    for symbol in card_symbols 
    for value in card_values]
possible_deck_amounts = [4,10,16]
bet_options = [25,50,75,100,200,500]
#   Booleans (can change during game loop)
game_active = False
sound_on = True
start_new_hand = False
show_starting_menu = True
show_restart_menu = False
show_game_menu = False
show_player_stopped = False
show_statistics = False
hand_active = False
reveal_dealer = False
next_player_card = False
player_stands = False
player_stopped = False
see_statistics = False
#   Game parameters and statistics
def reset_indices():
    deck_amount_i = 0
    bet_i = 0
    return (deck_amount_i, bet_i)

def reset_game():
    game_deck = []
    player_hand = []
    dealer_hand = []
    money = 1000
    outcome = 0
    last_bet = 0
    return (game_deck, player_hand, dealer_hand, money, outcome, last_bet)

def reset_statistics():
    totals = [0,0,0]
    num_rounds = 0
    num_blackjacks = 0
    cards_drawn_player = 0
    cards_drawn_dealer = 0
    max_money = 0
    return (totals, num_rounds, num_blackjacks, cards_drawn_player, cards_drawn_dealer, max_money)

def get_start_money():
    _, _, _, start_money, _, _ = reset_game()
    return start_money

# Initialize and reset game parameters and statistics
deck_amount_i, bet_i = reset_indices()
game_deck, player_hand, dealer_hand, money, outcome, last_bet = reset_game()
totals, num_rounds, num_blackjacks, cards_drawn_player, cards_drawn_dealer, max_money = reset_statistics()

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
        button_list.append(draw_and_create_button('SOUND ON', base_position, inverse_color=True))
    else:
        button_list.append(draw_and_create_button('SOUND OFF', base_position, inverse_color=True))
    button_list.append(draw_and_create_button(f'DECKS: {get_deck_amount()}', ((base_x + 300), base_y), True))
    button_list.append(draw_and_create_button('START', ((base_x + 600), base_y)))
    return button_list

def draw_restart_menu(result, bet=None):
    button_list = []
    button_list.append(draw_and_create_button('NEW HAND', (screen_width-400, 100)))
    button_list.append(draw_and_create_button(f'BET: ${get_current_bet()}', (screen_width-400, 400), inverse_color=True))
    button_list.append(draw_and_create_button('v', (screen_width-150, 400), mini=True, flipped=True, inverse_color=True))
    button_list.append(draw_and_create_button('v', (screen_width-150, 438), mini=True, inverse_color=True))
    # 1 => win, 2 => loss, 3 => tie, 4 => player bust
    if result == 0:
        string = 'Press NEW HAND to start the game!'
        bet_text = card_font.render('Change bet before dealing hand. (minimum $25)', True, black_color)
        screen.blit(bet_text, (5,350))
    elif result == 1:
        string = f'+${bet} Player wins!'
    elif result == 2:
        string = f'-${bet} Dealer wins...'
    elif result == 3:
        string = '+$0 Tie.'
    elif result == 4:
        string = f'-${bet} Player busted!'
    outcome_text = text_font.render(string, True, white_color)
    text_rect = outcome_text.get_rect()
    text_rect.midright = (screen_width-200, 30)
    screen.blit(outcome_text, text_rect)
    button_list += draw_sound(sound_on)
    if result != 0:  
        button_list += draw_cash_out()
    return button_list

def draw_game_menu():
    button_list = []
    button_list.append(draw_and_create_button('HIT ME', (screen_width-400, 40)))
    button_list.append(draw_and_create_button('STAND', (screen_width-400, 120)))
    button_list += draw_sound(sound_on)
    return button_list

def draw_cash_out():
    button_list = []
    button_list.append(draw_and_create_image_button(cash_out_img,(screen_width-130, 160)))
    return button_list

def draw_sound(sound):
    button_list = []
    if sound:
        sound_img = sound_on_img
    else:
        sound_img = sound_off_img
    button_list.append(draw_and_create_image_button(sound_img,(screen_width-130, 30)))
    return button_list

def draw_player_stopped(start_money, money_left):
    button_list = []
    if money_left < 25:
        button_list.append(draw_and_create_button("No more money left! :'(", (75,150), enormous=True, inverse_color=True))
    else:
        button_list.append(draw_and_create_button(f"Cashed out ${money_left}. Gain ($): {money_left-start_money}", (75,150), enormous=True, inverse_color=True))
    button_list.append(draw_and_create_button('Click HERE to view statistics', (75,400), enormous=True))
    return button_list

def draw_statistics():
    screen.fill(black_color)
    button_list = []
    button_list.append(draw_and_create_button('MAIN MENU', (screen_width-300, screen_height-125), inverse_color=True))
    base_x, base_y = (30, 30)
    strings = [
        f'STATISTICS',
        f'Amount of rounds played: {num_rounds}',
        f'Cards drawn by player: {cards_drawn_player}',
        f'Cards drawn by dealer: {cards_drawn_dealer}',
        f'Player blackjacks: {num_blackjacks}',
        f'Maximum amount of money held ($): {max_money}',
        f'Gain ($): {money-get_start_money()}',
        f'Win: {totals[0]} - Loss: {totals[1]} - Tie: {totals[2]}']
    for i in range(len(strings)):
        if i == 0:
            font = text_font
        else:    
            font = card_font
        text = font.render(strings[i], True, white_color)
        position = (base_x, base_y + (i*60))
        screen.blit(text, position)

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
        if i == 1 and hidden_card:
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
    player_text = card_font.render(f'Player: {player_score}', True, white_color)
    screen.blit(player_text, (35, screen_height-55))
    if reveal_dealer:
        string = f'Dealer: {dealer_score}'
    else:
        string = 'Dealer: ?'
    dealer_text = card_font.render(string, True, white_color)
    screen.blit(dealer_text, (35, 230))

def draw_and_create_button(text, position, inverse_color=False, mini=False, enormous=False, flipped=False):
    if inverse_color:
        primary_color = black_color
        secondary_color = white_color
    else:
        primary_color = white_color
        secondary_color = black_color
    if mini:
        size = (100, 38)
        font = card_font
    elif enormous:
        size = (850, 150)
        font = big_text_font
    else:
        size = (250, 75)
        font = text_font
    button_rect = pygame.Rect(position, size)
    button = pygame.draw.rect(screen, primary_color, button_rect, 0, 10)
    pygame.draw.rect(screen, secondary_color, button_rect, 3, 10)
    button_text = font.render(text, True, secondary_color)
    if flipped:
        text_copy = button_text.copy()
        flipped_text = pygame.transform.flip(text_copy, True, True)
        button_text = flipped_text
    text_rect = button_text.get_rect()
    text_rect.center = button_rect.center
    screen.blit(button_text, text_rect.topleft)
    return button

def draw_and_create_image_button(image, position):
    image_rect = image.get_rect()
    image_rect.topleft = position
    screen.blit(image, image_rect)
    return image_rect

def draw_totals(list):
    totals_text = card_font.render(f'Win: {list[0]} - Loss: {list[1]} - Tie: {list[2]}', True, black_color)
    money_text = card_font.render(f'Money: ${money}', True, black_color)
    screen.blit(totals_text, (370, screen_height-60))
    screen.blit(money_text, (screen_width-300, screen_height-115))

#   Initiate game deck
def get_deck_amount():
    return possible_deck_amounts[deck_amount_i % len(possible_deck_amounts)]

def generate_and_shuffle_game_deck():
    game_deck =  get_deck_amount() * single_deck
    random.shuffle(game_deck)
    return game_deck

#   Deal cards
def deal_card(hand, deck):
    if len(deck) == 0:
        deck = generate_and_shuffle_game_deck()
    top_card = deck.pop()
    if sound_on:
        deal_card_sfx.play()
    pygame.time.wait(500)
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

#   Betting
def get_current_bet():
    return bet_options[bet_i]

def next_bet_option():
    return bet_options[(bet_i+1)]

def previous_bet_option():
    return bet_options[(bet_i-1)]

def get_smallest_bet():
    return bet_options[0]

def get_biggest_bet():
    return bet_options[-1]

#   Endgame scenarios
def calculate_outcome(player, dealer):
    player_score = calculate_score(player)
    dealer_score = calculate_score(dealer)
    # 1 => win, 2 => loss, 3 => tie, 4 => player busted
    if player_score > 21:
        result = 4
        if sound_on:
            lose_sfx.play()
    elif dealer_score < player_score <= 21 or dealer_score > 21:
        result = 1
        if sound_on:
            win_sfx.play()
    elif player_score < dealer_score <= 21:
        result = 2
        if sound_on:
            lose_sfx.play()
    else:
        result = 3
        if sound_on:
            tie_sfx.play()
    pygame.time.wait(500)
    return result

def adjust_totals(result):
        if result == 1:
            totals[0] += 1
        elif result in [2,4]:
            totals[1] += 1
        elif result == 3:
            totals[2] += 1

def adjust_money(current_money, result):
    bet = get_current_bet()
    if result == 1:
        current_money += (2*bet)
    elif result == 3:
        current_money += bet
    return current_money

run_game = True
while run_game:
    # Draw new frame
    timer.tick(fps)
    draw_table()
    draw_deck()

    if not game_active and not see_statistics:
        buttons = draw_starting_menu()
        show_starting_menu = True
    
    if game_active:
        if hand_active:
            reveal_dealer = False
            if start_new_hand:
                num_rounds += 1
                dealer_hand = []
                player_hand = []
                money -= get_current_bet()
                last_bet = get_current_bet()
                for i in range(2):
                    player_hand, game_deck = deal_card(player_hand, game_deck)
                    cards_drawn_player += 1
                    draw_all_cards(player_hand, dealer_hand)
                    draw_totals(totals)
                    pygame.display.flip()
                    dealer_hand, game_deck = deal_card(dealer_hand, game_deck)
                    cards_drawn_dealer += 1
                    draw_all_cards(player_hand, dealer_hand)
                    draw_totals(totals)
                    pygame.display.flip()
            start_new_hand = False
            buttons = draw_game_menu()
            show_game_menu = True
            show_restart_menu = False
            if calculate_score(player_hand) >= 21:
                player_stands = True

            if next_player_card:
                player_hand, game_deck = deal_card(player_hand, game_deck)
                cards_drawn_player += 1
                draw_player_cards(player_hand)
                draw_totals(totals)
                draw_scores(player_hand, dealer_hand)
                pygame.display.flip()
                next_player_card = False

        if player_stands:
            hand_active = False
            show_game_menu = False
            player_score = calculate_score(player_hand)
            if player_score <= 21:
                reveal_dealer = True
                if sound_on:
                    reveal_dealer_sfx.play()
                pygame.time.wait(750)
                draw_all_cards(player_hand, dealer_hand, reveal_dealer)
                draw_totals(totals)
                pygame.display.flip()
            if player_score == 21:
                num_blackjacks += 1
            draw_all_cards(player_hand, dealer_hand, reveal_dealer)
            while calculate_score(dealer_hand) < 17 and player_score <= 21:
                dealer_hand, game_deck = deal_card(dealer_hand, game_deck)
                cards_drawn_dealer += 1
                draw_all_cards(player_hand, dealer_hand, reveal_dealer)
                draw_totals(totals)
                pygame.display.flip()
            outcome = calculate_outcome(player_hand, dealer_hand)
            adjust_totals(outcome) 
            money = adjust_money(money, outcome)
            if money >= max_money:
                max_money = money
            player_stands = False

        if not hand_active and not player_stands:
            buttons = draw_restart_menu(outcome, bet=last_bet)
            show_restart_menu = True

        draw_all_cards(player_hand, dealer_hand, reveal_dealer)
        draw_totals(totals)
        draw_scores(player_hand, dealer_hand, reveal_dealer)

        if (money < get_smallest_bet() and not hand_active) or player_stopped:
            show_restart_menu = False
            show_game_menu = False
            buttons = draw_player_stopped(get_start_money(), money)
            show_player_stopped = True

    if see_statistics and not game_active:
        buttons = draw_statistics()
        show_statistics = True

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
                    show_restart_menu = True
                    game_active = True

            if show_restart_menu:
                if buttons[0].collidepoint(event.pos) and get_current_bet() <= money:
                    hand_active = True
                    start_new_hand = True
                elif buttons[2].collidepoint(event.pos):
                    if not (get_current_bet() == get_biggest_bet()) and next_bet_option() <= money:
                        bet_i += 1
                elif buttons[3].collidepoint(event.pos): 
                    if not (get_current_bet() == get_smallest_bet()):
                        bet_i -= 1  
                elif buttons[4].collidepoint(event.pos):
                    sound_on = not sound_on
                elif outcome !=0 and buttons[5].collidepoint(event.pos):
                    if sound_on:
                        cash_out_sfx.play()
                    pygame.time.wait(750)
                    player_stopped = True
                    
            if show_game_menu:
                if buttons[0].collidepoint(event.pos):
                    next_player_card = True
                elif buttons[1].collidepoint(event.pos):
                    player_stands = True
                    hand_active = False
                elif buttons[2].collidepoint(event.pos):
                    sound_on = not sound_on

            if show_player_stopped:
                if buttons[1].collidepoint(event.pos):
                    see_statistics = True
                    game_active = False
                    show_player_stopped = False
                    player_stopped = False
            
            if show_statistics:
                if buttons[0].collidepoint(event.pos):
                    see_statistics = False
                    show_statistics = False
                    show_starting_menu = True
                    # reset game and statistics
                    game_deck, player_hand, dealer_hand, money, outcome, last_bet = reset_game()
                    totals, num_rounds, num_blackjacks, cards_drawn_player, cards_drawn_dealer, max_money = reset_statistics()
                    deck_amount_i, bet_i = reset_indices()    

    pygame.display.flip()
pygame.quit()