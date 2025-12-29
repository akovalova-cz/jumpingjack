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
        self.jump_strength = -14  # Tuned to jump exactly one floor (60 pixels)
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

    def update(self, platforms):
        # Track if we were jumping at start of frame
        was_jumping_before = self.jumping

        self.velocity_y += self.gravity

        if self.velocity_y < 0:
            for platform in platforms:
                if self.check_head_collision(platform, platforms):
                    self.y = platform.y + platform.height
                    self.velocity_y = 0
                    break

        self.y += self.velocity_y

        landed = False

        if self.velocity_y >= 0:
            for platform in platforms:
                if self.can_land_on_platform(platform, platforms):
                    self.y = platform.y - self.height
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

    def check_head_collision(self, platform, all_platforms):
        player_top = self.y
        player_next_top = player_top + self.velocity_y

        if player_top >= platform.y + platform.height and player_next_top <= platform.y + platform.height:
            player_center = self.x + self.width / 2

            # Find which gap (if any) is currently on this platform's level
            active_gap = None
            for p in all_platforms:
                if p.gap_current_platform_index == platform.original_platform_index:
                    active_gap = p
                    break

            if active_gap:
                # There's a gap on this level - check if player is in it
                gap_actual_start = (active_gap.gap_start + active_gap.x_offset) % active_gap.width
                gap_actual_end = gap_actual_start + active_gap.gap_width

                if gap_actual_end > active_gap.width:
                    in_gap = (player_center >= gap_actual_start or
                             player_center <= gap_actual_end - active_gap.width)
                else:
                    in_gap = gap_actual_start <= player_center <= gap_actual_end

                return not in_gap
            else:
                # No gap on this level - platform is solid
                return True

        return False

    def can_land_on_platform(self, platform, all_platforms):
        player_bottom = self.y + self.height

        distance_to_platform = abs(player_bottom - platform.y)

        if distance_to_platform <= abs(self.velocity_y) + 5:
            player_center = self.x + self.width / 2

            # Find which gap (if any) is currently on this platform's level
            active_gap = None
            for p in all_platforms:
                if p.gap_current_platform_index == platform.original_platform_index:
                    active_gap = p
                    break

            if active_gap:
                # There's a gap on this level - check if player is in it
                gap_actual_start = (active_gap.gap_start + active_gap.x_offset) % active_gap.width
                gap_actual_end = gap_actual_start + active_gap.gap_width

                if gap_actual_end > active_gap.width:
                    in_gap = (player_center >= gap_actual_start or
                             player_center <= gap_actual_end - active_gap.width)
                else:
                    in_gap = gap_actual_start <= player_center <= gap_actual_end

                return not in_gap
            else:
                # No gap on this level - can land (platform is solid)
                return True

        return False

    def check_crushed(self, platforms):
        touching_platforms = []
        for platform in platforms:
            if platform.check_collision(self):
                touching_platforms.append(platform)

        if len(touching_platforms) >= 2:
            return True

        return False

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
