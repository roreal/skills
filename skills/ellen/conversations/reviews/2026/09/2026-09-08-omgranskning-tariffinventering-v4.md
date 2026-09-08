---
review_id: "2026-09-08-004"
date: "2026-09-08"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v4.md
  - Fjarrvarmetariffer/batchplan-v4.md
  - skills commit ada05e73ad27617a19053c8289043471788414ee
reviewed_heads:
  skills: "ada05e73ad27617a19053c8289043471788414ee"
  enkey-agents: "fd8f8da3eb17cce638dc2f3370efa027c2afcad6"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-08-003"
---

# Omgranskning av tariffinventering v4 och batchplan v4

## Bedömning

V4 löser samtliga uttryckliga fynd i granskning `2026-09-08-003`. Kontrollmängden är
fortsatt komplett med exakt 78 katalog-ID:n och 14 variant-ID:n. E.ON/Navirums
36-månadersmetod, Kraftringens minimifaktor, VänerEnergis och Mälarenergis indata,
Finspångs variantstatus, lägesstatusarna och Borås-räkningen är i huvudsak rättade.
Committen `ada05e7` ändrar ingen produktkod eller tariffdata och gör hela den länkade
konversationsmappen spårad. `git diff --check HEAD^ HEAD` är rent.

Kontrollpunkten kan ändå inte godkännas för implementation. En fullständig förkontroll
mot den verkliga produktgrinden visar att bara 21 av de 45 bastariffer som V4 klassar
`ready_to_implement` passerar när tariffens egen utredningsflagga simuleras som löst och
medlemsblockeringarna tillfälligt tas bort för att synliggöra nästa hinder. De övriga 24
stoppas fortfarande av katalogform, okänd justering, okänd issue eller energiform. V4
nämner vissa av dessa motorarbeten, men saknar en komplett väg från dagens katalogpost
till en tariff som faktiskt kan aktiveras. Ingen implementation eller push godkänns före
en fokuserad V5-rättning.

## Fynd

### P1 — 24 av 45 `ready`-tariffer stoppas fortfarande av den befintliga grinden

Förkontrollen använde `tools.tariffer.katalog.grind` i `enkey-agents@fd8f8da`, satte
endast den enskilda tariffens `investigation.status` till `klar` i en minneskopia och
anropade grinden med en tom mängd medlemsblockeringar. Resultatet blev:

| Kvarvarande grindorsak | Antal | Berörda tariffer |
| --- | ---: | --- |
| `null i band` | 11 | E.ON Järfälla ×2, E.ON Malmö ×2, Navirum ×4, Kils, Kraftringen, Övik |
| `okänd issue` | 5 | Borlänge, C4, Falu ytterorter, Telge, TEMAB |
| `kapacitetsform` | 3 | Borås, Finspång, Sundsvall Indal/Liden/Lucksta |
| `okänd justeringstyp: flow_difference` | 3 | Jämtkraft ×3 |
| `energiform` | 1 | Stockholm Exergi |
| `kapacitetsformel med multiplikator` | 1 | Umeå Energi |

Batchplanen känner till kapacitetsformsarbetet, Jämtkrafts justering och Öviks
null-normalisering, men anger inte en grindöppnande åtgärd för samtliga övriga poster.
Att kalla posten `ready_to_implement` är rimligt som källstatus, men implementationsplanen
är inte komplett förrän varje kvarvarande grindorsak har en explicit data-, motor- eller
policyåtgärd och test.

**Begärd rättning:** lägg i V5 en maskinläsbar eller entydigt parsbar preflightmatris för
alla 45 `ready`-ID:n med dagens grindorsak, planerad åtgärd, berörd fil och förväntad
slutstatus. Acceptanskriteriet ska vara att föreslagna ändringar applicerade på en temporär
katalogkopia ger `grind(...) is None` för alla 45, att de 26 blockerade bastarifferna
fortsatt ger ett grindstopp och att de fem blockerade varianterna behåller sin disposition.

### P1 — E.ON/Navirum, Kraftringen och Kils saknar nödvändiga katalogrättningar

De åtta E.ON-/Navirum-raderna har `fixed: null` och `capacity.rate_period: null`. Den
godkända verifieringslistan säger däremot att ingen separat fast avgift finns och att
effektpriset är per kW och månad. Motorn multiplicerar bara kapacitetspriset med tolv när
`rate_period == "month"`; utan en uttrycklig katalogrättning finns därför både ett
grindstopp och risk för en årskostnad med faktor tolv fel. V4 planerar endast
flödeskorrigering och Malmötemperatur för dessa poster.

Kraftringen har på motsvarande sätt `fixed: null` och `rate_period: null`, trots att
verifieringslistan redan anger `fixed: 0` och `rate_period: year`. Kils samtliga band har
`fixed: null`, trots verifierat besked att ingen separat fast avgift finns och att null
ska mappas till noll. Öviks motsvarande rättning finns redan korrekt i V4.

**Begärd rättning:** lägg till exakta katalogmutationer och golden-test för
årsperiodisering: E.ON/Navirum `fixed: 0`, `rate_period: month`; Kraftringen `fixed: 0`,
`rate_period: year`; Kils `fixed: 0`. Testa minst ett handräknat helår per tidsenhet och
att månadsvärdet inte behandlas som årsbelopp.

### P1 — Umeås kapacitetskostnad saknas i arbetsordern

Umeås katalogformel är `(fixed + variable * billing_basis) * B` och bär en
`post_multiplier`. Verifieringslistan anger att leverantörens abonnerade effekt `A` och
uttagsfaktor `B` måste användas, eftersom bolagets normalårskorrigering inte är publicerad.
V4 beskriver bara den nya flödesjusteringen `asymmetric_flow_difference` och UI-indatan
"effekt + flöde". Den missar därför en obligatorisk kapacitetsfaktor som dagens grind
uttryckligen avvisar.

**Begärd rättning:** välj ett entydigt kontrakt för Umeå: obligatoriska leverantörsvärden
`A` och `B` (alternativt hela leverantörens kapacitetsbelopp), ny typad kapacitetsmotor,
policy-/UI-bindning och handräknade testfall. Rå mätdata får inte användas för att gissa
`B` utan en separat verifierad normalårsmodell.

### P1 — Stockholm Exergis årsprodukt saknar en körbar väg

Katalogpostens energiform är `monthly_with_peak_volume_replacement`, medan grinden endast
godkänner de energiformer som dagens generella katalogmotor kan räkna. V4 kallar motorn
befintlig och batch 7 säger "ingen ny formel", men produktens redan byggda
`monthly_invoice`-väg är inte automatiskt samma sak som att katalograden kan passera
årsproduktens grind.

**Begärd rättning:** V5 ska antingen beställa generell motor för energiformen med
topplastvolymersättning, eller uttryckligen binda detta katalog-ID till den befintliga
leverantörsspecifika Stockholm-motorn via en namngiven adapter. Ange berörda filer,
årsindata, kontraktsgrind och regressionstest i båda fallen.

### P1 — fem `issues` och medlemsblockeringarna saknar livscykel

Borlänge, C4, Falu ytterorter, Telge och TEMAB stoppas av issue-texter som inte ingår i
grindens godkännandelista. Leverantörsvalt band löser inte detta automatiskt. Särskilt:

- Borlänges höstpris är verifierat men 501-kW-gränsen ska förbli blockerad för automatiskt
  bandval.
- C4:s exakt 500 kW ska hanteras som leverantörsvalt band, inte gissas.
- Falu ytterorter har publicerade grupper endast till och med 500 kW; beräkning över den
  gränsen ska blockeras eller hanteras som specialavtal.
- Telges tillsvidarevillkor är redan accepterade i verifieringslistan men katalogens gamla
  kontroll-issue ligger kvar.
- TEMAB:s leverantörsvärde kan lösa beräkningen, men issue-typen måste normaliseras till
  ett känt, uttryckligt indatakrav.

Dessutom spärrar `remaining_information_requests` fortfarande 18 av de 45 `ready`-raderna
via 13 medlems-ID:n: Borlänge, C4, båda E.ON, Falu, Kraftringen, Mälarenergi, båda Navirum,
Söderhamn, Sundsvall, Telge och TEMAB. V4 säger att respektive utredning väntar på
implementation men beskriver inte hur medlemsomfattande förfrågningar avslutas utan att
råka öppna de 31 poster som ska förbli blockerade.

**Begärd rättning:** ange för varje issue och informationsförfrågan om den ska tas bort,
delas, normaliseras eller behållas, med konkret katalogändring och grindtest. Om en
medlemsförfrågan berör både `ready` och blockerade produkter måste den delas per faktiskt
tariff-ID eller ersättas av en lika säker strukturerad spärr.

## P2-fynd

- Batch 5c:s indatatext undantar korrekt Mälarenergi 2–4 lägenheter från effektkravet,
  men raden "Visas för användaren" kräver fortfarande effekt/band för hela batchen.
- Fyra variantkällor säger "samma URL som ovan" trots påståendet om direkt URL per rad.
  Finspångs variant pekar dessutom på 2025-underlag trots verifieringslistans aktuella
  officiella 2026-källa; motsvarande aktualitetskontroll behövs för Södertörn och Borås.
- Leveransloggen säger "sex bastariffrader" men räknar E.ON ×4, Navirum ×4 och
  VänerEnergi ×1, alltså nio rader. Ändringsloggen skriver i stället E.ON/Navirum ×6.
- De spårade konversationslänkarna finns nu, men tio historiska länkar är absoluta
  `/Users/robertrennel/...`-sökvägar och därför inte portabla till en annan checkout.

P2-fynden blockerar inte i sig motorimplementationen, men ska rättas i V5 så att
planeringsunderlaget och historiken blir entydiga.

## Verifieringar

- 78 produktubriker jämfördes maskinellt med katalogens 78 ID:n: inget saknas, inget är
  extra och ingen dubblett finns.
- Dispositionerna räknades oberoende: 7 implementerade, 45 redo och 26 blockerade.
- Varianttabellen innehåller 14 unika ID:n: 9 redo och 5 blockerade. Totalen
  7 + 54 + 31 = 92 stämmer.
- Samtliga 45 `ready`-ID:n finns i batchplanen.
- Den fullständiga grindförkontrollen gav 21 pass och 24 stopp enligt tabellen ovan.
- Med katalogens verkliga `remaining_information_requests` är 18 `ready`-rader över
  13 medlems-ID:n fortfarande medlemsblockerade.
- Alla 44 spårade Markdown-filer i `conversations` kontrollerades efter lokala länkmål;
  inga spårade mål saknas. Tio absoluta historiska länkar återstår.
- `git show --stat ada05e7` och `git diff --check ada05e7^ ada05e7` visar en ren
  dokumentationscommit. Implementationsrepona är rena på redovisade HEAD-versioner.
- Inga produkttester kördes eftersom V4 endast ändrar dokumentation. Grinden kördes
  skrivskyddat mot minneskopior; inga katalogdata ändrades.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v5.md` och `batchplan-v5.md`; ändra inte V4 i efterhand.
2. Lägg till preflightmatrisen för alla 45 `ready`-ID:n och gör grindens 45/45-pass samt
   fortsatt blockering av alla 31 blockerade poster till bindande acceptanskriterium.
3. Ta med de saknade katalogrättningarna för E.ON/Navirum, Kraftringen och Kils samt
   årsperiodiseringstester.
4. Komplettera Umeå med `A`/`B`-kontrakt och kapacitetsmotor; komplettera Stockholm med en
   konkret generell motor- eller adapterväg.
5. Beskriv exakt livscykel för de fem okända issue-texterna, tariffens egen
   `investigation.status` och samtliga medlemsomfattande informationsförfrågningar.
6. Begränsa Falu ytterorter till publicerat intervall och bevara alla osäkra gränsfall som
   fail-closed.
7. Rätta P2-motsägelserna om Mälarenergi, källor, antal och portabla länkar.
8. Skapa en fokuserad lokal dokumentationscommit ovanpå `ada05e7` och stanna för ny
   Codex-granskning. Ändra ingen produktkod eller tariffdata och pusha inte.
