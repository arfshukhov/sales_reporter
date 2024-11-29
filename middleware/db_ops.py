from model import *


class SalesReader:
    def __init__(self, session: Session = next(get_db())):
        self.session = session

    def read_by_date(
        self,
        date: date | str,
    ) -> SalesData | None:
        data = self.session.query(SalesDataModel).filter_by(date=date).one_or_none()
        if data:
            return SalesData.from_orm(data)
        else:
            return None


class SalesWriter:
    def __init__(self, session: Session = next(get_db())):
        self.session = session

    def write(self, data: SalesData) -> SalesData:
        try:
            sales_query = SalesDataModel(date=data.date)
            self.session.add(sales_query)
            self.session.commit()
        except Exception:
            self.session.rollback()
        try:
            for i in data.products:
                query = ProductModel(
                    name=i.name,
                    price=i.price,
                    quantity=i.quantity,
                    date=data.date,
                    category=i.category,
                )
                self.session.add(query)
                self.session.commit()
            return SalesData.from_orm(
                self.session.query(SalesDataModel)
                .filter_by(date=data.date)
                .one_or_none()
            )
        except Exception:
            self.session.rollback()


class ReportReader:
    def __init__(self, session: Session = next(get_db())):
        self.session = session

    def read_by_date(self, date: str | date) -> Report:
        rep = self.session.query(ReportModel).filter_by(date=date).one_or_none()
        if rep:
            return Report.from_orm(rep)
        else:
            return None


class ReportWriter:
    def __init__(self, session: Session = next(get_db())):
        self.session = session

    def write(self, report: Report) -> Report:
        try:
            query = ReportModel(date=report.date, report=report.report)
            self.session.add(query)
            self.session.commit()
            return Report.from_orm(
                self.session.query(ReportModel)
                .filter_by(date=report.date)
                .one_or_none()
            )
        except Exception:
            self.session.rollback()
