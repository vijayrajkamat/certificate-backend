from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import EmailStr
from typing import List

from database import init_db
from database import SessionLocal
from database import CertificateSubmission

from pdf_service import generate_pdf
from email_service import send_certificate_email

import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    
    pdf_path = generate_pdf(data, submission.id)
    
    send_certificate_email(
        to_email=data.email,
        name=data.name,
        pdf_path=pdf_path
	)

    db.close()

    return {
    
        "status": "success",
	"message": "Data stored, PDF generated, and email sent",
	"submission_id": submission.id,
    	"pdf_path": pdf_path
}	