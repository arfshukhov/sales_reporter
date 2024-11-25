from fastapi import APIRouter, Request, Depends
from datetime import date

from middleware.db_ops import SalesWriter, SalesReader
from middleware.xmlprocessor import XMLProcessor
from model import SalesData, Session, get_db

sales = APIRouter(tags=['sales'], prefix='/sales')

@sales.post("/set", response_model=SalesData)
async def set_sales(xml_body: Request,
                    session: Session = Depends(get_db)
                    ) -> SalesData:
    return SalesWriter().write(XMLProcessor(await xml_body.body()).get())

@sales.get("/get", response_model=SalesData)
async def get_sales(date: str|date,
                    session: Session = Depends(get_db)
                    ) -> SalesData:
    return SalesReader(session).read_by_date(date)