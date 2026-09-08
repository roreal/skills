---
review_id: "2026-09-08-005"
date: "2026-09-08"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v5.md
  - Fjarrvarmetariffer/batchplan-v5.md
  - skills commit ce53f75f5f91bfc12639ae9d7cd3858d52a67e3d
reviewed_heads:
  skills: "ce53f75f5f91bfc12639ae9d7cd3858d52a67e3d"
  enkey-agents: "fd8f8da3eb17cce638dc2f3370efa027c2afcad6"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-08-004"
---

# Omgranskning av tariffinventering v5 och batchplan v5

## Bedömning

V5 är ett tydligt steg framåt. Dispositionsräkningen är fortsatt korrekt: 78 katalograder
fördelas på 7 implementerade, 45 redo och 26 blockerade; de 14 separata varianterna
fördelas på 9 redo och 5 blockerade. Preflighttabellen innehåller exakt 45 unika ready-ID:n,
alla primärkällor är direkt utskrivna och de tidigare absoluta konversationslänkarna är
rättade. Committen `ce53f75` är avgränsad till dokumentation och
`git diff --check HEAD^ HEAD` är rent.

Kontrollpunkten kan ändå inte godkännas för implementation. Den rapporterade
`45/45`-körningen provar en simulerad kataloggrind, inte den fulla aktiveringskedjan. Flera
av de åtgärder som sägs få grinden att passera kan inte uttryckas i dagens kontrakt eller
generator: leverantörsvalt band saknar motorbindning, tariffvisa informationsförfrågningar
saknar datastruktur, Umeås multiplikator saknar typad bindning och Stockholm-vägen skulle
skapa en andra post för samma produkt. Batch 2 för Sundsvall skulle dessutom stoppas av
generatorns kontraktsgrind trots att den passerar `grind()`.

Det behövs därför en fokuserad V6-rättning av aktiveringskontraktet. Ingen produktkod,
tariffdata eller push godkänns ännu.

## Fynd

### P1 — `45/45 grind()` är inte en reproducerbar aktiveringspreflight

V5 anger att `investigation.status` simulerades löst och att planerade rättningar
applicerades i minnet, men inget körbart skript, ingen patch och ingen exakt mutationslista
finns sparad. Dagens `grind(tariff, utredda)` känner bara till tariffposten och en mängd
medlems-ID:n. Den har ingen åtkomst till policyregistret, någon adapterregistrering,
leverantörsvalt band eller Umeås framtida multiplikatorbindning. Tabellen kan därför inte
bevisa formuleringar som `grind() None via adapter`.

Alla 45 ready-rader redovisas fortfarande med `investigation.status: utreds`. V5 beskriver
inte den verkliga tariffvisa övergången (`lost`, `null` eller annan beslutad representation),
utan lyfter bara statusen i simuleringen. Även efter ett grindpass kräver generatorn
`contract_required: true` och en komplett `Tariffpolicy` för varje ny katalogtariff utanför
de sex frysta legacy-undantagen. Batch 2 säger tvärtom att Sundsvall Indal ska gå på
legacy-vägen utan kontrakt; tariff-ID:t finns inte i `LEGACY_UNDANTAGNA_TARIFF_ID`, så
`bygg_ts_fran_katalog()` skulle kasta.

**Begärd rättning:** ersätt grind-only-kriteriet med en reproducerbar
aktiveringspreflight för varje ready-ID: verklig utredningsstatus och request-scope,
`grind()`, generatorns kontraktsgrind med verkligt policyregister, genererat unikt
leverantörs-ID samt ett minimalt giltigt `annual_forward`-anrop. Saknad, felaktig och
gränsnära indata ska blockeras. Spara kommandot/skriptet eller ett entydigt testkontrakt så
resultatet kan köras om. De 26 blockerade basraderna och 5 blockerade varianterna ska
fortsatt vara blockerade av den sammansatta kontrollen, inte bara av mänsklig text.

### P1 — leverantörsvalt effektband finns inte i produktkontraktet

Katalogen anger `band_selection: supplier_confirmed_band_id_required`, men
`Tariffpolicy` och `IndataPost` kan bara binda ett numeriskt kapacitetsvärde. `till_prisar()`
översätter källintervallen till numeriska nivåer och `_niva()` väljer automatiskt första
band vars maxgräns täcker talet. `band_selection` når aldrig motorn.

En läsbar gränsprovning mot dagens kod bekräftar felet:

- Borlänge 501 kW väljs automatiskt in i band 5 trots att källan skriver `>501` och V5
  kräver leverantörens gruppbesked.
- C4 500 kW väljs automatiskt in i band 6 trots att exakt 500 kW är det uttryckligen
  osäkra gränsfallet.
- Falu ytterorter 501 kW kastar, vilket är fail-closed, men kontraktet saknar ett
  deklarerat maxvärde och planen anger inte hur UI/fasad ska stoppa värdet före motorn.

**Begärd rättning:** välj en faktisk, typad väg. Antingen införs en
`supplier_confirmed_band_id`-bindning som valideras mot katalogens band och används skilt
från det numeriska debiteringsunderlaget, eller så blockeras de osäkra exakta gränserna
tariffspecifikt. Falu behöver ett maskinellt maxkrav på 500 kW; dagens `KravPost` har bara
`minvarde` och `heltal`. Ange Python-, TypeScript-, generator-, UI- och testfiler för den
valda lösningen. Att endast normalisera issue-texten får inte öppna produkten.

### P1 — R03/R14 kan inte delas tariffvis med dagens datastruktur

`remaining_information_requests` bär `member_ids`, och `utredda_medlemmar()` reducerar
dem till en mängd medlems-ID:n. `grind()` frågar endast om `tariff.member_id` finns i den
mängden. Därför kan dagens kod inte låta Mälarenergi 2–4 lägenheter eller Sundsvall Indal
passera samtidigt som en syskontariff hos samma medlem behåller request-blockeringen.
Formuleringen "omskopa ... eller lägg till `tariff_ids`" lämnar själva kontraktet
obestämt.

**Begärd rättning:** välj en representation och följ den genom JSON-schema,
`utredda_medlemmar`/ersättningsfunktion, `grind`, tester och dokumentation. Det naturliga
alternativet är att grinden bedömer tariffens egna `investigation.request_ids` mot öppna
request-ID:n eller att request-posten får verifierade `tariff_ids`; i båda fallen ska
ready-syskonet passera och de namngivna blockerade syskonen stanna. Använd samma
representation för samtliga request-livscykler och ta bort "eller" ur arbetsordern.

### P1 — Umeås B-faktor saknar komplett typad data- och valideringsväg

Valet att ta leverantörens redan beräknade `B` i stället för att gissa normalårskorrigerat
`U` är sakligt rätt. Men `Tariffpolicy` har ingen multiplikatorbindning, `grind()` har
ingen policyparameter och batchens fillista utelämnar kontraktsschemat där den nya
bindningen måste definieras och serialiseras. V5 anger inte heller ett tillåtet intervall;
dagens kravmodell saknar maxvärde, så exempelvis `B = 14` skulle kunna passera som ett
ändligt tal och ge grovt fel årskostnad.

**Begärd rättning:** specificera ett dedikerat bindningsfält genom Python- och
TypeScript-kontrakt, generatorns policyserialisering, motor och UI. Validera B mot det
publicerade möjliga intervallet och blockera saknat/ogiltigt värde. Testa leverantörsvärden
vid och mellan giltiga gränser; kalla inte testen "U-intervall" när motorn uttryckligen
inte ska räkna U. Grinden får bara öppna Umeå när den verifierade bindningen verkligen
finns, inte via ett allmänt undantag för varje `post_multiplier`.

### P1 — Stockholm-planen har två källor för samma produkt och ingen säker adaptergrind

Den redan verifierade leverantörsfilen använder leverantörs-ID `stockholm-exergi` och
tariff-ID `stockholm-exergi-2026`. Om katalograden aktiveras skapar generatorns stabila
ID-regel i stället `stockholm-exergi-stockholm-exergi-normal`. Resultatet blir två val för
samma normalprodukt, vilket bryter inventeringens egen dedupliceringsregel.

Det finns inte heller någon adapterregistrering som `grind()` kan kontrollera. Ett
hårdkodat katalog-ID-undantag för energiformen skulle därför kunna öppna raden utan att
årsadapter och policy faktiskt finns. Den befintliga Stockholm-policyn täcker endast
`monthly_invoice`; dess tre krav gäller `monthly` och har en annan skalär
månadssemantik än de årsserier V5 beskriver.

**Begärd rättning:** välj exakt en produktionskälla. Rekommenderad väg är att utöka den
befintliga leverantörsfilens `stockholm-exergi-2026` med en separat, typad
`annual_forward`-adapter och låta katalogdubbletten förbli deduplicerat exkluderad. Om
katalogvägen väljs måste den atomärt ersätta leverantörsfilsposten, bevara publikt ID och
sparad-state-kompatibilitet samt bevisa att endast ett UI-val genereras. Använd ett
allowlistat adapterregister som både aktiveringsgrind och generator verifierar; inget rått
ID-undantag i `katalog.py`.

## P2-fynd

- Preflighttabellen säger `SPLITTA R10`, medan §7 säger att R10 tas bort. Falu-raden säger
  samtidigt att R15 ska splittras och tas bort. Använd en enda livscykel per request.
- Batcharnas fillistor omsätter inte konsekvent §7: bland annat saknas R11 i batch 1,
  R06/R10 i batch 3, R13 i batch 5a och R03 i batch 5c.
- `katalog.ts` finns inte i produktrepona. TypeScript-data genereras från Pythonkatalogen;
  den faktiska frontendmotorn heter `fjarrvarme.ts` och kontraktet
  `resultatkontrakt.ts`. Ersätt även den oklara förkortningen `justeringar.py/.ts` med de
  verkliga filerna `justeringar.py` och `adjustments.ts`.
- V5-loggen anger leverans `15:40:00`, men committen som redan innehåller samma logg är
  skapad `14:58:36`; vid kontrollen var lokal tid `15:14`. Leveranstiden är därför
  omöjlig. Rätta front matter/leveransrubrik och lägg en daterad korrigering utan att
  skriva om den äldre ändringsloggsraden i efterhand.

## Verifieringar

- Commit `ce53f75` innehåller endast åtta dokumentfiler; ingen produktkod, tariffdata eller
  genererad frontendfil är ändrad.
- `git diff --check HEAD^ HEAD` är rent. Skills-HEAD ligger fem commits före
  `origin/main` (`62181a1`) och är inte pushad.
- 78 katalogrubriker och 14 variant-ID:n är fortsatt fullständigt räknade; 45
  preflightrader är unika och motsvarar ready-mängden.
- `grind()` och generator-/policykoden lästes på
  `enkey-agents@fd8f8da`; produktkontraktet lästes på
  `neptune_academy@f1df177`.
- Gränsprovet kördes med Python 3.13 mot verklig katalog och motor: Borlänge 501 → band 5,
  C4 500 → band 6, Falu ytterorter 501 → `ValueError`.
- Generatorns ID-härledning kördes mot Stockholm-raden och gav
  `stockholm-exergi-stockholm-exergi-normal`, skilt från befintliga
  `stockholm-exergi`.
- Inga fulla produkttester kördes eftersom leveransen bara ändrar dokumentation.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v6.md` och `batchplan-v6.md`; ändra inte V5 i efterhand.
2. Ersätt den icke reproducerbara grind-only-preflighten med den sammansatta
   aktiveringspreflighten ovan, inklusive verklig utredningsstatus, requests, policy,
   generator, unikt produkt-ID och minimalt årsberäkningsfall.
3. Specificera och testa en riktig band-ID-/gränsmodell för Borlänge, C4, Falu och andra
   tariffer som kräver leverantörsbekräftat band.
4. Välj och implementeringsspecificera ett enda tariffvist request-scope för R03/R14 och
   samtliga övriga request-livscykler.
5. Slutför Umeås typade B-bindning med min/maxvalidering och fail-closed motorgrind.
6. Deduplicera Stockholm till en produktionskälla och bind årsadaptern strukturellt till
   den befintliga produkten eller genom en atomär migration.
7. Rätta P2-motsägelser, verkliga filnamn och leveranstid.
8. Skapa en fokuserad lokal dokumentationscommit ovanpå `ce53f75` och stanna för ny
   Codex-granskning. Ändra ingen produktkod eller tariffdata och pusha inte.
