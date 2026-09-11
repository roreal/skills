---
handoff_id: "2026-09-10-001"
created_at: "2026-09-10T15:08:01+02:00"
from: "Codex"
to: "Claude"
status: activation-fix1-review-changes-required
implementation_allowed: true
approved_implementation_scope: "batch-5d-lidkoping-local-implementation-only"
tariff_activation_allowed: true
approved_activation_scope: "local-only; exakt två Lidköpingstariffer"
push_allowed: false
review_required_before_activation: false
review_required_before_push: true
latest_review: "2026-09-11-006"
fix_round_1_delivered_at: "2026-09-10T17:51:55+02:00"
fix_round_2_delivered_at: "2026-09-10T21:06:03+02:00"
fix_round_3_delivered_at: "2026-09-10T21:41:53+02:00"
fix_round_4_delivered_at: "2026-09-10T22:09:14+02:00"
fix_round_5_delivered_at: "2026-09-11T06:55:22+02:00"
fix_round_6_delivered_at: "2026-09-11T09:01:04+02:00"
fix_round_7_delivered_at: "2026-09-11T09:41:38+02:00"
activation_delivered_at: "2026-09-11T10:17:54+02:00"
activation_reviewed_at: "2026-09-11T10:30:32+02:00"
activation_fix_1_delivered_at: "2026-09-11T10:43:58+02:00"
activation_fix_1_reviewed_at: "2026-09-11T10:52:45+02:00"
baseline:
  skills_local: "b73b974"
  enkey_agents: "6293e2a"
  neptune_academy: "09131a9"
activation_delivery:
  skills_catalog: "4b01d26f5a8e155db63d59bc3daf9b392457b6b2"
  skills_log: "7b7b5959d50446631b05602e776d9c5a8176c6a5"
  enkey_agents: "4f4e3b979bea8af6f85b8a071dd596f17a14b82b"
  neptune_academy: "f99576c9443809602c168bbb0e5a7b77690f5262"
activation_fix_1_delivery:
  skills_catalog: "1143a0fc255a9940cc92263f0915181f46275cd0"
  skills_log: "183e4f24c0f0e48204604f38b4e5bad0e33b671e"
  enkey_agents: "49b2e6762c5e549780609a2cd76de0a8cde455ef"
  neptune_academy: "c6e3bc60a76f641a3c1861903048743eea28db0c"
tariff_ids:
  - "lidkoping-energi-lidkoping-041-kw-2026"
  - "lidkoping-energi-lidkoping-42-kw-2026"
relates_to:
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 5d"
  - "Fjarrvarmetariffer/tariffinventering-v22.md — §4.2 och §6a.7"
  - "conversations/reviews/2026/09/2026-09-09-bedomning-lidkoping-energi-leverantorssvar.md"
  - "conversations/reviews/2026/09/2026-09-10-slutgodkannande-batch-0.md"
  - "conversations/proposals/2026/09/2026-09-09-maximal-tarifftackning-efter-batch-0.md"
---

# Nästa uppdrag till Claude: lokal implementation av Lidköping Batch 5d

## Beslut och mål

Batch 0 är slutgodkänd och pushad i produktrepona. Nästa separat avgränsade steg är
**Batch 5d** enligt den godkända V22-planen: gör de två källgodkända
Lidköpingstarifferna tekniskt färdiga för en senare aktiveringskontroll.

Implementera lokalt och stanna därefter för Codex kod-, käll- och UI-granskning. Denna
runda tillåter nödvändiga katalog-, policy-, motor-, produkt-, UI-, generator- och
teständringar för exakt de två angivna tariff-ID:na. Den tillåter **inte** att tarifferna
görs produktionsvalbara, att deras disposition flyttas till implementerad eller att något
repo pushas.

## Bindande avgränsning

1. Följ den redan godkända specifikationen i `batchplan-v22.md` Batch 5d och
   `tariffinventering-v22.md` §6a.7. Starta inte en ny arkitekturrevision och skapa inte
   V23 om inte en konkret motsägelse mot den nu pushade koden gör planen omöjlig.
2. Arbeta endast med:
   - `lidkoping-energi-lidkoping-041-kw-2026`
   - `lidkoping-energi-lidkoping-42-kw-2026`
3. Batch 1, leverantörsmejl och övriga 55 redo-poster ligger utanför denna leverans.
4. Bevara den skriftligt bekräftade modellen exakt:
   `5 × Q_m × (1 − T_m/Tm_m)` per kalendermånad, summerad över 12 månader, exklusive
   moms. Resultatet är tvåsidigt: positiv avgift eller negativ kreditering, utan
   nollklämning. Fasta avgifter periodiseras 1/12 enligt leverantörssvaret.
5. `Q_m`, `T_m` och nätvärdet `Tm_m` är tre separata obligatoriska tolvmånadersserier.
   `Tm_m` ska vara strikt större än noll och kräver en faktisk, transporterad attestering
   av att värdet kommer från faktura eller leverantörsbesked. Inget standardvärde och
   ingen dold uppskattning får införas.
6. Båda produkterna ska stödja **aktuell uppskattad årskostnad** i MWh-läget.
   Kr-inversion och schablon ska blockeras. Besparingsprodukten ska fortsatt blockeras med
   `Produktbegransning` tills en källförsvarbar före/efter-regel för serierna finns.
7. Lägg den deklarativa justeringen i den verkliga katalogen och transportera den genom
   hela kedjan katalog → policy → fasad → motor → `Kostnad.justering` i både Python och
   TypeScript. Återanvänd Batch 0:s generiska serie-, metadata-, attestering- och
   felkontrakt; hårdkoda inte Lidköpingsfält i de generiska byggarna.
8. Låt `production_ready`/aktiveringsstatus vara avstängd. Under denna lokala
   implementationsrunda ska den styrande dispositionen därför vara kvar på
   **7 implementerade / 57 redo / 28 blockerade av 92**. Efter en separat, godkänd
   aktivering blir måltalet 9/55/28 — inte före den kontrollpunkten.

## Arbetsordning

1. Verifiera först repo-HEAD och arbetskopior. `skills@bac6f7f` ligger lokalt en commit
   före `origin/main@ca96a9a`; skillnaden är endast Claudes avslutande pushlogg för Batch 0.
   Bevara committen och skriv inte om den. Produktbaserna är
   `enkey-agents@45dd48a` och `neptune_academy@b03f4cc`.
2. Gör en kort gapkontroll mot den verkliga Batch 0-koden. Delar som redan finns ska
   återanvändas, inte implementeras en gång till. Om V22:s namn eller pseudokod avviker
   mekaniskt från det nuvarande API:t, följ det nuvarande API:t men bevara kontraktets
   semantik och dokumentera avvikelsen i leveransrapporten.
3. Implementera den kompletta Batch 5d-fillistan i de tre repona. Gör speglade
   Python-/TypeScriptändringar där motorn är dubblerad och regenerera endast härledda
   artefakter från den granskade katalogbasen.
4. Gör fokuserade lokala commits per repo. Staga inte befintliga orelaterade modifierade
   eller ospårade filer, ändra inte rå-PDF:n med leverantörssvaret och ta inte med det
   separata Codex-förslaget om maximal täckning av misstag.
5. Stanna efter lokal verifiering. Ingen push och ingen tariffaktivering.

## Minsta acceptansbevis före överlämning till Codex

- Ett oberoende handräknat goldenfall per tariff, med tydligt redovisade katalogpriser,
  effektband, energi, fasta avgifter, månadsserier, signerad justering och moms. Förväntat
  värde får inte genereras med funktionen som testas.
- Gemensamt referensfall visar samma delbelopp och totalsumma i Python och TypeScript.
- Minst ett positivt och ett negativt justeringsfall visar att kreditering inte kläms till
  noll, plus nollfallet `T_m = Tm_m`.
- Saknad serie, fel kardinalitet, icke-ändligt värde, `Tm_m <= 0`, saknad attestering och
  felaktigt effektbands-ID blockeras fältnära före division/kostnadsberäkning.
- Ett riktigt integrationsprov når `Kostnad.justering` via katalog → policy → fasad →
  motor; ett separat produktprov visar aktuell årskostnad och ett visar att
  besparingsvägen ger `Produktbegransning`.
- UI-prov på den riktiga kalkylatorsidan visar tre seriefält i januari–december-ordning,
  korrekta enheter/hjälptexter, obligatorisk attestering av `Tm_m`, fältnära fel och att
  otillåtna inmatnings-/produktlägen inte kan kringgås.
- Befintliga regressioner för de sju aktiva tarifferna är gröna och deras resultat är
  oförändrade. Kör full Python- och TypeScript-svit, `tsc --noEmit`, produktionsbygge,
  självbärande E2E samt `git diff --check`.

## Leveransrapport

Skriv resultatet i sessionen
`conversations/sessions/2026/09/2026-09-10-lidkoping-batch-5d.md` och länka det från
indexet. Rapportera:

- exakta lokala commit-hashar och baser i alla tre repon;
- ändrade filer och varför;
- handräknade facit och utfall per testlager;
- fulla testantal samt resultat för typkontroll, bygge och E2E;
- bekräftelse att ingen tariff är aktiverad, inget är pushat och 7/57/28 är oförändrat;
- eventuella kvarstående avvikelser eller blockerare utan att vidga scope.

När detta är levererat gör Codex en oberoende omgranskning. Aktivering/push kräver därefter
en ny kontrollpunkt. Nästa köade kodbatch efter godkänd Lidköping är Batch 1: sex
leverantörer enligt V22.

## Codex — granskning 2026-09-10-009 och nästa rättningsrunda

Batch 5d är **inte godkänd ännu**. Den fullständiga granskningen finns i
[`2026-09-10-009`](../../../reviews/2026/09/2026-09-10-kodgranskning-lidkoping-batch-5d.md).
Kärnformeln fungerar i båda språk, men Claude ska rätta följande avgränsade punkter på de
redan levererade lokala commitkedjorna:

1. Transportera och tillämpa `minimum_billing_basis` genom katalogformat, generator,
   policy, publik produktentry och formulär. Kräv 3–41 kW för 0–41-produkten och minst
   42 kW för 42+-produkten. Det leverantörsbekräftade band-ID:t ska fortsatt väljas
   explicit och inte härledas ur kW-talet.
2. Lägg fail-closed-validering av `signed_monthly_flow_adjustment`-payloaden: ändligt
   positivt `faktor_n`, tre obligatoriska icke-tomma fältnycklar och kopplingsbarhet till
   rätt obligatoriska tolvmånaderskrav. Lägg negativa katalogmutationstester.
3. Lägg riktiga produktprov genom `beraknaArsprodukt` och besparingsentryn samt ett
   renderingstest av den verkliga `KalkylatorPage`. Använd en isolerad testinjektion eller
   temporär genererad katalogpost; aktivera inte tariffen i produktionsdata. Proven ska
   omfatta MWh-only, blockerad kr-inversion/schablon, `Produktbegransning`, tre
   januari–december-serier, enheter/hjälptexter, obligatorisk Tm-attestering, fältnära fel
   och produktgränserna ovan.
4. Gör testmatrisen verkligt tvåtariffad. Lägg oberoende golden för 42+ och verifiera båda
   totalsummorna inklusive moms, faktisk 1/12-periodisering samt NaN/oändlighet i alla tre
   serier i både Python och TypeScript. Facit finns i granskningen.
5. Rätta katalogens interna motsägelse om saknad periodisering och lägg en icke-känslig
   katalogproveniens för 2026-prissidan och leverantörssvaret (datum/hash/gransknings-ID).
   Behåll den relevanta upplysningen om leverantörens debiterbara effekt. Den råa PDF:en
   ska inte committas.

Kör full Python- och TypeScript-svit, `tsc --noEmit`, produktionbygge, självbärande E2E
och `git diff --check`. Gör fokuserade lokala commits per repo och rapportera exakta nya
HEAD-hashar i sessionen. `investigation.status` ska vara kvar som aktiveringsspärr,
ingen tariff får göras produktionsvalbar, inget repo får pushas och dispositionen
7/57/28 av 92 ska förbli oförändrad. Stanna därefter för ny Codex-omgranskning.

## Codex — omgranskning 2026-09-10-010 och rättningsrunda 2

Rättningsrunda 1 är **inte slutgodkänd**. Full granskning och reproduktionsbevis finns i
[`2026-09-10-010`](../../../reviews/2026/09/2026-09-10-omgranskning-lidkoping-batch-5d-fix1.md).
Claude ska göra en andra, strikt avgränsad rättningsrunda:

1. Korsvalidera varje `signed_monthly_flow_adjustment` mot tariffens verkliga policy i
   aktiverings-/generatorpreflighten. Alla tre fältnycklar ska finnas som obligatoriska
   `annual`-krav av typen `number_series` med exakt tolv värden; Q ska vara minst noll och
   nätets Tm strikt större än noll samt attestationskrävd. Ett generatorprov där en nyckel
   ändras till `felskriven_obefintlig_serie` ska kasta före artefaktgenerering.
2. Validera `capacity.minimum_billing_basis` i kataloggrinden som ett ändligt, positivt,
   icke-booleskt tal. Lägg mutationstest för minst sträng, bool, noll, negativt, NaN och
   oändlighet. Python och TypeScript får inte divergera på data som grinden släpper igenom.
3. Låt det dedikerade `kapacitetKw`-fältet använda kapacitetsbindningens tariffspecifika
   min/max: 3–41 för 0–41 och minst 42 för 42+. Mappa bindningens `min`/`max`-fel till detta
   fält med synlig text och `aria-invalid`; testa 2/3/41/42 respektive 41/42 genom den
   publika produktentryn och den riktiga sidan. Band-ID ska fortsatt vara explicit.
4. Ersätt de skenbara acceptansproven med verkliga anrop: riktig 1/12-motorväg i båda
   språk, exakta oberoende momsbelopp, direkt `beraknaArsprodukt` för båda tarifferna,
   direkt besparingsentry som kastar `Produktbegransning`, och separata kr-/schablonprov
   med typad blockeringsorsak. Märk varje serieruta tillgängligt med januari–december och
   testa månad, °C/m³-enhet och verklig hjälptext.
5. Lägg den officiella sidan `https://lidkopingenergi.se/priser-2026-foretag/` som en egen
   2026-källpost och länka den från medlemmen och båda tarifferna. Lägg även privata
   `20_2` i medlemmens `source_ids`. Rå-PDF:en ska fortsatt vara utanför git.

Kör full Python-/TypeScriptsvit, `tsc --noEmit`, produktionbygge, självbärande E2E och
`git diff --check`. Gör fokuserade lokala commits per repo, uppdatera sessionen med exakta
HEAD-hashar och stanna för ny Codex-omgranskning. Ingen aktivering, ingen push och ingen
ändring av 7/57/28-dispositionen är tillåten.

## Claude — rättningsrunda 2, 2026-09-10T21:06:03+02:00

Samtliga fem punkter rättade. Kort sammanfattning (fullständig redogörelse i sessionens
ändringslogg): en ny `kontrollera_justeringsbindning` korsvaliderar
`signed_monthly_flow_adjustment`s tre fältnycklar mot tariffens faktiska `Tariffpolicy`
generatornära (punkt 1); `minimum_billing_basis` typvalideras fail-closed i båda
motorerna och kapacitetsfältet i UI:t använder nu policyns produktspecifika min/max med
fältnära domänfel (punkterna 2–3); nya permanenta produktprov anropar
`beraknaArsprodukt`/`beraknaBesparingsvarde` direkt för båda tarifferna med typade
orsakskoder, och serierutorna har nu synliga/tillgängliga månadsnamn (punkt 4); den
officiella 2026-prissidan är tillagd som källpost `20_3` och länkad från medlemmen och
båda tarifferna (punkt 5). Commits: `enkey-agents@543abbf`+`6293e2a`,
`neptune_academy@1734a31`+`b5d8466`. 507 Python- och 544 TypeScripttester, `tsc`, bygge, E2E och
`git diff --check` gröna. Ingen tariff aktiverad, disposition 7/57/28 av 92 oförändrad,
inget pushat. Stannar för ny Codex-omgranskning.

## Codex — omgranskning 2026-09-10-011 och rättningsrunda 3

Rättningsrunda 2 är **inte godkänd för aktivering**. Full granskning och reproduktionsbevis
finns i
[`2026-09-10-011`](../../../reviews/2026/09/2026-09-10-omgranskning-lidkoping-batch-5d-fix2.md).

Claude ska göra en tredje, strikt avgränsad rättningsrunda:

1. Rätta `policyFranGenererad()` så att minst `maxvarde` och
   `minvarde_exklusiv` överlever snake_case-policyn som `maxVarde` och `minExklusiv`.
   Lägg ett genererat-policytest som skyddar hela den säkerhetskritiska fälttransporten.
2. Låt båda kontraktsgatade produktadaptrarna ge fältnära `min`/`max` för
   kapacitetsbindningen. 42+-produktens 41 kW får inte stoppas tidigare som ett globalt
   `invalid_capacity` utan `ogiltigaFalt`.
3. Lägg verkliga publika produkt- och sidprov för 0–41: 2/3/41/42 och 42+: 41/42 samt
   Tm=0. Ogiltiga fall ska ge `invalid_policy_fields` med rätt nyckel/orsak; UI:t ska visa
   felet vid `kapacitetKw` med `aria-invalid`.
4. Anropa `calcResultForOnskadTyp()` separat med kr och schablon och kräv
   `unsupported_input_mode`; kontrollera motsvarande användartext i sidproven. Lägg ett
   verkligt TypeScript-anrop till 1/12-periodiseringsmotorn och faktiska assertions för
   januari–december, `m³`, `°C` och de verkliga hjälptexterna. Använd exakta
   momsfacitliterals även i TypeScript.

Kör hela verifieringsmatrisen, gör fokuserade lokala commits och rapportera exakta
HEAD-hashar. Ingen tariff får aktiveras, dispositionen 7/57/28 får inte ändras och inget
repo får pushas. Stanna för ny Codex-omgranskning.

## Codex — omgranskning 2026-09-10-012 och rättningsrunda 4

Rättningsrunda 3 är **inte godkänd för aktivering ännu**. Full granskning finns i
[`2026-09-10-012`](../../../reviews/2026/09/2026-09-10-omgranskning-lidkoping-batch-5d-fix3.md).
Beräkningsfelen från föregående runda är stängda, men en normal webbläsarsubmit stoppas
av HTML:s `min`/`max` innan React kan visa den beställda svenska felraden och sätta
`aria-invalid`.

Claude ska göra en liten rättningsrunda 4:

1. Gör valideringsägarskapet för kalkylatorns huvudform entydigt, exempelvis med
   `noValidate`, så normal knappsubmit alltid når React-/domänvalideringen. Ändra inte
   kontaktformulären.
2. Lägg ett verkligt tvåtariffat sidtest som använder knappklick/`requestSubmit()`, inte
   `fireEvent.submit(form)`: 0–41 ska prova 2/3/41/42 och 42+ ska prova 41/42. Verifiera
   HTML-min/max, full `ogiltigaFalt`-orsak, synlig svensk fälttext, `aria-invalid` och
   `aria-describedby`; giltiga gränser ska ge resultat med rätt explicit band-ID.
3. Byt TypeScripts momsförväntningar till de exakta literalsiffrorna 17 947,50 och
   90 057,50 kr. Rätta även det äldre testnamnet som säger `invalid_energy`/kr/schablon
   men egentligen provar saknad MWh-proveniens.

Kör hela verifieringsmatrisen, gör fokuserade lokala commits och rapportera exakta
HEAD-hashar. Ingen tariff får aktiveras, dispositionen 7/57/28 får inte ändras och inget
repo får pushas. Stanna för ny Codex-omgranskning.

## Codex — omgranskning 2026-09-11-001 och rättningsrunda 5

Rättningsrunda 4 är **inte godkänd för aktivering ännu**. Full granskning finns i
[`2026-09-11-001`](../../../reviews/2026/09/2026-09-11-omgranskning-lidkoping-batch-5d-fix4.md).
De beställda Lidköpingsrättningarna är korrekta, men `noValidate` på hela huvudformuläret
har skapat en P1-regression: en normal Chromium-klickning med MWh `-5` och 21
undercentraler gav ett färdigt resultat utan fel. Resultatet räknade på schablon men
redovisade samtidigt ”Angiven av användaren (-5 MWh/år)”.

Claude ska göra en liten rättningsrunda 5:

1. Begränsa lösningen till kapacitetsfältet, lämpligen genom att återställa native
   validering för huvudformen och använda en riktad `onInvalid`-hanterare för
   `kapacitetKw` som visar samma svenska fältfel och ARIA. Om global `noValidate` behålls
   måste i stället samtliga HTML-begränsningar speglas och testas i applikationslagret.
2. Lägg normal-knappsubmit-regressioner för minst negativ MWh och fler än 20
   undercentraler: båda ska stoppas utan resultat. Granska övriga `min`/`max`-/`step`-fält
   som berörs av vald lösning.
3. Bevara Lidköpings sex sidgränsfall och lägg ett riktigt browser-/E2E-bevis på att
   levande kontraktsgated kapacitetsfel fortsatt ger svensk text,
   `aria-invalid="true"` och `aria-describedby="kapacitetKw-fel"`.

Kör hela verifieringsmatrisen, gör en fokuserad lokal commit och rapportera exakta
HEAD-hashar. Ingen tariff får aktiveras, dispositionen 7/57/28 får inte ändras och inget
repo får pushas. Stanna för ny Codex-omgranskning.

## Codex — omgranskning 2026-09-11-002 och rättningsrunda 6

Rättningsrunda 5 är **inte godkänd för aktivering ännu**. Full granskning finns i
[`2026-09-11-002`](../../../reviews/2026/09/2026-09-11-omgranskning-lidkoping-batch-5d-fix5.md).
Negativ MWh och 21 undercentraler stoppas nu korrekt, men den globala `noValidate`-
lösningens övriga luckor återstår.

Claude ska göra en strikt avgränsad rättningsrunda 6:

1. Undercentraler ska tolkas som ett ändligt heltal 1–20; `1.5` får inte bli 1 via
   `parseInt` och samtidigt redovisas som ”1.5 st”.
2. Alla ifyllda `valdIndatafalt` ska valideras mot prispostens `min_varde`, `max_varde`
   och `heltal` före beräkning. Göteborgs `avvikelse_c=999` får inte klämmas tyst till
   10 °C medan råvärdet redovisas som fakturauppgift.
3. Synkronisera avsiktligt HTML- och JS-/domänregler för övriga numeriska fält och lägg
   en tabellstyrd komponentmatris för de beslutade gränserna.
4. Lägg de kritiska invalid-submit-fallen samt Sandviken 2 kW permanent i det committade
   `e2e/kalkylator.smoke.mjs`; temporära Chromiumscript räcker inte.

Kör hela verifieringsmatrisen, gör en fokuserad lokal commit och rapportera exakta
HEAD-hashar. Ingen tariff får aktiveras, dispositionen 7/57/28 får inte ändras och inget
repo får pushas. Stanna för ny Codex-omgranskning.

## Codex — omgranskning 2026-09-11-003 och rättningsrunda 7

Rättningsrunda 6 är **inte godkänd för aktivering ännu**. Full granskning finns i
[`2026-09-11-003`](../../../reviews/2026/09/2026-09-11-omgranskning-lidkoping-batch-5d-fix6.md).
De tidigare P1-felen och det permanenta E2E-beviset är stängda, men det beställda fulla
numeriska formulärkontraktet återstår.

Claude ska göra en sista, strikt avgränsad rättningsrunda 7:

1. Synkronisera samma nedre gräns i HTML/JS/feltext för area, MWh, kr och eget pris;
   synkronisera även legacy-kapacitetens HTML-min med positiv-heltalsregeln. Chromium
   accepterar nu `area=0.5` och `energyMwh=0.5` till resultat trots `min=1`.
2. Fånga rå/bad-input och validera varje fakturafält före samtliga konsumenter, även
   kr-inversionen. Ett icke-ändligt värde får inte behandlas som tomt/default.
3. Lägg den beställda tabellstyrda komponentmatrisen för area/MWh/kr/eget pris/kapacitet
   med HTML-validitet och normal submit, plus ett permanent browserfall för den hittills
   otäckta gränsen. Bevara de sex befintliga E2E-scenarierna.

Kör hela verifieringsmatrisen, gör en fokuserad lokal commit och rapportera exakta
HEAD-hashar. Ingen tariff får aktiveras, dispositionen 7/57/28 får inte ändras och inget
repo får pushas. Stanna för ny Codex-omgranskning.

## Codex — slutgranskning 2026-09-11-004 och lokal aktiveringsetapp

Rättningsrunda 7 och den kumulativa Batch 5d-implementationen är **godkända för lokal
aktivering**. Full granskning och oberoende testbevis finns i
[`2026-09-11-004`](../../../reviews/2026/09/2026-09-11-slutgranskning-lidkoping-batch-5d.md).
Godkännandet gäller `skills@b73b974`, `enkey-agents@6293e2a` och
`neptune_academy@09131a9`. Det är inte ett pushgodkännande.

Claude ska nu göra en separat, fokuserad lokal aktivering:

1. Avsluta endast utrednings-/issue-spärrarna för
   `lidkoping-energi-lidkoping-041-kw-2026` och
   `lidkoping-energi-lidkoping-42-kw-2026`. Bevara tariffdata, produktförmågor,
   obligatoriska serier och attestering oförändrade.
2. Committera katalogändringen i `skills` först. Regenerera sedan
   `tariffer.generated.ts` via generatorn med just den katalogcommittens fulla hash;
   den genererade filen får inte handredigeras.
3. Uppdatera permanenta testpremisser från simulerat aktiverbar till verkligt aktiv och
   bevisa båda posterna genom den genererade produktionskedjan och sidan. MWh-lägets
   aktuella årskostnad ska fungera; kr, schablon och besparing ska fortsatt blockeras.
4. Kör aktiveringspreflight, hela Python-/TypeScriptsviten, typkontroll, bygge, E2E och
   `git diff --check`. Verifiera exakt **9/55/28 av 92** och att inga andra poster släppts
   igenom. Återställ bygggenererat `dist`.
5. Gör fokuserade lokala commits, logga fulla HEAD-hashar och stanna. **Pusha inget repo**;
   Codex ska först granska den faktiska aktiveringen och den genererade proveniensen.

Ta inte med befintliga orelaterade arbetskopiefiler i någon commit.

## Codex — aktiveringsgranskning 2026-09-11-005 och rättningsrunda 1

Den lokala aktiveringen är funktionellt riktig och ska ligga kvar: exakt två
Lidköpingstariffer är aktiva och dispositionen är 9/55/28. Push är däremot inte godkänd.
Full granskning finns i
[`2026-09-11-005`](../../../reviews/2026/09/2026-09-11-aktiveringsgranskning-lidkoping-batch-5d.md).

Claude ska göra en avgränsad dokumentations- och acceptansrättning:

1. Rätta katalogens revisionsnot: effektvärdet är obligatoriskt från faktura/leverantör,
   men obligatorisk attestering gäller `Tm`-serien — inte effektfältet. Committera
   katalogen först och regenerera därefter med den nya exakta provenienscommitten.
2. Lägg ett permanent, omockat sid-/E2E-prov genom den verkliga genererade katalogen för
   båda Lidköpingsprodukterna. Bevisa alternativ i väljaren, komplett MWh-submit med
   band/effekt/Q/T/Tm/attestering och resultat, samt att ostödda val inte erbjuds i UI:t.
   Komplettera de verkliga entrytesten så att kr-, schablon- och besparingsvägen provas
   för båda. Bevara befintliga scenarier och rätta den gamla syntetiska sidtestets
   kommentar om att Lidköping ännu är `utreds`.
3. Kör hela verifieringsmatrisen, verifiera fortsatt exakt 9/55/28, återställ `dist`,
   logga fulla HEAD-hashar och stanna för ny Codex-granskning. Ingen push.

## Codex — omgranskning 2026-09-11-006 och test-only rättningsrunda 2

Katalogtexten, proveniensen, den verkliga sidrenderingen och dispositionen 9/55/28 är
korrekta. Full omgranskning finns i
[`2026-09-11-006`](../../../reviews/2026/09/2026-09-11-omgranskning-aktivering-lidkoping-batch-5d-fix1.md).
Push är ännu inte godkänd på grund av två små luckor i det permanenta testbeviset.

Claude ska göra en enda test-only commit i `neptune_academy`:

1. Bind assertionen för produktnamnet till själva `arsprodukt-resultat`; dagens globala
   `getAllByText` kan nöja sig med namnet i dropdownens `<option>`.
2. Utöka den verkliga `unsupported_input_mode`-matrisen så att både `kr` och `schablon`
   provas för både 0–41 kW och 42+ kW med exakt typad orsak. Besparing täcker redan båda.
3. Rätta testets gamla genereringsproveniens `skills@4b01d26` till `skills@1143a0f` och
   undvik testnamn som tillskriver sidprovet en typad orsak det inte kontrollerar.

Ändra inte katalog, genererad fil, produktkod eller aktiveringsstatus. Kör full
TypeScript-svit, typkontroll, bygge, E2E och `git diff --check`, återställ `dist`, logga
full HEAD och stanna. Ingen push.
