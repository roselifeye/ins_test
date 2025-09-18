# Inspection Agent v1

一个基于 PRD 构建的端到端 Demo，包括：

- **前端**：Vue 3 + TypeScript + Vite + Element Plus，单页布局，左侧为配置区，右侧为内容与结果展示。
- **后端**：FastAPI，提供模型配置与评估 API，可连接到任意符合 OpenAI 协议的大模型（可配置 Base URL 与 Token）。

## 本地开发

### 后端

```bash
cd backend
pip install poetry
poetry install
poetry run uvicorn app.main:app --reload
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

默认 dev 服务器会通过 Vite 代理将 `/api` 请求转发到 `http://localhost:8000`。

## FastAPI 接口速览

- `GET /api/evaluation/config`：获取模型、检测器、评审角色等配置。
- `POST /api/evaluation/evaluate`：根据前端提交的模式（Compare/Jury）执行评估，内部可调用外部大模型，若未配置则回退至本地模拟逻辑。

## 测试

后端包含最基本的健康检查用例，可通过以下命令运行：

```bash
cd backend
poetry run pytest
```

## 目录结构

```
backend/   FastAPI 应用
frontend/  Vue3 单页前端
```
