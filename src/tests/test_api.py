"""
Task Manager API 单元测试

覆盖健康检查、任务 CRUD 的核心逻辑。
使用 FastAPI 的 TestClient 进行测试。
"""
import pytest
from fastapi.testclient import TestClient

from src.main import app
from src import storage


@pytest.fixture(autouse=True)
def clean_storage():
    """每个测试用例前清空内存存储，避免测试之间互相干扰"""
    storage.tasks_db.clear()
    yield
    storage.tasks_db.clear()


@pytest.fixture
def client():
    """创建测试客户端"""
    return TestClient(app)


# ============ 健康检查 ============

def test_health_check(client):
    """健康检查应返回 200 和 status: ok"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# ============ 创建任务 ============

def test_create_task(client):
    """创建任务应返回 201 和完整任务信息"""
    response = client.post("/tasks", json={
        "title": "测试任务",
        "description": "这是一个测试任务",
        "status": "todo"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "测试任务"
    assert data["status"] == "todo"
    assert "id" in data
    assert "created_at" in data


def test_create_task_invalid_title(client):
    """创建任务时标题为空应返回 422（Pydantic 校验失败）"""
    response = client.post("/tasks", json={
        "title": "",
        "status": "todo"
    })
    assert response.status_code == 422


def test_create_task_invalid_status(client):
    """创建任务时状态不合法应返回 422"""
    response = client.post("/tasks", json={
        "title": "测试",
        "status": "invalid_status"
    })
    assert response.status_code == 422


# ============ 获取任务 ============

def test_get_tasks_empty(client):
    """初始状态下任务列表应为空"""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_get_task_by_id(client):
    """根据 ID 获取任务应返回 200"""
    create_resp = client.post("/tasks", json={"title": "测试任务"})
    task_id = create_resp.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_get_task_not_found(client):
    """获取不存在的任务应返回 404"""
    response = client.get("/tasks/non-existent-id")
    assert response.status_code == 404
    assert response.json()["detail"] == "任务不存在"


# ============ 更新任务 ============

def test_update_task(client):
    """更新任务应返回 200 且内容已变更"""
    create_resp = client.post("/tasks", json={"title": "原任务"})
    task_id = create_resp.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={
        "title": "更新后的任务",
        "status": "in_progress"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "更新后的任务"
    assert data["status"] == "in_progress"


def test_update_task_not_found(client):
    """更新不存在的任务应返回 404"""
    response = client.put("/tasks/non-existent-id", json={"title": "新标题"})
    assert response.status_code == 404


# ============ 删除任务 ============

def test_delete_task(client):
    """删除任务应返回 204"""
    create_resp = client.post("/tasks", json={"title": "待删除任务"})
    task_id = create_resp.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    # 确认已被删除
    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404


def test_delete_task_not_found(client):
    """删除不存在的任务应返回 404"""
    response = client.delete("/tasks/non-existent-id")
    assert response.status_code == 404
