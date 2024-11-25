from fastapi import APIRouter, Request, Depends, HTTPException
from datetime import date

from middleware.db_ops import SalesReader, ReportReader
from middleware.llm import ReportProcessor

from model import Session, get_db

report = APIRouter(tags=["report"], prefix="/report")

@report.get("/")
async def get_report(date: date|str,
                     session: Session = Depends(get_db)):
    report = ReportReader(session).read_by_date(date)
    if report:
        return report
    else:
        raise HTTPException(status_code=404, detail="report not found or not uploaded")