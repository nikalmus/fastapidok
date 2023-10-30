from enum import Enum
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Category(Enum):
    TOOLS = 'tools'
    CONSUMABLES = 'consumables'

class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category

class UpdateItem(BaseModel):
    name: str | None = None
    price: float | None = None
    count: int | None = None
    category: Category | None = None

items = {
    0: Item(name="Hammer", price=9.99, count=20, id=0, category=Category.TOOLS),
    1: Item(name="Pliers", price=5.99, count=20, id=1, category=Category.TOOLS),
    2: Item(name="Nails", price=1.99, count=100, id=2, category=Category.CONSUMABLES),
}

@app.get("/")
def index() -> dict[str, dict[int, Item]]:
    return {"items": items}

@app.get("/items/{item_id}")
def get_item_by_id(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

#Function parameters that are not path parameters are query parameters, e.g. ?name=Hammer
Selection = dict[
    str, str | int | float | Category | None
    #dict containing the name of the query parameter as key and the type of the value as value
]


@app.get("/items/")
def get_item_by_params(
    name: str | None = None,
    price: float | None = None,
    count: int | None = None,
    category: Category | None = None,
) -> dict[str, Selection | list[Item]]:
    def check_item(item: Item):
        """Check if the item matches the query parameters"""
        return all(
            (
                name is None or item.name == name,
                price is None or item.price == price,
                count is None or item.count == count,
                category is None or item.category == category,
            )
        )
    selection = [item for item in items.values() if check_item(item)]
    return {
        "query": {
            "name": name,
            "price": price,
            "count": count,
            "category": category,
        },
        "selection": selection
        }

@app.post("/")
def add_item(item: Item) -> dict[str, Item]:

    if item.id in items:
        HTTPException(status_code=400, detail=f"Item with {item.id=} already exists.")

    items[item.id] = item
    return {"added": item}

# @app.put("/update/{item_id}")
# def update_item(
#     item_id: int,
#     name: str | None = None,
#     price: float | None = None,
#     count: int | None = None,
#     category: Category | None = None,
# ) -> dict[str, Item]:
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
#     item = items[item_id]
#     if name is not None:
#         item.name = name
#     if price is not None:
#         item.price = price
#     if count is not None:
#         item.count = count
#     if category is not None:
#         item.category = category
#     return {"updated": item}

# @app.put("/update/{item_id}")
# def update_item(
#     item_id: int,
#     request: Request,  #<-- get the request body
#     name: str | None = None, 
#     price: float | None = None,
#     count: int | None = None,
#     category: Category | None = None
# ) -> dict[str, Item]:
#     if item_id not in items:
#         raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
#     item = items[item_id]
#     print("UPDATE")

#     # Check query params for updates  
#     try:
#         if name is not None:
#             item.name = name
#         if price is not None:
#             item.price = price
#         if count is not None:
#             item.count = count
#         if category is not None:
#             item.category = category

#         return {"updated": item}
#     except Exception as e:
#         print("Error updating item:", e)
#         raise e

@app.put("/update/{item_id}")
def update_item(
    item_id: int,
    update_data: UpdateItem  # Use the Pydantic model as the request body
) -> dict[str, Item]:
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    item = items[item_id]

    # Update the item with data from the request body
    for field, value in update_data.dict().items():
        if value is not None:
            setattr(item, field, value)

    return {"updated": item}

@app.delete("/delete/{item_id}")
def delete_item(item_id: int) -> dict[str, Item]:
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    
    item = items[item_id]
    del items[item_id]
    return {"deleted": item}
