"""
teacher_module.py
=================
The educator-facing micro-learning screen, restyled on the dark theme.

For each character this module shows:
1. The medical facts in simple, plain language
2. Three classroom strategies that work
3. Common mistakes teachers make
4. A short 3-question multiple-choice quiz

Header uses brand NAVY (the "Tales" wordmark color) — calmer and more
professional than the kids' story screens. All quiz/scroll logic is
unchanged from the previous version.
"""

import tkinter as tk
from tkinter import messagebox

from constants import (
    NAVY, GOLD, WHITE,
    BG_DARK, CARD_DARK, PANEL_DARK,
    ALEX_COLOR, MAYA_COLOR,
    TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED, BORDER_SUBTLE,
    get_font,
)


# Tinted color pairs for quiz options — same pattern as the chapter
# choice buttons: (text color, dark background).
CHOICE_COLORS = [
    ("#1D9E75", "#0A3D2E"),
    ("#6C5CE7", "#1E1854"),
    ("#F5A623", "#3D2A00"),
    ("#B0ADCC", "#1A1930"),
]


# ----------------------------------------------------------------------
# All teacher-facing content. Same shape per character.
# ----------------------------------------------------------------------
TEACHER_CONTENT = {
    "alex": {
        "name": "Alex",
        "condition": "Tourette Syndrome",
        "color": ALEX_COLOR,
        "facts": [
            "Tourette Syndrome is a neurological condition involving sudden, "
            "repetitive movements or sounds called 'tics.'",
            "Tics are involuntary. Asking a student to 'stop' a tic is like "
            "asking them to stop a sneeze.",
            "Stress, anxiety, and being watched all increase tic frequency. "
            "A calm, accepting environment reduces it.",
            "Most students with Tourette's have average or above-average "
            "intelligence. The tics do not affect cognitive ability.",
        ],
        "strategies": [
            "Never ask Alex to 'stop' his tics in front of the class.",
            "Provide a private signal Alex can use to step out if tics "
            "become intense — a quiet hallway break can reset the nervous system.",
            "Educate the whole class about neurological differences early in "
            "the year, before incidents happen, not after.",
        ],
        "mistakes": [
            "Disciplining a student for tics they cannot control.",
            "Singling them out 'kindly' in front of the class.",
            "Assuming the tic is a behavior choice that can be modified "
            "with consequences.",
        ],
        "quiz": [
            {
                "question": "A student's vocal tic is disrupting class. "
                            "What is the BEST first response?",
                "options": [
                    "Ask the student to step outside until they can be quiet.",
                    "Continue teaching as if nothing happened, and follow up privately later.",
                    "Stop the lesson to address the class about the tic.",
                ],
                "correct": 1,
            },
            {
                "question": "Which of these increases tic frequency?",
                "options": [
                    "A calm, predictable classroom environment.",
                    "Stress, social pressure, and being closely watched.",
                    "Letting the student focus on a task they enjoy.",
                ],
                "correct": 1,
            },
            {
                "question": "True or false: students with Tourette's are "
                            "doing it on purpose for attention.",
                "options": [
                    "True — most tics are a learned behavior.",
                    "False — tics are involuntary neurological events.",
                    "It depends on the student.",
                ],
                "correct": 1,
            },
        ],
    },
    "maya": {
        "name": "Maya",
        "condition": "ADHD",
        "color": MAYA_COLOR,
        "facts": [
            "ADHD is a neurodevelopmental condition affecting attention, "
            "executive function, and impulse control.",
            "ADHD brains have differences in dopamine regulation, which makes "
            "tasks that aren't immediately stimulating very hard to start.",
            "Forgetting homework, losing things, and 'zoning out' are symptoms "
            "of ADHD — not signs of laziness or disrespect.",
            "Students with ADHD often hyper-focus on topics they love. The "
            "issue is not lack of attention — it's difficulty regulating it.",
        ],
        "strategies": [
            "Break instructions into small steps and write them on the board "
            "so they don't have to hold everything in working memory.",
            "Seat Maya near the front with minimal distractions — but not in "
            "a way that singles her out.",
            "Use a private check-in system (a sticky note, a hand signal) "
            "rather than calling her out in front of peers.",
        ],
        "mistakes": [
            "Labeling the student as 'lazy' or 'not trying.'",
            "Using public shame as a behavior correction tool.",
            "Removing recess or movement breaks as punishment — students "
            "with ADHD need MORE movement, not less.",
        ],
        "quiz": [
            {
                "question": "A student frequently forgets homework. The "
                            "MOST helpful response is:",
                "options": [
                    "Deduct points until they remember.",
                    "Set up a simple checklist system and check in privately.",
                    "Call their parents in front of the class.",
                ],
                "correct": 1,
            },
            {
                "question": "Why does an ADHD student struggle with long, "
                            "verbal instructions?",
                "options": [
                    "They are not listening on purpose.",
                    "Working memory and sustained attention are affected by ADHD.",
                    "They don't understand the words.",
                ],
                "correct": 1,
            },
            {
                "question": "True or false: removing recess is an effective "
                            "consequence for an ADHD student.",
                "options": [
                    "True — it teaches focus.",
                    "False — students with ADHD need more movement, not less.",
                    "It depends on the day.",
                ],
                "correct": 1,
            },
        ],
    },
}


class TeacherModule:
    """
    The educator-facing screen. Opens with a character picker, then shows
    the detailed teacher content for the chosen character.
    """

    def __init__(self, root, state):
        self.root = root
        self.state = state

        self.current_character = None
        self.quiz_index = 0
        self.quiz_correct = 0

        # Holds the currently active scrollable canvas so the mousewheel
        # handler knows which canvas to scroll.
        self._active_canvas = None

        self._show_picker()

    # ------------------------------------------------------------------
    # Mousewheel scrolling helpers
    # ------------------------------------------------------------------

    def _on_mousewheel(self, event):
        """Scroll the active canvas when the user uses the mouse wheel."""
        if self._active_canvas:
            self._active_canvas.yview_scroll(
                int(-1 * (event.delta / 120)), "units")

    def _enable_scroll(self, canvas):
        """Start listening for mousewheel events on this canvas."""
        self._active_canvas = canvas
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)

    def _disable_scroll(self):
        """Stop the mousewheel listener when leaving a scrollable screen."""
        self._active_canvas = None
        self.root.unbind_all("<MouseWheel>")

    # ------------------------------------------------------------------
    # Picker — choose which character to learn about
    # ------------------------------------------------------------------

    def _show_picker(self):
        """Let the teacher pick which student's material to view."""

        self._disable_scroll()

        for widget in self.root.winfo_children():
            widget.destroy()

        # NAVY header banner — brand color for the educator side.
        banner = tk.Frame(self.root, bg=NAVY, height=110)
        banner.pack(fill="x")
        banner.pack_propagate(False)

        tk.Label(
            banner,
            text="👩‍🏫  Teacher Module",
            font=get_font(22, "bold"),
            bg=NAVY,
            fg=WHITE,
        ).pack(pady=(25, 0))

        tk.Label(
            banner,
            text="Evidence-based micro-learning for educators",
            font=get_font(12),
            bg=NAVY,
            fg="#A9BBD8",
        ).pack()

        # Dark body.
        body = tk.Frame(self.root, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=40, pady=20)

        tk.Label(
            body,
            text="Choose a student to learn about:",
            font=get_font(14, "bold"),
            bg=BG_DARK,
            fg=TEXT_PRIMARY,
        ).pack(pady=(10, 20))

        # Two character buttons side by side — styled like mini cards.
        button_row = tk.Frame(body, bg=BG_DARK)
        button_row.pack()

        tk.Button(
            button_row,
            text="😊  Alex\nTourette Syndrome",
            font=get_font(13, "bold"),
            bg=ALEX_COLOR, fg=WHITE,
            activebackground=WHITE, activeforeground=ALEX_COLOR,
            relief="flat",
            padx=30, pady=20,
            cursor="hand2",
            width=18,
            command=lambda: self._show_content("alex"),
        ).grid(row=0, column=0, padx=15)

        tk.Button(
            button_row,
            text="🌈  Maya\nADHD",
            font=get_font(13, "bold"),
            bg=MAYA_COLOR, fg=WHITE,
            activebackground=WHITE, activeforeground=MAYA_COLOR,
            relief="flat",
            padx=30, pady=20,
            cursor="hand2",
            width=18,
            command=lambda: self._show_content("maya"),
        ).grid(row=0, column=1, padx=15)

        # Back-to-home button — muted, at the bottom.
        tk.Button(
            body,
            text="🏠  Back to Home",
            font=get_font(11),
            bg=PANEL_DARK, fg=TEXT_MUTED,
            activebackground=BORDER_SUBTLE, activeforeground=TEXT_SECONDARY,
            relief="flat",
            padx=14, pady=6,
            cursor="hand2",
            command=self._return_home,
        ).pack(pady=30)

    # ------------------------------------------------------------------
    # Main teacher content for one character
    # ------------------------------------------------------------------

    def _show_content(self, character_key):
        """Show facts, strategies, and mistakes for one character."""

        self.current_character = character_key
        content = TEACHER_CONTENT[character_key]

        for widget in self.root.winfo_children():
            widget.destroy()

        # Banner in this character's accent color.
        banner = tk.Frame(self.root, bg=content["color"], height=90)
        banner.pack(fill="x")
        banner.pack_propagate(False)

        tk.Label(
            banner,
            text=f"Teaching students with {content['condition']}",
            font=get_font(18, "bold"),
            bg=content["color"],
            fg=WHITE,
        ).pack(pady=25)

        # Canvas + Scrollbar so the long content can be scrolled.
        scrollbar = tk.Scrollbar(self.root, orient="vertical")
        canvas = tk.Canvas(
            self.root,
            bg=BG_DARK,
            highlightthickness=0,
            yscrollcommand=scrollbar.set,
        )
        scrollbar.config(command=canvas.yview)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scroll_frame = tk.Frame(canvas, bg=BG_DARK)

        def _update_scrollregion(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scroll_frame.bind("<Configure>", _update_scrollregion)

        canvas_window = canvas.create_window((0, 0), window=scroll_frame,
                                             anchor="nw")

        def _on_canvas_resize(event):
            canvas.itemconfig(canvas_window, width=event.width)

        canvas.bind("<Configure>", _on_canvas_resize)

        self._enable_scroll(canvas)

        # Content sections — each in its own dark panel.
        self._add_section(scroll_frame, "🧠  The science (in simple terms)",
                          content["facts"], content["color"])
        self._add_section(scroll_frame, "✅  Three classroom strategies",
                          content["strategies"], content["color"])
        self._add_section(scroll_frame, "⚠️  Common mistakes to avoid",
                          content["mistakes"], content["color"])

        # Buttons at the bottom.
        button_row = tk.Frame(scroll_frame, bg=BG_DARK)
        button_row.pack(pady=20)

        tk.Button(
            button_row,
            text="📝  Take the quick quiz",
            font=get_font(12, "bold"),
            bg=content["color"], fg=WHITE,
            activebackground=WHITE, activeforeground=content["color"],
            relief="flat",
            padx=20, pady=10,
            cursor="hand2",
            command=self._start_quiz,
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_row,
            text="⬅  Choose another student",
            font=get_font(11),
            bg=PANEL_DARK, fg=TEXT_SECONDARY,
            activebackground=BORDER_SUBTLE, activeforeground=TEXT_PRIMARY,
            relief="flat",
            padx=14, pady=8,
            cursor="hand2",
            command=self._show_picker,
        ).grid(row=0, column=1, padx=10)

    def _add_section(self, parent, title, items, color):
        """One titled section: accent heading + dark item cards."""

        tk.Label(
            parent,
            text=title,
            font=get_font(15, "bold"),
            bg=BG_DARK,
            fg=color,
            anchor="w",
        ).pack(fill="x", padx=20, pady=(15, 5))

        for item in items:
            card = tk.Frame(
                parent,
                bg=PANEL_DARK,
                highlightthickness=1,
                highlightbackground=BORDER_SUBTLE,
            )
            card.pack(fill="x", padx=20, pady=4)

            tk.Message(
                card,
                text=f"•  {item}",
                font=get_font(12),
                bg=PANEL_DARK,
                fg=TEXT_PRIMARY,
                width=780,
                justify="left",
            ).pack(padx=12, pady=8, anchor="w")

    # ------------------------------------------------------------------
    # The 3-question quiz
    # ------------------------------------------------------------------

    def _start_quiz(self):
        """Reset quiz progress and show the first question."""
        self._disable_scroll()
        self.quiz_index = 0
        self.quiz_correct = 0
        self._show_quiz_question()

    def _show_quiz_question(self):
        """Show the current quiz question, or the results if done."""

        content = TEACHER_CONTENT[self.current_character]
        questions = content["quiz"]

        if self.quiz_index >= len(questions):
            self._show_quiz_results()
            return

        question = questions[self.quiz_index]

        for widget in self.root.winfo_children():
            widget.destroy()

        # Banner.
        banner = tk.Frame(self.root, bg=content["color"], height=80)
        banner.pack(fill="x")
        banner.pack_propagate(False)

        tk.Label(
            banner,
            text="📝  Quick Quiz",
            font=get_font(16, "bold"),
            bg=content["color"],
            fg=WHITE,
        ).pack(pady=22)

        # Body.
        body = tk.Frame(self.root, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=40, pady=20)

        # Progress line in muted text.
        tk.Label(
            body,
            text=f"Question {self.quiz_index + 1} of {len(questions)}",
            font=get_font(11),
            bg=BG_DARK,
            fg=TEXT_MUTED,
        ).pack(pady=(0, 6))

        tk.Message(
            body,
            text=question["question"],
            font=get_font(14, "bold"),
            bg=BG_DARK,
            fg=TEXT_PRIMARY,
            width=720,
            justify="left",
        ).pack(pady=(4, 20))

        # One tinted button per option — same pattern as story choices.
        for index, option in enumerate(question["options"]):
            text_color, bg_color = CHOICE_COLORS[index % 4]
            tk.Button(
                body,
                text=option,
                font=get_font(12),
                bg=bg_color,
                fg=text_color,
                relief="flat",
                bd=0,
                anchor="w",
                wraplength=720,
                justify="left",
                padx=16,
                pady=12,
                cursor="hand2",
                activebackground=text_color,
                activeforeground=WHITE,
                command=lambda i=index: self._submit_quiz_answer(i),
            ).pack(fill="x", pady=5)

    def _submit_quiz_answer(self, chosen_index):
        """Check the answer, show feedback, move to the next question."""

        content = TEACHER_CONTENT[self.current_character]
        question = content["quiz"][self.quiz_index]
        correct_index = question["correct"]

        if chosen_index == correct_index:
            self.quiz_correct += 1
            messagebox.showinfo("Correct!", "✅  Great answer.")
        else:
            correct_text = question["options"][correct_index]
            messagebox.showinfo(
                "Not quite",
                f"❌  The best answer was:\n\n{correct_text}",
            )

        self.quiz_index += 1
        self._show_quiz_question()

    def _show_quiz_results(self):
        """Show the score and offer to retake or go back."""

        content = TEACHER_CONTENT[self.current_character]
        total = len(content["quiz"])

        for widget in self.root.winfo_children():
            widget.destroy()

        banner = tk.Frame(self.root, bg=content["color"], height=110)
        banner.pack(fill="x")
        banner.pack_propagate(False)

        tk.Label(
            banner,
            text="🎓  Quiz complete!",
            font=get_font(22, "bold"),
            bg=content["color"],
            fg=WHITE,
        ).pack(pady=35)

        body = tk.Frame(self.root, bg=BG_DARK)
        body.pack(fill="both", expand=True, padx=40, pady=20)

        # Score in gold — rewards are always gold in this brand.
        tk.Label(
            body,
            text=f"You scored {self.quiz_correct} out of {total}.",
            font=get_font(18, "bold"),
            bg=BG_DARK,
            fg=GOLD,
        ).pack(pady=15)

        if self.quiz_correct == total:
            message = "You're ready to support this student with confidence."
        elif self.quiz_correct >= total / 2:
            message = "Great progress! Review the strategies above for next time."
        else:
            message = "No worries — try reviewing the content and retake the quiz."

        tk.Label(
            body,
            text=message,
            font=get_font(13),
            bg=BG_DARK,
            fg=TEXT_SECONDARY,
        ).pack(pady=10)

        # Buttons to retake or finish.
        button_row = tk.Frame(body, bg=BG_DARK)
        button_row.pack(pady=25)

        tk.Button(
            button_row,
            text="🔁  Retake quiz",
            font=get_font(12),
            bg=content["color"], fg=WHITE,
            activebackground=WHITE, activeforeground=content["color"],
            relief="flat",
            padx=16, pady=8,
            cursor="hand2",
            command=self._start_quiz,
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            button_row,
            text="📚  Back to content",
            font=get_font(12),
            bg=PANEL_DARK, fg=TEXT_SECONDARY,
            activebackground=BORDER_SUBTLE, activeforeground=TEXT_PRIMARY,
            relief="flat",
            padx=16, pady=8,
            cursor="hand2",
            command=lambda: self._show_content(self.current_character),
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            button_row,
            text="🏠  Home",
            font=get_font(12),
            bg=PANEL_DARK, fg=TEXT_SECONDARY,
            activebackground=BORDER_SUBTLE, activeforeground=TEXT_PRIMARY,
            relief="flat",
            padx=16, pady=8,
            cursor="hand2",
            command=self._return_home,
        ).grid(row=0, column=2, padx=10)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def _return_home(self):
        """Go back to the character select screen."""
        self._disable_scroll()
        from character_select import CharacterSelectScreen
        CharacterSelectScreen(self.root, self.state)
