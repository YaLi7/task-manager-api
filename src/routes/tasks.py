from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime

from src.models.task import Task, TaskCreate, TaskUpdate
from src import storage

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("", response_model=List[Task])
def get_tasks():
    """获取所有任务列表"""
    return storage.get_all_tasks()

@router.get("/{task_id}", response_model=Task)
def get_task(task_id: str):
    """根据 ID 获取单个任务"""
    task = storage.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task

@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate):
    """创建新任务"""
    new_task = Task(**task_data.model_dump())
    return storage.create_task(new_task)

@router.put("/{task_id}", response_model=Task)
def update_task(task_id: str, task_data: TaskUpdate):
    """更新任务内容"""
    existing_task = storage.get_task(task_id)
    if not existing_task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    # 只更新传了的字段
    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_task, key, value)
    
    # 更新时间戳
    existing_task.updated_at = datetime.utcnow()
    return storage.update_task(task_id, existing_task)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    """删除任务"""
    if not storage.delete_task(task_id):
        raise HTTPException(status_code=404, detail="任务不存在")
    return None
