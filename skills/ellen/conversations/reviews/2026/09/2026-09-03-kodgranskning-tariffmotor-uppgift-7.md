---
review_id: "2026-09-03-001"
date: "2026-09-03"
reviewer: Codex
status: completed
scope:
  - enkey-agents tariffmotor
  - neptune_academy energipotential-kalkylator
reviewed_heads:
  enkey-agents: "4a124e4"
  neptune_academy: "33b0ec2"
---

# Kodgranskning: tariffmotorplanen och uppgift 7

## Bedömning

Implementationens struktur är genomtänkt och testsituationen är stark, men
ändringarna bör inte pushas som produktionsklara ännu. Jag ser tre direkta
produktfel och fyra viktiga härdnings- eller modellfrågor.

Det viktigaste fyndet är att Gotlands volymrabatt väljs på fel storhet. Det
påverkar både besparingsberäkningen och den nya logiken för tvetydig invers.
Det andra direkta produktfelet är att resultatvyn inte är en oföränderlig
ögonblicksbild av den indata som användes.

## Fynd

### P1 — Gotlands volymrabatt använder aktuellt år i stället för föregående kalenderår

Katalogen anger uttryckligen `basis: previous_calendar_year_MWh` och att vald
sats gäller all köpt energi:

- `Fjarrvarmetariffer/optimate-fjarrvarme-2026.json:3453`

Motorerna summerar i stället den energifördelning som just nu prissätts och
väljer rabattband från den:

- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/faktura.py:415`
- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/utils/fjarrvarme.ts:489`

I besparingsmodellen prissätts en syntetisk faktura före och en annan efter
besparingen. Nu kan därför rabattbandet ändras när den syntetiska energin
minskar, trots att fakturans rabatt ska vara bestämd av föregående
kalenderårs förbrukning och därmed vara densamma för båda jämförelsefallen.

Ett reproducerat exempel med 2 505 MWh och 15 procents besparing gav
462 799 kr i modellen, men 473 445 kr när baslinjens 12 kr/MWh-band hölls
konstant. Avvikelsen var 10 646 kr. Vid 5 respektive 25 procent var
avvikelsen 11 899 respektive 9 394 kr.

Den diskontinuitet och de dubbla rötter som den nya inversen hanterar uppstår
dessutom därför att samma okända MWh används både som årets köpta energi och
som föregående kalenderårs rabattgrund. De är inte två namn på samma
affärsvariabel.

Rekommendation: inför en separat, spårbar indata för föregående kalenderårs
MWh eller leverantörens valda rabattband. Lös bandet en gång och håll satsen
konstant i före/efter-jämförelsen. Om värdet saknas bör motorn redovisa
scenarier eller sänkt datakvalitet, inte koppla det tyst till aktuell energi.
Gör därefter om invers- och bandgränstesterna mot den rätta modellen.

### P1 — Resultat, varningar och inskickat underlag kan beskriva olika indata

`handleFormChange` och `handleFaltChange` ändrar formulärdata utan att rensa
eller märka det befintliga resultatet som inaktuellt:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.tsx:148`
- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.tsx:185`

Samtidigt beräknas listan över antagna fakturafält från formulärets levande
tillstånd, medan siffrorna kommer från det tidigare `result`-objektet:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.tsx:132`
- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.tsx:755`

Efter en beräkning kan användaren alltså fylla i ett fakturafält. Varningen
för antaget värde försvinner direkt, men resultatet räknas inte om. Tabellen
"Vad vi räknade på" och kontaktmeddelandet blandar på samma sätt gammalt
resultat med aktuella formulärvärden. Kontaktmeddelandet saknar dessutom de
tariffspecifika fältvärdena, så beräkningen går inte att reproducera:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.tsx:327`

Rekommendation: skapa ett komplett `calculationSnapshot` med normaliserad
indata, använda defaultvärden, leverantör, tariff-id, prisår och resultat.
Rendera resultat, varningar och kontaktunderlag enbart från denna ögonblicksbild,
eller dölj resultatet så fort någon relevant indata ändras. Lägg till ett
sidtest för ändring efter beräkning, leverantörsbyte och inskickat underlag.

### P1 — Ett enda temperaturfält kan inte återge tariffens månadsmodell

Katalogen beskriver Gotlands avkylning som månadsmedel och Norrenergis
returtemperatur som flödesvägd per månad:

- `Fjarrvarmetariffer/optimate-fjarrvarme-2026.json:3449`
- `Fjarrvarmetariffer/optimate-fjarrvarme-2026.json:6077`

Formuläret samlar däremot ett enda gemensamt tal per typ. Motorerna summerar
energin för alla berörda månader och applicerar detta enda tal på summan:

- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/faktura.py:491`
- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/utils/fjarrvarme.ts:579`

För Norrenergis stegvisa formel är detta inte matematiskt ekvivalent med att
räkna varje månad, särskilt när månadsvärden ligger på olika sidor om
60 °C-tröskeln. Ett årsmedel kan därför inte ge en exakt årskostnad.

Rekommendation: modellera månadsserier för de tariffposter som uttryckligen
är månatliga. Om ett enda sammanfattande värde ska behållas måste det märkas
som approximation, metoden dokumenteras och datakvaliteten sänkas.

### P2 — Datakvaliteten tar inte hänsyn till tariffantaganden

Datakvaliteten avgörs i dag av känd energi och uppskattad kapacitet, men inte
av saknade tariffspecifika fakturafält:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/utils/energiPotential.ts:254`

En kund kan därför få "hög datakvalitet" samtidigt som resultatet använder
flera antaganden. Fältet `ar_gissning`, som särskiljer Mölndals icke-neutrala
gissningar, exporteras men används ingenstans i gränssnittet eller
kvalitetsbedömningen.

Rekommendation: låt datakvaliteten väga in antal och betydelse av antagna
fält, särskilt `ar_gissning`. Skilj också mellan neutral nollpåverkan,
modellskattning och ett faktiskt fakturavärde. Orden "försiktigt
standardvärde" är inte generellt sanna för poster som kan ge bonus.

### P2 — Indataskyddet ändrar eller ignorerar fel utan spårbarhet

`resolvera_falt`/`resolveraFalt` klampar värden tyst till min/max, lämnar
okända nycklar orörda för att de senare ska ignoreras och accepterar `NaN`:

- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/justeringar.py:215`
- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/utils/fjarrvarme.ts:68`

Det skyddar totalsumman från vissa extrema tal, men en direkt integration
kan inte se att användarens uppgift ersatts med ett gränsvärde. Ett stavfel
i en nyckel blir ett tyst default och `NaN` kan spridas genom hela
beräkningen. Det är särskilt olämpligt för den framtida Ellen-integration
som kodkommentaren själv nämner.

Rekommendation: validera tariffens tillåtna nycklar, ändlighet och intervall
före beräkning. Returnera strukturerade fel eller åtminstone varningar och
det faktiskt använda värdet; klampa inte finansiell indata osynligt.

### P2 — Produktionsgrinden behandlar flera okända katalogvärden som kända defaultvärden

Grinden tillåter `null` för `basis_unit`, `rate_period` och `formula`, och
validerar inte `vat_basis`. Översättningen gör sedan `null` enhet till kW,
`null` period till år och okänd eller felstavad momsbasis till exklusive
moms:

- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/katalog.py:257`
- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/katalog.py:451`
- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/katalog.py:490`

Jag verifierade detta med minimala tariffer: samtliga passerade `grind()`.
En felaktig momsbasis kan innebära 25 procents kostnadsfel. Beteendet strider
mot planens uttryckliga regel att `null` betyder okänt och motorn ska vara en
godkännandelista.

Rekommendation: kräv uttryckligt tillåtna värden för alla fält som påverkar
formel, enhet, period och moms. Inga `or "kW"`- eller
`get(..., "exkl")`-defaultvärden bör finnas efter produktionsgrinden.

### P2 — Python och TypeScript avrundar exakta halvtal olika

Python använder `round`, som avrundar halvtal till jämnt, medan TypeScript
använder `Math.round`, som vid positiva tal avrundar uppåt:

- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/justeringar.py:249`
- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/utils/fjarrvarme.ts:77`

Vid Mölndals bandgräns blir 600,5 kWh/dygn 600 i Python men 601 i
TypeScript. Det väljer olika prisband och skiljer ungefär 3 059 kr inklusive
moms i årlig kapacitetskostnad. Att HTML-formuläret normalt kräver heltal
räcker inte när båda motorerna också är publika beräkningsgränssnitt.

Rekommendation: definiera en gemensam avrundningsregel och bind `.5` vid
varje bandgräns med paritetstest.

## Känd begränsning som inte bör bindas som önskat beteende

Testet `test_roten_kan_atas_upp_vid_diskontinuiteten` dokumenterar att
rotsökningen kan missa den verkliga roten nära ett volymrabattsteg och kräver
det nuvarande bristfälliga resultatet. Ett regressionstest bör normalt binda
önskat beteende eller markeras som förväntat fel, inte göra en känd brist till
kontrakt. Detta bör omprövas tillsammans med P1-fyndet om föregående års MWh.

## Det som är bra

- Python- och TypeScript-implementationerna är tydligt speglade.
- Okända justeringstyper stoppas i stället för att räknas som noll.
- Den genererade tariffilen är härledd och synktestad.
- Gotland-kraschen för tariff utan kapacitetsdel är rättad.
- Kommentarerna beskriver många av modellvalen ovanligt väl.
- Tester täcker tariffmotor, invers, paritet och regressionsfall omfattande.

## Verifiering

- `enkey-agents`: 167 tester godkända.
- `neptune-marketing`: 206 tester godkända.
- TypeScript: `tsc --noEmit` godkänd.
- Båda arbetskopiorna var rena efter testerna.
- Inga implementationer ändrades under denna granskning.

Gröna tester visar att implementationen följer sina nuvarande antaganden.
Fynden ovan gäller främst att några av dessa antaganden inte motsvarar
katalogens affärsvariabler eller att användargränssnittet inte bevarar en
spårbar beräkningsögonblicksbild.

## Rekommenderad ordning

1. Rätta volymrabattens tidsbasis och gör om inversen kring den modellen.
2. Inför en komplett, oföränderlig beräkningsögonblicksbild i kalkylatorn.
3. Bestäm och dokumentera månadsmodellen för temperatur- och avkylningsfält.
4. Koppla antagna fält till datakvalitet och spårbart kontaktunderlag.
5. Gör kataloggrinden och fältvalideringen strikt.
6. Lås en gemensam halvtalsavrundning i båda motorerna.

Separat från kodfynden kvarstår det tidigare säkerhetsfyndet: den röjda
autentiseringsuppgiften måste roteras och Git-historiken hanteras enligt en
godkänd plan. Värdet återges inte här.
