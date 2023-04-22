from schemas.user import UserUpdate, UserCreate, UserModel


class PatientModel(UserModel):
    status_id: int

    class Config:
        orm_mode = True


class PatientCreate(UserCreate):
    status_id: int


class PatientUpdate(UserUpdate):
    status_id: int
