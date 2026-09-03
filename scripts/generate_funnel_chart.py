"""Generate the portfolio-ready ecommerce funnel chart."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


STEPS = [
    "View item",
    "Add to cart",
    "Begin checkout",
    "Shipping info",
    "Payment info",
    "Purchase",
]
USERS = [61_252, 12_545, 9_715, 9_714, 5_751, 4_419]
PERCENT = [100.00, 20.48, 15.86, 15.86, 9.39, 7.21]


def main() -> None:
    output = Path(__file__).resolve().parents[1] / "charts" / "funnel-reach.png"

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=160)
    colors = ["#1a73e8"] + ["#5f9fea"] * 4 + ["#188038"]
    bars = ax.barh(STEPS, USERS, color=colors, height=0.62)
    ax.invert_yaxis()

    for bar, users, percent in zip(bars, USERS, PERCENT, strict=True):
        ax.text(
            bar.get_width() + 900,
            bar.get_y() + bar.get_height() / 2,
            f"{users:,} users  •  {percent:.2f}%",
            va="center",
            fontsize=10,
            color="#202124",
            fontweight="semibold",
        )

    ax.set_title(
        "GA4 Ecommerce Funnel Reach",
        loc="left",
        fontsize=18,
        fontweight="bold",
        color="#202124",
        pad=18,
    )
    ax.text(
        0,
        1.01,
        "Distinct users reaching each event • Share is relative to product viewers",
        transform=ax.transAxes,
        fontsize=10,
        color="#5f6368",
    )
    ax.set_xlabel("Distinct users", color="#3c4043", labelpad=10)
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{int(value / 1000)}K"))
    ax.grid(axis="x", color="#dadce0", linewidth=0.8)
    ax.grid(axis="y", visible=False)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#bdc1c6")
    ax.tick_params(axis="both", colors="#3c4043")
    ax.set_xlim(0, 70_000)

    fig.text(
        0.01,
        0.01,
        "Source: Google GA4 obfuscated ecommerce sample (2020-11-01 to 2021-01-31). "
        "Event reach is not a sequential session funnel.",
        fontsize=8.5,
        color="#5f6368",
    )
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()
