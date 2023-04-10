from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/hello")
def hello():
    return {"message": "안녕하세요 슈퍼코딩"}


@app.get("/items/{item_id}")
def read_item(item_id):
    return {"item_id": item_id}


@app.get("/int-items/{item_id}")
def read_item_int_only(item_id:int):
    return {"int-item_id": item_id}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)