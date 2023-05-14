import logging
from typing import List

import cv2
from db.predict_session import PredictSession
from schemas.patient import PatientUpdate
from schemas.predict_session import PredictSessionCreate, PredictSessionUpdate
from schemas.status import StatusCreate
from services.patient import read_patient, update_patient
from services.photo import read_photo
from services.status import read_status_by_name, create_status, read_healthy_status
from sqlalchemy.orm import Session
from tensorflow import keras

from backend.db.status import Status
from backend.schemas.predict_session import PredictSessionResponse

logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:  %(asctime)s  %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")


def create_predict_session(db: Session, predict_session: PredictSessionCreate) -> PredictSession:
    db_predict_session = PredictSession(
        patient_id=predict_session.patient_id,
        photo_id=predict_session.photo_id,
        predict_score=predict_session.predict_score,
        start_datetime=predict_session.start_datetime)
    db.add(db_predict_session)
    db.commit()
    db.refresh(db_predict_session)
    return db_predict_session


def read_predict_session(db: Session, predict_session_id: int) -> PredictSession:
    db_predict_session = db.query(PredictSession).filter(PredictSession.id == predict_session_id).first()
    if db_predict_session is None:
        raise ValueError(f"PredictSession not found with id {predict_session_id}")
    return db_predict_session


def read_predict_sessions(db: Session) -> List[PredictSession]:
    return db.query(PredictSession).all()


def update_predict_session(db: Session, predict_session_id: int, predict_session: PredictSessionUpdate) -> \
        PredictSession:
    db_predict_session = read_predict_session(db, predict_session_id)
    for key, value in predict_session.dict(exclude_unset=True).items():
        setattr(db_predict_session, key, value)
    db.commit()
    db.refresh(db_predict_session)
    return db_predict_session


def delete_predict_session(db: Session, predict_session_id: int) -> None:
    db_predict_session = read_predict_session(db, predict_session_id)
    db.delete(db_predict_session)
    db.commit()


def classes():
    return {4: 'врожденный меланоцитарный невус', 6: 'меланома',
            2: 'доброкачественный себорейный кератоз',
            1: 'базальноклеточная карцинома', 5: 'пиогенные гранулема и геморрагия',
            0: 'актинический кератоз и внутриэпителиальная карцинома',
            3: 'дерматофиброма'}


def result_from_model(db: Session, predict_session: PredictSession):
    model = keras.models.load_model('/app/services/model.h5')
    photo_path = read_photo(db, predict_session.photo_id).path
    img = cv2.imread(photo_path)
    cv2.imwrite(photo_path, img)
    img = cv2.resize(img, (28, 28))
    return model.predict(img.reshape(1, 28, 28, 3))


def predict(db: Session, predict_session_id: int):
    predict_session = read_predict_session(db, predict_session_id)
    patient = read_patient(db, predict_session.patient_id)
    result = result_from_model(db, predict_session)
    max_prob = max(result[0])
    status: Status
    if max_prob < 0.6:
        status = read_healthy_status(db)
    else:
        class_ind = list(result[0]).index(max_prob)
        class_name = classes()[class_ind]
        if status := read_status_by_name(db, class_name.lower()):
            pass
        else:
            status = create_status(db, StatusCreate(name=class_name[1].lower()))
    patient_update = PatientUpdate(name=patient.name, birthday_date=patient.birthday_date,
                                   residence=patient.residence, email=patient.email,
                                   telephone=patient.telephone, password=patient.password,
                                   status_id=status.id, photo_id=patient.photo_id)
    update_patient(db, patient.id, patient_update)
    predict_session_update = PredictSessionUpdate(photo_id=predict_session.photo_id,
                                                  predict_score=max_prob,
                                                  start_datetime=predict_session.start_datetime)
    update_predict_session(db, predict_session_id, predict_session_update)
    return PredictSessionResponse(id=predict_session_id,
                                  predict_score=max_prob,
                                  start_datetime=predict_session.start_datetime,
                                  status_name=status.name,
                                  patient_id=patient.id)
