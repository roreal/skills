---
review_id: "2026-09-15-008"
date: "2026-09-15"
reviewer: Codex
status: approved-for-local-implementation-behind-gate
scope:
  - "Batch 5a:s push och faktiska remote-huvuden"
  - "Batch 5b i Fjarrvarmetariffer/batchplan-v22.md"
  - "Sex annual_forward-bastariffer med leverantörseffekt, bekräftat band och fullårsflöde"
  - "Jönköpings räknade accessavgiftstäckning, utan dubblettprodukt"
baseline_remote_heads:
  skills: "cd0bdb2e4fa33b753305d8983fda952aab43afdc"
  enkey_agents: "4d5f8a66e68ff4439ed379377d456230938962df"
  neptune_academy: "6331f27420c10e7104b002d97ad7ba67bb647040"
implementation_changed_by_reviewer: false
implementation_status: approved-locally-behind-existing-investigation-gates
activation_status: not-approved
push_status: not-approved
tariff_disposition_before: "45 implemented / 19 ready / 28 blocked av 92"
tariff_disposition_during_implementation: "45 implemented / 19 ready / 28 blocked av 92"
tariff_disposition_after_future_approved_activation: "52 implemented / 12 ready / 28 blocked av 92"
sharp_products_before: "47 (45 katalogprodukter + 2 leverantörsfilsprodukter)"
sharp_products_during_implementation: "47"
sharp_products_after_future_approved_activation: "53 (51 katalogprodukter + 2 leverantörsfilsprodukter)"
handoff: "conversations/handoffs/2026/09/2026-09-15-batch-5b-fullarsflode.md"
---

# Beredskapskontroll: Batch 5b — fullårsflöde och Jönköpings accessavgift

## Beslut

**Batch 5a är pushad och Batch 5b är godkänd för lokal implementation bakom
de sex befintliga `investigation.status="utreds"`-spärrarna.** Faktisk lokal
HEAD och `origin/main` verifierades direkt med `git ls-remote` i alla tre
repon:

- `skills@cd0bdb2e4fa33b753305d8983fda952aab43afdc`
- `enkey-agents@4d5f8a66e68ff4439ed379377d456230938962df`
- `neptune_academy@6331f27420c10e7104b002d97ad7ba67bb647040`

Den enda committen efter den tidigare tekniska slutgranskningen i `skills`
är `cd0bdb2`, som bara lägger till Batch 5a:s pushlogg. Diffen är ren enligt
`git diff --check`. Inga kod- eller tariffdata ändrades efter godkännandet.

Batch 5b omfattar exakt sex fysiska katalograder:

1. `borlange-energi-borlange-2026`
2. `falu-energi-vatten-falun-2026`
3. `falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo-2026`
4. `habo-energi-habo-2026`
5. `mjolby-svartadalen-energi-mjolby-2026`
6. `jonkoping-energi-jonkoping-och-granna-2026`

Jönköpings `--accessavgift` är en sjunde **räknad täckningspost**, men ska
byggas in i bastariffen som ett obligatoriskt kundval. Den får inte bli en
sjunde fysisk katalograd eller en separat produkt i kalkylatorn.

## Tre rättelser som överstyr den gamla batchtexten

1. Alla sex katalograder har
   `capacity.band_selection="supplier_confirmed_band_id_required"`.
   Bekräftat band-ID krävs därför för **samtliga sex**, även Habos enbandsrad;
   det är inte ett extra fält bara för Borlänge.
2. Varje policy behöver minst **tre** kostnadsbärande krav: leverantörens
   effekt, bekräftat band och fakturans årsflöde `flode_m3`. Formuleringen
   "två bundna fält" i Batch 5b:s fillista är inaktuell.
3. Habos katalogtext om "medel av tre högsta dygnsmedeleffekter under
   rullande 12 månader" stämmer inte med leverantörens aktuella 2026-sida.
   Habo anger i stället att abonnerad effekt beräknas av leverantören ur
   medelvärdet av de två senaste kalenderårens normalårskorrigerade energi,
   dividerat med 2 200 för flerbostadshus/gruppanslutna enfamiljshus och
   1 700 för övriga angivna fastighetstyper. Katalogens
   `billing_basis_method` ska rättas; policyn ska ta leverantörens färdiga
   effektvärde och takas till `snapshot`, inte märkas `rullande=True`.

Jönköpings `billing_basis_method:null` kan samtidigt ersättas med den aktuella
leverantörstexten: medelvärdet av de tre högsta av de fem högsta
dygnsmedeleffekterna under de senaste tolv månaderna. Det bundna
leverantörsvärdet ska därför märkas rullande och ge högst `snapshot`.

## Bindande motor- och kontraktsgrindar

Batchen får inte förlita sig på `volume`-motorns äldre reservberäkning av
flöde från MWh och antagen delta-T. Lägg en generell, aktiveringsnära
korsvalidering för varje kontraktsstyrd katalograd med `volume`: exakt ett
`flode_m3`-krav ska finnas, vara ett annual/number-fält från
`supplier_value`, ha `minvarde=0` och nå motorns `falt`-kanal. Saknat eller
ogiltigt flöde ska blockera före kostnadsberäkning. Legacytariffernas
reservvärde får vara oförändrat.

Jönköpings accessavgift ska räknas som:

`vald kr/central/månad × 12 månader × antal värmeundercentraler`.

Det befintliga globala formulärfältet `substations` ska vara enda källan till
antalet; skapa inte ett andra synligt antal-fält. Kontraktet ska ändå vara
fail-closed även för direkta produktanrop. Handoffens rekommenderade
bindningsmodell är därför ett explicit, policybundet
`antal_undercentraler`-fält som produktadaptern fyller från `substations` och
som `policyFaltMetadata` utelämnar på samma sätt som det dedikerade
kapacitetsfältet. Källtypen ska beskriva ett kunduppgivet värde sanningsenligt
(lägg till en smal `customer_value`-typ i båda språk om den valda modellen
kräver det), inte felmärkas som ett leverantörsvärde.

Accessvalet ska vara ett separat obligatoriskt numeriskt enum-fält med exakt
allow-list `0/10/25/50`, utan default. Noll är ett giltigt uttryckligt val;
tomt, saknat, okänt eller feltypat värde blockerar. Ny justeringstyp och dess
katalogpayload ska korsvalidera både satsfältet och antalsfältet före
generering, med speglad Python-/TypeScript-beräkning och sluten typallow-list.

## Källkontroll 2026-09-15

Aktuella officiella sidor verifierar katalogens 2026-priser och ger bättre
proveniens än flera äldre Prisdialogen-poster:

- Borlänge: `https://www.borlange-energi.se/kontakta-oss/priser/fjarrvarmepris-for-naringsidkare`
- Falu tätort och ytterorter: `https://fev.se/varme--kyla/fjarrvarme/avtal-och-priser-foretag.html`
- Habo: `https://www.haboenergi.se/varme-miljo-foretag/`
- Mjölby: `https://www.mse.se/foretag/fjarrvarme/priser`
- Jönköping, priser och accessavgift: `https://jonkopingenergi.se/foretag/fjarrvarme/fjarrvarme/priser`
- Jönköping, effektmetod: `https://jonkopingenergi.se/foretag/kundcenter/guider/vad-bestar-fjarrvarmekostnaden-av`

Claude ska lägga till/uppdatera spårade källposter och `source_refs` med
`retrieved_on=2026-09-15`. Historiska underlag får bevaras, men ska inte stå
ensamma som 2026-proveniens för Habo eller Jönköping.

## Räknings- och leveransgrind

Under implementationen ska katalogen fortsatt ha 86 fysiska poster,
`godkanda(katalog, policyregister=POLICYREGISTER)` vara 45 och den skarpa
payloaden ha 47 produkter totalt. Ingen Batch 5b-produkt får läcka ut.

En isolerad aktiveringskopia med exakt de sex spärrarna rensade ska ge 51
godkända katalogprodukter och 53 skarpa produkter inklusive de två
leverantörsfilsprodukterna. Dispositionen räknar dessutom Jönköpings
inbyggda accessavgiftstäckning och blir då **52/12/28 av 92**. Det är inte en
räkningsmotsägelse: täckningsposten är ingen egen produkt.

Ingen aktivering och ingen push är godkänd. Den bindande ordern finns i
handoff `2026-09-15-001`.
