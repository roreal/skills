---
review_id: "2026-09-14-008"
date: "2026-09-14"
reviewer: Codex
status: approved-for-separate-local-activation
scope: "Slutgranskning av Batch 4 rättningsrunda 4 efter granskning 007"
reviewed_heads:
  skills: "a0d9f75"
  skills_catalog: "c1d83200c08903610e28ac20c504d748dd067081"
  enkey_agents: "fcecc48"
  neptune_academy: "dfe4b9f"
activation_allowed: true
push_allowed: false
review_required_before_push: true
tariff_disposition_before_activation: "33 implemented / 31 ready / 28 blocked av 92"
tariff_disposition_after_approved_activation: "37 implemented / 27 ready / 28 blocked av 92"
follows: "2026-09-14-007"
---

# Slutgranskning av Batch 4 rättningsrunda 4

## Beslut

**Godkänd för en separat lokal aktiveringsrunda.** Det sista P1-fyndet i granskning 007
är stängt. Umeås komponentkandidat speglar nu produktionspolicyns treåriga
`kalperiod_definition`, `rullande:false`, exakta effektetikett och hjälptext. Periodfältets
rendering, saknade/ogiltiga värde, normala submit och rensning vid produktbyte är provade.

Ingen produktions-, motor-, tariff- eller aktiveringsändring gjordes i fix-runda 4. De
fyra kandidaterna ligger fortfarande bakom `investigation.status="utreds"`, den skarpa
generatorn har fortsatt 33 katalogprodukter + 2 leverantörsfiler och dispositionen är
**33/31/28 av 92**. Lokal aktivering får nu göras enligt ordern nedan. **Ingen push före
en ny Codex-granskning av aktiveringsdiffen.**

## Stängt och verifierat

- Umeåmockens kapacitetskrav använder samma icke-tomma kalenderdefinition,
  `rullande:false`, `Debiterbar årseffekt (A)` och hjälptext som
  `policyregister.py:_umea_kapacitet_krav` producerar.
- `#kapacitetKw-period` visas med rätt etikett och hela treårsbeskrivningen.
- Saknad period och formatet `2023-01` ger fältnära `#kapacitetKw-fel`; ARIA är kopplad
  till periodfältet.
- Normal Umeå-submit använder `2023-01-01/2025-12-31` och ger ett synligt uppskattat
  resultat.
- Jämtkraft→Umeå visar ett tomt periodfält; Umeå→Jämtkraft tar bort det och byte tillbaka
  återanvänder inte den tidigare perioden.
- De tidigare B-, band- och flödesfelproven fyller en giltig period så att de träffar rätt
  felväg.
- Riktat komponentprov: **20 passed**.
- Full TypeScript-svit: **1221 passed** i 41 filer; `npx tsc --noEmit` rent.
- Full tariffsvit Python: **1272 passed, 4 skipped**; endast sandboxens cachevarning.
- Isolerat eval-bygge grönt; endast känd bundelstorleksvarning.
- Korrekt serverad kalkylator: **15/15 E2E** gröna. Batch 4 är ännu spärrad och ingår
  därför avsiktligt inte i skarp E2E.
- Generatorsynk: **2 passed**. Mekaniskt: katalog 86, `godkanda()` 33 och inga Batch
  4-ID:n aktiva. Diffkontrollerna är rena; orelaterad arbetskopiesmuts är orörd.

## Bindande lokal aktiveringsorder till Claude

1. Aktivera exakt dessa fyra katalogposter och inga andra:
   - `jamtkraft-ostersund-froson-as-2026`;
   - `jamtkraft-brunflo-och-opevagen-2026`;
   - `jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge-2026`;
   - `umea-energi-umea-enkel-2026`.
2. Sätt endast deras rena implementationsspärr `investigation` till `null`. Ändra inte
   priser, energisäsonger, kapacitetsband, effekt-/flödesformler, `issues`,
   `production_ready`, `contract_required`, källor eller någon annan tariff. Jämtkrafts
   kvarvarande månadsperiodiseringsissue ska ligga kvar eftersom godkännandet gäller
   uppskattad årskostnad, inte fakturamånader.
3. Uppdatera katalogrevision/historik och levande inventering, batchplan,
   verifieringslista, sessionslogg, handoff och index till det faktiska lokala läget.
   Flytta exakt fyra poster från `ready_to_implement` till
   `implemented_source_verified_annual`. Slutdispositionen ska vara exakt
   **37 implemented / 27 ready / 28 blocked av 92**; katalogen ska fortsatt ha 86
   fysiska poster.
4. Commitera katalog-/dokumentaktiveringen fokuserat i `skills` så dess slutliga
   katalogcommit kan anges som proveniens. Regenerera därefter TypeScriptartefakten med
   exakt den commiten. Generatorn ska ge **39 skarpa produkter totalt**: 37 ur katalogen
   och 2 leverantörsfiler.
5. Bevisa semantiskt att generatordiffen lägger till exakt de fyra ID:na ovan och ändrar
   noll av de 35 tidigare produkternas pris-, policy- eller kostnadsdata, bortsett från
   tillåten global generator-/katalogproveniens. Umeåposten ska bära den verkliga
   treårsperioden, B-bindningen och `annual/snapshot/complete`.
6. Uppdatera de spärrade implementationsproven till aktiverat läge: `godkanda(katalog)`
   ska vara 37, alla fyra ID:n ska ingå, den nakna Umeågrinden utan registrerad policy
   ska fortfarande blockera och okända issue-/justeringstyper ska fortsatt falla stängt.
7. Lägg permanenta **omockade** skarpa produkt-/UI-/E2E-prov. Dropdownen ska innehålla
   alla fyra. Kör minst ett Jämtkraftfall och Umeå hela vägen till synlig uppskattad
   årskostnad. Umeå ska visa och kräva effekt, period, band, oktober–aprilflöde och B;
   Jämtkraft ska visa och kräva effekt, band och oktober–aprilflöde utan periodfält.
   Verifiera även produktbyte utan återanvändning och blockerade kronor-/schablon-/
   besparingsvägar via den skarpa produktentryn.
8. Kör riktade Batch 4-prov, full Python, full TypeScript, `tsc`, isolerat bygge, E2E,
   generatorsynk, exakt dispositions-/produkträkning, semantisk före/efter-diff och
   `git diff --check` i samtliga repon.
9. Commitera fokuserat lokalt per repo, logga exakta commit-hashar och verifieringsutfall
   i sessionen och stanna för Codex granskning av aktiveringsdiffen.

**Lokal aktivering är tillåten. Push är inte tillåten.**
