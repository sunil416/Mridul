from pydantic import BaseModel, EmailStr, Field , field_validator, model_validator,computed_field
from typing import List, Dict, Optional, Annotated
''' strict prevents type coersion '''
''' Field Valiadator is used to field as per business usecases like business emails etc '''
''' pip install "pydantic[email]" '''
''' Annotated is used to attach meta data with field '''
''' field validator operates in 2 modes before( to recieve value thats before type coersion) and after mode ( to recieve value after type coersion). '''
''' Model Validator is used combine multiple fields into one and then do validation'''
class Patient(BaseModel):
    name: Annotated[str, Field(max_length=50)]
    email: EmailStr
    age: Annotated[int, Field(gt=0, lt=101, strict=True)]
    weight: Annotated[float, Field(gt=0, strict=True)]
    height: Annotated[float, Field(gt=0, strict=True)]
    married: Optional[bool] = False
    allergies: List[str]
    contact_details: Dict[str, str]
    
    @computed_field
    @property
    def bmi_calculate(self)-> float: 
        bmi=round(self.weight/self.height**2,2)
        return bmi
    
    @field_validator('email')
    @classmethod
    def valid_email(cls, value):
        valid_domains = ["softsuave.org", "soft.suave.org"]
        domain = value.split("@")[-1]
        if domain not in valid_domains:
            raise ValueError(f"Email domain '{domain}' is not allowed.")
        return value
    
    @model_validator(mode='after')
    def validate_emergency(cls, model):
        if model.age>60 and 'emergency_contact ' not in model.contact_details :
            raise ValueError
        else:
            return model
    

def insert_patient(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.bmi_calculate)
    print("Inserted")

patient_info = {
    'name': 'Abc',
    'email': 'abc@softsuave.org',
    'age': 60,                      # must be int
    'weight': 75.5,                 # must be float
    'height': 1.72,
    'married': True,
    'allergies': ['a', 'B', 'C'],
    'contact_details': {'email': 'abc@gmail.com', 'Phone': '1234567890'}
}

patient1 = Patient(**patient_info)
insert_patient(patient1)
