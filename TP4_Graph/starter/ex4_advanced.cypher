// 4.1 Trouver un tuteur : Étudiant en Master (année > 3) qui maîtrise Python et a eu >14/20 en BDD
MATCH (e:Etudiant)-[:MAITRISE]->(c1:Competence {nom: "Python"}),
      (e)-[s:SUIT]->(c2:Cours {code: "INFO401"}) // Assuming INFO401 is BDD
WHERE e.annee > 3 AND s.note > 14
RETURN e.prenom, e.nom, s.note;

// 4.2 Réseau alumni dans une entreprise (Sonatrach) jusqu'à 3 sauts
MATCH (moi:Etudiant {prenom: "Ahmed"})-[:CONNAIT*1..3]-(alumni:Etudiant)-[:A_STAGE_CHEZ]->(ent:Entreprise {nom: "Sonatrach"})
RETURN DISTINCT alumni.prenom, alumni.nom;

// 4.3 Détection de ponts
// To find bridge nodes we can use betweenness centrality
CALL gds.graph.project('bridges_graph', 'Etudiant', 'CONNAIT');
CALL gds.betweenness.stream('bridges_graph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).prenom AS etudiant, score
ORDER BY score DESC
LIMIT 5;
CALL gds.graph.drop('bridges_graph');

// 4.4 Croissance du réseau : nouvelles connexions par mois
MATCH ()-[r:CONNAIT]->()
RETURN r.depuis AS annee, count(r) AS nouvelles_connexions
ORDER BY annee;

// 4.5 Score de similarité (Jaccard) avec Ahmed
MATCH (ahmed:Etudiant {prenom: "Ahmed"})-[:SUIT|MEMBRE_DE|MAITRISE]->(item)
WITH ahmed, collect(id(item)) AS ahmed_items
MATCH (autre:Etudiant)-[:SUIT|MEMBRE_DE|MAITRISE]->(item)
WHERE autre <> ahmed
WITH autre, ahmed_items, collect(id(item)) AS autre_items
WITH autre, 
     size(gds.alpha.similarity.intersection(ahmed_items, autre_items)) AS intersection,
     size(ahmed_items) + size(autre_items) - size(gds.alpha.similarity.intersection(ahmed_items, autre_items)) AS union
RETURN autre.prenom, (1.0 * intersection / union) AS jaccard_similarity
ORDER BY jaccard_similarity DESC
LIMIT 5;
