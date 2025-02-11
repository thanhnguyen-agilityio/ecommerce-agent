from pydantic import BaseModel, conlist
from typing import Literal

from typing import Literal
from pydantic import BaseModel, conlist

# Generate allowed color codes from "000" to "074"
AllowedColor = Literal[*(f"{i:03}" for i in range(75))]  # '000' to '074'
AllowedSize = Literal["XS", "S", "M", "L", "XL", "XXL"]

class ProductInList(BaseModel):
    """
    Represents the data structure of a Product in list.
    """
    # name: str
    url: str


class Product(BaseModel):
    """
    Represents the data structure of a Product.
    """
    uuid: str
    name: str
    description: str
    price: float
    colors: conlist(AllowedColor, min_length=1)
    sizes: conlist(AllowedSize, min_length=1)
    category: str
    thumbnail: str
    url: str
    quantity: int

