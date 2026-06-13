# 🌟 TicTales: Every Story Matters

> A gamified empathy education game that helps children understand classmates with misunderstood neurological conditions.

**Stanford Code in Place — Final Project**

---

## 📖 What is TicTales?

TicTales is an interactive story game for schools. Players step into the shoes of a classmate and make real choices that affect a child with a misunderstood neurological condition. The goal is to **shift understanding in the people around the child** — not the child themselves.

Each story challenges a common misconception:

| Character | Condition | Misconception it challenges |
|-----------|-----------|-----------------------------|
| 😊 **Alex** | Tourette Syndrome | *"He's doing it for attention"* |
| 🌈 **Maya** | ADHD | *"She's lazy and doesn't try"* |
| ◉ **Dana** | Autism Spectrum | *"She's rude and doesn't want friends"* |

### Two kinds of users
- **Students (ages 8–14)** — play the interactive story quest
- **Teachers** — use the evidence-based micro-learning module with a short quiz

---

## 🎮 How to play

1. **Pick a classmate** on the home screen (Alex, Maya, or Dana).
2. **Read the scene** — a real moment from that child's school day.
3. **Make a choice** — four ways to react. Your choice changes how the child *feels*.
4. **See the outcome** — the consequence plays out.
5. **Learn the science** — a MYTH vs REALITY card plus real facts about the condition.
6. **Reflect** — a question to think about (no right answer).
7. **Earn badges** — make kind choices to collect empathy badges.

Teachers can open the **👩‍🏫 Teacher Module** for classroom strategies, common mistakes, and a 3-question quiz.

---

## 🏆 Scoring & badges

- Each chapter is worth up to **3 empathy points** (best choice = 3).
- Each character has **3 chapters** = up to **9 points**.
- Your total points unlock **rank titles**: Bystander → Helper → Ally → Champion.

**Badges you can earn:**

| Badge | How to earn it |
|-------|----------------|
| 👁️ Kind Observer | Score well in any Chapter 1 |
| 🥗 Lunch Hero | Score well in Maya/Alex Chapter 2 |
| 🫂 Calm Friend | Score well in Dana's Chapter 2 |
| 🤝 Team Player / 🧩 Problem Solver | Score well in a Chapter 3 |
| 🌟 Empathy Star | Get 8–9 / 9 points for a full character |
| 🏆 Tourette Champion | Complete all of Alex's chapters |
| 🎯 ADHD Ally | Complete all of Maya's chapters |
| 💜 Autism Ally | Complete all of Dana's chapters |

Progress saves automatically — close the game and come back any time.

---

## 🚀 Running the game

### Requirements
- **Python 3** (3.8 or newer; developed on 3.14)
- **Tkinter** — included with Python by default (no install needed)
- **Pillow (PIL)** — *optional*, only used to show the logo image. The game runs fine without it.

### Start it

From inside the `tictales` folder:

```bash
python main.py
```

> On some systems the command is `python3 main.py`.

In **VS Code**: open the `tictales` folder, then press `` Ctrl+` `` to open the terminal and run the command above — or right-click `main.py` → *Run Python File in Terminal*.

### Optional: the logo
The header looks for `assets/logo.png`. If the file is missing (or Pillow isn't installed), the game automatically shows a text **"Tic ✦ Tales"** wordmark instead — nothing breaks. To use the image:

```bash
pip install pillow
```
…and save your logo as `assets/logo.png`.

---

## 📁 Project structure

```
tictales/
├── main.py                  # Entry point — opens the window, loads the logo, shows the home screen
├── constants.py             # Brand colors & fonts (the "theme") used everywhere
├── game_state.py            # Tracks points, badges, ranks; saves/loads progress
├── character_select.py      # Home screen with the 3 character cards
├── chapter_engine.py        # Runs every chapter: Intro→Choice→Outcome→Fact→Reflection→Badge
├── alex_story.py            # Alex's story (loads alex_chapters.json)
├── maya_story.py            # Maya's story (loads maya_chapters.json)
├── dana_story.py            # Dana's story (loads dana_chapters.json)
├── teacher_module.py        # Teacher micro-learning screen + quiz
├── data/
│   ├── alex_chapters.json   # Alex's story content (text, choices, facts)
│   ├── maya_chapters.json   # Maya's story content
│   └── dana_chapters.json   # Dana's story content
├── assets/
│   └── logo.png             # (optional) game logo
└── tictales_save.json       # Auto-created — your saved progress
```

### How the pieces fit together
- **`main.py`** builds the window and creates one `GameState`, then hands control to the home screen.
- **`character_select.py`** shows the cards. Clicking one launches that character's story file.
- Each **story file** (`alex_story.py`, etc.) loads its JSON and feeds chapters one at a time to **`chapter_engine.py`**, which draws all six screens.
- **`game_state.py`** is passed around so every screen can read/update points and badges, and it writes everything to `tictales_save.json`.
- **`constants.py`** holds all the colors and fonts, so the whole game stays visually consistent.

---

## ✏️ Editing the stories (no coding needed)

All the story text lives in the `data/*.json` files — **you can change the writing without touching any Python.** Each chapter has:

```json
{
  "number": 1,
  "title": "The Classroom Tic",
  "intro": "What's happening in the scene...",
  "question": "What do you do?",
  "choices": [
    { "label": "A", "text": "...", "points": 0, "verdict": "WRONG", "outcome": "..." }
  ],
  "facts": ["A real fact about the condition"],
  "reflection": "A question to think about",
  "badge": "Kind Observer",
  "myth": "The common misconception",
  "reality": "What's actually true"
}
```

- `points`: 0–3 (3 is the kindest choice)
- `verdict`: `"BEST"`, `"OK"`, or `"WRONG"` (controls the color shown)

After editing, just relaunch the game.

---

## 🎨 Design notes

- **Theme:** dark "storybook at night" background for a calm, focused feel.
- **Brand colors** (from the logo) live in `constants.py`: red, navy, and gold.
- **Per-character accent colors:** Alex = teal, Maya = orange, Dana = purple.
- **Tone:** empathetic and child-friendly throughout — no scary or blaming language.
- **Animations:** gentle points count-up, a bouncing badge, and confetti on the badge screen (pure Tkinter, no extra libraries).

---

## 💙 About

TicTales was built to teach empathy, not pity. Every choice is a small lesson that the people *around* a child shape that child's experience far more than the condition itself does.

*Every story matters.*
