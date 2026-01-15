import random
import pygame
from enum import Enum


class Suit(Enum):
    """Enum for card suits."""
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"


class Rank(Enum):
    """Enum for card ranks."""
    FOUR = "10"
    TWO = "2"
    THREE = "7"
    FIVE = "5"
    SIX = "6"
    SEVEN = "3"
    EIGHT = "8"
    NINE = "9"
    TEN = "4"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"


class Card:
    """Represents a single playing card."""
    
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank
    
    def __repr__(self):
        return f"{self.rank.value}{self.suit.value}"


class Deck:
    """Represents a deck of playing cards."""
    
    def __init__(self):
        """Initialize a standard 52-card deck."""
        self.cards = []
        self._initialize_deck()
    
    def _initialize_deck(self):
        """Create all 52 cards and shuffle the deck."""
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(suit, rank))
        random.shuffle(self.cards)
    
    def draw_card(self):
        """Draw and return the top card from the deck.
        
        Returns:
            Card: The drawn card, or None if deck is empty.
        """
        if self.cards:
            return self.cards.pop()
        return None
    
    def cards_remaining(self):
        """Return the number of cards remaining in the deck."""
        return len(self.cards)
    
    def reset(self):
        """Reset and reshuffle the deck."""
        self.cards = []
        self._initialize_deck()


# Example usage
if __name__ == "__main__":
    pygame.init()
    
    # Screen setup
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 700
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Card Game")
    clock = pygame.time.Clock()
    
    # Colors
    GREEN = (34, 139, 34)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (220, 20, 60)
    GRAY = (200, 200, 200)
    
    # Fonts - use system font for Unicode support
    # Try multiple fonts that are likely to support Unicode card symbols
    font_large = pygame.font.SysFont('dejavusans,freesans,liberationsans,arial', 48)
    font_small = pygame.font.SysFont('dejavusans,freesans,liberationsans,arial', 24)
    font_card = pygame.font.SysFont('dejavusans,freesans,liberationsans,arial', 32, bold=True)
    
    # Game state
    deck = Deck()
    player_cards = []
    
    # Button class
    class Button:
        def __init__(self, x, y, width, height, text):
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.hovered = False
        
        def draw(self, surface):
            color = (100, 150, 100) if self.hovered else (70, 130, 70)
            pygame.draw.rect(surface, color, self.rect)
            pygame.draw.rect(surface, WHITE, self.rect, 2)
            text_surface = font_small.render(self.text, True, WHITE)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)
        
        def is_clicked(self, pos):
            return self.rect.collidepoint(pos)
        
        def update_hover(self, pos):
            self.hovered = self.rect.collidepoint(pos)
    
    # Create buttons
    draw_button = Button(50, 600, 150, 60, "Draw Card")
    reshuffle_button = Button(250, 600, 150, 60, "Reshuffle")
    quit_button = Button(800, 600, 150, 60, "Quit")
    
    # Main game loop
    running = True
    message = "Welcome to Card Game! Click 'Draw Card' to begin."
    message_timer = 0
    
    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if draw_button.is_clicked(mouse_pos):
                    card = deck.draw_card()
                    if card:
                        player_cards.append(card)
                        message = f"You drew: {card}"
                    else:
                        message = "No cards left in deck!"
                    message_timer = 120
                elif reshuffle_button.is_clicked(mouse_pos):
                    deck.reset()
                    player_cards = []
                    message = "Deck reshuffled! Cards returned to deck."
                    message_timer = 120
                elif quit_button.is_clicked(mouse_pos):
                    running = False
        
        # Update button hover states
        draw_button.update_hover(mouse_pos)
        reshuffle_button.update_hover(mouse_pos)
        quit_button.update_hover(mouse_pos)
        
        # Decrease message timer
        if message_timer > 0:
            message_timer -= 1
        
        # Draw everything
        screen.fill(GREEN)
        
        # Title
        title = font_large.render("Card Game", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 20))
        
        # Deck info
        deck_text = font_small.render(f"Cards in deck: {deck.cards_remaining()}", True, WHITE)
        screen.blit(deck_text, (50, 100))
        
        # Player cards
        player_text = font_small.render(f"Your cards ({len(player_cards)}):", True, WHITE)
        screen.blit(player_text, (50, 150))
        
        # Display player cards in a row
        card_x = 50
        for i, card in enumerate(player_cards):
            # Draw card background
            card_rect = pygame.Rect(card_x, 200, 60, 90)
            pygame.draw.rect(screen, WHITE, card_rect)
            pygame.draw.rect(screen, BLACK, card_rect, 2)
            
            # Determine card color based on suit
            if card.suit in [Suit.HEARTS, Suit.DIAMONDS]:
                card_color = RED
            else:
                card_color = BLACK
            
            # Draw card text with Unicode support and appropriate color
            card_text = font_card.render(str(card), True, card_color)
            text_rect = card_text.get_rect(center=card_rect.center)
            screen.blit(card_text, text_rect)
            
            card_x += 70
        
        # Message display
        if message_timer > 0:
            msg_surface = font_small.render(message, True, WHITE)
            screen.blit(msg_surface, (50, 350))
        
        # Draw buttons
        draw_button.draw(screen)
        reshuffle_button.draw(screen)
        quit_button.draw(screen)
        
        pygame.display.flip()
    
    pygame.quit()
