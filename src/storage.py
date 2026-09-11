from typing import Dict, List, Optional
from src.models.task import Task

# 内存存储：用字典模拟数据库
# key 是 task_id，value 是 Task 对象
tasks_db: Dict[str, Task] = {}

def get_all_tasks() -> List[Task]:
    """获取所有任务列表"""
    return list(tasks_db.values())

def get_task(task_id: str) -> Optional[Task]:
    """根据 ID 获取单个任务"""
    return tasks_db.get(task_id)

def create_task(task: Task) -> Task:
    """创建新任务"""
    tasks_db[task.id] = task
    return task

def update_task(task_id: str, task: Task) -> Optional[Task]:
    """更新任务"""
    if task_id in tasks_db:
        tasks_db[task_id] = task
        return task
    return None

def delete_task(task_id: str) -> bool:
    """删除任务"""
    if task_id in tasks_db:
        del tasks_db[task_id]
        return True
    return False
