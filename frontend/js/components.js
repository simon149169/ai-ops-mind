class AlertCard extends HTMLElement {
    constructor() {
        super();
    }
    
    connectedCallback() {
        this.render();
    }
    
    static get observedAttributes() {
        return ['severity', 'service', 'title', 'description', 'time'];
    }
    
    attributeChangedCallback() {
        this.render();
    }
    
    render() {
        const severity = this.getAttribute('severity') || 'P3';
        const service = this.getAttribute('service') || 'unknown';
        const title = this.getAttribute('title') || 'Alert';
        const description = this.getAttribute('description') || '';
        const time = this.getAttribute('time') || new Date().toISOString();
        
        this.innerHTML = `
            <div class="alert-card alert-${severity.toLowerCase()}">
                <div class="alert-header">
                    <span class="alert-severity">${severity}</span>
                    <span class="alert-service">${service}</span>
                </div>
                <h3 class="alert-title">${title}</h3>
                <p class="alert-desc">${description}</p>
                <div class="alert-meta">
                    <span>${time}</span>
                    <button class="btn btn-sm" onclick="viewAlertDetail('${title}')">查看详情</button>
                </div>
            </div>
        `;
    }
}

customElements.define('alert-card', AlertCard);

function viewAlertDetail(title) {
    console.log('Viewing alert:', title);
}

class ConfidenceBadge extends HTMLElement {
    constructor() {
        super();
    }
    
    connectedCallback() {
        this.render();
    }
    
    static get observedAttributes() {
        return ['level', 'score'];
    }
    
    attributeChangedCallback() {
        this.render();
    }
    
    render() {
        const level = this.getAttribute('level') || '--';
        const score = this.getAttribute('score') || '0';
        
        let color = '#22c55e';
        if (level === '中') color = '#eab308';
        else if (level === '低') color = '#ef4444';
        
        this.innerHTML = `
            <div class="confidence-badge">
                <span class="confidence-label">置信度</span>
                <span class="confidence-value" style="color: ${color}">${level} (${score}%)</span>
            </div>
        `;
    }
}

customElements.define('confidence-badge', ConfidenceBadge);

class SourceItem extends HTMLElement {
    constructor() {
        super();
    }
    
    connectedCallback() {
        this.render();
    }
    
    static get observedAttributes() {
        return ['id', 'title', 'similarity'];
    }
    
    attributeChangedCallback() {
        this.render();
    }
    
    render() {
        const id = this.getAttribute('id') || '';
        const title = this.getAttribute('title') || '';
        const similarity = parseFloat(this.getAttribute('similarity')) || 0;
        
        this.innerHTML = `
            <div class="source-item">
                <span class="source-title">${title || id}</span>
                <span class="source-similarity">相似度: ${((1 - similarity) * 100).toFixed(1)}%</span>
            </div>
        `;
    }
}

customElements.define('source-item', SourceItem);
