"""
constants.py
============
The TicTales brand system, extracted from assets/logo.png.

The logo shows a cartoon boy waving inside a rounded square frame with
a red "!" — and the wordmark "Tic" (bold red) · gold star · "Tales"
(bold navy). Flat cartoon style, thick outlines, rounded everywhere.

Every file imports its colors and fonts from here so the whole game
stays visually consistent. Change a color once — it changes everywhere.
"""

# ----------------------------------------------------------------------
# Core brand (from the logo)
# ----------------------------------------------------------------------
RED         = "#E8352A"   # "Tic" wordmark red — attention, alerts
NAVY        = "#1B3A6B"   # "Tales" wordmark navy — trust, nav, teachers
GOLD        = "#F5A623"   # Star separator dot — points, badges, rewards
WHITE       = "#FFFFFF"
OFF_WHITE   = "#FFF8F0"   # Kept for light text areas if ever needed

# ----------------------------------------------------------------------
# App background (dark, like a storybook at night)
# ----------------------------------------------------------------------
BG_DARK     = "#12112A"   # Main window background
CARD_DARK   = "#1E1C3A"   # Character card backgrounds
PANEL_DARK  = "#252340"   # Chapter panels, fact cards

# ----------------------------------------------------------------------
# Per-character accent colors
# ----------------------------------------------------------------------
ALEX_COLOR  = "#1D9E75"   # Teal green — Tourette
MAYA_COLOR  = "#F5821F"   # Warm orange — ADHD
DANA_COLOR  = "#6C5CE7"   # Soft purple — Autism

# ----------------------------------------------------------------------
# Verdict colors (outcome screen)
# ----------------------------------------------------------------------
COLOR_BEST  = "#27AE60"   # Green — best choice
COLOR_OK    = "#F39C12"   # Amber — okay choice
COLOR_WRONG = "#E8352A"   # Red — poor choice

# ----------------------------------------------------------------------
# UI text + borders
# ----------------------------------------------------------------------
TEXT_PRIMARY   = "#FFFFFF"
TEXT_SECONDARY = "#B0ADCC"
TEXT_MUTED     = "#6B6890"
BORDER_SUBTLE  = "#2E2B50"

# ----------------------------------------------------------------------
# Fonts
# ----------------------------------------------------------------------
# Preferred font families, best first. get_font() picks the first one
# that is actually installed on this computer.
_FONT_FAMILIES = ("Fredoka One", "Arial Rounded MT Bold",
                  "Comic Sans MS", "Arial")

# Cache: we only want to query the installed font list once.
_resolved_family = None


def get_font(size, weight="normal"):
    """
    Return a (family, size, weight) tuple using the best installed font.

    Tries Fredoka One first, then Arial Rounded MT Bold, then
    Comic Sans MS, then plain Arial. The font list can only be read
    after the Tk window exists, so we look it up lazily on first call
    and remember the answer.
    """
    global _resolved_family

    if _resolved_family is None:
        try:
            # tkinter.font.families() needs a running Tk root —
            # by the time any screen calls get_font(), main.py has
            # already created it.
            import tkinter.font as tkfont
            installed = set(tkfont.families())
            for family in _FONT_FAMILIES:
                if family in installed:
                    _resolved_family = family
                    break
            else:
                _resolved_family = "Arial"
        except Exception:
            # If anything goes wrong, just use Arial — always present.
            _resolved_family = "Arial"

    if weight == "bold":
        return (_resolved_family, size, "bold")
    return (_resolved_family, size)


# Ready-made font shortcuts (resolved at call time via get_font).
FONT_HEADING = lambda: get_font(24, "bold")
FONT_BODY    = lambda: get_font(13)
FONT_SMALL   = lambda: get_font(11)
FONT_BUTTON  = lambda: get_font(13, "bold")
