-- Establish the sample's coverage, volume, users, and event variety.
SELECT
  MIN(PARSE_DATE('%Y%m%d', event_date)) AS first_date,
  MAX(PARSE_DATE('%Y%m%d', event_date)) AS last_date,
  COUNT(*) AS total_events,
  COUNT(DISTINCT user_pseudo_id) AS unique_users,
  COUNT(DISTINCT event_name) AS event_types
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`;

