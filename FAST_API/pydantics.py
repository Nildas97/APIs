# HOW TO VALIDATE EXTERNAL MESSY DATA USING PYDANTIC

# importing libraries
from pydantic import BaseModel, field_validator
from typing import List, Optional
import json


def Pydantic():  # pydantic small intro
    """
    Pydantic is the data validation we need in Python. 
    It allows us to define a model and set the data types for each field, 
    making it not only easier to work with in our IDE but also checking the types at runtime, 
    which is something that is not in Python as standard.
    I've found that it helps when dealing with any external data 
    that we would want to process in our applications, 
    like user submitted data or data from files we have received outside our own ecosystem.
    """
    pass


# creating second class variant for sub categories inside product
class variant(BaseModel):
    name: str
    sku: str
    available: bool
    price: float

    # validating data
    @field_validator("sku")
    def sku_length(cls, value):
        if len(value) != 7:
            raise ValueError('sku must be 7 chars.')

        return value


class Product(BaseModel):  # creating main class Product
    id: int
    title: str
    variants: Optional[List[variant]]


# opening the external data
with open('data.json') as f:
    data = json.load(f)
    items = [Product(**item) for item in data['results']]

print(items)
print(items[0].variants[1].name)

# testing data
# item = Product(
#     id=123123,
#     title="cool shirt",
#     variants=[
#         variant(
#             name="small",
#             sku="abcabc",
#             available=True,
#             price=24.88
#         ),
#         variant(
#             name="medium",
#             sku="xyzxyz",
#             available="False",
#             price=27
#         )
#     ]
# )
# print(item)
