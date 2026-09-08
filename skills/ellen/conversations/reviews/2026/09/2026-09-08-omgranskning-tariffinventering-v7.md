---
review_id: "2026-09-08-007"
date: "2026-09-08"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v7.md
  - Fjarrvarmetariffer/batchplan-v7.md
  - skills commit f0f3ee716b39af062d6e1af706b44fbf64e8af5e
reviewed_heads:
  skills: "f0f3ee716b39af062d6e1af706b44fbf64e8af5e"
  enkey-agents: "fd8f8da3eb17cce638dc2f3370efa027c2afcad6"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-08-006"
---

# Omgranskning av tariffinventering v7 och batchplan v7

## Bedömning

V7 gör flera riktiga framsteg. Kontrollmängden är fortsatt komplett och mekaniskt
sammanhängande: 78 unika bastariffer, 14 variant-ID:n och fördelningen 7 implementerade,
55 redo samt 30 blockerade. Bandtabellen innehåller exakt de 42 av 45 ready-bastariffer
som katalogen markerar med `supplier_confirmed_band_id_required`, utan dubbletter eller
utelämnade ID:n. Band-ID:t ska nu välja prisraden direkt, Jönköpings accessavgift har fått
rätt disposition och request-planen har ett begripligt tariff-ID-spår.

Planen är ändå inte implementeringsklar. Umeå filtreras fortfarande bort innan den nya
kompositgrinden kan köras. Band-ID:t har lagts till genom att generellt vidga `Varde` till
sträng, men dagens validerare, årsfasad och produktadapter är numeriska och kan inte bära
det till motorn. Stockholm-adapterposten nås inte i dagens generatorordning, anger ingen
produktdispatch och årsfasaden kan varken validera eller använda de utlovade
månadsserierna. Kraftringens diskriminator och Jönköpings tillåtna värden saknar också
domänväg.

Det krävs därför en avgränsad V8-rättning av planeringsdokumenten. Ingen produktkod,
tariffdata, aktivering eller push är godkänd.

## P1-fynd

### P1 — Umeås efterkontroll kan aldrig öppna en tariff som redan filtrerats bort

V7 §6a.3 säger samtidigt att:

- den nakna `grind()` alltid ska avvisa `post_multiplier` och att Umeå aldrig passerar
  steg 2 ensam; och
- `kontrollera_kompositgrind(tariff, policy)` ska köras **efter** steg 2 och 3, aldrig i
  stället för dem.

Dagens generator anropar först `godkanda(katalog)`, som returnerar endast rader där
`grind()` gav `None`. En senare kontroll kan inte återinföra en rad som redan har
filtrerats bort. Reproduktion med Umeås status och issues neutraliserade gav
`grind(...) == "kapacitetsformel med multiplikator"` och noll rader från `godkanda()`.

Kompositgrindens angivna signatur tar dessutom bara tariff och policy. Den kan kontrollera
att en B-bindning är deklarerad, men kan inte kontrollera V7:s negativa körningsfall
`B=14`, eftersom faktisk `IndataPost` inte finns vid aktivering. Det värdet hör hemma i
`harled_resultatstatus`/kontraktsfasaden via `minvarde` och `maxvarde`, inte i en
aktiveringsfunktion med två statiska argument.

**Begärd rättning:** välj en körbar ordning. Rekommenderat är en sammansatt
aktiveringsfunktion som får tariff och verifierad policy innan slutlig filtrering, samlar
grindens strukturella fynd och får konsumera **endast** fyndet för en multiplikator som
har en explicit, motorstödd och annual-bunden capability. Alla andra fynd och varje okänd
`post_multiplier` ska fortsätta blockera. Alternativt kan `grind` få ett strikt typat
capability-argument med samma semantik. Visa i pseudokod exakt var funktionen anropas från
`godkanda()`/generatorn. Testa att Umeå genereras med rätt policy, att samma rad stoppas
utan bindningen och att en annan tariff med okänd multiplikator fortsatt stoppas. Flytta
`B=14`-testet till indatakontraktet där värdet faktiskt finns.

### P1 — bandkontraktet är inte ett säkert end-to-end-kontrakt

V7 §6a.2 föreslår `Varde = float | Sequence[float] | str`. Det räcker inte och skulle
försvaga alla befintliga numeriska fält:

- Python `_validera_varde` och TypeScript `valideraVarde` avvisar i dag varje sträng;
- `berakna_arskostnad_med_kontrakt` gör `float(post.varde)` för varje relevant skalär och
  TypeScript lägger varje sådan post i `Record<string, number>`;
- kalkylatorsidan konverterar alla dynamiska fält med `parseFloat`;
- `BesparingsvardeArgs.falt`/`KalkylatorInputs.falt` är `Record<string, number>`;
- `beraknaBesparingsvardeKontrakt` skapar i dag `IndataPost` endast för
  `kapacitetBindning`. Varje policy med band, flöde, temperatur, B eller annat extra krav
  blir därför `blocked` och därefter felklassad som ett konfigurationsfel.

Band-ID behöver en diskriminerad värdetyp, exempelvis `KravPost.vardetyp = "number" |
"number_series" | "band_id"`, inte en global union utan fältspecifik validering. Numeriska
krav ska fortsätta avvisa strängar; bandkravet ska kräva en icke-tom sträng, förbjuda
`minvarde`/`maxvarde`/`heltal` och aldrig hamna i motorns numeriska `falt`-dictionary.
Bandbindningen ska läsas separat och endast det validerade ID:t skickas som
`vald_niva_id`. Dubbletter i `nivaer[].id`, saknat ID, tom sträng, okänt ID, tal som band-ID
och sträng som numeriskt fält ska avvisas i båda språk.

Det saknas samtidigt en gemensam produktingång för **alla** policykrav. Produktadaptern
måste skapa `IndataPost` för exakt de policydeklarerade fälten, med rätt typ och proveniens,
och föra dem från `KalkylatorPage` via `energiPotential` och `besparingsvarde` till
kontraktsfasaden. Extra, ovaliderade fält får inte nå motorn. Detta är grundarbete före
första tariffbatchen, inte något som Sandvikens nuvarande kapacitets-only-adapter redan
löser.

Batchplanen motsäger sin egen 42-radstabell. De 41 katalograder som faktiskt aktiveras med
bandkrav fördelas på batch 1 (6), 3 (9), 4 (4), 5a (8), 5b (6), 5c (7) och Borås i batch 6
(1). Trots det nämner ingressen endast 5a/5b/3/4, batch 1 saknar band helt, batch 4 lägger
det bara på Umeå och 5a/5b kallar det ett extra fält bara för C4/Borlänge. De åtta
E.ON/Navirum-varianterna i 3b ärver samma bandkrav från sina bastariffer men listar bara
effekt, `Tf` och flöde.

**Begärd rättning:** lägg en uttrycklig grundbatch före batch 1 för värdetyp, bindning,
serialisering, motorparameter, produkt-API och UI. Ange de verkliga filerna i båda repon:
minst `resultatkontrakt.py`/`.ts`, `katalog.py`, `faktura.py`/`fjarrvarme.ts`,
`generera.py`, `besparingsvarde.ts`, `energiPotential.ts`, `KalkylatorPage.tsx`, genererad
data och tester. Synkronisera sedan obligatorisk indata, filer och testfall i samtliga sju
berörda basbatcher och i 3b. Stockholm är den 42:a men exkluderas som beskrivet.

### P1 — Stockholm har varken nåbar dedupliceringskontroll eller årsdispatch

V7:s `ADAPTERREGISTER` kontrolleras enligt texten när generatorn behandlar en
katalogtariff. Dagens `bygg_ts_fran_katalog()` gör däremot först
`ur_katalogen = godkanda(katalog)` och itererar därefter bara dessa rader. Stockholm-raden
förblir `utreds` och stoppas dessutom av `energiform`; den når alltså aldrig en
adapterkontroll inne i den nuvarande katalogloopen. Registret måste valideras mot den råa
katalogmängden före filtrering eller i en separat fail-closed preflight.

`AdapterEntry` anger bara `provider_id`, `tariff_id` och policytäckning. Den anger inte
vilken årsadapter produktdispatch ska anropa. Leverantörsfilens prispost står kvar i
`aktiveringslage: "validated"`; generatorn bifogar visserligen policyn, men sätter inte
`_kraver_kontrakt`. `kontraktsgatadPolicy()` returnerar då `undefined` och dagens
`beraknaBesparingsvarde` fortsätter på legacyvägen. Att lägga `annual_forward` i policyn
ändrar alltså inte årsberäkningen.

Årsindatan är inte heller representerad. Den befintliga årsfasaden tar
`mwh_kallt_per_manad` och ett enda `returtemp_c` som fria argument, inte från de validerade
policybindningarna. Ett returtemperaturtal används för alla vintermånader. De befintliga
Stockholm-kraven är månadsvisa skalärer, och `Tariffpolicy` förbjuder dubbla
`kravda_falt.nyckel`. V7:s formulering om nya annual-krav för "samma tre fält" anger därför
varken unika nycklar, en typad månadsserie, exakt månads-/längdvalidering eller hur värdena
binds till motorns två fria argument.

**Begärd rättning:** specificera hela kedjan:

1. validera varje adapterpost mot den råa katalogen, ett existerande `provider_id`, ett
   verkligt tariff-ID hos just den leverantören, rätt policytäckning och en känd
   årsadapter innan `godkanda()` filtrerar;
2. lägg en typad adapter-/dispatch-diskriminator i posten och visa hur
   `beraknaBesparingsvarde` väljer den utan att kräva `annual_inverse`;
3. välj en representerbar annual-indatamodell för 12 kalla energivärden och 5
   månadsreturtemperaturer, med full månadstäckning, unika nycklar och statiska bindningar;
4. låt endast de validerade värdena nå en motorväg som faktiskt kan använda
   returtemperatur per månad; inga parallella fria argument får kringgå policyn;
5. testa saknad/stale mapping, fel provider/tariff, policytäckning utan adapter, saknade
   månader, oförändrad `monthly_invoice` och exakt ett Stockholm-val i UI.

V7 §6 ska samtidigt säga **44 nya katalogpolicyer plus utökning av den befintliga
Stockholm-policyn**, inte att samtliga 45 behöver en ny registerpost.

### P1 — Kraftringens regelvariant når inte motorn och tappas i TypeScript

V7 inför `kapacitet_bindning_variant`, men fältet saknas i tabellen som påstås lista varje
ny Python-/JSON-/TypeScript-mappning. Det finns inte heller någon beskriven väg från
`Tariffpolicy` till justeringsmotorn: den nuvarande fasaden skickar bara numeriska `falt`,
och `faktura.py`/`fjarrvarme.ts` får inte policyn. Motorn kan därför inte grena på den
föreslagna strängdiskriminatorn. Namnet antyder dessutom kapacitetsbindning trots att
fältet väljer variant av `supply_temperature_adjusted_flow`.

**Begärd rättning:** ge fältet ett domänriktigt namn, en exakt Python-/TypeScript-literal,
allow-list-validering, JSON-mappning och en typad motorparameter. Korskontrollera att
diskriminatorn krävs exakt när tariffen har den aktuella justeringstypen och förbjuds eller
ignoreras säkert annars. Okänd/saknad variant ska blockera före kostnadsberäkning. Lägg
tester för båda varianterna, serialiseringsrundtur och direkt fasadanrop.

### P1 — Jönköpings fyrvärdesval saknar domänmässig allow-list

Beslutet 0/10/25/50 kr/mån utan default är rätt återgivet, men V7 anger bara UI-val och
en ny justeringstyp. Dagens `KravPost` kan uttrycka min, max och heltal, inte en diskret
mängd. Ett direkt API-/fasadanrop kan därför skicka exempelvis 17 kr/mån och få en
beräkning trots löftet att okänt värde ska blockera. UI-begränsning är inte en
domängrind, och värdet 0 måste dessutom skiljas från saknad indata.

**Begärd rättning:** lägg en deklarativ `tillatna_varden`-/enumregel i kontraktet eller en
likvärdig typad domänregel, serialiserad och validerad i båda språk. Testa exakt fyra
giltiga värden, tomt/saknat, 17, negativa/icke-ändliga värden och att uttryckligt 0 inte
tolkas som frånvaro. Lägg kontraktsfilerna i batch 5b:s fillista.

## P2-fynd

- V7 §6 rad 1632 säger fortfarande att samtliga 45 ready-rader kräver en **ny**
  policyregisterpost. Det motsäger §6a.4 och batch 7, där Stockholms befintliga policy ska
  utökas. Rätt antal är 44 nya katalogpolicyer + 1 utökad leverantörsfilspolicy.
- §7 återanvänder det borttagna namnet `oppna_tariff_ider()` i sammanfattningen trots att
  den valda funktionen heter `blockerade_tariff_ider()`. Samma avsnitt säger först att
  varje request får `tariff_ids`, men planen sätter det bara på R03/R14 och låter fyra
  äldre medlemsomfattande requests sakna fältet. Beskriv en enda faktisk JSON-form.
- Batch 4 använder fortfarande den icke existerande förkortningen
  `justeringar.py/.ts`; TypeScript-logiken ligger inline i `fjarrvarme.ts`.
- Batchsammanfattningens additiva uttryck på rad 470 summerar till 54 därför att batch 7
  saknas ur uttrycket. Räkningsnoten nedanför är korrekt och ger 55; gör även den första
  raden självbärande.
- V7 levererades i commit `f0f3ee7` med verifierbar committid 16:32:28, men session och
  överlämning anger 16:10 och sessionsloggens 16:10-rad ligger efter äldre rader i en annars
  omvänt kronologisk ändringslogg. Nästa leverans ska logga den verkliga committen och
  tiden utan att skriva om äldre historik.

## Verifieringar

- `skills@f0f3ee7` ändrar endast dokumentation och konversationslogg; ingen produktkod,
  tariffdata eller genererad frontendfil ingår.
- `git diff --check 058ffb4..f0f3ee7` är rent. Lokal `main` är åtta commits före
  `origin/main`; V7 är inte godkänd för push.
- Inventeringen har 78 unika produktrubriker, preflighttabellen 45 unika ready-ID:n och
  varianttabellen 14 ID:n. Bandtabellen har 42 unika ID:n och matchar exakt de 42
  preflight-ID:n vars katalograd har `supplier_confirmed_band_id_required`. Alla berörda
  katalog-ID:n är strängar.
- Relativa länkar i de ändrade V7- och konversationsdokumenten pekar på befintliga filer.
- `POLICYREGISTER`, `katalog.py`, `generera.py`, `resultatkontrakt.py`, `faktura.py`,
  TypeScript-spegeln, produktadaptern och kalkylatorsidan lästes på de pinnade
  produkt-HEAD:arna ovan.
- En skrivskyddad reproduktion mot Umeå gav grindorsaken
  `kapacitetsformel med multiplikator` och noll godkända rader. Ett strängformat
  `IndataPost.varde="1"` avvisades av dagens kontrakt som "värdet måste vara ett ändligt
  tal".
- Inga fulla produkttester kördes eftersom V7 endast ändrar dokumentation.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v8.md` och `batchplan-v8.md`; ändra inte V7 i efterhand.
2. Lägg en grundbatch före tariffbatcherna för ett diskriminerat policyindata- och
   produkt-API som stödjer numerik, månadsserier och band-ID fail-closed genom Python,
   generering, TypeScript, produktdispatch och UI.
3. Gör Umeås aktiveringsordning körbar och skilj statisk capability-kontroll från faktisk
   B-värdesvalidering.
4. Gör Stockholm-adaptern nåbar före katalogfiltreringen, ge den verklig årsdispatch och
   bind 12+5 månadsdata till motorn utan fria bypassargument.
5. Slutför Kraftringens typade diskriminator och Jönköpings diskreta allow-list genom hela
   kontrakts-/serialiseringskedjan.
6. Synkronisera obligatorisk bandindata och verkliga fillistor för alla 41 aktiverade
   bandbastariffer samt de åtta E.ON/Navirum-varianterna; rätta de mindre P2-
   motsägelserna.
7. Behåll dispositionerna 7/55/30 om ingen sakstatus ändras; inga nya produktbeslut från
   Robert behövs för dessa tekniska rättningar.
8. Skapa en fokuserad lokal dokumentationscommit ovanpå `f0f3ee7`, logga verklig hash/tid
   och stanna för ny Codex-granskning. Ändra ingen produktkod eller tariffdata och pusha
   inte.
