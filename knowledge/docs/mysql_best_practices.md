# MySQL 最佳实践

## 连接池配置

### 推荐配置

```ini
[mysqld]
max_connections = 151
wait_timeout = 60
interactive_timeout = 60
```

### 应用层配置

- 设置合理的最大连接数
- 实现连接复用
- 设置连接超时时间

## 查询优化

### 索引优化

1. 为经常查询的字段创建索引
2. 避免在索引列上使用函数
3. 复合索引遵循最左前缀原则

### 查询分析

```sql
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

## 慢查询日志

### 启用慢查询日志

```ini
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2
```

### 分析慢查询

```bash
mysqldumpslow /var/log/mysql/slow.log
```

## 主从复制

### 配置要点

1. 确保主从版本一致
2. 配置半同步复制
3. 监控复制延迟

### 故障切换

1. 确认主库不可用
2. 提升从库为主库
3. 更新应用连接配置

## 备份策略

### 全量备份

```bash
mysqldump -u root -p --all-databases > backup.sql
```

### 增量备份

使用二进制日志进行增量备份。

## 监控指标

- 连接数
- 查询响应时间
- 慢查询数量
- 复制延迟

---
