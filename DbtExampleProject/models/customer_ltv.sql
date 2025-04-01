WITH revenue AS (
    SELECT * FROM {{ ref('total_revenue_per_customer') }}
),
order_count AS (
    SELECT * FROM {{ ref('order_count_per_customer') }}
)
SELECT 
    r.customer_id,
    r.total_spent,
    o.order_count,
    r.total_spent / NULLIF(o.order_count, 0) AS avg_order_value
FROM revenue r
LEFT JOIN order_count o ON r.customer_id = o.customer_id