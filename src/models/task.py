from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime
import uuid

class Task(BaseModel):
    """任务数据模型"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="任务唯一ID")
    title: str = Field(..., min_length=1, max_length=100, description="任务标题")
    description: str = Field(default="", max_length=500, description="任务描述")
    status: Literal["todo", "in_progress", "done"] = Field(default="todo", description="任务状态")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="创建时间")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="更新时间")
