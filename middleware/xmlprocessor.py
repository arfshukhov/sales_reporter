import xmltodict
from model import SalesData


class XMLProcessor:
    def __init__(self, xml_object):
        self.__xml_object = xml_object

    def get(self):
        raw_data = xmltodict.parse(self.__xml_object)
        sales_data = raw_data["sales_data"]
        sales_data["date"] = sales_data.pop("@date")
        return SalesData(
            date=sales_data["date"], products=sales_data["products"]["product"]
        )
