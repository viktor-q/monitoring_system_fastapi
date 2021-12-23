import uvicorn
from fastapi import FastAPI
from modules.pinger import pinger_all_network_with_threading


app = FastAPI()

@app.get("/")
async def start_page():
    return f'mainpage'

@app.get("/net-scaner")
async def net_scaner():
    return pinger_all_network_with_threading.net_scanner()

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
