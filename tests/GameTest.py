import unittest

from cards.Card import Card, CardNumber, Genre
from games.Deck import Deck
from games.Game import Game
from players.Player import ID_generator, Player
from players.Policy import Policy
from rounds.Pot import Pot
from rounds.Round import Flop, Preflop, River, Turn
from rounds.RoundName import RoundName


class GameTest(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    # --------------------- Player Seats ------------------------
    def test_players_sit_in_right_place(self):
        # Given
        game = Game()
        harry = Player("Harry Potter", ID=ID_generator(), money=3)
        tom = Player("Tom Dwan", ID=ID_generator(), money=5)
        phil = Player("Phil Ivey", ID=ID_generator(), money=1)

        # When
        tom.join_game(game, position=4)
        harry.join_game(game, position=1)
        phil.join_game(game, position=0)

        # Then
        self.assertTrue(len(game.player_list) == 3)
        self.assertTrue(game.get_players_in_the_game() == [phil, harry, tom])

    def test_cannot_sit_on_a_place_taken(self):
        # Given
        game = Game()
        harry = Player("Harry Potter", ID=ID_generator(), money=3)
        harry.join_game(game, position=1)

        # When
        phil = Player("Phil Ivey", ID=ID_generator(), money=1)

        # Then
        self.assertRaises(KeyError, phil.join_game, game, 1)

    # --------------------------- Deck ----------------------------
    def test_deck_is_initialized(self):
        # Given, When
        deck = Deck()

        # Then
        cards = [Card(g, n) for g in Genre for n in CardNumber]
        self.assertNotEqual(cards, deck.cards)
        self.assertEqual(set(cards), set(deck.cards))

    def test_skip_one_card_in_deck(self):
        # Given
        deck = Deck()

        # When
        deck.skip_one_card()

        # Then
        self.assertTrue(deck.peek_top_card() == deck.cards[1])

    def test_pop_cards_from_deck(self):
        # Given
        deck = Deck()

        # When
        deck.skip_one_card()
        deck.pop_cards(3)
        deck.skip_one_card()
        cards = deck.pop_cards(2)

        # Then
        self.assertTrue(len(cards) == 2)
        self.assertEqual(deck.cards[5:7], list(cards))

    # --------------------------- Preflop ----------------------------
    def test_initialize_preflop(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        pot = Pot()
        deck = Deck()

        # When
        preflop = Preflop(players=(phil, harry), deck=deck, pot=pot, small_blind=1, big_blind=2)

        # Then
        # hands are distributed correctly
        self.assertTrue(deck.index == 4)
        self.assertTrue({deck.cards[0], deck.cards[2]}, set(phil.hands))
        self.assertTrue({deck.cards[1], deck.cards[3]}, set(harry.hands))

        # pot is initialized
        self.assertTrue(len(pot.roundpots[RoundName.PREFLOP]) == 2)
        self.assertEqual(pot.roundpots[RoundName.PREFLOP], {phil: 1, harry: 2})
        self.assertTrue(pot.compute_total_sum() == 3)
        self.assertFalse(pot.is_balanced(RoundName.PREFLOP))

        # Players have bet small and big blines
        self.assertTrue(phil.money == 149)
        self.assertTrue(harry.money == 298)

        self.assertTrue(preflop.check_round_result() == [])

    def test_preflop_pot_is_balanced_when_everyone_calls(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)

        # When
        phil.call(pot, roundname=RoundName.PREFLOP)

        # Then
        self.assertTrue(phil.money == 148)
        self.assertTrue(pot.is_balanced(RoundName.PREFLOP))
        self.assertTrue(preflop.check_round_result() == [], "round is not finished.")

    def test_preflop_pot_is_terminated_when_everyone_calls_and_big_blind_checks(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)

        # When
        phil.call(pot, roundname=RoundName.PREFLOP)
        harry.check()

        # Then
        self.assertTrue(phil.money == 148)
        self.assertTrue(pot.is_balanced(RoundName.PREFLOP))
        self.assertTrue(preflop.check_round_result() == [phil, harry])

    def test_preflop_result_when_all_players_but_one_fold(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)

        # When
        phil.fold()

        # Then
        self.assertTrue(phil.money == 149)
        self.assertFalse(pot.is_balanced(RoundName.PREFLOP))
        self.assertTrue(preflop.check_round_result() == [harry])

    def test_preflop_pot_is_unbalanced_when_small_blind_raises(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)

        # When
        phil.bet(pot, RoundName.PREFLOP, 9)

        # Then
        self.assertTrue(phil.money == 140)
        self.assertFalse(pot.is_balanced(RoundName.PREFLOP))
        self.assertTrue(preflop.check_round_result() == [], "round is not finished.")

    def test_preflop_pot_is_balanced_when_small_blind_raises_and_big_blind_calls(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)

        # When
        phil.bet(pot, RoundName.PREFLOP, 9)
        harry.call(pot, RoundName.PREFLOP)

        # Then
        self.assertTrue(phil.money == 140)
        self.assertTrue(harry.money == 290)
        self.assertTrue(pot.is_balanced(RoundName.PREFLOP))
        self.assertTrue(preflop.check_round_result() == [phil, harry])

    def test_preflop_pot_is_balanced_when_one_is_all_in(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)

        # When
        phil.bet(pot, RoundName.PREFLOP, 9)
        harry.bet(pot, RoundName.PREFLOP, 200)
        phil.call(pot, RoundName.PREFLOP)

        # Then
        self.assertTrue(phil.money == 0)
        self.assertTrue(harry.money == 98)
        self.assertTrue(pot.is_balanced(RoundName.PREFLOP))
        self.assertTrue(preflop.check_round_result() == [phil, harry])

    def test_run_preflop(self):
        # Given
        game = Game()
        tom = Player("Tom Dwan", ID=ID_generator(), money=50, policy=Policy.ALWAYS_CALL)
        tom.join_game(game, position=3)
        harry = Player("Harry Potter", ID=ID_generator(), money=300, policy=Policy.ALWAYS_CALL)
        harry.join_game(game, position=1)
        anton = Player("Anton Dom", ID=ID_generator(), money=1000, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        anton.join_game(game, position=4)
        phil = Player("Phil Ivey", ID=ID_generator(), money=150, policy=Policy.ALWAYS_CALL)
        phil.join_game(game, position=0)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)

        # When
        result = preflop.run()

        # Then
        self.assertTrue(phil.money == 148)
        self.assertTrue(harry.money == 298)
        self.assertTrue(tom.money == 48)
        self.assertTrue(anton.money == 1_000)
        self.assertTrue(pot.is_balanced(RoundName.PREFLOP))
        self.assertTrue(result == [phil, harry, tom])

    # --------------------------- Flop ----------------------------
    def test_initialize_flop(self):
        # Given
        game = Game()
        tom = Player("Tom Dwan", ID=ID_generator(), money=50, policy=Policy.ALWAYS_CALL)
        tom.join_game(game, position=3)
        harry = Player("Harry Potter", ID=ID_generator(), money=300, policy=Policy.ALWAYS_CALL)
        harry.join_game(game, position=1)
        anton = Player("Anton Dom", ID=ID_generator(), money=1000, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        anton.join_game(game, position=4)
        phil = Player("Phil Ivey", ID=ID_generator(), money=150, policy=Policy.ALWAYS_CALL)
        phil.join_game(game, position=0)

        deck = Deck()
        pot = Pot()

        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        tom.call(pot, roundname=RoundName.PREFLOP)
        anton.fold()
        phil.fold()
        harry.check()
        self.assertTrue(preflop.check_round_result() == [harry, tom])
        self.assertTrue(phil.money == 149)
        self.assertTrue(harry.money == 298)
        self.assertTrue(tom.money == 48)
        self.assertTrue(anton.money == 1_000)

        # When
        flop = Flop(players=preflop.check_round_result(), deck=deck, pot=pot)

        # Then
        self.assertTrue(deck.index == 12, "Flop cards should be displayed")
        self.assertTrue(phil.money == 149)
        self.assertTrue(harry.money == 298)
        self.assertTrue(tom.money == 48)
        self.assertTrue(anton.money == 1_000)
        self.assertTrue(pot.compute_total_sum() == 5)
        self.assertTrue(flop.check_round_result() == [], "round has not started")

    def test_flop_pot_is_unbalanced_when_one_raises(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        phil.call(pot, roundname=RoundName.PREFLOP)
        harry.check()

        # When
        flop = Flop(players=preflop.check_round_result(), deck=deck, pot=pot)
        phil.bet(pot, RoundName.FLOP, 9)

        # Then
        self.assertTrue(phil.money == 139)
        self.assertTrue(harry.money == 298)
        self.assertTrue(pot.compute_total_sum() == 13)
        self.assertFalse(pot.is_balanced(RoundName.FLOP))
        self.assertTrue(flop.check_round_result() == [], "round is not finished.")

    def test_flop_pot_is_balanced_when_everyone_calls(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        phil.call(pot, roundname=RoundName.PREFLOP)
        harry.check()

        # When
        flop = Flop(players=preflop.check_round_result(), deck=deck, pot=pot)
        phil.bet(pot, roundname=RoundName.FLOP, to_putin=5)
        harry.call(pot, roundname=RoundName.FLOP)

        # Then
        self.assertTrue(phil.money == 143)
        self.assertTrue(harry.money == 293)
        self.assertTrue(pot.compute_total_sum() == 14)
        self.assertTrue(pot.is_balanced(RoundName.FLOP))
        self.assertTrue(flop.check_round_result() == [phil, harry])

    def test_flop_result_when_all_players_but_one_fold(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        phil.call(pot, roundname=RoundName.PREFLOP)
        harry.check()

        # When
        flop = Flop(players=preflop.check_round_result(), deck=deck, pot=pot)
        phil.bet(pot, roundname=RoundName.FLOP, to_putin=5)
        harry.fold()

        # Then
        self.assertTrue(phil.money == 143)
        self.assertTrue(harry.money == 298)
        self.assertTrue(pot.compute_total_sum() == 9)
        self.assertFalse(pot.is_balanced(RoundName.FLOP))
        self.assertTrue(flop.check_round_result() == [phil])

    def test_flop_result_when_settled(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        phil.call(pot, roundname=RoundName.PREFLOP)
        harry.check()

        # When
        flop = Flop(players=preflop.check_round_result(), deck=deck, pot=pot)
        phil.bet(pot, roundname=RoundName.FLOP, to_putin=5)
        harry.fold()
        flop.settle(flop.check_round_result())

        # Then
        self.assertTrue(phil.money == 152)
        self.assertTrue(harry.money == 298)
        self.assertTrue(pot.compute_total_sum() == 0)

    def test_flop_pot_is_balanced_when_one_is_all_in(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        phil.call(pot, roundname=RoundName.PREFLOP)
        harry.check()

        # When
        flop = Flop(players=preflop.check_round_result(), deck=deck, pot=pot)
        phil.bet(pot, RoundName.FLOP, 9)
        harry.bet(pot, RoundName.FLOP, 200)
        phil.call(pot, RoundName.FLOP)

        # Then
        self.assertTrue(phil.money == 0)
        self.assertTrue(harry.money == 98)
        self.assertTrue(pot.compute_total_sum() == 352)
        self.assertTrue(pot.is_balanced(RoundName.FLOP))
        self.assertTrue(flop.check_round_result() == [phil, harry])

    def test_run_flop(self):
        # Given
        game = Game()
        tom = Player("Tom Dwan", ID=ID_generator(), money=50, policy=Policy.ALWAYS_CALL)
        tom.join_game(game, position=3)
        harry = Player("Harry Potter", ID=ID_generator(), money=300, policy=Policy.ALWAYS_CALL)
        harry.join_game(game, position=1)
        anton = Player("Anton Dom", ID=ID_generator(), money=1000, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        anton.join_game(game, position=4)
        phil = Player("Phil Ivey", ID=ID_generator(), money=150, policy=Policy.ALWAYS_CALL)
        phil.join_game(game, position=0)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        remaining_players = preflop.run()

        # When
        flop = Flop(players=remaining_players, deck=deck, pot=pot)
        remaining_players = flop.run()

        # Then
        self.assertTrue(phil.money == 148)
        self.assertTrue(harry.money == 298)
        self.assertTrue(tom.money == 48)
        self.assertTrue(anton.money == 1_000)
        self.assertTrue(pot.is_balanced(RoundName.FLOP))
        self.assertTrue(remaining_players == [phil, harry, tom])

    # --------------------------- Turn ----------------------------
    def test_initialize_turn(self):
        # Given
        game = Game()
        tom = Player("Tom Dwan", ID=ID_generator(), money=50, policy=Policy.ALWAYS_CALL)
        tom.join_game(game, position=3)
        harry = Player("Harry Potter", ID=ID_generator(), money=300, policy=Policy.ALWAYS_CALL)
        harry.join_game(game, position=1)
        anton = Player("Anton Dom", ID=ID_generator(), money=1000, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        anton.join_game(game, position=4)
        phil = Player("Phil Ivey", ID=ID_generator(), money=150, policy=Policy.ALWAYS_CALL)
        phil.join_game(game, position=0)

        deck = Deck()
        pot = Pot()

        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        tom.call(pot, roundname=RoundName.PREFLOP)
        anton.fold()
        phil.fold()
        harry.check()

        flop = Flop(players=preflop.check_round_result(), deck=deck, pot=pot)
        harry.check()
        tom.check()

        # When
        turn = Turn(players=flop.check_round_result(), deck=deck, pot=pot)

        # Then
        self.assertTrue(deck.index == 14, "Turn cards should be displayed")
        self.assertTrue(phil.money == 149)
        self.assertTrue(harry.money == 298)
        self.assertTrue(tom.money == 48)
        self.assertTrue(anton.money == 1_000)
        self.assertTrue(pot.compute_total_sum() == 5)
        self.assertTrue(turn.check_round_result() == [], "round has not started")

    def test_turn_pot_is_unbalanced_when_one_raises(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        phil.call(pot, roundname=RoundName.PREFLOP)
        harry.check()
        flop = Flop(players=preflop.check_round_result(), deck=deck, pot=pot)
        phil.check()
        harry.check()

        # When
        turn = Turn(players=flop.check_round_result(), deck=deck, pot=pot)
        phil.bet(pot, RoundName.TURN, 9)

        # Then
        self.assertTrue(phil.money == 139)
        self.assertTrue(harry.money == 298)
        self.assertTrue(pot.compute_total_sum() == 13)
        self.assertFalse(pot.is_balanced(RoundName.TURN))
        self.assertTrue(turn.check_round_result() == [], "round is not finished.")

    def test_turn_pot_is_balanced_when_everyone_calls(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        phil.call(pot, roundname=RoundName.PREFLOP)
        harry.check()
        flop = Flop(players=preflop.check_round_result(), deck=deck, pot=pot)
        phil.check()
        harry.check()

        # When
        turn = Turn(players=flop.check_round_result(), deck=deck, pot=pot)
        phil.bet(pot, roundname=RoundName.TURN, to_putin=5)
        harry.call(pot, roundname=RoundName.TURN)

        # Then
        self.assertTrue(phil.money == 143)
        self.assertTrue(harry.money == 293)
        self.assertTrue(pot.compute_total_sum() == 14)
        self.assertTrue(pot.is_balanced(RoundName.TURN))
        self.assertTrue(turn.check_round_result() == [phil, harry])

    def test_turn_result_when_all_players_but_one_fold(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        phil.call(pot, roundname=RoundName.PREFLOP)
        harry.check()
        flop = Flop(players=preflop.check_round_result(), deck=deck, pot=pot)
        phil.check()
        harry.check()

        # When
        turn = Turn(players=flop.check_round_result(), deck=deck, pot=pot)
        phil.bet(pot, roundname=RoundName.TURN, to_putin=5)
        harry.fold()

        # Then
        self.assertTrue(phil.money == 143)
        self.assertTrue(harry.money == 298)
        self.assertTrue(pot.compute_total_sum() == 9)
        self.assertFalse(pot.is_balanced(RoundName.TURN))
        self.assertTrue(turn.check_round_result() == [phil])

    def test_turn_result_when_settled(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        phil.call(pot, roundname=RoundName.PREFLOP)
        harry.check()
        flop = Flop(players=preflop.check_round_result(), deck=deck, pot=pot)
        phil.check()
        harry.check()

        # When
        turn = Turn(players=flop.check_round_result(), deck=deck, pot=pot)
        phil.bet(pot, roundname=RoundName.FLOP, to_putin=5)
        harry.fold()
        turn.settle(turn.check_round_result())

        # Then
        self.assertTrue(phil.money == 152)
        self.assertTrue(harry.money == 298)
        self.assertTrue(pot.compute_total_sum() == 0)

    def test_turn_pot_is_balanced_when_one_is_all_in(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        phil.call(pot, roundname=RoundName.PREFLOP)
        harry.check()
        flop = Flop(players=preflop.check_round_result(), deck=deck, pot=pot)
        phil.check()
        harry.check()

        # When
        turn = Turn(players=flop.check_round_result(), deck=deck, pot=pot)
        phil.bet(pot, RoundName.TURN, 9)
        harry.bet(pot, RoundName.TURN, 200)
        phil.call(pot, RoundName.TURN)

        # Then
        self.assertTrue(phil.money == 0)
        self.assertTrue(harry.money == 98)
        self.assertTrue(pot.compute_total_sum() == 352)
        self.assertTrue(pot.is_balanced(RoundName.TURN))
        self.assertTrue(turn.check_round_result() == [phil, harry])

    def test_run_turn(self):
        # Given
        game = Game()
        tom = Player("Tom Dwan", ID=ID_generator(), money=50, policy=Policy.ALWAYS_CALL)
        tom.join_game(game, position=3)
        harry = Player("Harry Potter", ID=ID_generator(), money=300, policy=Policy.ALWAYS_CALL)
        harry.join_game(game, position=1)
        anton = Player("Anton Dom", ID=ID_generator(), money=1000, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        anton.join_game(game, position=4)
        phil = Player("Phil Ivey", ID=ID_generator(), money=150, policy=Policy.ALWAYS_CALL)
        phil.join_game(game, position=0)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        remaining_players = preflop.run()
        flop = Flop(players=remaining_players, deck=deck, pot=pot)
        remaining_players = flop.run()

        # When
        turn = Turn(players=remaining_players, deck=deck, pot=pot)
        remaining_players = turn.run()

        # Then
        self.assertTrue(phil.money == 148)
        self.assertTrue(harry.money == 298)
        self.assertTrue(tom.money == 48)
        self.assertTrue(anton.money == 1_000)
        self.assertTrue(pot.is_balanced(RoundName.TURN))
        self.assertTrue(remaining_players == [phil, harry, tom])

    # --------------------------- River ----------------------------
    def test_initialize_river(self):
        # Given
        game = Game()
        tom = Player("Tom Dwan", ID=ID_generator(), money=50, policy=Policy.ALWAYS_CALL)
        tom.join_game(game, position=3)
        harry = Player("Harry Potter", ID=ID_generator(), money=300, policy=Policy.ALWAYS_CALL)
        harry.join_game(game, position=1)
        anton = Player("Anton Dom", ID=ID_generator(), money=1000, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        anton.join_game(game, position=4)
        phil = Player("Phil Ivey", ID=ID_generator(), money=150, policy=Policy.ALWAYS_CALL)
        phil.join_game(game, position=0)

        deck = Deck()
        pot = Pot()

        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        tom.call(pot, roundname=RoundName.PREFLOP)
        anton.fold()
        phil.fold()
        harry.check()

        flop = Flop(players=preflop.check_round_result(), deck=deck, pot=pot)
        harry.check()
        tom.check()

        turn = Turn(players=flop.check_round_result(), deck=deck, pot=pot)
        harry.check()
        tom.check()

        # When
        river = River(players=turn.check_round_result(), deck=deck, pot=pot)

        # Then
        self.assertTrue(deck.index == 16, "River cards should be displayed")
        self.assertTrue(phil.money == 149)
        self.assertTrue(harry.money == 298)
        self.assertTrue(tom.money == 48)
        self.assertTrue(anton.money == 1_000)
        self.assertTrue(pot.compute_total_sum() == 5)
        self.assertTrue(river.check_round_result() == [], "round has not started")

    def test_river_pot_is_unbalanced_when_one_raises(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        phil.call(pot, roundname=RoundName.PREFLOP)
        harry.check()

        flop = Flop(players=preflop.check_round_result(), deck=deck, pot=pot)
        phil.check()
        harry.check()

        turn = Turn(players=flop.check_round_result(), deck=deck, pot=pot)
        phil.check()
        harry.check()

        # When
        river = River(players=turn.check_round_result(), deck=deck, pot=pot)
        phil.bet(pot, RoundName.RIVER, 9)

        # Then
        self.assertTrue(phil.money == 139)
        self.assertTrue(harry.money == 298)
        self.assertTrue(pot.compute_total_sum() == 13)
        self.assertFalse(pot.is_balanced(RoundName.RIVER))
        self.assertTrue(river.check_round_result() == [], "round is not finished.")

    def test_river_pot_is_balanced_when_everyone_calls(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        phil.call(pot, roundname=RoundName.PREFLOP)
        harry.check()

        flop = Flop(players=preflop.check_round_result(), deck=deck, pot=pot)
        phil.check()
        harry.check()

        turn = Turn(players=flop.check_round_result(), deck=deck, pot=pot)
        phil.check()
        harry.check()

        # When
        river = River(players=turn.check_round_result(), deck=deck, pot=pot)
        phil.bet(pot, roundname=RoundName.RIVER, to_putin=5)
        harry.call(pot, roundname=RoundName.RIVER)

        # Then
        self.assertTrue(phil.money == 143)
        self.assertTrue(harry.money == 293)
        self.assertTrue(pot.compute_total_sum() == 14)
        self.assertTrue(pot.is_balanced(RoundName.RIVER))
        self.assertTrue(river.check_round_result() == [phil, harry])

    def test_river_result_when_all_players_but_one_fold(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        phil.call(pot, roundname=RoundName.PREFLOP)
        harry.check()

        flop = Flop(players=preflop.check_round_result(), deck=deck, pot=pot)
        phil.check()
        harry.check()

        turn = Turn(players=flop.check_round_result(), deck=deck, pot=pot)
        phil.check()
        harry.check()

        # When
        river = River(players=turn.check_round_result(), deck=deck, pot=pot)
        phil.bet(pot, roundname=RoundName.RIVER, to_putin=5)
        harry.fold()

        # Then
        self.assertTrue(phil.money == 143)
        self.assertTrue(harry.money == 298)
        self.assertTrue(pot.compute_total_sum() == 9)
        self.assertFalse(pot.is_balanced(RoundName.RIVER))
        self.assertTrue(river.check_round_result() == [phil])

    def test_river_result_when_settled(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        phil.call(pot, roundname=RoundName.PREFLOP)
        harry.check()

        flop = Flop(players=preflop.check_round_result(), deck=deck, pot=pot)
        phil.check()
        harry.check()

        turn = Turn(players=flop.check_round_result(), deck=deck, pot=pot)
        phil.check()
        harry.check()

        # When
        river = River(players=turn.check_round_result(), deck=deck, pot=pot)
        phil.bet(pot, roundname=RoundName.RIVER, to_putin=5)
        harry.fold()
        river.settle(turn.check_round_result())

        # Then
        self.assertTrue(phil.money == 152)
        self.assertTrue(harry.money == 298)
        self.assertTrue(pot.compute_total_sum() == 0)

    def test_river_pot_is_balanced_when_one_is_all_in(self):
        # Given
        game = Game()
        phil = Player("Phil Ivey", ID=ID_generator(), money=150)
        phil.join_game(game, position=0)
        harry = Player("Harry Potter", ID=ID_generator(), money=300)
        harry.join_game(game, position=1)

        deck = Deck()
        pot = Pot()
        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        phil.call(pot, roundname=RoundName.PREFLOP)
        harry.check()

        flop = Flop(players=preflop.check_round_result(), deck=deck, pot=pot)
        phil.check()
        harry.check()

        turn = Turn(players=flop.check_round_result(), deck=deck, pot=pot)
        phil.check()
        harry.check()

        # When
        river = River(players=turn.check_round_result(), deck=deck, pot=pot)
        phil.bet(pot, RoundName.RIVER, 9)
        harry.bet(pot, RoundName.RIVER, 200)
        phil.call(pot, RoundName.RIVER)

        # Then
        self.assertTrue(phil.money == 0)
        self.assertTrue(harry.money == 98)
        self.assertTrue(pot.compute_total_sum() == 352)
        self.assertTrue(pot.is_balanced(RoundName.RIVER))
        self.assertTrue(river.check_round_result() == [phil, harry])

    def test_run_river(self):
        # Given
        game = Game()
        tom = Player("Tom Dwan", ID=ID_generator(), money=50, policy=Policy.ALWAYS_CALL)
        tom.join_game(game, position=3)
        harry = Player("Harry Potter", ID=ID_generator(), money=300, policy=Policy.ALWAYS_CALL)
        harry.join_game(game, position=1)
        anton = Player("Anton Dom", ID=ID_generator(), money=1000, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        anton.join_game(game, position=4)
        phil = Player("Phil Ivey", ID=ID_generator(), money=150, policy=Policy.ALWAYS_CALL)
        phil.join_game(game, position=0)

        deck = Deck()
        pot = Pot()

        preflop = Preflop(players=game.get_players_in_the_game(), deck=deck, pot=pot, small_blind=1, big_blind=2)
        remaining_players = preflop.run()

        flop = Flop(players=remaining_players, deck=deck, pot=pot)
        remaining_players = flop.run()

        turn = Turn(players=remaining_players, deck=deck, pot=pot)
        remaining_players = turn.run()

        # When
        river = River(players=remaining_players, deck=deck, pot=pot)
        remaining_players = river.run()

        # Then
        self.assertTrue(phil.money == 148)
        self.assertTrue(harry.money == 298)
        self.assertTrue(tom.money == 48)
        self.assertTrue(anton.money == 1_000)
        self.assertTrue(pot.is_balanced(RoundName.TURN))
        self.assertTrue(remaining_players == [phil, harry, tom])

    # --------------------------- Game ----------------------------
    def test_game_ends_after_preflop(self):
        # Given
        game = Game()
        tom = Player("Tom Dwan", ID=ID_generator(), money=50, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        tom.join_game(game, position=3)
        harry = Player("Harry Potter", ID=ID_generator(), money=300, policy=Policy.ALWAYS_CALL)
        harry.join_game(game, position=1)
        anton = Player("Anton Dom", ID=ID_generator(), money=1000, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        anton.join_game(game, position=4)
        phil = Player("Phil Ivey", ID=ID_generator(), money=150, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        phil.join_game(game, position=0)

        # When
        game.start()

        # Then
        self.assertTrue(game.deck.index == 8)
        self.assertTrue(game.pot.compute_total_sum() == 0)
        self.assertTrue(phil.money == 149)
        self.assertTrue(harry.money == 301)
        self.assertTrue(tom.money == 50)
        self.assertTrue(anton.money == 1_000)

    def test_game_continues_after_turn(self):
        # Given
        game = Game()
        tom = Player("Tom Dwan", ID=ID_generator(), money=50, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        tom.join_game(game, position=3)
        harry = Player("Harry Potter", ID=ID_generator(), money=300, policy=Policy.ALWAYS_CALL)
        harry.join_game(game, position=1)
        anton = Player("Anton Dom", ID=ID_generator(), money=1000, policy=Policy.ALWAYS_CALL)
        anton.join_game(game, position=4)
        phil = Player("Phil Ivey", ID=ID_generator(), money=150, policy=Policy.ALWAYS_CHECK_OR_FOLD)
        phil.join_game(game, position=0)

        # When
        game.start()

        # Then
        self.assertTrue(game.deck.index == 14)
        self.assertTrue(game.pot.compute_total_sum() == 5)
        self.assertTrue(phil.money == 149)
        self.assertTrue(harry.money == 298)
        self.assertTrue(tom.money == 50)
        self.assertTrue(anton.money == 998)
