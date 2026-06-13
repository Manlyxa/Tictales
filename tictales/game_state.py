"""
game_state.py
=============
Tracks everything that needs to be remembered as the player plays:
- How many empathy points they have earned
- Which badges they have unlocked
- Which chapters they have completed

Also handles saving and loading progress as a JSON file, so the player
can close the game and come back later.
"""

import json
import os


# The file we save progress into. It lives next to the game files.
SAVE_FILE = "tictales_save.json"


class GameState:
    """
    A simple class that holds all of the player's progress.
    We pass an instance of this around the game so every screen
    can read and update it.
    """

    # Rank ladder: (points needed, title, emoji) — checked top-down,
    # so the highest rank the player qualifies for wins.
    RANK_THRESHOLDS = [
        (600, "Champion",  "🏆"),
        (300, "Ally",      "💜"),
        (100, "Helper",    "🧡"),
        (0,   "Bystander", "👀"),
    ]

    def __init__(self):
        """
        Set up a fresh game state with zero points and no badges.
        """

        # Total empathy points the player has earned overall.
        self.total_points = 0

        # Points earned for each character separately.
        # Example: {"alex": 7, "maya": 0, "dana": 3}
        self.character_points = {"alex": 0, "maya": 0, "dana": 0}

        # A list of badge names the player has unlocked.
        # We use a set so the same badge can't be added twice.
        self.badges = set()

        # Track which chapters have been completed.
        # Example: {"alex": [1, 2], "maya": [], "dana": [1]}
        self.completed_chapters = {"alex": [], "maya": [], "dana": []}

        # Try to load saved progress from disk, if a save file exists.
        self.load()

    # ------------------------------------------------------------------
    # Adding points and badges
    # ------------------------------------------------------------------

    def add_points(self, character, points):
        """
        Add empathy points for a specific character.
        character: "alex" or "maya"
        points:    a number between 0 and 3
        """
        self.character_points[character] += points
        self.total_points += points

    def award_badge(self, badge_name):
        """
        Give the player a badge if they don't already have it.
        Returns True if this is a NEW badge, False otherwise.
        """
        if badge_name in self.badges:
            return False
        self.badges.add(badge_name)
        return True

    def complete_chapter(self, character, chapter_number):
        """
        Mark a chapter as finished for a character.
        """
        if chapter_number not in self.completed_chapters[character]:
            self.completed_chapters[character].append(chapter_number)

    # ------------------------------------------------------------------
    # Checking progress
    # ------------------------------------------------------------------

    def get_character_points(self, character):
        """Return the points earned for one character."""
        return self.character_points.get(character, 0)

    def is_character_complete(self, character):
        """Return True if all 3 chapters for this character are done."""
        return len(self.completed_chapters.get(character, [])) >= 3

    def get_badge_list(self):
        """Return badges as a sorted list for easy display."""
        return sorted(self.badges)

    def get_rank(self):
        """Return (title, emoji) for the player's current total points."""
        for threshold, title, emoji in self.RANK_THRESHOLDS:
            if self.total_points >= threshold:
                return title, emoji
        return "Bystander", "👀"

    # ------------------------------------------------------------------
    # Saving and loading
    # ------------------------------------------------------------------

    def save(self):
        """
        Save the current progress to a JSON file so the player can
        return to it later.
        """
        # Convert the badges set into a list, because JSON doesn't
        # know how to store Python sets directly.
        data = {
            "total_points": self.total_points,
            "character_points": self.character_points,
            "badges": list(self.badges),
            "completed_chapters": self.completed_chapters,
        }

        # Open the save file for writing and dump the JSON into it.
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def load(self):
        """
        Try to load saved progress from disk.
        If no save file exists yet, just stay with the fresh values.
        """
        # If there's nothing to load, just return quietly.
        if not os.path.exists(SAVE_FILE):
            return

        # If there IS a save file, read it and update our values.
        try:
            with open(SAVE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.total_points = data.get("total_points", 0)
            loaded_pts = data.get("character_points", {})
            # Merge loaded points with defaults so old save files that
            # pre-date Dana still work — they just start Dana at 0.
            self.character_points = {
                "alex": loaded_pts.get("alex", 0),
                "maya": loaded_pts.get("maya", 0),
                "dana": loaded_pts.get("dana", 0),
            }
            self.badges = set(data.get("badges", []))
            loaded_ch = data.get("completed_chapters", {})
            # Same merge approach for completed chapters.
            self.completed_chapters = {
                "alex": loaded_ch.get("alex", []),
                "maya": loaded_ch.get("maya", []),
                "dana": loaded_ch.get("dana", []),
            }
        except (json.JSONDecodeError, OSError):
            # If the save file is broken, ignore it and start fresh.
            pass

    def reset(self):
        """
        Wipe all progress and start over.
        Useful for a teacher demo or a 'new game' button.
        """
        self.total_points = 0
        self.character_points = {"alex": 0, "maya": 0, "dana": 0}
        self.badges = set()
        self.completed_chapters = {"alex": [], "maya": [], "dana": []}
        self.save()
