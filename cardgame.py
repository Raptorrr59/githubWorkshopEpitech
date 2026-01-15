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
    
    def __init__(self, card, start_x, start_y, end_x, end_y, duration=30, to_deck=False):
        self.card = card
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.duration = duration
        self.elapsed = 0
        self.to_deck = to_deck
        
        # If card is going to deck, start at 0° (front), end at 180° (back)
        # If card is coming from deck, start at 180° (back), end at 0° (front)
        if to_deck:
            self.flip_angle = 0
        else:
            self.flip_angle = 180
    
    def update(self):
        """Update animation progress."""
        self.elapsed += 1
        if self.to_deck:
            # Flip effect: start at 0 degrees (front), flip to 180 degrees (back)
            self.flip_angle = (self.elapsed / self.duration) * 180
        else:
            # Flip effect: start at 180 degrees (back), flip to 0 degrees (front)
            self.flip_angle = 180 - (self.elapsed / self.duration) * 180
    
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
    DARK_GREEN = (0, 100, 0)
    BLUE = (30, 60, 130)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (220, 20, 60)
    DARK_BLUE = (20, 40, 100)
    LIGHT_BLUE = (100, 150, 200)
    
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
    shuffling = False
    shuffle_time = 0
    
    def draw_card_visual(surface, x, y, card=None, flip_angle=0):
        """Draw a card at the given position with optional flip animation."""
        card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        
        # Create a surface for the card
        card_surface = pygame.Surface((CARD_WIDTH, CARD_HEIGHT))
        
        if flip_angle > 90:
            # Back of card - draw decorative pattern
            card_surface.fill(DARK_BLUE)
            
            # Draw border
            pygame.draw.rect(card_surface, LIGHT_BLUE, card_surface.get_rect(), 2)
            
            # Draw decorative diamond pattern
            diamond_size = 8
            for row in range(0, CARD_HEIGHT + diamond_size, diamond_size * 2):
                for col in range(0, CARD_WIDTH + diamond_size, diamond_size * 2):
                    # Calculate points for a diamond shape
                    points = [
                        (col + diamond_size // 2, row),
                        (col + diamond_size, row + diamond_size // 2),
                        (col + diamond_size // 2, row + diamond_size),
                        (col, row + diamond_size // 2)
                    ]
                    pygame.draw.polygon(card_surface, (80, 120, 180), points, 1)
            
            # Draw center design
            center_x, center_y = CARD_WIDTH // 2, CARD_HEIGHT // 2
            pygame.draw.circle(card_surface, (100, 150, 200), (center_x, center_y), 8, 2)
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
                    # Animate all player cards back to the deck
                    shuffling = True
                    shuffle_time = 0
                    for i, card in enumerate(player_cards):
                        card_x = 50 + i * 70
                        card_y = 200
                        anim = AnimatedCard(card, card_x, card_y, DECK_X, DECK_Y, duration=30, to_deck=True)
                        animated_cards.append(anim)
                    player_cards = []
                    message = "Shuffling cards back to deck..."
                    message_timer = 120
                elif quit_button.is_clicked(mouse_pos):
                    running = False
        
        # Update animations
        for anim in animated_cards[:]:
            anim.update()
            if anim.to_deck:
                shuffle_time += 1
            if anim.is_complete():
                if anim.to_deck:
                    # Card animation returning to deck is complete
                    # Check if all animations are done
                    if all(a.is_complete() for a in animated_cards):
                        # All cards returned, reset deck
                        deck.reset()
                        shuffling = False
                        message = "Deck reshuffled! Cards returned to deck."
                        message_timer = 120
                else:
                    # Card animation from deck is complete, add to player hand
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
        
        # Calculate shake offset when shuffling
        shake_offset_x = 0
        shake_offset_y = 0
        if shuffling and animated_cards:
            # Shake the deck based on shuffle time
            shake_offset_x = int(math.sin(shuffle_time * 0.3) * 4)
            shake_offset_y = int(math.cos(shuffle_time * 0.3) * 4)
        
        # Draw deck visual
        deck_x_offset = DECK_X + shake_offset_x
        deck_y_offset = DECK_Y + shake_offset_y
        draw_card_visual(screen, deck_x_offset, deck_y_offset, card=None, flip_angle=180)
        
        # Draw spinning cards inside deck during shuffle
        if shuffling and animated_cards:
            for i in range(3):
                spin_angle = (shuffle_time * (i + 1) * 5) % 360
                spin_x = deck_x_offset + CARD_WIDTH // 2 + int(math.cos(spin_angle * math.pi / 180) * 8)
                spin_y = deck_y_offset + CARD_HEIGHT // 2 + int(math.sin(spin_angle * math.pi / 180) * 8)
                
                # Create a temporary surface for the spinning card
                temp_surface = pygame.Surface((CARD_WIDTH // 2, CARD_HEIGHT // 2), pygame.SRCALPHA)
                pygame.draw.rect(temp_surface, (100, 150, 200, 150), temp_surface.get_rect())
                pygame.draw.rect(temp_surface, LIGHT_BLUE, temp_surface.get_rect(), 1)
                
                # Rotate the card
                rotated = pygame.transform.rotate(temp_surface, spin_angle)
                rotated_rect = rotated.get_rect(center=(spin_x, spin_y))
                screen.blit(rotated, rotated_rect)
        
        # Draw deck shadow for 3D effect
        for i in range(1, 4):
            pygame.draw.rect(screen, BLACK, (deck_x_offset + i, deck_y_offset + i, CARD_WIDTH, CARD_HEIGHT), 1)
        
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