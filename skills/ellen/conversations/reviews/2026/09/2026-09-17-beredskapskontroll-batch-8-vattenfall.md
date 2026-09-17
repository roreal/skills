---
review_id: "2026-09-17-010"
date: "2026-09-17"
reviewer: Codex
status: "approved-for-local-implementation-behind-gate"
approved_by: Codex
dispatched_by: agent-bridge
implementation_allowed: true
activation_allowed: false
push_allowed: false
history_rewrite_allowed: false
scope: "batch-8-vattenfall-12-public-calculator-estimates"
reviewed_heads:
  skills: "55491dbfd92fcae2caf896f9a9457f1582d834c8"
  enkey_agents: "6059d5ec08858bdfa992065943220bdad6522c92"
  neptune_academy: "5c1bd8821cc288204b5a7bfb466b918ff61403a5"
live_remote_heads:
  skills: "0df504ed227126b5fd36f87f99b4e240001a99d5"
  enkey_agents: "6059d5ec08858bdfa992065943220bdad6522c92"
  neptune_academy: "22b473d30980051fb87a936b3d824c53b63d58e8"
---

# Beredskapskontroll: Batch 8 — Vattenfall, tolv uppskattade årsprodukter

## Beslut

Batch 8 är redo för **lokal implementation bakom de befintliga
`investigation`-spärrarna**. Omfattningen är de tolv befintliga katalograderna:
Standard och Spetsig för Haninge/Tyresö/Älta, Gustavsberg,
Motala/Askersund, Nyköping, Uppsala och Vänersborg.

Ingen av raderna får aktiveras i detta steg. Ingen push och ingen
historikomskrivning är tillåten. Batch 7:s separata publiceringshistorik och
den nu konstaterade skillnaden mellan lokala och externa repo-HEAD:ar ska
inte blandas in i Batch 8. Implementationens första stoppunkt är
`REVIEW_READY: Codex`.

Skarpt läge ska under implementationen förbli:

- 86 fysiska katalograder;
- 61 godkända katalograder;
- 63 genererade produkter;
- disposition `62 implemented / 2 ready / 28 blocked av 92`.

En isolerad framtida aktiveringsprojektion ska ge 73 godkända
katalograder, 75 produkter och disposition `74/2/16`. Projektionen är ett
test, inte en aktivering.

## Källbeslut

Normerande underlag är Vattenfalls officiella 2026-prislistor, den publika
företagskalkylatorn och FAQ:n om Standard/Spetsig. De lokala PDF-kopiorna
och `/tmp/vattenfall-*` är revisionsunderlag och ska inte automatiskt
committas.

Den publika kalkylatorns observerade modell är:

- energipris per kalendermånad;
- årseffektpris Standard per nät och 1 724 kr/kW för Spetsig;
- profilerna flerbostadshus `17,17,11,9,4,2,1,1,3,8,10,17`, industri
  `15,16,10,9,4,3,2,2,4,8,10,17` och lokal
  `14,14,10,9,5,4,2,3,5,9,10,15` procent januari–december;
- volymrabatt på oktober–april med 0/5/10/20/25/30 kr/MWh och
  gränserna 0, 250, 1 250, 2 500, 5 000 och 7 500 MWh;
- kategoriskt flödesval `-7,5/-3,75/0/+3,75/+7,5 m³/MWh` under
  oktober–april.

Kalkylatorns kod multiplicerar samtliga fem flödesval med 4 kr/m³.
2026-prislistorna anger däremot den verkliga tariffen asymmetriskt: premie
4 kr/m³ vid bättre avkylning och avgift 6 kr/m³ vid sämre avkylning. Batch
8 får därför återskapa kalkylatorns **uppskattning** med 4 kr/m³, men
resultat och hjälptext måste uttryckligen upplysa om att en positiv
flödesavvikelses verkliga avgift kan vara högre. Typen får inte återanvända
den befintliga fakturanära `asymmetric_flow_difference`-semantiken.

Officiella PDF:er anger dessutom överuttagsavgift och 150 kr/MWh avdrag
för tillverkande industri. Den publika kalkylatormodellen räknar inte dessa
poster. De ska bevaras som dokumenterade exkluderingar och visas för
användaren; de får varken räknas som noll eller ligga kvar som okända
`adjustments` som motorn tyst ignorerar.

## Bindande beräkningskontrakt

### Kapacitet och produktklass

Användaren ska ange Vattenfalls abonnemangs-/kalkyleffekt i kW. Den
prissätts som ett årsbelopp utan dold effektuppskattning i Ellen.

Standard gäller vid energi/effektförhållande `>= 1,2`; Spetsig vid `< 1,2`.
Valideringen ska vara generisk och katalogstyrd, inte ett villkor på ett
hårdkodat tariff-ID. Antingen ska två separata, tydligt namngivna
leverantörs-/kundvärden bindas till katalogens `eligibility`-regel:

1. energi i MWh under närmast föregående 1 maj–30 april; och
2. medelvärdet i kW av periodens tre högsta uppmätta timmedeleffekter,

eller så ska en uttrycklig, attesterad leverantörsbekräftelse av vald
produkt bäras av kontraktet. Ett vanligt års-MWh-värde dividerat med
abonnemangseffekten får inte tyst användas som ersättning för den
publicerade behörighetsdefinitionen.

### Energiprofil

Vattenfalls tre publicerade profiler ska vara synliga val. Profilvalet ska
styra de tolv energimängder som faktiskt når motorn. Det är inte
tillräckligt att bara rendera ett profilfält och sedan fortsätta räkna med
Ellens generella `fordelaEnergi`-profil.

Implementera en generell, statiskt verifierad bindning mellan ett
policyfält och katalogens profilregister. Bindningen ska minst kontrollera
att:

- exakt tolv ändliga, icke-negativa vikter finns;
- vikterna summerar till 100 procent;
- policyfältets allow-list och etiketter är bijektiva mot profil-ID:na;
- den omfördelade månadsserien summerar tillbaka till den angivna
  årsenergin;
- Python och TypeScript ger samma månadsserie.

En egen tolvmånadsprofil kan läggas till om den hinner få samma bindning,
summagrind och fältnära fel. Den får inte införas som en obunden, fri
sidokanal. De tre officiella profilerna är minsta godkända scope.

### Volymrabatt och flödesestimat

Skapa två nya, separat namngivna justeringstyper i båda motorerna:

1. säsongsbegränsad volymrabatt: band väljs från hela års-MWh men
   avdraget appliceras bara på oktober–april;
2. kategoriskt flödesestimat: vald avvikelse i m³/MWh × 4 kr/m³ ×
   samma sju månaders MWh.

Båda typerna ska ha slutna payloadscheman, statisk policybindning där
kundindata används, egen runtimevalidering och exakt språkparitet. De får
inte byggas genom att ge de befintliga helårs-/fakturaformerna en andra,
villkorad betydelse.

## Katalogrättelser inom implementationssteget

Följande får och ska rättas utan att aktiveringsspärren tas bort:

- `schema_version` och `as_of` ska synkas med en ny, unik change-log-revision;
  toppfältet stannade felaktigt på `0.1.25`/2026-09-15 medan
  change-log redan innehåller 0.1.26 och 0.1.27;
- källnotens `±7,5/±3,75 kr` ska rättas till `m³/MWh`;
- bind de officiella 2026-PDF:erna med URL, hämtdatum och verifierad hash;
- sätt källstyrkt `valid_from=2026-01-01`, fast kapacitetsdel 0 kr,
  årsperiod och en entydig årsperiodisering för kalkylestimatet;
- ersätt de tre gamla justeringsposterna med de två beräkningsbara
  kalkylestimattyperna och en uttrycklig struktur för exkluderade poster;
- flytta motsägande gamla `issues` och `investigation.conditions_sv` till
  daterad historik och lämna endast nuvarande implementationskrav aktiva;
- sätt `contract_required=true` för samtliga tolv rader, men behåll
  `investigation.status="utreds"` och `production_ready=false`.

## Oberoende facit och acceptansprov

Minst ett goldenfall ska handräknas utan produktionsmotorn. För Uppsala
Standard, 1 000 MWh, flerbostadsprofil, 300 kW och flödesval 0 blir:

- energi: 680 080 kr exkl. moms;
- effekt: 397 800 kr exkl. moms;
- volymrabatt: -4 450 kr exkl. moms;
- flöde: 0 kr;
- totalt: **1 073 430 kr exkl. moms**, eller **1 341 787,50 kr inkl.
  moms**.

Samma fall med `+7,5` respektive `-7,5 m³/MWh` ska ge kalkylatorns
symmetriska flödesändring `+26 700` respektive `-26 700` kr exkl. moms.
Testet ska samtidigt kontrollera att UI:t upplyser om den verkliga
6-kronorsavgiften på den positiva sidan.

Acceptansmatrisen ska dessutom omfatta:

- alla tolv tariff-ID:n och samtliga sex nätprisuppsättningar;
- alla tre profiler och månadsordningen januari–december;
- rabattgränserna 249/250, 1 249/1 250, 2 499/2 500,
  4 999/5 000 och 7 499/7 500 MWh;
- samtliga fem flödesval samt okänt värde;
- Standard/Spetsig exakt under, på och över 1,2;
- saknad/negativ/NaN/oändlig effekt, behörighetsindata och profil;
- strukturella mutationer av månader, profilvikter, enhet, sats,
  fältnamn och extra payloadnycklar;
- oberoende Python-/TypeScript-goldenfall, genererad data, React-test,
  ordinarie browser-E2E och en isolerad kandidat där exakt de tolv
  `investigation`-spärrarna tas bort i minnet;
- full Python-svit, full TypeScript-svit, `tsc`, bygge och
  `git diff --check`.

## Arbetskopior och publiceringsspärr

Följande är uttryckligen utanför tariffdiffen och ska bevaras:

- skills-repots råmejl, PDF:er, frågedokument, `AGENTS.md`, `SKILL.md`,
  automationsfiler och andra redan inventerade filer;
- `../milesight`;
- `enkey-agents` befintliga HEAD `6059d5e` och dess EG71-ändring;
- `neptune-marketing/dist/` exakt som det ligger;
- hela Batch 7:s commit-/publiceringsfråga.

Live-remoterna är asymmetriska: enkey-agents remote pekar på nuvarande
lokala HEAD, medan skills och neptune_academy fortfarande pekar på de
tidigare baserna. Det är i sig ett absolut pushstopp för denna batch.
Claude ska inte fetch/rebase/merge/reset eller försöka "rätta" historiken
inom Batch 8.
