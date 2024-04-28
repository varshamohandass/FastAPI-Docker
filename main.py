from fastapi import FastAPI, Query
from pydantic import BaseModel
import json

app=FastAPI()

db = "data.json"

class Item(BaseModel):
  sno: int
  desc: str = None 
  # lst: list[int] = None

class UpdateItem(BaseModel):
  sno: int
  desc: str = None

# class ItemList(BaseModel):
#   itemList: List
# adding a comment to check if jenkins connection is working or not
@app.get("/")
def index():  
  items = read_items_from_db()
  return items


@app.get("/root")
def root():  
  return "this is the root end point"
  
  

@app.get("/items/{item_id}")
async def get_item(item_id:int):
    items = read_items_from_db()
    for item in items:
      if item['sno'] == item_id:
        return item
    else:
      return f"item{item_id} not found"
    
# @app.post("/multiple_items", response_model=List[Item])
# async def post_list(item_list : List[Item]):
#   # for item in item_list:
#   #   items = get_item(item)
#   for item in item_list:
#     items = read_items_from_db()
#     items.append(item.model_dump())
#     store_item_to_db(items)
#   return item_list
    

# @app.get("/multiple-items/",response_model=List[Item])
# async def get_multiple_item(item_lst:List[ItemList] | None):
    
#     items = read_items_from_db()
#     for item_id in item_lst:      
#       for item in items:
#         if item['sno'] == int(item_id):
#           return item    
#         else:
#           return f"item{item_id} not found"
    
# @app.post("/multiple_item/")
# async def get_multiple_item(item:Item):
#     items = read_items_from_db
#     lst = item['lst']
#     new_list = []
#     for i in lst:
#       for item in items:
#         if i == item['sno']:
#           new_list = new_list.append(item)
#     return new_list
    
    

@app.post("/items/")
async def store_item_to_db(item:Item):
  items = read_items_from_db()
  items.append(item.model_dump())
  store_item_to_db(items)
  return{"result":item}

def read_items_from_db():
  try:
    with open(db,'r')as file:
      items = json.load(file)
  except FileNotFoundError:
    items = []
  return items

def store_item_to_db(data):
  with open(db, 'w') as file:
    json.dump(data,file,indent = 2)

@app.delete("/delete-items")
async def delete_all_items_from_db():
  items = read_items_from_db()
  items.clear()
  store_item_to_db(items)
  return items

@app.delete("/items/{item_id}")
async def delete_item_from_db(item_id:int):
  items = read_items_from_db()
  for item in items:
    if item['sno'] == item_id:
      items.remove(item)
      store_item_to_db(items)
      return f'{item} has been deleted'
  else:
    return f'item{item_id} not found'
  


  
@app.put("/items/{item_id}")
async def change_item_in_db(item:UpdateItem, item_id:int):
  items = read_items_from_db()
  for db_item in items:
    if db_item['sno'] == item_id:
      db_item['desc'] = item.desc
  store_item_to_db(items)

      

    
