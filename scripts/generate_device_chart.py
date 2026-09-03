"""Generate the portfolio-ready device conversion chart."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter


DEVICES = ["Mobile", "Desktop", "Tablet"]
RATES = [7.46, 7.00, 6.72]
VIEWERS = [24_810, 36_323, 1_443]


def main() -> None:
    output = Path(__file__).resolve().parents[1] / "charts" / "device-conversion.png"

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(9.5, 5.8), dpi=160)
    colors = ["#1a73e8", "#5f9fea", "#a8c7fa"]
    bars = ax.bar(DEVICES, RATES, color=colors, width=0.58)

    for bar, rate, viewers in zip(bars, RATES, VIEWERS, strict=True):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            rate + 0.12,
            f"{rate:.2f}%",
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight="semibold",
            color="#202124",
        )
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            rate / 2,
            f"{viewers:,}\nviewers",
            ha="center",
            va="center",
            fontsize=9.5,
            color="white" if bar is not bars[2] else "#202124",
            fontweight="semibold",
        )

    ax.set_title(
        "Product Viewer-to-Purchase Rate by Device",
        loc="left",
        fontsize=17,
        fontweight="bold",
        color="#202124",
        pad=18,
    )
    ax.text(
        0,
        1.01,
        "Mobile leads by 0.46 percentage points; tablet has a much smaller sample",
        transform=ax.transAxes,
        fontsize=10,
        color="#5f6368",
    )
    ax.set_ylabel("Viewer-to-purchase rate", color="#3c4043", labelpad=10)
    ax.set_xlabel("Device category", color="#3c4043", labelpad=10)
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
    ax.set_ylim(0, 8.5)
    ax.grid(axis="y", color="#dadce0", linewidth=0.8)
    ax.grid(axis="x", visible=False)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#bdc1c6")
    ax.tick_params(axis="both", colors="#3c4043")

    fig.text(
        0.01,
        0.01,
        "Source: Google GA4 obfuscated ecommerce sample (2020-11-01 to 2021-01-31). "
        "Rates are descriptive and users may overlap across device categories.",
        fontsize=8.5,
        color="#5f6368",
    )
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()
