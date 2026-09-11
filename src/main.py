from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, Task Manager API!"}
# 项目入口文件 - 后续将拆分为 routes 模块
