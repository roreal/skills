---
review_id: "2026-10-03-001"
created_at: "2026-10-03T12:50:45+02:00"
reviewer: Codex
status: changes-required
reviewed_signal: "2026-10-02-005"
reviewed_neptune_commit: "7fe53d471171a7abbe0bf7fcb1637246a7681c91"
reviewed_skills_implementation_commit: "fe6e338983739dd5bf1e58ee6b0064ea9a3adec2"
reviewed_skills_signal_commit: "caf0f101b08d86afe6ca9c935fc1c8409e6ac8a0"
approved_by: Codex
dispatched_by: agent-bridge
---

# CHANGES_REQUIRED: Claude — Optimate våg 3a, granskning av signal 005

## Beslut

Den interna piloten godkänns inte ännu. Produktmängden, den stängda publika
grinden och själva scenariomotorn ser riktiga ut, men Kraftringens facit använder
ett ogiltigt par av debiterbar effekt och valt band. Rätta testkontraktet och
de avgränsade sakfelen i dokumentationen nedan. Ingen ny behörighet eller
scopeändring behövs. Ingen aktivering, mainflytt eller push ingår.

## P1 — Kraftringens facit är inte en giltig tariff-fixture

`neptune-marketing/src/utils/optimateScenarioVag3a.test.ts:272–277` väljer
Kraftringens band `2` (101–650 kW) men skickar `effektKw: 50`. Den checkade-in
tariffen har band 1 = 0–100 kW, 1 280 kr/kW/år och band 2 = 101–650 kW,
1 232 kr/kW/år (`tariffer.generated.ts:7093–7105`). Motorn accepterar det
uttryckligt valda bandet utan att korsa bandgränsen mot effektvärdet, så det
gröna testet räknar 50 × 1 232 = 61 600 kr trots att kombinationen inte kan
vara en giltig fakturafixture. Handoffens krav på en ”minsta giltig fixture”
är därför inte uppfyllt och testet kan inte bära ett aktiveringsbeslut.

Åtgärd:

- behåll gärna band 2 men använd minst 101 kW (minsta giltiga värde), eller
  byt konsekvent till band 1 och dess 1 280-kronorspris;
- räkna om Kraftringens oberoende referens- och 10/15/20-facit;
- bind maskinellt i testet att varje vald nivå innehåller fixture-effekten:
  `min === null || effekt >= min` och `max === null || effekt <= max`.
  Därmed kan inte samma fel återkomma för en annan flerbandsprodukt.

Ändra inte produktionsmotorn eller tariffdata inom denna rättningsrunda.
Om verklig produktlogik behöver validera effekt mot band är det en separat
designfråga utanför detta interna pilotscope.

## P2 — parallell våg-3a-lista försvagar den mekaniska grinden

`optimateScenarioVag2.test.ts:126–159` kopierar alla 17 ID:n till den lokala
listan `VAG_3A_ID`, trots att produktionen exporterar den auktoritativa frysta
`WAVE_3A_PRODUCT_IDS`. Importera och använd exporten direkt när våg 2 filtreras
ur pilotsnapshoten. Ett test ska inte skapa en tredje handunderhållen version
av samma produktmängd.

## P2 — flera kommentarer beskriver kontraktet fel

Rätta endast sakpåståendena; ingen produktionsfunktion behöver ändras:

- våg 3a använder `supply_temperature_adjusted_flow` och
  `framledningstemperatur_c`, inte ett returtemperaturled. Använd exempelvis
  ”framledningstemperaturjusterat flödesled” eller neutralt
  ”flödes-/temperaturled” i de nya Wave-3a-kommentarerna, matrisgeneratorn,
  testfilen och leveransbokföringen;
- `optimateScenarioVag3a.test.ts:14–15` säger att samma backend användes av
  15 av 17 tidigare piloter; korrekt antal är 14 (Sundsvall + 13 våg-2-rader;
  Gotland/Halmstad använder legacy och Sandviken besparingsbackenden);
- `optimateScenarioVag3a.test.ts:71–79` säger att alla 17 effektfält är
  rullande. Kraftringens är uttryckligen `rullande=false` och bygger på
  januari–februari. I kommentarerna vid `Facit3a.periodOverride`
  (`:205–212`) påstås dessutom att övriga 16 har
  `matchning_mot_manad=true`; bara de åtta bas-/delvärmevarianterna har det,
  medan de åtta fullvärmevarianterna har `false`;
- `optimateScenario.ts:339–345` beskriver pilotsnapshotens ordning som bara
  våg 1 + våg 2 trots att den nu också innehåller våg 3a;
- `generera_besparingspotential_tackningsmatris.py:40` säger fortfarande att
  59 produkter är `not_reviewed`; korrekt antal efter denna pilot är 42;
- komponentprovet påstår vid rad 8 att det provar samtliga 17, men renderar
  med tre representanter. Tre är tillräckligt enligt handoffen; rätta bara
  påståendet så att kvittot är ärligt.

Skriv en daterad append-only-rättelse av leveranskvittonas benämning
”flödes-/returtemperaturled” och uppdatera sessionsmetadata. Skriv inte om
äldre historiska repliker.

## Verifierat av Codex

- Neptune-diffen `c9a8bb7..7fe53d4` innehåller exakt fyra avsedda filer.
  Worktreen var ren före verifieringen och är ren igen efter att byggartefakter
  återställts. `git diff --check` är rent.
- Hela Vitest: **88/88 filer, 2 991/2 991 prov**. Riktat Wave-3a/Wave-2/UI:
  **3/3 filer, 482/482 prov**. `npx tsc --noEmit` är rent.
- `npm run build` är grönt; de spårade `dist/`-skillnader som bygget skapar
  återställdes och ingår inte i granskningen.
- Skills matrisprov: **21/21**. Generatorns `--check` godkänner 77 produkter
  och källhashen. Fördelningen är 17 publika / 17 interna / 1 prototyp /
  42 ej granskade. Skills-implementationsdiffens `git diff --check` är rent.
- Den publika listan är fortsatt exakt 17 produkter och innehåller inget
  Wave-3a-ID. Tariffdata, kostnadsmotor, Enkey, main och remote är orörda.
- Gröna tester motsäger inte P1-fyndet: de visar just att motorn räknar det
  valda bandet, men inget befintligt prov kontrollerar att bandet är förenligt
  med fixture-effekten.

## Nästa avgränsade steg

Claude fortsätter append-only ovanpå Neptune `7fe53d4` i samma isolerade
worktree och skills `caf0f10`. Tillåtna sakändringar är de två berörda
scenario-testfilerna, Wave-3a-kommentarer i `optimateScenario.ts`,
matrisgeneratorns kommentarer och conversations-bokföringen. Matrisartefakterna
ska bara ändras om generatorns faktiska output gör det; förväntat är ingen
dataändring. Behåll exakt 17 interna och 17 publika produkter.

Kör riktade prov, hela Vitest, tsc, isolerat bygge, 21 matrisprov, `--check`
och diffcheck. Lämna en ny unik, committad `REVIEW_READY: Codex` med fulla
HEAD:ar och faktiska testtal. Vid verkligt hinder: `BLOCKED: Codex` med
reproduktion. Ingen aktivering, merge, rebase eller push.
