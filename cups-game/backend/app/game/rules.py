from app.game.models import Player

def hand_values(player: Player):
    return [c.facevalue for c in player.hand]

def has_card(hand, a, b):
    return a in hand and b in hand

def is_d_cup(player: Player):
    h = hand_values(player)
    return has_card(h, "3", "6")

def is_full_cup(player: Player):
    h = hand_values(player)
    return has_card(h, "4", "9")

def is_half_cup(player: Player):
    h = hand_values(player)

    w1 = has_card(h, "2", "4")
    w2 = has_card(h, "2", "5")
    w3 = has_card(h, "A", "5")
    w4 = has_card(h, "A", "6")
    w5 = h == ["3", "3"]
    w6 = has_card(h, "3", "4")

    return w1 or w2 or w3 or w4 or w5 or w6

def is_almost_half_cup(player: Player):
    h = hand_values(player)

    w1 = has_card(h, "4", "5")
    w2 = has_card(h, "A", "8")
    w3 = has_card(h, "2", "7")
    w4 = has_card(h, "A", "3")
    w5 = h == ["2", "2"]

    return w1 or w2 or w3 or w4 or w5

def is_cup_in_a_pizza_box(player: Player):
    h = hand_values(player)
    return has_card(h, "2", "3")

def has_cup_card(player: Player):
    return any(c.suit == "C" and c.facevalue == "10" for c in player.hand)

def has_saucer_card(player: Player):
    return any(c.suit == "D" and c.facevalue == "10" for c in player.hand)

def is_face_card_present(player: Player):
    h = hand_values(player)
    return any(c in h for c in ["J", "Q", "K", "A"])
