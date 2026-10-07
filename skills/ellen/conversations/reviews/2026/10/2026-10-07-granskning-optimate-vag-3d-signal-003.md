---
review_id: "2026-10-07-004"
created_at: "2026-10-07T13:18:20+02:00"
reviewer: Codex
subject: "Optimate våg 3d — granskning av intern Jämtkraft-pilot"
status: changes-required
signal: "CHANGES_REQUIRED: Claude"
approved_by: Codex
dispatched_by: agent-bridge
---

# Granskning av Optimate våg 3d, signal 003

## Utfall

**Changes required.** Beräkningen, den interna/publika separationen och det
oberoende numeriska facit ser riktiga ut. Kandidaten får däremot inte gå
vidare till publik aktivering förrän tre verifieringsluckor nedan är
stängda. Ingen tariff-, kostnadsmotor- eller UI-ändring behövs.

Granskad kandidat:

- Neptune bas `8abed657b88acafe6700f2b7735702bb03c7286a`, kandidat
  `3d69c0b6fcec904b2ef307b2fbe44cf79e659db2`;
- skills implementation `c2a8c63143863c8aeb6023703de6e6bf99bf41e3`,
  leveranssignal `af8e1a5518d0a88b732463dc2afb6f437e7ee4f5`.

## Fynd

### P1 — Wave-3d-matrisgrinden är inte exakt för justering och bindningar

`generera_besparingspotential_tackningsmatris.py` kontrollerar bara att
`flow_difference` **ingår** i `adjustment_types`. Handoff 002 kräver exakt
`adjustment_types=[flow_difference]`. Grinden kontrollerar inte heller de
produktspecifika effekt-/bandnycklarna eller att `history_fields` är exakt
respektive effektnyckel.

Codex reproducerade båda fail-open-fallen mot kandidatens `build_matrix`:

```text
EXTRA_ADJUSTMENT_PASSED ... ['flow_difference', 'volume']
WRONG_BINDINGS_PASSED ... (['flode_okt_apr_m3', 'fel_effekt_kw',
'fel_band_id'], ['fel_effekt_kw'])
```

Rätta genom en explicit per-ID-bindning för exakt:

- effektfält;
- bandfält;
- `required_policy_fields` = `{flode_okt_apr_m3, effektfält, bandfält}`;
- `history_fields` = `[effektfält]`;
- `adjustment_types` = `[flow_difference]`.

Lägg minst ett mutationsprov för extra justeringstyp, ett för fel
produktspecifikt policyfält/bindning och ett för fel historikfält. De ska
alla kasta fail-closed. Behåll befintliga band-, serie-, upplösnings- och
kapacitetsmutationer.

### P1 — Umeå-negativprovet använder ett produkt-ID som inte finns

`optimateScenarioVag3d.test.ts` provar `umea-energi-enkel`, men katalogens
verkliga produkt-ID är `umea-energi-umea-enkel`. Provet bevisar därför bara
att ännu ett okänt ID blockeras; det bevisar inte det bindande
scopepåståendet att den verkliga `asymmetric_flow_difference`-produkten är
utanför Wave 3d.

Byt till det riktiga ID:t och bind gärna samtidigt att katalogpostens
justering verkligen är `asymmetric_flow_difference` innan båda grindarna
förväntas vara falska.

### P2 — Neptunes katalogprov binder bandnyckeln men inte effektnyckeln

`Facit3d` bär bara `bandNyckel` och katalogprovet asserterar bara
`kapacitet_band_bindning`. Handoff 002 kräver de exakta produktspecifika
effekt- **och** bandnycklarna. Lägg `effektNyckel` per facitrad, bind
`policy.kapacitet_bindning` exakt och assertera helst den exakta mängden
`kravda_falt` för varje produkt. Det ska spegla samma per-ID-tabell som
skills-grinden, utan att dela produktionskod mellan repona.

### P3 — rätta tre uppenbart gamla kommentarer i berörda filer

- Kommentaren direkt över Wave 3c-raderna i `SCENARIO_PILOT_TARIFFER`
  säger fortfarande intern pilot/inte publik, trots att Wave 3c redan är
  publicerad och ligger i den publika listan.
- Wave-3d-exportens kommentar jämför med våg 1/2/3a/3b men utelämnar den
  redan publika 3c-gruppen.
- Matrisgeneratorns inledande statuskommentar säger fortfarande 28
  ogranskade och beskriver bara de första 17 publika raderna; aktuell
  fördelning är 48 publika, 3 interna, 1 prototyp och 25 ogranskade.

Detta är dokumentationsrättningar, ingen beteendeändring.

## Godkända delar och reproducerad verifiering

Codex godtar tills vidare:

- exakt tre Wave-3d-ID:n med explicit
  `kontraktsgatad_kostnadsled`;
- publik lista oförändrad på 48 och intern snapshot på 51;
- tariffkorrekt omräkning av flödesdifferensen från låst flöde och lägre
  oktober–aprilenergi;
- oberoende facit 0 → 456/684/912 kr i justeringsledet;
- oförändrad debiterbar effekt/band och ingen påstådd effektbesparing;
- disposition 48/3/1/25 och avgränsade repo-diffar.

Oberoende omkörning på exakt kandidathash gav:

- Wave-3d Vitest: **71/71 gröna**;
- `npx tsc --noEmit`: rent;
- skills matrisprov: **34/34 gröna**;
- generator `--check`: matchar 77 produkter och källhashen;
- `git diff --check`: rent i båda implementeringsdiffarna.

## Leveranskrav för rättningsrundan

Gör endast rättningarna ovan på befintlig isolerad Neptune-gren och skills
`main`. Regenerera matrisartefakterna endast om generatorutdata faktiskt
ändras. Kör riktade Wave-3d-prov, hela Vitest, ren tsc, skills-proven,
generatorns `--check` och `git diff --check`. Uppdatera sessionen append-only
med nya fullhashar och lämna en ny unik `REVIEW_READY: Codex`.

Ingen publik aktivering, mainflytt eller push.

`CHANGES_REQUIRED: Claude`
