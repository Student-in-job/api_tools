from typing import Union

import pymongo.collection

from app.scripts.mongo_db import *
from app.scripts.config import *
from fastapi import FastAPI, Request
import json

app = FastAPI()
mongo = open_connection(MONGO_HOST, MONGO_DATABASE)


@app.get("/")
def main(request: Request):
    origin_url = request.headers.get('host')
    # return {"mess": request.headers}
    return {"message": "You can use one of the following links to return DB records",
            "links": [{"url": "http://{0}/accounts/{{contract_id}}".format(origin_url), "method": "GET",
                       "description": "Returns accounts by contract_id"},
                      {"url": "http://{0}/katm_claims/{{contract_id}}".format(origin_url), "method": "GET",
                       "description": "Returns katm_claims by contract_id"},
                      {"url": "http://{0}/katm_reports/{{contract_id}}".format(origin_url), "method": "GET",
                       "description": "Returns katm_reports by contract_id"},
                      {"url": "http://{0}/katm_received_reports/{{contract_id}}".format(origin_url), "method": "GET",
                       "description": "Returns katm_received_reports by contract_id"},
                      {"url": "http://{0}/katm_reports/{{contract_id}}/report_number/{{report_number}}".format(origin_url), "method": "GET",
                       "description": "Returns katm_reports by contract_id"}
                      ],}


def save_to_file(name:str, data: list):
    f = open("/code/output/{0}".format(name), "w")
    for element in data:
        f.write(str(element))
        f.write("\n")
    f.close()


def get_data(collection_name: str, contract_id: int, katm_report: str=None):
    collection = get_collection(mongo, collection_name, False)
    arr = []
    query_filter = {"contract_id": contract_id}
    if katm_report is not None:
        query_filter['report_number'] = katm_report
    for item in collection.find(query_filter):
        item['_id'] = "Object({0})".format(str(item['_id']))
        item['body_json'] = json.loads(item['body'])
        item['body_json']['security']['pPassword'] = "***************"
        del(item['body'])
        arr.append(item)
        # item.pop('body')
    return arr


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/accounts/{contract_id}")
def read_accounts(contract_id: int):
    return {"data": get_data(COLLECTION_ACCOUNTS, contract_id)}


@app.get("/katm_claims/{contract_id}")
def read_accounts(contract_id: int):
    return {"data": get_data(COLLECTION_KATM_CLAIMS, contract_id)}


@app.get("/katm_received_reports/{contract_id}")
def read_accounts(contract_id: int):
    return {"data": get_data(COLLECTION_KATM_RECEIVED_REPORTS, contract_id)}


@app.get("/katm_reports/{contract_id}")
def read_accounts(contract_id: int):
    return {"data": get_data(COLLECTION_KATM_REPORTS, contract_id)}


@app.get("/katm_reports/{contract_id}/report_number/{report_number}")
def read_accounts(contract_id: int, report_number: str):
    return {"data": get_data(COLLECTION_KATM_REPORTS, contract_id, report_number)}