-- Compare product engagement and purchase reach by device category.
SELECT
  device.category AS device_category,
  COUNT(DISTINCT IF(event_name = 'view_item', user_pseudo_id, NULL))
    AS product_viewers,
  COUNT(DISTINCT IF(event_name = 'add_to_cart', user_pseudo_id, NULL))
    AS cart_users,
  COUNT(DISTINCT IF(event_name = 'purchase', user_pseudo_id, NULL))
    AS purchasers,
  ROUND(
    100 * COUNT(DISTINCT IF(event_name = 'purchase', user_pseudo_id, NULL))
    / NULLIF(
        COUNT(DISTINCT IF(event_name = 'view_item', user_pseudo_id, NULL)),
        0
      ),
    2
  ) AS viewer_to_purchase_percent
FROM `bigquery-public-data.ga4_obfuscated_sample_ecommerce.events_*`
WHERE event_name IN ('view_item', 'add_to_cart', 'purchase')
GROUP BY device_category
ORDER BY product_viewers DESC;

