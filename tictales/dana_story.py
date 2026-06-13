"""
dana_story.py
=============
Runs Dana's three-chapter story (Autism Spectrum).
Misconception challenged: "she's rude and doesn't want friends."

Content loads from data/dana_chapters.json. Visuals use the dark
storybook theme from constants.py — the loading and chapter-flow
logic is unchanged.
"""

import json
import os
import tkinter as tk

from chapter_engine import ChapterEngine
from constants import (
    WHITE, GOLD, BG_DARK, PANEL_DARK,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED,
    get_font,
)


# Path to the JSON file with all of Dana's chapters.
DATA_FILE = os.path.join(
    os.path.dirname(__file__), "data", "dana_chapters.json"
)


class DanaStory:
    """
    Loads Dana's chapters and plays them one after another.
    When the last chapter ends, returns to the home screen.
    """

    def __init__(self, root, state):
        self.root = root
        self.state = state

        # Load the chapter content from JSON.
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.character_color = data["color"]
        self.chapters = data["chapters"]

        self.current_index = 0
        self._show_story_intro()

    def _show_story_intro(self):
        """Character intro: big accent banner + storybook panel."""

        for widget in self.root.winfo_children():
            widget.destroy()

        # --- Accent-colored banner ---
        # Dana's icon is canvas-drawn on the home screen; here we use
        # her ring symbol "◉" as the banner mark.
        banner = tk.Frame(self.root, bg=self.character_color, height=200)
        banner.pack(fill="x")
        banner.pack_propagate(False)

        tk.Label(
            banner,
            text="◉",
            font=get_font(56, "bold"),
            bg=self.character_color,
            fg=WHITE,
        ).pack(pady=(18, 0))

        tk.Label(
            banner,
            text="Meet Dana",
            font=get_font(26, "bold"),
            bg=self.character_color,
            fg=WHITE,
        ).pack()

        tk.Label(
            banner,
            text="A classmate on the Autism Spectrum",
            font=get_font(13),
            bg=self.character_color,
            fg="#E8E6F5",
        ).pack()

        # --- Dark body with the intro text in a storybook panel ---
        body = tk.Frame(self.root, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=40, pady=20)

        intro_text = (
            "Dana is in your class. She's autistic, which means her brain "
            "processes the world differently from most people.\n\n"
            "She might not make eye contact when she talks. She might find "
            "loud noises genuinely painful. She might need things to happen "
            "in a specific order to feel okay. None of this is rudeness — "
            "it's just how her nervous system works.\n\n"
            "Dana doesn't want to be alone. She just needs the people around "
            "her to understand her a little better.\n\n"
            "You are about to walk through three real moments from Dana's day."
        )

        panel = tk.Frame(
            body,
            bg=PANEL_DARK,
            highlightthickness=1,
            highlightbackground=self.character_color,
        )
        panel.pack(fill="x", pady=10)

        tk.Message(
            panel,
            text=intro_text,
            font=get_font(13),
            bg=PANEL_DARK,
            fg=TEXT_PRIMARY,
            width=680,
            justify="left",
        ).pack(padx=20, pady=16)

        tk.Button(
            body,
            text="Start Chapter 1  ▶",
            font=get_font(14, "bold"),
            bg=self.character_color,
            fg=WHITE,
            activebackground=WHITE,
            activeforeground=self.character_color,
            relief="flat",
            padx=24,
            pady=10,
            cursor="hand2",
            command=self._play_current_chapter,
        ).pack(pady=20)

    def _play_current_chapter(self):
        """Hand the current chapter to the ChapterEngine."""
        chapter_data = self.chapters[self.current_index]

        ChapterEngine(
            root=self.root,
            state=self.state,
            character_key="dana",
            character_color=self.character_color,
            character_emoji="◉",
            chapter_data=chapter_data,
            on_complete=self._on_chapter_complete,
        )

    def _on_chapter_complete(self):
        """Move to the next chapter or wrap up Dana's story."""
        self.current_index += 1

        if self.current_index < len(self.chapters):
            self._play_current_chapter()
        else:
            self._show_story_end()

    def _show_story_end(self):
        """End-of-story summary on the dark theme."""

        for widget in self.root.winfo_children():
            widget.destroy()

        banner = tk.Frame(self.root, bg=self.character_color, height=120)
        banner.pack(fill="x")
        banner.pack_propagate(False)

        tk.Label(
            banner,
            text="🌟  Dana's Story Complete!",
            font=get_font(22, "bold"),
            bg=self.character_color,
            fg=WHITE,
        ).pack(pady=35)

        body = tk.Frame(self.root, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=40, pady=20)

        # Points: big gold number with a muted "/ 9 pts" beside it.
        points = self.state.get_character_points("dana")

        points_row = tk.Frame(body, bg=BG_DARK)
        points_row.pack(pady=(10, 4))

        tk.Label(points_row, text=str(points),
                 font=get_font(34, "bold"),
                 bg=BG_DARK, fg=GOLD).pack(side="left")
        tk.Label(points_row, text=" / 9 pts",
                 font=get_font(14),
                 bg=BG_DARK, fg=TEXT_MUTED).pack(side="left", anchor="s",
                                                 pady=(0, 8))

        tk.Label(
            body,
            text="empathy points earned for Dana",
            font=get_font(11),
            bg=BG_DARK,
            fg=TEXT_SECONDARY,
        ).pack()

        closing = (
            "Dana isn't rude. She isn't cold. She isn't difficult.\n\n"
            "She's navigating a world that was mostly designed for people whose "
            "brains work differently from hers — and she's doing it every single "
            "day.\n\n"
            "When you take a moment to understand instead of judge, you don't "
            "just help Dana. You make your classroom a place where everyone can "
            "breathe more easily.\n\n"
            "Thank you for walking in Dana's shoes today."
        )

        panel = tk.Frame(
            body,
            bg=PANEL_DARK,
            highlightthickness=1,
            highlightbackground=self.character_color,
        )
        panel.pack(fill="x", pady=16)

        tk.Message(
            panel,
            text=closing,
            font=get_font(13),
            bg=PANEL_DARK,
            fg=TEXT_PRIMARY,
            width=680,
            justify="left",
        ).pack(padx=20, pady=14)

        tk.Button(
            body,
            text="🏠  Back to Home",
            font=get_font(13, "bold"),
            bg=self.character_color,
            fg=WHITE,
            activebackground=WHITE,
            activeforeground=self.character_color,
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self._return_home,
        ).pack(pady=14)

    def _return_home(self):
        """Go back to the character select screen."""
        from character_select import CharacterSelectScreen
        CharacterSelectScreen(self.root, self.state)
