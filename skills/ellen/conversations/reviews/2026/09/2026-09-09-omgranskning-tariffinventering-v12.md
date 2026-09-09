---
review_id: "2026-09-09-003"
date: "2026-09-09"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v12.md
  - Fjarrvarmetariffer/batchplan-v12.md
  - skills commit a773524166eda3862736fb38e71771e1d09cb46e
reviewed_heads:
  skills: "a773524166eda3862736fb38e71771e1d09cb46e"
  enkey-agents: "fd8f8da3eb17cce638dc2f3370efa027c2afcad6"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-09-002"
---

# Omgranskning av tariffinventering v12 och batchplan v12

## Bedömning

V12 löser två av V11:s viktigaste blockerare. `maxVarde` null-normaliseras och den nya
förvalidatorn omfattar nu även min/max/heltal. `bygg_ts()` har också fått en körbar,
uttryckligen snävare adapterpreflight i stället för V11:s tomma katalog som alltid måste
kasta. Dessa delar ska bevaras.

Planen är ändå inte implementeringsklar. Parserns signatur kan inte ta emot den frånvarande
state-nyckel som texten kräver att den ska klassificera, och samma avsnitt använder både den
nya diskriminerade unionen och det gamla `PolicyValideringsFel`-språket för saknad indata.
Direkta produktanrop kan fortfarande inte få den utlovade listan `saknadeFalt`, eftersom
`harledResultatstatus` bara returnerar ett generiskt `blocked`-statusobjekt och kastar bort
sin lokala lista. Årsproduktens förmåga definieras motsägande för Sandviken, läser rå policy
utanför den enda tillåtna resolvern och skyddas bara i sidwrappern. Den påstått verkliga
`argsFranInputs` är fortfarande en `...`-platshållare och dess returtyp kräver
besparingsfält som en aktuell-årskostnad inte har.

Det krävs därför en koncentrerad V13-rättning av de två planeringsdokumenten. Ingen
produktkod, tariffdata, aktivering eller push är godkänd.

## P1-fynd

### P1 — parserkontraktet kan fortfarande inte uttrycka alla beskrivna anrop

V12 §6a.2 rad 1962 anger
`parsaPolicyIndata(metadata, ravarde: PolicyRawFormValue)`. Rad 1975–1978 och 2001–2005
kräver samtidigt att sidan itererar hela metadatalistan och skickar även en state-nyckel som
aldrig har initialiserats, vilken ska behandlas som saknad. Ett uppslag i
`Record<string, PolicyRawFormValue>` kan vid runtime ge `undefined`, men funktionens
signatur accepterar inte det värdet. Texten anger inte heller någon explicit normalisering
före anropet.

Rad 1972–1974 definierar den nya unionen korrekt som `parsed | saknat | ogiltigt`, men rad
1990–1995 säger fortfarande att fel kardinalitet och ett tomt serieelement blir
`PolicyValideringsFel`, inklusive orsaken `'saknat'`. Den typen har ingen sådan orsak; enligt
den nya unionen ska blankt bli `status:'saknat'` och ogiltig numerik/kardinalitet
`status:'ogiltigt'`. Batchplan rad 100–102 använder dessutom den odefinierade aliasen
`PolicyValideringsOrsak`, medan rad 111–112 lägger till `'min'|'max'|'heltal'` trots att
inventeringen rad 2131–2140 uttryckligen väljer `'numerik'` för alla tre.

**Begärd rättning:** ange exempelvis
`parsaPolicyIndata(metadata, ravarde: PolicyRawFormValue | undefined)` och ett enda exakt
utfall för frånvarande nyckel, blank skalär, blankt serieelement, fel kardinalitet,
icke-numeriskt värde och explicit noll. Definiera parserns och domänvalidatorns
orsaksunioner en gång och använd samma typer i inventering och batchplan. Ta bort det gamla
`PolicyValideringsFel`/`'saknat'`-språket ur parserbeskrivningen.

### P1 — `saknadeFalt` är fortfarande onåbart för direkta produktanrop

V12 rad 2111–2114 säger att `valideraPolicyIndata` bara granskar fält som redan finns i
indatakartan och lämnar saknade fält till `harledResultatstatus`. Rad 2142–2147 påstår sedan
att den befintliga blocked-vägen redan härleder `saknadeFalt` från statusen. Det stämmer inte
mot den lästa produktkoden: `Resultatstatus` på
`neptune-marketing/src/utils/resultatkontrakt.ts` rad 262–266 innehåller bara omfattning,
noggrannhet och fullständighet. `harledResultatstatus` rad 378–380 bygger en lokal
`saknade`-lista men returnerar endast generiskt `blocked`; själva nycklarna försvinner.

UI-parsern kan skapa en egen lista, men V12 kräver också direkta produktanrop som kringgår
formuläret (rad 2162–2164). Ett sådant anrop når
`beraknaBesparingsvardeKontrakt`/`beraknaArsprodukt` utan listan och kan därför inte fylla
`KontraktBlockerat.saknadeFalt` enligt planens eget kontrakt.

**Begärd rättning:** gör förkontrollen sluten över både närvaro och värde, exempelvis med
ett resultat `{ saknadeFalt, ogiltigaFalt }` för relevanta krav i vald omfattning. Kör den i
båda publika produktvägarna före fasaden. UI:t får använda samma funktion för fältnära
presentation, men domänlagret måste själv äga spärren. Lägg direkttest för ett helt saknat
`policyFalt`, en saknad enskild nyckel och ett ogiltigt värde; alla ska ge den exakta typade
felkanalen utan beroende av React-state.

### P1 — produktförmågan har tre olika definitioner och kan kringgås

Batchplan rad 41–43 och 128–135 säger att `stodjerAktuellArskostnad` är sann för varje
kontraktsgated tariff. Inventering rad 2709–2713 säger i stället att den är sann bara när
`kallenergiArsserieBindning` finns, och testkravet rad 2811–2815 kräver uttryckligen
`false` för Sandviken och `true` för Stockholm. Batchplan rad 659–662 återgår sedan till
"sann bara för kontraktsgated tariffer". Implementatören kan inte avgöra vilken sanning som
gäller.

Den detaljerade varianten läser dessutom
`prisar.policy?.kallenergiArsserieBindning` direkt. Dagens auktoritativa kod anger i
`besparingsvarde.ts` rad 134–156 att `kontraktsgatadPolicy(prisar)` är den enda plats som får
tolka den råa `_kraver_kontrakt`/`policy`-kombinationen, just för att feltypad eller
inkonsekvent metadata ska kasta fail-closed. Den nya hjälparen skulle kringgå den regeln.

Slutligen ligger spärren bara i `calcResultForOnskadTyp`. V12 rad 2711–2713 säger
uttryckligen att `beraknaArsprodukt` inte behöver skydda sig. Funktionen är samtidigt en ny
publik domänentry. Ett direkt anrop kan då räkna en tariff som kapacitetsfunktionen säger
inte stöder produkten eller nå legacydata utan den avsedda förkontrollen.

**Begärd rättning:** skriv en enda förmågetabell för icke-fjärrvärmesystem, legacytariff,
Sandviken och Stockholm och återanvänd den överallt. Om den avsedda specialprodukten bara är
Stockholms aktuella årskostnad ska Sandviken vara `false` i både inventering och batchplan.
Låt förmågefunktionen använda `kontraktsgatadPolicy(prisar)` och kontrollera energisystemet
där `KalkylatorInputs` finns. Upprepa den auktoritativa guarden inne i
`beraknaArsprodukt`; wrapperns kontroll får vara en UX-förkontroll, inte den enda spärren.
Testa både wrapper och direkt produktanrop för samtliga fyra tabellrader.

### P1 — `argsFranInputs` är fortfarande inte en implementerbar argumentbyggare

V12 rad 2755–2759 visar en funktion vars hela kropp är `...`. Detta är samma praktiska hål
som V11-granskningen bad V12 stänga. Returtypen gör dessutom den utelämnade logiken
avgörande: dagens `BesparingsvardeArgs` kräver `totalMwh`, `paverkbarMwh` och
`besparingsgrad` (`besparingsvarde.ts` rad 204–208). Dagens `calcResult` bygger tre olika
anrop med `mid`, `min` respektive `max` på rad 500–538. En
`argsFranInputs(inputs): BesparingsvardeArgs` måste därför antingen välja en enda
besparingsgrad, räkna om samma underlag tre gånger eller få ytterligare argument. En
aktuell årskostnad behöver över huvud taget varken `paverkbarMwh` eller
`besparingsgrad`.

Planen anger inte heller uttryckligen hur `policyFalt`, `energyScope`-uppskalningen,
MWh-proveniensen och kapaciteten bevaras i den nya funktionen. Att göra
`onskadTyp` obligatoriskt bryter samtidigt alla befintliga typade `KalkylatorInputs`-objekt
och `calcResult`-anrop; den lästa källträdet innehåller cirka 85 sådana deklarationer/anrop.

**Begärd rättning:** visa faktisk pseudokod utan ellips. Rekommenderad uppdelning är en
delad `Tariffberakningsunderlag`/basargs med total MWh efter scope-normalisering,
leverantör, kapacitet, `falt`, `policyFalt` och proveniens; besparingsvägen lägger därefter
till `paverkbarMwh` och respektive min/mid/max-grad. Låt `beraknaArsprodukt` ta en smalare
`ArskostnadArgs` som inte kräver påhittade besparingsfält. Gör `onskadTyp` bakåtkompatibelt
med `onskadTyp?: ...` och default `'besparing'`, eller lista och uppdatera samtliga
befintliga anrop i samma batch. Bevisa med tester att rumsvärme-scope, MWh-only,
`policyFalt`, proveniens och de tre besparingsgraderna är oförändrade.

## P2-fynd

- Adapterpreflightens kodidé är nu godtagbar, men förklaringen på rad 2537–2540 säger att
  `bygg_ts()` verifierar "båda riktningarna" för filer utan ersättningsmarkör trots att
  riktning 1 alltid hoppas över när `rak_katalog=None`. Beskriv den faktiska garantin utan
  detta undantag.
- Rad 2542–2546 säger fortfarande att `_bearbeta_leverantorsfil()` läser policyn från
  katalog-JSON. Den verkliga funktionen hämtar policyn ur `policyregister.py` och
  serialiserar den med `_policy_till_json()`. Rad 2548–2550 måste också kvalificera att en
  stale adapterpost mot saknad katalog/provider/tariff bara kan upptäckas i den fulla
  katalogvägen; standalone-vägen kör endast reverse-ledet.
- Batchplanens punktlista numrerar två efterföljande poster som 9 (rad 122 och 140).
  Inventeringens historikrad 88–89 säger samtidigt `onskadTyp` ligger i `args`, vilket inte
  är V12:s gällande signatur. Historik får stå kvar, men markera den specifika raden som
  superseded så den inte kan läsas som implementeringsinstruktion.
- Överlämningens frontmatter ligger efter V12-committen fortfarande på
  `v11-reviewed-changes-required`, scope v1–v11 och leverabler endast genom V11. Synkronisera
  leveransmetadata i V13-committen med verklig hash och committid.

## Verifieringar

- `skills@a773524` ändrar bara V12-dokumentation och konversationslogg. Ingen produktkod,
  tariffdata, genererad frontendfil eller aktivering ändrades.
- `git diff --check 136d9cd..a773524` är rent. Den verifierbara committiden för
  `a773524` är `2026-09-09T08:53:39+02:00`.
- Produktrepoerna är rena och oförändrade på `enkey-agents@fd8f8da` och
  `neptune_academy@f1df177`. Den verkliga parser-/statusbasen, policyresolven,
  `BesparingsvardeArgs`, `calcResult` och generatorn lästes som granskningsbas.
- V12 innehåller 78 bastariffrubriker och redovisar 78 bas + 14 varianter = 92 samt
  dispositionen 7 implementerade, 55 redo och 30 blockerade. Inget sakstatusfynd i V12
  motiverar en flytt i denna runda.
- Lokal `main` är 16 commits före `origin/main` och inte efter. V12 är inte godkänd för
  push.
- Inga fulla produkttester kördes eftersom V12 endast ändrar planeringsdokumentation och
  de planerade gränssnitten ännu inte finns i kod.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v13.md` och `batchplan-v13.md`; ändra inte V12 i efterhand.
2. Slut parserkontraktet över `undefined`, blankt, ogiltigt och explicit noll; använd en
   enda deklarerad uppsättning orsaker i båda dokumenten.
3. Låt domänens förkontroll returnera både exakta saknade och ogiltiga fält, så direkta
   produktanrop får samma typade fel som UI-anrop.
4. Skriv en enda produktförmågetabell, använd `kontraktsgatadPolicy` som rådatagrind och
   lägg den auktoritativa kapacitetskontrollen även i `beraknaArsprodukt`.
5. Ersätt `argsFranInputs`-ellipsen med en faktisk, typkorrekt basargumentbyggare och en
   smal aktuell-årskostnadstyp; bevara alla scope-, proveniens-, policyfält- och
   min/mid/max-regler samt bakåtkompatibiliteten för befintliga `calcResult`-anrop.
6. Rätta adapterförklaringen, punktnumreringen och leveransmetadata enligt P2-listan.
7. Behåll V12:s lösta min/max/heltal- och nulltransport, den snävare körbara
   `bygg_ts()`-preflighten, råstate/DTO-uppdelningen, band-/enumtyperna,
   provider-specifika reverse-nyckeln och dispositionerna 7/55/30 om ingen sakstatus ändras.
8. Skapa en fokuserad lokal dokumentationscommit ovanpå `a773524`, logga verklig hash/tid
   och stanna för ny Codex-granskning. Ändra ingen produktkod eller tariffdata och pusha
   inte.
