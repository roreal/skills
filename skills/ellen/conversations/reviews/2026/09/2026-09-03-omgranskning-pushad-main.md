---
review_id: "2026-09-03-002"
date: "2026-09-03"
reviewer: Codex
status: completed
scope:
  - enkey-agents tariffmotor efter åtgärdsrundan
  - neptune_academy energipotential-kalkylator efter åtgärdsrundan
reviewed_heads:
  enkey-agents: "b658d71"
  neptune_academy: "8a0b603"
remote_verified: true
---

# Omgranskning: tariffmotorns pushade main

## Bedömning

Den pushade implementationen är betydligt bättre än den tidigare versionen.
De båda lokala `main`-grenarnas HEAD matchar `origin/main` på GitHub. Den
ursprungliga P1-bristen där Gotlands rabattband kunde glida mellan
före/efter-fakturan är rättad när besparingen beräknas, stale resultat döljs
vid ändrad indata, temperaturfältens årsapproximation är dokumenterad och
Python/TypeScript har nu samma halvtalsavrundning.

Jag kan däremot inte bekräfta formuleringen att samtliga tidigare fynd är
helt stängda. Ett känt fel finns kvar i ett nuvarande användarflöde: Gotlands
kronor-till-MWh-invers när föregående års energi inte fylls i. Dessutom
beskriver kvalitetsmärkningen inte längre de faktiska orsakerna till hög,
medel eller låg kvalitet, och produktionsgrinden är fortfarande bara strikt
för fyra av flera katalogfält som påverkar beräkningens betydelse.

## Fynd

### P1 — Gotlands kr-läge kan fortfarande lösa ut fel energi när föregående år saknas

Det nya `foregaende_ars_mwh`-fältet är rätt modellvariabel och fungerar när
det anges. Men fältet är frivilligt och har `default: null`:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/data/tariffer.generated.ts:557`

När det lämnas tomt skickar UI:t inget värde till inversen:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.tsx:242`

Pythonmotorn väljer då rabattband från varje prövad MWh-kandidat i själva
rotsökningen:

- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/faktura.py:431`
- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/faktura.py:902`

Det innebär fortfarande att den okända energin både är det som ska lösas ut
och grunden för att välja föregående års rabattband. Jag byggde en riktig
årskostnad för 2 499 MWh med ett känt föregående-årsvärde och löste sedan
tillbaka den:

| Föregående år | Rätt resultat med fält | Resultat utan fält | Fel |
| ---: | ---: | ---: | ---: |
| 100 MWh | 2 499,000 MWh | 2 528,750 MWh | +29,750 MWh |
| 2 499 MWh | 2 499,000 MWh | 2 508,917 MWh | +9,917 MWh |
| 2 501 MWh | 2 499,000 MWh | 2 489,123 MWh | −9,877 MWh |

Detta är inte bara en framtida Ellen-integration: kalkylatorns nuvarande
Gotland-flöde tillåter kronor per år samtidigt som det kollapsade
fakturafältet lämnas tomt. Att datakvaliteten sänks är bra, men det gör inte
den här inversen entydig eller korrekt.

Rekommendation: kräv föregående kalenderårs MWh för Gotlands kronor-läge,
eller visa ett intervall/scenario per möjligt rabattband. En ensam härledd
MWh-siffra bör inte presenteras som om problemet hade en bestämd lösning.

### P2 — Datakvalitetens etiketter beskriver inte beräkningens verkliga underlag

`calcConfidence` sänker nu kvaliteten för uppskattad kapacitet och minst ett
fält med `ar_gissning`, vilket är en förbättring:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/utils/energiPotential.ts:268`

Men samma tre etiketter är fortfarande hårdkodade som:

- hög: faktisk energi angiven,
- medel: baserad på schablon,
- låg: schablon med värmeåtervinning.

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/utils/energiPotential.ts:560`

Det stämmer inte längre med tillståndsmaskinen. I kr-läget räknas en
baklängesberäknad MWh som `userProvided`, eftersom sidan skickar den som
`energyMwh`; kvaliteten kan därför bli hög trots att användaren aldrig har
angett faktisk energi. Medel kan bero på uppskattad kapacitet eller ett
gissat tarifffält, inte på energischablon. Låg kan uppstå av två sådana
nedgraderingar utan värmeåtervinning.

Bedömningen väger dessutom bara in `ar_gissning`. Norrenergis enda årliga
returtemperatur är uttryckligen en approximation av en månadsmodell men har
`ar_gissning: false`, så den påverkar inte kvaliteten:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/data/tariffer.generated.ts:903`
- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.tsx:323`

Rekommendation: låt resultatet bära strukturerade kvalitetsorsaker och bygg
texten från dem, exempelvis `energy_source`, `capacity_source`,
`assumed_fields` och `annual_temperature_approximation`. En sammanfattande
nivå kan finnas kvar, men dess text måste vara sann för varje väg till nivån.

### P2 — "Försiktigt standardvärde" är fortfarande inte sant för alla fält

Resultatvyn säger generellt att saknade fakturafält använder ett
"försiktigt standardvärde":

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.tsx:789`

Göteborgs standard är noll temperaturavvikelse och Gotlands avkylning
standardiseras till nollbidrag. Om den verkliga fakturan innehåller en bonus
(negativ justering) ger nollbidraget en högre kostnad och potentiellt högre
besparing än kundens verkliga tariffutfall. Standardvärdet är neutralt i
formeln, men inte alltid konservativt för besparingen:

- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/faktura.py:474`
- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/faktura.py:489`

Rekommendation: skriv "neutralt eller härlett standardvärde" och redovisa
för varje fält om antagandet kan under- eller överskatta besparingen.

### P2 — Produktionsgrinden är fortsatt fail-open för flera betydelsebärande katalogfält

Åtgärden gör `vat_basis`, kapacitetens `rate_period`, `basis_unit` och
`formula` strikta. Det är korrekt. Grinden kontrollerar däremot fortfarande
inte bland annat:

- tariffens `currency` och `price_year`,
- energiprisets `unit`,
- kapacitetens `fixed_unit` och `variable_unit`,
- känd justeringstyps `formula` och `unit`,
- `fixed_charge.unit` eller dess periodisering när `capacity` är `null`.

Jag muterade en minimal i övrigt giltig tariff separat för vart och ett av
dessa fall. `currency="EUR"`, `energy.unit="EUR/kWh"`,
`capacity.fixed_unit="EUR"`, `capacity.variable_unit="EUR/kW"`,
`price_year=null`, en känd justeringstyp med okänd formel/enhet samt en fast
avgift med okänd enhet/periodisering passerade alla `grind()` med `None`.

Översättningen antar sedan fortfarande kW, år, exklusive moms eller en
standardperiodisering på vissa direkta anropsvägar:

- `/Users/robertrennel/Code/enkey-agents/tools/tariffer/katalog.py:451`

Ingen av katalogens sex nu godkända tariffer har de muterade värdena, så
detta är främst en risk vid nästa kataloguppdatering. Men det ursprungliga
kravet var en godkännandelista för alla fält som påverkar formel, enhet,
period och moms; den egenskapen är ännu inte uppfylld.

Rekommendation: validera hela det beräkningsbara kontraktet mot ett schema
eller explicita register innan `till_prisar`, och ta därefter bort
fail-open-defaultvärdena ur översättningen.

### P3 — Kontaktunderlaget är förbättrat men inte fullt reproducerbart

Leverantör, prisår och explicit ifyllda fakturafält följer nu med, vilket
stänger den viktigaste delen av det tidigare fyndet. För standardvärden
skickas dock bara ordet `standardvärde`, inte det numeriskt resolverade
värdet. I MWh-läget säger energikällan bara "Angiven av användaren
(MWh/år)" utan den angivna totalen:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.tsx:218`
- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.tsx:383`

Underlaget kan därför återskapas endast genom att ha samma kodversion och
känna till hur dynamiska defaultvärden resolverades. Det är inte en
fristående beräkningsögonblicksbild.

Rekommendation: skicka tariff-id/version, rå totalenergi och varje faktiskt
använt normaliserat fältvärde med källmarkering (`invoice`, `derived`,
`neutral_default`).

## Bekräftade rättningar

- Gotlands föregående-årsband resolveras en gång och hålls konstant mellan
  före- och efter-fakturan i `beraknaBesparingsvarde`.
- Resultatet och dess metadata rensas vid relevanta formulärändringar.
- Temperatur- och avkylningsfältens årsapproximation är tydligt dokumenterad.
- `ar_gissning` påverkar nu den sammanfattande kvalitetsnivån.
- De fyra uttryckligen ändrade katalogfälten valideras fail-closed.
- Exakta positiva halvtal avrundas lika i Python och TypeScript.
- TypeScripts fältgränstabell innehåller det nya föregående-årsfältet och har
  ett regressionstest mot den genererade katalogen.

## Verifiering

- `enkey-agents`: 173 tester godkända.
- `neptune-marketing`: 214 tester godkända.
- TypeScript: `npx tsc --noEmit` godkänd.
- Produktionsbygge: `npm run build` godkänt; endast befintlig varning om
  stor JavaScript-bundle rapporterades.
- `enkey-agents` HEAD `b658d71` matchar GitHubs `origin/main`.
- `neptune_academy` HEAD `8a0b603` matchar GitHubs `origin/main`.
- Båda implementationsrepona var rena efter verifieringen.
- Inga implementationsfiler ändrades under omgranskningen.

## Kvarstående tidigare risker

Det tidigare uppskjutna indataskyddet är oförändrat: direkta motoranrop kan
fortfarande skicka `NaN`, felstavade nycklar eller värden som klampas utan
spårbar varning. Det är inte en normal HTML-väg i dagens kalkylator, men blir
relevant innan Ellen eller ett API anropar motorn direkt.

Separat från tariffkoden kvarstår säkerhetsfyndet om en tidigare pushad
autentiseringsuppgift. Den ska betraktas som röjd tills rotation och beslutad
historiksanering har genomförts; värdet återges inte här.

## Rekommenderad ordning

1. Gör Gotlands föregående-årsvärde obligatoriskt i kronor-läget eller visa
   bandscenarier i stället för en ensam MWh-lösning.
2. Bygg om kvalitetsmärkningen till strukturerade orsaker och rätta den
   generella texten om "försiktigt" standardvärde.
3. Slut hela katalogkontraktet fail-closed innan nästa tariff importeras.
4. Lägg en normaliserad beräkningsögonblicksbild i kontaktunderlaget.
5. Gör den uppskjutna direkta indatavalideringen innan en Ellen/API-integration.
