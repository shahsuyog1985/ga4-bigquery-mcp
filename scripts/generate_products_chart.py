"""Generate the portfolio-ready top-products chart."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


PRODUCTS = [
    "Google Zip Hoodie F/C",
    "Google Crewneck Sweatshirt Navy",
    "Google Men's Tech Fleece Grey",
    "Google Badge Heavyweight Pullover Black",
    "Super G Unisex Joggers",
    "Google Crewneck Sweatshirt Green",
    "Google Sherpa Zip Hoodie Charcoal",
    "Google Men's Puff Jacket Black",
    "Google Men's Tech Fleece Vest Charcoal",
    "Google Women's Puff Jacket Black",
]
REVENUE = [13_788, 10_714, 9_965, 9_712, 9_529, 8_382, 6_397, 6_187, 5_549, 5_313]
UNITS = [273, 236, 134, 201, 308, 184, 115, 64, 84, 57]


def main() -> None:
    output = Path(__file__).resolve().parents[1] / "charts" / "top-products.png"

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(11.5, 7.2), dpi=160)
    colors = ["#1a73e8"] + ["#5f9fea"] * 9
    bars = ax.barh(PRODUCTS, REVENUE, color=colors, height=0.62)
    ax.invert_yaxis()

    for bar, revenue, units in zip(bars, REVENUE, UNITS, strict=True):
        ax.text(
            revenue + 180,
            bar.get_y() + bar.get_height() / 2,
            f"${revenue:,.0f}  •  {units} units",
            va="center",
            fontsize=9.5,
            color="#202124",
            fontweight="semibold",
        )

    ax.set_title(
        "Top 10 Products by Purchase Revenue",
        loc="left",
        fontsize=18,
        fontweight="bold",
        color="#202124",
        pad=18,
    )
    ax.text(
        0,
        1.01,
        "Cold-weather apparel dominates during the November–January sample",
        transform=ax.transAxes,
        fontsize=10,
        color="#5f6368",
    )
    ax.set_xlabel("Item revenue (USD)", color="#3c4043", labelpad=10)
    ax.set_ylabel("")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${int(value / 1000)}K"))
    ax.set_xlim(0, 16_500)
    ax.grid(axis="x", color="#dadce0", linewidth=0.8)
    ax.grid(axis="y", visible=False)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#bdc1c6")
    ax.tick_params(axis="both", colors="#3c4043")

    fig.text(
        0.01,
        0.01,
        "Source: Google GA4 obfuscated ecommerce sample (2020-11-01 to 2021-01-31).",
        fontsize=8.5,
        color="#5f6368",
    )
    fig.tight_layout(rect=(0, 0.05, 1, 1))
    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(output)


if __name__ == "__main__":
    main()
