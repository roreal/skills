---
handoff_id: "2026-09-25-021"
created_at: "2026-09-25T14:22:04+02:00"
from: Codex
to: Claude
status: approved-for-implementation
approved_by:
  - Robert
  - Codex
---

# APPROVED_FOR_IMPLEMENTATION: Claude – Optimate våg 2, energiscenarier med låst kapacitet

## Mandat och mål

Robert har efter publicerad våg 1 sagt **"OK kör"** för nästa våg.
Implementera en intern, ej publik 10/15/20-pilot för exakt de 15 verkliga
produkter som den granskade täckningsmatrisen klassar som `review_wave == 2`.

Våg 2 avser produkter med ett debiterbart kapacitets-/effektled men utan
identifierat flödes-, returtemperatur-, serie- eller behörighetsberoende som
flyttar dem till en senare våg. Denna leverans ska visa den tariffkorrekta
kostnadseffekten av **10/15/20 procent mindre styrbar rumsvärme**, medan
debiterbar effekt/kapacitet och alla andra uttryckliga referensindata hålls
oförändrade.

En generell uppskattning om 20 procent lägre toppeffekt är inte tillräcklig
för tariffvis kostnadsberäkning och får inte bakas in i huvudscenariot. En
framtida, separat effektsensitivitet kräver tariffens mätfönster, historik och
ett explicit användarantagande. Den delen ska dokumenteras som kvarstående,
inte presenteras som besparing i denna runda.

## Verifierade baser

- skills `main@fe7099a590627fde10b489b9f1f55a1f3065e629`
- neptune_academy `main@f3ce263c532bdc9733acbe6e59a373ac90bc0336`
- enkey-agents `main@5150d0be882eee591112300d160e64f438d17f51`
- Skills och Neptune `origin/main` matchade respektive lokala HEAD efter
  våg 1-pushen.
- Enkey ska varken ändras eller pushas i denna leverans.

Stoppa och skriv `BLOCKED: Codex` om någon bas har flyttats på ett sätt som
gör en ren avgränsning omöjlig. Skriv inte om historik och ta inte med
orelaterade arbetskopiefiler.

## Exakt våg-2-scope

1. `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad`
2. `c4-energi-kristianstad`
3. `gavle-energi-gavle`
4. `halmstads-energi-och-miljo`
5. `harnosand-energi-miljo-harnosand`
6. `karlstads-energi-karlstad`
7. `kils-energi-kil`
8. `oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024`
9. `ovik-energi-ornskoldsvik`
10. `sandviken-energi-sandviken-normal`
11. `skovde-energi-skovde`
12. `soderhamn-nara-soderhamn-taxa-11-och-12`
13. `tekniska-verken-katrineholm-katrineholm`
14. `temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus`
15. `trollhattan-energi-trollhattan`

Mängden ska bindas mekaniskt mot matrisens `review_wave == 2`. Ingen
syntetisk produkt eller annan tariff får följa med.

## A. Intern scenariomotor

1. Utöka den interna pilotkonfigurationen med exakt dessa 15 ID:n.
   Behåll de två publicerade våg-1-produkterna. Gör den fullständiga interna
   pilotmängden maskinellt inspekterbar och oföränderlig, på motsvarande
   sätt som `SCENARIO_PUBLIKT_AKTIVERADE_ID`, så att prov kan jämföra hela
   listan och backendvalet utan punktvisa luckor.
2. Välj backend explicit per produkt:
   - `halmstads-energi-och-miljo` använder `legacy_arskostnad`;
   - övriga 14 använder `kontraktsgatad_kostnadsled`.
   Ingen automatisk fallback eller härledning från filform tillåts.
3. Använd samma tariffmotor, tariffversion och kompletta underlag före och
   efter. Endast den validerade månadsserien för styrbar rumsvärme minskas
   10/15/20 procent.
4. Följande ska vara bit-/värdemässigt låst till referensen där det finns:
   debiterbar effekt/kapacitet, valt kapacitetsband/taxesteg, historik,
   policyfält, fasta avgifter, flöde, returtemperatur, kölddygn,
   miljötillägg och produkt-ID. Motorn får inte välja om kapacitetsband
   därför att efterfallet använder mindre energi.
5. Energiberoende rabatter och gränser får endast ändras om den befintliga
   tariffmotorn faktiskt räknar om dem från efterfallets energiserie. Det
   gäller särskilt Gävles och Härnösands marginella årsvolymregler. Redovisa
   dessa komponenter separat; lås dem inte felaktigt och skapa ingen parallell
   prisformel.
6. Bevara Halmstads och Sandvikens befintliga publika besparingsvägar exakt.
   Ändra inte `_kraver_kontrakt`, `stodjer_besparing`, kataloggenerator,
   genererad tariffdata eller befintliga resultat för någon produkt.
7. `SCENARIO_PUBLIKT_AKTIVERADE_ID` ska förbli exakt våg 1:
   Gotland taxa 17 och Sundsvall Indal/Liden/Lucksta. Alla 15 våg-2-ID:n ska
   ha positiva interna och negativa publika förmågeprov.

## B. Tariffvis verifiering

För samtliga 15 produkter:

1. bygg en minsta giltig, verklighetsnära fixture med alla obligatoriska
   policyfält och ett explicit valt kapacitets-/taxesteg;
2. bind referenskostnad, 10/15/20 efterkostnader och skillnader mot ett
   oberoende facit som inte anropar funktionen under test för att skapa det
   förväntade svaret;
3. bind att den styrbara energin minskar rätt, att övrig last ligger kvar och
   att kapacitetskostnaden/kapacitetsunderlaget inte minskar;
4. bind kostnadsledssumman före och efter, moms/prisår och preliminär status;
5. prova ett relevant gränsfall: bandgräns, volymrabatt, miljötillägg,
   överuttag eller saknat obligatoriskt fält beroende på produkt;
6. bevisa att noll eller negativ kostnadsskillnad visas ärligt om en tariff
   ger det och aldrig kläms till ett positivt belopp.

Facit ska dokumenteras tillräckligt för att Codex ska kunna räkna om minst
ett exempel per tariff utan att lita på produktionsfunktionen. Dela gärna
testdata i en typad tabell, men dölj inte produktspecifika antaganden bakom
ett generiskt facit.

## C. UI-regression och framtida effektsensitivitet

Ingen ny React-funktion behövs för intern pilot om den befintliga generiska
våg-1-vägen fungerar. Verifiera däremot att:

- inget våg-2-kort eller våg-2-felmeddelande syns publikt;
- våg 1 och Stockholms särskilda prototyp är oförändrade;
- det befintliga formuläret kan bygga ett komplett underlag för varje
  våg-2-produkt utan dold default för ett obligatoriskt policyfält.

Lägg en kort teknisk designnot för en senare, separat
**effektsensitivitet**. Den ska minst ange explicit användarvärde/scenario,
tariffens mätfönster och historik, tidsmässigt genomslag samt att energi- och
effektbesparing inte får dubbelräknas. Implementera eller visa inte denna
funktion i den publika kalkylatorn nu.

## D. Matris och bokföring

1. Lägg en namngiven, fail-closed `WAVE_2_PRODUCT_IDS` och kontrollera att
   den är exakt identisk med snapshotens `review_wave == 2`.
2. Efter godkänd intern implementation sätts de 15 produkterna till
   `godkand_intern_pilot_ej_publik`. Förväntad statusfördelning av 77 val:
   - 2 `godkand_publik_10_15_20` (våg 1),
   - 15 `godkand_intern_pilot_ej_publik` (våg 2),
   - 1 `synlig_sarskild_preliminar_prototyp` (Stockholm),
   - 59 `not_reviewed`.
3. Regenerera JSON och Markdown endast via generatorn, bind aktuell
   Neptune-käll-SHA och kontrollera deterministisk andra generering.
4. Uppdatera sessionsfil och index append-only med unik nästa signal.

## Tillåtna huvudsakliga ändringar

Neptune:

- `neptune-marketing/src/utils/optimateScenario.ts`
- nya eller befintliga riktade `optimateScenario*.test.ts`
- vid behov en avgränsad negativ React-/sidtestfil
- en kort designnot i befintlig relevant dokumentationsyta eller i denna
  sessions/handoff-kedja

Skills:

- `Fjarrvarmetariffer/generera_besparingspotential_tackningsmatris.py`
- dess test
- de två genererade matrisartefakterna
- denna sessions-/indexbokföring och vid behov en avgränsad designnot

Om implementationen kräver ändring av tariffmotor, tariffdata,
KalkylatorPage-produktionskod eller Enkey: stoppa med `BLOCKED: Codex` och
beskriv exakt varför. Bredda inte scope tyst.

## Arbetsform och verifieringsgrind

Arbeta i en ny isolerad Neptune-worktree/branch från exakt `f3ce263`.
Committa fokuserat. Ingen publik aktivering, merge till main, rebase, push,
force eller historikomskrivning ingår.

Kör minst:

- riktade motor-/tariff-/gate-/regressionsprov för samtliga 15 produkter;
- hela Vitest i en ren, dokumenterad syskonlayout med rätt Enkey-snapshot;
- `npx tsc --noEmit` och isolerat bygge utan att lämna spårad `dist/`;
- relevant negativt Chromium/E2E som bevisar att våg 2 inte är publik;
- Python-unittest, generatorns `--check`, deterministisk omgenerering och
  `git diff --check`;
- exakta fillistor och kontroll av att orelaterade filer är orörda.

Lämna en unik committad toppsignal `REVIEW_READY: Codex` med commithashar,
testtal, exakta avvikelser och kvarstående risker. Om uppdraget inte kan
slutföras inom dessa gränser: skriv i stället en unik committad
`BLOCKED: Codex` med konkret blockerare.
