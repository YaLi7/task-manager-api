# Kubernetes 部署说明

## 前置条件
- Minikube 集群已启动
- Docker 镜像 `task-manager-api:v1` 已构建
- Ingress 插件已启用

## 部署步骤

1. 应用所有资源清单：
   kubectl apply -f k8s/
2. 检查 Pod 状态：
   kubectl get pods -n task-manager
3. 检查 Service 状态：
   kubectl get svc -n task-manager
4. 检查 Ingress 状态：
   kubectl get ingress -n task-manager

## 验证
1. 获取 Minikube IP：
   minikube ip
2. 配置本地 hosts：
   echo "$(minikube ip) task-manager.local" | sudo tee -a /etc/hosts
3. 测试 API：
   curl http://task-manager.local/health
   curl http://task-manager.local/tasks

## 清理
   kubectl delete -f k8s/
