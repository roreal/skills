---
review_id: "2026-09-12-014"
date: "2026-09-12"
reviewer: Codex
status: approved-for-local-activation
scope:
  - "Slutgranskning av Batch 1-rättningsrunda 5 efter 2026-09-12-013"
  - "Kumulativ implementation av sex annual_forward-tariffer"
reviewed_heads:
  skills: "ce2704a59bf6f78af7e93b41c95b5692233dda27"
  skills_catalog_commit: "d2b035e9ed27dcc1b7c8d0dafbef795570c996d3"
  enkey-agents: "59eb6ba62affeaca14cdd0b16f09004f98aa110d"
  enkey-agents_batch1_commit: "cd4c2ce7f1211618c86cd1c11bfba6e53790e07e"
  neptune_academy: "80c65ffcaeab8b5351642858dac72806398f365f"
remote_heads_verified:
  skills: "c0457515d96ffd0a58e59e6b4b69f62c2a89229b"
  enkey-agents: "59eb6ba62affeaca14cdd0b16f09004f98aa110d"
  neptune_academy: "d0dfb927f1e4815208acc45b041a4ec8df890401"
implementation_changed_by_reviewer: false
local_activation_allowed: true
push_allowed: false
tariff_disposition_before_activation: "9 implemented / 55 ready / 28 blocked av 92"
tariff_disposition_after_approved_activation: "15 implemented / 49 ready / 28 blocked av 92"
rechecks_review: "2026-09-12-013"
---

# Slutgranskning av Batch 1

## Beslut

**Godkänd för separat lokal aktivering.** Rättningsrunda 5 stänger de två sista
P2-fynden från granskning 013 och den kumulativa implementationen av följande sex
tariffer är godkänd:

1. Karlstads Energi 2026
2. Södertörns Fjärrvärme/SFAB 2026
3. VänerEnergi 2026
4. Övik Energi 2026
5. Telge Nät 2026
6. Partille Energi 2026

Godkännandet avser kalkylatorns **uppskattade årskostnad** enligt produktmålet. Det
är inte ett godkännande att hitta på eller visa månadsbelopp när leverantörens
månadsperiodisering saknas. Sådana frågor ska ligga kvar synligt och den månadsvisa
vägen ska fortsätta vara fail-closed.

Claude får nu göra den lokala aktiveringen av exakt dessa sex tariff-ID:n. Ingen push
är tillåten före Codex separata granskning av den faktiska aktiveringsdiffen.

## Stängda fynd

- Telge och Partille accepterar 0 kW i HTML, normal knappsubmit och domänlagret.
- Negativa värden ger nu den sanningsenliga texten ”måste vara minst 0” med fältnära
  ARIA, utan att påstå att det giltiga värdet 0 är ogiltigt.
- Telges källbelagda heltalsavrundning är identisk i Python och TypeScript. Decimal
  blockeras och heltal går igenom.
- Karlstad, Södertörn, VänerEnergi och Partille accepterar decimal kapacitet enligt
  sina policyer; Övik och Telge kräver heltal. Sandvikens befintliga heltalsregel är
  bevarad.
- Samtliga 39 kapacitetsband provas mot både vald bandidentitet, gränser och
  oberoende kapacitetskostnad.
- Partilles öppna toppband visas som `7 (2501+ kW)`.
- Den handunderhållna TypeScript-fixturen jämförs komplett med Pythonkatalogens
  `till_prisar()` och serialiserade policy utan tyst skip.
- Obligatoriska fält, typ-/gränsfel, produktbegränsningar och ARIA är fail-closed.

## Oberoende verifiering

- Python, hela tariffsviten: **698 passed, 4 skipped**, 0 failed.
- TypeScript, hela sviten: **894 passed** i 27 filer, 0 failed/0 skipped.
- Riktad Batch 1/UI/driftmatris: **280 passed** i 4 filer.
- `npx tsc --noEmit`: godkänt.
- `npm run build`: godkänt; endast befintlig bundlevarning.
- `npm run test:e2e`: samtliga **8** scenarier godkända.
- Bygggenererade `dist`-ändringar återställdes. Produktrepona är rena och
  `git diff --check` är rent.
- Katalogen ger fortsatt `godkanda(katalog)=9`; alla sex kandidater har fortfarande
  `investigation.status="utreds"`, alltså har ingen aktivering skett i smyg.

Pytest kunde inte skriva sin cache i sandboxen, vilket gav en varning men inte
påverkade de 698 godkända proven.

## Icke-blockerande redaktionell notis

`resultatkontrakt.batch1.test.ts` nämner även Sandviken/Lidköping i ett testnamn och
en kommentar trots att `BATCH1` bara innehåller de sex kandidaterna. Själva provet
kör rätt policyvillkor för Telge och Övik och resultatet är korrekt. Texten kan
förenklas till ”Batch 1-fält med `heltal=true`” under aktiveringsrundan; detta är
inte ett funktions- eller aktiveringshinder.

## Tillåten lokal aktiveringsrunda

1. Ändra endast de sex angivna katalogposternas aktiveringsspärr från
   `investigation.status="utreds"` till `investigation: null`, enligt det befintliga
   Lidköpingsmönstret. Ändra inte priser, band, formler, kapacitetsbaser eller
   obligatoriska fält.
2. **Bevara** de kända issue-texterna om okänd månadsperiodisering för Karlstad,
   Södertörn, VänerEnergi och Partille. De är avsiktligt godkända för årsprodukten
   men ska fortsatt blockera månadsvis fakturaredovisning. Rensa endast villkoret att
   implementationen väntar på granskning/aktivering.
3. Lägg en ny katalogrevision som tydligt säger att sex annual_forward-adaptrar
   aktiveras för uppskattad årskostnad, att månadsosäkerheten bevaras och att övriga
   katalogposter är orörda. Uppdatera katalogens versions-/datumfält konsekvent.
4. Uppdatera permanenta katalogtester från 9 till exakt **15** godkända tariffer och
   från 7 till exakt **13** leverantörer. Bevisa både de sex nya ID:na och att ingen
   sjunde tariff frigjorts. Förväntad disposition är **15/49/28 av 92**.
5. Regenerera TypeScript-artefakten från exakt den committade katalogversionen och
   uppdatera SHA-/commitproveniens genom den befintliga generatorn. Inga manuella
   ändringar i genererad tariffdata.
6. Lägg ett omockat acceptansprov mot den verkligt genererade artefakten: alla sex
   ska finnas i leverantörsvalet och komplett MWh-/annual_forward-indata ska nå ett
   riktigt årsresultat utan schablonfallback. Kr-/schablon- och otillräckliga
   underlag ska fortsatt blockeras typat.
7. Låt E2E kontrollera minst en verkligt aktiverad Batch 1-tariff och att alla sex
   finns i dropdownen. Kör därefter full Python, full TypeScript, tsc, bygge och E2E.
8. Commitera fokuserat per repo och stanna för Codex. Pusha ingenting.

`enkey-agents@59eb6ba` ligger redan på remote och innehåller Batch 1-koden under en
senare orelaterad commit. Historiken ska inte skrivas om eller backas. Vid den lokala
aktiveringen får endast nödvändiga nya kataloghash-/teständringar läggas ovanpå.
