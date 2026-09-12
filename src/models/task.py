import uuid
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

# 任务状态类型
TaskStatus = Literal["todo", "in_progress", "done"]

# 基础任务模型（用于响应）
class Task(BaseModel):
    """完整的任务数据模型"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="任务唯一ID")
    title: str = Field(..., min_length=1, max_length=100, description="任务标题")
    description: str = Field(default="", max_length=500, description="任务描述")
    status: TaskStatus = Field(default="todo", description="任务状态")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")

# 创建任务时接收的请求体（id 和时间由后端生成，不需要客户端传）
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="任务标题")
    description: str = Field(default="", max_length=500, description="任务描述")
    status: TaskStatus = Field(default="todo", description="任务状态")

# 更新任务时接收的请求体（所有字段可选，只更新传了的字段）
class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="任务标题")
    description: Optional[str] = Field(None, max_length=500, description="任务描述")
    status: Optional[TaskStatus] = Field(None, description="任务状态")
