"""Generate the portfolio-ready traffic acquisition chart."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


CHANNELS = [
    "Google / organic",
    "Direct / none",
    "Data deleted",
    "Store / referral",
    "Other / referral",
    "Other / other",
    "Google / cpc",
    "Other / organic",
]
REVENUE = [95_775, 79_650, 50_064, 46_521, 37_000, 35_470, 9_056, 8_232]
CONVERSION = [1.19, 1.39, 3.79, 2.18, 1.42, 0.98, 0.98, 0.96]


def main() -> None:
    output = Path(__file__).resolve().parents[1] / "charts" / "traffic-acquisition.png"

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(11, 6.8), dpi=160)
    colors = ["#1a73e8", "#188038", "#9aa0a6"] + ["#5f9fea"] * 5
    bars = ax.barh(CHANNELS, REVENUE, color=colors, height=0.62)
    ax.invert_yaxis()

    for bar, revenue, conversion in zip(bars, REVENUE, CONVERSION, strict=True):
        ax.text(
            revenue + 1_500,
            bar.get_y() + bar.get_height() / 2,
            f"${revenue:,.0f}  •  {conversion:.2f}% conversion",
            va="center",
            fontsize=9.5,
            color="#202124",
            fontweight="semibold",
        )

    ax.set_title(
        "Revenue by First-User Acquisition Source",
        loc="left",
        fontsize=18,
        fontweight="bold",
        color="#202124",
        pad=18,
    )
    ax.text(
        0,
        1.01,
        "Google organic leads revenue; obfuscated channels are retained but not actionable",
        transform=ax.transAxes,
        fontsize=10,
        color="#5f6368",
    )
    ax.set_xlabel("Purchase revenue (USD)", color="#3c4043", labelpad=10)
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${int(value / 1000)}K"))
    ax.set_xlim(0, 125_000)
    ax.grid(axis="x", color="#dadce0", linewidth=0.8)
    ax.grid(axis="y", visible=False)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#bdc1c6")
    ax.tick_params(axis="both", colors="#3c4043")

    fig.text(
        0.01,
        0.01,
        "Source: Google GA4 obfuscated ecommerce sample (2020-11-01 to 2021-01-31). "
        "Source/medium is first-user acquisition, not purchase-session attribution.",
        fontsize=8.5,
        color="#5f6368",
    )
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()
