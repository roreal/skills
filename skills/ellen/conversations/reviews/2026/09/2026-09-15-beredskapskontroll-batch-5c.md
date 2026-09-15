---
review_id: "2026-09-15-018"
created_at: "2026-09-15T21:08:00+02:00"
reviewer: Codex
status: approved-for-local-implementation-behind-lock
scope: "Batch 5c — åtta tariffer med säsongsvis flödesavgift"
baseline_remote_heads:
  skills: "df41660620f572b5b22d7dd27332c68b1be62049"
  enkey_agents: "5eaca3c4f3eafb3c7065319803592abe062f49ae"
  neptune_academy: "28ae62945ed50b23cffadd5a7b3070cc2d5c41ae"
implementation_allowed: true
tariff_activation_allowed: false
push_allowed: false
relates_to:
  - "conversations/handoffs/2026/09/2026-09-15-batch-5c-sasongsflode.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 5c"
  - "Fjarrvarmetariffer/tariffinventering-v22.md"
---

# Beredskapskontroll: Batch 5c — säsongsflöde

## Beslut

Batch 5b är pushad och remote-verifierad. Batch 5c är startklar för **lokal
implementation bakom befintliga `investigation.status="utreds"`-spärrar**.
Ingen av de åtta tarifferna får aktiveras eller pushas i denna fas.

Batchen omfattar exakt:

1. `lulea-energi-lulea-2026`
2. `oresundskraft-helsingborg-normal-2026`
3. `oresundskraft-angelholm-normal-2026`
4. `piteenergi-pitea-centrala-natet-2026`
5. `piteenergi-norrfjarden-och-sjulnas-2026`
6. `nevel-gimo-osterbybruk-och-osthammar-2026`
7. `tekniska-verken-linkoping-linkoping-2026`
8. `malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026`

Nuvarande verifierade utgångsläge är **51 implemented / 13 ready / 28
blocked av 92** och **53 skarpa produkter**. Bakom spärr ska dessa tal vara
oförändrade. En isolerad kopia där exakt de åtta spärrarna rensas ska ge
**59/5/28** och **61 skarpa produkter**.

## Gemensamt tekniskt hinder

Katalogens `volume`-poster anger tariffens exakta debiteringsmånader, men
Pythonmotorns `_flodesavgift` och TypeScriptmotorns `flodesavgift` använder i
dag bara ett skalärt `flode_m3` och läser inte postens `months`. Ett skalärt
årstal kan därför inte bevisa vilket flöde som hör till den debiterade
säsongen.

Det säkra kontraktet för Batch 5c är en **12-elements kalendermånadsserie**:

- januari till december i fast ordning;
- varje element är fakturans/leverantörens flöde i m³ för månaden;
- motorn summerar endast de månader som står i den enskilda `volume`-postens
  egen `months`-lista och multiplicerar med postens egen sats;
- övriga månadsvärden får finnas i serien men bidrar med exakt noll till
  just denna flödesavgift.

Att i stället fråga efter ett enda säsongsaggregat skulle göra `months`
overifierbart i motor och test och skulle inte passa den redan etablerade
`number_series`-/`falt_serier`-kanalen. Tolv månadsrutor återanvänder däremot
befintligt produktkontrakt och befintlig kalenderetiketterad UI-rendering.

## Månadsomfattning som måste bevisas mekaniskt

| Tariff | Exakta debiteringsmånader | Antal |
| --- | --- | ---: |
| Luleå | jan–maj, sep–dec | 9 |
| Öresundskraft Helsingborg | jan–mar, nov–dec | 5 |
| Öresundskraft Ängelholm | jan–mar, nov–dec | 5 |
| Piteå centrala nätet | jan–mar, okt–dec | 6 |
| Piteå Norrfjärden/Sjulnäs | jan–mar, okt–dec | 6 |
| Nevel Gimo/Österbybruk/Östhammar | jan–apr, okt–dec | 7 |
| Tekniska verken Linköping | jan–apr, okt–dec | 7 |
| Mälarenergi 2–4 lägenheter | jan–apr, okt–dec | 7 |

Samma lista får inte hårdkodas för hela batchen. Varje post ska använda sin
egen kataloglista. Tester ska ändra ett inkluderat och ett exkluderat
månadsflöde och visa rätt respektive noll kostnadsdelta.

## Källkontroll 2026-09-15

Följande aktuella officiella leverantörskällor styrker 2026-priserna och
säsongsgränserna. Historiska Prisdialogen-dokument får bevaras, men får inte
ensamma bära aktuella fakta.

| Tariff | Aktuell officiell källa | Särskild avgränsning |
| --- | --- | --- |
| Luleå | `https://www.luleaenergi.se/produktion-och-infrastruktur/fjarrvarme/priser-och-avtalsvillkor/lulea-foretag-2026/` | Flödespriset 4,60 kr/m³ sep–maj anges för primäranslutning. Produkthjälpen ska avgränsa kundtypen. |
| Öresundskraft Helsingborg/Ängelholm | `https://www.oresundskraft.se/globalassets/pdf/prisdialog/prisandringsmodell/prisandringsmodell-2026-2028.pdf` | Företag Normalpris: 4,68 respektive 4,76 kr/m³ jan–mar och nov–dec. Lägg inte konsumentproduktens avkylningsvillkor på företagstarifferna. |
| Piteå centrala | `https://www.piteenergi.se/fjarrvarme/priser-foretag/` | 2,60 kr/m³ kvartal 1 och 4, alltså okt–mar. |
| Piteå Norrfjärden/Sjulnäs | `https://www.piteenergi.se/fjarrvarme/priser-2-foretag/` | 2,56 kr/m³ kvartal 1 och 4. |
| Nevel | `https://nevel.com/sv/fjarrvarme/gimo/` och `https://nevel.com/wp-content/uploads/2025/10/Nevel_prislista_foretag_Osthammar_Gimo_Osterbybruk_2026.pdf` | 3,10 kr/m³ okt–apr. Prislistans standardprodukt gäller full värmeleverans; delvärme kräver särskilda villkor. |
| Tekniska verken | `https://tekniskaverken.se/foretag/fjarrvarme/priser` | Normal flödesavgift 5,35 kr/m³ okt–apr. Lågtemperatur 2,67 är en separat fortsatt blockerad variant. |
| Mälarenergi 2–4 lägenheter | `https://www.malarenergi.se/fjarrvarme/pris-for-fjarrvarme/` | 2026 inkl. moms: fast 9 855 kr, energi 985/780/295 kr/MWh och flöde 2,00 kr/m³ jan–apr/okt–dec. Katalogens exkl.-momsbelopp 7 884, 788/624/236 och 1,60 följer exakt `/1,25`. |

Nevels publicerade exempel är ett särskilt bra oberoende kontrollvärde, men
har en viktig avrundningsdetalj. Leverantörens total 613 622,50 kr exklusive
moms motsvarar 120 kW i band 2, 520 MWh fördelat med den angivna andelen
82,2 procent (**427,44 + 92,56 MWh**, före presentationsavrundning) och
8 320 m³ okt–apr. Om de i formelraden visade avrundade talen 427,4 + 92,6
används bokstavligt blir summan i stället 613 608,76 kr. Testet ska antingen
reproducera publicerad total med de oavrundade andelstalen eller uttryckligen
förvänta det bokstavliga avrundade utfallet; det får inte påstå att båda är
samma. Facit ska kodas som statiskt tal med formeln dokumenterad och får inte
skapas av produktionsmotorn.

## Katalog- och requesträttelse

`R03` är i dag felaktigt medlemsscoperad till hela Mälarenergi och blockerar
därför även tariffen för 2–4 lägenheter, trots att frågan gäller andra
Mälarenergitabeller. Vid implementation ska:

- `R03.member_ids` ersättas av `tariff_ids` med exakt
  `malarenergi-vasteras-och-hallstahammar-storre-fastigheter-2026` och
  `malarenergi-vasteras-och-hallstahammar-gruppanslutna-smahus-2026`;
- `R03` tas bort ur 2–4-lägenheters `investigation.request_ids`;
- de två namngivna raderna fortsätta vara blockerade;
- requestens historik, fråga och `status="utreds"` bevaras.

Detta är en scopesäkring, inte ett påstående att R03 har blivit externt
besvarad.

## Krav på fail-closed `volume`-kontrakt

Batchen ska samtidigt täppa till den nuvarande strukturluckan för
`volume`-poster:

- en typspecifik sluten schemavalidering ska kräva exakt nyckelmängd,
  `unit="SEK/m3"`, ändlig positiv `rate` samt en icke-tom lista med unika
  heltalsmånader inom 1–12;
- en kontraktsstyrd tariff får ha exakt en `volume`-post;
- fullårslistan 1–12 kräver fortsatt exakt ett skalärt, policybundet
  `flode_m3` med `vardetyp="number"` — Batch 5b och tidigare aktiva
  helårstariffer får inte ändras;
- en riktig delmängd av 1–12 kräver exakt ett policybundet `flode_m3` med
  `vardetyp="number_series"`, `antal_varden=12`, `minvarde=0`, annual-scope
  och endast `supplier_value`; serien är ett historiskt/fakturerat
  kalenderunderlag för en framåtriktad uppskattning och ska därför ha
  `rullande=False` samt `takad_till_snapshot=True` — särskilt viktigt för
  Mälarenergi, som saknar ett annat effektfält som annars takar statusen;
- fel typ, saknat fält, fel kardinalitet, negativt/icke-ändligt element,
  dubblett-/felaktig månad eller dubblerad `volume`-post ska blockera före
  kostnadsberäkning;
- direkt motoranrop som försöker kringgå preflight ska också kasta, inte
  använda MWh/ΔT-reserven för en säsongspost.

Det gemensamma fältnamnet `flode_m3` kan återanvändas: det är policyens
`vardetyp` och postens egen `months` som diskriminerar skalär helårsdata från
tolv månadsdata. `resultatkontrakt` transporterar redan serier via
`falt_serier`.

## Tariffspecifik indata och resultatstatus

Sju tariffer kräver leverantörens effekt, bekräftat band-ID och tolv
månadsflöden. Mälarenergi 2–4 lägenheter har `capacity:null` och ska därför
inte visa eller kräva effekt/band — bara tolv MWh och tolv flödesvärden,
utöver katalogens fasta årsavgift.

All visning gäller mwh-läget. Kronor, schablon och besparing förblir
blockerade. Resultatet är en uppskattad framåtriktad årskostnad och ska vara
`annual/snapshot/complete`, aldrig `exact`. Okänd månadsvis periodisering av
årsvisa effekt-/fastprisdelar får inte uppfinnas.

Luleå ska avgränsas till primäranslutning, Nevel till full värmeleverans och
Linköping till normaltemperatursystem. De separata specialvarianterna ska
förbli blockerade.

## Acceptansgrind före Codex-granskning

Leveransen måste innehålla speglade Python-/TypeScript-prov genom faktisk
katalog, policy, kontraktsfasad och motor:

- oberoende handräknat golden-facit för alla åtta;
- alla band-ID:n för var och en av de sju kapacitetstarifferna, plus
  saknat/tomt/okänt band och saknad/ogiltig effekt;
- exakt 5-, 6-, 7- och 9-månaderssemantik, inklusive delta-prov för
  inkluderad respektive exkluderad månad;
- felmatris för serien: saknad, skalär i stället för serie, 11/13 element,
  tomt element, sträng, negativt, NaN/oändlighet och över maxvärde;
- Mälarenergi utan effekt-/bandfält och med fast årsavgift;
- R03:s två kvarvarande blockeringar och frisläppt 2–4-lägenhetsrad i den
  isolerade kopian;
- oförändrat skalärt fullårsflöde för Batch 5b/VänerEnergi och oförändrad
  MWh/ΔT-reserv endast för Mölndals icke-kontraktsstyrda legacyväg;
- en riktig renderad React-väg från isolerat genererad policy, produktbyte
  mellan olika månadsuppsättningar samt till/från Mälarenergi, utan
  kvarhängande tariffspecifik indata;
- minst två omockade isolerade E2E-scenarier: en tariff med kapacitet
  (Luleå) och Mälarenergi utan kapacitet;
- mekaniska räkningsgrindar 51/53 skarpt och 59/61 i isolerad
  kandidatuppsättning.

Efter implementation ska Claude committa fokuserat lokalt i berörda repon,
logga exakta hashar och testutfall och stanna. Ingen aktivering, ingen push
och ingen handredigering av genererade filer eller `dist/`.

## Bedömning

**Godkänd för lokal implementation bakom spärr.** Nästa beslutspunkt är
Codex kodgranskning. Tariffaktivering kräver därefter ett separat tekniskt
slutgodkännande och Roberts uttryckliga klartecken; push kräver en ny separat
kontroll.
