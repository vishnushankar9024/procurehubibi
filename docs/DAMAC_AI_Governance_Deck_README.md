# DAMAC PMWeb — Enterprise AI Governance & Intelligence Layer

Executive consulting presentation for DAMAC leadership and technology stakeholders.

## Deliverable

| File | Description |
|------|-------------|
| `output/DAMAC_PMWeb_AI_Governance_Intelligence_Layer.pptx` | Boardroom-ready PowerPoint (35 slides) |

## Theme

- **Layout:** White/off-white slides with **black text** and **red accents** (not full dark slides)
- **Logos:** CMCS (top-right) and DAMAC (top-left) on every content slide — see `assets/`
- **AI Recommendation:** **Claude Enterprise** (single platform — not hybrid)
- **Positioning:** Enterprise AI Governance & Intelligence Layer — **not** direct AI-to-PMWeb/database connectivity
- **Style:** Premium McKinsey/Deloitte executive consulting deck

## Presentation Structure

1. **Executive Summary** — Challenges, opportunity, Current vs Future State
2. **DAMAC Use Cases** — CO approval, contract intelligence, management chatbot
3. **Why Direct AI-to-PMWeb Is Risky** — Anti-pattern vs recommended pattern
4. **Recommended Enterprise Architecture** — Layered architecture + RAG
5. **AI Model Comparison** — Claude, OpenAI, Azure, Gemini + **Claude Enterprise recommendation**
6. **Enterprise Pricing** — Token tables, scenarios, cost optimization
7. **Implementation Strategy** — 4-phase roadmap with timelines
8. **Security & Governance** — RBAC, audit, human-in-the-loop
9. **Future Vision** — DAMAC AI Governance Platform
10. **Final Recommendation** — Decision ask and next steps

## Regenerate

```bash
pip install -r requirements.txt
python3 scripts/generate_damac_ai_governance_deck.py
```

## Customization

Edit `scripts/generate_damac_ai_governance_deck.py` to adjust:

- Brand colors (`RED`, `BLACK`, etc.)
- Pricing tables (Section 06)
- Phase timelines (Section 07)
- DAMAC-specific use case wording

## Note on Pricing

Section 06 uses **indicative May 2026 enterprise API rates** for business-case modeling. Validate against current vendor contracts before board submission.
