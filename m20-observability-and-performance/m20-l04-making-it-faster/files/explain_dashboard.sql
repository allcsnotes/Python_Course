EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF)
SELECT c.title, c.price, count(*),
       array_agg(s.name ORDER BY s.id)
FROM courses c
JOIN enrollments e ON e.course_id = c.id
JOIN students s ON s.id = e.student_id
WHERE c.owner_id = 1
GROUP BY c.id
ORDER BY c.id;
