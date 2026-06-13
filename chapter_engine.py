"""
chapter_engine.py
=================
The heart of the game. Runs ONE chapter for ANY character through:

    1. Intro      — what's happening in the scene
    2. Choice     — show 4 options, player picks one
    3. Outcome    — the consequence of the choice
    4. Fact       — MYTH vs REALITY + real facts about the condition
    5. Reflection — a question for the player to think about
    6. Badge      — award an empathy badge if the player did well

Dark "storybook at night" theme — all colors from constants.py.
The game logic (points, badges, save/load) is unchanged; only the
visual layer was redesigned.
"""

import random
import tkinter as tk

from constants import (
    RED, NAVY, GOLD, WHITE,
    BG_DARK, CARD_DARK, PANEL_DARK,
    ALEX_COLOR, MAYA_COLOR, DANA_COLOR,
    COLOR_BEST, COLOR_OK, COLOR_WRONG,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, BORDER_SUBTLE,
    get_font,
)


# Verdict colors used to give the player visual feedback.
VERDICT_COLORS = {
    "BEST": COLOR_BEST,    # green
    "OK": COLOR_OK,        # amber
    "WRONG": COLOR_WRONG,  # red
}

# Verdict headlines for the outcome screen.
VERDICT_HEADLINES = {
    "BEST": "✅  Great choice!",
    "OK": "👍  Decent choice",
    "WRONG": "⚠️  What actually happened...",
}

# Tinted color pairs for the four choice buttons: (text color, dark bg).
CHOICE_COLORS = [
    ("#1D9E75", "#0A3D2E"),  # A: teal text, dark teal bg
    ("#6C5CE7", "#1E1854"),  # B: purple text, dark purple bg
    ("#F5A623", "#3D2A00"),  # C: amber text, dark amber bg
    ("#B0ADCC", "#1A1930"),  # D: muted text, near-black bg
]

# Which emoji celebrates each badge on the ceremony screen.
BADGE_EMOJIS = {
    "Kind Observer":     "👁️",
    "Lunch Hero":        "🥗",
    "Team Player":       "🤝",
    "Calm Friend":       "🫂",
    "Problem Solver":    "🧩",
    "Empathy Star":      "🌟",
    "Tourette Champion": "🏆",
    "ADHD Ally":         "🎯",
    "Autism Ally":       "💜",
    "First Step":        "🌱",
}

# Colors used by the confetti animation.
CONFETTI_COLORS = [GOLD, RED, ALEX_COLOR, MAYA_COLOR, DANA_COLOR, WHITE]


class ChapterEngine:
    """
    Runs a single chapter from start to finish.
    When the chapter ends, calls on_complete() so the story
    can move to the next chapter or back to the home screen.
    """

    def __init__(self, root, state, character_key, character_color,
                 character_emoji, chapter_data, on_complete):
        self.root = root
        self.state = state
        self.character_key = character_key
        self.color = character_color
        self.emoji = character_emoji
        self.chapter = chapter_data
        self.on_complete = on_complete

        # Track the points earned during THIS chapter (0-3).
        self.points_this_chapter = 0

        # Kick things off by showing the intro screen.
        self._show_intro()

    # ------------------------------------------------------------------
    # Helpers used by every screen
    # ------------------------------------------------------------------

    def _clear(self):
        """Wipe the window so we can draw the next screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def _header(self):
        """
        Accent-colored banner at the top of every chapter screen.
        Two rows: a small "Chapter N" label, then the chapter title.
        """
        banner = tk.Frame(self.root, bg=self.color, height=72)
        banner.pack(fill="x")
        banner.pack_propagate(False)

        inner = tk.Frame(banner, bg=self.color)
        inner.pack(expand=True)

        # Small chapter label in a lighter tint of white.
        tk.Label(
            inner,
            text=f"Chapter {self.chapter['number']}",
            font=get_font(11),
            bg=self.color,
            fg="#E8E6F5",      # soft near-white (Tk has no rgba)
        ).pack()

        tk.Label(
            inner,
            text=f"{self.emoji}  {self.chapter['title']}",
            font=get_font(17, "bold"),
            bg=self.color,
            fg=WHITE,
        ).pack()

    def _accent_button(self, parent, text, command):
        """A solid accent-colored button — same style on every screen."""
        return tk.Button(
            parent,
            text=text,
            font=get_font(13, "bold"),
            bg=self.color, fg=WHITE,
            activebackground=WHITE, activeforeground=self.color,
            relief="flat", padx=20, pady=10,
            cursor="hand2",
            command=command,
        )

    # ------------------------------------------------------------------
    # Step 1: Intro
    # ------------------------------------------------------------------

    def _show_intro(self):
        """The scene-setting paragraph in a storybook panel."""
        self._clear()
        self._header()

        intro_frame = tk.Frame(self.root, bg=BG_DARK)
        intro_frame.pack(fill="both", expand=True, padx=40, pady=20)

        tk.Label(
            intro_frame,
            text="📖  The scene...",
            font=get_font(14, "bold"),
            bg=BG_DARK,
            fg=self.color,
        ).pack(pady=(10, 8), anchor="w")

        # Storybook panel: dark card with a subtle accent border.
        panel = tk.Frame(
            intro_frame,
            bg=PANEL_DARK,
            highlightthickness=1,
            highlightbackground=self.color,
        )
        panel.pack(fill="x", pady=10)

        tk.Message(
            panel,
            text=self.chapter["intro"],
            font=get_font(14),
            bg=PANEL_DARK,
            fg=TEXT_PRIMARY,
            width=700,
            justify="left",
        ).pack(padx=20, pady=16, anchor="w")

        self._accent_button(
            intro_frame, "What do you do?  ▶", self._show_choices
        ).pack(pady=30)

    # ------------------------------------------------------------------
    # Step 2: Choices
    # ------------------------------------------------------------------

    def _show_choices(self):
        """Show all 4 tinted choice buttons."""
        self._clear()
        self._header()

        choices_frame = tk.Frame(self.root, bg=BG_DARK)
        choices_frame.pack(fill="both", expand=True, padx=40, pady=15)

        tk.Label(
            choices_frame,
            text=f"🤔  {self.chapter['question']}",
            font=get_font(16, "bold"),
            bg=BG_DARK,
            fg=TEXT_PRIMARY,
        ).pack(pady=(10, 20))

        # One tinted button per choice — each gets its own color pair.
        for i, choice in enumerate(self.chapter["choices"]):
            self._build_choice_button(choices_frame, choice, i)

    def _build_choice_button(self, parent, choice, index):
        """One choice button with a tinted dark background."""
        text_color, bg_color = CHOICE_COLORS[index % 4]

        btn = tk.Button(
            parent,
            text=f"  {choice['label']}.  {choice['text']}",
            font=get_font(12),
            bg=bg_color,
            fg=text_color,
            relief="flat",
            bd=0,
            anchor="w",
            padx=16,
            pady=14,
            cursor="hand2",
            wraplength=800,
            justify="left",
            command=lambda c=choice: self._show_outcome(c),
            activebackground=text_color,
            activeforeground=WHITE,
        )
        btn.pack(fill="x", pady=5)

        # Hover: show a thin border in the choice's text color.
        def on_enter(event):
            btn.config(highlightthickness=1,
                       highlightbackground=text_color,
                       highlightcolor=text_color)

        def on_leave(event):
            btn.config(highlightthickness=0)

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    # ------------------------------------------------------------------
    # Step 3: Outcome
    # ------------------------------------------------------------------

    def _show_outcome(self, choice):
        """Show what happened because of the player's choice."""

        # Remember the points so we can show the score at the end.
        self.points_this_chapter = choice["points"]

        # Add points to the long-term game state right away.
        self.state.add_points(self.character_key, choice["points"])

        self._clear()
        self._header()

        outcome_frame = tk.Frame(self.root, bg=BG_DARK)
        outcome_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # Verdict headline in its color.
        verdict = choice["verdict"]
        verdict_color = VERDICT_COLORS.get(verdict, TEXT_PRIMARY)
        headline = VERDICT_HEADLINES.get(verdict, verdict)

        tk.Label(
            outcome_frame,
            text=headline,
            font=get_font(18, "bold"),
            bg=BG_DARK,
            fg=verdict_color,
        ).pack(pady=(5, 2), anchor="w")

        tk.Label(
            outcome_frame,
            text=f"Your choice: {choice['label']}",
            font=get_font(11),
            bg=BG_DARK,
            fg=TEXT_MUTED,
        ).pack(pady=(0, 8), anchor="w")

        # Points — animated count-up from 0 to the earned amount.
        points_label = tk.Label(
            outcome_frame,
            text="+0 pts",
            font=get_font(15, "bold"),
            bg=BG_DARK,
            fg=GOLD,
        )
        points_label.pack(pady=4, anchor="w")
        self._animate_points(points_label, choice["points"])

        # Outcome text in a dark panel with accent left border.
        panel = tk.Frame(outcome_frame, bg=BG_DARK)
        panel.pack(fill="x", pady=(12, 5))

        tk.Frame(panel, bg=self.color, width=4).pack(side="left", fill="y")

        text_card = tk.Frame(panel, bg=PANEL_DARK)
        text_card.pack(side="left", fill="both", expand=True)

        tk.Label(
            text_card,
            text="What happened next:",
            font=get_font(12, "bold"),
            bg=PANEL_DARK,
            fg=TEXT_SECONDARY,
        ).pack(padx=16, pady=(12, 2), anchor="w")

        tk.Message(
            text_card,
            text=choice["outcome"],
            font=get_font(13),
            bg=PANEL_DARK,
            fg=TEXT_PRIMARY,
            width=680,
            justify="left",
        ).pack(padx=16, pady=(0, 14), anchor="w")

        self._accent_button(
            outcome_frame, "Learn the science  ▶", self._show_fact
        ).pack(pady=25)

    # ------------------------------------------------------------------
    # Step 4: Fact — MYTH vs REALITY + fact cards
    # ------------------------------------------------------------------

    def _show_fact(self):
        """MYTH/REALITY split cards, then the chapter's real facts."""
        self._clear()
        self._header()

        fact_frame = tk.Frame(self.root, bg=BG_DARK)
        fact_frame.pack(fill="both", expand=True, padx=30, pady=20)

        tk.Label(
            fact_frame,
            text="💡  Did you know?",
            font=get_font(18, "bold"),
            bg=BG_DARK,
            fg=self.color,
        ).pack(pady=(0, 16))

        # --- MYTH / REALITY split (only if the JSON provides them) ---
        myth = self.chapter.get("myth")
        reality = self.chapter.get("reality")

        if myth and reality:
            split = tk.Frame(fact_frame, bg=BG_DARK)
            split.pack(fill="x", pady=8)
            split.columnconfigure(0, weight=1)
            split.columnconfigure(1, weight=1)

            # MYTH card — red tint.
            myth_card = tk.Frame(split, bg="#2D0A0A",
                                 highlightthickness=1,
                                 highlightbackground=COLOR_WRONG)
            myth_card.grid(row=0, column=0, padx=(0, 6), sticky="nsew")

            tk.Label(myth_card, text="MYTH",
                     font=get_font(11, "bold"),
                     bg="#2D0A0A", fg=COLOR_WRONG).pack(pady=(10, 4))
            tk.Message(myth_card, text=myth,
                       font=get_font(12),
                       bg="#2D0A0A", fg="#FFAAAA",
                       width=320, justify="center").pack(padx=12,
                                                         pady=(0, 12))

            # REALITY card — green tint.
            reality_card = tk.Frame(split, bg="#0A2D1A",
                                    highlightthickness=1,
                                    highlightbackground=COLOR_BEST)
            reality_card.grid(row=0, column=1, padx=(6, 0), sticky="nsew")

            tk.Label(reality_card, text="REALITY",
                     font=get_font(11, "bold"),
                     bg="#0A2D1A", fg=COLOR_BEST).pack(pady=(10, 4))
            tk.Message(reality_card, text=reality,
                       font=get_font(12),
                       bg="#0A2D1A", fg="#AAFFCC",
                       width=320, justify="center").pack(padx=12,
                                                         pady=(0, 12))

        # --- Regular fact cards ---
        for fact in self.chapter["facts"]:
            card = tk.Frame(fact_frame, bg=PANEL_DARK,
                            highlightthickness=1,
                            highlightbackground=self.color)
            card.pack(fill="x", pady=6)

            tk.Message(
                card,
                text=f"💡  {fact}",
                font=get_font(12),
                bg=PANEL_DARK,
                fg=TEXT_PRIMARY,
                width=750,
                justify="left",
            ).pack(padx=15, pady=10, anchor="w")

        self._accent_button(
            fact_frame, "Got it!  ▶", self._show_reflection
        ).pack(pady=20)

    # ------------------------------------------------------------------
    # Step 5: Reflection
    # ------------------------------------------------------------------

    def _show_reflection(self):
        """A reflection question — no right answer, just thinking."""
        self._clear()
        self._header()

        reflect_frame = tk.Frame(self.root, bg=BG_DARK)
        reflect_frame.pack(fill="both", expand=True, padx=40, pady=20)

        tk.Label(
            reflect_frame,
            text="💭  Take a moment to think...",
            font=get_font(18, "bold"),
            bg=BG_DARK,
            fg=self.color,
        ).pack(pady=(10, 20))

        tk.Message(
            reflect_frame,
            text=self.chapter["reflection"],
            font=get_font(15),
            bg=BG_DARK,
            fg=TEXT_PRIMARY,
            width=700,
            justify="center",
        ).pack(pady=20)

        tk.Label(
            reflect_frame,
            text="(There's no right answer. Just notice what you feel.)",
            font=get_font(11),
            bg=BG_DARK,
            fg=TEXT_MUTED,
        ).pack(pady=5)

        self._accent_button(
            reflect_frame, "Finish chapter  ▶", self._show_badge
        ).pack(pady=25)

    # ------------------------------------------------------------------
    # Step 6: Badge ceremony
    # ------------------------------------------------------------------

    def _show_badge(self):
        """Award badges (if earned) and celebrate — then end the chapter."""
        self._clear()
        self._header()

        wrap_frame = tk.Frame(self.root, bg=BG_DARK)
        wrap_frame.pack(fill="both", expand=True, padx=40, pady=10)

        # ---------- game logic (unchanged) ----------
        self.state.complete_chapter(self.character_key,
                                    self.chapter["number"])

        new_badges = []

        # Chapter-specific badge requires at least 2 points.
        if self.points_this_chapter >= 2:
            chapter_badge = self.chapter["badge"]
            if self.state.award_badge(chapter_badge):
                new_badges.append(chapter_badge)

        # End-of-character badges (only after chapter 3).
        if self.state.is_character_complete(self.character_key):
            character_total = self.state.get_character_points(
                self.character_key)

            if character_total >= 8 and self.state.award_badge("Empathy Star"):
                new_badges.append("Empathy Star")

            if self.character_key == "alex":
                if self.state.award_badge("Tourette Champion"):
                    new_badges.append("Tourette Champion")
            elif self.character_key == "maya":
                if self.state.award_badge("ADHD Ally"):
                    new_badges.append("ADHD Ally")
            elif self.character_key == "dana":
                if self.state.award_badge("Autism Ally"):
                    new_badges.append("Autism Ally")

        self.state.save()
        # ---------- end game logic ----------

        # ---------- celebration visuals ----------
        if new_badges:
            # Confetti canvas strip across the top of the ceremony.
            confetti_canvas = tk.Canvas(wrap_frame, height=90,
                                        bg=BG_DARK, highlightthickness=0)
            confetti_canvas.pack(fill="x")
            self._show_confetti(confetti_canvas)

            # Celebrate the first new badge with a big bouncing emoji.
            first_badge = new_badges[0]
            badge_label = tk.Label(
                wrap_frame,
                text=BADGE_EMOJIS.get(first_badge, "⭐"),
                font=("Segoe UI Emoji", 20),
                bg=BG_DARK,
            )
            badge_label.pack(pady=4)
            self._animate_badge_bounce(
                badge_label,
                [20, 30, 45, 60, 70, 72, 70, 72, 70, 72],
            )

            tk.Label(
                wrap_frame,
                text="NEW BADGE UNLOCKED",
                font=get_font(11, "bold"),
                bg=BG_DARK,
                fg=GOLD,
            ).pack()

            tk.Label(
                wrap_frame,
                text=first_badge,
                font=get_font(22, "bold"),
                bg=BG_DARK,
                fg=WHITE,
            ).pack(pady=4)

            # Any additional badges listed in smaller gold text.
            for badge in new_badges[1:]:
                tk.Label(
                    wrap_frame,
                    text=f"{BADGE_EMOJIS.get(badge, '⭐')}  {badge}",
                    font=get_font(13, "bold"),
                    bg=BG_DARK,
                    fg=GOLD,
                ).pack(pady=2)
        else:
            tk.Label(
                wrap_frame,
                text="🎉  Chapter complete!",
                font=get_font(22, "bold"),
                bg=BG_DARK,
                fg=self.color,
            ).pack(pady=(25, 10))

            tk.Label(
                wrap_frame,
                text="(No new badges this time — try a kinder choice next time!)",
                font=get_font(11),
                bg=BG_DARK,
                fg=TEXT_MUTED,
            ).pack(pady=10)

        tk.Label(
            wrap_frame,
            text=f"You earned {self.points_this_chapter} empathy points this chapter.",
            font=get_font(13),
            bg=BG_DARK,
            fg=TEXT_SECONDARY,
        ).pack(pady=8)

        self._accent_button(
            wrap_frame, "Continue  ▶", self.on_complete
        ).pack(pady=18)

    # ------------------------------------------------------------------
    # Animations — pure Tkinter, driven by root.after()
    # ------------------------------------------------------------------

    def _animate_points(self, label, target, current=0):
        """Animate a label counting up from 0 to the points earned."""
        try:
            label.config(text=f"+{current} pts")
        except tk.TclError:
            return   # the screen changed mid-animation — stop quietly

        if current < target:
            # Faster steps for bigger numbers, never faster than 60fps.
            delay = max(16, int(500 / max(target, 1)))
            self.root.after(delay, self._animate_points,
                            label, target, current + 1)

    def _animate_badge_bounce(self, label, sizes, idx=0):
        """Bounce the badge emoji by cycling through font sizes."""
        if idx >= len(sizes):
            return
        try:
            label.config(font=("Segoe UI Emoji", sizes[idx]))
        except tk.TclError:
            return   # screen changed — stop quietly
        self.root.after(40, self._animate_badge_bounce,
                        label, sizes, idx + 1)

    def _show_confetti(self, canvas, dots=None, frame=0):
        """Animate ~20 colored dots falling down the canvas strip."""

        if dots is None:   # first frame — create the dots
            dots = []
            for _ in range(20):
                x = random.randint(20, 800)
                y = random.randint(-80, 0)
                color = random.choice(CONFETTI_COLORS)
                size = random.randint(6, 12)
                dot_id = canvas.create_oval(x, y, x + size, y + size,
                                            fill=color, outline="")
                dots.append({
                    "id": dot_id, "x": x, "y": y, "size": size,
                    "vx": random.uniform(-1, 1),
                    "vy": random.uniform(2, 4),
                })

        # Move each dot down (and slightly sideways).
        active = []
        try:
            for dot in dots:
                dot["y"] += dot["vy"]
                dot["x"] += dot["vx"]
                canvas.coords(dot["id"],
                              dot["x"], dot["y"],
                              dot["x"] + dot["size"],
                              dot["y"] + dot["size"])
                if dot["y"] < 110:   # still inside the strip
                    active.append(dot)
        except tk.TclError:
            return   # canvas was destroyed — stop quietly

        if active and frame < 120:   # run for at most ~2 seconds
            self.root.after(16, self._show_confetti,
                            canvas, active, frame + 1)
