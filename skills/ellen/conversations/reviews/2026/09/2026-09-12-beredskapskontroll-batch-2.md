---
review_id: "2026-09-12-018"
date: "2026-09-12"
reviewer: Codex
status: approved-to-start-with-authoritative-handoff
scope:
  - "Startberedskap för Batch 2 — Sundsvall Energi Indal, Liden och Lucksta"
  - "Remote-baser, källstatus, katalogstatus och faktiska kodberoenden"
verified_remote_heads:
  skills: "ca99492877814a5a4ba41769510a4c304f947d2c"
  enkey-agents: "a4cfdb297ea9079864e70c1e2d85c73a191e8c57"
  neptune_academy: "6ca7018a08067c5135cb7e36dfe2a630add3dd29"
implementation_allowed: true
tariff_activation_allowed: false
push_allowed: false
tariff_disposition_before: "15 implemented / 49 ready / 28 blocked av 92"
tariff_disposition_after_future_approved_activation: "16 implemented / 48 ready / 28 blocked av 92"
---

# Beredskapskontroll för Batch 2

## Beslut

**Batch 2 är klar att starta enligt den nya auktoritativa handoffen.** Ingen ny extern
information behövs. Implementationen får börja lokalt, men tariffen får inte aktiveras
eller pushas före separat Codex-granskning och Roberts klartecken.

## Verifierad bas

- Batch 1 är pushad och dess lokala `main` matchar verifierad `origin/main` i alla tre
  repon vid hashvärdena i frontmatter.
- Produktrepona är rena. Orelaterade, sedan tidigare befintliga filer i `skills` ligger
  utanför Batch 2 och får inte tas med.
- Senaste fulla baslinje är grön: 700+4 skip Python, 934 TypeScript, ren tsc, godkänt
  bygge och 9/9 E2E.
- Källan är redan godkänd i verifieringslistan: tariffen består av energipris
  **100,8 öre/kWh exklusive moms**, utan fast, effekt- eller flödesavgift.
- Mekanismen för `capacity.type="not_applicable"`/`EJ_TILLAMPLIGT` finns och har
  speglade Python-/TypeScript-tester. Tariffen själv har ännu korrekt förläget
  `capacity:null`, saknar policy och är spärrad.

## Två plan-/kodglapp som handoffen gör entydiga

1. `tariffinventering-v22.md:489–492` säger felaktigt legacyväg med MWh, kronor och
   schablon. Detta motsägs av samma fils senare rättelse vid `:1297–1299` och av
   `batchplan-v22.md:723–753`. Den senare, implementeringsbara modellen är styrande:
   `contract_required:true`, minimal `Tariffpolicy`, `annual_forward`, MWh-only;
   kronor och schablon blockeras.
2. V22 planerar `blockerade_tariff_ider(katalog)` och tariffscopade `tariff_ids`, men
   den pushade koden har fortfarande bara `utredda_medlemmar()` och en medlemsbaserad
   `grind()`. Detta är inte ett externt blockerande informationsbehov, men funktionen
   måste implementeras i Batch 2 och bevisas bakåtkompatibel innan R14 omskopas.

## Godkänd omfattning

Den bindande omfattningen finns i
[`2026-09-12-001`](../../../handoffs/2026/09/2026-09-12-batch-2-sundsvall-indal.md).
Den inkluderar exakt en tariff, den planerade generiska request-scope-funktionen och
den minsta nödvändiga dokumenträttelsen. Inga andra Sundsvall-priser eller tariffer får
aktiveras.
