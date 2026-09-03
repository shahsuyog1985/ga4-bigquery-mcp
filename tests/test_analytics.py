import pytest

from ga4_bigquery_mcp.analytics import GA4Analytics, validate_date_range


def test_validate_date_range() -> None:
    assert validate_date_range("2020-11-01", "2021-01-31") == ("20201101", "20210131")


@pytest.mark.parametrize(
    "start,end",
    [
        ("2021-01-02", "2021-01-01"),
        ("2020-10-31", "2021-01-01"),
        ("2020-11-01", "2021-02-01"),
        ("not-a-date", "2021-01-01"),
    ],
)
def test_invalid_date_ranges(start: str, end: str) -> None:
    with pytest.raises(ValueError):
        validate_date_range(start, end)


def test_rejects_unsafe_dataset() -> None:
    with pytest.raises(ValueError):
        GA4Analytics(dataset="dataset`; DROP TABLE x; --")

