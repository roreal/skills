---
review_id: "2026-09-16-015"
created_at: "2026-09-16T10:18:12+02:00"
reviewer: Codex
status: approved-for-local-implementation-behind-lock
scope: "Batch 6 — Borås och Finspång, två nya kapacitetsformer samt Borås miljötillägg"
approved_by: Codex
executed_by: null
dispatched_by: null
dispatch_via: agent-bridge
baseline_remote_heads:
  skills: "8356a716a956fb7101573f572d77897e27cc52ea"
  enkey_agents: "bebbb8073d95fd493168fdbcd57033dc0f02dcb5"
  neptune_academy: "ca0286059de493e9502e229beba4afe864401683"
implementation_allowed: true
tariff_activation_allowed: false
push_allowed: false
relates_to:
  - "conversations/handoffs/2026/09/2026-09-16-batch-6-nya-kapacitetsformer.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 6"
  - "Fjarrvarmetariffer/tariffinventering-v22.md"
---

# Beredskapskontroll: Batch 6 — nya kapacitetsformer

## Beslut

Batch 5c är pushad och remote-verifierad. Batch 6 är startklar för **lokal
implementation bakom befintliga `investigation.status="utreds"`-spärrar**.
Ingen tariff får aktiveras eller pushas i denna fas.

Batchen omfattar exakt två bastariffer och en räknad, inbyggd variant:

1. `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026`
2. `finspangs-tekniska-verk-finspang-2026`
3. Borås `--miljotillagg`, implementerat som ett synligt kundval i
   bastariffen, inte som en tredje katalograd eller UI-produkt.

Nuvarande verifierade läge är **59 implemented / 5 ready / 28 blocked av
92**, 59 godkända fysiska katalograder och **61 skarpa produkter**. Dessa
tal ska vara oförändrade under implementationen. En isolerad katalogkopia
där exakt de två bastariffernas spärrar rensas ska ge:

- **62/2/28 av 92** i den frusna kontrollmängden, eftersom även Borås
  miljötillägg är ett separat täckningskrav;
- 61 godkända fysiska katalograder;
- 63 produkter inklusive de två befintliga leverantörsfilsprodukterna;
- exakt två nya produkt-ID:n och inga borttagna eller ändrade äldre
  pris-/policyobjekt.

## Aktuell källkontroll 2026-09-16

### Borås

Leverantörens aktuella 2026-sida bekräftar sex prisgrupper, energipriset
609 kr/MWh, samtliga fasta koefficienter, att priserna gäller från
2026-01-01 och att Q bestäms av kunden och ställs på flödesbegränsaren:

`https://borasem.se/webb/foretag/fjarrvarme/priserochvillkor2026.4.3b2618bc1976272a99c471fd.html`

Katalogens befintliga källa `00_0`,
`https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Boras.pdf`,
har verifierad SHA-256
`a912a1d629fff0eb5f2828a773a4e305be3028e60c2e4395f6679258c4545ef9`.
Dokumentet säger uttryckligen att **priset 2026** för Bra Miljöval är ett
kundvalt tillägg på **31 kr/MWh**. Det är alltså inte en extrapolering från
2025 trots filnamnet.

Katalogen ska få en aktuell `borasem-2026`-källpost och tariffens
`source_refs` ska binda både den aktuella leverantörssidan för grundpriserna
och `00_0` för miljötillägget. Äldre källan bevaras; den får inte ensam bära
grundpriserna. `valid_from` kan sättas till `2026-01-01`.

Leverantörssidan omfattar även **Gånghester**, som saknas i nuvarande
`network_or_product` och visningsnamn. Behåll stabilt tariff-ID men rätta
det användarsynliga nät-/produktnamnet och pinna att inga andra äldre
produktnamn ändras. Topplastgruppen är en separat produktvariant och ingår
inte i Batch 6.

### Finspång

Leverantörens 2026-sida länkar den aktuella prislistan för flerfamiljshus
och lokaler:

- landningssida:
  `https://www.finspangstekniska.se/vara-tjanster/fjarrvarme/taxor-avtalsvillkor`
- PDF:
  `https://d2sabnli7hsonp.cloudfront.net/finspangs-tekniska/image/upload/fl_attachment/v1762179931/zvwzbdzlxxtsl15nsxrd.pdf`
- verifierad PDF-SHA-256:
  `909cbafc1f87be7c00b11f82818f703361f948cf7c2de3d6e04f792410b2ba26`.

PDF:en bekräftar energipriserna 708,6/355/212,2 kr/MWh, kapacitetsformeln
`(-0,204×P + 1093)×P` för `P <= 2600`, formeln
`98,45×P + 1 206 554` för `P > 2600`, årsdebitering periodiserad per dag
och flödesavgiften 20 kr/m³ när returtemperaturen överstiger 55 °C.
Leverantörssidan säger att verkliga kunder har individuellt uppmätt P.

Källposten `web-review-finspang-final` ska få korrekt titel,
`retrieved_on=2026-09-16` och SHA ovan. Tariffens `billing_basis_method`
ska beskriva leverantörens individuellt uppmätta P; den äldre 2025-källan
får stå kvar som historik men inte vara normativ för 2026-priserna.

Spetsvärmetillägget på 20 procent ingår inte: källan preciserar inte
entydigt vilka prisdelar påslaget träffar. Varianten ska fortsätta vara
`blocked_external_info`.

## Tekniska kontrakt som ska byggas

### Borås: `heterogeneous_bands`

- Prisgrupp 1–6 väljs uttryckligen från avtal/faktura; ingen automatisk
  gruppindelning och inget defaultval.
- Grupp 1–2 kräver Wn i MWh och förbjuder Q som aktiv beräkningsbas.
- Grupp 3–6 kräver Q i m³/h och förbjuder Wn som aktiv beräkningsbas.
- Båda fälten ska vara separata, synliga, enhetssatta och villkorligt
  validerade. Ett enda fält med skiftande enhet är inte godtagbart.
- Kapacitetskostnaden är `fixed + variable × Wn/Q` enligt valt band.
- Bra Miljöval är ett synligt val som ger exakt `31 × årets MWh` exklusive
  moms när det är valt och exakt noll annars.
- Resultatet är en uppskattad årskostnad; årsbelopp får inte presenteras
  som verifierad månadsfaktura.

### Finspång: `piecewise_polynomial` + `conditional_flow`

- P är ett obligatoriskt, ändligt, positivt leverantörs-/fakturavärde.
- Tolv returtemperaturer och tolv flöden ska bindas kalendermånadsvis.
  Saknad/feltypad serie ska blockera även vid direkt motoranrop.
- En månad debiteras med `20 × flöde_m3` exakt när returtemperaturen är
  **större än** 55 °C. Exakt 55 °C ger noll flödesavgift.
- Formelskiftet ska testas exakt vid 2600 kW och strax över; implementera
  inte en utjämnad eller interpolerad övergång.
- Spetsvärmetillägget ska inte finnas i katalog, policy, motor eller UI för
  denna produkt.

Båda kontrakten gäller endast MWh-/årsvägen. Kronor, schablon och besparing
förblir blockerade. Resultatstatus ska vara
`annual/snapshot/complete`, aldrig `exact`.

## Acceptansgrind före Codex-granskning

Leveransen ska minst ha:

- sluten katalogvalidering för båda nya kapacitetsformerna och båda nya
  justeringstyperna; okända/extra/saknade nycklar, bool som tal, NaN,
  oändlighet och negativa värden blockeras;
- speglad Python-/TypeScript-logik och tester genom verklig katalog,
  policy, kontraktsfasad och motor — inte bara hjälpfunktioner;
- Borås alla sex band, villkorlig Wn/Q-matris, okänt/tomt band, saknad och
  dubbel beräkningsbas samt miljötillägg av/på;
- oberoende statiskt facit som reproducerar Borås publicerade exempel
  80 MWh: 29 070 kr fast del + 48 720 kr energi = 77 790 kr exklusive
  moms, samt separata handräknade facit för Q-banden;
- Finspångs båda polynomgrenar, exakt 2600/över 2600, returtemperatur
  under/exakt/över 55 °C, flera avgiftsmånader och felmatris för båda
  12-elementsserierna;
- oberoende jämförelse av minst kapacitetskolumnen mot Finspångs
  publicerade typkundsexempel (t.ex. P=36 kW ger 48 855 kr inklusive moms
  efter källans avrundning). Gör inte ett helårsfacit av tabellens
  energikolumn utan dokumenterad månadsfördelning; tabellen är inklusive
  moms och visar ingen flödesavgift;
- renderade React-prov för båda produkterna från isolerat genererade
  policyer, inklusive villkorliga Boråsfält, tolv Finspångsmånader och
  produktbyte utan kvarhängande tariffdata;
- minst två omockade isolerade E2E-scenarier, ett per bastariff;
- regressioner för `selected_band_affine`, tidigare `volume`-/
  säsongsflödeslogik och samtliga redan aktiverade batcher;
- mekaniska räkningsgrindar 59/61 skarpt och 61/63 fysiskt/produkter i
  isolerad kandidat, plus 62/2/28 i den frusna kontrollmängden;
- full Python-svit, full TypeScript-svit, `tsc --noEmit`, isolerat bygge,
  ordinarie E2E, isolerad Batch 6-E2E och `git diff --check` i alla tre
  repon.

Golden-förväntningar får inte genereras av produktionsmotorn eller en kopia
av den. Ingen handredigering av genererade filer eller `dist/`.

## Bedömning

**Godkänd för lokal implementation bakom spärr.** Claude ska committa
fokuserat, skriva `REVIEW_READY: Codex` och stanna. Aktivering och push är
separata senare protokollsteg. Codex har inte pushat något i detta steg;
Claude är ensam pushverkställare först efter `APPROVED_FOR_PUSH: Claude`.
