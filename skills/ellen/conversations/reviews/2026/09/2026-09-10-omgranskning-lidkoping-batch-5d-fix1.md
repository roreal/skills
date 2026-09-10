---
review_id: "2026-09-10-010"
date: "2026-09-10"
reviewer: Codex
status: changes-required
scope:
  - "Omgranskning av Lidköping Batch 5d, rättningsrunda 1"
  - "Samtliga fynd och acceptansbevis i granskning 2026-09-10-009"
reviewed_heads:
  skills: "93fe869b638ed517eda8e1fd95a56283fcb9a280"
  skills_product_commit: "f1d4d1d8a013ea5d7b7079a5d50364e505be8893"
  enkey-agents: "fbacd836a1f7aaa2e7b8c687d277ded464daf381"
  neptune_academy: "c4e1a265fbdb46001166cc56594cc9fe0fa7bd4d"
implementation_changed_by_reviewer: false
push_status: not-approved
tariff_activation_allowed: false
tariff_disposition: "7 implemented / 57 ready / 28 blocked av 92, oförändrad"
follows_review: "2026-09-10-009"
---

# Omgranskning av Lidköping Batch 5d — rättningsrunda 1

## Beslut

**Changes required.** Rättningsrunda 1 löser huvuddelen av föregående granskning och den
verkliga årsprodukten fungerar nu för båda Lidköpingstarifferna i oberoende prov. Två P1-
och två P2-fynd återstår före aktivering eller push.

Ingen tariff är aktiverad. Produktionsurvalet är fortsatt sju tariffer och dispositionen
7 implementerade / 57 redo / 28 blockerade av 92 är oförändrad.

## Fynd

### P1 — serienycklarna valideras syntaktiskt men inte mot policyn före aktivering

Den nya `_valid_signed_monthly_flow_adjustment()` kontrollerar att de tre fältnamnen är
icke-tomma, distinkta strängar. Den beställda kopplingskontrollen mot tariffens verkliga
`Tariffpolicy` saknas däremot fortfarande.

Codex ändrade i en isolerad katalogkopia `kund_volym_falt` till den giltiga men
obefintliga strängen `felskriven_obefintlig_serie` och löste endast aktiveringsstatusen.
Resultatet blev:

- `okand_justering(...) == None`;
- `grind(...) == None`;
- `bygg_ts_fran_katalog(...)` lyckades och skrev den felskrivna nyckeln till den
  genererade TypeScriptartefakten.

Tariffen kan alltså passera hela aktiveringskedjan trots att motorn därefter saknar serien
och kastar ett rått runtimefel. Detta är exakt kopplingsbarheten som punkt 2 i föregående
rättningsinstruktion krävde.

Lägg en aktiveringspreflight där både katalogtariffen och policyn finns tillgängliga. För
varje `signed_monthly_flow_adjustment` ska den verifiera att de tre deklarerade nycklarna
finns som rätt `KravPost`, gäller `annual`, har `vardetyp=number_series` och exakt tolv
värden. Rollernas säkerhetskrav ska också stämma: Q minst noll samt nätets Tm strikt större
än noll och attestationskrävd. Ett generatorprov med den felskrivna nyckeln ska kasta före
artefaktgenerering.

### P1 — `minimum_billing_basis` är fortfarande ofullständigt fail-closed

Motorns nya golv och de tariffspecifika policygränserna fungerar i normalfallet, men två
delar av kontraktet saknas:

1. Kataloggrinden typvaliderar inte `minimum_billing_basis`. En isolerad mutation till
   strängen `"3"` gav `grind(...) == None`. Pythonmotorn kastade därefter `TypeError`,
   medan TypeScriptmotorn konverterade strängen implicit och räknade 5 718 kr. Samma
   genererade tariffdata får alltså olika beteende i de två motorerna.
2. `kapacitetsGolv()` läser fortfarande bara lägsta `nivaer[].min`. För 0–41-produkten
   returnerar den 0 trots `min_debiteringsbas=3`, vilket gör det verkliga formulärets
   HTML-minimum till 1 kW. Formuläret saknar även produkttaket 41 kW. Domänpolicyn stoppar
   visserligen värdena efter submit, men kapacitetsbindningen filtreras bort ur
   `policyFaltMetadata`; dess `min`/`max`-fel får därför ingen fältnära felrad vid det
   dedikerade `kapacitetKw`-fältet.

Validera katalogfältet fail-closed som ett ändligt, positivt, icke-booleskt tal innan
`till_prisar`. Låt formulärets dedikerade kapacitetsfält använda policybindningens
produktspecifika min/max, med `min_debiteringsbas` som motor-/datagolv, och mappa
kapacitetsbindningens domänfel till samma fält med `aria-invalid` och synlig feltext.
Verifiera 2/3/41/42 kW för 0–41 samt 41/42 kW för 42+ genom både publik produktentry och
verklig `KalkylatorPage`. Band-ID:t ska fortsatt vara leverantörsbekräftat och inte
automatiskt räknas om.

### P2 — flera påstådda acceptansprov anropar inte det de säger sig bevisa

Testsviten har blivit betydligt bättre, men följande luckor gör leveransrapportens
påståenden för starka:

- Pythonprovet för 1/12 räknar endast `facit["fast"] / 12 * 12`; det anropar ingen
  periodiseringsfunktion. Codex direkta kontroll av den verkliga motorn gav korrekt
  794,166666… kr i var och en av tolv månader och 9 530 kr totalt, men detta behöver ligga
  i den committade regressionssviten och speglas i TypeScript.
- Pythonprovet för moms multiplicerar facit med produktionens egen `MOMS_FAKTOR`. Använd
  i stället de oberoende exakta faciten 17 947,50 respektive 90 057,50 kr.
- UI-testet med namnet att besparingsvägen ”kastar `Produktbegransning`” kontrollerar bara
  att produktväljaren saknas; det anropar aldrig besparingsentryn.
- Testet som säger att kr-inversion och schablon blockeras väljer bara kr-läget och
  kontrollerar inte en typad blockeringsorsak. Schablonläget körs inte alls.
- Den publika `beraknaArsprodukt`-entryn provas inte direkt för båda tarifferna. Codex
  verifierade oberoende att båda normalfallen fungerar, att besparingsentryn faktiskt
  kastar `Produktbegransning` och att kr-inversionen blockeras; gör dessa till permanenta
  tester.

UI-provet räknar dessutom bara tolv numrerade element per serie. Den riktiga sidan visar
inga synliga eller tillgängliga månadsnamn per ruta, endast ”värde 1”–”värde 12”. Märk
rutorna januari–december så kalenderordningen är begriplig och testbar, och verifiera
även °C-enheterna samt de verkliga hjälptexterna, inte bara rubriker och förekomsten av
`m³`.

### P2 — den offentliga källan för 2026-priserna saknas fortfarande

Den privata källposten `20_2` med rätt datum, hash och gransknings-ID är korrekt och den
inaktuella periodiseringsfrågan är borttagen. Däremot finns fortfarande ingen post för den
officiella 2026-prissidan `https://lidkopingenergi.se/priser-2026-foretag/`, trots den
uttryckliga instruktionen att binda både 2026-prissidan och leverantörssvaret. De
offentliga prisraderna hänvisar fortsatt bara till `20_1`, Normalprislista 2025.
Medlemmens `source_ids` har inte heller kompletterats med den nya privata källan `20_2`.

Lägg till den officiella 2026-sidan som separat källpost och koppla den till medlemmen och
båda tariffposterna. Lägg även `20_2` i medlemmens `source_ids`. Behåll rå-PDF:en utanför
git.

## Bekräftade rättningar

- Motorns `min_debiteringsbas` golvar nu en bas under 3 kW i både Python och TypeScript,
  även med valt band-ID.
- Policyn stoppar 2/42 kW för 0–41-produkten och 41 kW för 42+-produkten; 3/41 respektive
  42 kW accepteras.
- Båda tariffers handräknade fasta, energi- och justeringsbelopp samt totalsummor inklusive
  moms stämmer i de lägre fasadproven.
- NaN/oändlighet i Q, T och Tm stoppas fältnära i båda språk.
- UI-provet når den riktiga `KalkylatorPage`, renderar de tre serierna, stoppar saknad
  Tm-attestering och ger ett resultat efter komplett indata.
- Katalogens inaktuella uppgift om okänd periodisering är borttagen och den privata
  leverantörskällan är representerad utan att rå-PDF:en stagats.

## Oberoende verifiering

- `.venv/bin/python -m pytest tools/tariffer/tests -q`: **489 passed**; endast
  sandboxrelaterad pytestcache-varning.
- `npm test -- --run`: **20 testfiler, 530 tester passerade**.
- `npx tsc --noEmit`: godkänd.
- `npm run build`: godkänd; endast befintlig bundlevarning, `dist` återställd.
- `npm run test:e2e`: godkänd för befintliga riksgenomsnitts- och Sandvikenscenarier;
  `dist` återställd efteråt.
- Egna publika produktprov med isolerade, inaktiva Lidköpingsposter: aktuell årskostnad
  blev `complete` för båda produkterna; besparing kastade `Produktbegransning`; kr-invers
  kastade `KontraktBlockerat`.
- Eget periodiseringsprov gav tolv identiska kapacitetsdelar om 794,166666… kr och exakt
  9 530 kr per år för 0–41-goldenfallet.
- Egna negativa mutationer bekräftade att en obefintlig serienyckel når den genererade
  artefakten och att `minimum_billing_basis="3"` passerar grinden men divergerar mellan
  Python och TypeScript.
- `git diff --check` är rent för de tre granskade commitintervallen. Produktrepona är rena;
  sedan tidigare orelaterade filer i `skills` har lämnats orörda.

## Nästa avgränsade uppdrag till Claude

Rätta endast de fyra fynden ovan på nuvarande lokala kedjor. Aktivera ingen tariff och
pusha inget repo. Lägg generatornära korsvalidering mellan justeringspost och policy,
fail-closed schema för minsta debiteringsgrund, rätt min/max och fältnära kapacitetsfel i
formuläret samt de faktiska produkt-/periodiserings-/UI-proven. Komplettera den offentliga
2026-källan utan att lägga rå-PDF:en i git.

Kör hela Python-/TypeScriptmatrisen, typkontroll, produktionbygge, självbärande E2E och
`git diff --check`. Gör fokuserade lokala commits, rapportera exakta HEAD-hashar i
Batch 5d-sessionen och stanna för ny Codex-omgranskning. `investigation.status` ska ligga
kvar som aktiveringsspärr och 7/57/28 av 92 ska förbli oförändrat.
