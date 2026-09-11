from fastapi import APIRouter

router = APIRouter(tags=["health"])

@router.get("/health", status_code=200)
def health_check():
    """健康检查端点，返回服务状态"""
    return {"status": "ok"}
