# AI Ops Mind - 智能运维助手平台 v2.0

> **产品定位**：面向生产环境的 AI 运维闭环平台。主动感知告警、智能分析根因、生成可信报告、自动沉淀知识，将运维从"救火模式"升级为"预防模式"。

## 核心功能

### 🚨 主动告警接入
- Webhook 网关（支持 Prometheus AlertManager、钉钉、飞书）
- 自动分诊引擎（P0/P1/P2/P3 级别路由）
- 幂等去重（Redis TTL 机制）
- 定时巡检调度

### 🔍 智能分析引擎
- 日志根因分析
- 多服务关联分析
- 告警聚合诊断
- 置信度评分（高/中/低）

### 📋 RCA 报告
- 自动触发生成
- 时间线梳理
- 来源引用标注
- Markdown 格式输出

### 📚 知识库闭环
- 历史案例检索（RAG）
- 分析结果自动沉淀
- 专家反馈校正
- 知识版本管理

### 💬 交互层
- SSE 流式对话
- 多轮上下文记忆
- 人工审批流
- 钉钉/飞书通知推送

## 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend                              │
│   HTML + CSS + JavaScript (暗色主题)                        │
├─────────────────────────────────────────────────────────────┤
│                     API Gateway                            │
│   FastAPI (路由 / JWT / 限流 / SSE)                         │
├─────────────────────────────────────────────────────────────┤
│                      Service Layer                         │
│   Chat / Log Analyzer / Alert Diagnoser / RCA Generator    │
│   Triage Engine / Webhook Handler / Notifier               │
├─────────────────────────────────────────────────────────────┤
│                        AI Layer                            │
│   LLM Adapter / RAG Engine / Prompt Manager                │
│   Confidence Scorer                                        │
├─────────────────────────────────────────────────────────────┤
│                       Data Layer                           │
│   ChromaDB (向量) / SQLite/PG (关系) / Redis (队列)         │
└─────────────────────────────────────────────────────────────┘
```

## 技术选型

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | HTML + CSS + JavaScript | 现代暗色主题，可嵌入 |
| 后端 | FastAPI (Python 3.11+) | 原生异步、SSE 支持、自动文档 |
| LLM | OpenAI-compatible API | 兼容 OpenAI / DeepSeek / Qwen / Ollama |
| 向量库 | ChromaDB | 零配置、内嵌式 |
| 数据库 | SQLite / PostgreSQL | 会话持久化、案例存储 |
| 队列 | Redis | 告警队列、幂等去重 |
| 调度 | APScheduler | 定时巡检 |
| 部署 | Docker + K8s | 一键部署、弹性伸缩 |

## 快速开始

### 环境要求

- Python 3.11+
- Redis 7.0+
- Docker (可选)

### 安装依赖

```bash
cd ai-ops-mind
pip install -r requirements.txt
```

### 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，配置 API Key 等参数
```

### 启动服务

```bash
# 方式1：直接运行
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 方式2：使用 Makefile
make run

# 方式3：使用 Docker Compose
docker-compose up -d
```

### 访问服务

- API 文档：http://localhost:8000/docs
- 前端界面：http://localhost:8000/static/index.html
- 健康检查：http://localhost:8000/api/health
- 指标端点：http://localhost:8000/api/metrics

<img width="1515" height="1247" alt="image" src="https://github.com/user-attachments/assets/09e05ce6-aa96-4beb-9a13-a40a613319da" />
<img width="2362" height="1157" alt="image" src="https://github.com/user-attachments/assets/d0430c51-8eaa-49c0-a4c3-c9c2d0ab129b" />


## API 接口

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/webhook/alert` | 接收外部告警推送 |
| POST | `/api/chat/stream` | 流式对话 |
| POST | `/api/analyze` | 日志智能分析 |
| POST | `/api/alert` | 告警聚合诊断 |
| POST | `/api/rca` | 生成 RCA 报告 |
| POST | `/api/feedback` | 提交分析反馈 |
| POST | `/api/knowledge/upload` | 上传知识文档 |
| GET | `/api/knowledge/search` | 知识库检索 |
| GET | `/api/metrics` | Prometheus 指标 |
| GET | `/api/health` | 健康检查 |

## 项目结构

```
ai-ops-mind/
├── app/                    # 后端应用
│   ├── main.py            # FastAPI 入口
│   ├── config.py          # 配置管理
│   ├── api/               # API 路由
│   ├── services/          # 业务服务层
│   ├── prompts/           # 提示词模板
│   ├── models/            # 数据模型
│   └── utils/             # 工具函数
├── frontend/              # 前端界面
│   ├── index.html
│   ├── css/
│   └── js/
├── knowledge/             # 知识库数据
│   ├── cases/             # 故障案例
│   └── docs/              # 技术文档
├── k8s/                   # K8s 部署配置
├── tests/                 # 测试用例
├── docker-compose.yml
├── Dockerfile
├── Makefile
└── requirements.txt
```

## 配置说明

### LLM 配置

支持多种 LLM 提供商：

```env
# DeepSeek (推荐)
OPENAI_API_BASE=https://api.deepseek.com/v1
OPENAI_MODEL_NAME=deepseek-chat

# OpenAI
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4o-mini

# 本地 Ollama
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_MODEL_NAME=qwen:7b-chat
```

### Webhook 签名

为确保安全性，Webhook 支持 HMAC-SHA256 签名验证：

```env
WEBHOOK_SECRET=your-secret-key
```

## 使用示例

### 发送告警

```bash
curl -X POST http://localhost:8000/api/webhook/alert \
  -H "Content-Type: application/json" \
  -d '{
    "alert_id": "test-001",
    "severity": "P0",
    "service": "payment-service",
    "title": "HighErrorRate",
    "description": "Error rate exceeded 300%",
    "fired_at": "2026-05-25T03:14:20Z"
  }'
```

### 分析日志

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"logs": "ERROR [payment] Connection refused to mysql:3306"}'
```

### 搜索知识库

```bash
curl "http://localhost:8000/api/knowledge/search?query=mysql%20connection"
```

## 测试

```bash
# 运行单元测试
pytest tests/ -v

# 检查指标
curl http://localhost:8000/api/metrics
```

## 部署

### Docker Compose

```bash
docker-compose up -d
```

### Kubernetes

```bash
kubectl apply -f k8s/
```

## 监控指标

系统在 `/api/metrics` 暴露以下 Prometheus 指标：

| 指标 | 说明 |
|------|------|
| `ops_llm_requests_total` | LLM 调用次数 |
| `ops_llm_latency_seconds` | LLM 调用耗时 |
| `ops_rag_hit_rate` | RAG 命中率 |
| `ops_webhook_received_total` | Webhook 接收数量 |
| `ops_analysis_confidence` | 分析置信度分布 |
| `ops_feedback_correct_rate` | 专家确认正确率 |

## 许可证

MIT License

---

**AI Ops Mind** - 让运维更智能 🚀
# ai-ops-mind
