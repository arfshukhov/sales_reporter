from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from datetime import date

from middleware.db_ops import SalesReader, ReportReader
from middleware.llm import ReportProcessor
from model import Session, Report, Error404, get_db
from settings import ServerSettings

report = APIRouter(tags=["report"], prefix="/report")


@report.get(
    "/daily",
    responses={
        404: {
            "description": "Item not found",
            "model": Error404,
        }
    },
    response_model=Union[Report, Error404],
)
async def get_report(
    date: date | str = date.today(), session: Session = Depends(get_db)
):
    rep = ReportReader(session).read_by_date(date)
    if rep:
        return Report.from_orm(rep)
    else:
        raise HTTPException(status_code=404, detail="report not found or not uploaded")


@report.get(
    "/currently",
    responses={
        404: {
            "description": "Item not found",
            "model": Error404,
        }
    },
    response_model=Union[Report, Error404],
)
async def get_current_report(session: Session = Depends(get_db)):
    sales_data = SalesReader(session).read_by_date(date.today())
    if sales_data:
        return Report(
            report=ReportProcessor(ServerSettings.LLM_API_KEY).report(sales_data),
            date=date.today(),
            id=0,
        )
    else:
        raise HTTPException(status_code=404, detail="sales data not found for today")
