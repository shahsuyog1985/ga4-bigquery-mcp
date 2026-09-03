"""MCP tool definitions for GA4 BigQuery analytics."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from mcp.server import MCPServer

from .analytics import GA4Analytics

mcp = MCPServer("GA4 BigQuery Analytics")


@lru_cache(maxsize=1)
def analytics() -> GA4Analytics:
    return GA4Analytics()


@mcp.tool()
def ecommerce_overview(start_date: str = "2020-11-01", end_date: str = "2021-01-31") -> list[dict[str, Any]]:
    """Return GA4 event, user, purchase, and revenue totals for an inclusive date range."""
    return analytics().overview(start_date, end_date)


@mcp.tool()
def daily_trends(start_date: str = "2020-11-01", end_date: str = "2021-01-31") -> list[dict[str, Any]]:
    """Return daily users, events, purchases, and revenue for an inclusive date range."""
    return analytics().daily_trends(start_date, end_date)


@mcp.tool()
def top_products(
    start_date: str = "2020-11-01", end_date: str = "2021-01-31", limit: int = 10
) -> list[dict[str, Any]]:
    """Return top purchased products ranked by revenue."""
    return analytics().top_products(start_date, end_date, limit)


@mcp.tool()
def traffic_acquisition(
    start_date: str = "2020-11-01", end_date: str = "2021-01-31", limit: int = 20
) -> list[dict[str, Any]]:
    """Return users, purchases, and revenue grouped by first-user source and medium."""
    return analytics().acquisition(start_date, end_date, limit)


@mcp.tool()
def checkout_funnel(start_date: str = "2020-11-01", end_date: str = "2021-01-31") -> list[dict[str, Any]]:
    """Return distinct-user counts across major ecommerce funnel events."""
    return analytics().checkout_funnel(start_date, end_date)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()

