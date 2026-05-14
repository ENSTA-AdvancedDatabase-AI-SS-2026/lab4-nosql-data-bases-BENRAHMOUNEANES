use("medical_db");

print("--- 5.1: Join Patients & Analyses ---");
const l1 = db.patients.aggregate([
  { $lookup: { from: "analyses", localField: "_id", foreignField: "patient_id", as: "tests" } },
  { $match: { "tests.0": { $exists: true } } },
  { $project: { nom: 1, prenom: 1, num_tests: { $size: "$tests" } } }
]).toArray();
printjson(l1);

print("--- 5.2: Unvalidated analyses with patient info ---");
const l2 = db.analyses.aggregate([
  { $match: { valide: false } },
  { $lookup: { from: "patients", localField: "patient_id", foreignField: "_id", as: "p" } },
  { $unwind: "$p" },
  { $project: { type: 1, patient: { $concat: ["$p.nom", " ", "$p.prenom"] } } }
]).toArray();
printjson(l2);

print("--- 5.3: Stats by wilaya ---");
const l3 = db.analyses.aggregate([
  { $lookup: { from: "patients", localField: "patient_id", foreignField: "_id", as: "p" } },
  { $unwind: "$p" },
  { $group: { _id: "$p.adresse.wilaya", count: { $sum: 1 } } }
]).toArray();
printjson(l3);
