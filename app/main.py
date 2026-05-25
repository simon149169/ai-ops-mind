from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import chat, analyze, alert, rca, webhook, knowledge, feedback, metrics, health
from app.config import settings
import uvicorn

app = FastAPI(
    title="AI Ops Mind - 智能运维助手平台",
    description="主动感知告警、智能分析根因、生成可信报告、自动沉淀知识",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(analyze.router, prefix="/api/analyze", tags=["Analyze"])
app.include_router(alert.router, prefix="/api/alert", tags=["Alert"])
app.include_router(rca.router, prefix="/api/rca", tags=["RCA"])
app.include_router(webhook.router, prefix="/api/webhook", tags=["Webhook"])
app.include_router(knowledge.router, prefix="/api/knowledge", tags=["Knowledge"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["Feedback"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["Metrics"])
app.include_router(health.router, prefix="/api/health", tags=["Health"])

@app.get("/")
async def root():
    return {"message": "AI Ops Mind v2.0 - 智能运维助手平台"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
