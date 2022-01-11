from typing import Dict, Optional

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field

from modules.databaser import dao
from modules.pinger import pinger_all_network_with_threading

app = FastAPI()


@app.get("/")
async def start_page():
    return f"mainpage"


class ScanNetworkParam(BaseModel):
    network_name: Optional[str] = None
    mac_addr: Optional[str] = None
    vendor: Optional[str] = None


class ResultAllNetScan(BaseModel):
    items: Dict[str, ScanNetworkParam] = Field(..., description="Dictonary")

    class Config:
        schema_extra = {
            "example": {
                "items": {
                    "192.168.1.1": {
                        "network_name": "_gateway",
                        "mac_addr": "20:4e:7f:98:28:42",
                        "vendor": "Netgear",
                    },
                    "192.168.1.5": {
                        "network_name": "Hobot-ubuntu-worker",
                        "mac_addr": "null",
                        "vendor": "null",
                    },
                }
            }
        }


@app.get(
    "/net-scaner",
    response_model=ResultAllNetScan,
    response_description="All keys is IPv4",
)
async def net_scaner():
    result = pinger_all_network_with_threading.net_scanner()
    return {"items": result}


class PushToDb(BaseModel):
    hard_type: str
    hard_name: str
    hard_ip: str
    hard_place: str
    hard_comment: str

    class Config:
        schema_extra = {
            "example": {
                "hard_type": "1",
                "hard_name": "Cisco",
                "hard_ip": "192.168.0.1",
                "hard_place": "27",
                "hard_comment": "This is comment",
            }
        }


class PushToDbResponse(BaseModel):
    hard_name: str
    hard_id: str

    class Config:
        schema_extra = {"example": {"hard_name": "Cisco", "hard_id": "1"}}


@app.post("/push-in-base", response_model=PushToDbResponse)
async def create_hardware_unit(pushed_json: PushToDb):

    new_id = dao.DAO().create_hardware_unit_with_comment(
        pushed_json.hard_type,
        pushed_json.hard_name,
        pushed_json.hard_ip,
        pushed_json.hard_place,
        pushed_json.hard_comment,
    )

    return PushToDbResponse(hard_name=pushed_json.hard_name, hard_id=new_id)


# @app.post("/push-in-base")
# async def create_hardware_unit(hard_type, hard_name, hard_ip, hard_place, hard_comment):
#
#         new_id = dao.DAO().create_hardware_unit_with_comment(
#             hard_type, hard_name, hard_ip, hard_place, hard_comment
#         )
#
#         return f"Устройство `{hard_name}` c id '{new_id}' теперь в базе"


class ReadFromBaseWithId(BaseModel):
    input_id: int


class ReturnFromBaseWithId(BaseModel):
    id: int
    hard_type: int
    hard_name: str
    hard_ip: str
    hard_place: int
    comment: str

    class Config:
        schema_extra = {
            "example": {
                "id": "1",
                "hard_type": "2",
                "hard_name": "Cisco",
                "hard_ip": "192.168.0.1",
                "hard_place": "27",
                "hard_comment": "This is comment",
            }
        }


@app.post("/read-from-base-id", response_model=ReturnFromBaseWithId)
async def read_from_base_with_id(pushed_json: ReadFromBaseWithId):
    result = dao.DAO().read_hardware_with_comment(pushed_json.input_id)
    return result


class PingOneIp(BaseModel):
    input_id: int


class ResultPingOneIp(BaseModel):
    result: str

    class Config:
        schema_extra = {"example": {"result": "Network NOT ACTIVE or Error"}}


@app.get("/ping-one-ip", response_model=ResultPingOneIp)
async def ping_one_ip(pushed_json: PingOneIp):
    result_one_ping = dao.DAO().pinger_for_page(pushed_json.input_id)
    return {"result": result_one_ping}


class InputNewComment(BaseModel):
    id_for_update: int
    new_comment: str


class ResponseNewComment(BaseModel):
    id_for_update: int
    new_comment: str

    class Config:
        schema_extra = {"example": {"id_for_update": "1", "new_comment": "This is new comment"}}


@app.post("/update-comment", response_model=ResponseNewComment)
async def update_comment(pushed_json: InputNewComment):
    result_replace_comment = dao.DAO().update_the_comment(
        pushed_json.id_for_update, pushed_json.new_comment
    )
    return result_replace_comment


class ReadHwWithAnyParam(BaseModel):
    type_hw: int
    locate: int


class ReturnHwWithAnyParam(BaseModel):
    id_in_db: str
    type: str
    name: str
    ip: str
    locate: str
    comment: str


class ReturnHwWithAnyItems(BaseModel):
    items: Dict[str, ReturnHwWithAnyParam] = Field(..., description="Dictonary")

    class Config:
        schema_extra = {
            "example": {
                "items": {
                    "1": {
                        "id_in_db": "1",
                        "type": "2",
                        "name": "Cisco",
                        "ip": "192.168.1.0",
                        "locate": "27",
                        "comment": "This is comment",
                    }
                }
            }
        }


@app.get(
    "/read-hardware-from-base-with-any-parameters",
    response_model=ReturnHwWithAnyItems,
    description="If input type or locate = [0], then readind all type or location, all items is number row in DB",
)
async def read_hardware_with_any_param(pushed_json: ReadHwWithAnyParam):
    result_read_hw_with_any_param = dao.DAO().read_hardware_with_param(
        pushed_json.type_hw, pushed_json.locate
    )
    return {"items": result_read_hw_with_any_param}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
