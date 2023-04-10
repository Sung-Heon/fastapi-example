from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/hello")
def hello():
    return {"message": "안녕하세요 슈퍼코딩"}


@app.get("/items/{item_id}")
def read_item(item_id):
    return {"item_id": item_id}


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)