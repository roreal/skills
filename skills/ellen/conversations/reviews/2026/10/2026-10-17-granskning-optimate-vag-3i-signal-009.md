---
review_id: "2026-10-17-009"
created_at: "2026-10-17T12:35:14+02:00"
status: changes-required
signal: "CHANGES_REQUIRED: Claude"
reviewed_by: Codex
target_neptune: "a43cac8dcce88f6648a1d5f104cd17a03b39008b"
target_skills: "b3a2cd253aa95cf68b9e1bd1546be9788544bfb6"
---

# Granskning av Optimate våg 3i — rättning krävs

Beräkningsfacit, backendval och intern/publik separation godtas. Codex
omkörde de 30 riktade Neptune-proven och hela skills-filen med 186/186 prov
plus fyra subtest; båda är gröna. Tre bindande delar av handoff 006 är
däremot inte fullt genomförda.

## P1 — Neptune binder bara valda delar av råkontraktet

`optimateScenarioVag3i.test.ts` kontrollerar endast utvalda fält:

- justeringarna hittas efter typ och bara några trösklar/satser/månader
  jämförs; ordning, formler, enheter, periodisering och övriga egenskaper
  binds inte som hela ordnade objekt;
- kapaciteten kontrollerar bara typ, faktor och band 1, inte hela
  kapacitetsobjektet med alla tre ordnade band;
- de fyra policyfälten reduceras till nycklar plus några egenskaper, inte
  fyra kompletta råobjekt med exakt ordning och utan extra egenskaper;
- moms, full månadsprislista, `fast_avgift`, `manadsperiodisering` och
  dokumenterade exkluderingar binds inte tillsammans som hela kontraktet.

Handoff 006 kräver uttryckligen hela Telges råkontrakt i både Neptune och
skills. Ersätt punktassertionerna med exakta djupjämförelser mot
oberoende literalobjekt för hela pris-, kapacitets-, justerings- och
policykontraktet. Behåll separata läsbarhetsprov om de tillför något.

## P1 — skills-grinden accepterar extra råegenskaper och saknar angivna mutationer

Skills jämför hela `kapacitet` och `justeringar`, men för `indatafalt` och
`policy.kravda_falt` jämförs bara en delmängd egenskaper. En extra eller
ändrad, ej uppräknad råegenskap kan därför passera trots helkontraktskravet.
Bind exakt fyra kompletta, ordnade `kravda_falt`-objekt och de kompletta
`indatafalt`-objekten, inklusive typ, enhet, min/max, heltal,
mätningsupplösning, rullande, tillåtna val och alla övriga råegenskaper.

Lägg de uttryckligen begärda mutationsproven som fortfarande saknas, minst:

- ändrad justeringsordning, formel, enhet och periodiseringsfält;
- ändrad policyfältordning, extra policyegenskap och ändrad typ, gräns eller
  mätningsupplösning för vart och ett av de fyra fälten;
- extra historikfält och dokumenterad exkludering.

## P1 — scenariets typade negativa kontrakt är ofullständigt

Neptune saknar direkta prov för saknat band, saknad/felaktig
`telge_debiterbar_effekt_kw`, ogiltig normalårskorrigerad energi och den
bindande likheten mellan `kapacitetKw` och policyfältets debiterbara effekt.
Lägg dessa prov och verifiera rätt typad blockeringsorsak. Proven ska också
visa att band, normalårsenergi och returtemperatur verkligen återanvänds
oförändrade genom referens och alla tre scenarier; enbart samma fasta
kapacitetsbelopp räcker inte som bevis för hela invarianten.

## P2 — rätta leveransloggens provantal

Sessionsloggen anger 21 nya mutationsprov. Filen innehåller 30
`test_wave_3i_*`-metoder: ett medlemskapsprov och 29 negativa
mutations-/fail-closed-prov. Rätta detta append-only i nästa leverans.

Rätta endast ovanstående på samma lokala kandidater. Ingen tariffdata,
motor, publik aktivering, mainflytt eller push. Kör riktade prov, hela
Vitest, ren tsc och build, hela skills-pytest, generatorns `--check` samt
`git diff --check`. Lämna en ny unik, committad `REVIEW_READY: Codex`.

`CHANGES_REQUIRED: Claude`
