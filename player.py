import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK


class Player:
    def __init__(self, sound_manager=None):
        self.width = 20
        self.height = 32
        self.x = 100
        self.y = 370 - 32  # Standing on ground at y=370, player height is 32
        self.velocity_y = 0
        self.jumping = False
        self.gravity = 0.8
        self.jump_strength = -11  # Tuned to jump exactly one floor (60 pixels)
        self.move_speed = 5
        self.animation_frame = 0  # For running animation
        self.last_direction = 0  # Track movement direction: 0=still, -1=left, 1=right
        self.sound_manager = sound_manager
        self.was_jumping = False  # Track if we were jumping last frame (for landing sound)

    def jump(self):
        if not self.jumping:
            self.velocity_y = self.jump_strength
            self.jumping = True
            if self.sound_manager:
                self.sound_manager.play('jump')

    def move_left(self):
        self.x -= self.move_speed
        if self.x + self.width < 0:
            self.x = SCREEN_WIDTH
        self.last_direction = -1
        self.animation_frame += 1
        # Play footstep sound when moving on ground
        if not self.jumping and self.sound_manager:
            self.sound_manager.play_walk()

    def move_right(self):
        self.x += self.move_speed
        if self.x > SCREEN_WIDTH:
            self.x = -self.width
        self.last_direction = 1
        self.animation_frame += 1
        # Play footstep sound when moving on ground
        if not self.jumping and self.sound_manager:
            self.sound_manager.play_walk()

    def update(self, gap_objects, platform_positions):
        # Track if we were jumping at start of frame
        was_jumping_before = self.jumping

        self.velocity_y += self.gravity

        # Check head collision against all 5 physical platform levels
        if self.velocity_y < 0:
            for platform_index, platform_y in enumerate(platform_positions):
                if self.check_head_collision_at_level(platform_index, platform_y, gap_objects):
                    self.y = platform_y + 3  # platform height is 3
                    self.velocity_y = 0
                    if self.sound_manager:
                        self.sound_manager.play('land')
                    break

        self.y += self.velocity_y

        landed = False

        # Check landing on all 5 physical platform levels
        if self.velocity_y >= 0:
            for platform_index, platform_y in enumerate(platform_positions):
                if self.can_land_on_platform_at_level(platform_index, platform_y, gap_objects):
                    self.y = platform_y - self.height
                    self.velocity_y = 0
                    self.jumping = False
                    landed = True
                    break

        if not landed and self.y >= SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
            self.velocity_y = 0
            self.jumping = False
            landed = True

        # Play landing sound if we just landed
        if was_jumping_before and not self.jumping and self.sound_manager:
            self.sound_manager.play('land')

        return True

    def check_head_collision_at_level(self, platform_index, platform_y, gap_objects):
        """Check if player's head hits a solid part of a platform level"""
        platform_height = 3
        player_top = self.y
        player_next_top = player_top + self.velocity_y

        # Check if player is about to hit this platform from below
        if player_top >= platform_y + platform_height and player_next_top <= platform_y + platform_height:
            player_center = self.x + self.width / 2

            # Find ALL gaps currently on this platform level
            active_gaps = []
            for gap in gap_objects:
                if gap.gap_current_platform_index == platform_index:
                    active_gaps.append(gap)

            if active_gaps:
                # There are gap(s) on this level - check if player is in ANY of them
                in_any_gap = False
                for active_gap in active_gaps:
                    gap_actual_start = (active_gap.gap_start + active_gap.x_offset) % active_gap.width
                    gap_actual_end = gap_actual_start + active_gap.gap_width

                    if gap_actual_end > active_gap.width:
                        in_gap = (player_center >= gap_actual_start or
                                 player_center <= gap_actual_end - active_gap.width)
                    else:
                        in_gap = gap_actual_start <= player_center <= gap_actual_end

                    if in_gap:
                        in_any_gap = True
                        break

                # If in a gap, can pass through; if not in gap, collide with solid platform
                return not in_any_gap
            else:
                # No gap on this level - platform is solid, collision occurs
                return True

        return False

    def can_land_on_platform_at_level(self, platform_index, platform_y, gap_objects):
        """Check if player can land on a solid part of a platform level"""
        player_bottom = self.y + self.height

        distance_to_platform = abs(player_bottom - platform_y)

        if distance_to_platform <= abs(self.velocity_y) + 5:
            player_center = self.x + self.width / 2

            # Find ALL gaps currently on this platform level
            active_gaps = []
            for gap in gap_objects:
                if gap.gap_current_platform_index == platform_index:
                    active_gaps.append(gap)

            if active_gaps:
                # There are gap(s) on this level - check if player is in ANY of them
                in_any_gap = False
                for active_gap in active_gaps:
                    gap_actual_start = (active_gap.gap_start + active_gap.x_offset) % active_gap.width
                    gap_actual_end = gap_actual_start + active_gap.gap_width

                    if gap_actual_end > active_gap.width:
                        in_gap = (player_center >= gap_actual_start or
                                 player_center <= gap_actual_end - active_gap.width)
                    else:
                        in_gap = gap_actual_start <= player_center <= gap_actual_end

                    if in_gap:
                        in_any_gap = True
                        break

                # If in gap, fall through; if not in gap, can land
                return not in_any_gap
            else:
                # No gap on this level - platform is solid, can land
                return True

        return False

    def check_crushed(self, platforms):
        # Get unique Y positions of platforms we're touching
        touching_platform_y_positions = set()
        for platform in platforms:
            if platform.check_collision(self):
                touching_platform_y_positions.add(platform.y)

        # Crushed only if touching 2+ platforms at different Y positions
        if len(touching_platform_y_positions) >= 2:
            return True

        return False

    @staticmethod
    def draw_small_jack(screen, x, y):
        """Draw a small Jack sprite at the given position (for lives display)"""
        # Scale factor for smaller sprite (increased from 0.5 to 0.7 for better visibility)
        scale = 0.7
        cx = int(x)

        # Head
        head_y = int(y + 3 * scale)
        pygame.draw.circle(screen, BLACK, (cx, head_y), int(3 * scale))

        # Body
        body_top = head_y + int(3 * scale)
        body_bottom = int(y + 13 * scale)
        pygame.draw.line(screen, BLACK, (cx, body_top), (cx, body_bottom), 2)

        # Arms (standing position)
        arm_y = int(y + 7 * scale)
        pygame.draw.line(screen, BLACK, (cx, arm_y), (cx - int(3 * scale), arm_y + int(4 * scale)), 2)
        pygame.draw.line(screen, BLACK, (cx, arm_y), (cx + int(3 * scale), arm_y + int(4 * scale)), 2)

        # Legs (standing position)
        legs_y = body_bottom
        pygame.draw.line(screen, BLACK, (cx, legs_y), (cx - int(2 * scale), int(y + 16 * scale)), 2)
        pygame.draw.line(screen, BLACK, (cx, legs_y), (cx + int(2 * scale), int(y + 16 * scale)), 2)

    def draw(self, screen):
        # Draw Jumping Jack character similar to original ZX Spectrum
        cx = int(self.x + self.width / 2)  # Center x

        # Head (black circle)
        head_y = int(self.y + 6)
        pygame.draw.circle(screen, BLACK, (cx, head_y), 5)

        # Body (black vertical line)
        body_top = head_y + 5
        body_bottom = int(self.y + self.height * 0.65)
        pygame.draw.line(screen, BLACK, (cx, body_top), (cx, body_bottom), 2)

        # Arms - animate based on running
        arm_y = int(self.y + 14)
        if self.last_direction != 0:
            # Running - arms at angles
            if (self.animation_frame // 4) % 2 == 0:
                # Left arm forward, right arm back
                pygame.draw.line(screen, BLACK, (cx, arm_y), (cx - 8, arm_y + 6), 2)
                pygame.draw.line(screen, BLACK, (cx, arm_y), (cx + 6, arm_y - 4), 2)
            else:
                # Right arm forward, left arm back
                pygame.draw.line(screen, BLACK, (cx, arm_y), (cx + 8, arm_y + 6), 2)
                pygame.draw.line(screen, BLACK, (cx, arm_y), (cx - 6, arm_y - 4), 2)
        else:
            # Standing still - arms down
            pygame.draw.line(screen, BLACK, (cx, arm_y), (cx - 6, arm_y + 8), 2)
            pygame.draw.line(screen, BLACK, (cx, arm_y), (cx + 6, arm_y + 8), 2)

        # Legs - animate based on running
        legs_y = body_bottom
        if self.last_direction != 0:
            # Running - legs at different angles
            if (self.animation_frame // 4) % 2 == 0:
                pygame.draw.line(screen, BLACK, (cx, legs_y), (cx - 6, int(self.y + self.height)), 2)
                pygame.draw.line(screen, BLACK, (cx, legs_y), (cx + 4, int(self.y + self.height)), 2)
            else:
                pygame.draw.line(screen, BLACK, (cx, legs_y), (cx + 6, int(self.y + self.height)), 2)
                pygame.draw.line(screen, BLACK, (cx, legs_y), (cx - 4, int(self.y + self.height)), 2)
        else:
            # Standing still - legs straight down
            pygame.draw.line(screen, BLACK, (cx, legs_y), (cx - 4, int(self.y + self.height)), 2)
            pygame.draw.line(screen, BLACK, (cx, legs_y), (cx + 4, int(self.y + self.height)), 2)
