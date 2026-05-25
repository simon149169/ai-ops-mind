const API_BASE = '/api';

let currentAnalysisId = null;

document.addEventListener('DOMContentLoaded', () => {
    initNavigation();
    initAnalysis();
    initFeedback();
    initRCA();
    initKnowledge();
});

function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.content-section');
    
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            navItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            
            const sectionId = `${item.dataset.section}-section`;
            sections.forEach(sec => sec.classList.remove('active'));
            document.getElementById(sectionId).classList.add('active');
        });
    });
}

function initAnalysis() {
    const analyzeBtn = document.getElementById('analyze-btn');
    const clearBtn = document.getElementById('clear-btn');
    const logInput = document.getElementById('log-input');
    const chatContainer = document.getElementById('chat-container');
    const confidenceIndicator = document.getElementById('confidence-indicator');
    const sourcesPanel = document.getElementById('sources-panel');
    const sourcesList = document.getElementById('sources-list');
    const feedbackPanel = document.getElementById('feedback-panel');
    
    analyzeBtn.addEventListener('click', async () => {
        const logs = logInput.value.trim();
        if (!logs) return;
        
        chatContainer.innerHTML += `
            <div class="message user-message">
                <div class="message-content">${escapeHtml(logs)}</div>
            </div>
        `;
        
        const assistantMsg = document.createElement('div');
        assistantMsg.className = 'message assistant-message';
        assistantMsg.innerHTML = '<div class="message-content" id="assistant-content"></div>';
        chatContainer.appendChild(assistantMsg);
        
        chatContainer.scrollTop = chatContainer.scrollHeight;
        
        const eventSource = new EventSource(`${API_BASE}/analyze/stream`);
        
        const formData = new FormData();
        fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ logs, context: '' })
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById('assistant-content').textContent = data.content;
            updateConfidence(data.confidence, data.confidence_score);
            currentAnalysisId = data.analysis_id;
            showSources(data.sources);
            feedbackPanel.style.display = 'block';
            chatContainer.scrollTop = chatContainer.scrollHeight;
        })
        .catch(err => {
            document.getElementById('assistant-content').textContent = '分析失败，请稍后重试';
            console.error(err);
        });
        
        logInput.value = '';
    });
    
    clearBtn.addEventListener('click', () => {
        logInput.value = '';
    });
}

function updateConfidence(confidence, score) {
    const indicator = document.querySelector('.confidence-value');
    indicator.textContent = `${confidence} (${(score * 100).toFixed(0)}%)`;
    
    let color = '#22c55e';
    if (confidence === '中') color = '#eab308';
    else if (confidence === '低') color = '#ef4444';
    indicator.style.color = color;
}

function showSources(sources) {
    const sourcesPanel = document.getElementById('sources-panel');
    const sourcesList = document.getElementById('sources-list');
    
    if (!sources || sources.length === 0) {
        sourcesPanel.style.display = 'none';
        return;
    }
    
    sourcesList.innerHTML = sources.map(source => `
        <div class="source-item">
            <span class="source-title">${source.title || source.id}</span>
            <span class="source-similarity">相似度: ${((1 - source.similarity) * 100).toFixed(1)}%</span>
        </div>
    `).join('');
    
    sourcesPanel.style.display = 'block';
}

function initFeedback() {
    const correctBtn = document.getElementById('feedback-correct');
    const incorrectBtn = document.getElementById('feedback-incorrect');
    const commentInput = document.getElementById('feedback-comment');
    
    correctBtn.addEventListener('click', () => submitFeedback(true));
    incorrectBtn.addEventListener('click', () => submitFeedback(false));
}

function submitFeedback(correct) {
    if (!currentAnalysisId) return;
    
    const comment = document.getElementById('feedback-comment').value;
    
    fetch(`${API_BASE}/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            analysis_id: currentAnalysisId,
            correct,
            comment
        })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        document.getElementById('feedback-comment').value = '';
    })
    .catch(err => console.error(err));
}

function initRCA() {
    const generateBtn = document.getElementById('generate-rca');
    
    generateBtn.addEventListener('click', async () => {
        const incident = document.getElementById('rca-incident').value.trim();
        const logs = document.getElementById('rca-logs').value.trim();
        
        if (!incident) {
            alert('请输入事件名称');
            return;
        }
        
        fetch(`${API_BASE}/rca`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ incident, logs })
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById('rca-report').textContent = data.content;
        })
        .catch(err => console.error(err));
    });
}

function initKnowledge() {
    const searchBtn = document.getElementById('search-btn');
    
    searchBtn.addEventListener('click', () => {
        const query = document.getElementById('knowledge-query').value.trim();
        if (!query) return;
        
        fetch(`${API_BASE}/knowledge/search?query=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
            const list = document.getElementById('knowledge-list');
            list.innerHTML = data.results.map(item => `
                <div class="knowledge-item">
                    <h4>${item.title || item.id}</h4>
                    <p class="knowledge-preview">${item.content.substring(0, 100)}...</p>
                    <span class="knowledge-meta">相似度: ${((1 - item.similarity) * 100).toFixed(1)}%</span>
                </div>
            `).join('');
        })
        .catch(err => console.error(err));
    });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
