use("medical_db");

print("--- 3.1: Diag distribution by wilaya ---");
const d1 = db.patients.aggregate([
  { $unwind: "$consultations" },
  { $group: { _id: { w: "$adresse.wilaya", d: "$consultations.diagnostic" }, total: { $sum: 1 } } },
  { $sort: { total: -1 } }
]).toArray();
printjson(d1);

print("--- 3.2: Top meds by spec ---");
const d2 = db.patients.aggregate([
  { $unwind: "$consultations" },
  { $unwind: "$consultations.medicaments" },
  { $group: { _id: { s: "$consultations.medecin.specialite", m: "$consultations.medicaments.nom" }, n: { $sum: 1 } } },
  { $sort: { n: -1 } },
  { $group: { _id: "$_id.s", best: { $first: "$_id.m" }, qty: { $first: "$n" } } }
]).toArray();
printjson(d2);

print("--- 3.3: Monthly stats ---");
const d3 = db.patients.aggregate([
  { $unwind: "$consultations" },
  { $group: { _id: { y: { $year: "$consultations.date" }, m: { $month: "$consultations.date" } }, count: { $sum: 1 } } },
  { $sort: { "_id.y": 1, "_id.m": 1 } }
]).toArray();
printjson(d3);

print("--- 3.4: High risk profile ---");
const d4 = db.patients.aggregate([
  { $match: { antecedents: { $in: ["Diabète", "HTA"] } } },
  { $project: { num_cons: { $size: "$consultations" } } },
  { $group: { _id: null, avg: { $avg: "$num_cons" }, total: { $sum: 1 } } }
]).toArray();
printjson(d4);

print("--- 3.5: Doctor leaderboard ---");
const d5 = db.patients.aggregate([
  { $unwind: "$consultations" },
  { $group: { _id: "$consultations.medecin.nom", total: { $sum: 1 }, users: { $addToSet: "$_id" } } },
  { $project: { total: 1, u_count: { $size: "$users" } } },
  { $addFields: { rate: { $multiply: [{ $divide: [{ $subtract: ["$total", "$u_count"] }, "$u_count"] }, 100] } } },
  { $sort: { total: -1 } },
  { $limit: 5 }
]).toArray();
printjson(d5);
