import pygame
import random
import sys

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BLACK, RED
from player import Player
from game_platform import Platform
from enemy_types import create_enemy
from sound_manager import SoundManager

pygame.init()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Jumping Jack")
        self.clock = pygame.time.Clock()
        self.running = True
        self.total_score = 0
        self.level = 1
        self.lives = 5
        self.level_transition = False
        self.transition_timer = 0
        self.score_timer = 0
        self.sound_manager = SoundManager()
        self.setup_level()

    def reset_game(self):
        self.total_score = 0
        self.level = 1
        self.lives = 5
        self.level_transition = False
        self.transition_timer = 0
        self.score_timer = 0
        self.setup_level()

    def setup_level(self):
        self.player = Player(self.sound_manager)
        self.platforms = []
        self.enemies = []
        self.base_speed = 1.5 + (self.level - 1) * 0.5
        self.invincibility_timer = FPS * 2  # 2 seconds of invincibility at start

        # 5 elevated platforms - closer together like the original
        # Player stands on ground at y=370 (no platform there)
        # First platform at y=340 (30 pixels above ground), then upward every 60 pixels
        self.platform_positions = [340, 280, 220, 160, 100]
        for i, y in enumerate(self.platform_positions):
            self.platforms.append(Platform(y, self.base_speed, i, self.platform_positions))

        # Progressive enemy spawning: X initial enemies, Y added during level
        # Level 1: 2 initial, 1 added | Level 2: 3 initial, 2 added | etc.
        self.initial_enemies = min(1 + self.level, 6)  # Start with 2, 3, 4... max 6
        self.enemies_to_spawn = min(self.level, 4)  # Add 1, 2, 3... max 4 during level
        self.enemy_spawn_timer = 0
        self.enemy_spawn_interval = FPS * 10  # Spawn new enemy every 10 seconds

        # Track which enemy types have been used to encourage variety
        self.used_enemy_types = set()

        # Level-based enemy types - unlock new enemies as levels progress
        if self.level == 1:
            self.all_enemy_types = ['snake', 'plane', 'axel', 'octopus']
        elif self.level == 2:
            self.all_enemy_types = ['snake', 'plane', 'axel', 'octopus', 'ghost']
        elif self.level == 3:
            self.all_enemy_types = ['snake', 'plane', 'axel', 'octopus', 'ghost', 'car']
        elif self.level == 4:
            self.all_enemy_types = ['snake', 'plane', 'axel', 'octopus', 'ghost', 'car', 'train']
        elif self.level == 5:
            self.all_enemy_types = ['snake', 'plane', 'axel', 'octopus', 'ghost', 'car', 'train', 'hunter']
        else:  # Level 6+
            self.all_enemy_types = ['snake', 'plane', 'axel', 'octopus', 'ghost', 'car', 'train', 'hunter', 'dinosaur']

        # Spawn initial enemies with random positions
        for _ in range(self.initial_enemies):
            self.spawn_enemy()

    def get_colors_on_screen(self):
        """Get set of all colors currently visible on screen"""
        colors_on_screen = set()
        for enemy in self.enemies:
            # Convert color tuple to a hashable format
            colors_on_screen.add(enemy.color)
        return colors_on_screen

    def spawn_enemy(self):
        """Spawn a new enemy at a random position, avoiding overlaps"""
        import random

        # Choose enemy type - prefer unused types before repeating
        available_types = [t for t in self.all_enemy_types if t not in self.used_enemy_types]
        if not available_types:
            # All types used - reset and start over
            self.used_enemy_types.clear()
            available_types = self.all_enemy_types.copy()

        chosen_type = random.choice(available_types)
        self.used_enemy_types.add(chosen_type)

        # Get all 6 possible colors for this enemy type
        from enemy_types import Snake, Plane, Axel, Octopus, Ghost, Car, Train, Hunter, Dinosaur
        enemy_class_map = {
            'snake': Snake, 'plane': Plane, 'axel': Axel, 'octopus': Octopus,
            'ghost': Ghost, 'car': Car, 'train': Train, 'hunter': Hunter, 'dinosaur': Dinosaur
        }

        # Create a temporary enemy to get its color list
        temp_class = enemy_class_map[chosen_type]
        temp_obj = temp_class(self.platform_positions, self.base_speed, 0, 0)

        # Get the colors list from the temporary object
        if chosen_type == 'snake':
            all_colors = [(50, 200, 50), (200, 200, 50), (50, 100, 200), (255, 140, 0), (0, 255, 127), (173, 216, 230)]
        elif chosen_type == 'plane':
            all_colors = [(200, 50, 50), (150, 50, 150), (255, 140, 0), (0, 191, 255), (255, 20, 147), (255, 215, 0)]
        elif chosen_type == 'axel':
            all_colors = [(255, 215, 0), (50, 200, 50), (255, 140, 0), (255, 20, 147), (0, 255, 255), (200, 50, 50)]
        elif chosen_type == 'octopus':
            all_colors = [(255, 20, 147), (50, 200, 50), (200, 50, 50), (255, 140, 0), (0, 191, 255), (150, 50, 150)]
        elif chosen_type == 'ghost':
            all_colors = [(0, 255, 255), (255, 140, 0), (255, 105, 180), (173, 216, 230), (50, 200, 50), (150, 50, 150)]
        elif chosen_type == 'car':
            all_colors = [(200, 200, 50), (0, 191, 255), (255, 140, 0), (0, 255, 127), (255, 20, 147), (200, 50, 50)]
        elif chosen_type == 'train':
            all_colors = [(138, 43, 226), (50, 200, 50), (255, 140, 0), (0, 191, 255), (255, 215, 0), (200, 50, 50)]
        elif chosen_type == 'hunter':
            all_colors = [(255, 140, 0), (50, 200, 50), (138, 43, 226), (0, 191, 255), (255, 20, 147), (200, 50, 50)]
        elif chosen_type == 'dinosaur':
            all_colors = [(0, 191, 255), (150, 50, 150), (255, 140, 0), (205, 92, 92), (255, 215, 0), (50, 200, 50)]
        else:
            all_colors = [(200, 50, 50), (50, 200, 50), (50, 100, 200), (255, 140, 0), (0, 255, 255), (255, 215, 0)]

        # Get colors currently on screen
        colors_on_screen = self.get_colors_on_screen()

        # Find colors not currently on screen
        available_colors = [c for c in all_colors if c not in colors_on_screen]

        # If all colors are on screen, use any color
        if not available_colors:
            available_colors = all_colors

        # Pick a random color from available colors
        chosen_color = random.choice(available_colors)
        color_variant = all_colors.index(chosen_color)

        max_attempts = 10
        for attempt in range(max_attempts):
            # Random platform, random starting side, random position offset
            platform_idx = random.randint(0, len(self.platform_positions) - 1)
            start_side = random.choice([-1, 1])  # -1 = left edge, 1 = right edge

            # Create temporary enemy using factory function
            temp_enemy = create_enemy(chosen_type, self.platform_positions, self.base_speed,
                                     start_platform_index=platform_idx, color_variant=color_variant)

            # Set random x position based on side
            if start_side == -1:
                # Start from left side, somewhere off-screen to 1/4 across
                temp_enemy.x = random.randint(-temp_enemy.width * 2, int(SCREEN_WIDTH * 0.25))
                temp_enemy.direction = 1  # Moving right
            else:
                # Start from right side, somewhere 3/4 across to off-screen
                temp_enemy.x = random.randint(int(SCREEN_WIDTH * 0.75),
                                             SCREEN_WIDTH + temp_enemy.width)
                temp_enemy.direction = -1  # Moving left

            # Check if this position overlaps with existing enemies
            overlaps = False
            for existing_enemy in self.enemies:
                # Check if enemies are on same platform and too close horizontally
                if (existing_enemy.current_platform_index == temp_enemy.current_platform_index):
                    x_distance = abs(existing_enemy.x - temp_enemy.x)
                    if x_distance < 100:  # Minimum 100 pixels apart
                        overlaps = True
                        break

            # Also check if enemy spawns too close to player's initial position
            # Player starts at x=100 on the ground (not on any platform)
            # Only check if enemy is on the ground level (platform index would be -1 or closest to ground)
            player_start_x = 100
            player_start_distance = abs(temp_enemy.x - player_start_x)
            # If enemy is on lowest platform and too close to player start position, skip
            if temp_enemy.current_platform_index == len(self.platform_positions) - 1:  # Closest to ground
                if player_start_distance < 150:  # Give player more space at start
                    overlaps = True

            if not overlaps:
                self.enemies.append(temp_enemy)
                return

        # If all attempts failed, just add it anyway
        self.enemies.append(temp_enemy)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if self.level_transition:
                        self.level_transition = False
                        self.setup_level()
                    else:
                        self.player.jump()
                elif event.key == pygame.K_r and self.lives <= 0:
                    self.reset_game()

    def update(self):
        if self.level_transition:
            self.transition_timer += 1
            if self.transition_timer >= FPS * 3:
                self.level_transition = False
                self.setup_level()
            return

        keys = pygame.key.get_pressed()
        moved = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
            moved = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
            moved = True

        # Reset direction if not moving
        if not moved:
            self.player.last_direction = 0

        for platform in self.platforms:
            platform.update()

        for enemy in self.enemies:
            enemy.update()

        self.player.update(self.platforms)

        if self.player.y <= 0:
            self.level += 1
            self.level_transition = True
            self.transition_timer = 0
            self.sound_manager.play('level_complete')
            return

        # Decrease invincibility timer
        if self.invincibility_timer > 0:
            self.invincibility_timer -= 1

        # Only check collisions if not invincible
        if self.invincibility_timer <= 0:
            if self.player.check_crushed(self.platforms):
                self.lives -= 1
                self.player.x = 100
                self.player.y = 370 - 32  # Standing on ground at y=370, player height is 32
                self.player.velocity_y = 0
                self.player.jumping = False
                self.invincibility_timer = FPS * 1  # 1 second invincibility after death
                self.sound_manager.play('death')

            for enemy in self.enemies:
                if enemy.check_collision(self.player):
                    self.lives -= 1
                    self.player.x = 100
                    self.player.y = 370 - 32  # Standing on ground at y=370, player height is 32
                    self.player.velocity_y = 0
                    self.player.jumping = False
                    self.invincibility_timer = FPS * 1  # 1 second invincibility after death
                    self.sound_manager.play('death')
                    break

        self.score_timer += 1
        if self.score_timer >= FPS:
            self.total_score += 10
            self.score_timer = 0

        # Progressive enemy spawning during level
        if self.enemies_to_spawn > 0:
            self.enemy_spawn_timer += 1
            if self.enemy_spawn_timer >= self.enemy_spawn_interval:
                self.spawn_enemy()
                self.enemies_to_spawn -= 1
                self.enemy_spawn_timer = 0

        # Update sound manager cooldowns
        self.sound_manager.update()

    def draw(self):
        if self.level_transition:
            self.screen.fill(WHITE)
            font_large = pygame.font.Font(None, 96)
            font_small = pygame.font.Font(None, 48)

            level_text = font_large.render(f"LEVEL {self.level}", True, BLACK)
            instruction_text = font_small.render("Press SPACE to continue", True, BLACK)

            level_rect = level_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))

            self.screen.blit(level_text, level_rect)
            self.screen.blit(instruction_text, instruction_rect)
        else:
            self.screen.fill(WHITE)

            for platform in self.platforms:
                platform.draw(self.screen, self.platforms)

            for enemy in self.enemies:
                enemy.draw(self.screen)

            self.player.draw(self.screen)

            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.total_score}", True, BLACK)
            lives_text = font.render(f"Lives: {self.lives}", True, BLACK)
            level_text = font.render(f"Level: {self.level}", True, BLACK)

            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (10, 50))
            self.screen.blit(level_text, (SCREEN_WIDTH - 150, 10))

            if self.lives <= 0:
                game_over_font = pygame.font.Font(None, 72)
                game_over_text = game_over_font.render("GAME OVER", True, RED)
                restart_text = font.render("Press R to Restart", True, BLACK)

                text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
                restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20))

                self.screen.blit(game_over_text, text_rect)
                self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()

            if self.lives > 0:
                self.update()

            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
