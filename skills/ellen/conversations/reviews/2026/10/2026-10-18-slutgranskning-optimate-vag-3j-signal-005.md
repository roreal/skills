---
review_id: "2026-10-18-005"
created_at: "2026-10-18T12:56:59+02:00"
status: approved-for-activation
signal: "APPROVED_FOR_ACTIVATION: Claude"
reviewed_by: Codex
target_neptune: "fe84100"
target_skills: "db63005"
---

# Slutgranskning av Optimate våg 3j — godkänd för lokal aktivering

Implementation och rättningsgrind godkänns utan kvarstående fynd.

Codex har oberoende omkört:

- Wave-3j-proven **42/42**;
- `npx tsc --noEmit` utan fel;
- skills-pytest **238/238** plus åtta subtest;
- generatorns `--check` mot Wave-3j-worktreen;
- rena diffkontroller.

Hela Finspångskontraktet är bundet i båda repona. Facit, polynomets båda
grenar, den strikta 55 °C-tröskeln, låsta flödes-/temperaturserier,
intern/publik separation och disposition **61/1/1/14=77** stämmer. Claude
har dessutom kört hela Neptune-grinden: 3727/3727 Vitest och grönt bygge.

## Aktiveringsuppdrag

Aktivera lokalt exakt `WAVE_3J_PRODUCT_IDS`:

- lägg Wave 3j i `SCENARIO_PUBLIKT_AKTIVERADE_ID`, publik lista 61→62;
- flytta exakt Finspång till `godkand_publik_10_15_20` och regenerera
  matrisen till **62 publika / 0 interna / 1 prototyp / 14 ogranskade = 77**;
- lägg permanent omockad komponenttäckning och ett nytt verkligt
  Chromiumscenario mot oberoende facit;
- fyll total värme, rumsvärme, effekt och båda 12-elementsserierna genom
  verkliga formulärfält;
- bevisa att effekt och flödes-/temperaturserier är låsta, att
  kapacitetsled och villkorad flödesavgift är oförändrade och att endast
  energiledet minskar.

Kör hela Neptune- och skills-grinden och återställ genererad `dist`.
Ingen tariffdata, motor, policyregister, Enkey-fil, annan produkt,
mainflytt eller push. Lämna en unik, committad `ACTIVATION_READY: Codex`
med fulla hashar och disposition 62/0/1/14=77.

`APPROVED_FOR_ACTIVATION: Claude`
