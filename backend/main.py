import logging

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette.requests import Request
from starlette.responses import Response

from db.base import Session, get_db, engine, Base
from schemas.token import Token
from routes import company, photo, status, specialty, education, user, patient, doctor, predict_session, work_place, \
    appointment, article
from db.company import Company
from db.photo import Photo
from db.user import User
from db.patient import Patient
from db.predict_session import PredictSession
from db.education_specialty import EducationSpecialty
from db.education import Education
from db.doctors_education import DoctorsEducation
from db.doctor import Doctor
from db.work_place import WorkPlace
from db.appointment import Appointment
from db.article import Article
from services.token import create_token

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

app = FastAPI()


@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Request-Method"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Request-Headers"] = "content-type"
    response.headers["Access-Control-Allow-Private-Network"] = "true"
    return response


app.include_router(company.router)
app.include_router(photo.router)
app.include_router(status.router)
app.include_router(specialty.router)
app.include_router(education.router)
app.include_router(user.router)
app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(predict_session.router)
app.include_router(work_place.router)
app.include_router(appointment.router)
app.include_router(article.router)


@app.get("/")
async def root():
    logging.info("Root application start")
    Base.metadata.create_all(engine)


@app.post("/token", response_model=Token)
async def access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    return create_token(db, form_data.username, form_data.password)


@app.options("/{full_path:path}")
def options_handler(r: Request, full_path: str | None):
    headers = {"Access-Control-Allow-Origin": "*",
               "Access-Control-Allow-Methods": "*",
               "Access-Control-Allow-Headers": "Content-Type"}
    return Response(status_code=200, headers=headers)
