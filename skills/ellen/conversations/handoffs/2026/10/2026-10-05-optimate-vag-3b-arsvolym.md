---
handoff_id: "2026-10-05-001"
created_at: "2026-10-05T12:27:09+02:00"
from: Robert/Codex
to: Claude
status: "APPROVED_FOR_IMPLEMENTATION: Claude"
approved_by:
  - Robert
  - Codex
dispatched_by: agent-bridge
skills_base: "abf4dba3159143f813827907d898f24217d0e0ba"
neptune_base: "4d6e3398b85079891585304085df022c5adf8536"
---

# APPROVED_FOR_IMPLEMENTATION: Claude — Optimate våg 3b, årsvis volymled

## Beslut

Robert godkände 2026-10-05 Codex urval av en sammanhållen nästa våg. Bygg
en **intern**, ännu inte publik 10/15/20-pilot för exakt följande sex
produkt-ID:n:

1. `borlange-energi-borlange`
2. `falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo`
3. `falu-energi-vatten-falun`
4. `habo-energi-habo`
5. `mjolby-svartadalen-energi-mjolby`
6. `vanerenergi-mariestad-och-toreboda`

Detta är hela och enda `WAVE_3B_PRODUCT_IDS`-scopet. Alla sex har
`cost_path=kontrakt_arskostnad`, `capacity_rule=effekt`, en årsvis
`volume`-justering med skalärt `flode_m3` och inga månadsseriefält. Mölndal,
Jönköping, månadsserieprodukterna och alla övriga rader är uttryckligen
utanför denna våg.

## Bindande beräkningskontrakt

- Återanvänd den befintliga scenariomotorn och välj explicit backend
  `kontraktsgatad_kostnadsled` för vart och ett av de sex ID:na. Ingen ny
  backend och ingen fallback/härledning från metadata.
- Endast `manadsEnergiMwh` och `totalMwh` får skilja mellan referens och
  efterfall, genom 10/15/20 procent lägre **styrbar rumsvärme**.
- `flode_m3`, debiterbar effekt, valt band, kapacitetshistorik och samtliga
  övriga policyfält ska vara bit-identiska med referensen. Scenariot får
  alltså inte tillskriva Optimate en odokumenterad flödes-, avkylnings-
  eller omedelbar effektbesparing.
- Volymjusteringens kostnadsled ska därför vara oförändrat mellan referens
  och samtliga tre efterfall. Bara de prisled som faktiskt beror på den
  ändrade energiserien får bidra till `kostnadsskillnadKr`.
- Befintlig preliminär status, proveniens, rumsvärmevalidering och
  fail-closed-beteende ska bevaras.

## Implementation bakom spärr

1. Utgå från en ren, isolerad Neptune-worktree vid exakt
   `4d6e3398b85079891585304085df022c5adf8536`. Kontrollera först att live
   Neptune `main`/`origin/main` fortfarande matchar; stoppa vid avvikelse.
2. Inför en exporterad, fryst `WAVE_3B_PRODUCT_IDS` som innehåller exakt de
   sex ID:na ovan och lägg samma ID:n explicit i den interna
   `SCENARIO_PILOT_TARIFFER` med `kontraktsgatad_kostnadsled`.
3. Ändra **inte** `SCENARIO_PUBLIKT_AKTIVERADE_ID`: den ska fortfarande
   innehålla exakt 34 produkter (våg 1 + våg 2 + våg 3a). Alla sex nya ska
   ge intern support men fortsatt nekas av den publika grinden.
4. Uppdatera skills-matrisens källregister för exakt dessa sex från
   `not_reviewed` till `godkand_intern_pilot_ej_publik`; regenerera JSON och
   Markdown enbart via generatorn. Målfördelning:
   **34 publika / 6 interna / 1 särskild prototyp / 36 ej granskade = 77**.
5. Ändra inte tariffkatalog, prisvärden, kostnadsmotor,
   `stodjer_besparing`, `stodjer_aktuell_arskostnad`, Enkey eller
   conversations/automation.

## Acceptanskriterier

- Maskinell mängdlikhet: `WAVE_3B_PRODUCT_IDS` är exakt de sex beslutade
  katalograderna, inga fler, är fryst och saknar dubbletter.
- Varje ID använder explicit `kontraktsgatad_kostnadsled`; okänt eller
  oregistrerat ID förblir fail-closed.
- Tabellstyrda, oberoende facit täcker samtliga sex produkter. Förväntade
  belopp ska härledas från dokumenterade prisformler och fixtures — inte
  skapas genom att anropa samma produktionsfunktion som testas.
- För varje produkt verifieras minst referenskostnad, 10/15/20-resultat,
  sparad styrbar MWh, preliminär status och att volymjusteringsledet samt
  alla låsta indata är oförändrade.
- Negativa prov visar att de sex inte är publikt aktiverade och att minst
  en närliggande produkt utanför scopet inte råkar inkluderas.
- Befintliga våg 1, 2 och 3a samt Stockholms särskilda prototyp är
  regressionsgröna och deras mängder/status ändras inte.
- Kör riktade prov, hela Vitest, `tsc --noEmit`, produktionsbygge,
  relevanta Python-matrisprov, generatorns `--check` och
  `git diff --check`. Återställ genererade `dist/`-artefakter som inte ska
  ingå.

## Leverans och stoppvillkor

Committera implementationen i den isolerade Neptune-grenen och de
avgränsade matris-/conversations-filerna i skills. Skriv därefter en ny,
unik toppsignal `REVIEW_READY: Codex` med fullständiga commit-hashar,
exakta testtal och diffscope.

Ingen publik aktivering, mainflytt eller push ingår. Stoppa med
`BLOCKED: Codex` om någon av de sex saknar fungerande kontraktskostnadsväg,
om volymledet inte kan hållas oförändrat utan ny tariff-/motorlogik, om
bas-HEAD har flyttats eller om implementationen kräver större scope.
