use("medical_db");

db.patients.createIndex({ "adresse.wilaya": 1, antecedents: 1 });

db.patients.createIndex({ "consultations.date": -1 });

db.patients.createIndex({ "consultations.diagnostic": "text" });

db.analyses.createIndex({ "patient_id": 1 });

const requeteTest = {
  "adresse.wilaya": "Alger",
  antecedents: "Diabète type 2"
};

print("=== AVANT index ===");
// we will drop the index to test before
db.patients.dropIndex("adresse.wilaya_1_antecedents_1");
let stats_avant = db.patients.find(requeteTest).explain("executionStats");
print(`nReturned: ${stats_avant.executionStats.nReturned}`);
print(`totalDocsExamined: ${stats_avant.executionStats.totalDocsExamined}`);
print(`executionTimeMillis: ${stats_avant.executionStats.executionTimeMillis}`);

print("\n=== APRÈS index ===");
db.patients.createIndex({ "adresse.wilaya": 1, antecedents: 1 });
let stats_apres = db.patients.find(requeteTest).explain("executionStats");
print(`nReturned: ${stats_apres.executionStats.nReturned}`);
print(`totalDocsExamined: ${stats_apres.executionStats.totalDocsExamined}`);
print(`executionTimeMillis: ${stats_apres.executionStats.executionTimeMillis}`);

db.analyses.createIndex({ date: 1 }, { expireAfterSeconds: 157680000 });
