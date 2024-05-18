import datetime

from fastapi import FastAPI, Depends, Form
from sqlmodel import Session, select

from crime.models import Crime
from database import get_session
from user.deps import get_current_user
from user.models import User

crime = FastAPI()


@crime.post("/")
async def report_crime(session: Session = Depends(get_session),
                       current_user: User = Depends(get_current_user),
                       category: str = Form(...),
                       details: str = Form(...),
                       state: str = Form(...),
                       lga: str = Form(...),
                       anonymous: str = Form(...)
                       ):
    crime_obj = Crime(category=category, details=details, state=state, lga=lga, date=datetime.datetime.now().date())
    if not anonymous:
        crime_obj.name = current_user.full_name

    session.add(crime_obj)
    session.commit()
    return {"message": "Crime has been reported successfully."}


@crime.get("/")
async def view_reported_crime(session: Session = Depends(get_session)):
    statement = select(Crime)
    reported_crime = session.exec(statement)
    return reported_crime.all()


@crime.delete("/")
async def delete_reported_crime():
    pass


@crime.put("/")
async def update_reported_crime():
    pass
