import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.routes import tasks, health

# 配置日志（任务要求：包含日志输出）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Task Manager API",
    description="一个简单的任务管理 API 服务",
    version="1.0.0"
)

# 注册路由
app.include_router(health.router)
app.include_router(tasks.router)

# 全局请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("请求: %s %s", request.method, request.url.path)
    response = await call_next(request)
    logger.info("响应: %s", response.status_code)
    return response

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("服务器错误: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误"}
    )

# 根路径
@app.get("/")
def read_root():
    return {"message": "Task Manager API is running", "docs": "/docs"}
