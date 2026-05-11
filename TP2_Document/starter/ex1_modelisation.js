use("medical_db");

db.createCollection("patients", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["cin", "nom", "prenom", "dateNaissance", "sexe"],
      properties: {
        cin: { bsonType: "string", description: "CIN obligatoire" },
        nom: { bsonType: "string" },
        prenom: { bsonType: "string" },
        dateNaissance: { bsonType: "date" },
        sexe: { enum: ["M", "F"] },
        groupeSanguin: { enum: ["O+", "O-", "A+", "A-", "B+", "B-", "AB+", "AB-"] }
      }
    }
  }
});

const patients = [
  {
    cin: "198001012300",
    nom: "Bensalem",
    prenom: "Ahmed",
    dateNaissance: new Date("1980-01-01"),
    sexe: "M",
    adresse: { wilaya: "Alger", commune: "Bab Ezzouar" },
    groupeSanguin: "O+",
    antecedents: ["Diabète type 2", "HTA"],
    allergies: ["Pénicilline"],
    consultations: [
      {
        id: UUID(),
        date: new Date("2024-01-15"),
        medecin: { nom: "Dr. Mansouri", specialite: "Cardiologie" },
        diagnostic: "Hypertension artérielle",
        tension: { systolique: 145, diastolique: 92 },
        medicaments: [{ nom: "Amlodipine", dosage: "5mg", duree: "30 jours" }],
        notes: "Surveillance tensionnelle recommandée"
      },
      {
        id: UUID(),
        date: new Date("2024-03-20"),
        medecin: { nom: "Dr. Mansouri", specialite: "Cardiologie" },
        diagnostic: "Hypertension artérielle contrôlée",
        tension: { systolique: 130, diastolique: 85 },
        medicaments: [{ nom: "Amlodipine", dosage: "5mg", duree: "30 jours" }],
        notes: "Tension stabilisée"
      }
    ]
  },
  {
    cin: "199002022301",
    nom: "Bouzid",
    prenom: "Fatima",
    dateNaissance: new Date("1990-05-12"),
    sexe: "F",
    adresse: { wilaya: "Oran", commune: "Es Senia" },
    groupeSanguin: "A+",
    antecedents: ["Asthme"],
    allergies: [],
    consultations: [
      {
        id: UUID(),
        date: new Date("2023-11-10"),
        medecin: { nom: "Dr. Kaddour", specialite: "Pneumologie" },
        diagnostic: "Crise d'asthme",
        tension: { systolique: 120, diastolique: 80 },
        medicaments: [{ nom: "Salbutamol", dosage: "100mcg", duree: "Si besoin" }],
        notes: "Prescription d'inhalateur"
      }
    ]
  }
];

for (let i = 2; i < 20; i++) {
    patients.push({
        cin: `20000000000${i}`,
        nom: `Patient${i}`,
        prenom: `Prenom${i}`,
        dateNaissance: new Date(1950 + i, 0, 1),
        sexe: i % 2 === 0 ? "M" : "F",
        adresse: { wilaya: ["Alger", "Oran", "Constantine", "Annaba", "Blida"][i % 5], commune: "Commune" },
        groupeSanguin: "B+",
        antecedents: i % 3 === 0 ? ["Diabète type 2", "HTA"] : [],
        allergies: [],
        consultations: [
            {
                id: UUID(),
                date: new Date(2023, i % 12, i),
                medecin: { nom: `Dr. Med${i}`, specialite: ["Généraliste", "Pneumologie", "Cardiologie"][i % 3] },
                diagnostic: ["Grippe", "Covid", "HTA", "Asthme"][i % 4],
                tension: { systolique: 120 + i, diastolique: 80 },
                medicaments: []
            }
        ]
    });
}

db.patients.insertMany(patients);

const patients_docs = db.patients.find().toArray();

const analyses = patients_docs.map((p, index) => ({
    patient_id: p._id,
    date: new Date(2023, index % 12, 15),
    type: ["Glycémie", "NFS", "Lipidogramme", "Créatinine", "ECG"][index % 5],
    resultats: { valeur: 1.0 + (index * 0.1) },
    laboratoire: "Labo Central",
    valide: true
}));

db.analyses.insertMany(analyses);

print("✅ Modélisation terminée. Patients insérés:", db.patients.countDocuments());
print("✅ Analyses insérées:", db.analyses.countDocuments());
