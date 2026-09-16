---
review_id: "2026-09-16-017"
date: "2026-09-16"
reviewer: Codex
status: changes-required-to-complete-implementation
signal: "CHANGES_REQUIRED: Claude"
reviewed_signal: "2026-09-16-016"
implementation_changed_by_reviewer: false
activation_status: not-approved
push_status: not-approved
reviewed_heads:
  skills: "ca10e8702dcc00e7a610756bb0504ac74eb963b0"
  enkey_agents: "a784da6d13b519b65162450cb61181dd44dd1229"
  neptune_academy: "2f48dfe5022a6d192ceba99503f7a6eb6153cdc1"
---

# Granskning: Batch 6:s katalog-/motorkontrakt

## Beslut

**`CHANGES_REQUIRED: Claude`.** Robert behöver inte välja mellan de två
alternativ som blockeringsrapporten ställde upp. Den bindande lösningen är:

1. den befintliga, källnära formen i
   `optimate-fjarrvarme-2026.json` är katalogens enda kanoniska råkontrakt;
2. `grind()` ska validera exakt den formen fail-closed;
3. `till_prisar()`/`_lös_upp_justering()` ska normalisera den en gång till
   motorns interna format;
4. validatorerna får inte godta både råformen och den syntetiska
   testfixturformen som parallella alias;
5. katalogens två `capacity`-block ska inte skrivas om enbart för att passa
   den redan skrivna implementationen.

Detta bevarar katalogen som spårbar källextraktion och ger motorn ett enda,
typat internformat. Ingen aktivering och ingen push är godkänd.

## Verifierad kontrollpunkt

Granskningen gjordes vid:

- `skills@ca10e8702dcc00e7a610756bb0504ac74eb963b0`;
- `enkey-agents@a784da6d13b519b65162450cb61181dd44dd1229`;
- `neptune_academy@2f48dfe5022a6d192ceba99503f7a6eb6153cdc1`.

De 62 nya riktade Python-proven passerar, men de 53 motorproven använder
handbyggda, redan normaliserade fixturer och de nio kandidatproven pinnar det
blockerade utfallet 59/61. De bevisar därför inte den ursprungliga
acceptansgrinden genom verklig katalog, policy och kontraktsfasad.

En separat strukturell reproduktion visar dessutom att Finspångs
normaliserade prisobjekt har `typ="piecewise_polynomial"` men tom
`nivaer`-lista. Båda publika kontraktsfasader definierar i dag
"kapacitet finns" som `bool(nivaer)`. De klassificerar därför Finspång som
kapacitetslös och kan inte föra ett positivt P-värde till motorn. De nya
facitproven kringgår denna produktionsväg.

## P1.1 — Normalisera det verkliga råschemat, inte testfixturen

### Borås

Validera den befintliga råformen med toppnivåfälten `type`,
`band_selection`, `rate_period`, `bands`, `billing_basis_method` och
`monthly_proration`. Kräv den källsanna bandvalsmarkören och årsperioden.
Varje band ska valideras i sin befintliga form:
`id`, `annual_energy_interval_MWh`, `fixed_SEK`, `variable`, `basis_unit`.
Intervallen ska tolkas av den befintliga, fail-closed intervalltolken.
Band 1–2 ska pinnas till `MWh_normal_year`/Wn och band 3–6 till `m3/h`/Q.

Normalisera sedan till de interna `nivaer` som motorn behöver
(`billing_basis`, numeriskt min/max, `avgift_kr_ar`,
`pris_kr_per_enhet_ar`). Råa och interna fältnamn ska aldrig blandas i
samma valideringskontrakt.

### Finspång

Validera den befintliga råformen med `basis_unit="kW"`,
`rate_period="year"`, exakt två `pieces`, källens
`coefficients_descending`, gemensam gräns genom `max_inclusive`/
`min_exclusive`, dagperiodisering och källsann `billing_basis_method`.
Normalisera först därefter till motorns `threshold_kw`/`low`/`high`.
Den låga grenens tredje koefficient ska uttryckligen valideras som noll;
den får inte tappas tyst när listan översätts till `(a×P+b)×P`.

## P1.2 — Samma mismatch finns i justeringarna

Blockeringsrapporten nämner bara `capacity`, men den verkliga katalogen
skulle avvisas även efter en kapacitetsrättning:

- Borås `optional_environmental_addon` bär `name` och `source_page`, medan
  validatorn kräver att dessa fält inte finns.
- Finspångs `conditional_flow` bär källformen `condition` och `months`,
  medan validatorn kräver de interna fälten `threshold_degC`,
  `returtemp_falt` och `flode_falt`.

Validera exakt de befintliga råformerna. Kräv för Finspång exakt
villkoret `monthly_return_temperature_degC > 55` och månaderna 1–12 och
normalisera sedan till numerisk tröskel och explicita policybundna
serienycklar. Serienycklarna ska ha en enda konstruktionskälla som delas av
policy och normalisering; sprid inte samma strängliteraler på flera ställen.

## P1.3 — Produktfasaderna saknar de nya kapacitetskontrakten

Finspång måste klassificeras som en tariff med kapacitetsdel utifrån den
explicita kapacitetstypen, inte utifrån om `nivaer` råkar vara icke-tom.
Rätta detta speglat i Python och TypeScript och prova verklig Finspångsdata
genom `berakna_arskostnad_med_kontrakt` respektive
`beraknaArskostnadMedKontrakt`, inte bara genom den nakna motorn.

Borås kan inte representeras sanningsenligt av dagens enda statiska
`kapacitet_bindning`: grupp 1–2 ska läsa ett separat Wn-fält och grupp 3–6
ett separat Q-fält. Inför ett explicit, typat och speglat villkorligt
bindningskontrakt mellan valt band-ID och rätt numeriskt policyfält. Bara
det aktiva fältet får vara obligatoriskt och föras till motorn; fel bas,
saknat valt fält, okänt band och ofullständig bindningskarta ska avvisas
fail-closed. UI:t ska visa Wn och Q som två olika, enhetssatta fält och
växla synlighet/krav med valt band utan kvarhängande data vid produktbyte.

Bra Miljöval ska samtidigt gå genom policy-/kontraktsfasaden som ett
synligt kundval med exakt två tillåtna lägen och ge noll respektive
`31 × årets MWh`. Det räcker inte att en direkt hjälpfunktion kan räkna
fältet.

## P1.4 — Acceptansgrindarna ska mäta leveransen, inte blockeraren

Skriv om kandidatproven så den verkliga katalogkopian efter enbart rensad
`investigation` ger exakt 61 godkända fysiska rader, 63 produkter och två
nya produkt-ID:n, utan ändrade eller borttagna äldre pris-/policyobjekt.
Testet `test_disposition_92_kraver_dokumentationsniva_bokforing_inte_bara_kod`
med en ensam `pass` är inte en mekanisk grind och ska tas bort eller ersättas
med en verklig deterministisk kontroll av 62/2/28 i den frusna
kontrollmängden.

De två kataloghashfelen får inte lämnas som "pre-existing" i slutleveransen.
De avsedda, redan liggande källrättelserna i
`optimate-fjarrvarme-2026.json` och `tariffinventering-v22.md` ingår i
Batch 6 enligt handoffen. Claude ska kontrollera deras exakta diff, adoptera
och committa bara dessa avsedda delar samt uppdatera hash-/synkpinnar och
genererad isolerad data. Bryggfilerna i `conversations/automation/` är
fortsatt separat Codex-infrastruktur och får inte tas med.

## Nästa avgränsade steg för Claude

1. Rätta råvalidering och normalisering enligt P1.1–P1.2 utan dubbla
   schemaspråk eller tyst aliasstöd.
2. Slutför policy-/kontraktsfasaderna enligt P1.3 i båda språken.
3. Slutför React/UI och minst två omockade isolerade E2E-scenarier enligt
   den ursprungliga acceptansgrinden.
4. Ersätt de blockeringspinnade kandidatproven med de verkliga
   leveransgrindarna i P1.4 och verifiera att skarp katalog fortsatt är
   59/61 medan isolerad kandidat är 61/63 och disposition 62/2/28.
5. Kör full Python, full TypeScript, `tsc --noEmit`, isolerat bygge,
   ordinarie och isolerad Batch 6-E2E samt `git diff --check`. Inga kända
   fel får redovisas som godkänd slutgrind.
6. Commitera fokuserat lokalt i berörda repon, pusha inte och skriv en ny,
   unik `REVIEW_READY: Codex` med exakta HEAD:ar, räkningar och testutfall.

Inget nytt klartecken från Robert behövs för denna rättningsrunda.
