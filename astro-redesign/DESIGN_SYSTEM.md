# FYRK AI Radar - Design System

## Summary of Improvements

### Visual Refinements
- **Typography Hierarchy**: Clear H1/H2/H3 system with improved line-height and letter-spacing
- **Spacing Rhythm**: Consistent 8px base unit with harmonious spacing scale
- **Card Design**: Uniform cards with subtle shadows, rounded corners (12px), improved hover states
- **Color Palette**: Refined black/white with subtle grays, maintaining Scandinavian minimalism
- **Animations**: Smooth 150ms transitions with subtle scale and opacity effects
- **Hero Section**: Larger headline, improved subhead, prominent CTA with gradient accent
- **Featured Tools Strip**: Horizontal scrolling strip for top tools
- **FYRK Recommends**: Curated block highlighting recommended tools
- **Mobile Optimization**: Significantly improved mobile layout with better touch targets

### Technical Improvements
- **Astro Framework**: Modern static site generation
- **Tailwind CSS**: Utility-first styling with design tokens
- **Component Architecture**: Reusable, maintainable components
- **Performance**: Lightweight, optimized bundle
- **Accessibility**: Improved semantic HTML and ARIA labels

## Wireframe Description

```
┌─────────────────────────────────────────┐
│  Header: Logo | Lang | Contact          │
├─────────────────────────────────────────┤
│                                           │
│  Hero: Large H1 + Subhead + CTA         │
│  [Soft gradient background]               │
│                                           │
├─────────────────────────────────────────┤
│  Featured Tools Strip (horizontal)       │
│  [Card] [Card] [Card] [Card] →          │
├─────────────────────────────────────────┤
│  Metrics Explanation (compact cards)     │
│  [Buzz] [Sentiment] [Utility] [Price]   │
├─────────────────────────────────────────┤
│  Filter Pills                            │
│  [All] [Core LLMs] [Code] ...           │
├─────────────────────────────────────────┤
│  Category Sections (expandable)         │
│  ┌─────────────────────────────────┐   │
│  │ Category Title                   │   │
│  │ ┌───┬──────────┬────┬────┬────┐ │   │
│  │ │ # │ Name     │Bz  │Sent│... │ │   │
│  │ ├───┼──────────┼────┼────┼────┤ │   │
│  │ │ 1 │ Tool     │100 │ 95 │... │ │   │
│  │ │ 2 │ Tool     │ 90 │ 85 │... │ │   │
│  │ └───┴──────────┴────┴────┴────┘ │   │
│  └─────────────────────────────────┘   │
├─────────────────────────────────────────┤
│  FYRK Recommends (curated block)        │
│  [Large Card] [Card] [Card]             │
├─────────────────────────────────────────┤
│  CTA Section                             │
│  "Want to use AI more effectively?"     │
│  [Contact Button]                        │
├─────────────────────────────────────────┤
│  Footer: Logo | Links | Meta            │
└─────────────────────────────────────────┘
```

## Component List

1. **Header.astro** - Site header with logo and navigation
2. **Hero.astro** - Hero section with headline and CTA
3. **FeaturedTools.astro** - Horizontal scrolling strip
4. **MetricsInfo.astro** - Metrics explanation cards
5. **FilterBar.astro** - Category filter pills
6. **CategorySection.astro** - Ranking table section
7. **RankingTable.astro** - Individual ranking table
8. **RankingRow.astro** - Table row component
9. **FyrkRecommends.astro** - Curated recommendations
10. **CTA.astro** - Call-to-action section
11. **Footer.astro** - Site footer
12. **MedalBadge.astro** - Rank badge (1, 2, 3)
13. **ProviderLogo.astro** - Provider logo with link

## Design Tokens

```json
{
  "colors": {
    "brand": {
      "navy": "#001F3F",
      "cyan": "#5AB9D3",
      "white": "#FFFFFF"
    },
    "neutral": {
      "900": "#0A0A0A",
      "800": "#18181B",
      "700": "#27272A",
      "600": "#52525B",
      "500": "#71717A",
      "400": "#A1A1AA",
      "300": "#D4D4D8",
      "200": "#E4E4E7",
      "100": "#F4F4F5",
      "50": "#FAFAFA"
    },
    "semantic": {
      "success": "#16A34A",
      "warning": "#EA580C",
      "error": "#DC2626",
      "info": "#2563EB"
    },
    "medals": {
      "gold": "#FFD700",
      "silver": "#C0C0C0",
      "bronze": "#CD7F32"
    }
  },
  "spacing": {
    "0": "0px",
    "1": "4px",
    "2": "8px",
    "3": "12px",
    "4": "16px",
    "5": "20px",
    "6": "24px",
    "8": "32px",
    "10": "40px",
    "12": "48px",
    "16": "64px",
    "20": "80px",
    "24": "96px"
  },
  "radius": {
    "sm": "6px",
    "md": "10px",
    "lg": "12px",
    "xl": "16px",
    "2xl": "20px",
    "full": "9999px"
  },
  "shadows": {
    "sm": "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    "md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    "lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
    "xl": "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)"
  },
  "typography": {
    "fontFamily": {
      "sans": ["DM Sans", "system-ui", "sans-serif"],
      "mono": ["IBM Plex Mono", "monospace"]
    },
    "fontSize": {
      "xs": ["12px", "16px"],
      "sm": ["14px", "20px"],
      "base": ["15px", "24px"],
      "lg": ["16px", "24px"],
      "xl": ["18px", "28px"],
      "2xl": ["20px", "28px"],
      "3xl": ["24px", "32px"],
      "4xl": ["32px", "40px"],
      "5xl": ["48px", "56px"]
    },
    "fontWeight": {
      "normal": "400",
      "medium": "500",
      "semibold": "600",
      "bold": "700"
    }
  },
  "transitions": {
    "fast": "120ms",
    "base": "150ms",
    "slow": "180ms"
  }
}
```

