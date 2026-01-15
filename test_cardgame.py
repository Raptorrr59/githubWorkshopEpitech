"""Unit tests for the card game."""
import unittest
from unittest.mock import Mock
from cardgame import Card, Deck, Suit, Rank


class TestCard(unittest.TestCase):
    """Test cases for the Card class."""
    
    def test_card_creation(self):
        """Test that a card can be created with suit and rank."""
        card = Card(Suit.HEARTS, Rank.ACE)
        self.assertEqual(card.suit, Suit.HEARTS)
        self.assertEqual(card.rank, Rank.ACE)
    
    def test_card_representation(self):
        """Test that card representation shows rank and suit."""
        card = Card(Suit.SPADES, Rank.KING)
        self.assertEqual(str(card), "K♠")


class TestDeck(unittest.TestCase):
    """Test cases for the Deck class."""
    
    def test_deck_initialization(self):
        """Test that a deck initializes with 52 cards."""
        deck = Deck()
        self.assertEqual(deck.cards_remaining(), 52)
    
    def test_deck_contains_all_cards(self):
        """Test that deck contains all 52 unique cards."""
        deck = Deck()
        card_strings = set(str(card) for card in deck.cards)
        # 4 suits * 13 ranks = 52 unique cards
        self.assertEqual(len(card_strings), 52)
    
    def test_draw_card_reduces_deck(self):
        """Test that drawing a card reduces deck size."""
        deck = Deck()
        initial_count = deck.cards_remaining()
        deck.draw_card()
        self.assertEqual(deck.cards_remaining(), initial_count - 1)
    
    def test_draw_card_returns_card(self):
        """Test that draw_card returns a Card object."""
        deck = Deck()
        card = deck.draw_card()
        self.assertIsInstance(card, Card)
    
    def test_draw_from_empty_deck(self):
        """Test that drawing from empty deck returns None."""
        deck = Deck()
        # Draw all cards
        for _ in range(52):
            deck.draw_card()
        # Try to draw from empty deck
        card = deck.draw_card()
        self.assertIsNone(card)
    
    def test_reset_deck(self):
        """Test that reset restores deck to 52 cards."""
        deck = Deck()
        # Draw some cards
        for _ in range(10):
            deck.draw_card()
        # Reset deck
        deck.reset()
        self.assertEqual(deck.cards_remaining(), 52)
    
    def test_deck_is_shuffled(self):
        """Test that deck is shuffled (cards in different order)."""
        deck1 = Deck()
        deck2 = Deck()
        # Get string representation of both decks
        deck1_order = [str(card) for card in deck1.cards]
        deck2_order = [str(card) for card in deck2.cards]
        # Decks should be in different order (very unlikely to be same if shuffled)
        self.assertNotEqual(deck1_order, deck2_order)


if __name__ == '__main__':
    unittest.main()
