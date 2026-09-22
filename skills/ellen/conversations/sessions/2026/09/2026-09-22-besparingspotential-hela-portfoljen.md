---
session_id: "2026-09-22-002"
started_at: "2026-09-22T10:06:28+02:00"
last_updated: "2026-09-22T10:06:28+02:00"
timezone: "Europe/Stockholm"
participants:
  - Robert
  - Codex
status: completed
topics:
  - Optimate
  - besparingspotential
  - alla godkända tariffer
source: visible-conversation
transcript_fidelity: summarized
---

# Beslutad målbild: besparingspotential för hela godkända portföljen

Robert: ”Då vill jag att planen framåt är att bygga in denna funktion för
samltiga godkända energibolag.”

Beslutet tolkas på nät-/tariffproduktnivå eftersom ett bolag kan ha flera
olika produkter. Codex kontrollerade nuvarande 2026-snapshot i kalkylatorn:
75 valbara produkt-ID:n, varav 74 verkliga och ett syntetiskt
riksgenomsnitt. Åtta val har befintlig äldre besparingsväg, 67
kontraktsstyrda val är satta till `stodjer_besparing=false`; Stockholm
Exergis nya Optimate-vy är en separat lokal prototyp.

Den dokumenterade [genomförandeplanen](../../../proposals/2026/09/2026-09-22-besparingspotential-alla-godkanda-tariffer.md)
anger mätbar 74/74-täckning, gemensam scenariomotor, tariffspecifika
beroende- och datagrindar, familjevis utrullning och verifiering. Den
skiljer preliminär energibesparing från villkorad effekt, flöde och retur.
Roberts 15/20/25-procenttal är scenarier, inte fakturerat utfall.

Ingen kod, tariffaktivering, commit, push eller automatisk agentstart
gjordes i denna planeringsrunda. Den lokala testservern från session
`2026-09-22-001` fortsätter att vara igång för Robert.
