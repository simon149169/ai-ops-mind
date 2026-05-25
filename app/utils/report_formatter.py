from datetime import datetime
from typing import List, Dict, Any

def format_rca_report(incident: str, analysis: str, confidence: str, 
                      sources: List[Dict[str, Any]], timeline: List[Dict[str, Any]]) -> str:
    report = f"""# 故障分析报告 — {incident}

**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**置信度**：{confidence}｜**参考案例**：{', '.join([s['id'] for s in sources])}

---

## 概要
{analysis[:200]}...

## 时间线

"""
    for event in timeline:
        report += f"- {event.get('time', '')}: {event.get('event', '')}\n"
    
    report += """

## 根因分析
""" + analysis + """

## 参考来源

"""
    for source in sources:
        report += f"- [{source['id']}] {source['title']} (相似度: {source['similarity']:.2%})\n"
    
    report += """

## 处置措施
1. 待确认根因后制定具体方案
2. 执行必要的修复操作
3. 验证修复效果

## 改进建议
- 建议增加监控告警规则
- 考虑引入自动化恢复机制

---
**专家确认状态**：待确认 ⏳
"""
    return report

def format_analysis_response(content: str, confidence: str, confidence_score: float, 
                             sources: List[Dict[str, Any]]) -> str:
    response = f"**根因分析**\n\n{content}\n\n"
    
    if sources:
        response += "**参考案例**\n"
        for source in sources:
            response += f"- [{source['id']}] {source['title']} (相似度: {source['similarity']:.2%})\n"
    
    response += f"\n**置信度**: {confidence} ({confidence_score:.2%})"
    
    return response
