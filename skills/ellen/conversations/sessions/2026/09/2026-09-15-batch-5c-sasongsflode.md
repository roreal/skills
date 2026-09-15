---
session_id: "2026-09-15-018"
created_at: "2026-09-15T21:08:00+02:00"
participants:
  - Robert
  - Codex
  - Claude
status: ready-for-claude-local-implementation
scope: "Batch 5c — åtta tariffer med säsongsvis flödesavgift"
remote_baseline:
  skills: "df41660620f572b5b22d7dd27332c68b1be62049"
  enkey_agents: "5eaca3c4f3eafb3c7065319803592abe062f49ae"
  neptune_academy: "28ae62945ed50b23cffadd5a7b3070cc2d5c41ae"
relates_to:
  - "conversations/reviews/2026/09/2026-09-15-beredskapskontroll-batch-5c.md"
  - "conversations/handoffs/2026/09/2026-09-15-batch-5c-sasongsflode.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 5c"
---

# Session: Batch 5c — säsongsflöde

## 2026-09-15 21:08 — Codex förbereder nästa steg

Robert meddelade att Claude verifierat Batch 5b-pushen och bad Codex
förbereda nästa steg.

Codex verifierade att lokala huvuden matchar `origin/main`:

- `skills@df41660620f572b5b22d7dd27332c68b1be62049`
- `enkey-agents@5eaca3c4f3eafb3c7065319803592abe062f49ae`
- `neptune_academy@28ae62945ed50b23cffadd5a7b3070cc2d5c41ae`

`enkey-agents` och `neptune_academy` är rena. `skills` innehåller sedan
tidigare orelaterade ändringar/otaggade filer; de ingår inte i detta uppdrag
och ska lämnas orörda.

Beredskapskontroll `2026-09-15-018` godkänner lokal implementation av
Batch 5c bakom spärr. Handoff `2026-09-15-002` ger Claude ett bindande
uppdrag för exakt åtta tariffer.

Det centrala beslutet är att säsongsflöde ska bäras som en 12-elements
kalendermånadsserie i befintliga `number_series`/`falt_serier`, varefter
motorn summerar exakt varje `volume`-posts egna `months`. Därmed kan 5, 6,
7 och 9 debiteringsmånader bevisas mekaniskt och ett exkluderat månadsflöde
garanteras ge noll kostnadsbidrag.

Sju tariffer kräver leverantörens effekt + bekräftat band + flödesserie.
Mälarenergi 2–4 lägenheter saknar kapacitetsdel och kräver bara energi och
flödesserie utöver sin fasta årsavgift. R03 ska scopesäkras till de två
andra fortsatt blockerade Mälarenergi-raderna; frågan är inte besvarad.

Utgångsläge och grind:

- skarpt under implementation: 51/13/28, 53 produkter;
- isolerat med exakt åtta spärrar rensade: 59/5/28, 61 produkter;
- ingen aktivering och ingen push före Codex granskning och Roberts senare
  uttryckliga beslut.

## Nästa svar från Claude

Claude ska läsa beredskapskontrollen och hela handoffen, implementera och
committa lokalt i berörda repon, logga exakta hashar/tester och stanna med
formuleringen att Batch 5c är implementerad bakom spärr men inte aktiverad
eller pushad.
