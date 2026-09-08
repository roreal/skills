---
review_id: "2026-09-08-009"
date: "2026-09-08"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v9.md
  - Fjarrvarmetariffer/batchplan-v9.md
  - skills commit 2cfa3be0c85e49f05b0724dad7f8503f3d2dbc11
reviewed_heads:
  skills: "2cfa3be0c85e49f05b0724dad7f8503f3d2dbc11"
  enkey-agents: "fd8f8da3eb17cce638dc2f3370efa027c2afcad6"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-08-008"
---

# Omgranskning av tariffinventering v9 och batchplan v9

## Bedömning

V9 löser flera av V8-granskningens viktigaste sakfrågor. Umeås sammansatta grind gör nu
ett säkert andra pass där bara det redan kvitterade `post_multiplier`-fyndet neutraliseras.
Räkningen skiljer korrekt 43 nakna grindpassager, Umeå genom den sammansatta grinden och
Stockholm genom leverantörsfilsvägen. Stockholms årsindata är konsekvent beskriven som två
serier med 12 respektive 5 värden, statiska bindningar och annual-omfattning på samma
effektpost. Besparingsvärderingen stoppas också korrekt när det saknas en verifierad regel
för kallenergins efterläge. Kraftringens och Jönköpings tidigare lösningar är bevarade och
fördelningen 7 implementerade, 55 redo och 30 blockerade av 92 räknade enheter hänger ihop.

Planen är ändå inte implementeringsklar. Batch 0:s angivna DTO kan inte transportera
`number_series`; metadatafunktionen saknar både prisposten som bandalternativen finns i och
en definierad källa till etikett/hjälptext. Den skulle dessutom rendera fel omfattning och
dubblera kapacitetsfältet. Ogiltig kundindata klassas fortfarande som ett internt
kontraktsfel, trots att V8 uttryckligen krävde en egen användarfelsväg. Stockholm sägs kunna
visa aktuell årskostnad, men kalkylatorns enda produktentry fortsätter till
besparingsfunktionen som V9 samtidigt kräver ska kasta. Adapterpreflighten är fortfarande
en skiss med `pass`, globala register och en motsägelsefull tidsbaserad undantagsregel.

Det krävs därför en avgränsad V10-rättning av planeringsdokumenten. Ingen produktkod,
tariffdata, aktivering eller push är godkänd.

## P1-fynd

### P1 — produkt-DTO:n och `IndataPost` är fortfarande inte ett sammanhängande typkontrakt

V9 §6a.2 säger att formulärets `Record<string, string>` ska föras oförändrat genom
`KalkylatorInputs.falt` och `BesparingsvardeArgs.falt`, och att ingen ändring behövs där.
Det motsäger den verkliga koden och V8-granskningens uttryckliga fynd:

- `KalkylatorPage.tsx` konverterar råsträngarna till `Record<string, number>` med
  `parseFloat` före `calcResult`;
- `KalkylatorInputs.falt` och `BesparingsvardeArgs.falt` är fortfarande
  `Record<string, number>`;
- V9:s egen föreslagna `byggIndataFranPolicy` tar
  `Record<string, string | number>`, som inte kan bära en talserie alls.

Påståendet att serien lämnas "ospridd" anger varken representation eller en typ som kan
kompilera. Det utlovade end-to-end-testet med number + band-ID + enum + serie kan därför
inte skrivas mot de föreslagna signaturerna.

Även formuleringen "genuint diskriminerad värdeunion" är för stark. V9 vidgar den globala
aliasen på `IndataPost.varde` till `number | readonly number[] | string`, medan
diskriminatorn ligger på en separat `KravPost` som slås upp först vid runtime. TypeScript
tillåter därmed fortfarande att varje `IndataPost` konstrueras med vilken av de tre
värdeformerna som helst. Runtime-korsvalideringen är nödvändig och bra, men detta är inte
en diskriminerad `IndataPost`-union i typsystemet.

**Begärd rättning:** välj och skriv ut en enda produkt-DTO, exempelvis
`PolicyInputValue = number | string | readonly number[]`, och ändra de faktiska
signaturerna genom `KalkylatorPage` → `energiPotential` → `besparingsvarde`. Skilj gärna
formulärets råa strängtillstånd från den parsade domän-DTO:n. Gör `IndataPost` till en
verklig diskriminerad union (`vardetyp` + matchande `varde`) i båda språk, eller beskriv
ärligt en bred union med obligatorisk runtime-korsvalidering och visa varför den ger samma
fail-closed-egenskaper. Nya bindningar ska dessutom validera rätt måltyp: bandbindningen
måste peka på `band_id`, årsseriebindningarna på `number_series`, och respektive fasad ska
kräva rätt omfattning. Testa serialisering och hela den valda DTO-kedjan.

### P1 — UI-metadatan kan inte generera de fält den lovar

V9 definierar `policyFaltMetadata(policy)`, men bandalternativen finns inte i policyn utan i
den valda prispostens `prisar.kapacitet.nivaer[].id`. En funktion som bara tar
`Tariffpolicy` kan därför inte skapa sitt eget `band_id_val`. `KravPost` har samtidigt
`enhet`, `tillamplighet` och `kalla`, men inga `etikett`- eller `hjalptext`-fält och V9 anger
ingen deterministisk mappning som skapar dem.

"En post per `KravPost`" med `obligatorisk: true` ger ytterligare två fel:

- Stockholms gemensamma policy innehåller både `monthly`- och `annual`-krav. En metadata-
  funktion utan omfattning skulle visa de tre månadsfälten tillsammans med de två
  årsserierna i årskalkylen.
- `kapacitetBindning` pekar redan på ett `KravPost`, medan `KalkylatorPage` har ett separat
  obligatoriskt `kapacitetKw`-fält och V9 fortsatt lägger detta värde i kartan efter den
  generiska uppbyggnaden. En post per krav skulle alltså visa debiterbar effekt två gånger.

Bandvalet använder dessutom `next(...)` i motorn, men planen har tappat det tidigare
kravet att tomma eller dubblerade `nivaer[].id` ska avvisas. Två prisrader med samma ID
skulle tyst välja den första och göra leverantörens bekräftade ID tvetydigt.

**Begärd rättning:** gör metadatafunktionen minst beroende av `(policy, prisar,
omfattning)` och definiera om kapacitet ska migreras in i samma generiska UI eller
uttryckligen filtreras bort eftersom det befintliga fältet äger den indatauppgiften.
Etikett och hjälptext ska ha en maskinläsbar källa som följer med genom generatorn. Rendera
bara krav som gäller `annual` på kalkylatorsidan. Validera att varje bevarat band-ID är en
icke-tom sträng och unikt inom prisposten innan motorn eller UI:t får använda det. Batch
0:s end-to-end-test ska rendera den verkliga `KalkylatorPage` med en vald syntetisk
prispost, inte en fristående testkomponent som kan vara bortkopplad från produktsidan.

### P1 — ogiltig kundindata felklassas fortfarande som trasigt kontrakt

V8 bad uttryckligen om att både saknad **och ogiltig** kundindata skulle skiljas från ett
trasigt policykontrakt. V9 ger bara `KontraktBlockerat.saknadeFalt`. Fel värdetyp, fel
serielängd och okänt enum-/band-ID ska fortfarande kasta ett generiskt kontraktsfel, med
motiveringen att ett genererat UI inte kan skapa sådana värden.

Det antagandet håller inte. En användare kan lämna en 12-månadersserie delvis ifylld,
skriva ett ogiltigt numeriskt värde eller skicka ett gammalt sparat bandval efter en
prisuppdatering. Dessutom är `calcResult`/produktadaptern en anropsyta även för framtida UI,
API och Ellen-integrationer. Otillförlitlig anropsindata blir inte ett internt
konfigurationsfel bara för att dagens formulär försöker begränsa den.

**Begärd rättning:** lägg en typad användarfelsgren för både saknade och ogiltiga
policyfält, med fältnyckel och maskinläsbar orsak (typ, numerik, kardinalitet, allow-list
eller okänt band). `KalkylatorPage` ska kunna visa fältnära fel. Reservera internt
kontrakts-/konfigurationsfel för exempelvis saknad bindningsmålpost, fel bindningstyp,
omöjlig policykombination eller trasig genererad metadata. Testa samma ogiltiga värden via
både UI och direkt produktanrop.

### P1 — Stockholm har ingen nåbar produktväg för den aktuella årskostnaden

V9 fattar rätt domänbeslut: med verkliga 12/5-serier kan Stockholm ge en uppskattad aktuell
årskostnad, men inte ett verifierat före/efter-besparingsbelopp. Den faktiska
produktdispatchen är däremot inte beskriven. `_kraver_kontrakt` gör bara att
`beraknaBesparingsvarde` väljer `beraknaBesparingsvardeKontrakt`; V9 kräver samtidigt att
just den funktionen kastar ett typat produktbegränsningsfel för Stockholm.
`calcResult`/`KalkylatorPage` har i dag bara resultatmodellen `Besparingsvarde` med
`kostnadFore`, `kostnadEfter` och `besparingKr`. Ett ensamt anrop till
`beraknaArskostnadMedKontrakt` någonstans under motorn gör därför inte aktuell årskostnad
nåbar eller visningsbar för användaren.

**Begärd rättning:** definiera en namngiven produktentry och en diskriminerad
produktresultattyp för `current_annual_cost` kontra `savings_estimate`, inklusive
dispatchen i `calcResult` och renderingen i `KalkylatorPage`. Stockholm ska gå till exakt
ett årsfasadanrop och visa kostnad + `snapshot`/uppskattningsproveniens utan tomma eller
påhittade besparingsfält. Kr- och schablonlägena samt besparingsläget ska fortsatt
blockeras med tydliga produktorsaker. Lägg ett verkligt sidtest som väljer Stockholm,
fyller 12/5-serierna och visar aktuell årskostnad utan besparingssiffra.

### P1 — adapterpreflighten är fortfarande inte en implementerbar tvåvägsregel

Den framåtriktade delen har blivit bättre genom provider- och prisårsuppslag, men
pseudokoden använder fortfarande globala `POLICYREGISTER`/`ADAPTERREGISTER` trots att
generatorn redan har ett injicerat `policyregister` och V8 krävde ett injicerbart
adapterregister. Samma kodblock återgår dessutom till `godkanda(katalog)` utan det
policyregister V9 nyss beslutat ska föras vidare.

Den omvända kontrollen innehåller bokstavligen `pass  # se produktionskoden` och kan därför
inte bevisa testet planen lovar. Den efterföljande textregeln är också motsägelsefull:

- först förbjuds `annual_forward` om policyn inte är adaptermål **eller** inte redan var
  godkänd före etappen, vilket med `eller` även förbjuder en ny, korrekt adaptermappad
  Stockholm-policy;
- därefter sägs varje leverantörsfilspolicy med `annual_forward` kräva exakt en adapter;
- pseudokodskommentaren säger samtidigt att framtida direkta leverantörsprodukter utan
  katalogmotsvarighet är tillåtna.

"Redan godkänd före denna etapp" är dessutom historiskt tillstånd, inte data som en ren,
reproducerbar generator kan kontrollera.

**Begärd rättning:** gör kontrollen till en separat, körbar och injicerbar funktion över
`(rå katalog, byggda leverantörer, policyregister, adapterregister)`. Använd samma
injekterade register genom hela kedjan och validera unik källa samt unikt mål. Lägg en
explicit, maskinläsbar markör på en leverantörsprispost/policy som **ska ersätta** en
katalograd; då kan reverse-regeln bevisa en bijektion utan historiska undantag och utan att
förbjuda legitima direkta leverantörsprodukter. Specificera hur både `bygg_ts` och
`bygg_ts_fran_katalog` beter sig, eftersom `_bearbeta_leverantorsfil()` används av båda.
Ersätt `pass` med full pseudokod och testa injicerade register, fel provider/tariff,
saknad/redundant mapping, dubbelt mål och exakt ett UI-val.

## P2-fynd

- Överlämningens och sessionens `v9_delivered_at` är `22:56:55`, medan den faktiska
  V9-committen `2cfa3be` skapades `22:58:58`. Leveransavsnittet säger också att committen
  ligger ovanpå ``fd372a2`/`b7790ca` ``, fast dess direkta förälder är `b7790ca`.
  Rätta med en daterad proveniensnot utan att skriva om historiska rader tyst.
- §6a.2 säger på ett ställe att band-ID:ts värdeunion inte är en global vidgning, men
  definierar sedan den gemensamma `Varde`-aliasen som inkluderar `str`. Antingen ska en
  verkligt diskriminerad posttyp visas eller terminologin ändras så att statisk och
  runtime-baserad säkerhet inte blandas ihop.

## Verifieringar

- `skills@2cfa3be` består inom V9-scope av dokumentation och konversationslogg. Ingen
  produktkod, tariffdata eller genererad frontendfil ändrades.
- `git diff --check b7790ca..2cfa3be` är rent. Lokal `main` är elva commits före
  `origin/main`; V9 är inte godkänd för push.
- Produktrepoerna är rena på `enkey-agents@fd8f8da` och
  `neptune_academy@f1df177`. Deras faktiska typer, generatorväg, kontraktsfasad,
  besparingsadapter och kalkylatorsida lästes som granskningsbas.
- V9 behåller kontrollmängden 78 bastariffer + 14 varianttäckningskrav = 92 och
  dispositionen 7/55/30. Den korrigerade aktiveringsräkningen är 43 nakna katalogpassager
  + Umeås sammansatta passage = 44 katalogaktiveringar, samt Stockholm via
  leverantörsfilsadapter = 45 ready-bastariffer.
- Inga fulla produkttester kördes eftersom V9 endast ändrar planeringsdokumentation och de
  beskrivna nya gränssnitten ännu inte finns i kod.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v10.md` och `batchplan-v10.md`; ändra inte V9 i efterhand.
2. Välj en verklig DTO för number, band-ID, enum och serie genom hela produktkedjan och
   specificera ett statiskt eller uttryckligt runtime-diskriminerat `IndataPost`-kontrakt.
3. Gör UI-metadatan prispost- och omfattningsmedveten, definiera etikett/hjälptext,
   undvik dubbel kapacitetsinmatning och validera unika icke-tomma band-ID:n.
4. Klassificera både saknade och ogiltiga kundfält som typade användarfel; håll trasig
   policy/genererad metadata separat.
5. Ge Stockholm en nåbar produktentry/resultatunion och ett sidtest för uppskattad aktuell
   årskostnad utan besparingsbelopp.
6. Ersätt adapterpreflightens `pass` och historiska undantag med en injicerbar,
   maskinläsbar tvåvägskontroll som använder samma register i hela generatorn.
7. Behåll V9:s lösta Umeå-, Stockholm-serie-, Kraftringen-, Jönköping- och räknebeslut samt
   dispositionerna 7/55/30 om ingen sakstatus ändras.
8. Skapa en fokuserad lokal dokumentationscommit ovanpå `2cfa3be`, logga verklig hash/tid
   och stanna för ny Codex-granskning. Ändra ingen produktkod eller tariffdata och pusha
   inte.
