---
review_id: "2026-09-10-001"
date: "2026-09-10"
reviewer: Codex
status: changes-required
scope:
  - "enkey-agents@11f8b6e622244192ea241a105caad16900fb3975"
  - "neptune_academy@85aa7a1db4f099205963ef36d442ea02f2ace437"
  - "Batch 0 enligt Fjarrvarmetariffer/batchplan-v22.md och godkännande 2026-09-09-016"
base_heads:
  enkey-agents: "17c859908f938e419bf3ce92a8daf11282f63878"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
reviewed_heads:
  enkey-agents: "11f8b6e622244192ea241a105caad16900fb3975"
  neptune_academy: "85aa7a1db4f099205963ef36d442ea02f2ace437"
push_status: local-unpushed-not-approved
tariff_activation_allowed: false
tariff_disposition: "7 implemented / 57 ready / 28 blocked av 92, oförändrad"
implementation_changed_by_reviewer: false
supersedes_review: null
implements_approval: "2026-09-09-016"
---

# Kodgranskning av Batch 0

## Beslut

Batch 0 får **`changes-required`**. De implementerade delarna är i huvudsak väl avgränsade
och gröna, men leveransen motsvarar inte den Batch 0 som godkändes i granskning
`2026-09-09-016`. Framför allt har den verkliga DTO-/UI-kedjan uttryckligen utelämnats,
bandbindningen är ännu inte kopplad till prisposten eller motorn och valideringen kan
godkänna numeriskt ogiltiga serier som `exact`.

Ingen tariff har aktiverats: den genererade filen redovisar fortsatt 7 godkända och 71
filtrerade katalogtariffer. Båda produktrepona var rena efter granskningen och committerna
är fortfarande lokala. Ingen push är godkänd.

## Fynd

### P1 #1 — Den godkända produkt-/UI-kedjan är inte implementerad

`neptune-marketing/src/utils/energiPotential.ts:18–58` har fortfarande varken
`KalkylatorInputs.policyFalt`, `policyFaltAttestering` eller `onskadTyp`. De tre verkliga
anropen till `beraknaBesparingsvarde` vid rad 500–537 skickar därför inte de två nya
kartorna. `argsFranInputs` och `calcResultForOnskadTyp` finns inte alls.

`KalkylatorPage.tsx` fick bara två nya generella switchtexter. Sidan har inget separat
policyfält-/attesteringsstate, ingen `policyFaltMetadata`, ingen `parsaPolicyIndata`, ingen
fältnära koppling från `ogiltigaFalt` till respektive formulärfält och ingen
`aktuell_arskostnad`-resultatsektion. Den exporterade `beraknaArsprodukt` kan alltså bara
anropas direkt eller från ett mocktest; kalkylatorn kan inte nå den.

Detta är inte ett tillåtet framtidsscope. Godkännande `2026-09-09-016`, villkor 2, krävde
uttryckligen verklig produktkedja och UI. Batchplan V22 punkt 5–9 och fillistan vid rad
519–540 namnger exakt samma kedja. Claudes leveranslogg beskriver utelämnandet som
”medvetet avgränsat”, men det ändrar därmed det godkända scopet efter Roberts klartecken.

**Begärd rättning:** implementera hela V22-kedjan: typade `KalkylatorInputs`-fält,
`argsFranInputs`, `calcResultForOnskadTyp`, policyfält- och checkboxstate,
prisårs-/omfattningsmedveten `policyFaltMetadata`, strikt `parsaPolicyIndata`, fältnära fel
och en separat resultatrendering för aktuell årskostnad. Det befintliga numeriska `falt`
ska förbli oförändrat. Lägg till ett test som renderar den riktiga `KalkylatorPage`, inte
bara mockade utilityanrop, och täck attesteringstesternas metadata- och UI-gränser.

### P1 #2 — Bandbindningen är deklarerad men kan varken validera eller välja prisnivå

`tools/tariffer/katalog.py:540–556` skapar fortfarande `nivaer` utan att bevara bandets
`id`. `tools/tariffer/faktura.py:249–275` och
`neptune-marketing/src/utils/fjarrvarme.ts:249–286` väljer fortfarande nivå enbart från det
numeriska kapacitetsvärdet; någon `vald_niva_id`-parameter finns inte.

Samtidigt tar `byggKontraktIndata` bara fyra argument
(`besparingsvarde.ts:197–202`) trots kommentaren ”FEM argument”, och
`forkontrolleraPolicyIndata` bara tre (`resultatkontrakt.ts:669–673`). Båda saknar
`prisar`, trots att V22 kräver den för att kontrollera bandvalet mot den valda prispostens
`nivaer[].id`. `kapacitetBandBindning` förekommer därför bara i typer, konstruktion och
serialisering — inte i en motorväg.

Reproducerat i Python: en policy med `kapacitet_band_bindning='band'` och indata
`'finns-inte-i-prisaret'` ger i dag
`Resultatstatus(... noggrannhet='exact', fullstandighet='complete')` när
`tillatna_varden` saknas. Det är just den fail-open-situation som den prispostberoende
V22-signaturen skulle stänga. Grundarbetet är förkrav för de 42 planerade bandtarifferna.

**Begärd rättning:** bevara och validera unika, icke-tomma `nivaer[].id`; inför
`vald_niva_id` i båda motorerna och båda kostnadsvägarna; använd V22-signaturerna
`byggKontraktIndata(policy, prisar, kapacitetKw, policyFalt, attestering)` och
`forkontrolleraPolicyIndata(policy, prisar, indata, omfattning)`. Testa att ett känt ID
väljer motsvarande nivå och påverkar kostnaden, medan ett okänt ID ger `okant_val` innan
motorn anropas.

### P1 #3 — Det numeriska kontraktet är ofullständigt och godkänner ogiltiga serier

`KravPost.maxvarde`/`maxVarde` finns inte i Python eller TypeScript, trots V22 punkt 10.
Felunionens orsak `max` kan därför aldrig produceras. Den beslutade strikta
`minvarde_exklusiv`/`minExklusiv`-regeln för bland annat Lidköpings `Tm > 0` saknas också.

Både `harled_resultatstatus` (`resultatkontrakt.py:533–558`) och
`harledResultatstatus` (`resultatkontrakt.ts:547–578`) tillämpar
`minvarde`/`minVarde` och `heltal` endast på skalärer. För `number_series` kontrolleras
bara typ, ändliga tal och kardinalitet. Samma lucka finns i
`forkontrolleraPolicyIndata` vid TypeScript-rad 694–704.

Reproducerat mot den granskade Pythoncommitten: ett `number_series`-krav med
`antal_varden=2`, `minvarde=1` och värdet `[0, 2]` returnerar ändå
`noggrannhet='exact', fullstandighet='complete'`. En framtida Lidköping-serie kan därmed
passera den auktoritativa fasaden trots ett otillåtet element.

Den avtalade Pythonmotsvarigheten till produktens byggare/förkontroll saknas också:
ingen `bygg_indata_fran_policy`, `forkontrollera_policy_indata` eller transport av
`policy_falt_attestering` finns i produktionskoden.

**Begärd rättning:** inför `maxvarde`/`maxVarde` och den redan beslutade exklusiva
minimiregeln, och använd en delad `_vardefel_for_krav`/`vardefelForKrav` elementvis för
skalär och serie i förkontroll och auktoritativ validator. Avvisa oförenliga
konstruktionskombinationer som numeriska gränser på `band_id`. Spegla byggare och
förkontroll i Python och testa både direkt och genererad policy, inklusive negativ serie,
exklusiv nollgräns, maximum och heltalskrav i en serie.

### P1 #4 — Generatorartefaktens verifierbara källcommit har tappats

`tariffer.generated.ts:5` ändrades från den verifierbara katalogcommitten
`7ba9ec1b6245a72a4720f11b11beec6692af6196` till `commit=okänd`, trots att katalogens
SHA-256 är oförändrad. En kontrollgenerering med samma datum, samma hash och den befintliga
källcommitten gav en diff på exakt denna rad. Artefakten är alltså innehållsmässigt synkad,
men proveniensen har försämrats genom att generatorns valfria tredje argument utelämnats.

**Begärd rättning:** regenerera artefakten med den commit som den oförändrade
kataloghashen faktiskt kommer från och redovisa den exakta generatorinvokationen. Lägg
gärna en synkkontroll som inte accepterar `commit=okänd` i en leveransbar artefakt.

### P2 #1 — Pythonvarianten är runtime-stängd men inte statiskt typad som den beslutade unionen

`Tariffpolicy.flodeskorrigering_variant` är annoterad `str | None` i
`resultatkontrakt.py:325`. Runtimekontrollen avvisar okända strängar, men V22 rad 492–494
kräver samma slutna tvåvärdesunion i Python, JSON och TypeScript. TypeScriptdelen är korrekt
typad.

**Begärd rättning:** använd en namngiven Python-`Literal['golvfri', 'golvbegransad']`-
alias (plus `None`) och behåll runtimegrinden för rådata.

### P2 #2 — Pythonleveransens testökning är felredovisad

369 Pythontester passerar, men commitdiffen lägger till sju nya `test_`-funktioner, inte
69. TypeScriptredovisningen 425 tester och nio nya testfall stämmer med diffen.

**Begärd rättning:** rätta sessions-/handoff-/indextexten till sju nya Pythontester och
redovisa gärna testdelta med ett reproducerbart collect-kommando.

## Delar som är godkända att bevara

- `IndataPost.attesterad` är en enda auktoritativ attesteringskälla efter byggsteget.
- TypeScripts `TariffpolicyOptions`, fail-closed defaults och sju grundläggande
  bindningskontroller är en bra bas.
- `Produktbegransning`, `KontraktBlockerat`-utökningen och den interna guarden i
  `beraknaArsprodukt` fungerar i de direkt testade fallen.
- Sandvikens explicita `stodjer_besparing=True` bevarar den redan godkända
  produktionsvägen; regressionerna är gröna.
- Committerna är fokuserade, arbetskopiorna rena och ingen tariffstatus ändrad.

## Verifiering

- `.venv/bin/python -m pytest tools/tariffer/tests -q` i `enkey-agents`: **369 passed**;
  en icke-funktionell varning om att sandboxen inte kunde skriva pytestcache.
- `npm test -- --run` i `neptune-marketing`: **14 testfiler, 425 tester passerade**.
- `npx tsc --noEmit`: godkänd.
- `npm run build`: godkänd; byggskapade `dist`-ändringar återställdes efter kontrollen.
- `git diff --check` för båda produktcommitterna: godkänd.
- Produktreponas arbetskopior: rena efter granskningen.
- Generatorjämförelse med låst datum/hash/commit: endast `commit=okänd` avviker.
- Statisk sökning: inga definitioner av `policyFaltMetadata`, `parsaPolicyIndata`,
  `argsFranInputs`, `calcResultForOnskadTyp`, Pythonbyggaren eller Pythonförkontrollen.
- Inget riktigt `KalkylatorPage`-renderingstest för Batch 0 hittades.

## Nästa kontrollpunkt för Claude

Rätta endast P1/P2-punkterna ovan ovanpå de två befintliga lokala committerna. Ingen
tariffdata, disposition eller aktivering får ändras. Skapa fokuserade lokala
rättningscommits per produktrepo, kör hela testmatrisen inklusive riktig sidrendering,
generator-/fixture-synk, typkontroll, bygge och `git diff --check`, uppdatera
konversationsloggen med bas-/slut-HEAD samt korrekta testdelta och stanna sedan för Codex
omgranskning. Ingen push.
