// 3.1 Path between S1 and S4
MATCH p = shortestPath((a:Student {id: "S1"})-[:FRIEND*]-(b:Student {id: "S4"}))
RETURN [n IN nodes(p) | n.name] AS path;

// 3.2 GDS Degree
CALL gds.graph.project('net', 'Student', {FRIEND: {orientation: 'UNDIRECTED'}});
CALL gds.degree.stream('net') YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score AS degree
ORDER BY degree DESC;

// 3.3 Louvain
CALL gds.louvain.stream('net') YIELD nodeId, communityId
RETURN communityId, collect(gds.util.asNode(nodeId).name) AS group
ORDER BY size(group) DESC;

CALL gds.graph.drop('net', false);
