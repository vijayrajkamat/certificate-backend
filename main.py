from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
from typing import List

app = FastAPI()


class CertificateRequest(BaseModel):
    email: EmailStr
    name: str
    strengths: List[str]
    skills: List[str]
    values: List[str]
    passions: List[str]
    purpose: str


@app.get("/")
def home():
    return {"message": "Certificate backend is running"}


@app.post("/generate-certificate")
def generate_certificate(data: CertificateRequest):
    return {
        "status": "success",
        "message": "Data received successfully",
        "received": data
    }