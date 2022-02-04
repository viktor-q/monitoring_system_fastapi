from typing import Dict, Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel, Field

from modules.databaser import dao
from modules.pinger import pinger_all_network_with_threading
from modules.security import security
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

#search this!11
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
#Authorize: AuthJWT = Depends()
async def net_scaner() -> dict:
#    Authorize.jwt_required()

    result = pinger_all_network_with_threading.net_scanner()
    return {"items": result}


class PushToDb(BaseModel):
    hard_type: int
    hard_name: str
    hard_ip: str
    hard_place: int
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
    id_in_db: int
    type: int
    name: str
    ip: str
    locate: int
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


class Settings(BaseModel):
    authjwt_secret_key: str = "secret"


@AuthJWT.load_config
def get_config():
    return Settings()

class User(BaseModel):
    login: str
    password: str

class ReturnLoginUser(BaseModel):
    access_token: str

    class Config:
        schema_extra = {"access_token": "blabla123bla456"}


@app.get("/login-user", response_model=ReturnLoginUser)
async def login_user(data: User, Authorize: AuthJWT = Depends()) -> dict:
    new_class = security.CustomSecurity()
    response_check_pass_in_db = new_class.check_user(data.login, data.password)
    if response_check_pass_in_db["status_pass"] == "BAD":
        raise HTTPException(status_code=401, detail="Bad username or password")

    access_token = Authorize.create_access_token(subject=data.login)
    return {"access_token": access_token}


@app.get("/create-user")
async def create_user(data: User):
    new_class = security.CustomSecurity()
    new_user_id = new_class.registration_new_user(data.login, data.password)
    return {"new_user_id": new_user_id}


# exception handler for authjwt
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
