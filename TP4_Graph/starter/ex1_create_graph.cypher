// TP4 - Exercice 1 : Création du graphe UniConnect DZ
MATCH (n) DETACH DELETE n;

CREATE CONSTRAINT etudiant_id IF NOT EXISTS FOR (e:Etudiant) REQUIRE e.id IS UNIQUE;
CREATE CONSTRAINT cours_code IF NOT EXISTS FOR (c:Cours) REQUIRE c.code IS UNIQUE;
CREATE CONSTRAINT competence_nom IF NOT EXISTS FOR (c:Competence) REQUIRE c.nom IS UNIQUE;

UNWIND [
  {nom: "Python", categorie: "Programmation"},
  {nom: "Java", categorie: "Programmation"},
  {nom: "SQL", categorie: "Bases de Données"},
  {nom: "NoSQL", categorie: "Bases de Données"},
  {nom: "Machine Learning", categorie: "IA"},
  {nom: "Deep Learning", categorie: "IA"},
  {nom: "React", categorie: "Web"},
  {nom: "Docker", categorie: "DevOps"},
  {nom: "Linux", categorie: "Systèmes"},
  {nom: "Réseaux", categorie: "Infrastructure"}
] AS comp
MERGE (:Competence {nom: comp.nom, categorie: comp.categorie});

UNWIND [
  {code: "INFO401", intitule: "Bases de Données Avancées", credits: 6, dept: "Informatique"},
  {code: "INFO402", intitule: "Intelligence Artificielle", credits: 6, dept: "Informatique"},
  {code: "INFO403", intitule: "Développement Web", credits: 4, dept: "Informatique"},
  {code: "INFO404", intitule: "Systèmes Distribués", credits: 5, dept: "Informatique"},
  {code: "INFO405", intitule: "Cloud Computing", credits: 4, dept: "Informatique"}
] AS cours
MERGE (:Cours {code: cours.code, intitule: cours.intitule, 
               credits: cours.credits, departement: cours.dept});

UNWIND [
  {id: "E001", prenom: "Ahmed", nom: "Bensalem", universite: "USTHB", filiere: "Informatique", annee: 3, ville: "Alger"},
  {id: "E002", prenom: "Fatima", nom: "Ouali", universite: "USTHB", filiere: "Informatique", annee: 3, ville: "Alger"},
  {id: "E003", prenom: "Youssef", nom: "Zitouni", universite: "UMBB", filiere: "Electronique", annee: 2, ville: "Boumerdes"},
  {id: "E004", prenom: "Yasmina", nom: "Kaddour", universite: "USTO", filiere: "Informatique", annee: 1, ville: "Oran"}
] AS data
MERGE (e:Etudiant {id: data.id})
SET e += data;

// Since I am keeping this simple for the sake of completion:
MATCH (a:Etudiant), (b:Etudiant) WHERE a.id <> b.id AND a.universite = b.universite
MERGE (a)-[:CONNAIT {depuis: 2023}]->(b);

MATCH (a:Etudiant {id: "E001"}), (b:Etudiant {id: "E003"}) MERGE (a)-[:CONNAIT {depuis: 2022}]->(b);
MATCH (a:Etudiant {id: "E003"}), (b:Etudiant {id: "E004"}) MERGE (a)-[:CONNAIT {depuis: 2024}]->(b);

MATCH (e:Etudiant {id: "E001"}), (c:Cours {code: "INFO401"}) MERGE (e)-[:SUIT {semestre: 5, note: 15}]->(c);
MATCH (e:Etudiant {id: "E002"}), (c:Cours {code: "INFO401"}) MERGE (e)-[:SUIT {semestre: 5, note: 16}]->(c);
MATCH (e:Etudiant {id: "E001"}), (c:Competence {nom: "Python"}) MERGE (e)-[:MAITRISE {niveau: "Avancé"}]->(c);

MATCH (n) RETURN labels(n)[0] AS type, count(n) AS total ORDER BY total DESC;
MATCH ()-[r]->() RETURN type(r) AS relation, count(r) AS total ORDER BY total DESC;
