import json
import os
from datetime import datetime


class Leaderboard:
    def __init__(self, filename='leaderboard.json'):
        self.filename = filename
        self.scores = []
        self.last_player_name = ""
        self.load()

    def load(self):
        """Load scores from file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                    self.scores = data.get('scores', [])
                    self.last_player_name = data.get('last_player_name', "")
            except (json.JSONDecodeError, IOError):
                self.scores = []
                self.last_player_name = ""

    def save(self):
        """Save scores to file"""
        try:
            data = {
                'scores': self.scores,
                'last_player_name': self.last_player_name
            }
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=2)
        except IOError:
            pass  # Silently fail if we can't write

    def add_score(self, player_name, score, level):
        """Add a new score to the leaderboard"""
        if not player_name:
            player_name = "Anonymous"

        self.last_player_name = player_name

        entry = {
            'name': player_name,
            'score': score,
            'level': level,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }

        self.scores.append(entry)
        # Sort by level first (descending), then by score (descending)
        self.scores.sort(key=lambda x: (x['level'], x['score']), reverse=True)
        # Keep all scores in the file (no limit)
        self.save()

    def get_top_scores(self, limit=10):
        """Get the top N scores"""
        return self.scores[:limit]

    def get_last_player_name(self):
        """Get the name of the last player"""
        return self.last_player_name
