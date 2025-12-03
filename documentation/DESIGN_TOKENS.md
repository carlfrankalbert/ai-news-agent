# Design Tokens - FYRK AI Score Redesign

Complete design token system for the redesigned FYRK AI Score.

---

## Colors

### Base Colors
```css
:root {
  /* Backgrounds */
  --bg-base: #fafafa;
  --bg-card: #ffffff;
  --bg-muted: #f4f4f5;
  --bg-overlay: rgba(0, 0, 0, 0.4);
  
  /* Text */
  --text-primary: #0a0a0a;      /* Increased contrast */
  --text-secondary: #52525b;     /* Increased contrast */
  --text-muted: #a1a1aa;
  --text-inverse: #ffffff;
  
  /* Borders */
  --border: rgba(0, 0, 0, 0.08);      /* Increased from 0.05 */
  --border-subtle: rgba(0, 0, 0, 0.03);
  --border-strong: rgba(0, 0, 0, 0.12);
  
  /* Accents */
  --accent-primary: #2563eb;
  --accent-primary-light: #dbeafe;
  --accent-primary-dark: #1e40af;
  
  --accent-success: #16a34a;
  --accent-success-light: #dcfce7;
  --accent-success-dark: #15803d;
  
  --accent-warning: #ea580c;
  --accent-warning-light: #fed7aa;
  --accent-warning-dark: #c2410c;
  
  --accent-danger: #dc2626;
  --accent-danger-light: #fee2e2;
  --accent-danger-dark: #b91c1c;
  
  /* Rankings */
  --gold: #fbbf24;
  --gold-light: #fef3c7;
  --silver: #94a3b8;
  --silver-light: #e2e8f0;
  --bronze: #d97706;
  --bronze-light: #fed7aa;
  
  /* Category Accents */
  --category-core-llm: #3b82f6;      /* Blue */
  --category-code: #10b981;          /* Green */
  --category-builder: #8b5cf6;        /* Purple */
  --category-image: #f59e0b;         /* Orange */
  --category-audio: #ec4899;         /* Pink */
  --category-agents: #06b6d4;        /* Cyan */
}
```

### Dark Mode (Optional)
```css
:root[data-theme="dark"] {
  --bg-base: #0a0a0a;
  --bg-card: #141414;
  --bg-muted: #1a1a1a;
  --text-primary: #fafafa;
  --text-secondary: #a1a1aa;
  --text-muted: #71717a;
  --border: rgba(255, 255, 255, 0.1);
  --border-subtle: rgba(255, 255, 255, 0.05);
}
```

---

## Typography

### Font Families
```css
:root {
  --font-body: 'DM Sans', system-ui, -apple-system, sans-serif;
  --font-mono: 'IBM Plex Mono', 'Menlo', 'Monaco', monospace;
}
```

### Font Sizes
```css
:root {
  --text-xs: 12px;
  --text-sm: 13px;
  --text-base: 15px;
  --text-lg: 16px;
  --text-xl: 18px;
  --text-2xl: 20px;
  --text-3xl: 24px;
  --text-4xl: 32px;
  --text-5xl: 48px;
}
```

### Font Weights
```css
:root {
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}
```

### Line Heights
```css
:root {
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.6;
  --leading-loose: 1.75;
}
```

### Letter Spacing
```css
:root {
  --tracking-tight: -0.02em;
  --tracking-normal: 0;
  --tracking-wide: 0.05em;
  --tracking-wider: 0.1em;
}
```

---

## Spacing

### Base Unit: 8px
```css
:root {
  --space-0: 0;
  --space-1: 4px;    /* 0.5x */
  --space-2: 8px;    /* 1x */
  --space-3: 12px;   /* 1.5x */
  --space-4: 16px;   /* 2x */
  --space-5: 20px;   /* 2.5x */
  --space-6: 24px;   /* 3x */
  --space-8: 32px;   /* 4x */
  --space-10: 40px;  /* 5x */
  --space-12: 48px;  /* 6x */
  --space-16: 64px;  /* 8x */
  --space-20: 80px;  /* 10x */
  --space-24: 96px;  /* 12x */
}
```

### Semantic Spacing
```css
:root {
  --space-xs: var(--space-1);
  --space-sm: var(--space-2);
  --space-md: var(--space-4);
  --space-lg: var(--space-6);
  --space-xl: var(--space-8);
  --space-2xl: var(--space-12);
  --space-3xl: var(--space-16);
}
```

---

## Border Radius

```css
:root {
  --radius-none: 0;
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-xl: 10px;
  --radius-2xl: 12px;
  --radius-3xl: 16px;
  --radius-full: 9999px;
}
```

---

## Shadows

```css
:root {
  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.02);
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.04);
  --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.08);
  --shadow-xl: 0 12px 32px rgba(0, 0, 0, 0.1);
  --shadow-2xl: 0 16px 48px rgba(0, 0, 0, 0.12);
  
  /* Colored shadows for rankings */
  --shadow-gold: 0 2px 8px rgba(251, 191, 36, 0.3);
  --shadow-silver: 0 2px 8px rgba(148, 163, 184, 0.3);
  --shadow-bronze: 0 2px 8px rgba(217, 119, 6, 0.3);
}
```

---

## Transitions

```css
:root {
  --transition-fast: 120ms ease;
  --transition-base: 150ms ease;
  --transition-slow: 200ms ease;
  --transition-slower: 300ms ease;
  --transition-slowest: 400ms ease;
  
  /* Easing functions */
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

---

## Z-Index Scale

```css
:root {
  --z-base: 0;
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-fixed: 300;
  --z-modal-backdrop: 400;
  --z-modal: 500;
  --z-popover: 600;
  --z-tooltip: 700;
  --z-toast: 800;
}
```

---

## Breakpoints

```css
:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
  --breakpoint-2xl: 1536px;
}
```

### Usage
```css
@media (min-width: 768px) {
  /* Tablet and up */
}

@media (min-width: 1024px) {
  /* Desktop and up */
}
```

---

## Component-Specific Tokens

### Rankings
```css
:root {
  --rank-badge-size: 40px;
  --rank-badge-size-mobile: 32px;
  --rank-badge-font-size: 16px;
  --rank-badge-font-size-mobile: 14px;
}
```

### Tables
```css
:root {
  --table-row-height: 64px;
  --table-row-height-mobile: auto;
  --table-cell-padding: var(--space-4);
  --table-cell-padding-mobile: var(--space-3);
  --table-border-width: 1px;
}
```

### Buttons
```css
:root {
  --button-height: 40px;
  --button-height-sm: 32px;
  --button-height-lg: 48px;
  --button-padding-x: var(--space-4);
  --button-padding-y: var(--space-2);
  --button-border-radius: var(--radius-md);
}
```

### Cards
```css
:root {
  --card-padding: var(--space-6);
  --card-padding-mobile: var(--space-4);
  --card-border-radius: var(--radius-2xl);
  --card-shadow: var(--shadow-sm);
  --card-shadow-hover: var(--shadow-md);
}
```

---

## Animation Durations

```css
:root {
  --duration-instant: 0ms;
  --duration-fast: 120ms;
  --duration-base: 150ms;
  --duration-slow: 200ms;
  --duration-slower: 300ms;
  --duration-slowest: 400ms;
  --duration-slowest-plus: 600ms;
}
```

---

## Touch Targets

```css
:root {
  --touch-target-min: 44px;
  --touch-target-comfortable: 48px;
  --touch-target-large: 56px;
}
```

---

## Usage Examples

### Applying Tokens
```css
.button {
  padding: var(--button-padding-y) var(--button-padding-x);
  height: var(--button-height);
  border-radius: var(--button-border-radius);
  font-family: var(--font-body);
  font-size: var(--text-base);
  font-weight: var(--font-semibold);
  transition: all var(--transition-base);
  box-shadow: var(--shadow-sm);
}

.button:hover {
  box-shadow: var(--shadow-md);
}

.button:focus {
  outline: 2px solid var(--accent-primary);
  outline-offset: 2px;
}
```

### Responsive Tokens
```css
.card {
  padding: var(--card-padding);
  border-radius: var(--card-border-radius);
}

@media (max-width: 768px) {
  .card {
    padding: var(--card-padding-mobile);
  }
}
```

---

## Accessibility Tokens

```css
:root {
  /* Focus indicators */
  --focus-ring-width: 2px;
  --focus-ring-offset: 2px;
  --focus-ring-color: var(--accent-primary);
  
  /* Minimum contrast ratios (for validation) */
  --contrast-min-normal: 4.5;
  --contrast-min-large: 3;
  --contrast-min-ui: 3;
}
```

---

## Export Formats

### CSS Variables (Current)
```css
:root {
  --color-primary: #2563eb;
  /* ... */
}
```

### JSON (For Design Tools)
```json
{
  "colors": {
    "primary": "#2563eb",
    "primaryLight": "#dbeafe"
  },
  "spacing": {
    "xs": "4px",
    "sm": "8px"
  }
}
```

### SCSS Variables (Alternative)
```scss
$color-primary: #2563eb;
$spacing-xs: 4px;
```

