---
review_id: "2026-10-16-007"
created_at: "2026-10-16T22:15:29+02:00"
reviewer: Codex
subject: "Optimate våg 3h — slutgranskning efter sluträttningen"
status: approved-for-activation
signal: "APPROVED_FOR_ACTIVATION: Claude"
approved_by: Codex
dispatched_by: agent-bridge
---

# Slutgranskning av Optimate våg 3h, signal 006

Sluträttningen `9cf9aab` godkänns utan kvarstående fynd. Båda punkterna i
omgranskning 2026-10-16-005 är stängda:

- Mölndals och Norrenergis hela kapacitetsobjekt djupjämförs nu exakt,
  inklusive toppnivåns nyckelmängd och hela den ordnade bandtabellen.
- Legacy-backendens negativa prov skiljer nu korrekt mellan okänt ID,
  kontraktsgatade katalog-ID:n och det verkliga men syntetiska, ogranskade
  katalogobjektet `riksgenomsnitt`.

Codex omkörde de två berörda testfilerna: **53/53** prov gröna, ren
`npx tsc --noEmit`, ren worktree och ren diff. Claudes fulla grind är också
grön: **3624/3624** Vitest, produktionsbygge med återställd `dist`,
**155/155** skills-prov plus fyra subtest samt grön generatorcheck.
Dispositionen är fortsatt **57 publika / 3 interna / 1 prototyp / 16
ogranskade = 77** och den publika listan är fortsatt exakt 57.

## Godkänd lokal aktivering

Aktivera lokalt exakt:

1. `gotlands-energi-gotland-taxa-21-over-50-mwh-ar`
2. `molndal-energi`
3. `norrenergi`

Krav för aktiveringsleveransen:

- lägg exakt `WAVE_3H_PRODUCT_IDS` i den publika allowlisten och bind hela
  listan mekaniskt till **60 unika, frysta ID:n**;
- flytta exakt samma tre matrisrader från
  `godkand_intern_pilot_ej_publik` till
  `godkand_publik_10_15_20`, med ny disposition **60/0/1/16=77**;
- lägg omockade komponent-/sidprov som bevisar att 10/15/20-kortet är
  synligt endast efter den publika grinden för samtliga tre och att
  nödvändiga tariffindata kan lämnas utan ID-specialfall i sidan;
- lägg eller utöka Chromium/E2E så att samtliga tre produkter körs genom
  den verkliga kalkylatorsidan med handoffens explicita 120 MWh-serie och
  låsta tariffvärden samt jämförs mot de redan oberoende faciten;
- bevisa negativt att minst ett fortsatt ogranskat objekt, inklusive
  `riksgenomsnitt`, saknar publikt besparingskort;
- ändra inte tariffdata, prisformler, scenarioalgoritm, enkey-agents eller
  någon annan produkt.

Kör hela Vitest, `tsc`, bygge med återställd `dist`, hela Chromiumsviten,
skills pytest, generatorcheck och diffkontroller. Committera lokalt och
lämna `ACTIVATION_READY: Codex` med fulla hashar och disposition.

Ingen mainflytt eller push.

`APPROVED_FOR_ACTIVATION: Claude`
