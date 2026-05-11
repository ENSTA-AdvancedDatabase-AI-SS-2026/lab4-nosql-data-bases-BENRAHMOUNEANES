use("medical_db");

const patientComplet = db.patients.aggregate([
  { $match: { cin: "198001012300" } },
  {
    $lookup: {
      from: "analyses",
      localField: "_id",
      foreignField: "patient_id",
      as: "dossier_analyses"
    }
  }
]).toArray();
printjson(patientComplet);

const patientsAnormaux = db.analyses.aggregate([
  { $match: { type: "Glycémie", "resultats.valeur": { $gt: 1.26 } } },
  {
    $lookup: {
      from: "patients",
      localField: "patient_id",
      foreignField: "_id",
      as: "patient_info"
    }
  },
  { $unwind: "$patient_info" }
]).toArray();
printjson(patientsAnormaux);

const statsCroisees = db.analyses.aggregate([
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
  }
]).toArray();
printjson(statsCroisees);
