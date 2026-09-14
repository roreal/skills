---
review_id: "2026-09-14-001"
date: "2026-09-14"
reviewer: Codex
status: changes-required-before-push
scope: "Omgranskning av rättningsrunda 1 efter lokal Batch 3b-aktivering"
reviewed_heads:
  skills: "3f211a734ec654426ce76cf849c723c7c4f96280"
  enkey_agents: "f6f52ff83da7de420950cb79a5e370dd15bbe78f"
  neptune_academy: "50a47c3c0c7083d7d84d7993ca88c0384baf2011"
activation_may_remain: true
push_allowed: false
tariff_disposition: "33 implemented / 31 ready / 28 blocked av 92"
follows: "2026-09-13-040"
---

# Omgranskning av lokal Batch 3b-aktivering — rättningsrunda 1

## Beslut

**Alla funktionella och bindande P2-fynd i granskning 040 är stängda.** Det permanenta
Navirum-scenariot testar den skarpa Bas-/delvärmeprodukten, dropdownen innehåller exakt
åtta varianter, levande tariffdokument har rätt commit/fältkontrakt och de uttryckligen
namngivna P3-enhetstexterna är korrigerade. Aktiveringen är fortsatt korrekt
**33/31/28** och får ligga kvar.

En sista ren P3-dokumentationsrättning återstår före push. Två gemensamma Batch 3-
facittabeller innehåller både månads- och årspriser men beskriver hela tabellen med bara
den ena enheten. Två testsektionsrubriker säger dessutom fortfarande "bakom spärr".
Ingen produktionskod, tariffdata, motor, payload eller aritmetik ska ändras.

## P3 — blandade `rate_period` har fortfarande fel enhetstext och två rubriker är stale

`test_batch_3_flodeskorrigering.py:490` ändrades till "variabelpris kr/kW/månad".
Det stämmer för E.ON/Navirum-posterna, men samma tabell innehåller Kraftringen med
`1232.0` och `rate_period="year"`; för den raden är värdet kr/kW/år.

Omvänt säger `resultatkontrakt.batch3.test.ts:24-25` fortfarande "kr/kW/år" om sin
blandade tabell, trots att E.ON-posten `108.17` har `ratePeriod: "month"`. Båda
tabellerna räknar korrekt med den intilliggande periodmarkören; endast kommentarerna är
fel.

Samtidigt heter sektionerna vid `test_batch_3_flodeskorrigering.py:486-488`
"Verkliga katalograder bakom spärr" och vid
`test_batch_3b_bas_delvarme.py:576-578` "implementation bakom spärr, oförändrad
disposition", trots att båda nu testar den aktiverade katalogen.

### Krävd rättning

- Beskriv båda blandade facittabellernas fält som exempelvis
  `variabelpris kr/kW per deklarerad rate_period (month/year)`; kalla inte hela tabellen
  vare sig månads- eller årsprissatt.
- Byt de två sektionsrubrikerna till sann aktiv-katalogsemantik.
- Ändra inga tal, `rate_period`, multiplikatorer eller testassertioner.
- Logga rättningen och stanna för en snabb slutkontroll. **Ingen push.**

## Verifierat av Codex

- Scenario 15 täcker Navirum Fullvärme/Bas-/delvärme, exakt åtta variantval, fyra
  policyfält plus fakturamånad och lyckad MWh-submit.
- Full Python-svit: **1230 passed, 4 skipped**.
- Full TypeScript-svit: **1177 passed i 39 filer**; `npx tsc --noEmit` godkänt.
- Isolerat bygge från aktiveringskontrollen är fortsatt giltigt; rättningsrundan ändrar
  endast test-/E2E-/Markdownfiler. E2E: **15/15** godkända.
- Katalog/payload och disposition är oförändrade **33/31/28**.
- `git diff --check` är rent i alla tre rättningsintervall; inget repo är pushat.

## Nästa steg för Claude

Gör en minimal P3-rättning av exakt de fyra kommentar-/rubrikställena ovan, kör riktade
tester plus `git diff --check`, commitera fokuserat lokalt per berört repo, logga exakta
hashar och stanna för Codex snabbkontroll.

**Ingen push.**
