import random
import math
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
    ACE = "A"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"


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


class AnimatedCard:
    """Represents a card being animated from deck to player hand."""
    
    def __init__(self, card, start_x, start_y, end_x, end_y, duration=30):
        self.card = card
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.duration = duration
        self.elapsed = 0
        self.flip_angle = 0
    
    def update(self):
        """Update animation progress."""
        self.elapsed += 1
        # Flip effect: rotate 180 degrees over animation duration
        self.flip_angle = (self.elapsed / self.duration) * 180
    
    def is_complete(self):
        """Check if animation is complete."""
        return self.elapsed >= self.duration
    
    def get_position(self):
        """Get current position using easing."""
        progress = self.elapsed / self.duration
        # Use ease-out cubic for smooth deceleration
        eased_progress = 1 - ((1 - progress) ** 3)
        x = self.start_x + (self.end_x - self.start_x) * eased_progress
        y = self.start_y + (self.end_y - self.start_y) * eased_progress
        return x, y


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
    DARK_GREEN = (25, 100, 25)
    
    # Fonts - use system font for Unicode support
    font_large = pygame.font.SysFont('dejavusans,freesans,liberationsans,arial', 48)
    font_small = pygame.font.SysFont('dejavusans,freesans,liberationsans,arial', 24)
    font_card = pygame.font.SysFont('dejavusans,freesans,liberationsans,arial', 32, bold=True)
    
    # Game state
    deck = Deck()
    player_cards = []
    animated_cards = []
    
    # Deck position on screen
    DECK_X = 850
    DECK_Y = 250
    CARD_WIDTH = 60
    CARD_HEIGHT = 90
    
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
    
    def draw_card_visual(surface, x, y, card=None, flip_angle=0):
        """Draw a card at the given position with optional flip animation."""
        card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        
        # Create a surface for the card
        card_surface = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        
        if flip_angle > 90:
            # Back of card (show green)
            card_surface.fill(DARK_GREEN)
        else:
            # Front of card
            card_surface.fill(WHITE)
            if card:
                # Determine card color based on suit
                if card.suit in [Suit.HEARTS, Suit.DIAMONDS]:
                    card_color = RED
                else:
                    card_color = BLACK
                
                # Draw card text
                card_text = font_card.render(str(card), True, card_color)
                text_rect = card_text.get_rect(center=(CARD_WIDTH // 2, CARD_HEIGHT // 2))
                card_surface.blit(card_text, text_rect)
        
        # Draw border
        pygame.draw.rect(card_surface, BLACK, card_surface.get_rect(), 2)
        
        # Apply flip animation by scaling width
        flip_angle_rad = flip_angle * math.pi / 180
        scaled_width = int(CARD_WIDTH * abs(math.cos(flip_angle_rad)))
        
        if scaled_width > 0:
            flipped_surface = pygame.transform.scale(card_surface, (scaled_width, CARD_HEIGHT))
            surface.blit(flipped_surface, (x + (CARD_WIDTH - scaled_width) // 2, y))
        else:
            # Card is flipping, show back
            back_surface = pygame.Surface((1, CARD_HEIGHT))
            back_surface.fill(DARK_GREEN)
            surface.blit(back_surface, (x + CARD_WIDTH // 2, y))
    
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
                        # Calculate end position for the card
                        card_x = 50 + (len(player_cards) + len(animated_cards)) * 70
                        card_y = 200
                        # Create animation
                        anim = AnimatedCard(card, DECK_X, DECK_Y, card_x, card_y, duration=30)
                        animated_cards.append(anim)
                        message = f"You drew: {card}"
                    else:
                        message = "No cards left in deck!"
                    message_timer = 120
                elif reshuffle_button.is_clicked(mouse_pos):
                    deck.reset()
                    player_cards = []
                    animated_cards = []
                    message = "Deck reshuffled! Cards returned to deck."
                    message_timer = 120
                elif quit_button.is_clicked(mouse_pos):
                    running = False
        
        # Update animations
        for anim in animated_cards[:]:
            anim.update()
            if anim.is_complete():
                # Add card to player cards only when animation is done
                player_cards.append(anim.card)
                animated_cards.remove(anim)
        
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
        
        # Deck info and visual
        deck_text = font_small.render(f"Deck: {deck.cards_remaining()}", True, WHITE)
        screen.blit(deck_text, (DECK_X - 20, DECK_Y + CARD_HEIGHT + 10))
        
        # Draw deck visual
        draw_card_visual(screen, DECK_X, DECK_Y)
        
        # Draw deck shadow for 3D effect
        for i in range(1, 4):
            pygame.draw.rect(screen, BLACK, (DECK_X + i, DECK_Y + i, CARD_WIDTH, CARD_HEIGHT), 1)
        
        # Player cards
        player_text = font_small.render(f"Your cards ({len(player_cards)}):", True, WHITE)
        screen.blit(player_text, (50, 150))
        
        # Display player cards in a row
        card_x = 50
        for i, card in enumerate(player_cards):
            draw_card_visual(screen, card_x, 200, card)
            card_x += 70
        
        # Draw animated cards
        for anim in animated_cards:
            x, y = anim.get_position()
            draw_card_visual(screen, x, y, anim.card, anim.flip_angle)
        
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