-- Q1: незакрытые P1 обращения
SELECT id, status FROM incidents WHERE priority='P1' AND status <> 'CLOSED' ORDER BY id;
-- Q2: незакрытые обращения без ответственного
SELECT id FROM incidents WHERE assignee IS NULL AND status <> 'CLOSED' ORDER BY id;
-- Q3: обращения с именем продукта
SELECT i.id, p.name FROM incidents i JOIN products p ON p.id=i.product_id WHERE i.status='OPEN' ORDER BY i.id;
-- Q4: число незакрытых обращений по продуктам; учитываются и нулевые значения
SELECT p.name, COUNT(i.id) AS active FROM products p LEFT JOIN incidents i ON i.product_id=p.id AND i.status <> 'CLOSED' GROUP BY p.id, p.name ORDER BY p.id;
-- Q5: повторяющиеся коды серверных ошибок
SELECT error_code, COUNT(*) AS total FROM incidents WHERE error_code >= 500 GROUP BY error_code HAVING COUNT(*) > 1 ORDER BY error_code;
-- Q6: количество закрытых обращений каждого приоритета
SELECT priority, COUNT(*) AS total FROM incidents WHERE status='CLOSED' GROUP BY priority ORDER BY priority;
