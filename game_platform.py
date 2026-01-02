import pygame
import random
from constants import SCREEN_WIDTH, RED, BLUE, WHITE


class Platform:
    def __init__(self, y, speed, platform_index, all_platform_ys, gap_id=0):
        self.y = y
        self.original_y = y
        self.height = 3  # Thinner platforms like the original
        self.speed = speed
        self.width = SCREEN_WIDTH
        self.original_platform_index = platform_index
        self.all_platform_ys = all_platform_ys
        self.gap_id = gap_id  # Unique ID for this gap to track its movement

        self.gap_start = random.randint(50, SCREEN_WIDTH - 100)
        self.gap_width = random.randint(60, 90)
        self.x_offset = 0

        self.gap_current_platform_index = platform_index
        self.direction = random.choice([-1, 1])
        self.vertical_direction = random.choice([-1, 1])
        self.has_reached_edge = False  # Track if gap has reached one edge

    def update(self):
        self.y = self.original_y  # Always keep platform at original position
        self.x_offset += self.direction * self.speed

        # Snake pattern: gap goes completely off screen, then appears on next platform from same edge
        # Going right - when gap END goes off right edge (gap_start + x_offset + gap_width >= width)
        if self.direction == 1 and (self.gap_start + self.x_offset + self.gap_width) >= self.width:
            # Gap completely off right edge - move to next platform
            self.move_gap_to_next_platform()
            # Reset to start from right edge going left
            # Position so the gap END is at the right edge
            self.x_offset = self.width - self.gap_start - self.gap_width
            self.direction = -1  # Now go left
        # Going left - when gap START goes off left edge (gap_start + x_offset <= 0)
        elif self.direction == -1 and (self.gap_start + self.x_offset) <= 0:
            # Gap completely off left edge - move to next platform
            self.move_gap_to_next_platform()
            # Reset to start from left edge going right
            # Position so gap start is at the left edge
            self.x_offset = -self.gap_start
            self.direction = 1  # Now go right

    def move_gap_to_next_platform(self):
        self.gap_current_platform_index += self.vertical_direction

        if self.gap_current_platform_index < 0:
            self.gap_current_platform_index = 0
            self.vertical_direction = 1
        elif self.gap_current_platform_index >= len(self.all_platform_ys):
            self.gap_current_platform_index = len(self.all_platform_ys) - 1
            self.vertical_direction = -1

    def is_in_gap(self, x_position):
        gap_actual_start = self.gap_start + self.x_offset
        gap_actual_end = gap_actual_start + self.gap_width

        while gap_actual_start < 0:
            gap_actual_start += self.width
            gap_actual_end += self.width

        gap_actual_start = gap_actual_start % self.width
        gap_actual_end = gap_actual_end % self.width

        if gap_actual_end < gap_actual_start:
            return x_position >= gap_actual_start or x_position <= gap_actual_end
        else:
            return gap_actual_start <= x_position <= gap_actual_end

    def check_collision(self, player):
        if not (player.y + player.height >= self.y and player.y <= self.y + self.height):
            return False

        if self.gap_current_platform_index == self.original_platform_index:
            player_center = player.x + player.width / 2
            return not self.is_in_gap(player_center)
        else:
            return True

    def draw(self, screen, all_platforms, debug_mode=False):
        # Find ALL gaps that should be displayed on this platform's level
        active_gaps = []
        for platform in all_platforms:
            if platform.gap_current_platform_index == self.original_platform_index:
                active_gaps.append(platform)

        if active_gaps:
            # Create a list to track all gap regions (to draw platform around them)
            gap_regions = []

            for active_gap in active_gaps:
                gap_actual_start = active_gap.gap_start + active_gap.x_offset
                gap_actual_end = gap_actual_start + active_gap.gap_width

                while gap_actual_start < 0:
                    gap_actual_start += self.width
                    gap_actual_end += self.width

                gap_actual_start = gap_actual_start % self.width
                gap_actual_end = gap_actual_end % self.width

                gap_regions.append((gap_actual_start, gap_actual_end, active_gap))

            # Draw solid platform first
            pygame.draw.rect(screen, RED, (0, self.y, self.width, self.height))

            # Then "cut out" gaps by drawing black rectangles over them
            for gap_start, gap_end, active_gap in gap_regions:
                if gap_end < gap_start:
                    # Gap wraps around screen edge - cut out left and right sections
                    pygame.draw.rect(screen, WHITE, (gap_start, self.y, self.width - gap_start, self.height))
                    pygame.draw.rect(screen, WHITE, (0, self.y, gap_end, self.height))
                else:
                    # Gap doesn't wrap - cut out middle section
                    pygame.draw.rect(screen, WHITE, (gap_start, self.y, gap_end - gap_start, self.height))

                # Draw gap ID only in debug mode (to track gap movement)
                if debug_mode:
                    font = pygame.font.Font(None, 24)
                    gap_text = font.render(str(active_gap.gap_id), True, BLUE)
                    # Position the number in the middle of the gap
                    gap_center = (gap_start + active_gap.gap_width / 2) % self.width
                    screen.blit(gap_text, (gap_center - 6, self.y - 2))
        else:
            # No gap on this platform level - draw solid platform
            pygame.draw.rect(screen, RED, (0, self.y, self.width, self.height))
