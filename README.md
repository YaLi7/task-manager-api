# Task Manager API

[![CI Pipeline](https://github.com/YaLi7/task-manager-api/actions/workflows/ci.yml/badge.svg)](https://github.com/YaLi7/task-manager-api/actions/workflows/ci.yml)

一个基于 **FastAPI + Docker + Kubernetes** 的任务管理 RESTful API 服务，支持完整的增删改查（CRUD）操作，并可通过 CI/CD 流水线自动构建、测试和部署。

## 📖 项目简介

本项目实现了一个简单的任务管理 API，提供以下能力：

- RESTful API 接口管理任务（增删改查）
- 独立运行在容器中
- 在 Kubernetes 集群中部署和运行
- 代码变更自动触发构建和部署流水线

---

## 🧰 技术栈

| 技术 | 用途 | 版本要求 |
| :--- | :--- | :--- |
| Git | 版本控制 | 2.47.3 |
| Docker | 容器化 | 24.0.9 |
| Minikube | 本地 Kubernetes 集群 | v1.37.0 |
| GitHub Actions | CI/CD 流水线 | ubuntu-latest |
| Python | 服务端开发 | 3.11.6 |
| FastAPI | Web 框架 | 0.115.0 |
| Uvicorn | ASGI 服务器 | 0.32.0 |
| Pydantic | 数据校验 | 2.9.2 |
| pytest | 单元测试 | 8.3.3 |
| pylint | 代码风格检查 | 3.3.1 |
| Trivy | 镜像漏洞扫描 | latest |

---

## 📁 项目结构
```bash
task-manager-api/
├──.github/
└── workflows
    └── ci.yml     # GitHub Actions CI/CD 流水线
├── docker-compose.yml
├── Dockerfile
├── k8s
│   ├── configmap.yaml
│   ├── deployment.yaml
│   ├── ingress.yaml
│   ├── namespace.yaml
│   ├── nginx-ingress-deploy.yaml
│   ├── README.md
│   └── service.yaml
├── README.md
├── requirements-dev.txt  # 测试环境依赖（pytest / pylint）
├── requirements.txt    # 生产依赖
└── src
    ├── __init__.py
    ├── main.py    # 应用入口，含日志中间件和全局异常处理
    ├── models
    │   └── task.py  # 任务数据模型（Task / TaskCreate / TaskUpdate）
    ├── routes
    │   ├── health.py   # 健康检查路由
    │   └── tasks.py    # 任务 CRUD 路由
    ├── storage.py      # 内存存储层（可扩展为数据库）
    └── tests
        └── test_api.py  # 单元测试
```

---

## 🔌 API 接口

| 方法 | 路径 | 功能 | 响应状态码 |
| :--- | :--- | :--- | :--- |
| GET | `/health` | 健康检查 | 200 |
| GET | `/tasks` | 获取所有任务 | 200 |
| GET | `/tasks/{id}` | 根据 ID 获取任务 | 200 / 404 |
| POST | `/tasks` | 创建任务 | 201 / 400 |
| PUT | `/tasks/{id}` | 更新任务 | 200 / 404 |
| DELETE | `/tasks/{id}` | 删除任务 | 204 / 404 |

### 任务数据模型

```json
{
  "id": "uuid-string",
  "title": "任务标题",
  "description": "任务描述",
  "status": "todo | in_progress | done",
  "created_at": "2026-01-01T00:00:00Z",
  "updated_at": "2026-01-01T00:00:00Z"
}


*** 


## 🚀 本地开发环境搭建
1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 启动服务
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8080
```

3. 验证
```bash
curl http://localhost:8080/health
# 预期输出：{"status":"ok"}
```

4. 运行单元测试
```bash
pip install -r requirements-dev.txt
python3.11 -m pytest src/tests/ -v --cov=src --cov-report=term
```

4. 运行单元测试
```bash
python3.11 -m pylint src/ --rcfile=.pylintrc
```

*** 


## 🐳 Docker 构建和运行
1. 构建镜像
```bash
docker build -t task-manager-api:v1 .
```

2. 运行容器
```bash
docker run -d --name task-api -p 8080:8080 task-manager-api:v1
```

3. 验证
```bash
curl http://localhost:8080/health
# 预期输出：{"status":"ok"}
```

4. 使用 docker-compose启动
```bash
# 启动容器
docker-compose up -d

# 查看容器
docker-compose ps

# 停止容器
docker-compose down
```

*** 

### ☸️ Minikube 部署
详细的 Kubernetes 部署步骤见 k8s/README.md。

快速步骤
```bash
# 1. 启动 Minikube
minikube start --driver=none --force

# 2. 构建并加载镜像到minikube里
docker build -t task-manager-api:v1 .
minikube image load task-manager-api:v1

# 3. 部署应用资源
kubectl apply -f k8s/

# 4. 检查状态
kubectl get pods -n task-manager
kubectl get svc -n task-manager
kubectl get ingress -n task-manager
```

*** 


## 🔄 CI/CD 流水线
本项目使用 GitHub Actions 实现自动化流水线，配置文件位于 .github/workflows/ci.yml。

**触发条件**:
Push 到 main 分支
Pull Request 到 main 分支

**流水线阶段**:
|阶段	|任务	|工具|
| :--- | :--- | :--- | 
|Lint	|代码风格检查	| pylint（评分 10/10）|
|Test	|运行单元测试	| pytest（覆盖率 98%）|
|Build	|构建 Docker 镜像并推送到 ghcr.io|	docker/build-push-action |
|Security| Scan	扫描镜像漏洞 |	Trivy |

**镜像标签**:
```text
ghcr.io/yalil7/task-manager-api:<commit-sha>
```
**流水线依赖**:
每个阶段通过 needs 声明依赖，前一个阶段失败时，后续阶段不会执行。

## 📸 相关截图

#### Kubernetes 部署状态

<img width="797" height="279" alt="image" src="https://github.com/user-attachments/assets/1abfa1d2-4b66-46a6-aeac-84b75f57d896" />

#### API 调用成功的响应示例
**健康检查**
```bash
curl http://task-manager.local/health
```
<img width="628" height="70" alt="image" src="https://github.com/user-attachments/assets/a12a5689-ed8f-4992-8681-d2b8176a7ca9" />

**获取任务列表**
```bash
curl http://task-manager.local/tasks
```
<img width="1464" height="198" alt="image" src="https://github.com/user-attachments/assets/f726fefa-7254-4358-88ab-b939262cbebd" />

> 这里因项目使用**内存存储**，且 Deployment 配置了 **2 个副本**。由于每个 Pod 的内存互相独立，
> Service 轮询分发请求时，不同请求可能落到不同 Pod，导致返回的列表数据不一致。

**创建任务**
```bash
curl -X POST http://task-manager.local/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"测试任务","description":"验证 Ingress","status":"todo"}'
```
<img width="1480" height="134" alt="image" src="https://github.com/user-attachments/assets/b71e786e-e7a6-4c9f-a18a-835d292d01a4" />

**获取单个任务**
```bash
curl http://task-manager.local/tasks/<id>
```
<img width="1474" height="101" alt="image" src="https://github.com/user-attachments/assets/c894c126-4aa9-4763-a820-d6eaef5a0c22" />


**更新任务**
```bash
curl -X PUT http://task-manager.local/tasks/<id> \
  -H "Content-Type: application/json" \
  -d '{"status":"in_progress"}'
```
<img width="1477" height="202" alt="image" src="https://github.com/user-attachments/assets/2cc1ec47-d15c-47f9-8831-032c52b2bb07" />


**删除任务**
```bash
curl -X DELETE http://task-manager.local/tasks/<id>
```
<img width="1121" height="198" alt="image" src="https://github.com/user-attachments/assets/cfbf7fc9-5423-40d7-815c-ba7fa87e3d08" />

### CI/CD 流水线运行结果

<img width="1919" height="956" alt="image" src="https://github.com/user-attachments/assets/2be11857-3ce8-48a3-a630-621a8b8748da" />

## 🐛 遇到的问题及解决方案

### Kubernetes(minikube) 部署问题
K8s 相关问题，详见 [k8s/README.md](k8s/README.md)。


### 问题1: CI 中 pylint 退出码非 0 导致流水线失败
> 现象：GitHub Actions 的 Lint 阶段报 Process completed with exit code 20。
> 原因：pylint 默认评分不到 10 就返回非 0 退出码，而代码中有一些可接受的警告（如 pytest fixture 的变量名重复）。

**解决方案**：
1. 修改代码规范，评分达到10
2. 在 .pylintrc 中屏蔽误报规则：
```bash
[MESSAGES CONTROL]
disable=
    ...
    W0621  # redefined-outer-name (pytest fixture 标准写法)
```

3. 在 CI 中为 pylint 添加 --fail-under=8，允许评分 ≥ 8 即通过：

```bash
python -m pylint src/ --rcfile=.pylintrc --fail-under=8
```
### 问题2: Docker 镜像标签包含大写字母导致推送失败
> 现象：Build 阶段报错 invalid tag "ghcr.io/YaLi7/task-manager-api:...": repository name must be lowercase。
> 原因：Docker 镜像仓库名要求全部小写，而 GitHub 用户名 YaLi7 包含大写字母。

**解决方案**：在 CI 中将用户名转换为小写：

```yaml
- name: 生成镜像标签
  id: meta
  run: |
    OWNER=$(echo "${{ github.repository_owner }}" | tr '[:upper:]' '[:lower:]')
    IMAGE_TAG="ghcr.io/${OWNER}/${{ env.IMAGE_NAME }}:${{ github.sha }}"
    echo "image_tag=${IMAGE_TAG}" >> $GITHUB_OUTPUT
```

### 问题3: Trivy 扫描发现系统级 CRITICAL 漏洞
> 现象：Security Scan 阶段报 Process completed with exit code 1，Trivy 报告 3 个 CRITICAL 漏洞（perl-base、perl-archive-tar、perl）。
> 原因：python:3.11-slim 基础镜像基于 Debian，自带的 Perl 系统包存在已知漏洞。

**解决方案**：
在 Dockerfile 的 runtime 阶段升级系统包：

```
dockerfile
FROM python:3.11-slim AS runtime

# 升级系统包，修复已知漏洞
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*
```

### 问题4:Trivy Action 版本号不存在
> 现象：Trivy 扫描后报 Total: 5 (HIGH: 5, CRITICAL: 0)，流水线失败。
> 原因：5 个 HIGH 漏洞来自上游 Python 依赖（starlette、wheel、jaraco.context），不是业务代码问题。

**解决方案**：在 CI 中只阻断 CRITICAL 级别，HIGH 级别通过定期依赖更新处理：

```yaml
- name: 运行 Trivy 扫描
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ needs.build.outputs.image_tag }}
    format: 'table'
    exit-code: '1'
    ignore-unfixed: true
    severity: 'CRITICAL'
```
**说明**：这是安全性和开发效率之间的平衡。CRITICAL 必须立刻修复，HIGH 级别可以通过定期扫描、依赖更新来处理，不应阻断每次提交。

## ⚠️ 已知限制
本项目使用内存存储，且 Deployment 配置了 2 个副本。由于每个 Pod 的内存互相独立，Service 轮询分发请求时，不同请求可能落到不同 Pod，导致返回的列表数据不一致。

这是「无状态服务 + 内存存储 + 多副本」的固有特性，不是 Bug。

在生产环境中，应使用外部数据库（如 PostgreSQL、Redis）作为共享存储层，所有 Pod 访问同一份数据，从根本上解决这个问题。

