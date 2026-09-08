---
review_id: "2026-09-04-011"
date: "2026-09-04"
reviewer: Codex
status: changes-required
scope:
  - enkey-agents commits 0842a59 and a0d5c6e
  - neptune_academy commits 45fc11c and a9a6cb8
  - rättningar och utökad grundetapp efter granskning 2026-09-04-010
reviewed_heads:
  enkey-agents: "a0d5c6e"
  neptune_academy: "a9a6cb8"
implementation_changed: false
push_status: local-unpushed
---

# Slutkontroll av policyregister och produktgrind

## Bedömning

Claude har stängt de tidigare kraschfallen för vanliga, icke-rullande
kapacitetsbindningar och byggt den efterfrågade kedjan från policyregister via generator till
TypeScript. Produktens befintliga råvägar blockeras också när en genererad tariff verkligen
är kontraktsmarkerad. Alla ordinarie tester, typkontrollen och produktionsbygget är gröna.
Inga riktiga tariffer, policyer eller genererade produktdata har aktiverats.

Kontrollpunkten är ändå **inte godkänd för push eller nästa tariffbatch**. En sanningskonvertering
gör aktiveringsflaggan mindre strikt än kontraktet, kapacitetsvalideringen förbjuder det redan
godkända E.ON/Navirum-fallet med ett skalärt snapshot-värde, och båda språken erbjuder
fortfarande en publik funktion som returnerar en naken `Kostnad` för kontraktsmarkerade
tariffer. Dessa tre luckor behöver stängas innan grunden kan anses fail-closed.

## Fynd

### P1 — aktiveringsgrinden godtar andra sanningsvärdiga typer än exakt `true`

`generera.py:136` skickar `bool(t.get("contract_required"))` till grinden. Därmed blir bland
annat strängen `"false"`, talet `1` och icke-tomma listor eller objekt `True` innan
`kontrollera_aktiveringsgrind` får se katalogvärdet. Grinden testar därefter bara
`if not contract_required` (`policyregister.py:50–71`). Detta uppfyller inte det uttryckliga
villkoret från granskning 010 att en ny tariff endast får aktiveras när
`contract_required is True`.

Codex reproducerade på `a0d5c6e` att en påhittad katalogpost med
`contract_required: "false"` och en komplett registrerad policy genereras utan fel.

**Begärd rättning:** skicka det råa katalogvärdet till aktiveringsgrinden och kräv identitet
med booleska `True` (`is True`), alternativt validera katalogschemat strikt före anropet.
Lägg negativa tester för minst `"false"`, `1` och ett objekt/listvärde. Typannoteringen
`bool` är inte en körningskontroll.

### P1 — E.ON/Navirums godkända snapshot-indata har gjorts omöjlig

`Tariffpolicy.__post_init__` avvisar nu varje kapacitetsbindning vars `KravPost` har
`rullande=True` (`resultatkontrakt.py:180–199`), och TypeScript-spegeln gör motsvarande.
Det stänger ett tidigare serieformat kraschfall, men är striktare än den godkända
domänmodellen. Den tekniska kartläggningens v4 säger uttryckligen att E.ON/Navirums effekt är
rullande över tolv månader, samtidigt som ett enda leverantörsvärde ska kunna ge
`snapshot/complete` och prissättas (`teknisk-kartlaggning-28-tariffer.md:23, 77, 93`).

Codex reproducerade att en sådan E.ON-liknande policy nu avvisas redan vid konstruktion,
oavsett att den faktiska `IndataPost.varde` som ska användas är ett enda skalärt värde.

**Begärd rättning:** tillåt att ett rullande krav är kapacitetsbindning när den faktiska
årsindatan är skalär; statusen ska då förbli högst `snapshot`, precis som v4 anger. Om den
faktiska indatan är en serie och ingen tariffspecifik reduceringsregel finns ska beräkningen
blockeras eller ge ett tydligt strukturfel före kostnadsanropet. Lägg speglade positiva tester
för skalärt E.ON-snapshot och negativa tester för en oreducerad serie.

### P1 — kontraktsfasaden kan fortfarande kringgås via en exporterad kostnadsfunktion

TypeScripts sentinel exporteras inte längre, vilket är en förbättring. Däremot exporteras
`arskostnadForKontraktfasad` från `fjarrvarme.ts:794`; ett valfritt produktanrop kan importera
den och få en naken `Kostnad` utan `Resultatstatus`. Python erbjuder på samma sätt den
publikt namngivna `arskostnad_for_kontraktfasad` i `faktura.py:689`. Codex anropade den
direkt med ett kontraktsmarkerat prisobjekt och fick en `Kostnad` utan statuskontroll.

Funktionernas kommentarer om "enda avsedda konsumenten" är en konvention, inte den
strukturella gräns som granskning 010 begärde. Den offentliga kontraktsfasaden ska vara
`berakna_arskostnad_med_kontrakt`/`beraknaArskostnadMedKontrakt`, som returnerar både status
och kostnad och vägrar räkna när resultatet är blockerat.

**Begärd rättning:** gör den nakna motorn och dess passersedel verkligt interna för
resultatkontraktsmodulen, exempelvis genom samlokalisering eller en intern modul som inte
exporteras till produktkonsumenter. Om språkens modulmodell kräver en separat hjälpfunktion,
gör den privat namngiven och lägg ett import-/arkitekturtest som endast tillåter anrop från
resultatkontraktsmodulen. Ett vanligt produktimport ska inte kunna få en kontraktsmarkerad
`Kostnad` utan `Resultatstatus`.

### P2 — korsrepo-testet är fortfarande beroende av en viss lokal checkout

Den direkta fixturejämförelsen är nu obligatorisk och verifierar faktiskt båda kopiorna i
Roberts nuvarande kataloglayout. Det är bättre än två oberoende hashkonstanter. Ett fristående
repo saknar dock motparten och fallerar om inte `ELLEN_FRISTAENDE_KLON=1` sätts; ingen
versionsstyrd CI-konfiguration i de granskade repona checkar ut motparten eller definierar
undantaget.

Detta är inte huvudblockeraren för domänkontraktet, men kontrollen är ännu inte portabel.
Dokumentera en konfigurerbar motpartssökväg och hur CI ska checka ut båda repona, eller flytta
fixturen till ett gemensamt versionsstyrt testpaket. Opt-out ska användas uttryckligt för en
fristående klon, inte vara den enda vägen till en grön vanlig CI-körning.

## Godkända delar i denna runda

- prisobjekt med kapacitetsnivå kräver nu kapacitetsbindning och ett prisobjekt utan
  kapacitetsdel får inte ha en,
- bindningen måste vara årsrelevant och serieformat motorfält hoppas inte längre över tyst,
- ett tariff-ID-indexerat, för närvarande tomt policyregister och ett uttryckligt legacy-set
  finns,
- generatorn blockerar huvudfallet där en ny tariff saknar markör, policy eller matchande ID,
- policydata serialiseras till genererad TypeScript och läses av `policyFranGenererad`,
- produktens befintliga råvägar har testats att kasta `KontraktKravs` för en markerad tariff,
- tidigare numerik-, datum- och kvalitetsrättningar är fortsatt gröna,
- inga riktiga tariffer, policyer eller genererade produktdata har aktiverats.

## Avgränsad rättningsbeställning till Claude

Rätta endast grundetappen och håll commitserierna lokala:

1. gör `contract_required` strikt boolesk och exakt `True` genom hela katalog-/generatorgrinden,
2. återställ E.ON/Navirums skalära rullande kapacitetsfall som `snapshot/complete`, men
   blockera en faktisk serie utan reduceringsregel,
3. ta bort den publikt importerbara vägen till naken `Kostnad` för kontraktsmarkerade
   tariffer,
4. lägg speglade negativa och positiva tester för ovanstående,
5. dokumentera eller gör korsrepojämförelsen portabel för vanlig CI,
6. kör hela Python- och TypeScript-sviten, `tsc --noEmit` och produktionsbygget.

Aktivera inga tariffer och rör inte Familj 4, Telge, E.ON/Navirum, Sundsvall Matfors eller
Vattenfalls tariffdata. Redovisa nya lokala commit-hashar och invänta ny Codex-kontroll före
push.

## Utförda kontroller

- `enkey-agents@a0d5c6e`: 281/281 tariff-pytest passerar i projektets `.venv`.
- `neptune_academy@a9a6cb8`: 303/303 Vitest passerar.
- `npx tsc --noEmit`: passerar.
- `npm run eval:build`: passerar; endast befintlig varning om stor bundle.
- `git diff --check`: rent för båda granskade commitkedjorna.
- Båda implementationsarbetskopiorna är rena; committerna är lokala och opushade.
- Riktat Pythonanrop bekräftade att `contract_required: "false"` passerar generatorgrinden.
- Riktat policybygge bekräftade att en rullande skalär kapacitetsmodell avvisas redan vid
  konstruktion.
- Direkt anrop till `arskostnad_for_kontraktfasad` returnerade en naken `Kostnad` för ett
  kontraktsmarkerat prisobjekt.
- Den direkta fixturejämförelsen passerar i Roberts checkout; ingen `.github`-konfiguration
  hittades som gör kontrollen portabel till en vanlig fristående CI-checkout.

Codex ändrade ingen implementation, tariffdata, commit eller push under granskningen.
