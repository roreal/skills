---
handoff_id: "2026-09-25-002"
created_at: "2026-09-25T09:02:13+02:00"
from: Codex
to: Claude
status: approved-for-implementation
approved_by:
  - Robert
  - Codex
---

# APPROVED_FOR_IMPLEMENTATION: Claude – portföljgrund 10/15/20 och aktuell matris

## Mandat och mål

Robert har testat Stockholm 10/15/20 och godkänt att de fem beslutade
utrullningsstegen genomförs. Detta uppdrag är den avgränsade grunden för
steg 1–2:

1. gör 10/15/20 till standard i den gemensamma scenariomotorn,
2. regenerera en aktuell, sanningsenlig täckningsmatris.

Ingen publik tariff aktiveras i denna leverans. Våg 1 startas först efter
Codex granskning av denna grund.

## Verifierade lokala baser

- skills `main@49866d822816efc1e93c4fbb537d711928904c67`
- neptune_academy lokal `main@e864d6ebbb1d258ddf5534bd1692e7d95b7aae96`
- Neptunes commit ovan är den slutgranskade Stockholm 10/15/20-leveransen.
- enkey-agents ska inte ändras; lokal `main@5150d0b` innehåller
  orelaterat Milesight-arbete.

Remote-pushen av Stockholm är separat blockerad av Claudes externa
pushklassificerare. Det ändrar inte den rena lokala kodbasen och får inte
blandas in i denna implementation.

## A. Gemensam scenariomotor

Tillåtna Neptune-filer:

- `neptune-marketing/src/utils/optimateScenario.ts`
- `neptune-marketing/src/utils/optimateScenario.test.ts`

Krav:

1. Byt den generiska motorns fasta scenarioandelar från 15/20/25 till
   10/15/20 procent.
2. Uppdatera samtliga kommentarer, variabelnamn och testfacit i dessa två
   filer. Inga stale generiska 15/20/25-påståenden får finnas kvar.
3. För pilotfixturen 96 MWh styrbar rumsvärme ska sparad energi vara
   `[9,6; 14,4; 19,2]` MWh och köpt totalvärme efter vara
   `[110,4; 105,6; 100,8]` MWh.
4. Referens, övrig last, kapacitet, flöde, retur, historik och behörighet
   ska fungera exakt som tidigare. Samma tariffmotor används före/efter.
5. Intern pilotallowlist förblir exakt Sundsvall Indal/Liden/Lucksta.
6. Publik allowlist förblir tom. Ingen UI-inkoppling eller
   `stodjer_besparing`-ändring.

## B. Aktuell täckningsmatris

Tillåtna skills-filer:

- `Fjarrvarmetariffer/generera_besparingspotential_tackningsmatris.py`
- `Fjarrvarmetariffer/test_generera_besparingspotential_tackningsmatris.py`
- `Fjarrvarmetariffer/besparingspotential-tackningsmatris-2026.json`
- `Fjarrvarmetariffer/besparingspotential-tackningsmatris-2026.md`

Krav:

1. Parsningen ska acceptera generatorns verkliga katalogcommitformat,
   7–40 hextecken, men fortsatt avvisa saknad eller icke-hex proveniens.
   Bind test för både kort och full hash.
2. Regenerera mot exakt Neptunes lokala `main@e864d6e` och bind den
   resulterande käll-SHA:n/proveniensen.
3. Mekaniskt förväntat nuläge är:
   - 77 produktval = 76 verkliga + 1 syntetiskt,
   - 8 befintliga besparingsvägar,
   - 69 enbart kontraktsstyrd årskostnad,
   - vågor `1:2`, `2:15`, `3:48`, `4:12`.
4. Lägg en explicit, fail-closed scenario-status i matrisen:
   - Stockholm: synlig särskild preliminär prototyp, 10/15/20,
   - Sundsvall Indal/Liden/Lucksta: godkänd intern pilot, inte publik,
   - övriga 75: ej granskade.
   Statusregistret ska vara en namngiven konfiguration med test att alla
   angivna ID:n finns exakt en gång i snapshoten; ingen tyst fallback för
   okända status-ID:n.
5. Matrisens sammanfattning ska skilja 76 verkliga leverantörsprodukter
   från det syntetiska riksgenomsnittet. Utrullningens måltal är de 76
   verkliga produkterna; riksgenomsnittet redovisas separat.
6. Bekräfta särskilt att Gävle och Härnösand finns i den nya matrisen
   och hamnar i våg 2.

## Verifiering

- Riktade `optimateScenario`-test och hela Vitest med den fungerande
  Härnösand-/Python-miljön.
- `npx tsc --noEmit` och isolerat bygge; återställ spårad `dist/`.
- Python-unittest för matrisgeneratorn, `--check`, deterministisk andra
  generering och `git diff --check`.
- Bevisa exakt fillista i respektive repo.

Arbeta i ny isolerad Neptune-worktree/branch baserad på `e864d6e`.
Committa Neptune- och skills-delarna fokuserat och skriv en ny unik
`REVIEW_READY: Codex`-toppost. Ingen aktivering, push, merge, rebase eller
historikomskrivning.
