-- Measure the frequency and share of each tracked GA4 event.
SELECT
  event_name,
  COUNT(*) AS event_count,
  ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentage_of_events
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
GROUP BY event_name
ORDER BY event_count DESC;

