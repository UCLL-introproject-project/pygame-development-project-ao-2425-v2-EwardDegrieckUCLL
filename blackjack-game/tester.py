possible_deck_amounts=[4,10,16]
deck_amount_i=0

def get_deck_amount():
    return possible_deck_amounts[deck_amount_i % 3]

print(deck_amount_i)
print(get_deck_amount())
deck_amount_i +=1
print(deck_amount_i)
print(get_deck_amount())
deck_amount_i +=1
print(deck_amount_i)
print(get_deck_amount())
deck_amount_i +=1
print(deck_amount_i)
print(get_deck_amount())
deck_amount_i +=1
print(deck_amount_i)
print(get_deck_amount())