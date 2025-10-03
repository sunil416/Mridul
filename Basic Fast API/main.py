from fastapi import  FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
import json

from Postpydantic import *
app=FastAPI()


def load_data():
    with open("test.json","r") as f:
        data =json.load(f)
    return data

def save_data(data):
    with open('test.json', 'w') as f:
        json.dump(data, f)

@app.get("/")
def hello():
    return {'message':"hello"} 


@app.get("/about")
def about():
    return{'mesage': 'Fully functional api'}


@app.get("/view")
def view():
    data =load_data()
    return data

@app.get("/view/{patient_id}")
def view_patient(patient_id:str = Path(...,description="ID OF Patient in DB", examples="P001")):
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(404,"Patient not found ")

@app.get("/sort")
def sort(sort_by: str =Query(..., description="Sort  on basis of weight BMI OR HEIGHT"), order: str = Query (... ,description="SORT ASCENDIN OR DESCENDING")):
    data=load_data()
    
    if(sort_by not in ["bmi","height","weight"]):
        raise HTTPException(400)
        
    if(order not in ["asc","desc"]):
        raise HTTPException(400)
        
    sort_order=True if order=="desc" else False
    SORTED_DATA=sorted(data.values(),key=lambda x:x.get(sort_by,0), reverse = sort_order)
    return SORTED_DATA



'''
A request body is HTTP request that contains data sent by client to server. It is typically used in HTTP methods like POST and PUT


'''

@app.post("/create")
def  create_patient(patient:Patient): 
    
    
    '''
    Step 1: Load Existing data
    
    step 2: Check if patient exist in Data
    
    Step 3: else add patient to data
    
    '''
    
    data = load_data()

    # check if the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exists')

    # new patient add to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'patient created successfully'})



''' patient_id as path parameter for and request body is json format for updating in put '''

@app.put("/edit/{patient_id}")
def update(patient_id:str , patient_update:PatientUpdate):
    # new pydantic model with optional fields.
    data=load_data()
    if patient_id  not in data:
        raise HTTPException(404)
    existing_info= data[patient_id]
    
    update_patient_info = patient_update.model_dump(exclude_unset=True)
    for key,value in update_patient_info.items():
        existing_info[key]=value
    
    
    ''' existing_info -> pydantic object -> updated bmi / verdict  -> pydantic object to dictionary. ''' 
    existing_info['id']=patient_id
    new_pydantic_object=Patient(**existing_info)
    existing_patient_info = new_pydantic_object.model_dump(exclude='id')

    # add this dict to data
    data[patient_id] = existing_patient_info

    # save data
    save_data(data)

    return JSONResponse(status_code=200, content={'message':'patient updated'})



@app.delete("/delete/{patient_id}")
def delete(patient_id: str):
    data = load_data()
    if patient_id not in data :
        raise HTTPException(404)
    del data[patient_id]
    save_data(data)
    
    return JSONResponse(status_code=200, content={'message':'patient updated'})