from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import EmailStr
from typing import List

from database import init_db
from database import SessionLocal
from database import CertificateSubmission

import json

app = FastAPI()


class CertificateRequest(BaseModel):

    email: EmailStr

    name: str

    strengths: List[str]

    skills: List[str]

    values: List[str]

    passions: List[str]

    purpose: str


@app.on_event("startup")
def startup():

    init_db()


@app.get("/")
def home():

    return {
        "message": "Certificate backend is running"
    }


@app.post("/generate-certificate")
def generate_certificate(data: CertificateRequest):

    db = SessionLocal()

    submission = CertificateSubmission(

        email=data.email,

        name=data.name,

        strengths=json.dumps(data.strengths),

        skills=json.dumps(data.skills),

        values=json.dumps(data.values),

        passions=json.dumps(data.passions),

        purpose=data.purpose
    )

    db.add(submission)

    db.commit()

    db.refresh(submission)

    db.close()

    return {

        "status": "success",

        "message": "Data stored successfully",

        "submission_id": submission.id
    }