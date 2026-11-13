"""Figure 1: threat model and credential-routing paths.

Layout rules: every label sits inside its box with padding, arrows start and
end on box edges, and arrow labels sit in the empty gutter between columns.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT = Path(__file__).resolve().parent

BLUE = "#D9EAF7"
ORANGE = "#FCE3D2"
TEAL = "#D8F0EA"
GREY = "#EEEEEE"
YELLOW = "#FFF3C4"
RED = "#F7D7D7"
EDGE = "#333333"


def box(ax, x, y, w, h, face, title, body=None, size=9):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.0,rounding_size=0.018",
        linewidth=1.1, edgecolor=EDGE, facecolor=face,
    ))
    cx, cy = x + w / 2, y + h / 2
    if body is None:
        ax.text(cx, cy, title, ha="center", va="center", fontsize=size, linespacing=1.3)
    else:
        ax.text(cx, cy + 0.035, title, ha="center", va="center", fontsize=9.5,
                weight="bold", family="monospace")
        ax.text(cx, cy - 0.03, body, ha="center", va="center", fontsize=8,
                linespacing=1.3)


def arrow(ax, start, end, color="#444444"):
    ax.add_patch(FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=11,
        linewidth=1.3, color=color, shrinkA=0, shrinkB=1,
    ))


def label(ax, x, y, text, color):
    ax.text(x, y, text, ha="center", va="center", fontsize=7.8, color=color,
            linespacing=1.15,
            bbox=dict(boxstyle="round,pad=0.18", facecolor="white",
                      edgecolor="none", alpha=0.95))


fig, ax = plt.subplots(figsize=(7.4, 4.1))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# Column geometry
LX, LW = 0.01, 0.20          # senders
VX, VW = 0.335, 0.27         # verifier
RX, RW = 0.705, 0.285        # policies

# Senders
box(ax, LX, 0.60, LW, 0.20, BLUE, "Honest sender\n(enrolled edge)")
box(ax, LX, 0.17, LW, 0.25, ORANGE, "External sender\nfalse option +\nclaimed positive\nrelation")

# Verifier
box(ax, VX, 0.37, VW, 0.28, TEAL,
    "Receiver-side verifier\nchecks HMAC token\nfor sender, receiver,\nand relation", size=8.5)

# Policies
box(ax, RX, 0.69, RW, 0.18, GREY, "none", "Trust claimed relation;\nroute to positive inbox")
box(ax, RX, 0.41, RW, 0.18, YELLOW, "downgrade", "Retain content; route to\nunverified-source inbox")
box(ax, RX, 0.13, RW, 0.18, RED, "drop", "Discard message before\nprompt construction")

# Sender -> verifier
arrow(ax, (LX + LW, 0.70), (VX, 0.58))
arrow(ax, (LX + LW, 0.295), (VX, 0.44))
label(ax, 0.278, 0.745, "valid token", "#365C8D")
label(ax, 0.29, 0.255, "missing token", "#A33A1F")

# Verifier -> policies (untokened traffic)
arrow(ax, (VX + VW, 0.60), (RX, 0.78), color="#666666")
arrow(ax, (VX + VW, 0.51), (RX, 0.50), color="#B38300")
arrow(ax, (VX + VW, 0.42), (RX, 0.22), color="#A33A1F")
ax.text(VX + VW / 2, 0.325, "untokened traffic follows\none of three policies", ha="center", va="center",
        fontsize=7.8, color="#555555", linespacing=1.2)

ax.text(0.5, 0.965, "Credential decision occurs before LLM deliberation",
        ha="center", va="center", fontsize=11, weight="bold")
ax.text(0.5, 0.045, "Routing policy controls provenance, not message truth",
        ha="center", va="center", fontsize=8.5, style="italic", color="#444444")

fig.savefig(OUT / "threat_model.png", dpi=300, bbox_inches="tight", pad_inches=0.05)
fig.savefig(OUT / "threat_model.pdf", bbox_inches="tight", pad_inches=0.05)
