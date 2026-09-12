# Kubernetes 部署说明

本文档描述如何在本地 Minikube 集群中部署 Task Manager API 服务。

---

## 前置条件

- Minikube 集群已启动（`--driver=docker` 模式）
- Docker 镜像 `task-manager-api:v1` 已构建
- `kubectl` 已正确配置并连接到 Minikube 集群

---

## 一、启动 Minikube 集群

一、将构建的好的本地 task-manager-api 镜像加载到 Minikube里
1. 加载镜像到 Minikube
``` bash
minikube image load task-manager-api:v1
```
> 说明：Minikube 运行在独立容器中，拥有自己的容器运行时，不会自动看到宿主机上构建的镜像。必须使用 minikube image load 手动加载。

2. 验证镜像已加载
``` bash
minikube ssh -- sudo crictl images | grep task-manager-api
```
## 二、部署 Ingress Controller
由于国内网络访问 registry.k8s.io 不稳定，minikube addons enable ingress 会出现镜像拉取失败。
采用手动部署官方 manifest 的方式：

1. 拉取镜像并重命名
```bash
docker pull k8s.mirror.nju.edu.cn/ingress-nginx/controller:v1.13.2
docker pull k8s.mirror.nju.edu.cn/ingress-nginx/kube-webhook-certgen:v1.6.2

docker tag k8s.mirror.nju.edu.cn/ingress-nginx/controller:v1.13.2 registry.k8s.io/ingress-nginx/controller:v1.13.2
docker tag k8s.mirror.nju.edu.cn/ingress-nginx/kube-webhook-certgen:v1.6.2 registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.6.2
```
2. 加载镜像到 Minikube
```bash
minikube image load registry.k8s.io/ingress-nginx/controller:v1.13.2
minikube image load registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.6.2
```
3. 下载官方部署文件并修改镜像地址
```bash
wget https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.13.2/deploy/static/provider/cloud/deploy.yaml -O nginx-ingress-deploy.yaml

# 去掉 SHA256 哈希，否则 K8s 会坚持远程拉取

sed -i 's|image: .*/controller:v1.13.2@sha256:.*$|image: registry.k8s.io/ingress-nginx/controller:v1.13.2|' nginx-ingress-deploy.yaml
sed -i 's|image: .*/kube-webhook-certgen:v1.6.2@sha256:.*$|image: registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.6.2|g' nginx-ingress-deploy.yaml

# 确认文件内此项设置存在，意思为优先本地镜像
imagePullPolicy: IfNotPresent 
```
4. 部署 Ingress Controller
```bash
kubectl apply -f k8s/nginx-ingress-deploy.yaml
```
5. 验证 Ingress Controller 状态
```bash
kubectl get all -n ingress-nginx
```
<img width="1156" height="271" alt="image" src="https://github.com/user-attachments/assets/b45b7257-75f7-4395-90e6-ebeed481dcca" />



## 三、部署应用资源
1. 应用所有资源清单
``` bash
kubectl apply -f k8s/
```
2. 检查资源状态
```bash
kubectl get all -n task-manager
```
<img width="792" height="278" alt="image" src="https://github.com/user-attachments/assets/038b916d-7823-45cf-bca5-1fddbac9ecb2" />

## 四、通过域名访问（本地验证）
> **说明**：在 docker 驱动的 Minikube 环境中，Ingress Controller 的 LoadBalancer 类型 Service
> 只会将端口（NodePort）绑定在 Minikube 容器内部的 IP（如 192.168.49.2）上，
> **不会映射到宿主机的任何端口**。因此从宿主机无法直接访问 `task-manager.local`。
>
> 为了模拟真实云环境中 LoadBalancer 提供外部入口的行为，这里使用 `kubectl port-forward`
> 将宿主机的 80 端口转发到 Ingress Controller，从而让域名路由完整生效。

1. 配置 hosts 文件
```bash
echo "127.0.0.1 task-manager.local" | sudo tee -a /etc/hosts
```
2. 以 root 身份启动端口转发（保持终端不关）
```bash
kubectl --kubeconfig=/home/minikube-user/.kube/config port-forward -n ingress-nginx svc/ingress-nginx-controller 80:80 --address 0.0.0.0
```
<img width="1422" height="252" alt="image" src="https://github.com/user-attachments/assets/fe3dddf3-7fe4-4251-86e3-beccf0fb5f9a" />

3. 新开一个终端，测试 API
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


## 五、资源清单说明

<img width="698" height="221" alt="image" src="https://github.com/user-attachments/assets/969c4c4f-dca0-4f1a-aca9-cc599f5a2772" />

目录结构：

k8s/
├── configmap.yaml
├── deployment.yaml
├── ingress.yaml
├── namespace.yaml
├── nginx-ingress-deploy.yaml
├── README.md
└── service.yaml

## 六、清理资源

**删除应用资源**
```bash
kubectl delete -f k8s/
```
**删除 Ingress Controller**
```bash
kubectl delete -f nginx-ingress-deploy.yaml
```
**停止 Minikube**
```bash
minikube stop
```
**删除 Minikube 集群**）
```bash
minikube delete
```
## 七、常见问题与解决方案
#### 问题 1：Pod 卡在 ImagePullBackOff
> 原因：Minikube 内部找不到镜像。

**解决方案**：
```bash
minikube image load task-manager-api:v1
```

***

#### 问题 2：Ingress Controller 镜像拉取失败
> 原因：国内网络访问 registry.k8s.io 超时，且官方 manifest 中的镜像地址带有 SHA256 哈希。

**解决方案**：见本文档「三、部署 Ingress Controller」章节。

***

#### 问题 3：curl http://task-manager.local/health 连接被拒绝
> 原因：
> 在 docker 驱动的 Minikube 环境中，Ingress Controller 的 LoadBalancer 类型 Service
> 只会将端口（NodePort）绑定在 Minikube 容器内部的 IP上，
> 不会映射到宿主机的任何端口**。因此从宿主机无法直接访问 

**解决方案**：
添加 hosts 为 127.0.0.1 task-manager.local
使用 kubectl port-forward ... 80:80 建立隧道

***
