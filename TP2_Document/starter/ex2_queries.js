use("medical_db");

// 2.1 Trouver tous les patients diabétiques de plus de 50 ans à Alger
const patientsDiabetiques = db.patients.find({
  "adresse.wilaya": "Alger",
  antecedents: "Diabète type 2",
  dateNaissance: { $lte: new Date(new Date().setFullYear(new Date().getFullYear() - 50)) }
}).toArray();
print("\n=== 2.1 Patients diabétiques > 50 ans à Alger ===");
printjson(patientsDiabetiques);

// 2.2 Patients allergiques à la Pénicilline avec au moins 3 consultations
const patientsPenicilline = db.patients.find({
  allergies: "Pénicilline",
  $expr: { $gte: [{ $size: "$consultations" }, 3] }
}).toArray();
print("\n=== 2.2 Patients allergiques à la Pénicilline avec >= 3 consultations ===");
printjson(patientsPenicilline);

// 2.3 Projection : Nom, prénom, et dernière consultation seulement
const projectionPatients = db.patients.find(
  {},
  { 
    nom: 1, 
    prenom: 1, 
    derniereConsultation: { $arrayElemAt: ["$consultations", -1] }, 
    _id: 0 
  }
).toArray();
print("\n=== 2.3 Projection Nom, Prénom et dernière consultation ===");
printjson(projectionPatients);

// 2.4 Patients sans antécédents dont la tension systolique > 140 en dernière consultation
const patientsTension = db.patients.find({
  $or: [{ antecedents: { $exists: false } }, { antecedents: { $size: 0 } }],
  $expr: {
    $gt: [
      { $let: { vars: { last_consultation: { $arrayElemAt: ["$consultations", -1] } }, in: "$$last_consultation.tension.systolique" } },
      140
    ]
  }
}).toArray();
print("\n=== 2.4 Patients sans antécédents avec tension systolique > 140 ===");
printjson(patientsTension);

// 2.5 Recherche textuelle sur les diagnostics (créer index text d'abord)
db.patients.createIndex({ "consultations.diagnostic": "text" });

const rechercheTexte = db.patients.find({
  $text: { $search: "Hypertension" }
}).toArray();
print("\n=== 2.5 Recherche textuelle (Hypertension) ===");
printjson(rechercheTexte);
