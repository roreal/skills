---
review_id: "2026-09-04-002"
date: "2026-09-04"
reviewer: Codex
status: changes-required
scope:
  - Claudes tekniska kartläggning av 28 källgodkända tariffer
  - tariffmotorn i enkey-agents
  - TypeScript-spegeln och KalkylatorPage i neptune-marketing
reviewed_heads:
  enkey-agents: "545f1e054c82ce127e919c335bb31210fd866e4a"
  neptune-marketing: "f2dfe6c01b11d89d92ab731f83414b9ccb446add"
baseline_commit: "8ef69559a8471ee4ae2a0462c419bba6844e5927"
remote_verified: false
---

# Granskning av teknisk kartläggning för 28 tariffer

## Bedömning

Baslinjecommitten `8ef6955` är korrekt avgränsad till de fyra beställda filerna och behöver
inte göras om. Den tekniska kartläggningen är däremot inte klar som implementeringsunderlag.
Den innehåller flera materiella luckor som kan ge en tariff som räknar utan obligatoriska
leverantörsvärden eller periodiserar en månadsregel fel.

Ingen implementation bör starta från den nuvarande kartläggningen. Claude bör först rätta
fynden nedan och lämna en ny per-tariffmatris för Python, TypeScript och användargränssnitt.

## Fynd

### P1 — obligatorisk debiterbar effekt saknar datakontrakt och spärr

Kartläggningen säger att det befintliga effektfältet bara behöver vara obligatoriskt och
tydligt märkt när källan kräver leverantörens värde, men klassar ändå bland annat Sandviken
och Södertörn som rena katalogändringar:

- `Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md:19`
- `Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md:39`
- `Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md:41`

I den faktiska webbprodukten är fältet uttryckligen frivilligt, och båda beräkningsvägarna
ersätter ett saknat värde med `uppskattaEffekt(...)`:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.tsx:647`
- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/utils/besparingsvarde.ts:146`
- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/utils/besparingsvarde.ts:286`

Det räcker därför inte att ändra katalogdata. Det behövs strukturerad metadata för när
leverantörens effekt är obligatorisk, genomföring till genererad TypeScript-data, spärr i
den domännära MWh- och kronorvägen samt tariffanpassad etikett/hjälptext i formuläret. Minst
Sandviken, Matfors/Kvissleby, Södertörn och Vattenfall berörs uttryckligen av källvillkoret.

E.ON/Navirum har dessutom en rullande, månadsvis omräknad effekt. Ett enda konstant
`kapacitetKw` kan inte återskapa tolv månadsfakturor när effekten ändras mellan månader.
Kartläggningen måste välja och namnge omfattningen: månadsserie, enbart årsberäkning med
dokumenterad approximation eller en avgränsning till ett leverantörsfastställt värde för
den aktuella beräkningen.

### P1 — E.ON/Navirums föreslagna temperaturdefault är inte neutralt

Kartläggningen föreslår `Tf = 60 °C` som neutralt standardvärde för formeln

`volym × grundpris × (0,02 × (Tf − 60) + 0,2)`.

Vid 60 °C är faktorn `0,2`, inte noll. Defaulten skapar alltså en faktisk flödeskostnad på
20 procent av grundpriset. Om volymen samtidigt härleds ur MWh och antagen 45 K avkylning
bygger resultatet på två kundspecifika antaganden, trots att verifierings- och to-do-listan
uttryckligen förbjuder dolda standardvärden.

- `Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md:76`
- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/justeringar.py:24`
- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/faktura.py:441`

`Tf` och verklig volym måste vara obligatoriska för en exakt beräkning. Ett
volymviktat årsvärde kan vara algebraiskt användbart för en ren årssumma om grundpriset är
konstant, men det får då inte presenteras som en exakt månadsmodell. För månadsresultat
behövs månadsvärden eller fakturans redan uträknade post.

### P1 — tre olika flödesregler slås ihop innan deras kontrakt är definierade

E.ON/Navirums formel är temperaturjusterad men inte nätrelativ. Matfors/Kvissleby använder
en symmetrisk avvikelse mot nätets m³/MWh. Vattenfall använder separata premie- och
avgiftssatser mot ett nätmedel. De delar vissa byggstenar, men är inte samma prismodell.

Kartläggningens rekommendation om en enda ”nätrelativ flödesjustering” är därför för tidig:

- `Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md:40`
- `Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md:138`

Dagens motor räknar dessutom varje justering en gång som ett årsbelopp och
`manadsuppdelning` fördelar sedan beloppet efter månadens energiandel. Den räknar inte om
justeringen med månadens temperatur eller nätvärde:

- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/faktura.py:1025`
- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/faktura.py:1036`

Claude behöver först skriva exakt algebra, enheter, tecken, giltiga månader och nödvändiga
indata för var och en av de tre familjerna. Därefter kan gemensamma lägre byggstenar delas,
men katalogtyperna bör förbli uttryckliga och fail-closed.

### P1 — Vattenfalls omfattning är inte tillräckligt avgränsad

Fyra problem behöver lösas tillsammans:

1. Oktober–april är sju månader, inte sex som kartläggningen anger.
2. Nuvarande `volume_discount` väljer band från `foregaende_ars_mwh` och drar rabatt från
   hela årets energi. Vattenfall kräver föregående 1 maj–30 april som bandgrund och rabatt
   endast på oktober–april. Ett nytt obligatoriskt basvärde behövs, särskilt i kronorläget.
3. Katalogposterna innehåller `capacity_overrun`, som dagens grind inte känner. Regeln får
   bara avgränsas bort om katalog och UI samtidigt tvingar leverantörens rekommenderade
   effekt; dagens frivilliga/uppskattade effekt uppfyller inte det villkoret.
4. Standard/Spetsig är ett giltighetsvillkor, inte bara en kosmetisk varning. Antingen ska
   kunden uttryckligen bekräfta produkten från avtal/faktura, eller så måste nödvändiga
   historiska energi- och effektvärden krävas och fel produkt blockeras.

- `Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md:94`
- `Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md:104`
- `Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md:114`
- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/faktura.py:430`

Rekommendation: hård spärr när faktiska kvalificeringsvärden motsäger vald tariff. Om dessa
värden saknas bör användaren välja den avtalade Vattenfallprodukten uttryckligen och
resultatet märkas som beroende av detta val; motorn ska inte välja från en schablon.

### P2 — Telge är felklassificerad och dess månadsregel reduceras till en approximation

Telges nyttjandetidstillägg är redan katalogtypen `low_utilization`, och typen är redan
implementerad i både Python och TypeScript. Det är alltså inte sannolikt en ny
Telge-specifik justeringspost som kartläggningen säger.

Samtidigt använder den befintliga `incremental_return_temperature` ett enda årsvärde för
en icke-linjär månadstrappa. Kodens egen dokumentation säger att detta inte är matematiskt
ekvivalent när månader korsar trösklarna. Telge kan därför inte beskrivas som en ren
katalogändring för en exakt månadsmodell. Normalårskorrigerad energi behöver dessutom vara
obligatorisk om det exakta nyttjandetidstillägget ska beräknas.

- `Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md:125`
- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/justeringar.py:97`
- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/justeringar.py:177`

### P2 — ren energitariff ska ha ”ej tillämpligt”, inte en påhittad periodisering

För Sundsvall Indal/Liden/Lucksta föreslås en godtycklig
`days_in_month/days_in_year`-regel för en stående kostnad som inte finns. Det ger rätt
summa eftersom noll multipliceras med vad som helst, men blandar ihop ”ej tillämpligt” med
en faktisk leverantörsregel. Skillnaden är en uttrycklig invariant i Ellens SKILL.

- `Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md:126`
- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/katalog.py:513`
- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/faktura.py:1001`

Den robusta lösningen är att grinden och månadsfunktionen accepterar
`manadsperiodisering = null` endast när både kapacitetsdel och fast avgift uttryckligen är
ej tillämpliga, och då periodiserar enbart månadens uppmätta energi.

### P2 — ”kronorläget fungerar automatiskt” är ännu bara en hypotes

Den numeriska inversen återanvänder årskostnaden, men nya obligatoriska fält måste också
föras genom `Indatafalt`, TypeScripts `FALT_GRANSER`, React-valideringen och den domännära
kronorwrappern. Nya rabattsteg eller asymmetriska justeringar kan dessutom ge
diskontinuiteter eller flera rötter. Varje ny prismodell behöver därför egna rundturs-,
monotonicitets- och feltester innan kronorläget kan sägas fungera.

- `Fjarrvarmetariffer/teknisk-kartlaggning-28-tariffer.md:27`
- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/utils/besparingsvarde.ts:254`

### P3 — sammanfattningen i kommunikationsloggen räknar fel

Claude skriver att elva tariffer är rena katalogfyllnader. Själva kartläggningen redovisar
fem i grupp 1 när Matfors/Kvissleby räknas bort. Övik och Södertörn ingår redan bland dessa
fem och får inte läggas till en gång till. Antalet måste räknas om efter att obligatoriska
effektfält och månadsnoggrannhet har klassificerats korrekt.

## Det som är korrekt och kan behållas

- Baslinjecommitten innehåller exakt de fyra beställda filerna.
- Malmö/Burlövs beräkningstemperatur ska rättas från −15 till −8 °C.
- Öviks fasta bandbelopp ska ändras från `null` till 0 och periodiseringen till
  kalenderdagar.
- Vattenfalls Standard/Spetsig behöver strukturerad giltighetslogik.
- Sundsvalls rena energitariff behöver ett uttryckligt motorstöd för avsaknad av stående
  kostnad.
- Det är rätt att återanvända gemensamma byggstenar, men först efter att de tre
  flödesfamiljernas separata kontrakt är definierade.

## Begärd rättning innan implementation

Claude bör lämna en reviderad kartläggning som för varje tariff/familj anger:

1. exakt avsedd produktomfattning och vad som blockeras,
2. varje obligatorisk, frivillig och uppskattad indata med källa och tidsupplösning,
3. om årssumma och månadsresultat är exakta eller approximativa,
4. katalogtyp och fullständig formel med enheter, tecken och månader,
5. ändringar i Python, generator, TypeScript, domänwrapper och React,
6. hur MWh-läge, kronorläge, saknade värden och tariffgiltighet testas,
7. korrigerat antal verkliga katalogändringar respektive motorändringar.

Först därefter bör Robert välja första implementationbatchen.
