from fastapi import FastAPI
from routes.sales import sales
from routes.report import report
app = FastAPI()

app.include_router(sales)
app.include_router(report)