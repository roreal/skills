---
review_id: "2026-09-16-033"
created_at: "2026-09-16T20:28:57+02:00"
reviewer: Codex
status: approved-for-local-implementation-behind-lock
scope: "Batch 7 — Stockholm Exergis befintliga leverantörsfilsprodukt får annual_forward via en bijektiv katalogadapter"
approved_by: Robert
implementation_directed_by: Codex
executed_by: null
dispatched_by: agent-bridge
dispatch_via: agent-bridge
baseline_heads:
  skills: "0df504ed227126b5fd36f87f99b4e240001a99d5"
  enkey_agents: "9b5125dbb6f2b8188cf880a0619c841b4c10f001"
  neptune_academy: "22b473d30980051fb87a936b3d824c53b63d58e8"
baseline_remote_heads:
  skills: "0df504ed227126b5fd36f87f99b4e240001a99d5"
  enkey_agents: "9b5125dbb6f2b8188cf880a0619c841b4c10f001"
  neptune_academy: "22b473d30980051fb87a936b3d824c53b63d58e8"
implementation_allowed: true
tariff_activation_allowed: false
push_allowed: false
relates_to:
  - "conversations/handoffs/2026/09/2026-09-16-batch-7-stockholm-exergi.md"
  - "conversations/reviews/2026/09/2026-09-09-inventering-akermannen-fakturaarkiv.md"
  - "conversations/reviews/2026/09/2026-09-09-verifiering-akermannen-augusti-2026.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 7"
  - "Fjarrvarmetariffer/tariffinventering-v22.md §6a.4"
---

# Beredskapskontroll: Batch 7 — Stockholm Exergis årsprodukt

## Beslut

Robert har uttryckligen bett att steg 3 i den redovisade planen genomförs:
Stockholm Exergi ska tas vidare som Batch 7 och Åkermannens fakturor ska
användas där de stärker valideringen. Batch 6 är pushad och remote-verifierad
i alla tre repon. Batch 7 är därför godkänd för **lokal implementation bakom
befintlig spärr**.

Den här signalen godkänner inte aktivering eller push. Den stående
automationsfullmakten gäller fortfarande den efterföljande granskningskedjan,
men varje protokollgrind ska skrivas och verifieras i ordning.

## Utgångsläge och oföränderliga identiteter

- Lokal HEAD och `origin/main` matchar exakt i samtliga tre repon:
  `skills@0df504e`, `enkey-agents@9b5125d`,
  `neptune_academy@22b473d`.
- Nuvarande disposition är **62 implemented / 2 ready / 28 blocked av 92**.
- Den skarpa genereringen innehåller 61 godkända fysiska katalograder och
  **63 produkter**: 61 katalogprodukter och två leverantörsfilsprodukter.
- `stockholm-exergi-2026` finns redan som fakturavaliderad
  leverantörsfilsprodukt och dess `monthly_invoice`-kontrakt är aktivt.
- Katalograden
  `stockholm-exergi-stockholm-exergi-normal-2026` ska **inte aktiveras**.
  Dess `production_ready:false`, `investigation.status="utreds"` och
  kataloggrind ska lämnas kvar.
- Under implementationen ska skarp disposition, antal godkända katalograder
  och antal produkter vara oförändrade. En isolerad aktiveringsprojektion ska
  ge **63/1/28**, fortsatt 61 godkända katalograder och fortsatt exakt 63
  produkter. Stockholm får aldrig bli ett andra eller tredje UI-val.

## Verifierat implementationsgap

Grundinfrastrukturen från Batch 0 finns redan i båda språken:
`number_series`, `kallenergi_arsserie_bindning`/
`kallenergiArsserieBindning`, returtemperaturens årsseriebinding,
`ersatter_katalograd`/`ersatterKatalograd`, `beraknaArsprodukt`,
`calcResultForOnskadTyp` och det typade avslaget för besparing.

Det återstående, faktiska gapet är avgränsat:

1. Stockholms befintliga policy täcker endast `monthly_invoice`; dess tre
   krav är fortfarande månadsskopade.
2. Leverantörsfilsprodukten får ännu inte `_kraver_kontrakt` för årsvägen.
3. Något `ADAPTERREGISTER` och någon rå katalog-preflight finns inte ännu.
4. Befintliga Stockholmtester bevisar uttryckligen det gamla tillståndet att
   `_kraver_kontrakt` aldrig sätts; de måste ersättas av tester för både
   bevarad månadsväg och ny årsväg.
5. Leverantörsfilens verifieringsmetadata säger fortfarande motsägande
   18 respektive 21 fakturor till juli 2026, trots den senare inventeringen
   av 22 PDF-filer/20 unika perioder till augusti 2026.

## Bindande adapter- och policykontrakt

Implementera den rättade modellen i `batchplan-v22.md`, Batch 7, utan nya
parallella lösningar:

1. Utöka samma `Tariffpolicy` för `stockholm-exergi-2026` till
   `tackning={"monthly_invoice", "annual_forward"}`. Skapa inte en andra
   policy med samma nyckel.
2. Behåll de befintliga månadskraven oförändrade. Lägg exakt två separata
   årskrav:
   - `kall_energi_mwh_arsserie`: `number_series`, 12 värden,
     `rullande=True`, `kravs_for=("annual",)`;
   - `returtemperatur_c_vintermanader`: `number_series`, exakt 5 värden i
     ordningen november, december, januari, februari, mars,
     `kravs_for=("annual",)`.
3. Bredda samma `debiterbar_effekt_kw`-post till både `monthly` och
   `annual`; duplicera inte nyckeln.
4. Bind serierna via `kallenergi_arsserie_bindning` och
   `returtemperatur_arsserie_bindning`. Sätt
   `stodjer_aktuell_arskostnad=True`, `stodjer_besparing=False` och
   `ersatter_katalograd="stockholm-exergi-stockholm-exergi-normal-2026"`.
5. Inför ett typat `ADAPTERREGISTER` med exakt relationen katalog-ID →
   `{provider_id:"stockholm-exergi", tariff_id:"stockholm-exergi-2026",
   kravd_tackning:"annual_forward"}`.
6. `kontrollera_adapterpreflight` ska vara injicerbar och bijektiv.
   `bygg_ts_fran_katalog()` ska kontrollera båda riktningarna mot råkatalogen
   före filtrering. `bygg_ts()` ska anropa samma kontroll med
   `rak_katalog=None` och endast bevisa reverse-ledet. Fel provider,
   tariff-ID, täckning, katalog-ID, markeringsrelation eller saknad/stale
   registerpost ska blockera.
7. `_bearbeta_leverantorsfil()` ska sätta `_kraver_kontrakt=True` för den
   befintliga Stockholmprisposten när den utökade policyn har
   `annual_forward`. Härled aldrig markören ur katalog-JSON.
8. Årsvägen ska ge `annual/snapshot/complete` och UI-texten uppskattad
   aktuell årskostnad utan besparingssiffra. MWh är enda tillåtna
   inmatningsläge; kronor, schablon och besparing ska blockeras typat.

## Fakturavalidering och integritet

Åkermannens underlag får användas, men de två valideringsändamålen ska
hållas åtskilda:

### A. Permanent anonymiserad fakturaregression

- Behåll `akermannen-baslinje.json` fryst till maj 2025–april 2026.
- Lägg en **separat** anonymiserad arkiv-/out-of-sample-fixtur i båda
  produktrepona med de redan godkända, sanitiserade värdena från
  granskningarna `2026-09-09-008` och `2026-09-09-009`.
- Testa januari–april 2025 och augusti 2026 som enkla fakturaperioder.
- Testa maj–juli 2026 som en sammanhållen preliminär-/avräkningskedja;
  juli är 7,190 MWh som kalendermånad, inte fakturans 21,823 MWh-rad.
- Skilj fakturaperiod, faktisk energiperiod, avläst/preliminär kvalitet,
  återföring och kalenderkostnad. `exact` får bara beskriva
  formelåterspelning, inte datakvalitet.
- Råa PDF:er, föreningsnamn, adress, kund-, avtals-, mätpunkts-, faktura-
  eller betalningsuppgifter får aldrig kopieras, stagas, loggas eller
  pushas.
- Först när fixturen och testerna passerar får leverantörsmetadata synkas
  till: 20 unika månadsfakturor/fakturaperioder januari 2025–augusti 2026,
  22 PDF-filer inklusive två dubblettkopior.

### B. Oberoende årsreferens

Årsfacit ska vara ett separat, statiskt och handräknat 2026-fall byggt från
den officiella prislistans formler och priser. Förväntat svar får varken
genereras av produktionsmotorn eller av en kopia av dess funktioner.

Fakturorna till och med augusti 2026 utgör inte ett komplett kalenderår.
Skapa därför inte påhittade september–decembervärden under etiketten
"Åkermannen 2026" och påstå inte att ett syntetiskt fall är kundens
faktiska helår. Om anonymiserade fakturavärden återanvänds som del av ett
representativt 12-månadersfall ska syntetiska kompletteringar och deras
roll anges explicit. Det enklaste och säkraste är ett helt fristående,
syntetiskt men källverifierat 12-månadersfacit, medan fakturafixturen ovan
står för verklig kundvalidering.

## Minsta acceptansmatris

- Fel längd 11/13 för kallenergiserien och 4/6 för vinterreturserien
  blockeras genom det verkliga kontraktet i båda språken.
- Effektkravet fungerar för både `monthly_invoice` och `annual_forward`.
- Befintlig månadsväg återspelar samma fakturor och komponenter som före
  ändringen, inklusive augusti 2026 och avräkningskedjan.
- Adapterpreflightens samtliga felvägar provas, inklusive reverse-regeln
  policy utan adapterpost; två injicerade register måste ge olika utfall.
- Produktionsregistret passerar `bygg_ts()`s reverse-kontroll och
  `bygg_ts_fran_katalog()`s fulla tvåvägskontroll.
- Exakt ett Stockholm-val genereras och renderas.
- `calcResultForOnskadTyp(... onskadTyp:'aktuell_arskostnad')` når den
  riktiga årsmotorn och ger det oberoende facitvärdet utan besparing.
- `onskadTyp:'besparing'`, kronor och schablon blockeras via de publika
  entrypunkterna; Sandvikens besparingsväg förblir grön.
- Reactprov verifierar de två seriernas etiketter, 12 respektive 5 fält,
  ordningen Nov–Mar, obligatorisk effekt, produktbyte utan kvarhängande
  tariffdata och resultattexten.
- Minst ett omockat isolerat browser-E2E-scenario går genom den verkliga
  genereringen och sidan. Ordinarie E2E ska samtidigt förbli grön.
- Python- och TypeScriptsviter, `tsc --noEmit`, isolerat bygge och
  `git diff --check` ska vara gröna. Golden-värden ska vara statiska och
  oberoende.
- Mekanisk räkningsgrind: skarpt under implementation 62/2/28,
  61 godkända katalograder och 63 produkter; isolerad aktiveringsprojektion
  63/1/28, fortsatt 61 katalograder och 63 produkter.
- Äldre pris-/policyobjekt, katalogradens spärr och det befintliga
  `monthly_invoice`-kontraktet ska vara byte-/beteendemässigt oförändrade
  utanför de uttryckligt utökade Stockholmfälten.

## Arbetskopiegrind

Följande orelaterade ändringar fanns före Batch 7 och ska bevaras ostagade:

- `skills`: `conversations/automation/README.md`,
  `conversations/automation/agent-bridge.zsh`, `../milesight` och redan
  otrackade projekt-/källfiler;
- `neptune_academy`: sju raderade filer under
  `neptune-marketing/dist/assets/` och modifiererad
  `neptune-marketing/dist/index.html`;
- `enkey-agents`: rent vid start.

Ingen handredigering av genererade filer eller `dist/`. Commitera endast
avsedda filer per repo och redovisa exakt vad som stagats.

## Stoppunkt

När implementation och hela grinden är klar ska Claude skriva en ny unik
toppost `REVIEW_READY: Codex` med exakta HEAD:ar, testantal, räkningsutfall,
fixtureproveniens och bevarade arbetskopieundantag. Ingen aktivering och
ingen push får ske före efterföljande Codex-granskning.
