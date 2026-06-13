"""
character_select.py
===================
The home screen of TicTales, in the dark "storybook at night" theme.

Layout:
  ┌─────────────────────────────────────────────┐
  │  [LOGO / Tic·Tales wordmark]   ⭐ pts  rank │
  │  "Choose a classmate to learn their story"  │
  │  [Alex card]   [Maya card]   [Dana card]    │
  │  [Teacher Module]  🏆 badges  [Start Over]  │
  └─────────────────────────────────────────────┘

All colors and fonts come from constants.py — the brand system
extracted from assets/logo.png.
"""

import math
import tkinter as tk
from tkinter import messagebox

from constants import (
    RED, NAVY, GOLD, WHITE,
    BG_DARK, CARD_DARK, PANEL_DARK,
    ALEX_COLOR, MAYA_COLOR, DANA_COLOR,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, BORDER_SUBTLE,
    get_font,
)


class CharacterSelectScreen:
    """
    Builds and shows the home screen.
    """

    def __init__(self, root, state):
        self.root = root
        self.state = state

        # Wipe whatever was on screen before.
        for widget in self.root.winfo_children():
            widget.destroy()

        self._build_header()
        self._build_character_cards()
        self._build_footer()

    # ------------------------------------------------------------------
    # Header — logo, points chip, rank, streak
    # ------------------------------------------------------------------

    def _build_header(self):
        """Logo on the left, player stats on the right."""

        header = tk.Frame(self.root, bg=BG_DARK)
        header.pack(fill="x", padx=24, pady=(18, 0))

        # --- Left side: the logo ---
        # If main.py managed to load assets/logo.png, show the image.
        # Otherwise draw the wordmark as text: red "Tic", gold dot,
        # white "Tales" (navy is too dark to read on this background).
        import main as main_module
        if main_module.LOGO_IMAGE is not None:
            tk.Label(
                header,
                image=main_module.LOGO_IMAGE,
                bg=BG_DARK,
            ).pack(side="left")
        else:
            wordmark = tk.Frame(header, bg=BG_DARK)
            wordmark.pack(side="left")

            tk.Label(wordmark, text="Tic", font=get_font(30, "bold"),
                     bg=BG_DARK, fg=RED).pack(side="left")
            tk.Label(wordmark, text="✦", font=get_font(16, "bold"),
                     bg=BG_DARK, fg=GOLD).pack(side="left", padx=2)
            tk.Label(wordmark, text="Tales", font=get_font(30, "bold"),
                     bg=BG_DARK, fg=WHITE).pack(side="left")

        # --- Right side: stats chips ---
        stats = tk.Frame(header, bg=BG_DARK)
        stats.pack(side="right")

        # Points chip — gold text in a subtle rounded-feeling panel.
        points_chip = tk.Frame(stats, bg=PANEL_DARK,
                               highlightthickness=1,
                               highlightbackground=BORDER_SUBTLE)
        points_chip.grid(row=0, column=0, padx=6)
        tk.Label(
            points_chip,
            text=f"⭐ {self.state.total_points} pts",
            font=get_font(11, "bold"),
            bg=PANEL_DARK, fg=GOLD,
            padx=12, pady=5,
        ).pack()

        # Rank chip — title based on total points.
        rank_title, rank_emoji = self.state.get_rank()
        rank_chip = tk.Frame(stats, bg=PANEL_DARK,
                             highlightthickness=1,
                             highlightbackground=BORDER_SUBTLE)
        rank_chip.grid(row=0, column=1, padx=6)
        tk.Label(
            rank_chip,
            text=f"{rank_emoji} {rank_title} rank",
            font=get_font(11, "bold"),
            bg=PANEL_DARK, fg=TEXT_PRIMARY,
            padx=12, pady=5,
        ).pack()

        # Streak chip — placeholder until streak logic exists.
        streak_chip = tk.Frame(stats, bg=PANEL_DARK,
                               highlightthickness=1,
                               highlightbackground=BORDER_SUBTLE)
        streak_chip.grid(row=1, column=0, columnspan=2, pady=(6, 0),
                         sticky="e")
        tk.Label(
            streak_chip,
            text="🔥 Start your streak!",
            font=get_font(10),
            bg=PANEL_DARK, fg=TEXT_SECONDARY,
            padx=12, pady=4,
        ).pack()

        # --- Invite line under the header ---
        tk.Label(
            self.root,
            text="Choose a classmate to learn their story",
            font=get_font(13),
            bg=BG_DARK,
            fg=TEXT_MUTED,
        ).pack(pady=(16, 8))

    # ------------------------------------------------------------------
    # Three character cards
    # ------------------------------------------------------------------

    def _build_character_cards(self):
        """Draw all three character cards side by side in one row."""

        cards_frame = tk.Frame(self.root, bg=BG_DARK)
        cards_frame.pack(pady=8)

        # Alex — Tourette Syndrome (teal)
        self._build_card(
            parent=cards_frame,
            name="Alex",
            tagline="Tourette Syndrome",
            description="Alex has tics he can't control.\nWalk through his school day.",
            color=ALEX_COLOR,
            character_key="alex",
            column=0,
            emoji="😊",
        )

        # Maya — ADHD (warm orange)
        self._build_card(
            parent=cards_frame,
            name="Maya",
            tagline="ADHD",
            description="Maya's brain works fast.\nSee the world through her eyes.",
            color=MAYA_COLOR,
            character_key="maya",
            column=1,
            emoji="🌈",
        )

        # Dana — Autism Spectrum (soft purple, canvas icon)
        self._build_card(
            parent=cards_frame,
            name="Dana",
            tagline="Autism Spectrum",
            description="Dana experiences the world\ndifferently. See through her eyes.",
            color=DANA_COLOR,
            character_key="dana",
            column=2,
            emoji=None,              # None = draw the canvas icon
        )

    def _build_card(self, parent, name, tagline, description,
                    color, character_key, column, emoji=None):
        """
        Build one character card on the dark theme:
        a CARD_DARK panel with a 4px accent strip on the left edge,
        a thin progress bar, and a solid accent-colored Play button.
        """

        # Outer wrapper — dark card.
        card = tk.Frame(parent, bg=CARD_DARK, cursor="hand2",
                        highlightthickness=0,
                        highlightbackground=color)
        card.grid(row=0, column=column, padx=12, pady=10)

        # Left color accent bar — a 4px-wide frame filling the height.
        accent_bar = tk.Frame(card, bg=color, width=4)
        accent_bar.pack(side="left", fill="y")

        # Content area. Width is pinned; height grows to fit.
        content = tk.Frame(card, bg=CARD_DARK)
        content.pack(side="left", fill="both", expand=True,
                     padx=14, pady=16)

        # Invisible spacer pins the content width to 220px while the
        # height stays free — so nothing gets cut off at high DPI.
        tk.Frame(content, width=220, height=1, bg=CARD_DARK).pack()

        # --- Icon ---
        if emoji:
            tk.Label(content, text=emoji,
                     font=("Segoe UI Emoji", 48),
                     bg=CARD_DARK, fg=WHITE).pack()
        else:
            self._draw_dana_icon(content, color)

        # --- Name ---
        tk.Label(content, text=name,
                 font=get_font(20, "bold"),
                 bg=CARD_DARK, fg=WHITE).pack()

        # --- Condition (in the character's accent color) ---
        tk.Label(content, text=tagline,
                 font=get_font(11),
                 bg=CARD_DARK, fg=color).pack(pady=(0, 4))

        # --- Description ---
        tk.Label(content, text=description,
                 font=get_font(10),
                 bg=CARD_DARK, fg=TEXT_SECONDARY,
                 justify="center").pack(pady=4)

        # --- Progress bar (thin Canvas strip) ---
        completed = len(self.state.completed_chapters.get(character_key, []))
        points = self.state.get_character_points(character_key)
        pct = completed / 3.0

        bar_canvas = tk.Canvas(content, width=190, height=6,
                               bg=BORDER_SUBTLE, highlightthickness=0)
        bar_canvas.pack(pady=(8, 2))
        if pct > 0:
            bar_canvas.create_rectangle(0, 0, int(190 * pct), 6,
                                        fill=color, outline="")

        tk.Label(content,
                 text=f"Ch {completed}/3  ·  ⭐ {points}/9 pts",
                 font=get_font(10),
                 bg=CARD_DARK, fg=TEXT_MUTED).pack()

        # --- Play button ---
        tk.Button(
            content,
            text=f"▶  Play as {name}",
            font=get_font(11, "bold"),
            bg=color, fg=WHITE,
            activebackground=WHITE, activeforeground=color,
            relief="flat", padx=12, pady=7,
            cursor="hand2",
            command=lambda k=character_key: self._start_story(k),
        ).pack(pady=(12, 4))

        # --- Hover effect: light up the card border ---
        def on_enter(event):
            card.config(highlightthickness=1, highlightbackground=color)

        def on_leave(event):
            card.config(highlightthickness=0)

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)

    # ------------------------------------------------------------------
    # Dana's canvas icon
    # ------------------------------------------------------------------

    def _draw_dana_icon(self, parent, color):
        """
        Dana's icon, drawn with Tkinter Canvas shapes: a white ring with
        six evenly-spaced dots inside and a centre dot — representing
        how Dana notices precise patterns others walk past.

        math.cos / math.sin place the dots 60° apart around the circle.
        """

        SIZE = 64
        cx = cy = SIZE // 2
        R = SIZE // 2 - 8

        canvas = tk.Canvas(parent, width=SIZE, height=SIZE,
                           bg=CARD_DARK, highlightthickness=0)
        canvas.pack()

        # Outer ring.
        canvas.create_oval(cx - R, cy - R, cx + R, cy + R,
                           outline=WHITE, width=2, fill="")

        # Six dots around the ring, starting at the top (-90°).
        dot_radius = 4
        dot_orbit = R - 8
        for i in range(6):
            angle = math.radians(i * 60 - 90)
            x = cx + dot_orbit * math.cos(angle)
            y = cy + dot_orbit * math.sin(angle)
            canvas.create_oval(x - dot_radius, y - dot_radius,
                               x + dot_radius, y + dot_radius,
                               fill=WHITE, outline="")

        # Centre dot in the character accent color.
        canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5,
                           fill=color, outline="")

    # ------------------------------------------------------------------
    # Footer
    # ------------------------------------------------------------------

    def _build_footer(self):
        """Teacher button, badge count, and reset — dark restyle."""

        footer = tk.Frame(self.root, bg=BG_DARK)
        footer.pack(pady=16)

        # Teacher Module — navy, like the "Tales" wordmark.
        tk.Button(
            footer,
            text="👩‍🏫  Teacher Module",
            font=get_font(12, "bold"),
            bg=NAVY, fg=WHITE,
            activebackground=WHITE, activeforeground=NAVY,
            relief="flat", padx=18, pady=8,
            cursor="hand2",
            command=self._open_teacher_module,
        ).grid(row=0, column=0, padx=10)

        # Badge count — gold on dark.
        badge_count = len(self.state.badges)
        tk.Label(
            footer,
            text=f"🏆 Badges earned: {badge_count}",
            font=get_font(12),
            bg=BG_DARK, fg=GOLD,
        ).grid(row=0, column=1, padx=20)

        # Reset — small and muted so it doesn't tempt anyone.
        tk.Button(
            footer,
            text="🔄  Start Over",
            font=get_font(9),
            bg=PANEL_DARK, fg=TEXT_MUTED,
            activebackground=BORDER_SUBTLE, activeforeground=TEXT_SECONDARY,
            relief="flat", padx=10, pady=5,
            cursor="hand2",
            command=self._confirm_reset,
        ).grid(row=0, column=2, padx=10)

    # ------------------------------------------------------------------
    # Navigation / button actions
    # ------------------------------------------------------------------

    def _start_story(self, character_key):
        """
        Launch the story for the chosen character.
        Imports live inside the function to avoid circular imports.
        """
        if character_key == "alex":
            from alex_story import AlexStory
            AlexStory(self.root, self.state)

        elif character_key == "maya":
            from maya_story import MayaStory
            MayaStory(self.root, self.state)

        elif character_key == "dana":
            from dana_story import DanaStory
            DanaStory(self.root, self.state)

    def _open_teacher_module(self):
        """Open the educator-facing micro-learning screen."""
        from teacher_module import TeacherModule
        TeacherModule(self.root, self.state)

    def _confirm_reset(self):
        """Ask before wiping all progress."""
        if messagebox.askyesno(
            "Start Over?",
            "This will erase all points and badges. Are you sure?",
        ):
            self.state.reset()
            CharacterSelectScreen(self.root, self.state)
