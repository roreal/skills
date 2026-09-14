---
session_id: "2026-09-14-002"
date: "2026-09-14"
participants: [Robert, Codex, Claude]
status: "Batch 5a godkänd för lokal implementation bakom åtta spärrar; ingen aktivering eller push"
topic: "Batch 5a: åtta tariffer med leverantörens effekt och bekräftade band"
relates_to:
  - "conversations/handoffs/2026/09/2026-09-14-batch-5a-leverantorsvarde.md"
  - "conversations/reviews/2026/09/2026-09-14-beredskapskontroll-batch-5a.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 5a"
---

# Session: Batch 5a — leverantörens effekt och bekräftade band

## Startbeslut

Robert bad Codex kontrollera loggen och, om Batch 4 var tillfredsställande,
ta nästa batch. Codex verifierade de tre faktiska `origin/main` med
`git ls-remote`:

- `skills@13b2a4ffc4520b7ebaca10eaa2efe0eb548259ff`;
- `enkey-agents@5d498cfab3f968af42ba60751b5143c6f96536e0`;
- `neptune_academy@ebe4d621ff800cab1f8248cd8e4e07ba042064fd`.

Batch 4 har ingen opushad kod och är stängd på 37 implemented / 27 ready /
28 blocked av 92, med 39 skarpa produkter. Den tidigare felaktiga uppgiften
om pushauktorisation är uttryckligen rättad i Batch 4-loggen; Robert har valt
att låta pushen stå kvar.

## Beredskapsbedömning

Batchplan V22 anger Batch 5a som nästa steg. Codex jämförde de åtta
katalograderna med aktuella officiella 2026-källor och den redan pushade
band-ID-/resultatkontraktsinfrastrukturen. Slutsatsen är att ingen ny motor
behövs: varje produkt kan uppskatta årskostnaden med tolv MWh-värden,
leverantörens numeriska effekt och leverantörens bekräftade band.

En motsägelse i Batch 5a-texten rättades: valt band-ID ska inte valideras mot
parserns intervalltolkning. Katalogens normativa kontrakt och inventeringens
§6a.2 säger att det bekräftade ID:t väljer prisraden direkt, särskilt i C4:s
tvetydiga 500 kW-fall.

## Bindande handoff

Claude ska följa
`conversations/handoffs/2026/09/2026-09-14-batch-5a-leverantorsvarde.md`.
Uppdraget omfattar:

- aktuell 2026-proveniens för samtliga åtta;
- katalogrättelser för C4, Kil och TEMAB samt requestlivscykel R05/R12/R13;
- åtta policyer med exakt effekt + bekräftat band;
- oberoende golden-facit i båda språken och UI-/produktbytesprov;
- mekaniskt bevis att spärrar, 37/27/28 och 39 skarpa produkter består.

Ingen aktivering och ingen push är godkänd. Claude ska göra fokuserade lokala
commits, logga hashar/tester här och stanna för Codex granskning.

## Händelselogg

- `2026-09-14T20:53:08+02:00` – Codex verifierade Batch 4:s remote-huvuden,
  återverifierade Batch 5a:s aktuella officiella källor, rättade V22:s
  bandsemantik och utfärdade beredskapskontroll `2026-09-14-011` samt handoff
  `2026-09-14-002`.
