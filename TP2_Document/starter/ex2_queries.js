use("medical_db");

db.patients.createIndex({ "$**": "text" });

const q1 = db.patients.find({
  "adresse.wilaya": "Alger",
  antecedents: "Diabète type 2",
  dateNaissance: { $lte: new Date(new Date().setFullYear(new Date().getFullYear() - 50)) }
}).toArray();
printjson(q1);

const q2 = db.patients.find({
  allergies: "Pénicilline",
  $expr: { $gte: [{ $size: "$consultations" }, 3] }
}).toArray();
printjson(q2);

const q3 = db.patients.find(
  {},
  { nom: 1, prenom: 1, derniereConsultation: { $arrayElemAt: ["$consultations", -1] }, _id: 0 }
).toArray();
printjson(q3);

const q4 = db.patients.find({
  $or: [{ antecedents: { $exists: false } }, { antecedents: { $size: 0 } }],
  $expr: {
    $gt: [
      { $let: { vars: { last_consultation: { $arrayElemAt: ["$consultations", -1] } }, in: "$$last_consultation.tension.systolique" } },
      140
    ]
  }
}).toArray();
printjson(q4);

const q5 = db.patients.find({
  $text: { $search: "Hypertension" }
}).toArray();
printjson(q5);
