---
review_id: "2026-09-13-035"
date: "2026-09-13"
reviewer: Codex
status: approved-for-local-implementation
scope: "Batch 3b — E.ON/Navirums bas-/delvärmevarianter med leverantörens 36-månaderseffekt"
baseline_remote_heads:
  skills: "19c68fe95e52492b58cc24965ef39a1083a655c8"
  enkey_agents: "4b1d4b6d78c010a4722f54df833ab7903431e9dc"
  neptune_academy: "55731894428d7fe43be00b9ddf36dad2597e8098"
implementation_allowed: true
activation_allowed: false
push_allowed: false
tariff_disposition: "25 implemented / 39 ready / 28 blocked av 92"
expected_after_future_approved_activation: "33 implemented / 31 ready / 28 blocked av 92"
---

# Beredskapskontroll för Batch 3b

## Beslut

Batch 3 är pushad och oberoende remote-verifierad i alla tre repon. Batch 3b är godkänd
att starta som en **lokal implementationsfas** enligt den separata arbetsordern
`conversations/handoffs/2026/09/2026-09-13-batch-3b-bas-delvarme.md`.

Källunderlaget räcker. Ingen ny leverantörsfråga och ingen ny 36-månadersmotor behövs.
Leverantörens redan beräknade debiterbara månadseffekt tas emot från faktura/leverantör
och används som ett snapshot-värde. Godkännandet omfattar åtta katalogvarianter,
policyer, generatorns stabila variant-ID:n, generiska UI-/kontraktstester och en avgränsad
proveniensrättning. Det omfattar inte aktivering, skarpa variantposter i produktkatalogen
eller push. En regenererad artefakt får däremot bära ny katalogproveniens och de åtta
befintliga produkternas förtydligade `Fullvärme`-etiketter.

## Verifierat nuläge

- `git ls-remote origin refs/heads/main` matchar lokala HEAD i alla tre repon:
  `skills@19c68fe`, `enkey-agents@4b1d4b6`, `neptune_academy@5573189`.
- Batch 3 är implementerad, aktiverad och pushad. Dispositionen är **25/39/28 av 92**.
- De åtta Batch 3b-ID:na är `ready_to_implement` i inventeringens §5 men finns ännu inte
  som katalogposter. Den nuvarande generatorn kan därför inte producera dem enbart genom
  att lägga policyer i `POLICYREGISTER`.
- Samtliga åtta bastariffer har samma tre prisdelar och samma golvfria
  flödeskorrigering i bas-/delvärmefallet. Endast källmetoden för debiterbar effekt
  skiljer sig från fullvärmeprodukten.
- E.ON:s fyra officiella 2026-PDF:er var åtkomliga 2026-09-13 och bekräftar både priserna,
  36-månadersregeln och flödeskorrigeringen. Katalogens nuvarande `03_0`, `04_0`, `25_0`
  och `26_0` pekar däremot på äldre 2025-dokument; nya 2026-källposter ska därför läggas
  till i stället för att skriva om de historiska källposterna.

## Arkitekturbeslut

1. Varje bas-/delvärmeprodukt blir en riktig, räknad katalogpost med inventeringens stabila
   `--bas-delvarme`-ID och ett explicit `variant_of` som pekar på bastariffen. Detta håller
   katalog, policyregister, generator och produktlista i samma modell.
2. Prisdata dupliceras från respektive bastariff eftersom katalogformatet ännu saknar
   arv. Ett tabellstyrt paritetstest måste därför faila om energi, effektpris, fast del,
   flödespris, moms, kundscope eller källor glider isär. Tillåtna skillnader är ID,
   produktetikett, `variant_of`, effektmetod och implementations-/aktiveringsstatus.
3. `variant_of` är ett kontrakt, inte fri metadata. En generisk katalogvalidering ska
   fail-closed på saknad/feltypad förälder, självreferens, kedjad variant eller avvikande
   medlem/prisår innan `godkanda()` returnerar produktkandidater.
4. Produkt-ID ska vara årsoberoende även när årtalet står före variantsuffixet:
   `<bas>-2026--bas-delvarme` ska genereras som `<bas>--bas-delvarme`. Detta byggs
   generiskt i `_stabilt_tariff_id`, inte med åtta hårdkodade undantag.
5. Fullvärme- och bas-/delvärmevalen måste vara entydiga i leverantörslistan. De befintliga
   åtta etiketterna får suffixet `Fullvärme`; de nya får `Bas-/delvärme`. ID:n och priser
   för de befintliga fullvärmeprodukterna ändras inte.
6. Variantpolicyn har ingen rå 36-månadersserie. Den kräver leverantörens debiterbara
   effekt för fakturamånaden, flöde, medelframledningstemperatur och samma bekräftade
   band-ID som bastariffen. Batchplanens formulering "samma tre fält, ingen fjärde" betyder
   att ingen separat 36-månadersindata tillkommer; den upphäver inte det redan införda,
   fail-closed band-ID-kontraktet för rader med
   `supplier_confirmed_band_id_required`.
7. Alla åtta variantresultat ska vara `annual/snapshot/complete`. Endast MWh stöds.
   Kronor, schablon, besparing, månadsfaktura och egen topp-tre-beräkning förblir blockerade.

## Källor som ska materialiseras i katalogen

- `03_1`: E.ON, Bro/Bålsta/Järfälla/Kungsängen 2026 —
  `https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--bro-balsta-jarfalla-kungsangen-2026.pdf`
- `04_1`: E.ON, Malmö/Burlöv 2026 —
  `https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser-malmo-2026.pdf`
- `25_1`: E.ON/Navirum, Norrköping/Söderköping 2026 —
  `https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--norrkoping-soderkoping-2026.pdf`
- `26_1`: E.ON/Navirum, Hallsberg/Kumla/Örebro 2026 —
  `https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--hallsberg-kumla-orebro-2026.pdf`

Claude ska hämta exakt dessa bytes, beräkna och lagra SHA-256 samt koppla både bas- och
variantposterna till rätt ny 2026-källa och sidorna 1–2. De gamla `_0`-posterna bevaras
som historisk proveniens.

## Fasordning

1. Materialisera och implementera de åtta varianterna bakom en ren lokal
   `investigation.status="utreds"`-spärr. `godkanda(katalog)` ska fortsatt vara 25 och
   projektets disposition fortsatt 25/39/28.
2. Codex granskar variantkopplingens fail-closed-validering, katalogparitet, policyer,
   stabila ID:n, kontraktsfasader, UI-fixtur och full testmatris.
3. Först efter ett nytt uttryckligt godkännande får de åtta spärrarna tas bort, den skarpa
   tariffartefakten regenereras och verkliga UI-/E2E-prov läggas till. Då förväntas
   **33/31/28 av 92**.
4. En separat Codex-granskning krävs före varje push.

Kraftringens Brunnshögsvariant, övriga batcher, priser och blockerade leverantörsfrågor
ligger helt utanför denna arbetsorder.
