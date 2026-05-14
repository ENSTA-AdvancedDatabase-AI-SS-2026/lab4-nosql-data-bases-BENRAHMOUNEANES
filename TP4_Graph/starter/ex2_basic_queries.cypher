// 2.1 Direct friends of S1
MATCH (s:Student {id: "S1"})-[:FRIEND]-(f)
RETURN f.name;

// 2.2 Friends of friends (not direct)
MATCH (s:Student {id: "S1"})-[:FRIEND*2]-(fof)
WHERE NOT (s)-[:FRIEND]-(fof) AND s <> fof
RETURN DISTINCT fof.name;

// 2.3 Enrolled in CS101 but not friend of S1
MATCH (c:Course {code: "CS101"})<-[:ENROLLED]-(other)
MATCH (s:Student {id: "S1"})
WHERE NOT (s)-[:FRIEND]-(other) AND s <> other
RETURN other.name;

// 2.4 Top courses
MATCH (c:Course)<-[:ENROLLED]-()
RETURN c.name, count(*) AS count ORDER BY count DESC;
