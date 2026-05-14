use("medical_db");

db.patients.drop();
db.analyses.drop();

db.createCollection("patients", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["cin", "nom", "prenom", "dateNaissance", "sexe"],
      properties: {
        cin: { bsonType: "string" },
        nom: { bsonType: "string" },
        prenom: { bsonType: "string" },
        dateNaissance: { bsonType: "date" },
        sexe: { enum: ["M", "F"] },
        adresse: {
          bsonType: "object",
          required: ["wilaya"],
          properties: { wilaya: { bsonType: "string" } }
        }
      }
    }
  }
});

const wilayas_list = ["Alger", "Oran", "Constantine", "Annaba", "Blida"];
const names_list = ["Abid", "Ziane", "Hamidi", "Belkacem", "Haddad"];
const paths_list = ["Diabète", "HTA", "Asthme"];

let p_list = [];
for (let i = 0; i < 20; i++) {
  p_list.push({
    cin: "X" + i.toString().padStart(5, '0'),
    nom: names_list[i % 5],
    prenom: "P" + i,
    dateNaissance: new Date(1970 + i, 5, 15),
    sexe: i % 2 === 0 ? "M" : "F",
    adresse: { wilaya: wilayas_list[i % 5] },
    antecedents: [paths_list[i % 3]],
    consultations: [
      {
        id: UUID(),
        date: new Date(2024, i % 12, 1),
        medecin: { nom: "Dr. L", specialite: "General" },
        diagnostic: paths_list[i % 3],
        tension: { systolique: 130 + i, diastolique: 85 }
      }
    ]
  });
}

db.patients.insertMany(p_list);

const docs = db.patients.find().toArray();
db.analyses.insertMany(docs.map(d => ({
  patient_id: d._id,
  date: new Date(),
  type: "Glycémie",
  resultats: { val: 1.2 },
  valide: true
})));

print("Done. Patients:", db.patients.countDocuments());
