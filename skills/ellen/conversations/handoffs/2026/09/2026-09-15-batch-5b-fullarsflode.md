---
handoff_id: "2026-09-15-001"
created_at: "2026-09-15T10:57:00+02:00"
from: Codex
to: Claude
status: ready-for-local-implementation
implementation_allowed: true
approved_implementation_scope: "batch-5b-six-full-year-volume-tariffs-and-jonkoping-access-coverage"
tariff_activation_allowed: false
push_allowed: false
review_required_before_activation: true
review_required_before_push: true
baseline_remote_heads:
  skills: "cd0bdb2e4fa33b753305d8983fda952aab43afdc"
  enkey_agents: "4d5f8a66e68ff4439ed379377d456230938962df"
  neptune_academy: "6331f27420c10e7104b002d97ad7ba67bb647040"
tariff_disposition_before: "45 implemented / 19 ready / 28 blocked av 92"
tariff_disposition_during_implementation: "45 implemented / 19 ready / 28 blocked av 92"
tariff_disposition_after_future_approved_activation: "52 implemented / 12 ready / 28 blocked av 92"
sharp_products_before: "47"
sharp_products_during_implementation: "47"
sharp_products_after_future_approved_activation: "53"
relates_to:
  - "conversations/reviews/2026/09/2026-09-15-beredskapskontroll-batch-5b.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 5b"
  - "Fjarrvarmetariffer/tariffinventering-v22.md — §4.1, §5, §6a.2 och §7"
  - "Fjarrvarmetariffer/verifieringslista-fjarrvarmebolag.md"
---

# Uppdrag till Claude: Batch 5b — fullårsflöde och Jönköpings accessavgift

## Mål och stoppunkt

Implementera lokalt exakt dessa sex `annual_forward`-produkter bakom deras
befintliga `investigation.status="utreds"`-spärrar:

1. `borlange-energi-borlange-2026`
2. `falu-energi-vatten-falun-2026`
3. `falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo-2026`
4. `habo-energi-habo-2026`
5. `mjolby-svartadalen-energi-mjolby-2026`
6. `jonkoping-energi-jonkoping-och-granna-2026`

Bygg samtidigt Jönköpings räknade `--accessavgift`-täckning som ett
obligatoriskt val i bastariffen. Skapa ingen separat katalograd, inget separat
leverantörsalternativ och ingen dubblettprodukt.

Kalkylen ska skapa uppskattad årskostnad från tolv MWh-värden,
leverantörens effekt, bekräftat band och fakturans fullårsflöde. Jönköping
ska dessutom lägga till rätt accessavgift per central och månad.
Resultatstatus ska vara `annual/snapshot/complete`, aldrig `exact`.

Detta är endast implementation bakom spärr. **Rensa inte
`investigation`, regenerera inte in kandidaterna i skarp payload, aktivera
inte och pusha inte.** Commitera fokuserat lokalt i berörda repon,
dokumentera hash/tester och stanna för Codex kodgranskning.

## 1. Rätta plan och källproveniens först

Synka de levande Batch 5b-avsnitten i `batchplan-v22.md` och
`tariffinventering-v22.md` med följande bindande fakta:

- alla sex behöver tre grundkrav: effekt + bekräftat band-ID + `flode_m3`;
- alla sex har `supplier_confirmed_band_id_required`, inte bara Borlänge;
- Jönköpings accessavgift byggs i denna batch och är ingen egen produkt;
- Habo använder inte den nuvarande katalogtextens rullande topp-tre-metod.

Verifiera och spåra dessa aktuella officiella källor med
`retrieved_on=2026-09-15`:

| Tariff | Officiell källa | Katalogkrav |
| --- | --- | --- |
| Borlänge | `https://www.borlange-energi.se/kontakta-oss/priser/fjarrvarmepris-for-naringsidkare` | Uppdatera `borlange-web`; sidan styrker 2026-priser, helårsflöde och rullande effekt. |
| Falu båda nät | `https://fev.se/varme--kyla/fjarrvarme/avtal-och-priser-foretag.html` | Uppdatera `web-review-falu-final`; sidan styrker båda tabellerna, 3,5 kr/m³ och årsrevision 1 april. |
| Habo | `https://www.haboenergi.se/varme-miljo-foretag/` | Lägg aktuell webbkälla och rätta `billing_basis_method` till leverantörens tvååriga normalårsmodell; bevara priser exkl. moms. |
| Mjölby | `https://www.mse.se/foretag/fjarrvarme/priser` | Uppdatera titel/datum för `web-review-mjolby-final`; sidan styrker pris, flöde och årsvis tvåårsmedel för effektsignaturen. |
| Jönköping priser | `https://jonkopingenergi.se/foretag/fjarrvarme/fjarrvarme/priser` | Lägg aktuell webbkälla för 2026-priser, 3,7 kr/m³ och 0/10/25/50 kr per central/månad. |
| Jönköping effekt | `https://jonkopingenergi.se/foretag/kundcenter/guider/vad-bestar-fjarrvarmekostnaden-av` | Sätt `billing_basis_method` till medel av de tre högsta av de fem högsta dygnsmedeleffekterna senaste tolv månaderna. |

Råhämtningar ska inte committas. Historiska Prisdialogen-källor får bevaras
som stöd men inte stå ensamma för aktuella Habo-/Jönköpingsdata.

## 2. Katalog och policyer bakom spärr

Sätt `contract_required:true` på samtliga sex men bevara
`production_ready:false` och `investigation.status="utreds"`.

Varje policy ska ha `tackning={"annual_forward"}`,
`stodjer_aktuell_arskostnad=True`, `stodjer_besparing=False` och:

- ett tariffspecifikt numeriskt effektfält bundet med
  `kapacitet_bindning`;
- ett tariffspecifikt `band_id`-fält bundet med
  `kapacitet_band_bindning`, även för Habos enda band;
- det gemensamma numeriska `flode_m3`, obligatoriskt för `annual`, källa
  `supplier_value`, `minvarde=0`, lämpligt övre säkerhetstak och hjälptext
  som anger fakturans fullårsflöde.

Effektfältens periodmetadata ska vara källsann:

- Borlänge och Jönköping: `rullande=True`;
- Falu tätort och ytterorter, Habo och Mjölby: inte rullande; använd
  `takad_till_snapshot=True` för leverantörsvärdet som revideras årsvis
  eller bygger på ett fast flerårsunderlag.

Falu ytterorters effektkrav ska ha `maxvarde=500`. 500 med bekräftat band 4
är giltigt; varje högre värde blockerar utan extrapolering. Normalisera
Borlänges och Falu ytterorters issues till grindens kända språk. Flytta R04
och R15 från `remaining_information_requests` till
`resolved_information_requests`, på samma sätt som R05/R12/R13:

- R04:s 559 kr/MWh september–oktober är verifierat på den aktuella
  2026-sidan. Exakt 501 kW är fortfarande källmässigt oklart, men inte
  längre produktblockerande eftersom bekräftat leverantörsband krävs.
- R15 är inte externt besvarad men inte längre produktblockerande: Falu
  ytterorter stoppar mekaniskt över 500 kW som specialavtal. Ta samtidigt
  bort den felaktiga medlemsvida R15-kopplingen från Falu tätort.

Bevara frågornas historik och skriv sanningsenliga status-/resolutionstexter
och `change_log`; markera inte 501-gränsen eller ytterorternas specialavtal
som externt verifierade.

## 3. Stäng `volume`-reservvägen för kontraktstariffer

Lägg en generell korsvalidering i aktiveringspreflighten för varje
kontraktsstyrd tariff som har en `volume`-post. Den ska kräva exakt ett
policyfält `flode_m3` med:

- `vardetyp="number"`;
- `"annual"` i `kravs_for`;
- `supplier_value` som tillåten källa;
- `minvarde=0`;
- transport till motorns generiska `falt`-kanal.

Saknat, negativt, icke-ändligt eller över maxvärdet ska blockera med ett
fältnära fel innan kostnadsberäkning. Bevisa i test att den kontraktsstyrda
vägen aldrig faller tillbaka på `MWh/(1,163×45)`. Ändra inte det befintliga
legacybeteendet för redan aktiva icke-kontraktstariffer i denna batch.

## 4. Jönköpings accessavgift — en kostnadsdel, inte UI-dekoration

Inför en sluten justeringstyp i Python, TypeScript, katalogvalidator och
generator med två explicit refererade policyfält:

1. valt pris per central/månad — numeriskt enum med exakt allow-list
   `0, 10, 25, 50`, obligatoriskt och utan default;
2. antal värmeundercentraler — heltal 1–20, bundet till kalkylatorns redan
   befintliga globala `substations`-värde.

Årskostnaden är `pris × 12 × antal`. Beloppen är exklusive moms och ska gå
genom samma momsbehandling som övriga kostnadsdelar. Ett uttryckligt val 0
är giltigt; tomt/saknat/20/feltypat enum blockerar. Antal 0, 21, decimal,
NaN eller oändlighet blockerar.

Undvik dubbla formulärfält: lägg vid behov en explicit
`antal_undercentraler_bindning` i policykontraktet, låt produktadaptern
injicera det validerade `substations`-värdet och filtrera just denna bindning
ur `policyFaltMetadata`. Lägg en sann källtyp, exempelvis
`customer_value`, i den slutna Python-/TypeScript-unionen om bindningen
annars skulle tvingas märkas felaktigt som `supplier_value`.

Accesspostens aktiveringspreflight ska korsvalidera båda fältnycklarna,
allow-listen, heltals-/intervallkravet och annual-omfattningen mot den
faktiska policyn före generering. Motorn ska också kasta tydligt om en
direktanropare kringgår preflighten.

UI-valets etiketter ska beskriva alternativen:

- 0 — ingen tillkommande avgift/nyckeltub;
- 10 — elektronisk kod;
- 25 — nyckel eller tagg hos Jönköping Energi;
- 50 — ledsagning av fastighetsskötare.

Hjälptexten ska ange att posten gäller per central och månad för fastighet
med tillsynstjänst och avtal tecknat från och med 2024. Kunden ska göra ett
aktivt val även när värdet är 0.

## 5. Oberoende tester

Lägg permanenta, speglade Python-/TypeScript-prov genom verklig katalog,
policy, kontraktsfasad och motor:

- ett oberoende handräknat golden-facit per bastariff som inkluderar
  energi, bandets `fixed + variable × effekt`, `flode_m3 × rate` och moms;
- samtliga band-ID:n, plus saknat/tomt/okänt band för alla sex
  (tariffidentiska fixturer får härledas mekaniskt från Pythonkällan, inte
  handkopieras mellan språk);
- saknat/ogiltigt flöde samt bevis att ändrat flöde ändrar facit med exakt
  `delta_m3 × rate` före moms;
- Falu ytterorter vid 500 respektive över 500 kW;
- Jönköpings fyra giltiga accessval, saknat/tomt/okänt val och både 1 och
  flera undercentraler; skillnaden inklusive moms ska vara
  `delta_rate × 12 × antal × 1,25`;
- produktbyte nollställer tariffspecifika effekt-/band-/flödes-/accessfält
  men bevarar och återanvänder det globala antalet undercentraler;
- kronor, schablon och besparing förblir blockerade;
- en riktig renderad React-testväg från genererad/isolert genererad policy,
  inte en handbyggd policydublett;
- ett omockat E2E-scenario för Jönköping med minst två undercentraler och
  ett icke-noll accessval;
- regressionsprov för Mölndals legacy-`volume`, Batch 3:s `flode_m3`,
  Batch 4, Batch 5a samt generatorns nollutsläpp bakom spärr.

Golden-förväntningar ska räknas direkt från dokumenterade formler och
statiska tal. De får inte genereras genom `calcResult`,
`beraknaArsprodukt`, motorn själv eller en kopia av produktionsalgoritmen.

## 6. Räkningsgrind och leverans

Under implementationen ska följande bestå:

- disposition: `45/19/28 av 92`;
- godkända katalograder: 45;
- skarpa produkter: 47;
- inga Batch 5b-ID:n i skarp genererad payload.

En isolerad kopia där exakt de sex Batch 5b-spärrarna rensas ska ge:

- 51 godkända katalogprodukter;
- 53 skarpa produkter inklusive två leverantörsfilsprodukter;
- disposition `52/12/28`, eftersom den inbyggda accessavgiften räknas som
  en egen täckningspost men inte som en produkt.

Kör minst full Python-svit, full TypeScript-svit, `tsc --noEmit`, isolerat
produktionsbygge, full E2E och `git diff --check` i berörda repon. Redovisa
exakta testantal och fokuserade commit-hashar. Rör inte användarägda
oannonserade filer eller `neptune-marketing/dist`.

## 7. Aktiveringsrapport (2026-09-15, efter Codex slutgranskning
`2026-09-15-015` och Roberts uttryckliga klartecken "Ja starta")

Denna sektions §6-disposition `52/12/28` (och frontmatterns
`tariff_disposition_after_future_approved_activation`, samma tal) visade
sig INTE mekaniskt korrekt — den byggde på ett antagande att den inbyggda
accessavgiften skulle räknas som en egen täckningspost. Den mekaniskt
räknade (`godkanda(katalog, policyregister=POLICYREGISTER)`) dispositionen
efter aktivering är i stället **51 implemented / 13 ready / 28 blocked av
92**, exakt matchande Codex slutgranskning `2026-09-15-015`s tal. Skarpa
produkter: **53** (51 katalog + 2 leverantörsfiler), mekaniskt parsat ur
den genererade `TARIFFER`-ordboken.

Frontmatterns fält (skrivna av Codex, ej ändrade här) lämnas oförändrade
per instruktion — läs `51/13/28` som det korrekta, mekaniskt bekräftade
talet framåt, inte handoffens ursprungliga `52/12/28`.

Aktivering utförd: `investigation` satt till `null` för exakt de sex
namngivna tarifferna (`skills@c2fcdd9`), `tariffer.generated.ts`
regenererad från den riktiga generatorn (`enkey-agents@5eaca3c`,
`neptune_academy@28ae629`) — mekaniskt diffat: exakt sex nya produkter,
noll ändrade äldre. Ingen push.

Stanna därefter för Codex kodgranskning. Ingen aktivering och ingen push.
