from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


OUT = Path(__file__).resolve().parent


def box(ax, x, y, w, h, text, face, edge="#333333", fontsize=9):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=1.2,
        edgecolor=edge,
        facecolor=face,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize)


def arrow(ax, start, end, color="#444444", style="-"):
    patch = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=12,
        linewidth=1.3,
        linestyle=style,
        color=color,
    )
    ax.add_patch(patch)


fig, ax = plt.subplots(figsize=(6.9, 3.8))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

blue = "#D9EAF7"
orange = "#FCE3D2"
teal = "#D8F0EA"
grey = "#EEEEEE"
red = "#F7D7D7"

box(ax, 0.03, 0.66, 0.18, 0.19, "Honest sender\n(enrolled edge)", blue)
box(ax, 0.03, 0.22, 0.18, 0.22, "External identity\nfalse option + claimed\npositive relation", orange)
box(ax, 0.30, 0.45, 0.21, 0.25, "Receiver-side verifier\nchecks sender, receiver,\nrelation, and step nonce", teal)

arrow(ax, (0.21, 0.755), (0.30, 0.61))
arrow(ax, (0.21, 0.33), (0.30, 0.52))
label_bg = dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none", alpha=0.92)
ax.text(0.255, 0.80, "valid token", ha="center", fontsize=8, color="#365C8D", bbox=label_bg)
ax.text(0.255, 0.41, "missing/invalid", ha="center", fontsize=8, color="#A33A1F", bbox=label_bg)

box(ax, 0.60, 0.70, 0.35, 0.18, "none\nTrust claimed relation; route to positive inbox", grey)
box(ax, 0.60, 0.41, 0.35, 0.18, "downgrade\nRetain content; route to unknown-relation inbox", "#FFF3C4")
box(ax, 0.60, 0.12, 0.35, 0.18, "drop\nDiscard unauthenticated message", red)

arrow(ax, (0.51, 0.62), (0.60, 0.78), color="#666666")
arrow(ax, (0.51, 0.57), (0.60, 0.50), color="#B38300")
arrow(ax, (0.51, 0.51), (0.60, 0.21), color="#A33A1F")

ax.text(0.50, 0.95, "Credential decision occurs before LLM deliberation", ha="center", fontsize=11, weight="bold")
ax.text(0.775, 0.035, "Routing policy controls provenance, not message truth", ha="center", fontsize=8.5)

fig.tight_layout(pad=0.4)
fig.savefig(OUT / "threat_model.png", dpi=300, bbox_inches="tight")
fig.savefig(OUT / "threat_model.pdf", bbox_inches="tight")
