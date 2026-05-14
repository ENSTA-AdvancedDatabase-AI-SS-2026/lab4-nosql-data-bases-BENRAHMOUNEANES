MATCH (n) DETACH DELETE n;

// Constraints
CREATE CONSTRAINT e_id IF NOT EXISTS FOR (e:Student) REQUIRE e.id IS UNIQUE;

// Core Data
UNWIND ["Python", "NoSQL", "AI", "Cloud"] AS skill
MERGE (:Skill {name: skill});

UNWIND [
  {id: "S1", name: "Anes", uni: "USTHB"},
  {id: "S2", name: "Amine", uni: "USTHB"},
  {id: "S3", name: "Sarah", uni: "UMBB"},
  {id: "S4", name: "Rami", uni: "USTO"}
] AS s
MERGE (:Student {id: s.id, name: s.name, university: s.uni});

// Relations
MATCH (s1:Student {id: "S1"}), (s2:Student {id: "S2"}) MERGE (s1)-[:FRIEND]-(s2);
MATCH (s2:Student {id: "S2"}), (s3:Student {id: "S3"}) MERGE (s2)-[:FRIEND]-(s3);
MATCH (s3:Student {id: "S3"}), (s4:Student {id: "S4"}) MERGE (s3)-[:FRIEND]-(s4);

MERGE (c:Course {name: "Big Data", code: "CS101"});

MATCH (s:Student {university: "USTHB"}), (c:Course {code: "CS101"})
MERGE (s)-[:ENROLLED {grade: 15}]->(c);

MATCH (s:Student {id: "S1"}), (sk:Skill {name: "Python"})
MERGE (s)-[:KNOWS {level: "Expert"}]->(sk);
