from fastapi import FastAPI, Path,  HTTPException,Query
import database
from schema import Patient

app = FastAPI()

@app.get("/")
def hello ():
    return {"message": "Live from FastAPI!"}

@app.get("/patients")
def get_all_patients():
    return database.get_patients()

@app.post("/create_patients")
def create_patient(patient: Patient):
    success = database.create_patients(
        patient.name,
        patient.age,
        patient.gender,
        patient.blood_type,
        patient.contact_phone,
        patient.contact_email,
        patient.Medical_History,
        patient.doctor_assigned
    
    )
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add patient")
    return {"message": "Patient added successfully"}


@app.put("/update_patients/{patient_id}")
def update_existing_patient(patient_id: int = Path(..., description="The ID of the patient to update"), patient: Patient = ...):
    success = database.update_patient(patient_id, patient.name, patient.age, patient.gender, patient.blood_type, patient.contect_phone)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to update patient")
    return {"message": "Patient updated successfully"}

@app.delete("/delete_patients/{patient_id}")
def delete_existing_patient(patient_id: int = Path(..., description="The ID of the patient to delete")):
    success = database.delete_patient(patient_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to delete patient add existing id ")
    return {"message": "Patient deleted successfully"}


@app.get("/sort_patient") 
def sort_patients(sort_by: str = Query(..., description= "sort on the basis of blood_type ,age or gender"),
                  order: str = Query("asc", description="Order of sorting: 'asc' for ascending, 'desc' for descending")):
    valid_fileds = ["blood_type", "age", "gender"]
    
    if sort_by not in valid_fileds: 
        raise HTTPException(status_code=400, detail=f"Invalid sort_by field. Must be one of {valid_fileds}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order. Must be 'asc' or 'desc'")
    
    data = database.get_patients()
    sort_order = True if order == "desc" else False
    sorted_data = sorted(data, key=lambda x: x[sort_by], reverse=sort_order)
    
    return {"sorted_patients": sorted_data}