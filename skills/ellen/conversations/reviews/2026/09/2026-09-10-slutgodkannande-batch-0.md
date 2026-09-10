---
review_id: "2026-09-10-008"
date: "2026-09-10"
reviewer: Codex
status: approved
scope:
  - "Batch 0-grundkontrakt och samtliga rättningsrundor mot godkännande 2026-09-09-016"
  - "Sluträttning efter omgranskning 2026-09-10-007"
reviewed_heads:
  skills: "0b7e8b3e5e7e148b505905e7d37aa76f2c77627d"
  enkey-agents: "45dd48a39ff9f01805847bfc4d3051d4a3a2581a"
  neptune_academy: "b03f4cc2ac09ccc9711d9dc6ee566ac1a526852f"
implementation_changed_by_reviewer: false
push_status: approved-for-push
tariff_activation_allowed: false
tariff_disposition: "7 implemented / 57 ready / 28 blocked av 92, oförändrad"
follows_review: "2026-09-10-007"
implements_approval: "2026-09-09-016"
---

# Slutgodkännande av Batch 0

## Beslut

**Batch 0 är godkänd för push vid de två exakta produkt-HEAD-versionerna ovan och den
granskade `skills`-basen.** Rättningsrunda 7 stänger det sista P1- och P2-fyndet i
`2026-09-10-007`: fysikgrinden gäller nu både policybunden och fri kallenergiserie, och
seriebindningens `annual`-kontroll sker före statusens tidiga `blocked`-retur.

Inga blockerande eller icke-blockerande nya kodfynd återstår inom Batch 0-scope. Detta
godkännande gäller infrastrukturen och dess testade produktintegration. Det aktiverar
ingen ny tariff och ändrar inte dispositionen 7 implementerade / 57 redo / 28 blockerade
av 92.

## Bekräftade kontrollpunkter

- `kallenergiArsserieBindning`/`kallenergi_arsserie_bindning` måste peka på ett
  `number_series`-krav som gäller `annual`.
- Scope-felet kastas före status även när annan obligatorisk årsindata saknas.
- Den bundna serien måste ha exakt tolv element i januari–december-ordning.
- Bunden och fri kallenergikälla är ömsesidigt uteslutande; ingen källa ignoreras tyst.
- `0 <= kallenergi[m] <= totalenergi[m]` gäller för varje använd månad, oavsett om serien
  kommer från policybindningen eller legacyargumentet.
- Negativ och överstor bunden serie ger `SeriebindningOgiltig`; produktentryn klassar om
  detta till fältnära `KontraktBlockerat('invalid_policy_fields')` med rätt nyckel och
  orsak.
- Negativ och överstor fri legacyserie stoppas med tydlig parameteridentitet före
  kostnadsmotorn; en giltig fri serie fungerar fortsatt utan policybindning.
- Kalenderordningen verifieras med distinkta serie-/prisvärden och ett oberoende facit i
  både Python och TypeScript.
- Batch 0:s UI-metadata, värdetyper, attestering, bandval, produktförmågor och fältnära
  valideringsfel är fortsatt regressionsgröna.

## Utförda kontroller

- `.venv/bin/python -m pytest tools/tariffer/tests -q`: **401 passed**; endast
  sandboxrelaterad pytestcache-varning.
- `npm test -- --run`: **17 testfiler, 486 tester passerade**.
- `npx tsc --noEmit`: godkänd.
- `npm run test:e2e`: godkänd; produktionbygget och båda kalkylatorscenarierna passerade.
  Endast den befintliga varningen om stor bundle visades.
- Oberoende direktanrop i Python och TypeScript bekräftade att det tidigare fallet
  150 MWh fri kall energi mot 100 MWh total energi nu kastar före kostnad.
- Oberoende direktanrop bekräftade att ett negativt fritt värde stoppas i båda språk.
- Oberoende direktanrop bekräftade att en `monthly`-märkt seriebindning kastar även när
  annan årsindata saknas.
- `git diff --check` är rent för båda slutcommitterna.
- `enkey-agents` och `neptune_academy` är rena efter test; bygggenererade `dist`-ändringar
  återställdes.

## Godkännandets gräns

Godkännandet omfattar de kumulativa lokala Batch 0-kedjorna vid:

- `skills@0b7e8b3e5e7e148b505905e7d37aa76f2c77627d`;
- `enkey-agents@45dd48a39ff9f01805847bfc4d3051d4a3a2581a`;
- `neptune_academy@b03f4cc2ac09ccc9711d9dc6ee566ac1a526852f`.

Codex slutgodkännande och de mekaniska statusuppdateringarna i `conversations` skapades
efter `skills@0b7e8b3`. Claude får därför göra **en enda dokumentationscommit** ovanpå
denna skills-bas som endast tar med granskningsfilen `2026-09-10-008` samt tillhörande
uppdateringar av session, handoff och index. Den orelaterade ospårade förslagsfilen ska
inte tas med. Den loggcommitten behöver ingen ny kodgranskning; produkt-HEAD-versionerna
får däremot inte ändras utan ny granskning.

Det innebär inte att de 57 `ready_to_implement`-tarifferna är aktiverade eller
produktionsgodkända. Varje kommande implementationsbatch måste fortfarande få sina
tariffdata, formler, obligatoriska indata, produktförmågor och tester granskade före
aktivering. Den orelaterade ospårade förslagsfilen i `skills` ingår inte i detta
godkännande.

## Push och nästa etapp

Robert kan nu be Claude skapa den avgränsade slutloggcommitten och därefter pusha.
Rekommenderad ordning är `skills` → `enkey-agents` → `neptune_academy`. Efter push ska
produktreponas remote-HEAD matcha fullhasharna ovan och skills remote-HEAD matcha den nya
rena loggcommitten vars förälder är `0b7e8b3`.

Efter verifierad push kan nästa separat avgränsade tariffbatch startas enligt den
godkända V22-batchplanen. Ingen tariff ska aktiveras som en del av själva Batch 0-pushen.
Codex utförde ingen push och ändrade ingen produktkod eller tariffdata i granskningen.
