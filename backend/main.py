import logging

from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm

from db.base import Session, get_db
from schemas.token import Token
from routes import company, photo, status, specialty, education, user, patient, doctor, predict_session, work_place, \
    doctor_jobs, appointment
from services.token import create_token

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

app = FastAPI()
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
app.include_router(doctor_jobs.router)
app.include_router(appointment.router)


@app.get("/")
async def root():
    logging.info("Root application start")


@app.post("/token", response_model=Token)
async def access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    return create_token(db, form_data.username, form_data.password)
