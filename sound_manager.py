import pygame
import numpy as np
import io


class SoundManager:
    """Manages all game sounds with retro-style synthesized effects"""

    def __init__(self):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self.sounds = {}
        self.generate_all_sounds()

        # Sound cooldowns to prevent spam
        self.walk_cooldown = 0
        self.walk_cooldown_max = 8  # frames between footstep sounds

    def generate_tone(self, frequency, duration, volume=0.3, sample_rate=22050):
        """Generate a simple sine wave tone"""
        n_samples = int(duration * sample_rate)
        t = np.linspace(0, duration, n_samples, False)
        wave = np.sin(2 * np.pi * frequency * t) * volume
        # Convert to 16-bit signed integers
        wave = (wave * 32767).astype(np.int16)
        # Make stereo
        stereo_wave = np.column_stack((wave, wave))
        return pygame.sndarray.make_sound(stereo_wave)

    def generate_sweep(self, freq_start, freq_end, duration, volume=0.3, sample_rate=22050):
        """Generate a frequency sweep (slide)"""
        n_samples = int(duration * sample_rate)
        t = np.linspace(0, duration, n_samples, False)
        # Linear frequency sweep
        freq = np.linspace(freq_start, freq_end, n_samples)
        phase = np.cumsum(2 * np.pi * freq / sample_rate)
        wave = np.sin(phase) * volume
        # Add envelope for smoother sound
        envelope = np.exp(-3 * t / duration)  # Decay envelope
        wave = wave * envelope
        # Convert to 16-bit signed integers
        wave = (wave * 32767).astype(np.int16)
        # Make stereo
        stereo_wave = np.column_stack((wave, wave))
        return pygame.sndarray.make_sound(stereo_wave)

    def generate_noise(self, duration, volume=0.2, sample_rate=22050):
        """Generate white noise (for landing/falling sounds)"""
        n_samples = int(duration * sample_rate)
        t = np.linspace(0, duration, n_samples, False)
        wave = np.random.uniform(-1, 1, n_samples) * volume
        # Add envelope
        envelope = np.exp(-8 * t / duration)  # Fast decay
        wave = wave * envelope
        # Convert to 16-bit signed integers
        wave = (wave * 32767).astype(np.int16)
        # Make stereo
        stereo_wave = np.column_stack((wave, wave))
        return pygame.sndarray.make_sound(stereo_wave)

    def generate_all_sounds(self):
        """Generate all game sound effects"""
        try:
            # Jump sound - upward sweep (rising pitch)
            self.sounds['jump'] = self.generate_sweep(200, 600, 0.15, volume=0.25)

            # Walk/footstep - short low tone
            self.sounds['walk'] = self.generate_tone(150, 0.08, volume=0.15)

            # Landing sound - quick downward sweep with noise
            landing_sweep = self.generate_sweep(400, 150, 0.12, volume=0.2)
            landing_noise = self.generate_noise(0.08, volume=0.15)
            # Mix both sounds
            self.sounds['land'] = landing_sweep

            # Death/hit sound - harsh downward sweep
            self.sounds['death'] = self.generate_sweep(600, 100, 0.3, volume=0.3)

            # Level complete - upward celebration sweep
            self.sounds['level_complete'] = self.generate_sweep(300, 800, 0.5, volume=0.25)

        except Exception as e:
            print(f"Warning: Could not generate sounds: {e}")
            # Disable sounds if generation fails
            self.sounds = {}

    def play(self, sound_name):
        """Play a sound effect"""
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Warning: Could not play sound '{sound_name}': {e}")

    def play_walk(self):
        """Play footstep sound with cooldown to avoid spam"""
        if self.walk_cooldown <= 0:
            self.play('walk')
            self.walk_cooldown = self.walk_cooldown_max

    def update(self):
        """Update sound cooldowns"""
        if self.walk_cooldown > 0:
            self.walk_cooldown -= 1
