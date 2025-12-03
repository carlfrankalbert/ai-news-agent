# Component Specifications - FYRK AI Score Redesign

This document provides detailed specifications for all redesigned components.

---

## 1. Metric Header with Tooltip

### Structure
```html
<div class="metric-header">
  <span class="metric-label">Buzz</span>
  <button 
    class="info-icon" 
    aria-label="Informasjon om Buzz-metrikken"
    aria-describedby="buzz-tooltip"
    tabindex="0">
    ℹ️
  </button>
  <div 
    id="buzz-tooltip" 
    class="tooltip" 
    role="tooltip"
    aria-hidden="true">
    Hvor mye modellen diskuteres i communityet (0-100). 
    Basert på antall mentions på Hacker News, GitHub og X.
  </div>
</div>
```

### Styles
```css
.metric-header {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  position: relative;
}

.info-icon {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--bg-muted);
  border: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: help;
  font-size: 11px;
  color: var(--text-muted);
  transition: all 150ms ease;
  padding: 0;
  flex-shrink: 0;
}

.info-icon:hover,
.info-icon:focus {
  background: var(--accent-primary-light);
  color: var(--accent-primary);
  outline: 2px solid var(--accent-primary);
  outline-offset: 2px;
}

.tooltip {
  position: absolute;
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%) translateY(-4px);
  background: var(--text-primary);
  color: white;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 13px;
  line-height: 1.5;
  max-width: 300px;
  width: max-content;
  z-index: 1000;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  pointer-events: none;
  opacity: 0;
  transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
  white-space: normal;
}

.info-icon:hover + .tooltip,
.info-icon:focus + .tooltip,
.tooltip[aria-hidden="false"] {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

/* Tooltip arrow */
.tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 6px solid transparent;
  border-top-color: var(--text-primary);
}
```

### JavaScript
```javascript
function initTooltips() {
  const infoIcons = document.querySelectorAll('.info-icon');
  
  infoIcons.forEach(icon => {
    const tooltip = icon.nextElementSibling;
    
    icon.addEventListener('mouseenter', () => {
      tooltip.setAttribute('aria-hidden', 'false');
    });
    
    icon.addEventListener('mouseleave', () => {
      tooltip.setAttribute('aria-hidden', 'true');
    });
    
    icon.addEventListener('focus', () => {
      tooltip.setAttribute('aria-hidden', 'false');
    });
    
    icon.addEventListener('blur', () => {
      tooltip.setAttribute('aria-hidden', 'true');
    });
  });
}
```

---

## 2. Enhanced Ranking Row

### Structure
```html
<div 
  class="ranking-row" 
  data-buzz="100" 
  data-sentiment="100" 
  data-utility="100" 
  data-price="80"
  data-rank="1">
  
  <!-- Main Row -->
  <div class="rank-badge rank-1" aria-label="Rangert som nummer 1">
    <span class="rank-number">1</span>
    <span class="rank-medal">🥇</span>
  </div>
  
  <div class="item-info">
    <div class="item-name-group">
      <span class="item-name">Claude 3.5 Sonnet</span>
      <span class="item-version">v3.5.1</span>
    </div>
    <div class="item-meta">
      <span class="item-provider">
        <img src="anthropic-logo.svg" alt="Anthropic" class="provider-logo">
        <a href="https://anthropic.com" class="provider-link">Anthropic</a>
      </span>
      <span class="item-updated">Oppdatert: 1. des 2025</span>
    </div>
  </div>
  
  <span class="score-cell score-high" aria-label="Buzz score: 100 av 100">
    <span class="score-value">100</span>
    <div class="score-bar">
      <div class="score-fill" style="width: 100%"></div>
    </div>
  </span>
  
  <span class="score-cell score-high" aria-label="Sentiment score: 100 av 100">
    <span class="score-value">100</span>
    <div class="score-bar">
      <div class="score-fill" style="width: 100%"></div>
    </div>
  </span>
  
  <span class="score-cell score-high" aria-label="Nytte score: 100 av 100">
    <span class="score-value">100</span>
    <div class="score-bar">
      <div class="score-fill" style="width: 100%"></div>
    </div>
  </span>
  
  <span class="score-cell score-high" aria-label="Pris score: 80 av 100">
    <span class="score-value">80</span>
    <div class="score-bar">
      <div class="score-fill" style="width: 80%"></div>
    </div>
  </span>
  
  <span class="trend-cell trend-up" aria-label="Opp 3 plasser siden forrige måned">
    <span class="trend-arrow">↑</span>
    <span class="trend-value">+3</span>
  </span>
  
  <div class="row-actions">
    <button class="action-button compare-button" aria-label="Legg til i sammenligning">
      <span class="action-icon">⚖️</span>
    </button>
    <button 
      class="action-button expand-button" 
      aria-expanded="false"
      aria-controls="explanation-1"
      aria-label="Vis detaljer">
      <span class="action-icon">ℹ️</span>
    </button>
  </div>
  
  <!-- Expandable Content -->
  <div 
    id="explanation-1" 
    class="expand-content" 
    aria-hidden="true"
    role="region">
    
    <div class="ranking-explanation">
      <h4>Hvorfor er denne rangert her?</h4>
      <p>Claude 3.5 Sonnet topper listen med sterk resonnering, 
      utmerket kodegenerering og god norsk støtte. Høy buzz 
      på Hacker News og positive utviklerfeedback.</p>
    </div>
    
    <div class="detailed-scores">
      <h4>Detaljerte scores</h4>
      <div class="score-breakdown">
        <div class="breakdown-item">
          <div class="breakdown-header">
            <span class="breakdown-label">Buzz</span>
            <span class="breakdown-value">100</span>
          </div>
          <div class="breakdown-bar">
            <div class="breakdown-fill" style="width: 100%"></div>
          </div>
          <small class="breakdown-detail">450 mentions, 180 kommentarer</small>
        </div>
        <!-- More breakdown items -->
      </div>
    </div>
  </div>
</div>
```

### Styles
```css
.ranking-row {
  display: grid;
  grid-template-columns: 48px 1fr 80px 80px 80px 80px 60px 80px;
  gap: var(--space-md);
  align-items: center;
  padding: var(--space-md);
  border-bottom: 1px solid var(--border-subtle);
  background: var(--bg-card);
  transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.ranking-row:hover {
  background: var(--bg-muted);
  border-left: 3px solid var(--accent-primary);
  padding-left: calc(var(--space-md) - 3px);
  box-shadow: var(--shadow-sm);
}

.rank-badge {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  color: white;
  position: relative;
  animation: badgeAppear 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

.rank-1 {
  background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
  box-shadow: 0 2px 8px rgba(251, 191, 36, 0.3);
}

.rank-2 {
  background: linear-gradient(135deg, #94a3b8 0%, #64748b 100%);
  box-shadow: 0 2px 8px rgba(148, 163, 184, 0.3);
}

.rank-3 {
  background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
  box-shadow: 0 2px 8px rgba(217, 119, 6, 0.3);
}

.item-version {
  font-size: 12px;
  color: var(--text-muted);
  font-family: 'IBM Plex Mono', monospace;
  margin-left: var(--space-xs);
}

.item-updated {
  font-size: 12px;
  color: var(--text-muted);
  margin-left: var(--space-sm);
}

.score-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: center;
}

.score-value {
  font-weight: 600;
  font-size: 16px;
}

.score-bar {
  width: 100%;
  height: 4px;
  background: var(--bg-muted);
  border-radius: 2px;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  background: var(--accent-primary);
  transition: width 300ms ease;
}

.score-high .score-fill {
  background: var(--accent-success);
}

.score-mid .score-fill {
  background: var(--accent-warning);
}

.score-low .score-fill {
  background: var(--accent-danger);
}

.trend-cell {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 6px 10px;
  border-radius: 6px;
  font-weight: 600;
  font-size: 13px;
}

.trend-up {
  background: var(--accent-success-light);
  color: var(--accent-success);
}

.trend-down {
  background: #fee2e2;
  color: #dc2626;
}

.trend-neutral {
  background: var(--bg-muted);
  color: var(--text-secondary);
}

.expand-content {
  grid-column: 1 / -1;
  max-height: 0;
  overflow: hidden;
  transition: max-height 400ms cubic-bezier(0.4, 0, 0.2, 1),
              padding 400ms ease,
              opacity 300ms ease;
  opacity: 0;
  padding: 0;
}

.expand-content[aria-hidden="false"] {
  max-height: 2000px;
  padding: var(--space-lg) 0;
  opacity: 1;
}

@keyframes badgeAppear {
  0% {
    transform: scale(0) rotate(-180deg);
    opacity: 0;
  }
  60% {
    transform: scale(1.1) rotate(10deg);
  }
  100% {
    transform: scale(1) rotate(0deg);
    opacity: 1;
  }
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .ranking-row {
    grid-template-columns: 40px 1fr;
    gap: var(--space-sm);
  }
  
  .score-cell,
  .trend-cell,
  .row-actions {
    grid-column: 1 / -1;
    display: flex;
    justify-content: space-between;
  }
}
```

---

## 3. Enhanced Expand Button

### Structure
```html
<button 
  class="expand-button-pill"
  aria-expanded="false"
  aria-controls="category-content-1"
  aria-label="Vis alle 10 modeller i kategorien Kjerne-LLM-er">
  <span class="button-text">Vis alle 10 modeller</span>
  <span class="expand-icon" aria-hidden="true">↓</span>
</button>
```

### Styles
```css
.expand-button-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: var(--bg-card);
  border: 1.5px solid var(--border);
  border-radius: 24px;
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 150ms ease;
  font-family: inherit;
  margin-top: var(--space-md);
}

.expand-button-pill:hover {
  background: var(--bg-muted);
  border-color: var(--accent-primary);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.expand-button-pill:active {
  transform: translateY(0);
}

.expand-button-pill:focus {
  outline: 2px solid var(--accent-primary);
  outline-offset: 2px;
}

.expand-button-pill[aria-expanded="true"] .expand-icon {
  transform: rotate(180deg);
}

.expand-icon {
  display: inline-block;
  transition: transform 200ms ease;
  font-size: 12px;
}
```

---

## 4. Category Header with Description

### Structure
```html
<div class="category-header">
  <div class="category-title-group">
    <h2 class="category-title">Kjerne-LLM-er</h2>
    <span class="category-count">10 <span>modeller</span></span>
  </div>
  <p class="category-description">
    Store språkmodeller for generell bruk. Godt egnet for 
    resonnering, tekstgenerering og komplekse oppgaver.
    <a href="#methodology" class="learn-more-link">Lær mer</a>
  </p>
  <button 
    class="category-info-button"
    aria-label="Informasjon om kategorien Kjerne-LLM-er"
    aria-expanded="false"
    aria-controls="category-info-1">
    <span class="info-icon">ℹ️</span>
    <span>Hva er dette?</span>
  </button>
</div>
```

### Styles
```css
.category-header {
  margin-bottom: var(--space-lg);
  padding-bottom: var(--space-md);
  border-bottom: 1px solid var(--border);
}

.category-title-group {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: var(--space-md);
  margin-bottom: var(--space-sm);
}

.category-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
}

.category-count {
  font-size: 14px;
  color: var(--text-secondary);
  font-weight: 500;
}

.category-description {
  font-size: 15px;
  line-height: 1.6;
  color: var(--text-secondary);
  margin: var(--space-sm) 0;
  max-width: 65ch;
}

.learn-more-link {
  color: var(--accent-primary);
  text-decoration: none;
  font-weight: 500;
  margin-left: var(--space-xs);
}

.learn-more-link:hover {
  text-decoration: underline;
}

.category-info-button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: transparent;
  border: 1px solid var(--border);
  border-radius: 6px;
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 150ms ease;
  margin-top: var(--space-xs);
}

.category-info-button:hover {
  background: var(--bg-muted);
  border-color: var(--accent-primary);
  color: var(--accent-primary);
}
```

---

## 5. Compare Models Mode

### Structure
```html
<div class="compare-mode-container">
  <label class="compare-mode-toggle">
    <input 
      type="checkbox" 
      id="compare-mode"
      aria-label="Aktiver sammenligningsmodus">
    <span class="toggle-label">
      <span class="toggle-icon">⚖️</span>
      Sammenlign modeller
    </span>
  </label>
  
  <div class="compare-selection" aria-live="polite" aria-atomic="true">
    <span class="selection-count">0 valgt</span>
    <button class="clear-selection" aria-label="Fjern alle valg">
      Nullstill
    </button>
  </div>
</div>

<!-- Comparison Panel (shown when 2+ models selected) -->
<div 
  class="comparison-panel" 
  role="region"
  aria-label="Modellsammenligning"
  aria-hidden="true">
  <div class="comparison-header">
    <h3>Sammenligning</h3>
    <button class="close-comparison" aria-label="Lukk sammenligning">
      ✕
    </button>
  </div>
  <div class="comparison-table">
    <!-- Comparison content -->
  </div>
</div>
```

### Styles
```css
.compare-mode-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-md);
  background: var(--bg-muted);
  border-radius: var(--radius-md);
  margin-bottom: var(--space-lg);
}

.compare-mode-toggle {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  cursor: pointer;
}

.compare-mode-toggle input[type="checkbox"] {
  width: 20px;
  height: 20px;
  cursor: pointer;
  accent-color: var(--accent-primary);
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 500;
  font-size: 14px;
  color: var(--text-primary);
}

.comparison-panel {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  max-height: 70vh;
  background: var(--bg-card);
  border-top: 1px solid var(--border);
  box-shadow: 0 -4px 24px rgba(0, 0, 0, 0.1);
  transform: translateY(100%);
  transition: transform 300ms cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1000;
  overflow-y: auto;
}

.comparison-panel[aria-hidden="false"] {
  transform: translateY(0);
}

.comparison-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-lg);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  background: var(--bg-card);
  z-index: 10;
}

/* Checkbox in ranking row */
.ranking-row .compare-checkbox {
  position: absolute;
  top: var(--space-sm);
  right: var(--space-sm);
  width: 20px;
  height: 20px;
  opacity: 0;
  transition: opacity 200ms ease;
}

.ranking-row:hover .compare-checkbox,
.compare-mode:checked ~ .ranking-row .compare-checkbox {
  opacity: 1;
}
```

---

## 6. Mobile Capabilities Card

### Structure
```html
<div class="capability-card" data-model="claude">
  <div class="card-header">
    <div class="model-info">
      <img src="anthropic-logo.svg" alt="Anthropic" class="model-logo">
      <div>
        <h3 class="model-name">Claude</h3>
        <p class="model-provider">Anthropic</p>
      </div>
    </div>
    <button class="card-expand" aria-label="Vis detaljer">
      <span>▼</span>
    </button>
  </div>
  
  <div class="card-content">
    <div class="capability-category">
      <h4 class="category-name">Kognitiv</h4>
      <ul class="capability-list">
        <li class="capability-item">
          <span class="capability-name">Koding</span>
          <span class="capability-score score-yes">✓</span>
        </li>
        <li class="capability-item">
          <span class="capability-name">Resonnering</span>
          <span class="capability-score score-yes">✓</span>
        </li>
        <li class="capability-item">
          <span class="capability-name">Norsk</span>
          <span class="capability-score score-yes">✓</span>
        </li>
      </ul>
    </div>
    
    <div class="best-for-section">
      <h4>Best for</h4>
      <p>Generell reasoning, koding, norsk tekst</p>
    </div>
  </div>
</div>
```

### Styles
```css
.capability-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  margin-bottom: var(--space-md);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  transition: all 200ms ease;
}

.capability-card:active {
  transform: scale(0.98);
  box-shadow: var(--shadow-md);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-md);
  padding-bottom: var(--space-md);
  border-bottom: 1px solid var(--border-subtle);
}

.model-info {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.model-logo {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
}

.model-name {
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 2px 0;
}

.model-provider {
  font-size: 13px;
  color: var(--text-secondary);
  margin: 0;
}

.capability-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-sm) 0;
  border-bottom: 1px solid var(--border-subtle);
  min-height: 44px; /* Touch target */
}

.capability-item:last-child {
  border-bottom: none;
}

.capability-name {
  font-size: 15px;
  color: var(--text-primary);
}

.capability-score {
  font-size: 18px;
  font-weight: 600;
}

.score-yes {
  color: var(--accent-success);
}

.score-best {
  color: var(--gold);
}

.score-no {
  color: var(--text-muted);
}
```

---

## 7. Hero Section with Versioning

### Structure
```html
<section class="hero-section">
  <div class="hero-content">
    <h1 class="hero-title">FYRK AI Score</h1>
    <div class="version-info">
      <span class="version-badge">v2.1.0</span>
      <span class="version-separator">•</span>
      <span class="update-date">Oppdatert 2. des 2025</span>
    </div>
    <p class="hero-description">
      Månedlig rangering av AI-verktøy basert på buzz, 
      sentiment og nytteverdi
    </p>
  </div>
</section>
```

### Styles
```css
.hero-section {
  padding: var(--space-2xl) 0;
  text-align: center;
  background: linear-gradient(180deg, #fafafa 0%, #f8f8f8 100%);
  border-bottom: 1px solid var(--border);
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  margin: 0 0 var(--space-md) 0;
  letter-spacing: -0.02em;
}

.version-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-lg);
  font-size: 14px;
  color: var(--text-secondary);
}

.version-badge {
  font-family: 'IBM Plex Mono', monospace;
  background: var(--bg-muted);
  padding: 4px 10px;
  border-radius: 4px;
  font-weight: 600;
  color: var(--text-primary);
}

.hero-description {
  font-size: 18px;
  line-height: 1.6;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
}
```

---

## Responsive Breakpoints

```css
/* Mobile First */
:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
}

/* Example usage */
@media (min-width: 768px) {
  .ranking-row {
    grid-template-columns: 48px 1fr 80px 80px 80px 80px 60px 80px;
  }
}

@media (max-width: 767px) {
  .ranking-row {
    grid-template-columns: 40px 1fr;
  }
}
```

---

## Accessibility Checklist

- [ ] All interactive elements have focus states
- [ ] Tooltips are keyboard accessible
- [ ] ARIA labels and roles are properly set
- [ ] Color contrast meets WCAG AA standards
- [ ] Screen reader announcements for dynamic content
- [ ] Skip links for keyboard navigation
- [ ] Touch targets are minimum 44x44px
- [ ] Text is resizable up to 200% without breaking layout

