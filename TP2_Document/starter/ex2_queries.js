use("medical_db");

print("--- 2.1 Diabetics > 50 in Alger ---");
const q21 = db.patients.find({
  "adresse.wilaya": "Alger",
  antecedents: "Diabète",
  dateNaissance: { $lt: new Date(1974, 0, 1) }
}).toArray();
print("Count:", q21.length);

print("--- 2.2 Penicillin Allergy & 3+ Cons ---");
const q22 = db.patients.find({
  allergies: "Pénicilline",
  "consultations.2": { $exists: true }
}).toArray();
print("Count:", q22.length);

print("--- 2.3 Last Consultation Projection ---");
const q23 = db.patients.find({}, {
  nom: 1, prenom: 1, last_cons: { $slice: ["$consultations", -1] }, _id: 0
}).limit(3).toArray();
printjson(q23);

print("--- 2.4 No history, high tension ---");
const q24 = db.patients.find({
  $or: [{ antecedents: { $size: 0 } }, { antecedents: { $exists: false } }],
  "consultations.tension.systolique": { $gt: 140 }
}).toArray();
print("Count:", q24.length);

print("--- 2.5 Text Search ---");
db.patients.createIndex({ "consultations.diagnostic": "text" });
const q25 = db.patients.find({ $text: { $search: "Diabète" } }).toArray();
print("Found:", q25.length);
