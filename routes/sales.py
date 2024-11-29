from fastapi import APIRouter, Request, Depends
from datetime import date

from middleware.db_ops import SalesWriter, SalesReader
from middleware.xmlprocessor import XMLProcessor
from model import SalesData, Session, get_db


descr = """
            Пример XML-запроса:
            
            <sales_data date="2024-11-29">
                <product>
                    <name>Product R</name>
                    <quantity>121</quantity>
                    <unit_price>1500.0</unit_price>
                    <category>Food</category>
                </product>
                <product>
                    <name>Product F</name>
                    <quantity>233</quantity>
                    <unit_price>750.5</unit_price>
                    <category>Oil</category>
                </product>
            </sales_data>
            
            В данном запросе `sales_data` содержит атрибут `date` и список продуктов с соответствующими данными.
            Пожалуйста, отправьте XML с заголовком `Content-Type: application/xml`.
          """
sales = APIRouter(tags=["sales"], prefix="/sales")


@sales.post("/set", response_model=SalesData, description=descr)
async def set_sales(xml_body: Request, session: Session = Depends(get_db)) -> SalesData:
    print(descr)
    return SalesWriter(session).write(XMLProcessor(await xml_body.body()).get())


@sales.get("/get", response_model=SalesData)
async def get_sales(date: str | date, session: Session = Depends(get_db)) -> SalesData:
    return SalesReader(session).read_by_date(date)
