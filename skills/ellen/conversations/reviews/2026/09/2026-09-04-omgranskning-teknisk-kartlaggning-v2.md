---
review_id: "2026-09-04-004"
date: "2026-09-04"
reviewer: Codex
status: changes-required
scope:
  - teknisk-kartlaggning-28-tariffer.md version 2
  - forskningsbedömning 2026-09-04-003
  - aktuell Pythonmotor och TypeScript-wrapper
  - lokala officiella Vattenfall-villkor för 2026
reviewed_heads:
  enkey-agents: "545f1e054c82ce127e919c335bb31210fd866e4a"
  neptune-marketing: "f2dfe6c01b11d89d92ab731f83414b9ccb446add"
implementation_changed: false
---

# Omgranskning av teknisk kartläggning v2

## Bedömning

V2 är väsentligt bättre än v1 och har rättat huvuddelen av fynden i granskning
`2026-09-04-002`: den synliggör den tysta effektuppskattningen, tar bort E.ONs felaktiga
temperaturdefault, separerar tre olika flödesfamiljer, utökar Vattenfalls omfattning,
omklassificerar Telge och ger den rena energitariffen en semantiskt riktig lösning.

Kartläggningen är ändå inte implementeringsklar. Den blandar fortfarande tre olika
produktnivåer — fakturakorrekt resultat, års-/ögonblicksbild och uppskattning — och två av
de föreslagna månadsmodellerna bygger på antaganden som den befintliga motorn uttryckligen
inte uppfyller. Claude bör lämna en v3 som stänger fynden nedan innan kodarbete startar.

## Fynd

### P1 — datakontraktet måste omfatta alla obligatoriska fakturavärden, inte bara effekt

V2 föreslår ett booleskt `billing_basis_required_from_customer` för debiterbar effekt,
men lämnar andra kostnadsgrundande kundvärden frivilliga eller med befintliga neutrala/
härledda standardvärden.

Det tydligaste fallet är E.ON/Navirum:

- v2 rad 106 anger `flode_m3` som frivilligt,
- v2 rad 110 säger samtidigt att årssumman bara är exakt med faktisk volym,
- dagens `_flodesavgift` härleder saknad volym ur årsenergin och ett antaget ΔT på 45 K
  (`faktura.py:441–449`).

Samma problem finns för VänerEnergis befintliga `volume`-typ och, i annan form, för
Södertörns, Telges och Vattenfalls temperatur-/flödesvärden. En tariff kan få räkna med
en uppskattning, men resultatet får då inte märkas som fakturakorrekt.

**Begärd rättning:** ersätt eller komplettera effektflaggan med tariffstyrda
`required_inputs` som per fält anger källa, tidsupplösning och vilken noggrannhetsnivå
fältet krävs för. Minst följande resultatnivåer behövs:

```text
supplier_value   # leverantörens/fakturans fastställda värde
calculated       # reproducerat ur tidsserie enligt leverantörens metod
estimated        # schablon eller modell med redovisad osäkerhet
```

För `exact_annual` ska E.ON/Navirums faktiska `flode_m3` och volymviktade `Tf` vara
obligatoriska. För `exact_monthly` krävs tolv månadsvärden. Saknat värde ska blockera det
exakta läget; en härledning får endast ske i ett uttryckligt uppskattningsläge.

### P1 — den befintliga månadsfunktionen räknar inte månadsjusteringar

V2 rad 263–267 säger att dagens `_justeringar`/`manadsuppdelning` redan klarar den
säsongsbundna mekanismen. Det stämmer bara för **årssummans urvalsbas**, inte för en
fakturakorrekt månadsmodell.

I aktuell kod:

- `_mwh_for_manader` summerar valda månader inne i årsberäkningen,
- `manadsuppdelning` anropar `_justeringar` en gång för hela året
  (`faktura.py:1025`),
- årsbeloppet fördelas därefter proportionellt mot samtliga månaders andel av årets energi
  (`faktura.py:1036–1039`).

Kodens egen docstring kallar detta ett redovisningsval, inte leverantörens
debiteringsregel. En oktober–april-justering kan därmed redovisas även i maj–september.
Det räcker inte för Vattenfall, Matfors/Kvissleby, E.ON/Navirum eller en annan tariff där
månadens eget Q, W, temperatur- eller nätvärde avgör posten.

**Begärd rättning:** v3 ska välja en av två tydliga omfattningar:

1. endast exakt årssumma/årsestimat och uttryckligen ingen fakturareproduktion per månad,
2. en ny månadsberäkning som utvärderar varje justering per månad med månadens egna indata.

Om alternativ 2 väljs ska tester verifiera både den faktiska månadsformeln och att posten
är noll/ej tillämplig utanför tariffens månader — inte bara att tolv redovisningsrader
summerar till årskostnaden.

### P1 — Vattenfalls nätmedel är inte verifierat som ett statiskt katalogtal

V2 rad 236–237 beskriver `network_average` som ett enda tal per nät. Den lokalt sparade
officiella prislistan för Haninge/Tyresö/Älta 2026 beskriver i stället flödesposten genom
kundens Q/W och nätets Q/W-medel samt anger att Q/W beräknas för aktuell månad. Underlaget
ger inget stöd för att lägga ett enda statiskt års-/nättal i katalogen.

Detta påverkar samtliga tolv Vattenfalltariffer. För en exakt beräkning behövs per månad:

```text
customer_volume_m3
customer_energy_mwh
network_average_m3_per_mwh
```

**Begärd rättning:** fastställ med primärkälla eller leverantör om nätmedlet är ett
månadsvis fakturavärde, en publicerad månadsserie eller ett i förväg fastställt referenstal.
Tills dess ska Vattenfalls flödespost vara blockerad, inte fyllas med ett antaget
katalogvärde.

### P1 — `capacity_overrun` är ej tillämplig i vald omfattning, inte verifierad noll

V2 rad 243–250 föreslår att typen registreras med `beraknas=False`, vilket gör att den
bidrar med noll. Testplanen på rad 357 befäster samma beteende. Men källan säger inte att
avgiften är noll; den säger att den gäller när kunden har gjort ett eget effektval.

Om första batchen begränsas till Vattenfalls rekommenderade effekt är regeln **ej
tillämplig**. Om ett eget effektval når motorn måste den blockera tills
överuttagsberäkningen är implementerad.

**Begärd rättning:** modellera den uttryckliga produktomfattningen och villkoret. Testa att
rekommenderad effekt gör posten ej tillämplig och att eget val stoppas. Testa inte att en
okänd avgift tyst blir noll.

### P2 — effekthindret berör 27 av 28 tariffer

Rubriken på rad 36, mekanismtexten på rad 70–71, testplanen på rad 354 och räkningen på
rad 376–377 säger att effekthindret gäller alla 28. Samma dokument fastställer på rad
328–329 att Indal/Liden/Lucksta saknar både kapacitet och fast avgift och är en ren
energitariff.

**Begärd rättning:** ändra omfattningen till 27 tariffer och sätt aldrig
`billing_basis_required_from_customer` på den rena energitariffen. Slutsatsen att ingen av
de 28 är helt utan motorarbete kan fortfarande vara sann: de 27 behöver det gemensamma
indatakontraktet och den återstående tariffen behöver sitt `ej_tillämpligt`-stöd.

### P2 — Vattenfalls volymrabatt behöver inte lämnas som en öppen tillämpningsfråga

V2 rad 227–229 säger att `application: null` måste klargöras med Vattenfall. Den officiella
prislistan anger redan att årsvolymen föregående 1 maj–30 april väljer rabattnivå och att
det valda prisavdraget gäller per köpt MWh oktober–april. Detta motsvarar en vald sats på
hela den köpta energin under de angivna månaderna, inte en marginaltrappa.

**Begärd rättning:** strukturera den verifierade regeln i katalogen, exempelvis
`selected_rate_applies_to_all_purchased_energy_in_months`, med separat fält för
bandgrundens period. Lämna inte en redan publicerad regel som beslutspunkt för Robert.

### P2 — E.ON/Navirums samlade exakthet är otydligt beskriven

V2 rad 110–118 beskriver när flödesdelen kan vara exakt på årsnivå. Effektdelen är däremot
rullande och ändras månadsvis, medan v2 föreslår att senaste fakturans enda effektvärde
används för hela beräkningen (rad 119–121). Det kan vara en användbar ögonblicksbild, men
inte en exakt rekonstruktion av tolv fakturamånader.

**Begärd rättning:** redovisa exakthet per komponent:

- energi,
- effekt,
- flöde,
- total årssumma,
- månadsresultat.

Ett enda effektvärde ska ge status `supplier_value_snapshot`. Exakt tolvmånadersresultat
kräver de tolv effektvärden som faktiskt gällde respektive fakturamånad, eller att de
räknas fram ur leverantörens föreskrivna rullande historik.

### P3 — tabellen för familj 4 har två avskiljarrader

Rad 284–285 innehåller två Markdown-avskiljare och kan renderas som en tom/felaktig rad.
Ta bort den ena.

## Forskningsunderlagets konsekvens för v3

Granskning `2026-09-04-003` förändrar inte leverantörernas formler, men den ger en tydligare
produktarkitektur. V3 bör skilja på två leveranser:

1. **Fas A — faktura-/leverantörsläge:** obligatoriska, synliga leverantörsvärden. Detta är
   snabbaste vägen förbi effekthindret och kan användas före en automatisk effektmotor.
2. **Fas B — automatisk effektmotor:** en separat modul som producerar spårbart
   effektunderlag från tim-/dygnsserier, väderdata, rätt historikfönster, reservregel och
   avrundning för varje leverantör.

En tredje framtida nivå, forskningsbaserad uppskattning från referensgrupper eller
fullasttimmar, får endast ge status `estimated` med osäkerhetsintervall. Den får inte
aktivera eller fakturagodkänna en tariff.

## Begärt nästa underlag från Claude

Claude bör nu, utan implementation:

1. rätta de åtta fynden ovan i en v3,
2. lägga till en per-tariffmatris för de 27 kapacitetstarifferna med metod,
   mätupplösning, historikperiod, dagurval, väderkälla, referenstemperatur, reservregel,
   avrundning, uppdateringsfrekvens och möjlig status (`supplier_value`, `calculated`,
   `estimated`),
3. redovisa obligatoriska indata separat för exakt årssumma och exakt månadsresultat,
4. föreslå en första Fas A-batch som använder leverantörens/fakturans effekt och blockerar
   alla saknade kostnadsgrundande kundvärden,
5. föreslå en senare Fas B-pilot för en tydligt publicerad effektsignatur, lämpligen
   Sandviken, innan de mer sammansatta E.ON- och Vattenfallfamiljerna automatiseras,
6. lämna v3 till Codex för ny kontroll innan Robert godkänner implementation.

## Kontrollerade lokala underlag

- `Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md`
- `Fjarrvarmetariffer/fjarrvarme-energi-effekt-forskningsunderlag.md`
- `Fjarrvarmetariffer/verifieringslista-fjarrvarmebolag.md`
- `Fjarrvarmetariffer/prislistor/vattenfall/prislista-fjarrvarme-haninge-tyreso-alta-2026.pdf`
- `conversations/reviews/2026/09/2026-09-04-bedomning-forskningsunderlag-energi-effekt.md`
- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/faktura.py`
- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/utils/besparingsvarde.ts`
