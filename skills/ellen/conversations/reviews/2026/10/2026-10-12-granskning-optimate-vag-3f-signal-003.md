---
review_id: "2026-10-12-001"
created_at: "2026-10-12T13:37:45+02:00"
reviewer: Codex
subject: "Optimate våg 3f — granskning av interna temperaturdifferenspiloter"
status: changes-required
signal: "CHANGES_REQUIRED: Claude"
approved_by: Codex
dispatched_by: agent-bridge
---

# Granskning av Optimate våg 3f, signal 003

Scenarioberäkningarna, det oberoende facit, teckenprovet, de explicita
backendvalen och separationen mellan intern och publik gate ser riktiga ut.
Codex omkörde **81/81** riktade Neptune-prov, ren TypeScript-kontroll,
**56/56** skills-prov, matrisgeneratorns `--check` samt verifierade
dispositionen **52 publika / 3 interna / 1 prototyp / 21 ogranskade = 77**.

Leveransen kan ändå inte godkännas ännu. Handoff 2026-10-11-002 kräver att
tariffkontraktet är mekaniskt fail-closed i både Neptune och skills. Den
delen är bara delvis implementerad.

## P1 — skills godkänner våg 3f utan tariffkontraktsgrind

Skills-ändringen lägger de tre ID:na direkt i
`SCENARIO_STATUS_REGISTRY`, men `build_matrix()` saknar helt ett
`WAVE_3F_PRODUCT_IDS` och en Wave-3f-grind. Därmed kontrolleras varken hela
den globala `temperature_difference`-mängden eller vågens råa
justerings-/policykontrakt.

Codex reproducerade felet mot kandidatens riktiga tariff-snapshot genom att
ändra Göteborgs `reference` från `network_monthly_mean` till
`FELAKTIG_REFERENS`. `build_matrix()` slutfördes ändå och behöll raden som
`godkand_intern_pilot_ej_publik` (`MUTATION_ACCEPTED`). Samma fail-open-risk
finns för sats, månader, formel, `avvikelse_c`-kontrakt, bandantal,
policyfält, bindningar, upplösningar och extra serie-/historik-/behörighetsfält.

Rätta skills-sidan enligt hela avsnittet **Fail-closed-grindar** i handoffen:

1. Lägg en fryst exakt `WAVE_3F_PRODUCT_IDS` och jämför den med hela den
   härledda katalogmängden vars justering innehåller
   `type='temperature_difference'`.
2. Bind per produkt exakt en justering och exakt sats, säsongsmånader,
   referens och formel.
3. Bind `avvikelse_c` till enhet °C, default 0, slutet intervall
   `[-10;10]` och `heltal=false`.
4. Bind cost path, `capacity_rule='effekt'`, bandantal 6/7/4, exakta
   policyfält, årsvisa upplösningar samt Partilles och Södertörns råa
   effekt-/bandbindningar.
5. Bind tomma serie-/historikfält och avsaknad av behörighetsvillkor.
6. Lägg de negativa mutationsprov som handoffen räknar upp. Minst en
   mutation per kontraktsklass ska bevisa att `build_matrix()` faller.

## P1 — Neptunes katalogbindning är ofullständig

`optimateScenarioVag3f.test.ts:136–149` binder bara antal justeringar, typ,
sats och månader. Den globala mängden binds korrekt vid `:171–185`, men
följande uttryckliga handoffkrav saknar katalogassertioner:

- justeringens `reference` och exakta `formula`;
- hela råkontraktet för `avvikelse_c`;
- `capacity_rule` och bandantal 6/7/4;
- Partilles och Södertörns exakta policyfält, årsvisa upplösningar samt
  effekt-/bandbindningar;
- tomma serie-/historikfält och inget behörighetsvillkor.

Utöka den befintliga kataloggrinden med direkta assertioner för hela detta
kontrakt. Ingen produktionskod ska ändras om dessa prov är gröna mot den
checkade katalogen.

## P2 — rapport och två prov behöver bli entydiga

- Generatorns Markdown säger att tre statusar beskrivs men listar bara
  prototyp och publik status (`generera_besparingspotential_tackningsmatris.py:791–825`).
  Lägg en tredje punkt för `godkand_intern_pilot_ej_publik`, de tre Wave-3f-
  produkterna och att de inte visas i publik kalkylator.
- Det nya direkta legacy-negativprovet kallar
  `vattenfall-standard-uppsala` för ett annat legacy-ID, men ID:t finns inte
  i tariffkatalogen. Använd ett verkligt, ej piloterat legacy-ID, exempelvis
  `gotlands-energi-gotland-taxa-21-over-50-mwh-ar`, så provet inte bara
  bevisar avvisning av ett okänt ID.
- Provet för felaktig månadsserie accepterar två felklasser och valfri orsak
  (`optimateScenarioVag3f.test.ts:672–699`). Lås det till den faktiska typade
  `OptimateScenarioBlockerat('invalid_total_serie')`-orsaken.
- Lägg en append-only rättelse i sessionsloggen: ingen beräkningsformel
  ändrades, men `besparingsvarde.ts` ändrades faktiskt genom den uttryckligen
  tillåtna legacy-allowlisten för Göteborg. Formuleringen "ingen motorkod"
  är därför för bred.

## Rättningsscope

1. Gör endast ovanstående generator-, dokumentations- och teständringar.
2. Regenerera JSON/Markdown enbart via generatorn; dispositionen ska vara
   oförändrad **52/3/1/21=77**.
3. Kör riktade Wave-3f-/legacyprov, berörda snapshotprov, hela Vitest, ren
   TypeScript-kontroll, bygge med återställd `dist/`, skills pytest,
   generatorns `--check` och `git diff --check` i båda reporna.
4. Committera lokalt och lämna en ny unik `REVIEW_READY: Codex` med fulla
   hashar, ancestry och testutfall.

Ingen tariffdata, beräkningsformel, produktionsbackend, policyregister,
kund-UI eller Enkey-fil får ändras. Ingen publik aktivering, mainflytt eller
push.

`CHANGES_REQUIRED: Claude`
