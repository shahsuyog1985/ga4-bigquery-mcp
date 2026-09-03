-- Measure distinct users who reached each event (not a sequential session funnel).
SELECT
  step,
  users,
  ROUND(
    100 * users / MAX(IF(step = 'view_item', users, NULL)) OVER (),
    2
  ) AS percent_of_product_viewers
FROM (
  SELECT
    event_name AS step,
    COUNT(DISTINCT user_pseudo_id) AS users
  FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
  WHERE event_name IN (
    'view_item',
    'add_to_cart',
    'begin_checkout',
    'add_shipping_info',
    'add_payment_info',
    'purchase'
  )
  GROUP BY event_name
)
ORDER BY CASE step
  WHEN 'view_item' THEN 1
  WHEN 'add_to_cart' THEN 2
  WHEN 'begin_checkout' THEN 3
  WHEN 'add_shipping_info' THEN 4
  WHEN 'add_payment_info' THEN 5
  WHEN 'purchase' THEN 6
END;

