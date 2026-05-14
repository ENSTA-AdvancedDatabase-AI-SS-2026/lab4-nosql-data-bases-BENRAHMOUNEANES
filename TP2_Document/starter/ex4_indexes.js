use("medical_db");

db.patients.createIndex({ cin: 1 }, { unique: true });
db.patients.createIndex({ "adresse.wilaya": 1, dateNaissance: -1 });
db.patients.createIndex({ "consultations.date": 1 });
db.analyses.createIndex({ patient_id: 1 });

const stats = db.patients.find({ "adresse.wilaya": "Alger" }).sort({ dateNaissance: -1 }).explain("executionStats");
print("Scan docs:", stats.executionStats.totalDocsExamined);
print("Time (ms):", stats.executionStats.executionTimeMillis);
