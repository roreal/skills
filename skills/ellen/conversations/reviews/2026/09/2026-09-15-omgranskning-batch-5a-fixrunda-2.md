---
review_id: "2026-09-15-002"
date: "2026-09-15"
reviewer: Codex
status: changes-required-before-activation
scope:
  - "Batch 5a rättningsrunda 2 bakom spärr"
  - "skills@ed2a63c (leveranslogg skills@58f2515)"
  - "enkey-agents@c99ff79"
  - "neptune_academy@4f62fe8"
implementation_changed_by_reviewer: false
activation_status: not-approved
push_status: not-approved
tariff_disposition: "37 implemented / 27 ready / 28 blocked av 92"
handoff: "conversations/handoffs/2026/09/2026-09-14-batch-5a-leverantorsvarde.md"
previous_review: "conversations/reviews/2026/09/2026-09-15-omgranskning-batch-5a-fixrunda-1.md"
---

# Omgranskning: Batch 5a rättningsrunda 2

## Beslut

**Changes required före aktivering.** De tre tidigare P1-problemen är i sak
nästan stängda: sex fasta/ogenomskinliga underlag har skilts från C4:s och
Trollhättans verkligt rullande semantik, UI-provet drivs nu av den
generatorbundna fixturen och inventeringen mappar exakt rätt åtta ID:n. Alla
ordinarie testsviter är gröna och samtliga åtta katalogspärrar är orörda.

Det nya snapshot-fältet uppfyller däremot ännu inte det uttryckliga kravet att
vara slutet och fail-closed. Både Python och den publika JSON→TypeScript-vägen
accepterar exempelvis strängen `"false"`; eftersom värdet sanningskonverteras
blir resultatet tyst `annual/snapshot/complete`. Det återstår också tre mindre,
men tidigare uttryckligen beställda, rättelser: C4:s entydiga bandgränser,
verifieringslistans verkliga implementationsstatus och källsann beskrivning av
Öresund/TEMAB.

Ingen tariffkod ändrades av Codex. Ingen aktivering eller push är godkänd;
**37/27/28** och 39 skarpa produkter ska bestå.

## Fynd

### P1. Det nya snapshot-taket accepterar godtyckliga sanningslika värden

`KravPost.takad_till_snapshot` deklareras som `bool`, men `__post_init__`
kontrollerar bara kombinationen med `rullande` och aldrig själva runtime-typen
(`resultatkontrakt.py:177-202,335-344`). TypeScript gör samma sak:
`policyFranGenererad()` tar `any`, för vidare råvärdet med `?? false`,
`skapaKravPost()` validerar bara kombinationen `=== true`, och statusvägen
använder `Boolean(...)` (`resultatkontrakt.ts:170-182,212-216,437-462`).

Codex reproducerade därför följande i båda språk med ett i övrigt giltigt,
verifierat årsunderlag:

```text
Python: takad_till_snapshot="false" -> runtime type str -> annual/snapshot/complete
TS JSON: takad_till_snapshot="false" -> runtime type string -> annual/snapshot/complete
```

Det är motsatsen till den förra granskningens bindande krav att det nya
serialiserade policytaket ska vara slutet/fail-closed. Det är särskilt viktigt i
TypeScript eftersom modulens eget kontrakt säger att genererad JSON inte är mer
betrodd än handbyggd policy.

Validera att fältet är exakt boolean i Pythonkonstruktionen och i
`skapaKravPost`/`policyFranGenererad`; avvisa strängar, tal, `null` och andra
värden i stället för att sanningskonvertera dem. Lägg språkparitetsprov för
default `false` (äldre policy kan fortfarande ge `exact` när övriga villkor
tillåter), explicit `true` (ger `snapshot`), fel typ (kastar) och kombinationen
`rullande=true` + tak (kastar). Pinna dessutom orsaken per Batch 5a-policy:
exakt C4/Trollhättan ska vara rullande utan tak och de sex andra ska ha tak utan
`rullande`; dagens statusprov bevisar bara slutordet `snapshot`, inte vilken
metadata som orsakade det.

### P2. C4:s entydiga bandgränser undantas fortfarande från matrisen

Den nya matrisen är komplett för sex leverantörer och TypeScript har nu en
verklig spegel, vilket stänger större delen av föregående fynd. Klassen undantar
emellertid hela C4 med hänvisning till den enda tvetydiga 500 kW-punkten
(`test_leverantorsvarde_batch5a_kontrakt.py:315-330`). C4-proven testar endast
500 kW med band 5 respektive 6 (`:279-312`).

Handoffens krav var varje bands båda ändar **där källan är entydig**. Lägg i
båda språk C4:s klara punkter: band 2 vid 3/49, band 3 vid 50/99, band 4 vid
100/199, band 5 vid 200/499 och en representativ giltig punkt över 500 för band
6. Behåll det separata dubbelprovet vid 500. Dokumentera uttryckligen att band
1:s publicerade 0–2 inte kan nås genom policyns verifierade minimum 3 och därför
inte ska förfalskas till ett gränsprov.

### P2. Verifieringslistan är ännu inte synkad med rättningen

Föregående granskning bad om både status och källa för de fem återstående
Batch 5a-posterna. Rundan lade endast till käll-/återverifieringsannotationer:
C4, Söderhamn, TEMAB, Trollhättan och Öresund Totalvärme står fortfarande bara
som godkända 2026-09-04, inte lokalt implementerade bakom spärr
(`verifieringslista-fjarrvarmebolag.md:52-58,331-351,376-381,453-456`).

Samtidigt säger Kil, Skövde och Katrineholm fortfarande att
`rullande=True`/"rullande 3-årssemantik" ger snapshot
(`:169,317,358`), trots att rättningen uttryckligen bytte dessa policyer till
`rullande=False` + `takad_till_snapshot=True`.

Synka exakt alla åtta poster med den lokala, ännu inte aktiverade
implementationen och den nya metadataorsaken. Markera dem inte som skarpa eller
aktiverade.

### P2. Snapshot-takets dokumentation gör två starkare källpåståenden än källorna

Python- och TypeScriptkontrakten säger att samtliga sex takade leverantörer,
inklusive Öresund och TEMAB, har officiella källor som beskriver ett fast,
periodiskt/årsvis omräknat underlag (`resultatkontrakt.py:177-182` och
`resultatkontrakt.ts:170-177`). Öresundspolicyn skärper detta till att A är
"ett fast prisårsunderlag" (`policyregister.py:1406-1409`).

De aktuella officiella källorna räcker inte för de påståendena. Öresundskraft
anger bara att aktuellt A finns på senaste energifakturan; den publicerade
2026-sidan anger ingen omräkningsperiod. TEMAB anger att P fastställs med
kategoritalsmetoden (eller anslutningsvärde när metoden inte passar), men
publicerar varken metodens historikfönster eller uppdateringsintervall. Det
motiverar ett konservativt snapshot-tak, men inte etiketten "fast
kalenderårsunderlag".

Behåll gärna samma explicita tak, men definiera det generellt som en konservativ
maxnoggrannhet när värdets period/oberoende verifierbarhet är otillräcklig. Säg
endast "fast/årsvis" på de policyer där källan faktiskt styrker det. Alternativt
krävs en ny officiell källa som styrker Öresunds och TEMAB:s påstådda period.

## Stängda fynd från granskning 2026-09-15-001

- Sex icke-rullande kandidater har separat snapshot-tak; endast C4 och
  Trollhättan bär `rullande=True`.
- UI-mocken använder generatorfixturens `PRISAR`/`POLICY_JSON`; kronor och
  schablon provas genom den riktiga sidan. `abc`-fallet är nu ärligt beskrivet
  som DOM-sanerad tomväg, medan NaN provas direkt i kontraktet.
- Inventeringen har exakt de åtta rätta Batch 5a-raderna och en permanent
  exakt-ID-kontroll.
- Bandmatriserna täcker samtliga band för Trollhättan, Söderhamn, Kil,
  Katrineholm, Öresund och TEMAB i båda språk.
- Sessionsloggens Kil/Skövde- och R13-rättelser samt Kils byteidentiska
  URL-alias är dokumenterade.

## Verifierat i omgranskningen

- Tariffprojektets fulla Python-scope: **1439 passed, 4 skipped**. Pytest gav
  en enda sandboxrelaterad cachevarning men inga testfel.
- Full TypeScriptsvit: **1381 passed** i 45 filer.
- `npx tsc --noEmit`: rent. `npm run eval:build`: grönt med känd
  chunkstorleksvarning.
- Diffcheck: rent för `skills@82e774b..58f2515`,
  `enkey-agents@674a057..c99ff79` och
  `neptune_academy@c6c50a9..4f62fe8`.
- Katalog: **86** fysiska, **37** godkända; exakt de åtta har fortsatt
  `contract_required:true`, `production_ready:false`,
  `investigation.status="utreds"`.
- Skarp genererad fil: **39** produkter, inga Batch 5a-ID:n.
- Disposition: **37 implemented / 27 ready / 28 blocked av 92**.
- Orelaterad arbetskopiesmuts i `skills` och befintliga `dist`-ändringar i
  Neptune är orörda.

## Rättningsordning till Claude

1. Gör `takad_till_snapshot`/`takadTillSnapshot` strikt boolean och
   fail-closed vid båda publika konstruktions-/JSON-gränserna; lägg generiska
   språkparitetsprov samt exakt 2+6-metadatafördelning för Batch 5a.
2. Komplettera C4:s entydiga bandpunkter i Python och TypeScript utan att
   automatisera eller gissa 500 kW.
3. Synka verifieringslistans åtta implementationsstatusar och ersätt de tre
   stale `rullande=True`-beskrivningarna.
4. Bredda snapshot-takets dokumenterade betydelse för ogenomskinliga
   leverantörsvärden, eller tillför officiellt stöd för Öresund/TEMAB:s
   omräkningsperiod. Rätta den osäkra Öresundstexten i policyn.
5. Kör samma fulla sviter, tsc, eval-bygge, generator-/SHA-/spärr-/räknings-
   och diffkontroll. Commitera fokuserat lokalt och stanna för Codex
   omgranskning. Ingen aktivering och ingen push.
