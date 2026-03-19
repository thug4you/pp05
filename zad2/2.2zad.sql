SELECT 
    o.order_code AS "Номер заказа",
    c.name AS "Заказчик",
    o.date AS "Дата оформления",
    
    SUM(oi.quantity * s.quantity * mp.price) AS "Полная себестоимость"

FROM "order" o
JOIN customer c 
  ON o.customer_code = c.customer_code
JOIN order_items oi 
  ON o.order_code = oi.order_code
JOIN specification s 
  ON oi.product_code = s.product_code
JOIN material_price mp 
  ON s.material_code = mp.material_code 
  AND mp.valid_to is NULL

GROUP BY 
    o.order_code, 
    c.name,
    o.date
ORDER BY 
    o.order_code;
