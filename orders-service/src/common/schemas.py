from pydantic import BaseModel


class Order(BaseModel):
    id: str
    item: str
    quantity: int
    price: float

class Product(BaseModel):
    id: str 
    name: str
    price: float

class BusketItem(BaseModel):
    product_id: str
    quantity: int


class Busket(BaseModel):
    items: list[BusketItem]    