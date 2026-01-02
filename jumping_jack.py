import pygame
import random
import sys

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, WHITE, BLACK, RED, BLUE
from player import Player
from game_platform import Platform
from enemy_types import create_enemy
from sound_manager import SoundManager
from leaderboard import Leaderboard

pygame.init()


class Game:
    def __init__(self, debug_mode=False):
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
        self.debug_mode = debug_mode
        self.leaderboard = Leaderboard()
        self.player_name = ""
        self.name_entry_active = True
        self.game_started = False
        self.show_leaderboard = False

    def reset_game(self):
        self.total_score = 0
        self.level = 1
        self.lives = 5
        self.level_transition = False
        self.transition_timer = 0
        self.score_timer = 0
        self.name_entry_active = True
        self.game_started = False
        self.show_leaderboard = False
        # Keep player_name to show as default in name entry

    def setup_level(self):
        self.player = Player(self.sound_manager)
        self.platforms = []
        self.enemies = []
        # More gradual speed increase: +0.2 per level
        # Level 1: 1.2, Level 2: 1.4, Level 3: 1.6, Level 6: 2.2, Level 10: 3.0
        self.base_speed = 1.2 + (self.level - 1) * 0.2
        self.invincibility_timer = FPS * 2  # 2 seconds of invincibility at start

        # 5 elevated platforms - closer together like the original
        # Player stands on ground at y=370 (no platform there)
        # First platform at y=340 (30 pixels above ground), then upward every 60 pixels
        self.platform_positions = [340, 280, 220, 160, 100]

        # Number of gaps increases with level: Level 1 = 6 gaps, Level 2 = 7 gaps, etc.
        num_gaps = 5 + self.level

        # Create gaps with random starting platforms - gaps may naturally meet on same platform
        # if they move there from different directions
        # Each gap gets a unique ID (0, 1, 2, ...) to track its movement in debug mode
        for gap_index in range(num_gaps):
            # Each gap starts on a random platform
            platform_index = random.randint(0, len(self.platform_positions) - 1)
            y = self.platform_positions[platform_index]
            self.platforms.append(Platform(y, self.base_speed, platform_index, self.platform_positions, gap_id=gap_index))

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
                if self.name_entry_active:
                    # Handle name entry
                    if event.key == pygame.K_RETURN:
                        if not self.player_name:
                            self.player_name = self.leaderboard.get_last_player_name() or "Anonymous"
                        self.name_entry_active = False
                        self.game_started = True
                        self.setup_level()
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        # Load last player name as default
                        self.player_name = self.leaderboard.get_last_player_name()
                    elif len(self.player_name) < 20:  # Limit name length
                        if event.unicode.isprintable():
                            self.player_name += event.unicode
                elif event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    if self.level_transition:
                        self.level_transition = False
                        self.setup_level()
                    elif self.game_started:
                        self.player.jump()
                elif event.key == pygame.K_r:
                    if self.lives <= 0:
                        self.reset_game()
                    elif self.show_leaderboard:
                        self.show_leaderboard = False
                elif event.key == pygame.K_l and self.lives <= 0:
                    # Toggle leaderboard display
                    self.show_leaderboard = not self.show_leaderboard

    def update(self):
        # Don't update if game hasn't started yet (still in name entry)
        if not self.game_started:
            return

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

        self.player.update(self.platforms, self.platform_positions)

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
                if self.lives <= 0:
                    # Game over - save score and show leaderboard
                    self.leaderboard.add_score(self.player_name, self.total_score, self.level)
                    self.show_leaderboard = True
                self.player.x = 100
                self.player.y = 370 - 32  # Standing on ground at y=370, player height is 32
                self.player.velocity_y = 0
                self.player.jumping = False
                self.invincibility_timer = FPS * 1  # 1 second invincibility after death
                self.sound_manager.play('death')

            for enemy in self.enemies:
                if enemy.check_collision(self.player):
                    self.lives -= 1
                    if self.lives <= 0:
                        # Game over - save score and show leaderboard
                        self.leaderboard.add_score(self.player_name, self.total_score, self.level)
                        self.show_leaderboard = True
                    self.player.x = 100
                    self.player.y = 370 - 32  # Standing on ground at y=370, player height is 32
                    self.player.velocity_y = 0
                    self.player.jumping = False
                    self.invincibility_timer = FPS * 1  # 1 second invincibility after death
                    self.sound_manager.play('death')
                    break

        # Only increment score when player is not on the ground
        if self.player.y < 370 - 32:  # Ground level is 370, player height is 32
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
        if self.name_entry_active:
            self.draw_name_entry()
        elif self.level_transition:
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

            # Draw each of the 5 physical platform bars
            # For each platform level, find ALL gaps currently on it and render them
            for platform_index in range(len(self.platform_positions)):
                y = self.platform_positions[platform_index]

                # Find ALL gaps currently on this platform level
                active_gaps = []
                for gap in self.platforms:
                    if gap.gap_current_platform_index == platform_index:
                        active_gaps.append(gap)

                if active_gaps:
                    # Draw platform with gaps
                    # Draw solid platform first
                    pygame.draw.rect(self.screen, RED, (0, y, SCREEN_WIDTH, 3))

                    # Then cut out the gaps
                    for active_gap in active_gaps:
                        gap_actual_start = active_gap.gap_start + active_gap.x_offset
                        gap_actual_end = gap_actual_start + active_gap.gap_width

                        while gap_actual_start < 0:
                            gap_actual_start += SCREEN_WIDTH
                            gap_actual_end += SCREEN_WIDTH

                        gap_actual_start = gap_actual_start % SCREEN_WIDTH
                        gap_actual_end = gap_actual_end % SCREEN_WIDTH

                        if gap_actual_end < gap_actual_start:
                            # Gap wraps around screen edge
                            pygame.draw.rect(self.screen, WHITE, (gap_actual_start, y, SCREEN_WIDTH - gap_actual_start, 3))
                            pygame.draw.rect(self.screen, WHITE, (0, y, gap_actual_end, 3))
                        else:
                            # Gap doesn't wrap
                            pygame.draw.rect(self.screen, WHITE, (gap_actual_start, y, gap_actual_end - gap_actual_start, 3))

                        # Draw gap ID in debug mode
                        if self.debug_mode:
                            font = pygame.font.Font(None, 24)
                            gap_text = font.render(str(active_gap.gap_id), True, BLUE)
                            gap_center = (gap_actual_start + active_gap.gap_width / 2) % SCREEN_WIDTH
                            self.screen.blit(gap_text, (gap_center - 6, y - 2))
                else:
                    # No gaps on this platform level - draw solid platform
                    pygame.draw.rect(self.screen, RED, (0, y, SCREEN_WIDTH, 3))

            for enemy in self.enemies:
                enemy.draw(self.screen)

            self.player.draw(self.screen)

            font = pygame.font.Font(None, 36)
            score_text = font.render(f"Score: {self.total_score}", True, BLACK)
            level_text = font.render(f"Level: {self.level}", True, BLACK)

            self.screen.blit(score_text, (10, 10))

            # Draw lives as Jack sprites instead of text
            lives_label = font.render("Lives:", True, BLACK)
            self.screen.blit(lives_label, (10, 50))
            for i in range(self.lives):
                Player.draw_small_jack(self.screen, 90 + i * 15, 53)

            self.screen.blit(level_text, (SCREEN_WIDTH - 150, 10))

            if self.lives <= 0:
                if self.show_leaderboard:
                    self.draw_leaderboard()
                else:
                    game_over_font = pygame.font.Font(None, 72)
                    game_over_text = game_over_font.render("GAME OVER", True, RED)
                    restart_text = font.render("Press R to Restart", True, BLACK)
                    leaderboard_text = font.render("Press L for Leaderboard", True, BLACK)

                    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 80))
                    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20))
                    leaderboard_rect = leaderboard_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 60))

                    self.screen.blit(game_over_text, text_rect)
                    self.screen.blit(restart_text, restart_rect)
                    self.screen.blit(leaderboard_text, leaderboard_rect)

        pygame.display.flip()

    def draw_name_entry(self):
        """Draw the name entry screen"""
        self.screen.fill(WHITE)
        font_title = pygame.font.Font(None, 72)
        font_normal = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 28)

        # Title
        title_text = font_title.render("JUMPING JACK", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, 100))
        self.screen.blit(title_text, title_rect)

        # Instructions
        prompt_text = font_normal.render("Enter your name:", True, BLACK)
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH/2, 220))
        self.screen.blit(prompt_text, prompt_rect)

        # Name input box
        name_display = self.player_name if self.player_name else self.leaderboard.get_last_player_name()
        name_box_width = 400
        name_box_height = 50
        name_box_x = SCREEN_WIDTH/2 - name_box_width/2
        name_box_y = 270

        # Draw box
        pygame.draw.rect(self.screen, BLACK, (name_box_x, name_box_y, name_box_width, name_box_height), 2)

        # Draw name text
        name_text = font_normal.render(name_display, True, BLACK)
        name_text_rect = name_text.get_rect(center=(SCREEN_WIDTH/2, name_box_y + name_box_height/2))
        self.screen.blit(name_text, name_text_rect)

        # Cursor blinking
        if pygame.time.get_ticks() % 1000 < 500:
            cursor_x = name_text_rect.right + 5
            cursor_y = name_box_y + 10
            pygame.draw.line(self.screen, BLACK, (cursor_x, cursor_y), (cursor_x, cursor_y + 30), 2)

        # Instructions
        hint1 = font_small.render("Press ENTER to start", True, BLACK)
        hint2 = font_small.render("Press ESC to use last player name", True, BLACK)
        hint3 = font_small.render("Press BACKSPACE to delete", True, BLACK)

        hint1_rect = hint1.get_rect(center=(SCREEN_WIDTH/2, 380))
        hint2_rect = hint2.get_rect(center=(SCREEN_WIDTH/2, 415))
        hint3_rect = hint3.get_rect(center=(SCREEN_WIDTH/2, 450))

        self.screen.blit(hint1, hint1_rect)
        self.screen.blit(hint2, hint2_rect)
        self.screen.blit(hint3, hint3_rect)

    def draw_leaderboard(self):
        """Draw the leaderboard overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(230)
        overlay.fill(WHITE)
        self.screen.blit(overlay, (0, 0))

        font_title = pygame.font.Font(None, 64)
        font_header = pygame.font.Font(None, 32)
        font_entry = pygame.font.Font(None, 28)
        font_small = pygame.font.Font(None, 24)

        # Title
        title_text = font_title.render("LEADERBOARD", True, BLACK)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, 50))
        self.screen.blit(title_text, title_rect)

        # Headers
        y_pos = 120
        header_text = font_header.render("Rank  Name                Score    Level    Date", True, BLACK)
        self.screen.blit(header_text, (50, y_pos))

        # Draw line under header
        pygame.draw.line(self.screen, BLACK, (50, y_pos + 35), (SCREEN_WIDTH - 50, y_pos + 35), 2)

        # Entries - show only top 6
        y_pos = 170
        scores = self.leaderboard.get_top_scores(6)

        for i, entry in enumerate(scores):
            rank = f"{i + 1}."
            name = entry['name'][:18]  # Truncate long names
            score = f"{entry['score']}"
            level = f"{entry['level']}"
            date = entry['date'].split()[0]  # Just the date, not time

            entry_text = f"{rank:<5} {name:<20} {score:<8} {level:<8} {date}"

            # Highlight current player's score
            color = RED if entry['name'] == self.player_name and entry['score'] == self.total_score else BLACK
            text = font_entry.render(entry_text, True, color)
            self.screen.blit(text, (50, y_pos))
            y_pos += 35

        # Instructions
        instruction = font_small.render("Press R to Restart  |  Press L to close", True, BLACK)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT - 40))
        self.screen.blit(instruction, instruction_rect)

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
    # Check for debug flag
    debug_mode = '--debug' in sys.argv
    game = Game(debug_mode=debug_mode)
    game.run()
