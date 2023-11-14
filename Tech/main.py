from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from routes.access_data import list_data

words = FastAPI(
    title="The Longest Word",
    description="This API find the longest word in a list, aditional you can CRUD the DB with Mongo!!! Enjoy it!"
)
words.include_router(list_data)

class Item(BaseModel):
    Items: list

@words.get("/", tags=["Longest"])
def Init():
    return "App en servicio"


if __name__ == "__main__":
    uvicorn.run("main:words", host="127.0.0.1", reload=True)