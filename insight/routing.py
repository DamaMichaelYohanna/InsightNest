import datetime
import os
import pathlib

from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy import create_engine
from sqlmodel import Session, select, SQLModel

from insight.schema import InsightCompose
from user.models import get_session, User
from user.deps import get_current_user
from insight.models import Insight

insight = FastAPI()


@insight.get('')
async def insight_list(session: Session = Depends(get_session),
                       current_user: User = Depends(get_current_user)):
    """List out all the insight by a user."""
    insights = session.exec(select(Insight).where(Insight.user == current_user))
    return insights


@insight.get("/{insight_id}")
async def insight_detail(insight_id: int,
                         session: Session = Depends(get_session),
                         current_user: User = Depends(get_current_user)
                         ):
    """display details of a particular insight"""
    return session.get(Insight, insight_id)


@insight.post('/compose',)
async def compose_insight(new_insight: InsightCompose,
                          session: Session = Depends(get_session),
                          current_user: User = Depends(get_current_user)):
    new_insight.date = str(datetime.datetime.now().date())
    new_insight.user = current_user.id
    print(new_insight)
    session.add(new_insight)
    session.commit()
    return new_insight
