---
review_id: "2026-09-10-002"
date: "2026-09-10"
reviewer: Codex
status: changes-required
scope:
  - "enkey-agents@714da6fe12a8a6c171968e01eddefa50fedc0a0f"
  - "neptune_academy@b87ff5853623b2c492cc56b91ba046920013caea"
  - "Rättningar mot kodgranskning 2026-09-10-001"
base_heads:
  enkey-agents: "11f8b6e622244192ea241a105caad16900fb3975"
  neptune_academy: "85aa7a1db4f099205963ef36d442ea02f2ace437"
reviewed_heads:
  enkey-agents: "714da6fe12a8a6c171968e01eddefa50fedc0a0f"
  neptune_academy: "b87ff5853623b2c492cc56b91ba046920013caea"
push_status: local-unpushed-not-approved
tariff_activation_allowed: false
tariff_disposition: "7 implemented / 57 ready / 28 blocked av 92, oförändrad"
implementation_changed_by_reviewer: false
supersedes_review: null
follows_review: "2026-09-10-001"
implements_approval: "2026-09-09-016"
---

# Omgranskning av Batch 0-rättningarna

## Beslut

Rättningarna får fortsatt **`changes-required`**. Fyra viktiga delar är nu korrekt
implementerade och får bevaras: nivå-ID:n når motorerna, numeriska regler valideras
elementvis i båda språk, Pythonvarianten är en sluten `Literal` och den genererade filens
källcommit är återställd. Alla ordinarie tester, typkontrollen och produktionsbygget är
gröna.

Batch 0 är ändå inte komplett mot det uttryckligen godkända V22-kontraktet. Den verkliga
produktsidan är fortfarande inte kopplad till de nya kontrakten, den nya
årskostnadsdispatchen duplicerar och avviker från scope-/provenienslogiken och okända
band-ID:n lämnar fortfarande den typade användarfelsvägen. Ingen tariff får aktiveras och
ingen av de lokala produktcommitterna är godkänd för push.

## Fynd

### P1 #1 — Den godkända UI-kedjan saknas fortfarande, utan tekniskt blockerande skäl

`KalkylatorPage.tsx:353–381` anropar fortfarande enbart `calcResult` och skickar varken
`onskadTyp`, `policyFalt` eller `policyFaltAttestering`. Sidan har inget separat råstate för
policyfält/checkboxar, renderar ingen prisårs-/omfattningsmedveten metadata, kör ingen
strikt parser eller fältnära förkontroll och har ingen separat resultatsektion för
`aktuell_arskostnad`.

Definitionerna `policyFaltMetadata`, `PolicyRawFormValue`, `PolicyParseResultat` och
`parsaPolicyIndata` saknas helt. `KravPost.etikett`/`hjalptext` är dessutom fortsatt
valfria (`resultatkontrakt.ts:148–151`; Pythonrader 232–235), trots V22:s fail-closed-krav
att UI-metadata måste vara obligatorisk och komma från policyregistret.

Claudes uppgivna blockerare håller inte: `neptune-marketing/package.json:33` har redan
Playwright som direkt `devDependency`. V22 tillåter uttryckligen React Testing Library
**eller motsvarande**, så ett riktigt webbläsar-/DOM-test kan byggas med befintlig
infrastruktur. Att lägga till en testmiljö hade dessutom varit en normal del av den redan
godkända Batch 0-implementationen, inte ett nytt produktbeslut.

**Begärd rättning:** implementera hela V22 punkt 5–8 på den verkliga sidan, inklusive
obligatorisk metadata, strikt råparser, alla tre värdetyper plus numeriskt enumläge,
attestering och fältnära `saknadeFalt`/`ogiltigaFalt`. Lägg till V22:s riktiga sidtest med
Playwright eller annan reproducerbar DOM-miljö. Legacyfältet `falt` ska vara oförändrat.

### P1 #2 — Årskostnadsdispatchen använder inte den gemensamma argumentbyggaren och kan räkna fel energi

V22 definierar `argsFranInputs(inputs): Tariffberakningsunderlag` som enda ägare av
energi-scope och MWh-proveniens. Den implementerade funktionen är i stället privat, tar fyra
argument och returnerar `Omit<BesparingsvardeArgs, 'besparingsgrad'>`
(`energiPotential.ts:438–451`). `calcResult` räknar därför fortfarande ut scope och
proveniens före hjälparen, medan `calcResultForOnskadTyp` inte anropar hjälparen alls utan
bygger ett andra objekt manuellt (`energiPotential.ts:658–688`).

Det ger ett konkret beräkningsfel: för `energyScope === 'space_heat_excl_dhw'` skalar
`calcResult` upp angiven rumsvärme med `1 / (1 - VARMVATTEN_ANDEL)`
(`energiPotential.ts:487–548`), men årskostnadsgrenen skickar råa `inputs.energyMwh`
oförändrade vid rad 682. Samma kundindata får därmed olika totalenergi och årskostnaden
undervärderas i den nya produkten.

Dispatchen gör dessutom tariffuppslagningen före V22:s energisystemgrind, saknar de
namngivna resolverfunktionerna `stodjerAktuellArskostnad(prisar)` och
`stodjerBesparing(prisar)`, och returnerar `KalkylatorResult | ArsprodukResultat` i stället
för den beslutade diskriminerade `KalkylatorResultUnion` där legacyresultatet omsluts som
`{ typ: 'fullstandig', resultat }`. Inget test i `src/**/*test.ts` anropar
`calcResultForOnskadTyp`, så just denna nya produktkedja är inte verifierad.

**Begärd rättning:** implementera V22:s exakta delade kontrakt: exporterad
`argsFranInputs(inputs)` som ensam räknar `totalMwh` och proveniens, använd den från både
legacyberäkningen och `beraknaArsprodukt`, inför de två fail-closed-resolverfunktionerna,
kontrollera `energySystem` före tariffuppslagning och returnera den diskriminerade unionen.
Testa minst båda dispatchgrenarna, icke-fjärrvärme, unsupported tariff samt
`space_heat_excl_dhw` mot handräknad uppskalning.

### P1 #3 — Okänt band-ID blir fortfarande ett generiskt fel före den typade förkontrollen

`byggKontraktIndata` kastar ett generiskt `Error` för ett okänt nivå-ID
(`besparingsvarde.ts:213–220`). Båda publika produktvägarna anropar byggaren **före**
`forkontrolleraPolicyIndata` (`besparingsvarde.ts:426–440` och 536–544). Den nya
prispostmedvetna grenen som korrekt kan producera `{ orsak: 'okant_val' }`
(`resultatkontrakt.ts:718–753`) är därför onåbar i det verkliga produktflödet för just ett
okänt bandval; användaren får inte den avtalade `KontraktBlockerat('invalid_policy_fields')`
med ett fältnära fel.

Pythonmotsvarigheten är också bara delvis speglad:
`forkontrollera_policy_indata(policy, indata, omfattning)` tar inte `prisar`
(`resultatkontrakt.py:706–710`) och kontrollerar därför bara en eventuell statisk
`tillatna_varden`, inte den valda prispostens verkliga `nivaer[].id`. Ett okänt ID upptäcks
först senare i årsfasaden som `ValueError` (`resultatkontrakt.py:883–899`).

**Begärd rättning:** låt byggaren bygga det typade indataobjektet utan att kapa den
fältnära felkanalen; låt prispostmedveten förkontroll klassificera okänt band som
`okant_val` innan fasad/motor. Spegla prispostparametern och medlemskontrollen i Python.
Behåll motorns/fasadens oberoende fail-closed-kontroll som defense in depth. Testa hela den
publika produktentryn, inte bara byggaren och förkontrollen var för sig.

### P2 #1 — Pythonförkontrollens felorsak är inte statiskt sluten

`PolicyValideringsFel.orsak` är fortsatt annoterad som fri `str`
(`resultatkontrakt.py:700–703`) samtidigt som funktionskommentaren säger att den speglar
TypeScripts slutna `PolicyValideringsOrsak`. Detta gör stavfel eller nya, icke avtalade
orsaker typmässigt möjliga på Pythonsidan.

**Begärd rättning:** deklarera en namngiven Python-`Literal` för samma åtta orsaker som
TypeScript och använd den i både `_vardefel_for_krav` och `PolicyValideringsFel.orsak`.

## Rättningar som är godkända att bevara

- `nivaer[].id` bevaras och valideras som unika, icke-tomma ID:n; valt ID når både Python-
  och TypeScriptmotorn och kan välja den faktiska prisnivån.
- `maxvarde`/`maxVarde`, exklusivt minimum och elementvis min/max/heltal-validering är
  implementerade i både den auktoritativa statusvägen och förkontrollen.
- Python har nu byggare/förkontroll samt en sluten
  `FlodeskorrigeringVariant = Literal['golvfri', 'golvbegransad']`.
- Generatorartefakten anger åter källcommit
  `7ba9ec1b6245a72a4720f11b11beec6692af6196`; kataloghash och disposition är oförändrade.
- Rättningscommitterna är fokuserade och `git diff --check` är rent.

## Verifiering

- `.venv/bin/python -m pytest tools/tariffer/tests -q` i `enkey-agents`: **385 passed**;
  endast en sandboxrelaterad varning om pytestcache.
- `npm test -- --run` i `neptune-marketing`: **14 testfiler, 439 tester passerade**.
- `npx tsc --noEmit`: godkänd.
- `npm run build`: godkänd; byggskapade `dist`-ändringar återställdes efter kontrollen.
- `git diff --check 11f8b6e..714da6f` och `git diff --check 85aa7a1..b87ff58`:
  godkända.
- Produktreponas arbetskopior: rena efter granskningen.
- Statisk sökning: inget anrop till `calcResultForOnskadTyp` i tester eller produktsida;
  ingen `policyFaltMetadata`, `parsaPolicyIndata`, `PolicyParseResultat` eller namngiven
  capability-resolver finns.
- `package.json` och låsfilen bekräftar Playwright 1.59.1 som direkt installerad
  utvecklingsdependency.

## Nästa kontrollpunkt för Claude

Rätta endast P1/P2-punkterna ovan ovanpå de befintliga lokala committerna. Ingen tariffdata,
disposition eller aktivering får ändras. Använd befintlig Playwright-infrastruktur eller en
reproducerbar DOM-testmiljö för den verkliga sidan; detta kräver inget nytt beslut från
Robert. Skapa fokuserade lokala rättningscommits per produktrepo, kör hela testmatrisen,
typkontroll, bygge, verklig sidrendering och `git diff --check`, logga bas-/slut-HEAD och
stanna för Codex omgranskning. Ingen push.
