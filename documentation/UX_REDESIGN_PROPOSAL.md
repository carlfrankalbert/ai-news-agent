# FYRK AI Score - UX Redesign Proposal

**Designer:** Senior Product Designer  
**Date:** December 2025  
**Version:** 1.0

---

## Executive Summary

This proposal outlines a comprehensive UX redesign for FYRK AI Score, focusing on improved clarity, enhanced interactivity, and mobile-first usability while maintaining the site's Scandinavian minimalism and data-driven aesthetic.

### Key Improvements
- **Clarity**: Enhanced explanations, tooltips, and context for new users
- **Interactivity**: Subtle, purposeful interactions without visual clutter
- **Mobile**: Redesigned tables and multi-column content for small screens
- **Trust**: Clearer methodology, versioning, and transparency
- **Accessibility**: Improved contrast, keyboard navigation, and screen reader support

---

## Design Philosophy

### Core Principles
1. **Scandinavian Minimalism**: Clean, airy layouts with generous whitespace
2. **Data-First**: Information architecture prioritizes clarity and scannability
3. **Progressive Disclosure**: Show essentials first, reveal details on demand
4. **Calm UI**: Low cognitive load, subtle animations, professional tone
5. **Mobile-First**: Touch-friendly, responsive, swipeable interactions

### Visual Identity
- **Typography**: DM Sans (body), IBM Plex Mono (data/metrics)
- **Color Palette**: Neutrals with subtle category accents
- **Spacing**: 8px base unit (4px, 8px, 16px, 24px, 32px, 48px, 64px)
- **Shadows**: Subtle, layered depth (sm, md, lg)
- **Borders**: Ultra-light (0.5px, rgba(0,0,0,0.03-0.05))

---

## 1. Scores Page Redesign

### Current State Analysis
**Strengths:**
- Clear category organization
- Sortable columns
- Expandable rows

**Pain Points:**
- Unclear metric definitions (Buzz, Sentiment, Nytte, Pris)
- No version numbers or timestamps
- Limited mobile usability
- No comparison mode
- Trend indicators lack context

### Redesigned Layout

```
┌─────────────────────────────────────────────────────────────┐
│  Header: Logo | Lang | Contact                             │
├─────────────────────────────────────────────────────────────┤
│  [Tabs: Scores | Capabilities]                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Hero Section                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  FYRK AI Score – Desember 2025                       │   │
│  │  v2.1.0 • Oppdatert 2. des 2025                     │   │
│  │                                                      │   │
│  │  Månedlig rangering av AI-verktøy basert på         │   │
│  │  buzz, sentiment og nytteverdi                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Highlights Bar (Compact)                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Ny: Gemini 2.0 Flash • DeepSeek-R1 • Aider        │   │
│  │  Movers: Tabnine ↓ • Grok-2 ↓                      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Metrics Explanation (Expandable)                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  📊 Slik leser du dataene  [ℹ️]                     │   │
│  │  ┌─────────┬──────────┬─────────┬─────────┐        │   │
│  │  │ Buzz ℹ️ │ Sentiment│ Nytte ℹ️ │ Pris ℹ️ │        │   │
│  │  │ 0-100   │ Pos/Neg  │ 0-100   │ 0-100   │        │   │
│  │  └─────────┴──────────┴─────────┴─────────┘        │   │
│  │  [Vis detaljer]                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Filter Bar (Sticky on Mobile)                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Filtrer: [Alle] [Kjerne-LLM] [Kode] [Builder] ...  │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Category: Kjerne-LLM-er                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Kjerne-LLM-er                   10 modeller         │   │
│  │  Store språkmodeller for generell bruk              │   │
│  │  [ℹ️ Hva er dette?]                                │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  ┌──┬──────────────┬─────┬──────────┬──────┬─────┐ │   │
│  │  │# │Navn          │Buzz │Sentiment │Nytte │Pris │ │   │
│  │  │  │              │ ℹ️  │    ℹ️    │  ℹ️  │ ℹ️  │ │   │
│  │  ├──┼──────────────┼─────┼──────────┼──────┼─────┤ │   │
│  │  │🥇│Claude 3.5    │ 100 │   100    │ 100  │ 80  │ │   │
│  │  │  │Sonnet v3.5.1 │     │          │      │     │ │   │
│  │  │  │Anthropic     │     │          │      │     │ │   │
│  │  │  │[Compare] [ℹ️] │     │          │      │     │ │   │
│  │  ├──┼──────────────┼─────┼──────────┼──────┼─────┤ │   │
│  │  │🥈│GPT-4o        │  80 │    80    │ 100  │ 60  │ │   │
│  │  │  │v4o-2024-11-06│     │          │      │     │ │   │
│  │  │  │OpenAI        │     │          │      │     │ │   │
│  │  │  │[Compare] [ℹ️] │     │          │      │     │ │   │
│  │  └──┴──────────────┴─────┴──────────┴──────┴─────┘ │   │
│  │  [Vis alle 10 modeller]                            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [Compare Selected Models] (when 2+ selected)              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Key Improvements

#### 1.1 Enhanced Header with Versioning
```html
<div class="hero-section">
  <h1>FYRK AI Score – Desember 2025</h1>
  <div class="version-info">
    <span class="version-badge">v2.1.0</span>
    <span class="update-date">Oppdatert 2. des 2025</span>
  </div>
  <p class="hero-description">Månedlig rangering av AI-verktøy...</p>
</div>
```

**Rationale:** Version numbers and timestamps build trust and help users understand data freshness.

#### 1.2 Tooltips for Metrics
Each column header includes an info icon (ℹ️) with a tooltip:

- **Buzz ℹ️**: "Hvor mye modellen diskuteres i communityet (0-100). Basert på antall mentions på Hacker News, GitHub og X."
- **Sentiment ℹ️**: "Hvor positivt/negativt modellen omtales. Høyere = mer positivt."
- **Nytte ℹ️**: "Opplevd praktisk nytteverdi basert på utviklerfeedback (0-100)."
- **Pris ℹ️**: "Kost/nytte-forhold. Lavere = bedre verdi. Basert på prising og opplevd verdi."

**Implementation:**
```css
.metric-header {
  display: flex;
  align-items: center;
  gap: 4px;
}

.info-icon {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--bg-muted);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: help;
  font-size: 10px;
  color: var(--text-muted);
  transition: all 150ms ease;
}

.info-icon:hover {
  background: var(--accent-primary-light);
  color: var(--accent-primary);
}

.tooltip {
  position: absolute;
  background: var(--text-primary);
  color: white;
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 13px;
  max-width: 280px;
  z-index: 1000;
  box-shadow: var(--shadow-lg);
  pointer-events: none;
  opacity: 0;
  transform: translateY(-4px);
  transition: all 150ms ease;
}

.info-icon:hover + .tooltip,
.info-icon:focus + .tooltip {
  opacity: 1;
  transform: translateY(0);
}
```

#### 1.3 Model Version Numbers
Each model row displays version information:

```html
<div class="item-info">
  <span class="item-name">Claude 3.5 Sonnet</span>
  <span class="item-version">v3.5.1</span>
  <span class="item-provider">Anthropic</span>
  <span class="item-updated">Oppdatert: 1. des 2025</span>
</div>
```

#### 1.4 Expandable Comparison Rows
Enhanced expandable rows with "Why it's ranked here" section:

```html
<div class="ranking-row expanded">
  <!-- Main row content -->
  <div class="expand-content">
    <div class="ranking-explanation">
      <h4>Hvorfor er denne rangert her?</h4>
      <p>Claude 3.5 Sonnet topper listen med sterk resonnering, 
      utmerket kodegenerering og god norsk støtte. Høy buzz 
      på Hacker News og positive utviklerfeedback.</p>
    </div>
    <div class="detailed-scores">
      <div class="score-breakdown">
        <span>Buzz: 100</span>
        <div class="score-bar"><div style="width: 100%"></div></div>
        <small>450 mentions, 180 kommentarer</small>
      </div>
      <!-- More breakdowns -->
    </div>
  </div>
</div>
```

#### 1.5 Compare Models Mode
Add multi-select checkboxes and comparison view:

```html
<div class="compare-mode-toggle">
  <label>
    <input type="checkbox" id="compare-mode">
    Sammenlign modeller
  </label>
</div>

<!-- When 2+ models selected -->
<div class="comparison-panel">
  <h3>Sammenligning</h3>
  <div class="comparison-table">
    <!-- Side-by-side comparison -->
  </div>
</div>
```

#### 1.6 Improved Trend Indicators
Enhanced trend cells with context:

```html
<span class="trend-cell trend-up" title="Opp 3 plasser siden forrige måned">
  <span class="trend-arrow">↑</span>
  <span class="trend-value">+3</span>
</span>
```

---

## 2. Capabilities Page Redesign

### Current State Analysis
**Strengths:**
- Clear matrix layout
- Mobile card view exists

**Pain Points:**
- Desktop table is hard to scan
- No explanations of capabilities
- Missing model icons/logos
- No "Best for X" guidance

### Redesigned Layout

#### Desktop View
```
┌─────────────────────────────────────────────────────────────┐
│  Capabilities                                               │
│  Hva kan hver modell?                                       │
├─────────────────────────────────────────────────────────────┤
│  [Legend: ⭐ Best | ✓ Yes | ✗ No]                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┬───────┬───────┬───────┬───────┬───────┐     │
│  │          │Claude │GPT-4o │Gemini │Llama  │DeepSeek│     │
│  │          │[logo] │[logo] │[logo] │[logo] │[logo] │     │
│  ├──────────┼───────┼───────┼───────┼───────┼───────┤     │
│  │Kognitiv  │       │       │       │       │       │     │
│  ├──────────┼───────┼───────┼───────┼───────┼───────┤     │
│  │Koding ℹ️ │   ✓   │   ✓   │  ⭐   │   ✓   │   ✓   │     │
│  │Resonnering│  ✓   │   ✓   │  ⭐   │   ✓   │   ✓   │     │
│  │Norsk ℹ️  │   ✓   │   ✓   │   ✓   │  ⭐   │   ✓   │     │
│  ├──────────┼───────┼───────┼───────┼───────┼───────┤     │
│  │Visuell   │       │       │       │       │       │     │
│  ├──────────┼───────┼───────┼───────┼───────┼───────┤     │
│  │Bildegen. │   ✗   │   ✗   │   ✓   │   ✓   │  ⭐   │     │
│  │Bildeanal.│   ✗   │   ✗   │   ✗   │   ✗   │   ✗   │     │
│  └──────────┴───────┴───────┴───────┴───────┴───────┘     │
│                                                             │
│  Best for:                                                  │
│  • Claude: Generell reasoning, koding, norsk               │
│  • GPT-4o: Multimodal tasks, API-integration               │
│  • Gemini: Koding, resonnering, bildegenerering            │
└─────────────────────────────────────────────────────────────┘
```

#### Mobile View (Card-Based)
```
┌─────────────────────────────────────┐
│  [Claude] [GPT-4o] [Gemini] [→]    │ ← Swipeable tabs
├─────────────────────────────────────┤
│                                     │
│  ┌───────────────────────────────┐ │
│  │ Claude                         │ │
│  │ Anthropic                     │ │
│  │                                │ │
│  │ Kognitiv                       │ │
│  │ • Koding ℹ️          ✓        │ │
│  │ • Resonnering        ✓        │ │
│  │ • Norsk ℹ️           ✓        │ │
│  │                                │ │
│  │ Visuell                        │ │
│  │ • Bildegenerering    ✗        │ │
│  │                                │ │
│  │ Best for:                      │ │
│  │ Generell reasoning, koding    │ │
│  └───────────────────────────────┘ │
│                                     │
└─────────────────────────────────────┘
```

### Key Improvements

#### 2.1 Capability Tooltips
Hover/press on capability names shows explanation:

```html
<th class="capability-header">
  Koding
  <span class="info-icon" data-tooltip="Kodegenerering og debugging. 
  Støtte for flere programmeringsspråk og IDE-integrasjon.">ℹ️</span>
</th>
```

#### 2.2 Model Icons/Logos
Add provider logos in table headers:

```html
<th class="model-header">
  <img src="anthropic-logo.svg" alt="Anthropic" class="model-logo">
  <span>Claude</span>
</th>
```

#### 2.3 "Best for X" Section
Add contextual recommendations:

```html
<div class="best-for-section">
  <h3>Best for</h3>
  <div class="best-for-grid">
    <div class="best-for-item">
      <strong>Claude</strong>
      <p>Generell reasoning, koding, norsk tekst</p>
    </div>
    <!-- More items -->
  </div>
</div>
```

#### 2.4 Enhanced Mobile Cards
Improved card design with better spacing and touch targets:

```css
.capability-card {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  margin-bottom: var(--space-md);
  box-shadow: var(--shadow-sm);
  transition: all 150ms ease;
}

.capability-card:active {
  transform: scale(0.98);
  box-shadow: var(--shadow-md);
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
```

---

## 3. Model Overview Panels Enhancement

### Category Descriptions
Add short descriptions under each category header:

```html
<div class="category-header">
  <div class="category-title-group">
    <h2 class="category-title">Kjerne-LLM-er</h2>
    <span class="category-count">10 modeller</span>
  </div>
  <p class="category-description">
    Store språkmodeller for generell bruk. Godt egnet for 
    resonnering, tekstgenerering og komplekse oppgaver.
    <a href="#methodology" class="learn-more">Lær mer</a>
  </p>
</div>
```

### "Why it's ranked here" Expandable
Enhanced expandable sections with structured explanations:

```html
<div class="ranking-explanation">
  <button class="explanation-toggle" aria-expanded="false">
    <span>Hvorfor er denne rangert her?</span>
    <span class="toggle-icon">▼</span>
  </button>
  <div class="explanation-content hidden">
    <div class="explanation-section">
      <h4>Styrker</h4>
      <ul>
        <li>Utmerket resonnering og logisk tenkning</li>
        <li>Stark kodegenerering med god kontekstforståelse</li>
        <li>God norsk språkstøtte</li>
      </ul>
    </div>
    <div class="explanation-section">
      <h4>Data</h4>
      <dl>
        <dt>Buzz</dt>
        <dd>450 mentions på Hacker News denne måneden</dd>
        <dt>Sentiment</dt>
        <dd>Overveiende positiv (85% positive mentions)</dd>
      </dl>
    </div>
  </div>
</div>
```

### Improved Color-Coding for Trends
Enhanced trend indicators with better contrast:

```css
.trend-cell {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: 4px;
  font-weight: 600;
  font-size: 13px;
}

.trend-up {
  background: var(--accent-success-light);
  color: var(--accent-success);
}

.trend-down {
  background: #fee2e2; /* Light red */
  color: #dc2626;
}

.trend-neutral {
  background: var(--bg-muted);
  color: var(--text-secondary);
}
```

---

## 4. Methodology / About Page

### New Dedicated Page Structure

```
┌─────────────────────────────────────────────────────────────┐
│  Om AI Score                                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Hva er FYRK AI Score?                                      │
│  Et eksperiment fra FYRK Lab hvor vi utforsker hvordan     │
│  man kan sammenligne AI-modeller på en enkel måte.          │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Innholdsfortegnelse                                │   │
│  │  • Datakilder                                       │   │
│  │  • Evalueringsprosess                               │   │
│  │  • Scoring-matematikk                               │   │
│  │  • Oppdateringsplan                                 │   │
│  │  • Begrensninger                                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Datakilder                                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  1. Offentlig tilgjengelig informasjon              │   │
│  │     • Modellspesifikasjoner                         │   │
│  │     • Prisinformasjon                               │   │
│  │     • Offisielle dokumentasjoner                    │   │
│  │                                                      │   │
│  │  2. Egne praktiske tester                           │   │
│  │     • Kodegenerering                                │   │
│  │     • Norsk språkstøtte                             │   │
│  │     • Multimodal evne                               │   │
│  │                                                      │   │
│  │  3. Inntrykk fra utviklere                          │   │
│  │     • Hacker News diskusjoner                       │   │
│  │     • GitHub issues og diskusjoner                   │   │
│  │     • X/Twitter sentiment                           │   │
│  │                                                      │   │
│  │  4. AI-genererte vurderinger                       │   │
│  │     • Claude API-analyse                            │   │
│  │     • Strukturert rangering                         │   │
│  │     • Validert av menneskelige eksperter            │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  Evalueringsprosess                                         │
│  [Step-by-step process visualization]                       │
│                                                             │
│  Scoring-matematikk                                          │
│  [Formula breakdowns]                                        │
│                                                             │
│  Oppdateringsplan                                            │
│  • Månedlig oppdatering (første mandag i måneden)          │
│  • Versjonshistorikk                                        │
│  • Changelog                                                │
│                                                             │
│  Begrensninger                                               │
│  • Ikke en vitenskapelig benchmark                          │
│  • Subjektive vurderinger                                  │
│  • Basert på tilgjengelig data                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Implementation

```html
<article class="methodology-page">
  <header class="page-header">
    <h1>Om AI Score</h1>
    <p class="page-subtitle">Metodikk, datakilder og begrensninger</p>
  </header>

  <nav class="methodology-nav">
    <a href="#datakilder">Datakilder</a>
    <a href="#evaluering">Evaluering</a>
    <a href="#scoring">Scoring</a>
    <a href="#oppdatering">Oppdatering</a>
    <a href="#begrensninger">Begrensninger</a>
  </nav>

  <section id="datakilder">
    <h2>Datakilder</h2>
    <!-- Content -->
  </section>

  <!-- More sections -->
</article>
```

---

## 5. Footer & CTA Redesign

### Enhanced Footer

```
┌─────────────────────────────────────────────────────────────┐
│  Footer                                                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────┬─────────────────────────────────┐ │
│  │  FYRK Lab           │  Kontakt                        │ │
│  │                     │  ┌─────────────────────────────┐ │ │
│  │  Eksperimenter innen │  │ [Kontakt oss]              │ │ │
│  │  AI og              │  │ hei@fyrk.no                │ │ │
│  │  produktledelse     │  └─────────────────────────────┘ │ │
│  │                     │                                  │ │
│  │  © 2025 FYRK        │  Lenker                         │ │
│  │                     │  • fyrk.no                     │ │
│  │                     │  • Om AI Score                 │ │
│  │                     │  • Metodikk                    │ │
│  └─────────────────────┴─────────────────────────────────┘ │
│                                                             │
│  Transparensnotater                                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ⚠️ Ikke en benchmark                                │   │
│  │  📊 Eksperimentell data                              │   │
│  │  🔄 Oppdatert månedlig                              │   │
│  │  📅 Versjon 2.1.0 • 2. des 2025                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Enhanced CTA Section

```html
<section class="cta-section-enhanced">
  <div class="cta-content">
    <h3>Vil du bruke AI mer effektivt i teamet ditt?</h3>
    <p>FYRK hjelper bedrifter å velge riktige verktøy og bygge AI-drevne arbeidsflyter.</p>
    <div class="cta-actions">
      <a href="mailto:hei@fyrk.no" class="cta-button-primary">
        Kontakt oss
        <span class="cta-arrow">→</span>
      </a>
      <a href="#om" class="cta-button-secondary">
        Les mer om FYRK
      </a>
    </div>
  </div>
</section>
```

---

## 6. Functional Improvements

### 6.1 Sticky Category Selector (Mobile)
```css
@media (max-width: 768px) {
  .filter-bar {
    position: sticky;
    top: 0;
    background: var(--bg-card);
    z-index: 100;
    padding: var(--space-md);
    box-shadow: var(--shadow-sm);
    border-bottom: 1px solid var(--border);
  }
}
```

### 6.2 Swipeable Table Sections
```javascript
// Enable horizontal swipe on mobile tables
const tableContainer = document.querySelector('.rankings-table');
let touchStartX = 0;
let touchEndX = 0;

tableContainer.addEventListener('touchstart', (e) => {
  touchStartX = e.changedTouches[0].screenX;
});

tableContainer.addEventListener('touchend', (e) => {
  touchEndX = e.changedTouches[0].screenX;
  handleSwipe();
});

function handleSwipe() {
  if (touchEndX < touchStartX - 50) {
    // Swipe left - scroll right
    tableContainer.scrollBy({ left: 200, behavior: 'smooth' });
  }
  if (touchEndX > touchStartX + 50) {
    // Swipe right - scroll left
    tableContainer.scrollBy({ left: -200, behavior: 'smooth' });
  }
}
```

### 6.3 Smooth Transitions
```css
.ranking-row {
  transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
}

.ranking-row.expanding {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.expand-content {
  max-height: 0;
  overflow: hidden;
  transition: max-height 300ms ease, padding 300ms ease;
}

.expand-content.expanded {
  max-height: 1000px;
  padding: var(--space-lg) 0;
}
```

### 6.4 Column Sorting Enhancement
```javascript
function sortTable(table, column, direction) {
  const rows = Array.from(table.querySelectorAll('.ranking-row'));
  const sorted = rows.sort((a, b) => {
    const aVal = parseFloat(a.dataset[column]) || 0;
    const bVal = parseFloat(b.dataset[column]) || 0;
    return direction === 'asc' ? aVal - bVal : bVal - aVal;
  });
  
  // Animate reordering
  sorted.forEach((row, index) => {
    row.style.opacity = '0';
    row.style.transform = 'translateY(-10px)';
    setTimeout(() => {
      table.appendChild(row);
      row.style.transition = 'all 200ms ease';
      row.style.opacity = '1';
      row.style.transform = 'translateY(0)';
    }, index * 20);
  });
}
```

### 6.5 Persist Filters in Local Storage
```javascript
// Save filter state
function saveFilterState(category) {
  localStorage.setItem('fyrk-active-filter', category);
}

// Restore on load
function restoreFilterState() {
  const saved = localStorage.getItem('fyrk-active-filter');
  if (saved) {
    switchTab(saved);
  }
}
```

### 6.6 Light/Dark Mode (Optional)
```css
:root[data-theme="dark"] {
  --bg-base: #0a0a0a;
  --bg-card: #141414;
  --bg-muted: #1a1a1a;
  --text-primary: #fafafa;
  --text-secondary: #a1a1aa;
  --border: rgba(255, 255, 255, 0.1);
}

.theme-toggle {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: var(--bg-card);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-lg);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
```

---

## 7. Visual Improvements

### 7.1 Category Color Accents
```css
.category-section[data-category="core-llm"] {
  border-left: 3px solid #3b82f6; /* Blue */
}

.category-section[data-category="code-assistants"] {
  border-left: 3px solid #10b981; /* Green */
}

.category-section[data-category="builder-platform"] {
  border-left: 3px solid #8b5cf6; /* Purple */
}

.category-section[data-category="image-video"] {
  border-left: 3px solid #f59e0b; /* Orange */
}
```

### 7.2 Subtle Row Dividers
```css
.ranking-row:not(:last-child) {
  border-bottom: 1px solid var(--border-subtle);
}

.ranking-row:hover {
  background: var(--bg-muted);
  border-left: 2px solid var(--accent-primary);
  padding-left: calc(var(--space-md) - 2px);
}
```

### 7.3 Improved Contrast
```css
:root {
  --text-primary: #0a0a0a; /* Increased from #18181b */
  --text-secondary: #52525b; /* Increased from #71717a */
  --border: rgba(0, 0, 0, 0.08); /* Increased from 0.05 */
}
```

### 7.4 Enhanced Expand Button
```html
<button class="expand-button-pill">
  <span>Vis alle 10 modeller</span>
  <span class="expand-icon">↓</span>
</button>
```

```css
.expand-button-pill {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: var(--bg-card);
  border: 1.5px solid var(--border);
  border-radius: 24px;
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 150ms ease;
}

.expand-button-pill:hover {
  background: var(--bg-muted);
  border-color: var(--accent-primary);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}
```

### 7.5 Micro-animations for Badges
```css
.rank-badge {
  animation: badgeAppear 400ms cubic-bezier(0.34, 1.56, 0.64, 1);
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
```

---

## 8. Accessibility Improvements

### 8.1 Keyboard Navigation
```css
.tab:focus,
.filter-pill:focus,
.expand-button:focus {
  outline: 2px solid var(--accent-primary);
  outline-offset: 2px;
}

/* Skip to content link */
.skip-link {
  position: absolute;
  top: -40px;
  left: 0;
  background: var(--accent-primary);
  color: white;
  padding: 8px;
  z-index: 100;
}

.skip-link:focus {
  top: 0;
}
```

### 8.2 Screen Reader Support
```html
<button 
  class="expand-button"
  aria-expanded="false"
  aria-controls="expand-content-1"
  aria-label="Vis alle 10 modeller i kategorien Kjerne-LLM-er">
  Vis alle
</button>

<div 
  id="expand-content-1"
  role="region"
  aria-labelledby="category-title-1"
  hidden>
  <!-- Content -->
</div>
```

### 8.3 ARIA Labels for Interactive Elements
```html
<button 
  class="info-icon"
  aria-label="Informasjon om Buzz-metrikken"
  aria-describedby="buzz-tooltip">
  ℹ️
</button>

<div 
  id="buzz-tooltip"
  role="tooltip"
  class="tooltip">
  Hvor mye modellen diskuteres i communityet...
</div>
```

### 8.4 Color Contrast Compliance
- All text meets WCAG AA standards (4.5:1 for normal text, 3:1 for large text)
- Interactive elements have 3:1 contrast ratio
- Focus indicators are clearly visible

---

## 9. Mobile-First Responsive Design

### Breakpoints
```css
/* Mobile First */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
```

### Mobile Table Strategy
1. **Horizontal Scroll**: Tables scroll horizontally on mobile
2. **Card View**: Alternative card-based view for capabilities
3. **Sticky Headers**: Category filters stick to top
4. **Touch Targets**: Minimum 44x44px for all interactive elements
5. **Swipe Gestures**: Swipe to navigate between models/categories

---

## 10. Implementation Roadmap

### Phase 1: Core Improvements (Week 1-2)
- [ ] Add tooltips to all metric headers
- [ ] Implement version numbers and timestamps
- [ ] Enhance expandable rows with explanations
- [ ] Improve mobile table scrolling
- [ ] Add category descriptions

### Phase 2: Enhanced Interactivity (Week 3-4)
- [ ] Implement compare models mode
- [ ] Add capability tooltips
- [ ] Enhance trend indicators
- [ ] Improve mobile card views
- [ ] Add "Best for X" sections

### Phase 3: Methodology & Trust (Week 5-6)
- [ ] Create dedicated methodology page
- [ ] Enhance footer with transparency notes
- [ ] Improve CTA section
- [ ] Add version history/changelog

### Phase 4: Polish & Accessibility (Week 7-8)
- [ ] Implement all accessibility improvements
- [ ] Add micro-animations
- [ ] Optimize performance
- [ ] Cross-browser testing
- [ ] User testing and refinement

---

## 11. Alternative Design Directions

### Option A: More Visual, Less Text
- Larger model logos
- More prominent visualizations
- Chart-based comparisons
- **Trade-off**: Less information density

### Option B: More Compact, Data-Dense
- Smaller fonts, tighter spacing
- More models visible at once
- Inline tooltips
- **Trade-off**: Higher cognitive load

### Option C: Story-Driven
- Narrative explanations for rankings
- Case studies and examples
- More editorial content
- **Trade-off**: Less scannable

**Recommendation**: Current proposal (balanced approach)

---

## 12. Success Metrics

### User Experience
- Time to understand scoring system (target: <30 seconds)
- Mobile usability score (target: >90)
- Accessibility score (target: WCAG AA compliance)

### Engagement
- Average time on page (target: +20%)
- Capabilities page views (target: +30%)
- Methodology page views (target: +50%)

### Trust
- User feedback on clarity (target: >4/5)
- Trust in data (target: >4/5)

---

## Conclusion

This redesign proposal maintains FYRK's Scandinavian minimalism while significantly improving usability, clarity, and trust. The changes are incremental and can be implemented in phases, allowing for user testing and iteration.

**Key Differentiators:**
- Professional, trustworthy presentation
- Mobile-first, touch-optimized
- Accessible and inclusive
- Data-driven with clear methodology
- Calm, low-cognitive-load UI

The redesigned site will serve professionals, teams, and decision-makers looking for reliable AI tool comparisons with clear, actionable insights.

---

**Next Steps:**
1. Review and approve design direction
2. Create detailed component specifications
3. Begin Phase 1 implementation
4. Conduct user testing after each phase

