---
review_id: "2026-09-12-021"
date: "2026-09-12"
reviewer: Codex
status: approved-for-separate-local-activation
scope: "Batch 2 rättningsrunda 2 efter granskning 020"
reviewed_heads:
  skills: "2696359fa9f6ccfd51e978ca991a49352b0ce6a8"
  skills_catalog_commit: "08a8d6a795b0f6353b461ffda3056e1117f3819e"
  enkey_agents: "12c5c6d5ad0df9f08e0afccc6985871d6567378f"
  neptune_academy: "fbc925f27c87764943cd534aa778d22c206fbe67"
activation_allowed: true
push_allowed: false
tariff_disposition_before_activation: "15 implemented / 49 ready / 28 blocked av 92"
expected_after_activation: "16 implemented / 48 ready / 28 blocked av 92"
---

# Slutgranskning av Batch 2-implementationen

## Bedömning

Samtliga funktionella fynd i granskning 019 och 020 är stängda. Batch 2:s lokala
implementation av Sundsvall Energi Indal/Liden/Lucksta är godkänd för en **separat,
lokal aktiveringsfas**. Godkännandet gäller inte push.

## Verifierat av Codex

- Dubblerade katalogtariff-ID:n kastar innan index eller mängder byggs.
- Katalogens tariff-/medlems-ID:n, request-ID:n och scope-/requestreferenser
  typkontrolleras som icke-tomma strängar.
- `tariff_ids`, `member_ids` och ett närvarande `investigation.request_ids` måste vara
  riktiga listor; en bar sträng accepteras inte som itererbar referenslista.
- Okända, dubblerade och felomfattade referenser förblir fail-closed.
- Riktad Batch 2-svit: `30 passed`.
- Full tariffsvit: `730 passed, 4 skipped`.
- Rättningscommitten ändrar endast `tools/tariffer/katalog.py` och
  `tools/tariffer/tests/test_batch_2_sundsvall_indal.py`; diffkontrollen är ren.
- Ingen TypeScript-, katalogdata-, tariffmodell- eller aktiveringsändring gjordes i
  rättningsrunda 2. Tidigare verifierade `942 passed` och ren tsc gäller oförändrat.
- `godkanda(katalog)` ger fortsatt 15 och Sundsvall Indal/Liden/Lucksta ingår inte.

Leveransloggen sade först “sex nya negativa tester” och “24 tidigare + 6”, men diffen
och insamlingen visar **fyra** nya testfunktioner: 26 tidigare + 4 = 30. Sessionsloggen
är rättad i samband med detta godkännande. Det är ett redaktionellt fel, inte ett
funktionellt hinder för aktiveringsfasen.

## Godkänd lokal aktiveringsfas

Aktivera exakt katalogtariffen
`sundsvall-energi-indal-liden-och-lucksta-2026` för uppskattad årskostnad med
bekräftad MWh. Ingen annan tariff får byta status.

### Katalog och grind

1. Sätt endast målpostens `investigation` till `null`, enligt samma livscykel som
   tidigare aktiveringar. Behåll `capacity.type="not_applicable"`, priset 1 008
   SEK/MWh exklusive moms, `contract_required:true`, källor och övriga fält.
2. Höj katalogrevisionen och lägg en exakt ändringslogg som säger att aktiveringen
   gäller `annual_forward`, inte fakturagaranti, månadsredovisning, kronor,
   schablon eller besparing.
3. R14 ska fortsatt peka på exakt Sundsvall normal och Matfors/Kvissleby. Dessa två
   tariffer ska förbli blockerade och oförändrade.
4. Verifiera exakt 16 godkända katalogtariffer från 14 medlemmar. Total disposition
   ska bli 16/48/28; avslagsorsaken `utreds` ska minska med exakt ett.

### Generator, produkt och UI

5. Regenerera `tariffer.generated.ts` från den nya fokuserade katalogcommitten med
   korrekt SHA-256 och full commitproveniens. Den genererade summeringen ska ange
   16 godkända och 62 filtrerade katalogtariffer.
6. Den verkliga genererade posten ska använda katalogtariff-ID:t ovan. Kontrollera
   generatorns faktiska produkt-/leverantörs-ID; det förväntas vara
   `sundsvall-energi-indal-liden-och-lucksta` utan årsändelsen. Hårdkoda inte det
   antagandet utan att jämföra mot den genererade posten.
7. Lägg permanenta prov mot den verkliga genererade posten, inte en mock:
   - publik `beraknaArsprodukt` med 100 MWh ger status `annual/exact/complete`,
     126 000 kr inklusive moms och `kapacitetKw === undefined`;
   - fast-, kapacitets- och justeringsdel är noll i kontraktsfacit;
   - kronor och schablon blockeras typat med `unsupported_input_mode`;
   - besparingsvägen förblir blockerad med `besparing_ej_stodd`.
8. Lägg ett riktigt komponentprov mot den genererade posten: leverantören är valbar,
   inget kapacitets- eller policyfält visas, MWh kan skickas via formulärets normala
   submit och resultatet visar 126 000 kr. Lägg motsvarande scenario i den byggda
   sidans E2E-test.

### Verifiering och leverans

9. Uppdatera permanenta Pythonräknare/proveniensprov och Batch 2-testets
   preaktiveringstexter till verklig aktiveringsstatus. Bevara de syntetiska
   mekanismproven där de fortfarande ger eget värde.
10. Kör riktade aktiveringsprov, full `tools/tariffer/tests`, full TypeScript, tsc,
    isolerat bygge via `npm run eval:build` samt E2E mot det bygget. De redan befintliga,
    orelaterade ändringarna i `neptune-marketing/dist` får inte återställas, skrivas över
    eller tas med i commit.
11. Kör `git diff --check`, commitera fokuserat lokalt per repo, uppdatera sessionsloggen
    med exakta hashvärden/testantal och stanna för Codex granskning.

Ingen push. Batch 3 startar först efter att den lokala aktiveringen slutgranskats,
pushats normalt och samtliga tre remote-HEAD:ar verifierats.
