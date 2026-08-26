# test_cups.py
import pytest
from unittest.mock import patch
import consoleclasses as cups


def card(v, s):
    return cups.Card(v, s)


def hand(*cards):
    return [card(v, s) for v, s in cards]


@pytest.fixture
def game():
    gm = cups.GameManager()
    gm.players = {
        "Dealer": cups.Player("Dealer"),
        "Player": cups.Player("Player"),
    }
    return gm


@pytest.mark.parametrize(
    "method_name, player_hand, dealer_hand, winner, payout",
    [
        ("isDCup", hand(("3", "H"), ("6", "S")), hand(("A", "H"), ("K", "S")), "Player", 400),
        ("isDCup", hand(("A", "H"), ("K", "S")), hand(("3", "H"), ("6", "S")), "Dealer", 400),
        ("isFullCup", hand(("4", "H"), ("9", "S")), hand(("A", "H"), ("K", "S")), "Player", 100),
        ("isFullCup", hand(("A", "H"), ("K", "S")), hand(("4", "H"), ("9", "S")), "Dealer", 100),
        ("isHalfCup", hand(("2", "H"), ("4", "S")), hand(("A", "H"), ("K", "S")), "Player", 50),
        ("isHalfCup", hand(("A", "H"), ("K", "S")), hand(("2", "H"), ("4", "S")), "Dealer", 50),
        ("isHalfCup", hand(("2", "H"), ("5", "S")), hand(("A", "H"), ("K", "S")), "Player", 50),
        ("isHalfCup", hand(("A", "H"), ("K", "S")), hand(("A", "H"), ("6", "S")), "Dealer", 50),
        ("isHalfCup", hand(("3", "H"), ("3", "S")), hand(("A", "H"), ("K", "S")), "Player", 50),
        ("isHalfCup", hand(("A", "H"), ("K", "S")), hand(("3", "H"), ("4", "S")), "Dealer", 50),
        ("isAlmostHalfCup", hand(("4", "H"), ("5", "S")), hand(("A", "H"), ("K", "S")), "Player", 45),
        ("isAlmostHalfCup", hand(("A", "H"), ("K", "S")), hand(("4", "H"), ("5", "S")), "Dealer", 45),
        ("isAlmostHalfCup", hand(("A", "H"), ("8", "S")), hand(("J", "H"), ("2", "S")), "Player", 45),
        ("isAlmostHalfCup", hand(("J", "H"), ("2", "S")), hand(("A", "H"), ("8", "S")), "Dealer", 45),
        ("isCupInAPizzaBox", hand(("2", "H"), ("3", "S")), hand(("A", "H"), ("K", "S")), "Player", 60),
        ("isCupInAPizzaBox", hand(("A", "H"), ("K", "S")), hand(("2", "H"), ("3", "S")), "Dealer", 60),
    ],
)
def test_winning_hands(game, method_name, player_hand, dealer_hand, winner, payout):
    game.players["Player"].hand = player_hand
    game.players["Dealer"].hand = dealer_hand

    result = getattr(game, method_name)(
        game.players["Player"],
        game.players["Dealer"],
    )

    assert result is True
    if winner == "Player":
        assert game.players["Player"].money == payout
        assert game.players["Dealer"].money == 0
    else:
        assert game.players["Dealer"].money == payout
        assert game.players["Player"].money == 0


@pytest.mark.parametrize(
    "method_name, player_hand, dealer_hand",
    [
        ("isDCup", hand(("2", "H"), ("4", "S")), hand(("A", "H"), ("K", "S"))),
        ("isFullCup", hand(("2", "H"), ("4", "S")), hand(("A", "H"), ("K", "S"))),
        ("isHalfCup", hand(("A", "H"), ("K", "S")), hand(("2", "H"), ("7", "S"))),
        ("isAlmostHalfCup", hand(("2", "H"), ("3", "S")), hand(("4", "H"), ("6", "S"))),
        ("isCupInAPizzaBox", hand(("4", "H"), ("5", "S")), hand(("A", "H"), ("K", "S"))),
    ],
)
def test_non_winning_hands_return_false(game, method_name, player_hand, dealer_hand):
    game.players["Player"].hand = player_hand
    game.players["Dealer"].hand = dealer_hand

    result = getattr(game, method_name)(
        game.players["Player"],
        game.players["Dealer"],
    )

    assert result is False
    assert game.players["Player"].money == 0
    assert game.players["Dealer"].money == 0


def test_has_cup_card(game):
    game.players["Player"].hand = [cups.CupCard(), cups.Card("A", "H")]
    game.players["Dealer"].hand = [cups.Card("2", "H"), cups.Card("3", "S")]

    assert game.hasCupCard(game.players["Player"], game.players["Dealer"]) is True
    assert game.players["Player"].money == 75


def test_has_saucer_card(game):
    game.players["Player"].hand = [cups.SaucerCard(), cups.Card("A", "H")]
    game.players["Dealer"].hand = [cups.Card("2", "H"), cups.Card("3", "S")]

    assert game.hasSaucerCard(game.players["Player"], game.players["Dealer"]) is True
    assert game.players["Player"].money == 80


def test_check_game_end(game):
    game.deck.cards = [1, 2, 3]
    assert game.checkGameEnd() is True
    game.deck.cards = [1, 2, 3, 4]
    assert game.checkGameEnd() is False


def test_doubling_bonus(game):
    game.deck.cards = [cups.PostDoubleBonusCard()]
    player = game.players["Player"]
    player.money = 700

    with patch("builtins.input", side_effect=["yes", "yes"]), patch("time.sleep", lambda _: None):
        game.doublingBonus(player)

    assert player.money == 1500
