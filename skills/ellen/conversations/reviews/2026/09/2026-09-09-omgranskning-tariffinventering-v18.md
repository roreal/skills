---
review_id: "2026-09-09-012"
date: "2026-09-09"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v18.md
  - Fjarrvarmetariffer/batchplan-v18.md
  - skills commits a3ce065b00b17790d2c7ce1b581cb411c4a4e837 and 673a618ad8a20e66a3be41ede4c8a0b46822f1dc
reviewed_heads:
  skills: "673a618ad8a20e66a3be41ede4c8a0b46822f1dc"
  enkey-agents: "fd8f8da3eb17cce638dc2f3370efa027c2afcad6"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-09-011"
preserve_source_reviews:
  - "2026-09-09-006"
  - "2026-09-09-008"
  - "2026-09-09-009"
---

# Omgranskning av tariffinventering v18 och batchplan v18

## Bedömning

V18 väljer rätt modell för Tm-proveniens, gör själva min-/max-/heltalsalgoritmen
seriekompatibel och beskriver ett separat `Produktbegransning`-fel. Den framtida Batch
5d-fillistan innehåller nu den verkliga katalogfilen och namngivna tester. Dessa delar ska
bevaras.

Planen är ändå inte implementeringsklar. Två nya säkerhetsfält saknas i den uttryckliga
Python→JSON→TypeScript-transporten, Tm-attesteringen är bara en kringgåbar UI-spärr och
besparingsförmågan är fail-open. Den utskrivna produktguarden ersätter dessutom den
verkliga femparametersfunktionen med en inkompatibel tvåparameterssignatur, och dokumenten
har kvar de äldre normativa kontrakt som V18 uppger sig ha ersatt. V19 krävs före
produktkod, tariffdata, aktivering eller push.

## P1-fynd

### P1 — de nya policyfälten transporteras inte hela vägen

V18 säger korrekt att `policyFranGenererad()` mappar fälten för hand, men tabellen vid
`tariffinventering-v18.md:2095–2110` innehåller fortfarande exakt fjorton äldre fält. Den
saknar både:

- `Tariffpolicy.stodjer_besparing` → `stodjerBesparing`, och
- den deklaration/transport som ska bära `KravPost.krav_attestering` →
  `kravAttestering` till UI-metadatan.

Rad 2112 säger fortfarande ”samtliga fjorton fält”. Den verkliga TypeScriptkoden bekräftar
att detta inte sker automatiskt: `policyFranGenererad()` bygger varje `KravPost` och varje
`Tariffpolicy`-option uttryckligen, medan `skapaTariffpolicy()` också har en explicit
options-typ och ett explicit returvärde. V18 anger ingen motsvarande ändring av options-
eller returvägen.

Konsekvensen är säkerhetskritisk: Python kan generera `stodjer_besparing=False`, men
TypeScript får `undefined`; V18:s resolver tolkar sedan `undefined !== false` som att
besparing är tillåten. På samma sätt kan attestkravet försvinna innan UI:t skapas.

**Begärd rättning:** utöka den auktoritativa transporttabellen med båda fälten och skriv ut
hela konstruktionskedjan: Python-dataklass, genererad snake_case-JSON, TypeScriptinterface,
`policyFranGenererad()`, `skapaTariffpolicy()`s options och returvärde samt
`PolicyFaltMetadata`. Lägg negativa transporttester som bevisar att explicit `false` och
`true` överlever genereringen och att attestkravet når sin konsument.

### P1 — Tm-attesteringen är UI-only och kan kringgås

V18 rad 4212–4224 kallar attesteringen uttryckligen en ”REN UI-nivå-spärr”. Det räcker inte
för ett värde som domänlagret därefter märker `supplier_value`: ett direkt anrop kan skicka
Tm-serien utan någon attestering och ändå få samma källklassning. Den uppräknade
`PolicyFaltMetadata`-formen vid rad 2453–2455 innehåller dessutom inte ens
`kravAttestering`, och formuleringen om en Python-generering av `policyFaltMetadata` anger
ingen verklig ägare eller transport.

**Begärd rättning:** gör attestkravet till ett verkligt `KravPost`-fält i Python och
TypeScript och transportera det enligt föregående fynd. För att en kundberäkning ska få
använda `supplier_value` måste den faktiska attesteringen också finnas i den typade
produktindatan och kontrolleras i den auktoritativa produkt-/domänvägen före skapandet av
`IndataPost`; kryssrutan är endast dess UI. Ett direkt produktanrop utan attestering ska
blockeras i test, medan ett attesterat anrop ska passera. Hårdkoda inte Lidköpingsnyckeln i
validatorn.

### P1 — `Produktbegransning`-guarden passar inte den verkliga funktionssignaturen

V18 rad 3177–3185 skriver om `beraknaBesparingsvardeKontrakt` till två parametrar
`(args, prisar)` och kallar därefter kroppen oförändrad. Den verkliga privata funktionen i
`besparingsvarde.ts:251–259` tar fem parametrar:
`(args, leverantor, prisar, kapacitetGolv, policy)`, och det verkliga anropet vid rad 361
skickar alla fem. En rak implementation av V18 tappar alltså tre värden som resten av
kroppen behöver.

Testtexten vid V18 rad 3194 använder samtidigt `onskadTyp:'besparing'` i ett
`beraknaBesparingsvarde`-anrop, trots att det fältet enligt samma plan tillhör
`KalkylatorInputs`, inte den verkliga `BesparingsvardeArgs`-typen. V18 skapar dessutom en
Pythonklass i en påstådd `besparingsvarde.py`, men ingen sådan Python-produktmodul finns i
något av de två produktrepoerna.

**Begärd rättning:** placera guarden först i den befintliga femparametersfunktionen och
använd den redan upplösta `policy`-parametern, eller visa en komplett och typkorrekt
signatur-/anropsändring. Det direkta testet ska anropa rätt entry med dess verkliga typ;
sidtestet får separat använda `KalkylatorInputs.onskadTyp`. Ta bort den fiktiva
Pythonfilen ur plan och fillista om en verklig Pythonkonsument inte uttryckligen ska
införas och testas.

### P1 — besparingsförmågan är fail-open

V18 rad 3367–3397 väljer `stodjer_besparing=True` som Python-default,
`stodjerBesparing?: boolean` som TypeScriptfält och `!== false` som resolver. Varje ny
kontraktsgatad tariff får därmed besparingsstöd om en utvecklare glömmer att deklarera
fältet. Det strider mot Ellens grundregel att bara kostnadskomponenter som faktiskt
påverkas av åtgärden får räknas som besparing. Tillsammans med den saknade mappningen ovan
gör det redan nu avsedda `false` för Stockholm och Lidköping till ett möjligt `true`.

**Begärd rättning:** använd explicit opt-in för kontraktsgatade tariffer:
`stodjer_besparing=False` som Python-default och `policy.stodjerBesparing === true` i
TypeScript. Sätt Sandviken uttryckligen till `True`; Stockholm och Lidköping till `False`.
Legacytariffer kan behålla sin nuvarande väg utanför kontraktsgrinden. Testa saknat,
`false` och `true` samt att de två förmågefälten fortsatt är oberoende.

### P1 — äldre normativa kontrakt finns kvar och motsäger V18-beslutet

V18 uppger att den äldre capability-texten är ersatt, men följande aktuella instruktioner
finns fortfarande kvar:

- inventeringen rad 3291–3309 säger ”Löst med EN tabell” men visar den gamla
  Stockholmsspecifika `kallenergiArsserieBindning`-resolvern; först därefter kommer en ny
  rättelse,
- rad 3264 kallar årsresultatet ”Stockholm-fallet, enda varianten” trots att samma plan nu
  använder entryn för Stockholm och Lidköping,
- rad 3272 kallar `beraknaBesparingsvardeKontrakt` oförändrad trots ny guard och delad
  indatabyggare,
- batchplanen rad 460–462 har kvar den ogiltiga `kallaTyp:'snapshot'` och intern
  resultattext ”uppskattat”,
- batchplanen rad 1015–1018 säger att `stodjerBesparing` kontrolleras inuti
  `beraknaArsprodukt`. Det skulle blockera precis den aktuella årskostnad som Stockholm och
  Lidköping ska stödja; årsentryn ska kontrollera aktuell-årskostnadsförmågan, medan
  besparingsförmågan hör till besparingsentryn,
- batchplanen rad 1040 kallar produktbegränsningsfelet ”oförändrat” trots att det är nytt.

**Begärd rättning:** skapa V19 som ett rent aktuellt kontrakt, inte ännu ett lager av
historiska rättelser. Ta bort eller märk äldre varianter som uttryckligen historiska och
icke normativa. Det ska finnas en resolver, en capability-tabell, en aktuell signatur och
en fillista som går att implementera bokstavligt.

### P1 — den delade serievalidatorns ägare/import är oklar

Själva algoritmen vid rad 2040–2068 är korrekt, inklusive strikt minimum. Men
TypeScriptkommentaren säger att samma funktion ligger i ”`besparingsvarde.ts /
resultatkontrakt.ts`”. Den använder `arSerie`, som i den verkliga
`resultatkontrakt.ts:67` är privat. Statusvalidatorn finns i `resultatkontrakt.ts`, medan
den planerade produktförkontrollen ligger i `besparingsvarde.ts`; en icke exporterad
funktion kan inte delas mellan dem.

**Begärd rättning:** ange exakt en ägare och en importväg utan importcykel, exempelvis en
exporterad `vardefelForKrav` i `resultatkontrakt.ts` som importeras av
`besparingsvarde.ts`. Gör motsvarande Pythonägarskap konkret och säkerställ att den delade
orsakstypen är åtkomlig. Behåll testet som jämför förkontroll och direkt fasad.

## Godkända delar och verifieringar

- `Tm_m` som `supplier_value` med automatiskt `noggrannhet:'snapshot'` via
  `rullande=True` är rätt käll-/statusmodell. Det behövs ingen ny medlem i `KALLTYPER`.
- `vardefelForKrav`/`_vardefel_for_krav` har rätt elementvisa min-, max- och
  heltalssemantik; endast ägarskap och verklig inkoppling behöver preciseras.
- En separat `Produktbegransning` med egen UI-mappning är rätt felmodell.
- Batch 5d listar nu den riktiga `optimate-fjarrvarme-2026.json`, motorregistren,
  facade→motor-transporten och relevanta namngivna tester.
- V17:s kanoniska `signed_monthly_flow_adjustment` och `faltSerier`/`falt_serier`-kedja
  ska bevaras.
- Lidköpings två produkter förblir källgodkända och `ready_to_implement`; ingen Tm-serie
  får gissas eller hårdkodas.
- Dispositionen förblir 7 implementerade, 57 redo och 28 externt blockerade av totalt 92.
- `git diff --check 497fbfc..673a618` är rent. V18-committarna ändrar endast dokumentation
  och logg. Produktrepoerna står kvar på `enkey-agents@fd8f8da` och
  `neptune_academy@f1df177`; ingen tariff är aktiverad.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v19.md` och `batchplan-v19.md`; ändra inte V18 i efterhand.
2. Lägg in `stodjer_besparing` och `krav_attestering` i hela Python→JSON→TypeScript-
   transporten, inklusive `skapaTariffpolicy`, `policyFranGenererad`, metadata och
   negativa transporttester.
3. Gör attesteringen generisk och auktoritativ även för direkta produkt-/domänanrop;
   transportera faktisk attestering i den typade indatan och behåll kryssrutan som UI.
4. Anpassa `Produktbegransning`-guarden till den verkliga femparametersfunktionen och
   korrigera entry-/testtyperna. Ta bort den icke-existerande Pythonproduktfilen om den
   inte faktiskt införs.
5. Gör kontraktsgatad besparingsförmåga explicit fail-closed. Sandviken ska opta in;
   Stockholm och Lidköping ska vara spärrade. Legacyvägen ska förbli oförändrad.
6. Ersätt, i stället för att komplettera, alla kvarvarande gamla normativa capability-,
   källtyp-, resultattyp-, signatur- och ”oförändrad”-stycken i båda dokumenten.
7. Ange en exakt ägare/import för den delade elementvisa validatorn och bevara direkta
   fasadtester i båda språken.
8. Bevara den godkända motortransporten, Batch 5d:s verkliga katalog-/testfillista,
   Lidköpings källstatus, räkningen 7/57/28 och Åkermannen-underlaget. Lägg denna granskning
   och loggändringarna i en fokuserad lokal dokumentationscommit, logga verklig hash/tid
   och stanna för omgranskning. Ändra ingen produktkod, tariffdata, aktivering eller push.
