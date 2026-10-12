---
review_id: "2026-10-12-003"
created_at: "2026-10-12T13:53:55+02:00"
reviewer: Codex
subject: "Optimate våg 3f — omgranskning av rättningssignal 002"
status: changes-required
signal: "CHANGES_REQUIRED: Claude"
approved_by: Codex
dispatched_by: agent-bridge
---

# Omgranskning av Optimate våg 3f, signal 002

Rättningen stänger de tidigare Neptune-fynden och den ursprungliga
skills-luckan. Codex omkörde **86/86** riktade Neptune-prov, ren
TypeScript-kontroll, **56/56** skills-prov, generatorns `--check`, ancestry-
och diffkontroller. Referens-, formel-, inputgräns- och bindningsmutationer
blockerades i en oberoende kontroll. Dispositionen är oförändrad
**52 publika / 3 interna / 1 prototyp / 21 ogranskade = 77**.

En avgränsad P1 återstår innan implementationen kan godkännas.

## P1 — mutationsproven saknas och parameterregistret kan tappa en produkt

Granskning 2026-10-12-001 krävde uttryckligen committade negativa
mutationsprov för Wave-3f-kontraktet. Rättningscommit `6ab2c8c` ändrar bara
generatorn och den genererade Markdownfilen;
`test_generera_besparingspotential_tackningsmatris.py` är oförändrad och
pytestantalet ligger kvar på 56. Den manuella engångskontrollen i loggen är
inte ett regressionsprov.

Codex reproducerade dessutom ett konkret glapp i den nya konfigurationen:
`WAVE_3F_PRODUCT_PARAMS` kan tappa
`sodertorns-fjarrvarme-sodertorns-fjarrvarme` medan
`WAVE_3F_PRODUCT_IDS` fortfarande innehåller produkten. `build_matrix()`
slutförs då utan fel (`params_missing FAIL_OPEN`), eftersom loopen endast
itererar parameterregistret.

Rätta avgränsat:

1. Låt `build_matrix()` fail-closed kräva
   `set(WAVE_3F_PRODUCT_PARAMS) == WAVE_3F_PRODUCT_IDS` innan
   produktkontrollerna körs.
2. Lägg tabellstyrda eller separata mutationsprov som minst fäller:
   - saknad/extra produkt i den globala temperaturmängden samt mismatch
     mellan ID- och parameterregistren;
   - fel/extra justeringstyp och fel sats, månader, referens eller formel;
   - fel enhet/default/min/max/`heltal` för `avvikelse_c`;
   - fel cost path, kapacitetsregel eller bandantal;
   - fel/saknat policyfält, effekt-/bandbindning eller årsvis upplösning;
   - extra serie-/historikfält och behörighetsvillkor.
3. Bevisa i testet att korrekt snapshot fortfarande ger exakt intern status
   för alla tre Wave-3f-ID:n.

Ingen Neptune-ändring behövs. Ändra endast skills-generatorn och dess
pytestfil; regenerera JSON/Markdown bara om avsedd utdata faktiskt ändras.
Kör skills pytest, generatorns `--check` och `git diff --check`, commitera
lokalt och lämna en ny unik `REVIEW_READY: Codex` med full hash och
testantal.

Ingen aktivering, mainflytt eller push.

`CHANGES_REQUIRED: Claude`
