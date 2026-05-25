# Kubernetes 故障排除指南

## 常见问题

### Pod 无法启动

**现象**：Pod 状态为 Pending 或 CrashLoopBackOff

**排查步骤**：
1. 检查资源配额：`kubectl describe pod <pod-name>`
2. 检查镜像是否可拉取
3. 检查 Init Container 是否成功执行
4. 查看事件：`kubectl get events`

### 服务无法访问

**现象**：Service 无法转发流量到 Pod

**排查步骤**：
1. 检查 Endpoints：`kubectl get endpoints <service-name>`
2. 验证 Pod 标签选择器
3. 检查网络策略
4. 验证 Service 类型

### 网络问题

**现象**：Pod 之间无法通信

**排查步骤**：
1. 检查网络策略配置
2. 验证 CNI 插件状态
3. 检查防火墙规则
4. 使用 `kubectl exec` 测试网络连通性

## 资源限制

### CPU 限制

```yaml
resources:
  limits:
    cpu: "1"
    memory: "512Mi"
  requests:
    cpu: "0.5"
    memory: "256Mi"
```

### 内存限制

OOM Killer 会在内存不足时杀死进程，需要合理设置资源限制。

## 日志查看

```bash
# 查看 Pod 日志
kubectl logs <pod-name>

# 查看最近日志
kubectl logs --tail=100 <pod-name>

# 查看所有容器日志
kubectl logs <pod-name> --all-containers
```

## 监控指标

- CPU 使用量
- 内存使用量
- 网络流量
- 磁盘 I/O

---
