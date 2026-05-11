MATCH p = shortestPath(
  (a:Etudiant {prenom: "Ahmed"})-[:CONNAIT*..10]-(b:Etudiant {prenom: "Yasmina"})
)
RETURN [n IN nodes(p) | CASE WHEN n:Etudiant THEN n.prenom + " (" + n.universite + ")" ELSE "Unknown" END] AS chemin,
       length(p) AS nb_intermediaires;

CALL gds.graph.project(
  'reseau_social',
  'Etudiant',
  'CONNAIT'
);

CALL gds.degree.stream('reseau_social')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).prenom AS etudiant,
       gds.util.asNode(nodeId).universite AS universite,
       score AS nb_connexions
ORDER BY score DESC
LIMIT 10;

CALL gds.louvain.stream('reseau_social')
YIELD nodeId, communityId
WITH communityId, collect(gds.util.asNode(nodeId).prenom) AS membres
RETURN communityId,
       size(membres) AS taille,
       membres[0..5] AS exemple_membres
ORDER BY taille DESC;

MATCH (moi:Etudiant {prenom: "Ahmed"})-[:CONNAIT*2]-(suggestion:Etudiant)
WHERE NOT (moi)-[:CONNAIT]-(suggestion) AND moi <> suggestion
OPTIONAL MATCH (moi)-[:SUIT]->(c:Cours)<-[:SUIT]-(suggestion)
WITH moi, suggestion, count(DISTINCT c) AS cours_communs
OPTIONAL MATCH (moi)-[:CONNAIT]-(ami)-[:CONNAIT]-(suggestion)
WITH suggestion, cours_communs, count(DISTINCT ami) AS amis_communs,
     CASE WHEN moi.filiere = suggestion.filiere THEN 1 ELSE 0 END AS meme_filiere
WITH suggestion, (amis_communs * 3 + cours_communs * 2 + meme_filiere) AS score
RETURN suggestion.prenom AS suggestion, score
ORDER BY score DESC
LIMIT 5;

MATCH path = (debut:Cours)-[:REQUIERT*]->(but:Competence {nom: "Machine Learning"})
RETURN [n IN nodes(path) | CASE WHEN n:Cours THEN n.intitule ELSE n.nom END] AS parcours_apprentissage;

CALL gds.graph.drop('reseau_social');
