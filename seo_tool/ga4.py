"""Google Analytics 4: organisch verkeer per landingspagina."""

from __future__ import annotations

from .google_auth import get_credentials


def landing_pages(property_id: str, start: str, end: str, limit: int = 1000, organic_only: bool = True) -> list[dict]:
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        DateRange,
        Dimension,
        Filter,
        FilterExpression,
        Metric,
        OrderBy,
        RunReportRequest,
    )

    client = BetaAnalyticsDataClient(credentials=get_credentials())
    metrics = ["sessions", "engagedSessions", "keyEvents", "totalRevenue"]
    req = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[DateRange(start_date=start, end_date=end)],
        dimensions=[Dimension(name="landingPagePlusQueryString")],
        metrics=[Metric(name=m) for m in metrics],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="sessions"), desc=True)],
        limit=limit,
    )
    if organic_only:
        req.dimension_filter = FilterExpression(
            filter=Filter(
                field_name="sessionDefaultChannelGroup",
                string_filter=Filter.StringFilter(value="Organic Search"),
            )
        )
    resp = client.run_report(req)
    rows = []
    for r in resp.rows:
        row = {"landing_page": r.dimension_values[0].value}
        for name, v in zip(metrics, r.metric_values):
            row[name] = float(v.value) if "." in v.value else int(v.value)
        rows.append(row)
    return rows
