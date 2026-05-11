use("medical_db");

// 5.1 Joindre patients et analyses pour récupérer
// le dossier complet d'un patient
const dossierComplet = db.patients.aggregate([
  { $match: { cin: "198001012300" } }, // Exemple avec un CIN spécifique
  {
    $lookup: {
      from: "analyses",
      localField: "_id",
      foreignField: "patient_id",
      as: "dossier_analyses"
    }
  }
]).toArray();
print("\n=== 5.1 Dossier complet (Patient + Analyses) ===");
printjson(dossierComplet);

// 5.2 Trouver les patients dont la glycémie dépasse 1.26 g/L
// (dans la collection analyses séparée)
const patientsGlycemieAnormale = db.analyses.aggregate([
  { $match: { type: "Glycémie", "resultats.valeur": { $gt: 1.26 } } },
  {
    $lookup: {
      from: "patients",
      localField: "patient_id",
      foreignField: "_id",
      as: "patient_info"
    }
  },
  { $unwind: "$patient_info" },
  { $project: { "patient_info.nom": 1, "patient_info.prenom": 1, "resultats.valeur": 1, date: 1 } }
]).toArray();
print("\n=== 5.2 Patients avec Glycémie > 1.26 g/L ===");
printjson(patientsGlycemieAnormale);

// 5.3 Statistiques croisées : taux d'analyses anormales par wilaya
const statsWilaya = db.analyses.aggregate([
  { $match: { "resultats.valeur": { $gt: 1.26 } } },
  {
    $lookup: {
      from: "patients",
      localField: "patient_id",
      foreignField: "_id",
      as: "patient_info"
    }
  },
  { $unwind: "$patient_info" },
  {
    $group: {
      _id: "$patient_info.adresse.wilaya",
      analyses_anormales: { $sum: 1 }
    }
  },
  { $sort: { analyses_anormales: -1 } }
]).toArray();
print("\n=== 5.3 Taux d'analyses anormales par wilaya ===");
printjson(statsWilaya);
