"""BigQuery-backed GA4 ecommerce analytics."""

from __future__ import annotations

import os
import re
from datetime import date
from typing import Any

from google.cloud import bigquery

DEFAULT_DATASET = "bigquery-public-data.ga4_obfuscated_sample_ecommerce"
DEFAULT_MAX_BYTES_BILLED = 2 * 1024**3  # 2 GiB per query
MIN_DATE = date(2020, 11, 1)
MAX_DATE = date(2021, 1, 31)
_DATASET_RE = re.compile(r"^[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+$")


def validate_date_range(start_date: str, end_date: str) -> tuple[str, str]:
    """Validate and convert ISO dates to BigQuery table suffixes."""
    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
    except ValueError as exc:
        raise ValueError("Dates must use YYYY-MM-DD format.") from exc
    if start > end:
        raise ValueError("start_date must be on or before end_date.")
    if start < MIN_DATE or end > MAX_DATE:
        raise ValueError(f"Dates must be between {MIN_DATE} and {MAX_DATE}.")
    return start.strftime("%Y%m%d"), end.strftime("%Y%m%d")


class GA4Analytics:
    """Run safe, predefined analytics against a GA4 BigQuery export."""

    def __init__(self, project: str | None = None, dataset: str | None = None) -> None:
        self.project = project or os.getenv("GOOGLE_CLOUD_PROJECT")
        self.dataset = dataset or os.getenv("GA4_BIGQUERY_DATASET", DEFAULT_DATASET)
        if not _DATASET_RE.fullmatch(self.dataset):
            raise ValueError("Dataset must have the form project.dataset.")
        self.client = bigquery.Client(project=self.project)

    def _run(
        self,
        sql: str,
        start_date: str,
        end_date: str,
        parameters: list[bigquery.ScalarQueryParameter] | None = None,
    ) -> list[dict[str, Any]]:
        start_suffix, end_suffix = validate_date_range(start_date, end_date)
        query_parameters = [
            bigquery.ScalarQueryParameter("start_suffix", "STRING", start_suffix),
            bigquery.ScalarQueryParameter("end_suffix", "STRING", end_suffix),
            *(parameters or []),
        ]
        max_bytes_billed = int(
            os.getenv("BIGQUERY_MAX_BYTES_BILLED", str(DEFAULT_MAX_BYTES_BILLED))
        )
        job_config = bigquery.QueryJobConfig(
            query_parameters=query_parameters,
            maximum_bytes_billed=max_bytes_billed,
        )
        rows = self.client.query(sql, job_config=job_config).result()
        return [dict(row.items()) for row in rows]

    @property
    def tables(self) -> str:
        return f"`{self.dataset}.events_*`"

    def overview(self, start_date: str, end_date: str) -> list[dict[str, Any]]:
        sql = f"""
        SELECT
          COUNT(*) AS events,
          COUNT(DISTINCT user_pseudo_id) AS users,
          COUNT(DISTINCT IF(event_name = 'purchase', event_bundle_sequence_id, NULL)) AS purchases,
          ROUND(SUM(IF(event_name = 'purchase', ecommerce.purchase_revenue_in_usd, 0)), 2) AS revenue_usd
        FROM {self.tables}
        WHERE _TABLE_SUFFIX BETWEEN @start_suffix AND @end_suffix
        """
        return self._run(sql, start_date, end_date)

    def daily_trends(self, start_date: str, end_date: str) -> list[dict[str, Any]]:
        sql = f"""
        SELECT
          PARSE_DATE('%Y%m%d', event_date) AS date,
          COUNT(*) AS events,
          COUNT(DISTINCT user_pseudo_id) AS users,
          COUNTIF(event_name = 'purchase') AS purchases,
          ROUND(SUM(IF(event_name = 'purchase', ecommerce.purchase_revenue_in_usd, 0)), 2) AS revenue_usd
        FROM {self.tables}
        WHERE _TABLE_SUFFIX BETWEEN @start_suffix AND @end_suffix
        GROUP BY date
        ORDER BY date
        """
        return self._run(sql, start_date, end_date)

    def top_products(self, start_date: str, end_date: str, limit: int = 10) -> list[dict[str, Any]]:
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100.")
        sql = f"""
        SELECT
          item.item_name,
          item.item_category,
          SUM(item.quantity) AS units,
          ROUND(SUM(item.item_revenue_in_usd), 2) AS revenue_usd
        FROM {self.tables}, UNNEST(items) AS item
        WHERE _TABLE_SUFFIX BETWEEN @start_suffix AND @end_suffix
          AND event_name = 'purchase'
        GROUP BY item.item_name, item.item_category
        ORDER BY revenue_usd DESC
        LIMIT @limit
        """
        return self._run(
            sql,
            start_date,
            end_date,
            [bigquery.ScalarQueryParameter("limit", "INT64", limit)],
        )

    def acquisition(self, start_date: str, end_date: str, limit: int = 20) -> list[dict[str, Any]]:
        if not 1 <= limit <= 100:
            raise ValueError("limit must be between 1 and 100.")
        sql = f"""
        SELECT
          COALESCE(traffic_source.source, '(direct)') AS source,
          COALESCE(traffic_source.medium, '(none)') AS medium,
          COUNT(DISTINCT user_pseudo_id) AS users,
          COUNTIF(event_name = 'purchase') AS purchases,
          ROUND(SUM(IF(event_name = 'purchase', ecommerce.purchase_revenue_in_usd, 0)), 2) AS revenue_usd
        FROM {self.tables}
        WHERE _TABLE_SUFFIX BETWEEN @start_suffix AND @end_suffix
        GROUP BY source, medium
        ORDER BY users DESC
        LIMIT @limit
        """
        return self._run(
            sql,
            start_date,
            end_date,
            [bigquery.ScalarQueryParameter("limit", "INT64", limit)],
        )

    def checkout_funnel(self, start_date: str, end_date: str) -> list[dict[str, Any]]:
        sql = f"""
        WITH steps AS (
          SELECT 1 AS step_order, 'view_item' AS step UNION ALL
          SELECT 2, 'add_to_cart' UNION ALL
          SELECT 3, 'begin_checkout' UNION ALL
          SELECT 4, 'add_shipping_info' UNION ALL
          SELECT 5, 'add_payment_info' UNION ALL
          SELECT 6, 'purchase'
        ), counts AS (
          SELECT event_name AS step, COUNT(DISTINCT user_pseudo_id) AS users
          FROM {self.tables}
          WHERE _TABLE_SUFFIX BETWEEN @start_suffix AND @end_suffix
            AND event_name IN ('view_item', 'add_to_cart', 'begin_checkout',
                               'add_shipping_info', 'add_payment_info', 'purchase')
          GROUP BY event_name
        )
        SELECT steps.step, COALESCE(counts.users, 0) AS users
        FROM steps LEFT JOIN counts USING (step)
        ORDER BY step_order
        """
        return self._run(sql, start_date, end_date)
