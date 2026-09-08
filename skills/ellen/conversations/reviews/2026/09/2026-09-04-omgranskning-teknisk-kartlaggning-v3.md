---
review_id: "2026-09-04-005"
date: "2026-09-04"
reviewer: Codex
status: changes-required
scope:
  - teknisk-kartlaggning-28-tariffer.md version 3
  - verifieringslista-fjarrvarmebolag.md
  - forskningsbedömning 2026-09-04-003
  - omgranskning 2026-09-04-004
  - aktuell tariffkatalog
implementation_changed: false
---

# Omgranskning av teknisk kartläggning v3

## Bedömning

V3 har rättat merparten av de konkreta sakfelen i granskning `2026-09-04-004`:

- scope är nu årsnivå och dokumentet beskriver korrekt att dagens månadsfunktion bara
  fördelar ett redan beräknat årsbelopp,
- Vattenfalls nätreferens antas inte längre vara ett statiskt katalogvärde,
- `capacity_overrun` behandlas som ej tillämplig vid rekommenderad effekt och som blockerande
  vid eget effektval,
- omfattningen är rättad till 27 kapacitetstariffer och en ren energitariff,
- Vattenfalls volymrabatt har fått en strukturerad tillämpningsprincip,
- E.ON/Navirums rullande effektvärde har fått ett eget snapshot-begrepp.

Kartläggningen är fortfarande inte implementeringsklar. Fyra frågor påverkar själva
resultatkontraktet och kan annars göra ett ofullständigt eller uppskattat resultat synligt som
`exact_annual`. Claude bör lämna en kort v4 eller ett separat kontraktstillägg som rättar
fynden nedan innan kodarbete startar.

## Fynd

### P1 — datakontraktet blandar tariffkrav med kundens indata och resultatstatus

V3 rad 53–67 placerar `value`, `basis_type`, `required_for`, `source_period` och
`measurement_resolution` i samma `required_inputs`-objekt. Det blandar tre skilda saker:

1. tariffens statiska krav,
2. kundens eller fakturans faktiska värde och härkomst,
3. resultatets noggrannhets- och fullständighetsstatus.

Dessutom säger rad 48 att kontraktet har tre statusnivåer (`supplier_value`, `calculated`,
`estimated`), medan rad 43 och matrisen använder en fjärde,
`supplier_value_snapshot`. `exact_annual` används samtidigt både som resultatnivå och som
indatakrav. Dessa begrepp kan inte ligga i samma enum utan att motorn och UI:t får oklara
tillstånd.

**Begärd rättning:** dela upp kontraktet minst så här:

```text
Tariffmetadata / required_input:
  key
  unit
  required_for[]
  allowed_basis_types[]
  cadence
  measurement_resolution
  source_period_definition
  applicability
  source_reference

Körningsindata / supplied_input:
  key
  value | series
  basis_type                 # supplier_value | calculated | estimated
  observed_period
  valid_from / valid_to
  source_reference
  quality

Resultatmetadata:
  scope                      # annual | monthly
  accuracy                   # exact | snapshot | estimated
  completeness               # complete | partial | blocked
```

Ett kundvärde ska alltså inte lagras i tariffkatalogens kravobjekt. `required_for` bör vara
en lista eftersom samma fält kan krävas för flera resultatnivåer. Snapshot ska vara en
resultategenskap, inte en fjärde sorts mätvärdeskälla.

### P1 — E.ON-snapshot och en ofullständig Vattenfalltariff kan inte ge `exact_annual`

E.ON-tabellen säger på rad 110 att ett enda effektvärde är en ögonblicksbild av en rullande
månadsserie, men rad 112 säger ändå att årssumman är exakt med leverantörens effektvärde.
Det är motsägande. Ett enda aktuellt effektvärde kan ge ett användbart årsscenario med
dagens priser, men inte rekonstruera de tolv debiterade effektvärdena.

För Vattenfall anger rad 188–190 att flödesposten är blockerad. Samtidigt placerar rad
296 tariffen under `exact_annual` och steg 5 på rad 315–316 föreslår implementation av övriga
delar medan flödesposten lämnas blockerad. En totalsumma där en obligatorisk prispost saknas
är inte exakt och får inte exponeras som en produktionsgodkänd tariff.

**Begärd rättning:**

- E.ON/Navirum med ett effektvärde ska ge `accuracy: snapshot`, inte `exact`, även om
  energi- och flödeskomponenterna är exakta.
- Exakt historisk årssumma för E.ON/Navirum kräver de tolv effektvärden som faktiskt
  debiterades eller en verifierad rekonstruktion av varje månads rullande grund.
- Vattenfalls interna delkomponenter får gärna implementeras och testas, men hela tariffen
  ska ha `completeness: blocked` och förbli inaktiv tills flödesposten kan beräknas.
- Ingen totalsumma får status `exact` när en kostnadskomponent är utelämnad.

### P1 — neutrala temperaturdefaultar är fortfarande okända värden, inte verifierad noll

V3 rad 75 säger att Södertörns och Telges defaultvärden ger “korrekt nollbidrag” och därför
kan behållas. Noll är bara korrekt om kundens faktiska returtemperatur eller avvikelse ger
noll enligt tariffen. När värdet saknas är utfallet okänt; ett neutralt default är ett
scenario eller en uppskattning, inte ett fakturavärde.

Problemet syns också i indatatabellen på rad 296: exakt årsresultat kräver varken Södertörns
temperaturavvikelse eller Telges returtemperaturunderlag, trots att katalogen innehåller
`temperature_difference` respektive `incremental_return_temperature`. Den senare kan inte
generellt reproduceras exakt från ett neutralt årsmedel om månads- eller tröskelregler påverkar
beloppet.

**Begärd rättning:** lägg dessa fält i tariffens obligatoriska indata för ett exakt resultat.
Saknade värden ska antingen blockera exaktheten eller ge ett tydligt märkt
snapshot-/estimatläge. Samma regel ska gälla VänerEnergis `flode_m3`, vilket v3 redan anger
korrekt.

### P1 — scope-texten säger att blockerade justeringar både ska byggas och inte byggas

Rad 88–90 säger att E.ON/Navirum, Sundsvall Matfors och Vattenfalls nya justeringar “byggs”
med befintlig årsbegränsning. Rad 188–190 och 317–318 säger i stället att Matfors och
Vattenfalls flödespost ska vara oimplementerade. Det är en viktig skillnad mellan en
årsberäkning och en blockerad, okänd formel.

**Begärd rättning:** begränsa byggpåståendet till de poster som faktiskt har verifierad
formel och komplett årsindata. Lista Matfors och Vattenfalls flödespost som ej byggbara och
tariffblockerande, inte som årsposter med redovisningsmässig månadsfördelning.

### P2 — matrisen är familjeaggregerad, inte en per-tariffmatris för 27 tariffer

Rubriken på rad 266 och ändringsloggen säger att alla 27 kapacitetstariffer finns i en
per-tariffmatris. Tabellen har i praktiken elva rader och slår ihop E.ON-, Navirum- och
Vattenfalltariffer med `×2`, `×4` och `×12`. För Vattenfall anges exempelvis ett intervall av
referenstemperaturer “per ort”, utan att koppla rätt temperatur och nätvillkor till ett
tariff-ID. Tabellen kan därför inte fungera som direkt implementationsunderlag.

**Begärd rättning:** använd antingen 27 explicita tariff-ID-rader eller två normaliserade
tabeller:

1. en familjetabell för gemensam algoritm,
2. en nät-/tariffparameter-tabell med varje tariff-ID, referenstemperatur, historikperiod,
   dagurval, reservregel, avrundning, uppdateringsfrekvens och källreferens.

Om en uppgift saknas ska `ej publicerat` stå på just den tariffen. Samma struktur bör bära
källreferensen, inte bara hänvisa generellt till katalog och verifieringslista.

### P2 — Vattenfalls årliga uppdatering är bättre belagd än matrisen anger

Matrisen anger `Årlig (ej bekräftat)` för Vattenfall. Den lokalt sparade officiella
prislistan beskriver att den rekommenderade effekten beräknas en gång per år och meddelas
för nästkommande år. Om formuleringen avser samma debiteringseffekt bör den anges som
bekräftad med sidreferens. Om den avser en annan effektstorhet måste raden delas så att de
tre Vattenfallbegreppen inte sammanblandas.

## Rekommenderad väg till implementation

1. Låt Claude rätta kontraktsmodellen och exakthetsreglerna i v4 utan kodändringar.
2. Godkänn därefter en Fas A-lista där varje hel tariff har samtliga kostnadskomponenter och
   obligatoriska kundvärden kartlagda.
3. Implementera gärna blockerade familjers fristående delregler internt, men exponera inte
   tariffen som användbar förrän resultatets `completeness` är `complete`.
4. Behåll Sandviken som möjlig Fas B-pilot efter att datakontraktet är låst.

## Slutsats

V3 är nära ett användbart beslutsunderlag och sakfrågorna från v2 är till stor del lösta.
Det kvarvarande arbetet är främst ett strikt kontrakt för **källa**, **noggrannhet** och
**fullständighet**. Det bör rättas före implementation eftersom efterhandsändringar annars
måste göras samtidigt i katalog, Python, TypeScript och UI.

Ingen implementation eller tariffdata ändrades i denna granskning.

## Kontrollerade lokala underlag

- `Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md`
- `Fjarrvarmetariffer/optimate-fjarrvarme-2026.json`
- `Fjarrvarmetariffer/verifieringslista-fjarrvarmebolag.md`
- `Fjarrvarmetariffer/fjarrvarme-energi-effekt-forskningsunderlag.md`
- `Fjarrvarmetariffer/prislistor/vattenfall/prislista-fjarrvarme-haninge-tyreso-alta-2026.pdf`
- `conversations/reviews/2026/09/2026-09-04-omgranskning-teknisk-kartlaggning-v2.md`
