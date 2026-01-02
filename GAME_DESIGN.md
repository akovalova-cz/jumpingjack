# Jumping Jack - Game Design Document

This document describes the complete requirements for building the Jumping Jack game in any programming language or framework. It focuses on game mechanics, visual design, and behavior without language-specific implementation details.

## Game Overview

Jumping Jack is a retro-style platformer inspired by the 1983 ZX Spectrum classic. The player controls Jack, a stick figure character who must navigate through moving platforms with deadly gaps while avoiding enemies to reach the top of the screen.

## Visual Design

### Screen Layout

- **Aspect ratio**: 4:3 or similar classic proportions
- **Background**: White
- **Color scheme**: Black (player), Red (platforms), multi-colored enemies, White (gaps)

### Platforms

- **Total platforms**: 5 elevated horizontal platforms
- **Platform appearance**: Thin red horizontal bars
- **Platform positioning**:
  - Evenly spaced vertically across the screen
  - Equal distance from ground to first platform
  - Equal distance between all platforms
  - Equal distance from top platform to ceiling
  - All platforms span the full width of the screen
- **Ground level**: Player starts on solid ground (no platform bar visible)

### Player Character (Jack)

Jack is rendered as a stick figure with the following elements:
- **Head**: Black filled circle
- **Body**: Black vertical line from head to hips
- **Arms**: Two black diagonal lines extending from shoulders
- **Legs**: Two black diagonal lines extending from hips to feet

**Animation states**:

1. **Standing still**:
   - Arms angled downward at sides
   - Legs straight down with slight spread

2. **Running** (left or right):
   - Arms alternate between forward and back positions
   - Legs alternate in running motion
   - Animation cycles every 4-8 frames
   - Direction affects arm/leg positions

3. **Lives display**:
   - Smaller scaled version of Jack sprite (approximately 70% scale)
   - Standing pose
   - Displayed in row at top of screen

### Enemies

**9 different enemy types**, each with unique visual appearance:

1. **Snake**
   - Wavy horizontal body with animated segments
   - Body curves with sine wave pattern
   - Animation creates slithering motion

2. **Plane**
   - Side-view aircraft
   - Fuselage (main body)
   - Wings extending from center
   - Tail fin at rear
   - Window details

3. **Axel**
   - Spinning wheel/gear shape
   - Central hub
   - 4-6 spokes radiating from center
   - Spokes rotate continuously

4. **Octopus**
   - Rounded head/body (ellipse)
   - Two eyes on head
   - 4 tentacles attached to bottom of body
   - Tentacles wave with sine wave animation

5. **Ghost**
   - Rounded top (semi-circle)
   - Wavy bottom edge (3 wave curves)
   - Floating appearance

6. **Car**
   - Rectangular body
   - Windows (smaller rectangles)
   - Two circular wheels at bottom
   - Wheels rotate

7. **Train**
   - Locomotive design
   - Cabin/body rectangle
   - Smokestack at rear
   - Wheels at bottom
   - Cabin appears to pull forward

8. **Hunter**
   - Stick figure similar to Jack
   - Head (circle)
   - Body (vertical line)
   - Arms holding gun
   - Gun rectangle extending horizontally
   - Gun should be visibly larger/prominent
   - Legs in walking animation

9. **Dinosaur (T-Rex style)**
   - Large head positioned horizontally
   - Jaw/mouth detail
   - Small eye
   - Large body (ellipse)
   - Long tail extending backward
   - Two thick legs at bottom
   - Legs alternate in walking motion

**Enemy color system**:
- Each enemy spawns with a **random color** from a palette of 6 possible colors
- **Smart color selection**: When spawning, avoid colors already visible on screen
- If all 6 colors are in use, allow color repetition
- Colors should be bright and distinct from each other
- Suggested palette per enemy type: include variations of red, green, blue, orange, purple, yellow, cyan, pink, etc.

**Enemy sizes**:
- Vary between types for visual interest
- Train should be longest enemy
- All enemies should fit on platform bars
- Heights should not exceed platform spacing

## Game Mechanics

### Player Controls

**Movement**:
- Move left: Left arrow or A key
- Move right: Right arrow or D key
- Jump: Spacebar or Up arrow

**Movement behavior**:
- Horizontal movement speed: Constant velocity
- Screen wrapping: When player exits one edge, appear at opposite edge
- Movement while jumping: Full air control

### Physics

**Jumping**:
- Jump strength: Negative vertical velocity (upward)
- Gravity: Constant downward acceleration applied each frame
- Jump height: Calibrated to reach exactly one platform level above
- No double jumping: Can only jump when on ground or platform
- **Critical**: Cannot jump through solid platforms - hitting platform from below stops jump

**Gravity**:
- Applied constantly to vertical velocity
- Creates natural arc for jumps
- Affects falling through gaps

**Collision with platforms**:
- Can land on solid portions of platforms
- Fall through gaps in platforms
- Cannot jump through solid platform from below
- Jump height limited to single platform spacing (cannot skip platforms)

### Platform Gap System

**Progressive difficulty**:
- Number of gaps increases with each level
- Formula: `gaps = 5 + current_level`
- Level 1: 6 gaps
- Level 2: 7 gaps
- Level 3: 8 gaps
- And so on...

**Gap initialization**:
- Each gap starts on a random platform level
- Random starting horizontal position within platform
- Random width within specified range
- Random horizontal direction (left or right)
- Random vertical direction (up or down through platforms)

**Gap movement (Snake pattern)**:
- Each gap scrolls horizontally across its current platform
- Speed increases with level
- When gap completely exits screen edge:
  - Move to next platform (up or down based on vertical direction)
  - Appear from same edge it exited
  - Reverse horizontal direction
  - Continue this snake/zigzag pattern
- When reaching top or bottom platform, reverse vertical direction
- **Multiple gaps can meet on same platform** if they move there from different directions

**Gap rendering**:
- Platform drawn as solid red bar
- Gap appears as white rectangle "cut out" of platform
- Multiple gaps on same platform render as multiple white sections
- Gaps wrap around screen edges seamlessly

### Enemy System

**Enemy spawning**:

Progressive spawning with level:
- Initial enemies at level start increases with level
- Additional enemies spawn during gameplay
- Formula:
  - Initial: `min(1 + level, 6)` enemies (max 6)
  - During level: `min(level, 4)` additional enemies (max 4)
- Level 1: 2 initial + 1 during play = 3 total
- Level 5+: 6 initial + 4 during play = 10 total
- New enemies spawn every 10 seconds during gameplay

**Enemy type unlocking**:
- Level 1: Snake, Plane, Axel, Octopus
- Level 2: + Ghost
- Level 3: + Car
- Level 4: + Train
- Level 5: + Hunter
- Level 6+: + Dinosaur

**Enemy movement**:
- Each enemy moves horizontally on its assigned platform
- Same snake pattern as gaps:
  - Scrolls across platform completely
  - When exiting screen edge, moves to adjacent platform
  - Appears from same edge, moving opposite direction
  - Bounces between top and bottom platforms
- Speed increases with level
- Animation frames update continuously (walking, flying, rolling, etc.)

**Enemy-player collision**:
- Collision detected when player and enemy sprites overlap
- Results in player losing one life
- Player respawns at starting position
- Brief invincibility period after respawn (1 second)
- Brief invincibility at level start (2 seconds)

**Spawn positioning**:
- Enemies spawn at random platform levels
- Start at screen edges (left or right)
- Random initial offset for variety
- Prevent overlapping: minimum distance between enemies
- Avoid spawning too close to player starting position

### Level Progression

**Level completion**:
- Player must reach the very top of screen (above all platforms)
- Triggers level transition

**Level transition**:
- Show "LEVEL X" screen
- White background, black text
- Pause for 3 seconds or until player presses jump
- Reset player to ground starting position
- Increase difficulty for next level

**Difficulty scaling**:
- Gap speed increases: `base_speed + (level - 1) * increment`
- Enemy speed increases: Same formula as gaps
- More gaps: Formula `5 + level`
- More enemies: As described in spawning section

### Scoring System

**Score mechanics**:
- Points earned only while player is off the ground
- No points while standing on ground level
- Award 10 points per second when:
  - Standing on platforms
  - In mid-air (jumping or falling)
- Score persists across levels
- Use frame-rate independent timing (track elapsed time)

### Lives System

**Lives**:
- Start with 5 lives
- Lose life when touching enemy
- **Do not** lose life from falling or getting crushed between platforms
- Display lives as row of small Jack sprites at top of screen
- Position: Below or next to "Lives:" label

**Respawn**:
- Return to starting position on ground
- Reset velocity to zero
- Brief invincibility period
- Lives counter updates

**Game Over**:
- Triggered when lives reach zero
- Display "GAME OVER" message
- Show leaderboard
- Options: Restart or view leaderboard

## Sound Effects

All sounds should be **retro-style synthesized** (not sampled):

**Sound types**:

1. **Jump**:
   - Rising pitch sweep
   - Frequency: 200 Hz → 600 Hz
   - Duration: 0.15 seconds
   - Trigger: When jump starts

2. **Footsteps**:
   - Low tone
   - Frequency: 150 Hz
   - Duration: 0.08 seconds
   - Trigger: While walking on ground
   - Cooldown: Don't play every frame (e.g., every 8 frames)

3. **Landing**:
   - Downward pitch sweep
   - Frequency: 400 Hz → 150 Hz
   - Duration: 0.12 seconds
   - Trigger: When landing on platform or ground

4. **Death**:
   - Harsh downward sweep
   - Frequency: 600 Hz → 100 Hz
   - Duration: 0.3 seconds
   - Trigger: When hit by enemy

5. **Level Complete**:
   - Upward celebration sweep
   - Frequency: 300 Hz → 800 Hz
   - Duration: 0.5 seconds
   - Trigger: When reaching top of screen

**Sound generation**:
- Use exponential decay envelope for authentic retro feel
- Generate waveforms programmatically (sine waves, square waves, etc.)
- Keep volume moderate (around 30% max volume)

## User Interface

### HUD (Always visible during gameplay)

**Top left**:
- Score: "Score: XXXXX" in black text
- Lives: "Lives:" label + row of small Jack sprites

**Top right**:
- Level: "Level: X" in black text

### Name Entry Screen (Pre-game)

**Display**:
- Title: "JUMPING JACK" (large, centered)
- Prompt: "Enter your name:"
- Input box with current text
- Blinking cursor
- Instructions:
  - "Press ENTER to start"
  - "Press ESC to use last player name"
  - "Press BACKSPACE to delete"

**Behavior**:
- Allow typing alphanumeric characters
- Limit: 20 characters
- Pre-fill with last player's name
- Default to "Anonymous" if blank
- Remember name for next session

### Level Transition Screen

**Display**:
- White background
- Large centered text: "LEVEL X"
- Smaller text: "Press SPACE to continue"

**Behavior**:
- Auto-continue after 3 seconds
- Or continue immediately on jump button press

### Game Over Screen

**Display**:
- Semi-transparent overlay over game
- Large text: "GAME OVER" (red)
- Options:
  - "Press R to Restart"
  - "Press L for Leaderboard"

**Behavior**:
- R key: Return to name entry
- L key: Toggle leaderboard view

### Leaderboard

**Display**:
- Semi-transparent white overlay
- Title: "LEADERBOARD"
- Table columns:
  - Rank (1-10)
  - Player Name
  - Score
  - Level Reached
  - Date
- Current player's score highlighted in red
- Instructions: "Press R to Restart | Press L to close"

**Data storage**:
- Persist top 10 scores to file
- File format: JSON or similar structured format
- Fields per entry:
  - name (string)
  - score (integer)
  - level (integer)
  - date (timestamp string)

**Sorting**:
- Primary: Score (descending)
- Secondary: Level (descending)
- Keep only top 10 entries

**File location**:
- Same directory as game executable
- Filename: `leaderboard.json` or similar

## Debug Mode

**Activation**:
- Command-line flag: `--debug` or similar
- Or debug toggle in settings

**Visual changes**:
- Display gap origin platform number inside each gap
- Number appears in blue text centered in gap
- Shows which platform each gap originally belonged to
- Helps understand gap movement system

## Technical Requirements

### Rendering

**Frame rate**:
- Target: 60 FPS
- Use frame-rate independent physics (delta time)
- Cap frame rate for consistency

**Draw order** (back to front):
1. Background (white)
2. Platforms (red bars with white gaps)
3. Enemies (colored sprites)
4. Player (black stick figure)
5. UI elements (score, lives, level)
6. Overlays (transitions, game over, leaderboard)

### Game Loop

Standard structure:
1. Process input events
2. Update game state (physics, AI, collisions)
3. Render frame
4. Maintain frame rate

### Collision Detection

**Platform collision**:
- Check player bottom against platform top for landing
- Check player top against platform bottom for head collision
- Account for all gaps currently on each platform level
- Player lands only if not in any gap
- Player blocked from jumping if hits solid platform

**Enemy collision**:
- Bounding box or circle collision
- Check overlap between player and enemy rectangles
- Only during non-invincible periods

**Screen wrapping**:
- Check if player x-position exceeds screen bounds
- Wrap to opposite edge seamlessly

### State Management

**Game states**:
1. Name Entry
2. Playing
3. Level Transition
4. Game Over
5. Leaderboard View

**State transitions**:
- Name Entry → Playing (on name submit)
- Playing → Level Transition (on reaching top)
- Level Transition → Playing (after timer/input)
- Playing → Game Over (on losing all lives)
- Game Over ↔ Leaderboard View (toggle with L key)
- Game Over → Name Entry (on restart)

## Web-Specific Considerations (for JavaScript/TypeScript)

### Canvas Rendering
- Use HTML5 Canvas API for all drawing
- Clear canvas each frame
- Use requestAnimationFrame for game loop

### Input Handling
- Listen for keyboard events on document or canvas
- Prevent default behavior for arrow keys to avoid page scrolling
- Handle key down/up for movement, key press for jumps

### Asset Loading
- Generate sounds programmatically using Web Audio API
- No external image assets needed (all procedural drawing)

### Data Persistence
- Use localStorage for leaderboard data
- JSON.stringify/parse for data serialization
- Handle localStorage quota limits gracefully

### Browser Compatibility
- Test in major browsers (Chrome, Firefox, Safari, Edge)
- Handle vendor prefixes if needed
- Provide fallbacks for older browsers

### Deployment
- Single HTML file with embedded CSS/JS, or
- Separate files: index.html, game.js, styles.css
- No build process required for pure JavaScript
- For TypeScript: compile to JavaScript, bundle if needed
- Host on static file server or GitHub Pages

## Game Balance

**Recommended values** (adjust for desired difficulty):

- **Jump height**: Should reach exactly one platform level
- **Platform spacing**: Even vertical distribution
- **Gap speed**: Start slow, increase gradually with levels
- **Gap width**: Random within reasonable range (not too small or large)
- **Enemy speed**: Slightly slower than or equal to gap speed
- **Invincibility duration**: 2 seconds at level start, 1 second after death
- **Score rate**: 10 points per second off ground
- **Lives**: 5 starting lives (generous for casual play)

## Optional Enhancements

Ideas for extending the base game:

- Power-ups (invincibility, slow-motion, extra lives)
- Different platform patterns per level
- Background music (retro-style chip tune)
- Online leaderboard with server sync
- Multiple player characters with different abilities
- Boss levels every 5 levels
- Achievement system
- Mobile touch controls
- Particle effects for jumps/landings
- Screen shake on collisions

## Summary Checklist

A complete Jumping Jack implementation must include:

- ✅ Stick figure player with running animation
- ✅ 5 evenly-spaced platforms
- ✅ Progressive gap system (more gaps each level)
- ✅ Snake/zigzag gap movement pattern
- ✅ 9 unique enemy types with unlocking system
- ✅ Random enemy colors with smart collision avoidance
- ✅ Physics-based jumping with gravity
- ✅ Platform collision (can't jump through solid platforms)
- ✅ Screen wrapping for player
- ✅ Lives system with respawning
- ✅ Scoring (only when off ground)
- ✅ Level progression with difficulty scaling
- ✅ Retro-style synthesized sound effects
- ✅ Name entry system
- ✅ Persistent leaderboard (top 10 scores)
- ✅ Level transition screens
- ✅ Game over screen with restart option
- ✅ Debug mode showing gap indices
- ✅ 60 FPS rendering with smooth animations

---

**Good luck building Jumping Jack!** 🎮
