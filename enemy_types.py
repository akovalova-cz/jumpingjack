import pygame
from constants import SCREEN_WIDTH, PURPLE, YELLOW, GREEN, BLACK, BLUE, RED, GRAY


class BaseEnemy:
    """Base class for all enemy types"""
    def __init__(self, platform_positions, speed, start_platform_index=None, color_variant=0):
        self.speed = speed
        self.platform_positions = platform_positions
        self.color_variant = color_variant

        # Set size and color in subclass
        self.width = 30
        self.height = 25
        self.color = PURPLE

        # Position setup
        if start_platform_index is None:
            import random
            self.current_platform_index = random.randint(0, len(platform_positions) - 1)
        else:
            self.current_platform_index = start_platform_index

        import random
        self.direction = random.choice([-1, 1])
        self.vertical_direction = random.choice([-1, 1])
        self.has_reached_edge = False
        self.animation_frame = 0

        if self.direction == 1:
            self.x = 0
        else:
            self.x = SCREEN_WIDTH - self.width

        self.y = platform_positions[self.current_platform_index] - self.height

    def update(self):
        self.x += self.direction * self.speed * 0.8
        self.animation_frame += 1

        # Snake pattern: enemy goes completely off screen
        if self.direction == 1 and self.x >= SCREEN_WIDTH + self.width:
            self.move_to_next_platform()
            self.x = SCREEN_WIDTH + self.width - 1
            self.direction = -1
        elif self.direction == -1 and self.x <= -(self.width * 2):
            self.move_to_next_platform()
            self.x = -(self.width * 2 - 1)
            self.direction = 1

    def move_to_next_platform(self):
        self.current_platform_index += self.vertical_direction

        if self.current_platform_index < 0:
            self.current_platform_index = 0
            self.vertical_direction = 1
        elif self.current_platform_index >= len(self.platform_positions):
            self.current_platform_index = len(self.platform_positions) - 1
            self.vertical_direction = -1

        self.y = self.platform_positions[self.current_platform_index] - self.height

    def check_collision(self, player):
        if (player.x < self.x + self.width and
            player.x + player.width > self.x and
            player.y < self.y + self.height and
            player.y + player.height > self.y):
            return True
        return False

    def draw(self, screen):
        """Override in subclass"""
        pass


class Snake(BaseEnemy):
    def __init__(self, platform_positions, speed, start_platform_index=None, color_variant=0):
        super().__init__(platform_positions, speed, start_platform_index, color_variant)
        self.width = 35
        self.height = 20
        # More color variety
        colors = [GREEN, YELLOW, BLUE, (255, 140, 0), (0, 255, 127), (173, 216, 230)]  # Orange, Spring Green, Light Blue
        self.color = colors[color_variant % len(colors)]

    def draw(self, screen):
        cx = int(self.x + self.width / 2)
        cy = int(self.y + self.height / 2)

        # Snake body segments
        num_segments = 5
        for i in range(num_segments):
            offset_x = int(self.x + i * (self.width / num_segments))
            wave_y = int(cy + 4 * pygame.math.Vector2(1, 0).rotate((self.animation_frame + i * 30) % 360).y)
            pygame.draw.circle(screen, self.color, (offset_x + 4, wave_y), 5)

        # Snake head
        head_x = int(self.x + self.width - 6) if self.direction == 1 else int(self.x + 6)
        pygame.draw.circle(screen, self.color, (head_x, cy), 6)
        # Eye
        eye_x = head_x + (2 if self.direction == 1 else -2)
        pygame.draw.circle(screen, BLACK, (eye_x, cy - 2), 2)


class Plane(BaseEnemy):
    def __init__(self, platform_positions, speed, start_platform_index=None, color_variant=0):
        super().__init__(platform_positions, speed, start_platform_index, color_variant)
        self.width = 50
        self.height = 20
        colors = [RED, PURPLE, (255, 140, 0), (0, 191, 255), (255, 20, 147), (255, 215, 0)]  # Orange, Deep Sky Blue, Deep Pink, Gold
        self.color = colors[color_variant % len(colors)]

    def draw(self, screen):
        cx = int(self.x + self.width / 2)
        cy = int(self.y + self.height / 2)

        if self.direction == 1:  # Moving right
            nose_x = int(self.x + self.width - 5)
            pygame.draw.polygon(screen, self.color, [
                (nose_x, cy), (nose_x - 8, cy - 4), (nose_x - 8, cy + 4)])
            pygame.draw.rect(screen, self.color, (self.x + 8, cy - 3, self.width - 18, 6))
            tail_x = int(self.x + 5)
            pygame.draw.polygon(screen, self.color, [
                (tail_x, cy), (tail_x + 5, cy - 5), (tail_x + 8, cy)])
            pygame.draw.rect(screen, self.color, (self.x + 15, cy + 3, 15, 2))
            pygame.draw.circle(screen, BLACK, (nose_x - 10, cy - 1), 2)
        else:  # Moving left
            nose_x = int(self.x + 5)
            pygame.draw.polygon(screen, self.color, [
                (nose_x, cy), (nose_x + 8, cy - 4), (nose_x + 8, cy + 4)])
            pygame.draw.rect(screen, self.color, (self.x + 10, cy - 3, self.width - 18, 6))
            tail_x = int(self.x + self.width - 5)
            pygame.draw.polygon(screen, self.color, [
                (tail_x, cy), (tail_x - 5, cy - 5), (tail_x - 8, cy)])
            pygame.draw.rect(screen, self.color, (self.x + 10, cy + 3, 15, 2))
            pygame.draw.circle(screen, BLACK, (nose_x + 10, cy - 1), 2)


class Axel(BaseEnemy):
    def __init__(self, platform_positions, speed, start_platform_index=None, color_variant=0):
        super().__init__(platform_positions, speed, start_platform_index, color_variant)
        self.width = 25
        self.height = 25
        colors = [(255, 215, 0), GREEN, (255, 140, 0), (255, 20, 147), (0, 255, 255), RED]  # Gold (first), then others
        self.color = colors[color_variant % len(colors)]

    def draw(self, screen):
        cx = int(self.x + self.width / 2)
        cy = int(self.y + self.height / 2)

        pygame.draw.circle(screen, self.color, (cx, cy), int(self.width / 2))

        num_spokes = 4
        for i in range(num_spokes):
            angle = (self.animation_frame * 5 + i * (360 / num_spokes)) % 360
            end_x = int(cx + (self.width / 2 - 2) * pygame.math.Vector2(1, 0).rotate(angle).x)
            end_y = int(cy + (self.width / 2 - 2) * pygame.math.Vector2(1, 0).rotate(angle).y)
            pygame.draw.line(screen, BLACK, (cx, cy), (end_x, end_y), 2)

        pygame.draw.circle(screen, BLACK, (cx, cy), 4)


class Octopus(BaseEnemy):
    def __init__(self, platform_positions, speed, start_platform_index=None, color_variant=0):
        super().__init__(platform_positions, speed, start_platform_index, color_variant)
        self.width = 30
        self.height = 25
        colors = [(255, 20, 147), GREEN, RED, (255, 140, 0), (0, 191, 255), PURPLE]  # Deep Pink (first), then others
        self.color = colors[color_variant % len(colors)]

    def draw(self, screen):
        cx = int(self.x + self.width / 2)
        head_y = int(self.y + 8)

        pygame.draw.ellipse(screen, self.color, (self.x + 5, self.y, self.width - 10, 16))

        eye_left = int(self.x + self.width * 0.35)
        eye_right = int(self.x + self.width * 0.65)
        pygame.draw.circle(screen, BLACK, (eye_left, head_y), 3)
        pygame.draw.circle(screen, BLACK, (eye_right, head_y), 3)

        num_tentacles = 4
        for i in range(num_tentacles):
            # Distribute tentacles closer to the body center
            tentacle_x = int(self.x + self.width * 0.3 + i * (self.width * 0.4 / (num_tentacles - 1)))
            wave_offset = int(3 * pygame.math.Vector2(1, 0).rotate((self.animation_frame * 3 + i * 45) % 360).y)
            pygame.draw.line(screen, self.color,
                           (tentacle_x, self.y + 16),
                           (tentacle_x + wave_offset, self.y + self.height), 2)


class Ghost(BaseEnemy):
    def __init__(self, platform_positions, speed, start_platform_index=None, color_variant=0):
        super().__init__(platform_positions, speed, start_platform_index, color_variant)
        self.width = 28
        self.height = 28
        colors = [(0, 255, 255), (255, 140, 0), (255, 105, 180), (173, 216, 230), GREEN, BLACK]  # Cyan (first), then others including black
        self.color = colors[color_variant % len(colors)]

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, (self.x + 3, self.y, self.width - 6, self.height - 8))

        num_waves = 3
        for i in range(num_waves):
            wave_x = int(self.x + 5 + i * (self.width - 10) / num_waves)
            wave_y = int(self.y + self.height - 6 + 3 * pygame.math.Vector2(1, 0).rotate((self.animation_frame * 4 + i * 120) % 360).y)
            pygame.draw.circle(screen, self.color, (wave_x, wave_y), 4)

        eye_left = int(self.x + self.width * 0.35)
        eye_right = int(self.x + self.width * 0.65)
        pygame.draw.circle(screen, BLACK, (eye_left, int(self.y + 10)), 3)
        pygame.draw.circle(screen, BLACK, (eye_right, int(self.y + 10)), 3)


class Car(BaseEnemy):
    def __init__(self, platform_positions, speed, start_platform_index=None, color_variant=0):
        super().__init__(platform_positions, speed, start_platform_index, color_variant)
        self.width = 45
        self.height = 18
        colors = [YELLOW, (0, 191, 255), (255, 140, 0), (0, 255, 127), (255, 20, 147), RED]  # Yellow (first), then others
        self.color = colors[color_variant % len(colors)]

    def draw(self, screen):
        cx = int(self.x + self.width / 2)
        cy = int(self.y + self.height / 2)

        pygame.draw.rect(screen, self.color, (self.x + 5, cy - 5, self.width - 10, 10))
        pygame.draw.rect(screen, self.color, (self.x + 12, cy - 10, self.width - 24, 5))

        window_x = int(self.x + 15)
        pygame.draw.rect(screen, BLACK, (window_x, cy - 9, 8, 4))
        pygame.draw.rect(screen, BLACK, (window_x + 12, cy - 9, 8, 4))

        wheel_y = int(self.y + self.height - 3)
        pygame.draw.circle(screen, BLACK, (int(self.x + 12), wheel_y), 3)
        pygame.draw.circle(screen, BLACK, (int(self.x + self.width - 12), wheel_y), 3)


class Train(BaseEnemy):
    def __init__(self, platform_positions, speed, start_platform_index=None, color_variant=0):
        super().__init__(platform_positions, speed, start_platform_index, color_variant)
        self.width = 55
        self.height = 22
        colors = [(138, 43, 226), GREEN, (255, 140, 0), (0, 191, 255), (255, 215, 0), RED]  # Blue Violet (first), then others
        self.color = colors[color_variant % len(colors)]

    def draw(self, screen):
        cx = int(self.x + self.width / 2)
        cy = int(self.y + self.height / 2)

        # Main body
        pygame.draw.rect(screen, self.color, (self.x + 10, cy - 6, self.width - 20, 12))

        # Cabin and smokestack should be at the BACK (opposite of movement direction)
        if self.direction == 1:  # Moving right - cabin at left (back)
            # Cabin at back (left)
            pygame.draw.rect(screen, self.color, (self.x + 5, cy - 10, 10, 10))
            # Smokestack at back
            pygame.draw.rect(screen, self.color, (self.x + 16, cy - 14, 4, 8))
            # Window on cabin
            pygame.draw.circle(screen, BLACK, (int(self.x + 10), cy - 5), 2)
        else:  # Moving left - cabin at right (back)
            # Cabin at back (right)
            pygame.draw.rect(screen, self.color, (self.x + self.width - 15, cy - 10, 10, 10))
            # Smokestack at back
            pygame.draw.rect(screen, self.color, (self.x + self.width - 20, cy - 14, 4, 8))
            # Window on cabin
            pygame.draw.circle(screen, BLACK, (int(self.x + self.width - 10), cy - 5), 2)

        # Wheels (4 wheels)
        wheel_y = int(self.y + self.height - 3)
        for i in range(4):
            wheel_x = int(self.x + 12 + i * 10)
            pygame.draw.circle(screen, BLACK, (wheel_x, wheel_y), 3)


class Hunter(BaseEnemy):
    def __init__(self, platform_positions, speed, start_platform_index=None, color_variant=0):
        super().__init__(platform_positions, speed, start_platform_index, color_variant)
        self.width = 22
        self.height = 30
        colors = [(255, 140, 0), GREEN, (138, 43, 226), (0, 191, 255), (255, 20, 147), RED]  # Orange (first), then others
        self.color = colors[color_variant % len(colors)]

    def draw(self, screen):
        cx = int(self.x + self.width / 2)

        head_y = int(self.y + 5)
        pygame.draw.circle(screen, self.color, (cx, head_y), 4)

        body_top = head_y + 4
        body_bottom = int(self.y + self.height * 0.6)
        pygame.draw.line(screen, self.color, (cx, body_top), (cx, body_bottom), 2)

        arm_y = int(self.y + 12)
        if self.direction == 1:
            pygame.draw.line(screen, self.color, (cx, arm_y), (cx - 6, arm_y + 4), 2)
            pygame.draw.line(screen, self.color, (cx, arm_y), (cx + 8, arm_y), 2)
            pygame.draw.rect(screen, BLACK, (cx + 8, arm_y - 2, 8, 3))
        else:
            pygame.draw.line(screen, self.color, (cx, arm_y), (cx - 8, arm_y), 2)
            pygame.draw.line(screen, self.color, (cx, arm_y), (cx + 6, arm_y + 4), 2)
            pygame.draw.rect(screen, BLACK, (cx - 16, arm_y - 2, 8, 3))

        legs_y = body_bottom
        if (self.animation_frame // 4) % 2 == 0:
            pygame.draw.line(screen, self.color, (cx, legs_y), (cx - 4, int(self.y + self.height)), 2)
            pygame.draw.line(screen, self.color, (cx, legs_y), (cx + 3, int(self.y + self.height)), 2)
        else:
            pygame.draw.line(screen, self.color, (cx, legs_y), (cx + 4, int(self.y + self.height)), 2)
            pygame.draw.line(screen, self.color, (cx, legs_y), (cx - 3, int(self.y + self.height)), 2)


class Dinosaur(BaseEnemy):
    def __init__(self, platform_positions, speed, start_platform_index=None, color_variant=0):
        super().__init__(platform_positions, speed, start_platform_index, color_variant)
        self.width = 40
        self.height = 28
        colors = [(0, 191, 255), PURPLE, (255, 140, 0), (205, 92, 92), (255, 215, 0), GREEN]  # Deep Sky Blue (first), then others
        self.color = colors[color_variant % len(colors)]

    def draw(self, screen):
        cx = int(self.x + self.width / 2)
        cy = int(self.y + self.height / 2)

        # Body - larger and positioned lower for T-Rex stance
        pygame.draw.ellipse(screen, self.color, (self.x + 8, cy - 4, self.width - 16, 18))

        # Head - bigger and positioned at same level as body (not above)
        if self.direction == 1:
            head_x = int(self.x + self.width - 6)
        else:
            head_x = int(self.x + 6)

        # Bigger head for T-Rex
        pygame.draw.ellipse(screen, self.color, (head_x - 8, cy - 8, 16, 14))

        # Eye positioned higher
        pygame.draw.circle(screen, BLACK, (head_x, cy - 6), 2)

        # Jaw/mouth for T-Rex
        if self.direction == 1:
            pygame.draw.line(screen, BLACK, (head_x + 4, cy - 2), (head_x + 6, cy), 2)
        else:
            pygame.draw.line(screen, BLACK, (head_x - 4, cy - 2), (head_x - 6, cy), 2)

        # Tail - longer and more substantial
        if self.direction == 1:
            tail_x = int(self.x + 5)
            pygame.draw.polygon(screen, self.color, [
                (tail_x + 8, cy), (tail_x, cy - 6), (tail_x, cy + 6)])
        else:
            tail_x = int(self.x + self.width - 5)
            pygame.draw.polygon(screen, self.color, [
                (tail_x - 8, cy), (tail_x, cy - 6), (tail_x, cy + 6)])

        # Legs - thicker for T-Rex
        leg_y = int(self.y + self.height)
        if (self.animation_frame // 4) % 2 == 0:
            pygame.draw.line(screen, self.color, (cx - 4, cy + 6), (cx - 4, leg_y), 3)
            pygame.draw.line(screen, self.color, (cx + 4, cy + 6), (cx + 4, leg_y), 3)
        else:
            pygame.draw.line(screen, self.color, (cx - 2, cy + 6), (cx - 4, leg_y), 3)
            pygame.draw.line(screen, self.color, (cx + 2, cy + 6), (cx + 4, leg_y), 3)


# Factory function to create enemies
def create_enemy(enemy_type, platform_positions, speed, start_platform_index=None, color_variant=0):
    """Factory function to create the appropriate enemy subclass"""
    enemy_classes = {
        'snake': Snake,
        'plane': Plane,
        'axel': Axel,
        'octopus': Octopus,
        'ghost': Ghost,
        'car': Car,
        'train': Train,
        'hunter': Hunter,
        'dinosaur': Dinosaur
    }

    enemy_class = enemy_classes.get(enemy_type, Snake)
    return enemy_class(platform_positions, speed, start_platform_index, color_variant)
