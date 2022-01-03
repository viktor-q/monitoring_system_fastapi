import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from modules.databaser import dao
from modules.pinger import pinger_all_network_with_threading

app = FastAPI()


@app.get("/")
async def start_page():
    return f"mainpage"


@app.get("/net-scaner")
async def net_scaner():
    return pinger_all_network_with_threading.net_scanner()


class PushToDb(BaseModel):
    hard_type: str
    hard_name: str
    hard_ip: str
    hard_place: str
    hard_comment: str

    # class Config:
    #     orm_mode = True


@app.post("/push-in-base")
async def create_hardware_unit(pushed_json: PushToDb):

    new_id = dao.DAO().create_hardware_unit_with_comment(
        pushed_json.hard_type,
        pushed_json.hard_name,
        pushed_json.hard_ip,
        pushed_json.hard_place,
        pushed_json.hard_comment,
    )

    return f"Устройство `{pushed_json.hard_name}` c id '{new_id}' теперь в базе"


# @app.post("/push-in-base")
# async def create_hardware_unit(hard_type, hard_name, hard_ip, hard_place, hard_comment):
#
#         new_id = dao.DAO().create_hardware_unit_with_comment(
#             hard_type, hard_name, hard_ip, hard_place, hard_comment
#         )
#
#         return f"Устройство `{hard_name}` c id '{new_id}' теперь в базе"


@app.post("/read-from-base-id")
async def read_from_base_with_id(input_id):
    result = dao.DAO().read_hardware_with_comment(input_id)
    return f"{result}"


# @app.get("/users/{user_id}")
# async def user(user_id: str):
#     return {"user_id": user_id}
#
# userlist = ["Spike", "Jet", "Ed", "Faye", "Ein"]
# @app.get("/userlist")
# async def userlist_(start: int = 0, limit: int = 10):
#     return userlist[start:start+limit]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
