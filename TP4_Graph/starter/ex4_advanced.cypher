// 4.1 Recommendation based on common friends
MATCH (s:Student {id: "S1"}), (other:Student)
WHERE NOT (s)-[:FRIEND]-(other) AND s <> other
MATCH (s)-[:FRIEND]-(f)-[:FRIEND]-(other)
RETURN other.name, count(f) AS common_friends
ORDER BY common_friends DESC LIMIT 3;

// 4.2 High grade in CS101
MATCH (s:Student)-[e:ENROLLED]->(c:Course {code: "CS101"})
WHERE e.grade > 14
RETURN s.name, e.grade;

// 4.3 Similarity using Jaccard (shared courses/skills)
MATCH (s1:Student {id: "S1"})-[:ENROLLED|KNOWS]->(item)
WITH s1, collect(id(item)) AS s1_items
MATCH (s2:Student)-[:ENROLLED|KNOWS]->(item) WHERE s1 <> s2
WITH s1, s1_items, s2, collect(id(item)) AS s2_items
RETURN s2.name, gds.similarity.jaccard(s1_items, s2_items) AS sim
ORDER BY sim DESC LIMIT 5;
