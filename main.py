"""
TicTales: Every Story Matters
=============================
Stanford Code in Place — Final Project
A gamified empathy education game built with Python + Tkinter.

Run this file to start the game:
    python main.py
"""

import os
import tkinter as tk

from character_select import CharacterSelectScreen
from game_state import GameState
from constants import BG_DARK


# The logo image lives here after main() loads it.
# Other files do:  import main; main.LOGO_IMAGE
# If PIL isn't installed or the file is missing, this stays None and
# the home screen shows a text "Tic·Tales" wordmark instead.
LOGO_IMAGE = None

# Path to the logo, relative to this file so it works from any folder.
LOGO_PATH = os.path.join(os.path.dirname(__file__), "assets", "logo.png")


def _load_logo():
    """
    Try to load assets/logo.png with PIL.
    Must be called AFTER the Tk root window exists, because
    ImageTk.PhotoImage needs a running Tk to attach to.
    Returns the image, or None if anything is missing.
    """
    global LOGO_IMAGE
    try:
        from PIL import ImageTk, Image as PILImage
        _logo = PILImage.open(LOGO_PATH).resize((180, 60), PILImage.LANCZOS)
        LOGO_IMAGE = ImageTk.PhotoImage(_logo)
    except Exception:
        LOGO_IMAGE = None   # falls back to text wordmark
    return LOGO_IMAGE


def main():
    """
    The main function — this is where the game starts.
    """

    # Step 1: Create the main game window.
    root = tk.Tk()
    root.title("TicTales: Every Story Matters")

    # Comfortable size for kids to read, with room for three cards.
    root.geometry("960x700")
    root.minsize(900, 660)

    # Dark navy background — like a storybook at night.
    root.configure(bg=BG_DARK)

    # Step 2: Load the logo (needs the root window to exist first).
    _load_logo()

    # Step 3: Create the GameState — remembers points, badges, progress.
    state = GameState()

    # Step 4: Show the home screen.
    CharacterSelectScreen(root, state)

    # Step 5: Start the event loop — keeps the window open.
    root.mainloop()


if __name__ == "__main__":
    main()
