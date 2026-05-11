// 2.1 Trouver tous les amis d'Ahmed (1 saut)
MATCH (ahmed:Etudiant {prenom: "Ahmed"})-[:CONNAIT]-(ami)
RETURN ami.prenom, ami.nom;

// 2.2 Trouver les amis d'amis d'Ahmed qui ne sont pas déjà ses amis
MATCH (ahmed:Etudiant {prenom: "Ahmed"})-[:CONNAIT*2]-(ami_d_ami)
WHERE NOT (ahmed)-[:CONNAIT]-(ami_d_ami) AND ahmed <> ami_d_ami
RETURN ami_d_ami.prenom, ami_d_ami.nom;

// 2.3 Étudiants qui suivent le même cours que Fatima mais ne la connaissent pas
MATCH (fatima:Etudiant {prenom: "Fatima"})-[:SUIT]->(c:Cours)<-[:SUIT]-(autre:Etudiant)
WHERE NOT (fatima)-[:CONNAIT]-(autre) AND fatima <> autre
RETURN autre.prenom, c.intitule;

// 2.4 Clubs les plus populaires (par nombre de membres)
MATCH (e:Etudiant)-[:MEMBRE_DE]->(c:Club)
RETURN c.nom, count(e) as membres
ORDER BY membres DESC
LIMIT 5;

// 2.5 Profil complet d'un étudiant : amis, cours, compétences, clubs
MATCH (e:Etudiant {prenom: "Ahmed"})
OPTIONAL MATCH (e)-[:CONNAIT]-(ami)
OPTIONAL MATCH (e)-[:SUIT]->(cours)
OPTIONAL MATCH (e)-[:MAITRISE]->(comp)
OPTIONAL MATCH (e)-[:MEMBRE_DE]->(club)
RETURN e.prenom, 
       collect(DISTINCT ami.prenom) AS amis, 
       collect(DISTINCT cours.intitule) AS cours, 
       collect(DISTINCT comp.nom) AS competences, 
       collect(DISTINCT club.nom) AS clubs;
