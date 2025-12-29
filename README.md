# Jumping Jack

A Python remake of the classic ZX Spectrum game Jumping Jack!

## Description

Navigate Jack through multiple levels of scrolling platforms with gaps while avoiding colorful enemies. Jump through gaps, reach the top to complete levels, and survive as long as possible!

This is a fully-featured 2D platformer built with Python and Pygame, demonstrating object-oriented game design, physics simulation, collision detection, and progressive difficulty scaling.

## Installation

1. Make sure you have Python 3.7+ installed
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Play

Run the game:

```bash
python jumping_jack.py
```

### First Time Setup

When you first run the game, you'll be prompted to enter your name. This name will be used for the leaderboard.

- Type your name and press **ENTER** to start
- Press **ESC** to use the last player's name
- Press **BACKSPACE** to delete characters
- If you leave it blank and press ENTER, your name will be "Anonymous"

Your name will be remembered and shown by default the next time you play.

### Debug Mode

Run the game with debug mode to display gap numbers on platforms:

```bash
python jumping_jack.py --debug
```

In debug mode, each gap will show its origin platform number (0-4) in blue text in the middle of the gap. This is useful for understanding and debugging the gap movement system.

## Controls

### In-Game Controls
- **LEFT ARROW** or **A** - Move left
- **RIGHT ARROW** or **D** - Move right
- **UP ARROW** or **SPACEBAR** - Jump (or continue to next level)

### Game Over Controls
- **R** - Restart the game (enter name again)
- **L** - Toggle leaderboard display

## Gameplay Rules

### Movement
- Jack can move left and right across the screen
- When you move off one edge of the screen, you wrap around to the other edge
- Jump to navigate between platforms

### Platforms
- 5 elevated platforms (no ground platform - player stands on empty ground)
- Platform positions: [510, 430, 350, 270, 190] - evenly spaced 80 pixels apart
- Each gap follows a snake/zigzag pattern:
  - Travels completely across one platform line until fully off-screen
  - Appears on the next platform from the same edge, moving in opposite direction
  - Example: left-to-right on platform 0 → right-to-left on platform 1 → left-to-right on platform 2
  - Initial direction and starting platform are random
- Gaps bounce between top and bottom platforms
- **CRITICAL: You can ONLY jump through gaps** - hitting a solid platform from below immediately stops your jump
- Jumping through solid platform lines is NOT possible - the player will be blocked
- **Jump height is limited to exactly one platform level (80 pixels)** - you cannot jump through multiple platforms in a single jump, even if gaps are aligned
- You can land on solid parts of platforms

### Enemies
- **9 different enemy types** that unlock as you progress through levels
- Each type has unique visual appearance and animations
- **Smart color system**:
  - Each enemy type has 6 possible colors
  - When an enemy spawns, it randomly picks a color that's NOT already on screen
  - This ensures maximum visual variety - you'll rarely see two enemies with the same color!
- Enemies follow the same snake/zigzag pattern as gaps:
  - Travel completely across one platform line until fully off-screen
  - Appear on the next platform from the same edge, moving in opposite direction
  - Example: left-to-right on platform 0 → right-to-left on platform 1 → left-to-right on platform 2
- Enemies bounce between the top and bottom platforms
- **Enemy variety system**: When spawning enemies, the game prefers enemy types that haven't appeared yet. Once all types have spawned, the cycle resets and repeats.
- Touching an enemy costs a life

#### Enemy Types by Level
- **Level 1**: Snake, Plane, Axel, Octopus
- **Level 2**: + Ghost (floating with wavy bottom)
- **Level 3**: + Car (side view with wheels)
- **Level 4**: + Train (locomotive with smokestack)
- **Level 5**: + Hunter (stick figure with gun)
- **Level 6+**: + Dinosaur (T-Rex style)

#### Enemy Details
Each enemy type has 6 color variants. The first color listed is the default (appears first time), ensuring visual variety:

1. **Snake** (green/yellow/blue/orange/spring green/light blue) - Wavy animated body with segments
2. **Plane** (red/purple/orange/deep sky blue/deep pink/gold) - Side-view aircraft with wings and tail
3. **Axel** (gold/green/orange/deep pink/cyan/red) - Spinning wheel with rotating spokes
4. **Octopus** (deep pink/green/red/orange/deep sky blue/purple) - Alien with waving tentacles
5. **Ghost** (cyan/orange/hot pink/light blue/green/purple) - Floating specter with wavy bottom edge
6. **Car** (yellow/deep sky blue/orange/spring green/deep pink/red) - Automobile with windows and wheels
7. **Train** (blue violet/green/orange/deep sky blue/gold/red) - Locomotive with cabin and smokestack at the back, pulling forward
8. **Hunter** (orange/green/blue violet/deep sky blue/deep pink/red) - Stick figure carrying a gun
9. **Dinosaur** (deep sky blue/purple/orange/indian red/gold/green) - T-Rex with animated walking legs

### Sound Effects
- **Retro-style synthesized sounds** generated programmatically
- **Jump**: Rising pitch sweep (200-600 Hz) when you jump
- **Footsteps**: Low tone when walking on ground (with cooldown to avoid spam)
- **Landing**: Quick downward sweep when landing from a jump
- **Death**: Harsh downward sweep when hit by enemy
- **Level Complete**: Upward celebration sweep when reaching the top
- All sounds are generated using NumPy and Pygame's audio mixer

### Invincibility System
- **2 seconds of invincibility** at the start of each level to give you time to react
- **1 second of invincibility** after losing a life and respawning
- During invincibility, you cannot take damage from enemies
- This prevents instant death when enemies spawn near you or when respawning

### Level Progression
- Start at the bottom of the screen
- Reach the very top (ceiling) to complete the level
- **Level transition screen**: White background with black text showing "LEVEL #" in the center
- Press SPACE or wait 3 seconds to start the next level
- You start at the bottom again on each new level

### Scoring & Lives
- Earn 10 points per second of survival **while off the ground** (only when on platforms or jumping)
- Start with 5 lives
- Lives are displayed as small Jack sprites at the top of the screen
- **Lose a life only when touching an enemy**
- Game over when all lives are lost
- Your score is automatically saved to the leaderboard when the game ends

### Leaderboard
- Tracks the top 10 high scores
- Displays player name, score, level reached, and date
- Automatically shown when game ends
- Press **L** to toggle leaderboard view during game over
- Stored persistently in `leaderboard.json`
- Your current score is highlighted in red on the leaderboard

### Difficulty Progression
- Each level increases:
  - Platform scrolling speed
  - Initial enemy count (X)
  - Enemies spawned during level (Y)
- **Progressive enemy spawning**:
  - Level 1: 2 initial enemies, 1 spawns during play, speed 1.5
  - Level 2: 3 initial enemies, 2 spawn during play, speed 2.0
  - Level 3: 4 initial enemies, 3 spawn during play, speed 2.5
  - Level 4: 5 initial enemies, 4 spawn during play, speed 3.0
  - Level 5+: 6 initial enemies (max), 4 spawn during play (max)
- New enemies spawn every 10 seconds during gameplay
- Enemies spawn at random platforms with random starting positions
- Spawn system prevents overlapping enemies (minimum 100 pixels apart)

## Game Features

- Screen-wrapping movement for player
- Dynamic platform gaps with bidirectional scrolling
- Platform gaps that jump between levels like enemies
- Multi-platform enemy patrol system
- Progressive difficulty scaling
- Level-based progression system
- Score tracking across levels
- Lives system displayed as Jack sprites
- **Persistent leaderboard** - top 10 scores saved to file
- **Player name entry** - personalized gameplay experience
- Retro-style graphics inspired by the ZX Spectrum original
- **Retro-style sound effects** - synthesized jump, walk, landing, death, and victory sounds

## Tips

- Gaps and enemies follow a snake/zigzag pattern - they go completely across one line before moving to the next
- Time your jumps to align with platform gaps
- Use screen wrapping to quickly reposition
- Watch enemy patrol patterns carefully
- The game gets harder with each level - plan your route carefully!
- Jump height is calibrated for exactly one platform level - no double jumps!

Good luck and have fun!

---

## Technical Implementation

### Architecture

The game follows an object-oriented design with separate modules for each game entity:

- **constants.py** - Game constants (screen dimensions, colors, FPS)
- **player.py** - Player class with movement and physics
- **game_platform.py** - Platform class with dynamic gaps
- **enemy_types.py** - Enemy classes with unique behaviors and designs
- **sound_manager.py** - Sound effects generation and playback
- **leaderboard.py** - Score persistence and leaderboard management
- **jumping_jack.py** - Main game loop and Game class

### Core Game Loop

The game follows a standard game loop pattern at 60 FPS:

```python
while running:
    handle_events()  # Process keyboard input
    update()         # Update game state
    draw()           # Render to screen
    clock.tick(FPS)  # Maintain 60 FPS
```

### Player Physics ([player.py](player.py))

#### Movement System
- **Horizontal movement**: 5 pixels per frame in response to arrow keys or A/D keys
- **Screen wrapping**: When player x-position exceeds screen bounds, wraps to opposite edge
  ```python
  if self.x + self.width < 0:
      self.x = SCREEN_WIDTH
  ```

#### Jump Mechanics
- **Jump strength**: -11 pixels/frame (negative = upward)
- **Gravity**: 0.8 pixels/frame² constant acceleration
- **Physics update**: `velocity_y += gravity` then `y += velocity_y`
- **Jump constraint**: Can only jump when not already jumping (prevents mid-air jumps)
- **Jump height**: Calibrated for exactly one platform level (60 pixels)
  - Maximum jump height: ~76 pixels (calculated as `jump_strength² / (2 * gravity)`)
  - Platform spacing: 60 pixels
  - This allows jumping to the next platform but prevents double-platform jumps

#### Collision Detection

**Landing on platforms** ([player.py:94-125](player.py#L94-L125)):
```python
def can_land_on_platform(self, platform, all_platforms):
    # Find which gap (if any) is currently on this platform's level
    active_gap = None
    for p in all_platforms:
        if p.gap_current_platform_index == platform.original_platform_index:
            active_gap = p
            break

    # Check if player is falling and close to platform surface
    if distance_to_platform <= abs(self.velocity_y) + 5:
        # Check if player center is NOT in the active gap
        if active_gap and not in_gap:
            return True
```

**Head collision** ([player.py:62-92](player.py#L62-L92)):
- When jumping upward (velocity_y < 0), checks if player will hit platform from below
- Searches all platforms to find which gap is currently on the platform level being checked
- Stops upward movement if hitting solid platform (not in active gap)
- Allows jumping through active gaps only

**Key implementation detail**: All collision detection accounts for dynamic gap movement between platform levels, searching for the "active gap" on each platform level rather than checking each platform's own gap position. Jumping is only possible through gaps - hitting a solid platform from below stops the jump.

### Platform System ([game_platform.py](game_platform.py))

#### Dynamic Gap Movement

Each platform has a gap that scrolls independently. The update logic ensures gaps travel completely across one platform line before moving to the next:

```python
def update(self):
    self.y = self.original_y  # Keep platform bar fixed
    self.x_offset += self.direction * self.speed  # Scroll gap

    # Snake pattern: gap goes completely off screen, then appears on next platform from same edge
    # Going right - when gap END goes off right edge
    if self.direction == 1 and (self.gap_start + self.x_offset + self.gap_width) >= self.width:
        self.move_gap_to_next_platform()  # Move up or down
        self.x_offset = self.width - self.gap_start - self.gap_width  # Reset to right edge
        self.direction = -1  # Reverse to left

    # Going left - when gap START goes off left edge
    elif self.direction == -1 and (self.gap_start + self.x_offset) <= 0:
        self.move_gap_to_next_platform()  # Move up or down
        self.x_offset = -self.gap_start  # Reset to left edge
        self.direction = 1  # Reverse to right
```

**Key implementation details**:
- Platform bars stay fixed at their original Y positions: [340, 280, 220, 160, 100] - evenly spaced 60 pixels apart
- Player stands on ground at y=370 (no platform there - just empty ground)
- Gap position tracked separately via `gap_current_platform_index`
- **Snake pattern implementation** (critical for proper behavior):

  Each gap has these key properties:
  - `gap_start`: Initial random position (50 to width-100)
  - `gap_width`: Random width (60-90 pixels)
  - `x_offset`: Cumulative horizontal scroll offset (starts at 0)
  - `direction`: Current horizontal direction (1 = right, -1 = left)
  - `vertical_direction`: Platform switching direction (1 = down, -1 = up)
  - `gap_current_platform_index`: Which platform level (0-4) the gap is currently on

  The actual gap position is calculated as: `gap_start + x_offset`

  **Going right** (direction = 1):
  - Gap scrolls right by increasing `x_offset` by `speed` each frame
  - When gap END reaches right edge: `(gap_start + x_offset + gap_width) >= width`
  - Move to next platform (up or down based on `vertical_direction`)
  - Reset position: `x_offset = width - gap_start - gap_width` (gap END at right edge)
  - Reverse direction: `direction = -1` (now go left)
  - Direction check prevents double-triggering on same screen traversal

  **Going left** (direction = -1):
  - Gap scrolls left by decreasing `x_offset` by `speed` each frame
  - When gap START reaches left edge: `(gap_start + x_offset) <= 0`
  - Move to next platform (up or down based on `vertical_direction`)
  - Reset position: `x_offset = -gap_start` (gap START at left edge)
  - Reverse direction: `direction = 1` (now go right)
  - Direction check prevents double-triggering on same screen traversal

  **Platform bouncing**:
  - Gaps bounce between platform indices 0 (bottom) and 4 (top)
  - When reaching index -1, set to 0 and reverse `vertical_direction` to 1 (down)
  - When reaching index 5, set to 4 and reverse `vertical_direction` to -1 (up)

- x_offset remains continuous for smooth scrolling (never resets to 0)
- Each platform level always displays exactly one gap at any time
- Gap width: randomly 60-90 pixels per gap
- **Critical**: The edge detection checks the gap boundaries (start/end), not just `x_offset`, ensuring gaps go completely off-screen before switching platforms

#### Gap Rendering Logic ([game_platform.py:72-99](game_platform.py#L72-L99))

The draw method searches all platforms to find which gap should be displayed on this platform's level:

```python
def draw(self, screen, all_platforms):
    # Find which gap (if any) should be displayed on this platform's level
    active_gap = None
    for platform in all_platforms:
        if platform.gap_current_platform_index == self.original_platform_index:
            active_gap = platform
            break

    if active_gap:
        # Draw this platform with the active gap
        [draw gap logic using active_gap's x_offset and gap_start]
    else:
        # No gap on this platform level - draw solid platform
        pygame.draw.rect(screen, RED, (0, self.y, self.width, self.height))
```

This ensures that gaps remain visible at all times by drawing whichever gap is currently positioned on each platform level.

#### Wrap-Around Math ([game_platform.py:45-60](game_platform.py#L45-L60))

Gaps can wrap around screen edges. The `is_in_gap()` method handles this:

```python
gap_actual_start = (gap_start + x_offset) % width
gap_actual_end = gap_actual_start + gap_width

# If gap wraps around edge
if gap_actual_end > width:
    return (x >= gap_actual_start) or (x <= gap_actual_end - width)
```

### Enemy System ([enemy.py](enemy.py))

#### Multi-Platform Patrol (Snake Pattern)

Enemies follow a snake/zigzag pattern across platforms. Unlike gaps which use `gap_start + x_offset`, enemies use absolute `x` position:

```python
def update(self):
    self.x += self.direction * self.speed * 0.8

    # Snake pattern: enemy goes completely off screen, then appears on next platform from same edge
    # Going right - when enemy completely off right edge
    if self.direction == 1 and self.x >= SCREEN_WIDTH + self.width:
        self.move_to_next_platform()  # Move up or down
        self.x = SCREEN_WIDTH + self.width - 1  # Position just off right edge
        self.direction = -1  # Reverse to left

    # Going left - when enemy completely off left edge
    elif self.direction == -1 and self.x <= -(self.width * 2):
        self.move_to_next_platform()  # Move up or down
        self.x = -(self.width * 2 - 1)  # Position just off left edge
        self.direction = 1  # Reverse to right
```

**Enemy movement properties**:
- Each enemy has these key properties:
  - `x`: Absolute screen x-position
  - `y`: Calculated from `platform_positions[current_platform_index] - height`
  - `direction`: Horizontal direction (1 = right, -1 = left)
  - `vertical_direction`: Platform switching direction (1 = down, -1 = up)
  - `current_platform_index`: Which platform level (0-4) enemy is on
  - `speed`: Movement speed (multiplied by 0.8 for slightly slower than gap speed)

**Vertical movement**:
- When enemy goes completely off-screen, it moves to next platform in `vertical_direction`
- Appears from the same edge it disappeared from, moving in opposite direction
- Bounces between platform indices 0 (bottom) and 4 (top)
- Direction check (`direction == 1` or `direction == -1`) ensures platform change happens only once per screen traversal
- Enemy starts at random platform with random horizontal and vertical directions

#### Enemy Spawning System

**Initial Spawning**:
- Enemies spawn at random platforms with random positions
- Position can be anywhere from off-screen left to 1/4 across (moving right) OR 3/4 across to off-screen right (moving left)
- Spawn system checks for overlaps - enemies must be at least 100 pixels apart on the same platform
- Up to 10 attempts to find non-overlapping position before forcing spawn

**Progressive Spawning**:
- New enemies spawn every 10 seconds during gameplay
- Formula: Initial = min(1 + level, 6), Additional = min(level, 4)
- Level 1: 2 start + 1 added = 3 total max
- Level 2: 3 start + 2 added = 5 total max
- Level 5+: 6 start + 4 added = 10 total max

**Enemy Types**:
- **9 different enemy types** that unlock progressively (first color listed is default):
  1. **Snake** (green/yellow/blue/orange/spring green/light blue) - 35x20px, wavy animated body
  2. **Plane** (red/purple/orange/deep sky blue/deep pink/gold) - 50x20px, largest enemy with wings and tail
  3. **Axel** (gold/green/orange/deep pink/cyan/red) - 25x25px, spinning wheel with rotating spokes
  4. **Octopus** (deep pink/green/red/orange/deep sky blue/purple) - 30x25px, alien with waving tentacles
  5. **Ghost** (cyan/orange/hot pink/light blue/green/purple) - 28x28px, floating with wavy bottom (Level 2+)
  6. **Car** (yellow/deep sky blue/orange/spring green/deep pink/red) - 45x18px, automobile with wheels (Level 3+)
  7. **Train** (blue violet/green/orange/deep sky blue/gold/red) - 55x22px, locomotive with cabin at back (Level 4+)
  8. **Hunter** (orange/green/blue violet/deep sky blue/deep pink/red) - 22x30px, stick figure with gun (Level 5+)
  9. **Dinosaur** (deep sky blue/purple/orange/indian red/gold/green) - 40x28px, T-Rex with animated legs (Level 6+)
- Each type has unique size, color variants, visual appearance, and animations
- Train is the longest enemy (55x22 pixels), Plane is widest (50x20)
- All follow same snake/zigzag movement pattern
- **IMPORTANT**: Each enemy type has a unique default color to ensure maximum visual variety when multiple enemies appear simultaneously

**Color Variant System**:
- Each enemy type has 6 different color variants for maximum variety
- **Random color selection**: When an enemy spawns, it picks a RANDOM color from its 6 available colors
- **Smart color avoidance**: The game checks which colors are already visible on screen and avoids using them
- Only when all 6 colors of that enemy type are already on screen will it reuse a color
- Colors include: primary colors (red, green, blue), secondary colors (purple, yellow, orange), and special colors (cyan, hot pink, gold, light blue, etc.)
- This creates maximum visual variety - no two enemies will have the same color unless absolutely necessary
- Implementation:
  ```python
  # Get colors currently on screen
  colors_on_screen = self.get_colors_on_screen()

  # Find colors not currently on screen
  available_colors = [c for c in all_colors if c not in colors_on_screen]

  # If all colors are on screen, use any color
  if not available_colors:
      available_colors = all_colors

  # Pick a random color from available colors
  chosen_color = random.choice(available_colors)
  ```

**Enemy Variety System**:
- Game tracks which enemy types have been spawned in the current cycle
- When spawning a new enemy, prefers types that haven't appeared yet
- Once all 4 types have been used, resets the tracking and starts a new cycle
- This ensures visual variety and prevents the same enemy type from appearing repeatedly
- Implementation:
  ```python
  # Choose enemy type - prefer unused types before repeating
  available_types = [t for t in all_types if t not in used_types]
  if not available_types:
      used_types.clear()  # All types used - reset cycle
      available_types = all_types.copy()

  chosen_type = random.choice(available_types)
  used_types.add(chosen_type)
  ```

#### Collision Detection

Simple rectangle intersection (AABB collision):

```python
if (player.x < enemy.x + enemy.width and
    player.x + player.width > enemy.x and
    player.y < enemy.y + enemy.height and
    player.y + player.height > enemy.y):
    return True  # Collision detected
```

### Level Progression ([jumping_jack.py](jumping_jack.py))

#### Win Condition

Player must reach the ceiling (y <= 0) to complete level:

```python
if self.player.y <= 0:
    self.level += 1
    self.level_transition = True
```

#### Difficulty Scaling ([jumping_jack.py:36-48](jumping_jack.py#L36-L48))

Each level increases challenge:

```python
# Speed increases by 0.5 per level
self.base_speed = 1.5 + (self.level - 1) * 0.5

# Enemy count increases (capped at 8)
num_enemies = min(2 + self.level, 8)
```

| Level | Speed | Enemies |
|-------|-------|---------|
| 1     | 1.5   | 3       |
| 2     | 2.0   | 4       |
| 3     | 2.5   | 5       |
| 7+    | 4.5+  | 8 (max) |

### Scoring System ([jumping_jack.py:274-279](jumping_jack.py#L274-L279))

Frame-rate independent scoring using a timer. Score only increments when player is off the ground:

```python
# Only increment score when player is not on the ground
if self.player.y < 370 - 32:  # Ground level is 370, player height is 32
    self.score_timer += 1
    if self.score_timer >= FPS:  # Every 60 frames = 1 second
        self.total_score += 10
        self.score_timer = 0
```

Awards 10 points per second while on platforms or jumping (not while standing on ground).

### Lives and Respawning

Player starts with 5 lives. Life is lost only when touching an enemy.

Lives are displayed visually as small Jack sprites at the top of the screen next to the "Lives:" label.

On life loss, player respawns at (100, 338) with reset velocity, standing on the ground at y=370 (no platform there).

### Sound System ([sound_manager.py](sound_manager.py))

**Retro-style synthesized sound effects** using NumPy and Pygame's audio mixer:

```python
class SoundManager:
    def generate_sweep(self, freq_start, freq_end, duration, volume=0.3):
        """Generate frequency sweep using NumPy"""
        n_samples = int(duration * sample_rate)
        t = np.linspace(0, duration, n_samples, False)
        freq = np.linspace(freq_start, freq_end, n_samples)
        phase = np.cumsum(2 * np.pi * freq / sample_rate)
        wave = np.sin(phase) * volume
        envelope = np.exp(-3 * t / duration)  # Decay envelope
        wave = wave * envelope
        return pygame.sndarray.make_sound(stereo_wave)
```

**Sound Effects**:
- **Jump**: 200→600 Hz rising sweep (0.15s)
- **Walk**: 150 Hz tone (0.08s) with 8-frame cooldown
- **Land**: 400→150 Hz downward sweep (0.12s)
- **Death**: 600→100 Hz harsh sweep (0.3s)
- **Level Complete**: 300→800 Hz celebration sweep (0.5s)

All sounds use exponential decay envelopes for authentic retro feel.

### Leaderboard System ([leaderboard.py](leaderboard.py))

**Persistent high score tracking** using JSON file storage:

```python
class Leaderboard:
    def add_score(self, player_name, score, level):
        """Add a new score to the leaderboard"""
        entry = {
            'name': player_name,
            'score': score,
            'level': level,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        self.scores.append(entry)
        # Sort by score (descending), then by level (descending)
        self.scores.sort(key=lambda x: (x['score'], x['level']), reverse=True)
        # Keep only top 10
        self.scores = self.scores[:10]
```

**Features**:
- Stores top 10 scores in `leaderboard.json`
- Tracks player name, score, level reached, and timestamp
- Remembers last player name for quick re-entry
- Automatically saves scores when game ends
- Displays leaderboard with current player's score highlighted in red

**Name Entry System**:
- Shows name entry screen before game starts
- Pre-fills with last player's name as default
- Supports typing, backspace, and escape to load previous name
- 20 character limit for names
- Defaults to "Anonymous" if left blank

### Game States

The game manages multiple states:

1. **Name Entry**: Initial screen where player enters their name
2. **Playing**: Normal gameplay
3. **Level Transition**: Shows "LEVEL X" screen for 3 seconds
4. **Game Over**: Shows when lives <= 0, displays leaderboard
5. **Leaderboard View**: Overlay showing top 10 scores (toggleable with L key)

### Rendering ([jumping_jack.py:290-336](jumping_jack.py#L290-L336))

Draw order (back to front):
1. White background
2. Platforms (red rectangles with gaps)
3. Enemies (colored sprites with unique designs)
4. Player (Jack stick figure sprite)
5. UI elements:
   - Score text (top left)
   - Lives label and Jack sprite icons (below score)
   - Level text (top right)
6. Overlays (level transition, game over)

### Technical Challenges Solved

1. **Screen wrapping**: Modulo arithmetic for seamless edge transitions
2. **Gap wrap-around**: Special handling when gaps cross screen edges
3. **Platform-gap separation**: Keeping platforms fixed while gaps move between levels
4. **Gap visibility persistence**: Each platform searches all gaps to find which one to display on its level, ensuring gaps never disappear
5. **Smooth gap transitions**: Continuous x_offset prevents flickering when gaps change platform levels
6. **Dynamic collision detection**: Player collision checks search for "active gap" on each level rather than using platform's own gap
7. **Frame-rate independence**: Timer-based scoring instead of per-frame
8. **Collision precision**: Velocity-based landing detection to prevent falling through platforms
9. **Multi-directional movement**: Both horizontal (left/right) and vertical (platform switching) for enemies and gaps
10. **Balanced jump mechanics**: Jump strength calibrated to exactly one floor height (80 pixels) to prevent multi-floor jumping

### Critical Implementation Insights

#### Why Check Gap END for Right Edge?
When a gap moves right, we check `(gap_start + x_offset + gap_width) >= width` instead of just checking `gap_start + x_offset >= width`. This ensures the ENTIRE gap (not just its start) goes off the right edge before switching platforms. If we only checked the start position, the gap would disappear from the middle of the screen, breaking the snake pattern.

#### Why Different Reset Positions for Each Direction?
- **Going right**: Reset to `x_offset = width - gap_start - gap_width` positions the gap END at the right edge
- **Going left**: Reset to `x_offset = -gap_start` positions the gap START at the left edge
This ensures gaps appear from the edge they just disappeared from, maintaining visual continuity.

#### Why Direction Checks in Conditions?
Using `if self.direction == 1 and (gap condition)` prevents the condition from re-triggering immediately after switching. Without this:
1. Gap goes off right edge, switches platforms, reverses to direction=-1
2. On next frame, with direction=-1, the right-edge condition might still be true
3. Gap would switch platforms again immediately (double-trigger bug)

The direction check ensures each condition only fires when moving in the correct direction.

#### Why Enemies Use Absolute Position vs Gaps Use Offset?
- **Gaps**: Use `gap_start + x_offset` because gap_start is randomized (50 to width-100) and stays constant, while x_offset scrolls continuously
- **Enemies**: Use absolute `x` position because they start at edge (0 or width) and scroll across screen, simpler than offset-based positioning

This design choice makes gap collision detection consistent regardless of initial gap position, while keeping enemy logic straightforward.

### Code Statistics

- **Total files**: 7 Python modules
- **Total classes**: 13 (Game, Player, Platform, BaseEnemy + 9 enemy types, SoundManager, Leaderboard)
- **Lines of code**: ~900+
- **Dependencies**: pygame, numpy (for sound synthesis)
- **Platform spacing**: 60 pixels uniform vertical spacing
- **Jump calibration**: Jump strength -11, gravity 0.8, tuned for single-floor jumps
- **Data persistence**: leaderboard.json for high scores

### Future Enhancement Ideas

- Power-ups (invincibility, slow-motion)
- Different platform patterns per level
- ~~Sound effects~~ ✓ **DONE** - Retro-style synthesized sounds added!
- ~~High score persistence~~ ✓ **DONE** - Leaderboard with player names added!
- Background music
- Online leaderboard sync
- Multiple player characters
- Boss levels
- More detailed sprite animations
- Achievement system
