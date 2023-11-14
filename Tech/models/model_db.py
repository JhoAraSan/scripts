from pydantic import BaseModel

class Dict_list(BaseModel):
    id: str
    lt: list
    answer: dict

class Item(BaseModel):
    Items: list