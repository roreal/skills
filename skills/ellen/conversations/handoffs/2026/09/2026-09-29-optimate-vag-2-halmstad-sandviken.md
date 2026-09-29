---
handoff_id: "2026-09-29-001"
created_at: "2026-09-29T20:52:09+02:00"
from: Codex
to: Claude
status: changes-required
approved_by:
  - Robert
  - Codex
---

# CHANGES_REQUIRED: Claude – slutför Optimate våg 2 med Halmstad och Sandviken

## Beslut

Robert har godkänt fortsatt arbete. Fortsätt append-only ovanpå den
isolerade Neptune-kandidaten `49c65a9230f709bde477be712642c6a7b5dc44cc`
och slutför exakt de två blockerade våg-2-produkterna. De 13 redan
implementerade produkterna ska bevaras och omverifieras.

Lösningen ska inte ändra genererad tariffdata eller påstå att Sandviken
stödjer den publika produkten aktuell årskostnad. Publik Optimate-lista ska
fortsatt vara exakt de två våg-1-produkterna.

Verifierade baser vid beslutet:

- skills lokal `main@92bef08492ba65c3732858b5c3a298c27480c26c`
- skills `origin/main@fe7099a590627fde10b489b9f1f55a1f3065e629`
- Neptune lokal/remote `main@f3ce263c532bdc9733acbe6e59a373ac90bc0336`
- Neptune isolerad kandidat `worktree-agent-ae46c6f3096412378@49c65a9`

Ingen Enkey-ändring, merge till main, rebase, push eller publik aktivering
ingår.

## A. Halmstad – explicit legacy-backend

1. Ersätt den enskilda konstanten
   `LEGACY_KOSTNADSLED_TILLATEN_TARIFF` i `besparingsvarde.ts` med en
   namngiven, oföränderlig och fail-closed lista/mängd som innehåller exakt:
   - `gotlands-energi-gotland-taxa-17-under-50-mwh-ar`
   - `halmstads-energi-och-miljo`
2. Backend-entryn ska själv kontrollera listan. Ett tredje legacy-ID ska
   fortsatt kasta `legacy_kostnadsled_ej_tillaten`; kontrollen får inte bara
   ligga i `optimateScenario.ts`.
3. Lägg Halmstad i den interna pilotkonfigurationen med backend
   `legacy_arskostnad`. Bind explicit månadsserie, angiven och oförändrad
   kapacitet samt oberoende referens-/10/15/20-facit.
4. Bevisa att Halmstads befintliga publika legacy-besparingsväg och Gotland
   taxa 17 är regressionsmässigt oförändrade.

## B. Sandviken – separat kontraktsgated besparingsbackend

1. Ändra inte `tariffer.generated.ts`, kataloggeneratorn eller policyn:
   - `stodjer_aktuell_arskostnad` ska förbli `false`;
   - `stodjer_besparing` ska förbli `true`.
2. Inför en tredje explicit `OptimateScenarioBackend`, exempelvis
   `kontraktsgatad_besparingsled`, och bind exakt Sandviken till den.
3. Skapa en smal domänentry i `besparingsvarde.ts` för ett
   kontraktsgated besparingsscenario med fulla kostnadsled och explicit
   tolvmånadersserie. Återanvänd samma privata validering, policyindata,
   `beraknaArskostnadMedKontraktProdukt` och statuslogik som den befintliga
   kontraktsvägen; duplicera ingen tariff- eller prisformel.
4. Den nya entryn ska vara fail-closed i två lager:
   - endast en kontraktsgated policy med `stodjer_besparing === true`;
   - en namngiven exakt allowlist som i denna runda bara innehåller
     `sandviken-energi-sandviken-normal`.
   Okänt ID, en tariff utan besparingsstöd och direktanrop utanför listan ska
   avvisas.
5. Den befintliga `beraknaArsproduktMedKostnadsled` och
   `stodjerAktuellArskostnad` ska fortsatt avvisa Sandviken. Den nya entryn
   är en intern scenariokostnad för en redan tillåten besparingsprodukt,
   inte en ny publik aktuell-årskostnadsförmåga.
6. Bind Sandvikens referens-/10/15/20-facit med explicit månadsserie och
   oförändrad debiterbar effekt. Befintlig publik
   `beraknaBesparingsvarde`-regression ska vara identisk före/efter.

Om återanvändningen kräver en liten intern refaktorering av
`beraknaArsproduktKarna` eller kontraktsvalideringen är det tillåtet, men
de befintliga exporterade entrypunkternas gate, returvärden och felorsaker
ska förbli kompatibla. Undvik en ny parallell kostnadsmotor.

## C. Exakt scope, matris och verifiering

1. Den kompletta interna pilotsnapshoten ska bestå av 17 produkter:
   2 från våg 1 + exakt alla 15 `review_wave == 2`. Bind hela
   ID→backend-listan och dess oföränderlighet i prov.
2. Den publika listan ska mekaniskt förbli exakt Gotland taxa 17 och
   Sundsvall Indal/Liden/Lucksta. Bind negativa publika prov för Halmstad,
   Sandviken och minst en av de övriga 13.
3. Slutför handoff 021 avsnitt D: `WAVE_2_PRODUCT_IDS` ska exakt matcha
   matrisens 15 våg-2-rader. Sätt alla 15 till
   `godkand_intern_pilot_ej_publik` och regenerera endast via generatorn.
   Förväntad fördelning av 77 val: 2 publika, 15 interna, 1 särskild
   Stockholm-prototyp och 59 `not_reviewed`.
4. Rätta kandidatens stale kommentarer som fortfarande säger 13/15 eller
   att Halmstad/Sandviken är blockerade.
5. Kör riktade prov för alla 15, alla direkta backendgrindar och
   befintliga Halmstad-/Sandviken-regressioner; därefter full Vitest i ren
   syskonlayout, `tsc --noEmit`, isolerat bygge och relevant negativt E2E.
   Kör även Python-unittest, matrisens `--check`, deterministisk
   omgenerering och `git diff --check`.
6. Redovisa exakt fillista och oberoende facit. Lämna en unik committad
   toppsignal `REVIEW_READY: Codex`. Ingen aktivering, mainflytt eller push.

Tillåten Neptune-breddning jämfört med handoff 021 är uttryckligen
`neptune-marketing/src/utils/besparingsvarde.ts` och dess riktade tester.
Tariffdata, React-produktionskod och Enkey är fortsatt utanför scope.
