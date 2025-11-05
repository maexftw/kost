# Performance – Core Web Vitals & Budgets

- Budgets (default, override per project):
  - LCP ≤ 2.5s
  - INP ≤ 200ms
  - CLS ≤ 0.1
  - Hero image ≤ 200KB (webp/avif), other images ≤ 100KB where possible
- Images: dimensions set, responsive srcset, lazy-load non-critical
- Critical CSS: inline minimal above-the-fold; defer rest
- JS: defer/async; avoid long tasks; remove unused deps
- Fonts: swap/fallbacks; subset; limit weights
- Caching: set proper cache headers; reuse CDN
