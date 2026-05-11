use("medical_db");

print("=== 3.1 : Top diagnostics par wilaya ===");
const diagParWilaya = db.patients.aggregate([
  { $unwind: "$consultations" },
  { $group: { _id: { wilaya: "$adresse.wilaya", diagnostic: "$consultations.diagnostic" }, count: { $sum: 1 } } },
  { $sort: { count: -1 } },
  { $limit: 20 }
]).toArray();
printjson(diagParWilaya);

print("\n=== 3.2 : Top médicaments par spécialité ===");
const medsParSpecialite = db.patients.aggregate([
  { $unwind: "$consultations" },
  { $unwind: "$consultations.medicaments" },
  { $group: { _id: { specialite: "$consultations.medecin.specialite", medicament: "$consultations.medicaments.nom" }, count: { $sum: 1 } } },
  { $sort: { count: -1 } },
  { $group: { _id: "$_id.specialite", top_medicament: { $first: "$_id.medicament" }, count: { $first: "$count" } } }
]).toArray();
printjson(medsParSpecialite);

print("\n=== 3.3 : Consultations par mois (12 derniers mois) ===");
const evolutionMensuelle = db.patients.aggregate([
  { $unwind: "$consultations" },
  { $match: { "consultations.date": { $gte: new Date(new Date().setFullYear(new Date().getFullYear() - 1)) } } },
  { $group: { _id: { annee: { $year: "$consultations.date" }, mois: { $month: "$consultations.date" } }, count: { $sum: 1 } } },
  { $sort: { "_id.annee": 1, "_id.mois": 1 } },
  { $project: { month_year: { $concat: [{ $toString: "$_id.annee" }, "-", { $toString: "$_id.mois" }] }, count: 1, _id: 0 } }
]).toArray();
printjson(evolutionMensuelle);

print("\n=== 3.4 : Profil patients à risque élevé ===");
const patientsRisque = db.patients.aggregate([
  { $match: { antecedents: { $all: ["Diabète type 2", "HTA"] } } },
  { $addFields: { age: { $divide: [{ $subtract: [new Date(), "$dateNaissance"] }, 31536000000] }, consultations_count: { $size: "$consultations" } } },
  { $match: { age: { $gte: 60 } } },
  { $group: { _id: null, avg_consultations: { $avg: "$consultations_count" }, total_patients: { $sum: 1 } } }
]).toArray();
printjson(patientsRisque);

print("\n=== 3.5 : Top 5 médecins & taux de ré-consultation ===");
const rapportMedecins = db.patients.aggregate([
  { $unwind: "$consultations" },
  { $group: { _id: "$consultations.medecin.nom", patients_uniques: { $addToSet: "$_id" }, total_consultations: { $sum: 1 } } },
  { $addFields: { 
      patients_uniques_count: { $size: "$patients_uniques" },
      taux_reconsultation: { 
          $multiply: [ 
              { $divide: [ { $subtract: ["$total_consultations", { $size: "$patients_uniques" }] }, { $size: "$patients_uniques" } ] }, 
              100 
          ] 
      } 
  }},
  { $sort: { total_consultations: -1 } },
  { $limit: 5 }
]).toArray();
printjson(rapportMedecins);
