import pygame
import random
import sys
import urllib.request
import os

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (135, 206, 250)
GREEN = (34, 139, 34)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Bird Constants
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
BIRD_X = 100
GRAVITY = 0.5
JUMP_STRENGTH = -10

# Pipe Constants
PIPE_WIDTH = 70
PIPE_GAP = 200
PIPE_SPEED = 3
PIPE_SPAWN_FREQUENCY = 90  # frames

# Asset URLs
ASSETS = {
    'yellow_bird1': 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/yellowbird-downflap.png',
    'yellow_bird2': 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/yellowbird-midflap.png',
    'yellow_bird3': 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/yellowbird-upflap.png',
    'blue_bird1': 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/bluebird-downflap.png',
    'blue_bird2': 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/bluebird-midflap.png',
    'blue_bird3': 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/bluebird-upflap.png',
    'red_bird1': 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/redbird-downflap.png',
    'red_bird2': 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/redbird-midflap.png',
    'red_bird3': 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/redbird-upflap.png',
    'pipe': 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/pipe-green.png',
    'background': 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/background-day.png',
    'base': 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/base.png',
    'message': 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/message.png',
    'gameover': 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/sprites/gameover.png',
    'font': 'https://github.com/google/fonts/raw/main/ofl/pressstart2p/PressStart2P-Regular.ttf'
}

SOUNDS = {
    'wing': 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/audio/wing.wav',
    'point': 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/audio/point.wav',
    'hit': 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/audio/hit.wav',
    'die': 'https://raw.githubusercontent.com/samuelcust/flappy-bird-assets/master/audio/die.wav'
}

def download_assets():
    """Download game assets if they don't exist"""
    assets_dir = 'assets'
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    for name, url in ASSETS.items():
        if name == 'font':
            filepath = os.path.join(assets_dir, f'{name}.ttf')
        else:
            filepath = os.path.join(assets_dir, f'{name}.png')
        if not os.path.exists(filepath):
            try:
                print(f'Downloading {name}...')
                urllib.request.urlretrieve(url, filepath)
            except Exception as e:
                print(f'Failed to download {name}: {e}')
    
    for name, url in SOUNDS.items():
        filepath = os.path.join(assets_dir, f'{name}.wav')
        if not os.path.exists(filepath):
            try:
                print(f'Downloading {name} sound...')
                urllib.request.urlretrieve(url, filepath)
            except Exception as e:
                print(f'Failed to download {name} sound: {e}')
    
    return assets_dir

def load_assets(assets_dir):
    """Load all game assets"""
    images = {}
    try:
        # Load bird animation frames for all colors
        images['bird_frames'] = {
            'yellow': [
                pygame.image.load(os.path.join(assets_dir, 'yellow_bird1.png')).convert_alpha(),
                pygame.image.load(os.path.join(assets_dir, 'yellow_bird2.png')).convert_alpha(),
                pygame.image.load(os.path.join(assets_dir, 'yellow_bird3.png')).convert_alpha()
            ],
            'blue': [
                pygame.image.load(os.path.join(assets_dir, 'blue_bird1.png')).convert_alpha(),
                pygame.image.load(os.path.join(assets_dir, 'blue_bird2.png')).convert_alpha(),
                pygame.image.load(os.path.join(assets_dir, 'blue_bird3.png')).convert_alpha()
            ],
            'red': [
                pygame.image.load(os.path.join(assets_dir, 'red_bird1.png')).convert_alpha(),
                pygame.image.load(os.path.join(assets_dir, 'red_bird2.png')).convert_alpha(),
                pygame.image.load(os.path.join(assets_dir, 'red_bird3.png')).convert_alpha()
            ]
        }
        
        images['pipe'] = pygame.image.load(os.path.join(assets_dir, 'pipe.png')).convert_alpha()
        images['background'] = pygame.image.load(os.path.join(assets_dir, 'background.png')).convert_alpha()
        images['base'] = pygame.image.load(os.path.join(assets_dir, 'base.png')).convert_alpha()
        images['message'] = pygame.image.load(os.path.join(assets_dir, 'message.png')).convert_alpha()
        images['gameover'] = pygame.image.load(os.path.join(assets_dir, 'gameover.png')).convert_alpha()
    except Exception as e:
        print(f'Error loading assets: {e}')
        return None
    
    # Try to load custom font
    font_path = os.path.join(assets_dir, 'font.ttf')
    if os.path.exists(font_path):
        images['custom_font'] = font_path
    
    return images

def load_sounds(assets_dir):
    """Load all game sounds"""
    sounds = {}
    #Loading assets from different sounds extracted from github
    try:
        pygame.mixer.init()
        sounds['wing'] = pygame.mixer.Sound(os.path.join(assets_dir, 'wing.wav'))
        sounds['point'] = pygame.mixer.Sound(os.path.join(assets_dir, 'point.wav'))
        sounds['hit'] = pygame.mixer.Sound(os.path.join(assets_dir, 'hit.wav'))
        sounds['die'] = pygame.mixer.Sound(os.path.join(assets_dir, 'die.wav'))
    except Exception as e:
        print(f'Error loading sounds: {e}')
        return None
    return sounds

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-4, -1)
        self.color = color
        self.size = random.randint(2, 5)
        self.lifetime = random.randint(20, 40)
        self.age = 0
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.2  # gravity
        self.age += 1
        
    def draw(self, screen):
        alpha = int(255 * (1 - self.age / self.lifetime))
        if alpha > 0:
            s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
            color_with_alpha = (*self.color, alpha)
            pygame.draw.circle(s, color_with_alpha, (self.size, self.size), self.size)
            screen.blit(s, (int(self.x - self.size), int(self.y - self.size)))
    
    def is_dead(self):
        return self.age >= self.lifetime

class Bird:
    def __init__(self, frames=None):
        self.x = BIRD_X
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.frames = frames
        self.frame_index = 0
        if frames and len(frames) > 0:
            self.width = frames[0].get_width()
            self.height = frames[0].get_height()
        else:
            self.width = BIRD_WIDTH
            self.height = BIRD_HEIGHT
        
    def jump(self):
        self.velocity = JUMP_STRENGTH
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
    def draw(self, screen):
        if self.frames and len(self.frames) > 0:
            # Get current frame
            current_frame = self.frames[self.frame_index]
            # Rotate bird based on velocity
            angle = -self.velocity * 3
            angle = max(-90, min(angle, 45))
            rotated_image = pygame.transform.rotozoom(current_frame, angle, 1)
            rotated_rect = rotated_image.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
            screen.blit(rotated_image, rotated_rect)
        else:
            # Fallback to drawn bird
            pygame.draw.ellipse(screen, YELLOW, (self.x, self.y, self.width, self.height))
            pygame.draw.circle(screen, BLACK, (self.x + 30, self.y + 10), 5)
            beak_points = [(self.x + self.width, self.y + 15),
                           (self.x + self.width + 10, self.y + 12),
                           (self.x + self.width, self.y + 18)]
            pygame.draw.polygon(screen, RED, beak_points)
    
    def animate(self):
        """Cycle through animation frames"""
        if self.frames:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Pipe:
    def __init__(self, x, image=None, base_y=None):
        self.x = x
        self.image = image
        self.base_y = base_y if base_y else SCREEN_HEIGHT - 50
        if image:
            self.width = image.get_width()
        else:
            self.width = PIPE_WIDTH
        self.gap_y = random.randint(150, int(self.base_y) - 250)
        self.passed = False
        
    def update(self):
        self.x -= PIPE_SPEED
        
    def draw(self, screen):
        if self.image:
            # Top pipe (flipped)
            top_pipe = pygame.transform.flip(self.image, False, True)
            pipe_height = self.gap_y
            # Tile the pipe vertically
            for y in range(0, pipe_height, self.image.get_height()):
                if y + self.image.get_height() > pipe_height:
                    # Crop the last tile
                    crop_height = pipe_height - y
                    cropped = pygame.Surface((self.image.get_width(), crop_height), pygame.SRCALPHA)
                    cropped.blit(top_pipe, (0, 0), (0, self.image.get_height() - crop_height, self.image.get_width(), crop_height))
                    screen.blit(cropped, (self.x, y))
                else:
                    screen.blit(top_pipe, (self.x, y))
            
            # Bottom pipe - stop at ground level
            bottom_pipe_y = self.gap_y + PIPE_GAP
            for y in range(bottom_pipe_y, int(self.base_y), self.image.get_height()):
                if y + self.image.get_height() > self.base_y:
                    # Crop the last tile to stop at ground
                    crop_height = int(self.base_y - y)
                    if crop_height > 0:
                        cropped = pygame.Surface((self.image.get_width(), crop_height), pygame.SRCALPHA)
                        cropped.blit(self.image, (0, 0), (0, 0, self.image.get_width(), crop_height))
                        screen.blit(cropped, (self.x, y))
                else:
                    screen.blit(self.image, (self.x, y))
        else:
            # Fallback to drawn pipes
            pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.gap_y))
            pygame.draw.rect(screen, BLACK, (self.x, 0, self.width, self.gap_y), 2)
            pygame.draw.rect(screen, GREEN, (self.x - 5, self.gap_y - 20, self.width + 10, 20))
            pygame.draw.rect(screen, BLACK, (self.x - 5, self.gap_y - 20, self.width + 10, 20), 2)
            bottom_pipe_y = self.gap_y + PIPE_GAP
            pygame.draw.rect(screen, GREEN, (self.x, bottom_pipe_y, self.width, SCREEN_HEIGHT - bottom_pipe_y))
            pygame.draw.rect(screen, BLACK, (self.x, bottom_pipe_y, self.width, SCREEN_HEIGHT - bottom_pipe_y), 2)
            pygame.draw.rect(screen, GREEN, (self.x - 5, bottom_pipe_y, self.width + 10, 20))
            pygame.draw.rect(screen, BLACK, (self.x - 5, bottom_pipe_y, self.width + 10, 20), 2)
        
    def collides_with(self, bird):
        bird_rect = bird.get_rect()
        
        # Top pipe collision
        top_pipe_rect = pygame.Rect(self.x, 0, self.width, self.gap_y)
        if bird_rect.colliderect(top_pipe_rect):
            return True
            
        # Bottom pipe collision - only up to ground level
        bottom_pipe_y = self.gap_y + PIPE_GAP
        bottom_pipe_height = self.base_y - bottom_pipe_y
        bottom_pipe_rect = pygame.Rect(self.x, bottom_pipe_y, self.width, bottom_pipe_height)
        if bird_rect.colliderect(bottom_pipe_rect):
            return True
            
        return False
        
    def is_off_screen(self):
        return self.x + self.width < 0

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        
        # Load assets
        print('Loading assets...')
        assets_dir = download_assets()
        self.images = load_assets(assets_dir)
        self.sounds = load_sounds(assets_dir)
        
        # Load custom font or use system fonts
        if self.images and self.images.get('custom_font'):
            try:
                self.font = pygame.font.Font(self.images['custom_font'], 42)
                self.small_font = pygame.font.Font(self.images['custom_font'], 20)
                self.tiny_font = pygame.font.Font(self.images['custom_font'], 14)
            except:
                self.font = pygame.font.SysFont('arial', 54, bold=True)
                self.small_font = pygame.font.SysFont('arial', 24, bold=True)
                self.tiny_font = pygame.font.SysFont('arial', 18, bold=False)
        else:
            self.font = pygame.font.SysFont('arial', 54, bold=True)
            self.small_font = pygame.font.SysFont('arial', 24, bold=True)
            self.tiny_font = pygame.font.SysFont('arial', 18, bold=False)
        
        # Bird animation timer
        self.bird_anim_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.bird_anim_timer, 200)
        
        # Scale background to fit screen
        if self.images and self.images.get('background'):
            self.images['background'] = pygame.transform.scale(self.images['background'], (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Scale base to fit screen width and position at bottom
        if self.images and self.images.get('base'):
            base_height = self.images['base'].get_height()
            self.images['base'] = pygame.transform.scale(self.images['base'], (SCREEN_WIDTH, base_height))
            self.base_y = SCREEN_HEIGHT - base_height
        else:
            self.base_y = SCREEN_HEIGHT - 50
        
        self.base_x = 0
        self.reset()
        
    def reset(self):
        # Select random bird color
        if not hasattr(self, 'bird_color'):
            self.bird_color = random.choice(['yellow', 'blue', 'red'])
        
        if self.images and 'bird_frames' in self.images:
            bird_frames = self.images['bird_frames'].get(self.bird_color, self.images['bird_frames']['yellow'])
        else:
            bird_frames = None
        
        self.bird = Bird(bird_frames)
        self.pipes = []
        self.score = 0
        self.frame_count = 0
        self.game_over = False
        self.game_started = False
        self.paused = False
        self.particles = []
        
        # Load high score from file
        if not hasattr(self, 'high_score'):
            try:
                with open('highscore.txt', 'r') as f:
                    self.high_score = int(f.read())
            except:
                self.high_score = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == self.bird_anim_timer:
                self.bird.animate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        # Change bird color on restart
                        self.bird_color = random.choice(['yellow', 'blue', 'red'])
                        self.reset()
                    elif not self.game_started:
                        self.game_started = True
                        self.bird.jump()
                        if self.sounds:
                            self.sounds['wing'].play()
                        # Create particles on jump
                        self.create_jump_particles()
                    elif not self.paused:
                        self.bird.jump()
                        if self.sounds:
                            self.sounds['wing'].play()
                        # Create particles on jump
                        self.create_jump_particles()
                if event.key == pygame.K_p and self.game_started and not self.game_over:
                    self.paused = not self.paused
                if event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def create_jump_particles(self):
        """Create particles when bird jumps"""
        bird_colors = {
            'yellow': (255, 215, 0),
            'blue': (100, 149, 237),
            'red': (220, 20, 60)
        }
        color = bird_colors.get(self.bird_color, (255, 255, 255))
        for _ in range(5):
            self.particles.append(Particle(self.bird.x + self.bird.width // 2, 
                                          self.bird.y + self.bird.height, color))
    
    def create_score_particles(self):
        """Create particles when scoring"""
        for _ in range(10):
            self.particles.append(Particle(SCREEN_WIDTH // 2, 60, (255, 215, 0)))
        
    def update(self):
        # Update particles always
        for particle in self.particles[:]:
            particle.update()
            if particle.is_dead():
                self.particles.remove(particle)
        
        if not self.game_started or self.game_over or self.paused:
            return
            
        # Update bird
        self.bird.update()
        
        # Check if bird hit ground or ceiling
        if self.bird.y + self.bird.height >= self.base_y or self.bird.y < 0:
            if not self.game_over:
                if self.sounds:
                    self.sounds['die'].play()
                self.save_high_score()
            self.game_over = True
            
        # Update pipes
        self.frame_count += 1
        if self.frame_count % PIPE_SPAWN_FREQUENCY == 0:
            pipe_image = self.images.get('pipe') if self.images else None
            self.pipes.append(Pipe(SCREEN_WIDTH, pipe_image, self.base_y))
            
        for pipe in self.pipes[:]:
            pipe.update()
            
            # Check collision
            if pipe.collides_with(self.bird):
                if not self.game_over:
                    if self.sounds:
                        self.sounds['hit'].play()
                    self.save_high_score()
                self.game_over = True
                
            # Check if bird passed pipe
            if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                pipe.passed = True
                self.score += 1
                if self.sounds:
                    self.sounds['point'].play()
                # Create score particles
                self.create_score_particles()
                
            # Remove off-screen pipes
            if pipe.is_off_screen():
                self.pipes.remove(pipe)
    
    def save_high_score(self):
        """Save high score if current score is higher"""
        if self.score > self.high_score:
            self.high_score = self.score
            try:
                with open('highscore.txt', 'w') as f:
                    f.write(str(self.high_score))
            except:
                pass
                
    def draw(self):
        # Draw background
        if self.images and self.images.get('background'):
            self.screen.blit(self.images['background'], (0, 0))
        else:
            self.screen.fill(BLUE)
        
        # Draw and scroll base (ground)
        if self.images and self.images.get('base'):
            if self.game_started and not self.game_over:
                self.base_x -= PIPE_SPEED
                if self.base_x <= -SCREEN_WIDTH:
                    self.base_x = 0
            self.screen.blit(self.images['base'], (self.base_x, self.base_y))
            self.screen.blit(self.images['base'], (self.base_x + SCREEN_WIDTH, self.base_y))
        
        # Draw bird
        self.bird.draw(self.screen)
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(self.screen)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
            
        # Draw score with outline for visibility
        if self.game_started and not self.game_over:
            score_str = str(self.score)
            # Draw outline
            for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2), (-2, 0), (2, 0), (0, -2), (0, 2)]:
                score_outline = self.font.render(score_str, True, BLACK)
                outline_rect = score_outline.get_rect(center=(SCREEN_WIDTH // 2 + dx, 55 + dy))
                self.screen.blit(score_outline, outline_rect)
            
            # Draw main score
            score_text = self.font.render(score_str, True, WHITE)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 55))
            self.screen.blit(score_text, score_rect)
        
        # Draw pause overlay
        if self.paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            pause_text = self.font.render("PAUSED", True, WHITE)
            pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
            self.screen.blit(pause_text, pause_rect)
            
            continue_text = self.small_font.render("Press P to Continue", True, WHITE)
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
            self.screen.blit(continue_text, continue_rect)
        
        # Draw start message
        if not self.game_started:
            if self.images and self.images.get('message'):
                msg = self.images['message']
                msg_rect = msg.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(msg, msg_rect)
            else:
                start_text = self.small_font.render("Press SPACE to Start", True, WHITE)
                start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(start_text, start_rect)
            
        # Draw game over screen
        if self.game_over:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            # Draw GAME OVER sprite or text
            if self.images and self.images.get('gameover'):
                gameover = self.images['gameover']
                gameover_rect = gameover.get_rect(center=(SCREEN_WIDTH // 2, 100))
                self.screen.blit(gameover, gameover_rect)
            else:
                game_over_text = self.font.render("GAME OVER", True, RED)
                game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
                self.screen.blit(game_over_text, game_over_rect)
            
            # Draw score panel with rounded appearance
            panel_width = 300
            panel_height = 150
            panel_x = (SCREEN_WIDTH - panel_width) // 2
            panel_y = 180
            
            # Draw panel shadow
            shadow_offset = 4
            pygame.draw.rect(self.screen, (100, 95, 70), (panel_x + shadow_offset, panel_y + shadow_offset, panel_width, panel_height), border_radius=10)
            
            # Draw main panel
            pygame.draw.rect(self.screen, (240, 230, 180), (panel_x, panel_y, panel_width, panel_height), border_radius=10)
            pygame.draw.rect(self.screen, (200, 185, 130), (panel_x, panel_y, panel_width, panel_height), 5, border_radius=10)
            
            # Draw divider line
            divider_y = panel_y + panel_height // 2
            pygame.draw.line(self.screen, (200, 185, 130), (panel_x + 20, divider_y), (panel_x + panel_width - 20, divider_y), 2)
            
            # Draw scores with better styling
            score_label = self.small_font.render("SCORE", True, (100, 90, 70))
            self.screen.blit(score_label, (panel_x + 25, panel_y + 25))
            score_value = self.font.render(str(self.score), True, (60, 55, 40))
            score_value_rect = score_value.get_rect(right=panel_x + panel_width - 25, centery=panel_y + 42)
            self.screen.blit(score_value, score_value_rect)
            
            best_label = self.small_font.render("BEST", True, (100, 90, 70))
            self.screen.blit(best_label, (panel_x + 25, panel_y + 90))
            best_value = self.font.render(str(self.high_score), True, (60, 55, 40))
            best_value_rect = best_value.get_rect(right=panel_x + panel_width - 25, centery=panel_y + 107)
            self.screen.blit(best_value, best_value_rect)
            
            # Draw restart instruction with styled background
            restart_y = panel_y + panel_height + 30
            
            # First render text to get its size
            restart_text = self.tiny_font.render("Press SPACE to Restart", True, WHITE)
            text_width = restart_text.get_width()
            
            # Make button fit text with padding
            restart_width = text_width + 20
            restart_height = 35
            restart_x = (SCREEN_WIDTH - restart_width) // 2
            
            # Draw button shadow
            pygame.draw.rect(self.screen, (40, 40, 40), (restart_x + 3, restart_y + 3, restart_width, restart_height), border_radius=8)
            
            # Draw button
            pygame.draw.rect(self.screen, (70, 70, 70), (restart_x, restart_y, restart_width, restart_height), border_radius=8)
            pygame.draw.rect(self.screen, (120, 120, 120), (restart_x, restart_y, restart_width, restart_height), 3, border_radius=8)
            
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, restart_y + restart_height // 2))
            self.screen.blit(restart_text, restart_rect)
            
            # Show bird color hint (smaller and closer)
            color_hint = self.tiny_font.render("(New random color)", True, (180, 180, 180))
            color_rect = color_hint.get_rect(center=(SCREEN_WIDTH // 2, restart_y + restart_height + 15))
            self.screen.blit(color_hint, color_rect)
        
        # Draw controls hint above the ground (when playing)
        if self.game_started and not self.game_over and not self.paused:
            controls_text = self.tiny_font.render("Press P to Pause", True, (150, 150, 150))
            controls_rect = controls_text.get_rect(center=(SCREEN_WIDTH // 2, self.base_y - 20))
            self.screen.blit(controls_text, controls_rect)
            
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
