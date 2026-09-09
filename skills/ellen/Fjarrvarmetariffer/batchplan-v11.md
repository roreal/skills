# Batchplan v11.0 — implementationsordning för `ready_to_implement`

Upprättad 2026-09-09 av Claude. Ersätter `batchplan-v10.md` i sin helhet (v10 ändras INTE i
efterhand — kvar som historik), som svar på Codex omgranskning
[2026-09-09-001](../conversations/reviews/2026/09/2026-09-09-omgranskning-tariffinventering-v10.md)
(supersedes `2026-09-08-009`). Bygger på dispositionerna i
[`tariffinventering-v11.md`](tariffinventering-v11.md) §4.1 (45 bastariffer) och §5 (10
`ready_to_implement`-varianter), samt §6/§6a:s sammansatta aktiveringspreflight och §7:s
`blockerade_tariff_ider`-baserade livscykel för informationsförfrågningar. Ingen batch är
påbörjad — detta är ett förslag till Codex granskning och Roberts prioritering.

**Vad som är nytt i v11** (se granskning `2026-09-09-001` för fullständig motivering):

1. **Rått formulärstate skilt från den parsade policy-DTO:n** (batch 0, §6a.2): nytt
   `PolicyRawFormValue = string | readonly string[]` som det RÅA React-statet, och en enda
   strikt parser `parsaPolicyIndata` till `PolicyInputValue` — v10 lät statet VARA
   `PolicyInputValue` direkt, vilket antingen inte kan bära en delvis ifylld serie
   (`string[]`) eller, om `Number(...)` körs per ruta, tyst skulle göra tomma rutor till
   giltiga nollor. Jönköpings numeriska enum konverteras nu till tal medan band-ID förblir
   sträng — v10:s regel "enum/band parsas aldrig" höll inte, Jönköpings `tillatna_varden` är
   uttryckligen `tuple[float, ...]`.
2. **En körbar felkanal för ogiltig indata** (batch 0, §6a.2 punkt 6): ny
   `valideraPolicyIndata(policy, prisar, indata)` som körs FÖRE fasadanropet och returnerar
   `{nyckel, orsak}[]` — v10:s design (läsa `ogiltigaFalt` ur ett `blocked`-resultat) kunde
   inte köras, eftersom `harledResultatstatus` bara returnerar `blocked` för SAKNADE fält;
   allt annat (fel typ/numerik/serieform/gräns) kastar `Error` i valideringsloopen, och det
   finns alltså inget statusobjekt att läsa `orsak` ur.
3. **Stockholm Exergi får en namngiven produktentry, nu med tre dispatch-grenar** (batch 7,
   §6a.4): ny `ArsprodukResultat`-union och `beraknaArsprodukt(args: BesparingsvardeArgs &
   { onskadTyp })` — v10:s enda `annars`-gren gjorde besparingsflödet onåbart för Sandviken
   och alla framtida kontraktstariffer; nu tre explicita grenar plus en delad
   `byggKontraktIndata`-funktion och en separat `calcResultForOnskadTyp`-wrapper i stället
   för en omöjlig retrofit av `KalkylatorResult`s obligatoriska besparingsfält.
4. **Adapterpreflighten får ETT anropskontrakt för `bygg_ts()`** (batch 7, §6a.4): v10 sa att
   `bygg_ts()` skulle köra preflighten med tomt adapterregister "när inga adapterposter är
   relevanta" — men Stockholms `ersatter_katalograd`-markör byggs OVILLKORAT in i policyn, så
   ett tomt register skulle alltid kasta. `bygg_ts()` får nu ALLTID det verkliga,
   injicerade produktionsregistret. Reverse-nyckeln byts samtidigt från `set(tariff_id)`
   till hela `(provider_id, tariff_id, ersatter_katalograd)`-relationen, så en adaptermarkör
   inte kan kvitteras felaktigt av en annan leverantör med samma `tariff_id`.
5. **P2 rättat:** etikett/hjälptext har EN källa (policyregistret); batch 0 säger nu TRE
   värdetyper, inte fyra; `kontrollera_adapterpreflight` ägs av `generera.py` i ALLA batchar
   (batch 0:s referens till `katalog.py` var fel).
6. **Dispositionerna 7/55/30/92 oförändrade** — samtliga v11-fynd var körbarhets-/
   typningsfel i redan beslutade kontraktsdesigner, ingen post flyttar.

## Batch 0 — Grundkontrakt: diskriminerad värdetyp, bandbindning, seriekardinalitet och en genererad produkt-/UI-ingång (granskning 2026-09-08-007/-008/-009, 2026-09-09-001, P1)

**Krävs FÖRE varje batch som bär ett bandkrav** (1, 3, 3b, 4, 5a, 5b, 5c, 6 — se
`tariffinventering-v10.md` §6a.2:s 42-radstabell) OCH före batch 7 (Stockholms seriekrav
delar samma grundmekanism). Utan detta grundarbete blir varje sådan tariff `blocked`/
felklassad som konfigurationsfel: `beraknaBesparingsvardeKontrakt` (`besparingsvarde.ts`)
bygger i dag `IndataPost` ENDAST för `kapacitetBindning`.

- **Tariffer:** inga — detta är rent infrastrukturarbete, ingen katalograd ändras.
- **Innehåll:**
  1. `KravPost.vardetyp: "number" | "number_series" | "band_id" = "number"` (Python +
     TypeScript), validerat i `__post_init__`/`skapaKravPost` (§6a.2).
  2. **Rättat P1 (granskning `2026-09-08-009`):** `IndataPost.varde` får en NY, egen typ
     `IndataVarde = Varde | str` (Python) / `IndataVarde = Varde | string` (TS) — `Varde`
     SJÄLVT (den delade parametertypen för `_validera_varde`/`valideraVarde`) rörs INTE, för
     att inte vidga vad de generiska numeriska validatorerna formellt accepterar (§6a.2,
     "Diskriminerad värdetyp"-avsnittet).
  3. `KravPost.antal_varden: int | None = None` (**nytt i v9**, §6a.2) — generiskt
     kardinalitetskrav för `number_series`, kastar i `harled_resultatstatus` vid fel längd.
  4. `Tariffpolicy.kapacitet_band_bindning`, `till_prisar()` bevarar `nivaer[].id` (med
     validering att varje bevarat ID är en icke-tom sträng och unikt inom prisposten — **nytt
     P1, granskning `2026-09-08-009`**, se punkt 6), ny motorparameter `vald_niva_id` i
     `arskostnad`/`manadskostnad` (§6a.2).
  5. **Rättat P1 (granskning `2026-09-08-009`) — egen, typad produkt-DTO i stället för det
     befintliga numeriska `falt`:** nytt, parallellt fält `policyFalt?: Record<string,
     PolicyInputValue>` genom `KalkylatorPage.tsx` (nytt state, skilt från `faltVarden`) →
     `KalkylatorInputs.policyFalt` → `BesparingsvardeArgs.policyFalt`. Ny hjälpfunktion
     `byggIndataFranPolicy(policy, policyFalt)` i `besparingsvarde.ts`, kallad från
     `beraknaBesparingsvardeKontrakt` i stället för det nuvarande enda
     `kapacitetBindning`-inlägget (§6a.2), inklusive `number_series`-hantering. Det befintliga
     numeriska `falt` rörs INTE — det förblir legacyvägens fria fakturafält (Gotlands
     `foregaende_ars_mwh` m.fl.).
  6. **Genererad, prispost- och omfattningsmedveten UI-metadata (rättat P1, granskning
     `2026-09-08-009`):** ny `policyFaltMetadata(policy, prisar, omfattning)`-funktion i
     `resultatkontrakt.ts` (v9:s `policyFaltMetadata(policy)` kunde inte bygga sitt eget
     bandval utan `prisar`, blandade `monthly`-/`annual`-krav och dubblerade
     kapacitetsfältet — alla tre rättade genom de två nya parametrarna och ett explicit
     filter som utesluter `policy.kapacitetBindning`). Ger `KalkylatorPage.tsx`
     inmatningstyp, en OBLIGATORISK, maskinläsbar `etikett`/`hjalptext` (nya `KravPost`-fält,
     satta av `policyregister.py`, inte härledda vid runtime), obligatoriskhet, tillåtna
     alternativ (bandval från den VALDA tariffens `nivaer[].id`, validerat unikt/icke-tomt
     vid katalogbyggnad, enumval från `tillatnaVarden`) och seriekardinalitet.
  7. **Felklassning — saknad OCH ogiltig indata (rättat P1, granskning `2026-09-08-009`):**
     `KontraktBlockerat.saknadeFalt?: string[]` (legitimt saknad kundindata) PLUS ett nytt
     `ogiltigaFalt?: { nyckel: string; orsak: 'typ' | 'numerik' | 'kardinalitet' |
     'okant_val' }[]` (strukturellt ogiltigt värde — fel `vardetyp`, fel längd, okänt band-/
     enumval). Båda visas fältnära i `KalkylatorPage.tsx`; interna kontrakts-/
     konfigurationsfel reserveras för fall UTAN ett specifikt användarfält att peka på
     (§6a.2 punkt 6).
  8. **Namngiven produktentry för Stockholms aktuella årskostnad, tre dispatch-grenar
     (rättat P1, granskning `2026-09-09-001`, ersätter v10:s onåbara besparingsgren):** ny
     `ArsprodukResultat`-diskriminerad union och funktionen `beraknaArsprodukt(args:
     BesparingsvardeArgs & { onskadTyp })` i `besparingsvarde.ts` — den delade
     `byggKontraktIndata`/`calcResultForOnskadTyp`-wrappern i `energiPotential.ts`, med
     `KalkylatorPage.tsx`-rendering för `{ typ: 'aktuell_arskostnad' }` utan besparingsfält
     (§6a.4) och ett bevarat, oförändrat `{ typ: 'besparing' }`-flöde för Sandviken m.fl.
  9. `KravPost.tillatna_varden` (§6a.6) och `KravPost.maxvarde`/`Tariffpolicy.kapacitet_
     multiplikator_bindning`/`Tariffpolicy.flodeskorrigering_variant`/`Tariffpolicy.
     kallenergi_arsserie_bindning`/`Tariffpolicy.returtemperatur_arsserie_bindning`/
     `Tariffpolicy.ersatter_katalograd` (§6a.1/6a.3/6a.4/6a.5) — samtliga nya kontraktsfält
     samlas i SAMMA commit som grundarbetet, eftersom de delar samma
     `policyFranGenererad()`-mappningsbehov (§6a.1s tabell).
- **Filer:** `resultatkontrakt.py`/`.ts` (samtliga nya fält, `vardetyp`-/`antal_varden`-gren
  i `harled_resultatstatus`/`harledResultatstatus`, ny `IndataVarde`-typ, ny
  `policyFaltMetadata`-signatur, ny `valideraPolicyIndata`), `katalog.py` (`till_prisar`
  bandbevaring + unikhetskontroll — **rättat P2, granskning `2026-09-09-001`:**
  `kontrollera_adapterpreflight` ägs av `generera.py`, tillagd i batch 7, INTE av
  `katalog.py`, konsekvent med batch 7:s fillista), `faktura.py`/`fjarrvarme.ts`
  (`vald_niva_id`-parameter),
  `besparingsvarde.ts` (`byggIndataFranPolicy`, `KontraktBlockerat.saknadeFalt`/
  `ogiltigaFalt`, `ArsprodukResultat`, `beraknaArsprodukt`), `energiPotential.ts`
  (`KalkylatorInputs.policyFalt`, dispatch till `beraknaArsprodukt`), `KalkylatorPage.tsx`
  (nytt `policyFaltVarden`-state, renderar `policyFaltMetadata` i stället för att anta
  `type="number"` för allt, fältnära `saknadeFalt`/`ogiltigaFalt`-visning, egen
  resultatsektion för `aktuell_arskostnad`), genererad testdata.
- **Teststrategi:** enhetstest per nytt `KravPost`-fält (giltigt/ogiltigt värde, kombination
  med förbjudna fält som `minvarde`+`band_id`, fel `antal_varden`), en
  `byggIndataFranPolicy`-svit som bevisar att ETT policykrav utan `policyFalt`-motsvarighet
  ger `blocked` med `saknadeFalt` satt (inte en generisk kastad `Error`), att ett STRUKTURELLT
  ogiltigt värde ger `ogiltigaFalt` (inte samma generiska fel), och att ett extra
  `policyFalt`-fält utan policykrav ignoreras; ett integrationstest med en syntetisk policy
  som har ett numeriskt, ett band-ID- och ett seriekrav SAMTIDIGT; ETT syntetiskt
  end-to-end-test som RENDERAR den riktiga `KalkylatorPage`, fyller i number + band-ID + enum
  + serie via den genererade UI-metadatan, och bevisar att den beräknade kostnaden stämmer —
  inte bara ett direkt anrop till `byggIndataFranPolicy`; ett sidtest för `beraknaArsprodukt`
  som visar `aktuell_arskostnad` utan besparingsfält.
- **Visas för användaren:** inget eget resultat — infrastruktur, men den genererade
  UI-metadatan (punkt 6) är den första synliga effekten: rätt inmatningstyp per fält i
  stället för att allt renderas som ett tal.

## Gemensamt för samtliga batcher (Sandviken-mallen)

Oförändrat — se granskningarna `2026-09-06-004` till `2026-09-07-003` för den fullt
utarbetade mallen (katalogändring → `Tariffpolicy` med `minvarde`/`heltal` → produktsidans
`kontraktsgatadPolicy`/`KontraktBlockerat`/`energyProvenance` återanvänd rakt av → kr/schablon
blockerade → golden-/gräns-/kontraktsfasad-/produktadapter-/diff-/momstest i båda språk →
tre fokuserade lokala commits, Codex-granskning, push i ordningen skills → enkey-agents →
neptune_academy).

## Batch 1 — Familj 4-resten + Telge + Partille (6 tariffer)

Ligger FÖRST enligt överlämningens ordningsregel (ingen kund-/prospektprioritet är angiven).

- **Tariffer:** `karlstads-energi-karlstad-2026`,
  `sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026`,
  `vanerenergi-mariestad-och-toreboda-2026`, `ovik-energi-ornskoldsvik-2026`,
  `telge-nat-telge-foretag-och-bostadsrattsforeningar-2026`,
  `partille-energi-partille-2026`.
- **Modell:** Sandviken-mönstret. Ingen ny motorkod — samtliga fält (effekt,
  `temperature_difference`, `low_utilization`, `incremental_return_temperature`) finns
  redan i `JUSTERINGSTYPER`. Partille tillagd i v3 (samma `temperature_difference`-mönster
  som Göteborg/Södertörn; v1/v2 utelämnade felaktigt att den har ett obligatoriskt
  temperaturfält, granskning `2026-09-08-001`).
- **Avvikande regler:** Övik behöver katalogrättelse (`fixed`, `monthly_proration`) FÖRE
  aktivering. Telge behöver TRE obligatoriska fält (effekt, normalårskorrigerad energi,
  returtemperatur), inte ett. Södertörn: bara SFAB:s rekommenderade effekt +
  returtemperaturavvikelse aktiveras — kundvald effekt med överuttagsavgift är en egen,
  blockerad variant (`sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026--kundvald-effekt`,
  inventeringens §5), inte del av denna batch. Partille: effekt + returtemperaturavvikelse,
  formeln `energi_MWh×7×avvikelse`, redan känd typ.
- **Obligatorisk indata:** debiterbar effekt (kW) för alla sex; VänerEnergi dessutom
  helårsflöde i m³ (fakturan, `volume`-justering, gäller alla 12 månader — rättat i v4,
  granskning 2026-09-08-003, P1: v3:s batchtext saknade detta fält trots att inventeringens
  rad och katalogens `adjustments` redan hade det); Telge dessutom normalårskorrigerad
  energi (MWh) och returtemperatur (°C); Södertörn och Partille dessutom
  returtemperaturavvikelse (°C).
- **Filer:** 6× katalograd, `policyregister.py` (6 nya policyer), `remaining_information_
  requests` (R11 TAS BORT — Telges tillsvidarevillkor redan besvarade, se inventeringens §7).
- **Teststrategi:** en `test_familj4_resten_kontrakt.py`, golden-värden mot respektive
  prislista, gränstest vid varje bands golv/tak, Telges tre fälts blockering testad separat.
- **Visas för användaren:** mwh-läge med tariffspecifika obligatoriska fält; kr/schablon
  blockerade.

## Batch 2 — Sundsvall Indal, Liden och Lucksta (1 tariff, minst risk)

- **Tariff:** `sundsvall-energi-indal-liden-och-lucksta-2026`.
- **Modell:** ren energitariff, `capacity: {"type": "not_applicable"}`. `EJ_TILLAMPLIG_
  KAPACITETSFORM`-mekanismen (byggd och testad mot fixture sedan etapp 1–4, 2026-09-04) tar
  bort ALLA grindstopp relaterade till kapacitetsformen. Det räcker DÄREMOT INTE för
  aktivering — se rättelsen nedan.
- **RÄTTAD (granskning 2026-09-08-005, P1): tariffen kräver en riktig `Tariffpolicy`, inte
  legacy-vägen.** v5 påstod felaktigt att en ren energitariff "går på legacy-vägen utan
  kontraktskrav". Verifierat direkt mot `policyregister.py`:
  `sundsvall-energi-indal-liden-och-lucksta-2026` finns INTE i `LEGACY_UNDANTAGNA_TARIFF_ID`
  (frozensetten innehåller uteslutande de sex tariffer som redan var produktionsgodkända
  INNAN resultatkontraktet fanns — Sundsvall Indal är inte en av dem). Generatorns
  `bygg_ts_fran_katalog()` kräver därför `contract_required: true` OCH en registrerad,
  komplett `Tariffpolicy` för denna rad, precis som för Sandviken — annars `raise`:er den.
  Batchen bygger alltså en MINIMAL policy: `capacity_bindning=None` (ingen kapacitetsdel
  att binda), `kravda_falt` bara energi (ingen effekt), `tackning={"annual_forward"}`. Samma
  mönster Sandviken redan bevisat, ingen ny mekanism.
- **Obligatorisk indata:** ingen utöver energimängd (MWh) — men eftersom tariffen nu blir
  kontraktsgated gäller den generella regeln (§2): kr och schablon blockeras tills en egen
  `annual_inverse`-fasad finns, inte "alla tre lägen" som v5 påstod.
- **Filer:** katalog-JSON (`contract_required: true`), `policyregister.py` (ny minimal
  policy), `godkanda()`-testet i `test_katalog.py` (räknaren 7→8), `remaining_information_
  requests` (R14 får `tariff_ids` satt till de två fortsatt blockerade Sundsvall-tarifferna
  — se inventeringens §7 — INTE en "delning" av `member_ids`, som datastrukturen inte
  stödjer idag).
- **Teststrategi:** regressionstest att `grind()` godkänner raden, golden-värde mot
  100,8 öre/kWh via KONTRAKTSFASADEN (inte naket `arskostnad`-anrop), test att
  `bygg_ts_fran_katalog()` INTE kastar för denna rad, kr/schablon-blockeringstest (samma
  mönster som Sandvikens `unsupported_input_mode`).
- **Visas för användaren:** mwh-läge endast, med källverifierat energipris. Kr och schablon
  blockerade — RÄTTAT från v5:s "mwh, kr och schablon, alla tre", som byggde på det felaktiga
  legacy-antagandet ovan.

## Batch 3 — Delad flödeskorrigeringsmotor: E.ON, Navirum, Kraftringen (9 tariffer)

- **Tariffer:** `e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026`,
  `e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter-2026`,
  `e-on-malmo-malmo-och-burlov-bostader-2026`,
  `e-on-malmo-malmo-och-burlov-ovriga-fastigheter-2026`,
  `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader-2026`,
  `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter-2026`,
  `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader-2026`,
  `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter-2026`,
  `kraftringen-kraftringen-2026`.
- **Modell (rättat i v4, granskning 2026-09-08-003, P1):** NY motorkod:
  `supply_temperature_adjusted_flow` i `justeringar.py` (speglad inline i `fjarrvarme.ts`) som en
  PARAMETRISERAD motortyp med TVÅ verifierade regelvarianter, inte en enda odelad formel —
  v3:s odelade formel skulle underdebitera Kraftringen vid `Tf < 60 °C`:
  - **E.ON/Navirum** (8 tariffer): `volym × base_rate × (0,02×(Tf−60) + 0,2)`, INGET golv.
    Källverifierad i verifieringslistan (`03_0`/`04_0`/`25_0`/`26_0`) — katalogens egna
    `correction_formula`-fält är `null` för samtliga åtta rader (verifierat direkt mot
    JSON), formeln är alltså INTE katalognativ.
  - **Kraftringen** (1 tariff): `volym × 10,40 × max(0,2; 0,2 + (Tf−60)×0,02)` — MED golv
    vid 0,2. Katalogens `candidate_factor`-fält bär redan denna exakta sträng.
  Regelvalet styrs av ett EXPLICIT, typat `Tariffpolicy`-fält
  `flodeskorrigering_variant: Literal["golvfri", "golvbegransad"]` (RÄTTAT namn, granskning
  `2026-09-08-007` — v7:s `kapacitet_bindning_variant` antydde fel sak och saknade en
  beskriven väg till motorn; inventeringens §6a.5 specificerar nu en ny motorparameter som
  bär diskriminatorn från fasaden till justeringsfunktionen) — satt per tariff-ID i
  `policyregister.py`, ALDRIG härlett implicit från leverantörs-ID. En okänd/saknad
  diskriminator på en tariff med denna justeringstyp BLOCKERAR.
  Samtliga nio rader kräver DESSUTOM ett bekräftat effektband-ID
  (`supplier_confirmed_band_id`, inventeringens §6a.2 — verifierat: alla nio har
  `band_selection`).
  `noggrannhet: snapshot` (aldrig `exact`) när effekten är ett enskilt leverantörsvärde —
  effekten är en rullande 12-månadersserie i källan.
- **Avvikande regler:** Malmö/Burlöv `-15→-8 °C` katalogrättelse. Endast fullvärmekunder i
  denna batch — E.ON/Navirums 36-månadersmetod byggs som EGNA variant-ID:n i batch 3b, INTE
  samtidigt. Kraftringens Brunnshög är en egen, blockerad variant
  (`kraftringen-kraftringen-2026--brunnshog`), inte del av denna batch.
- **Obligatorisk indata:** debiterbar effekt, medelframledningstemperatur `Tf` (°C), flöde
  (m³) — samtliga tre för samtliga nio tariffer. Kraftringens `Tf` är den
  FÖRBRUKNINGSVÄGDA månadsmedelframledningstemperaturen (fakturan/nätdata) — samma fält som
  E.ON/Navirums, inte ett separat krav.
- **Filer:** katalograder ×9, EN delad motorformel i `justeringar.py` (speglad inline i
  `fjarrvarme.ts`), `policyregister.py` (parametriserad policyfunktion, likt
  `_stockholm_exergi_policy`), `remaining_information_requests` (R06 TAS BORT, R10 TAS
  BORT — se inventeringens §7).
- **Teststrategi:** golden-värde mot minst en orts publicerade räkneexempel, gränstest för
  flödesformelns temperaturberoende, `noggrannhet: snapshot`-regressionstest, kontraktsfasad-
  test i båda språk. `okand_justering`-regressionstest att `supply_temperature_adjusted_flow`
  nu är känd men fortfarande blockerar tariffer som saknar `Tf`/flöde. MINST ETT
  gränstest per regelvariant (rättat i v4): E.ON/Navirum vid `Tf` under/vid/över 60 °C utan
  golv, och Kraftringen specifikt vid `Tf < 60 °C` som bevisar att golvet 0,2 tillämpas i
  stället för att formeln tillåts gå under det.
- **Visas för användaren:** mwh-läge, tre obligatoriska fält; resultat märkt uppskattning
  (snapshot); kr/schablon blockerade.

## Batch 3b — E.ON/Navirums 36-månadersvariant (8 variantrader, EFTER batch 3)

**Rättat i v4 (granskning 2026-09-08-003, P1):** v3 krävde felaktigt ett "36 månaders
rullande medelvärde av framledningstemperatur" som obligatorisk indata. Den verifierade
regeln (verifieringslistan) gäller i stället medelvärdet av de TRE HÖGSTA
DYGNSMEDELEFFEKTERNA (kW) — effekt, inte temperatur — under de senaste 36 månaderna
inklusive fakturamånaden. Valt kontrakt: leverantörens egna 36-månadersberäkning tas emot
som leverantörsvärde (SAMMA mönster som batch 3:s huvudfall, vars effekt också kommer från
leverantörens beräkning, inte en kalkylatorregression). Ingen ny 36-månaders tidsseriemotor
byggs i kalkylatorn — v3:s formulering "plus det rullande 36-månadersvärdet" var
självmotsägande (tre fält, sedan ett fjärde).

- **Tariffer:** de åtta variant-ID:n i inventeringens §5
  (`<bas-id>--bas-delvarme`, en per E.ON/Navirum-bastariff i batch 3).
- **Modell:** leverantörsvärde-mönstret för kunder med bas-/delvärmekälla i stället för
  fullvärme — ingen ny beräkningsmotor, bara en ny `Tariffpolicy`-variant per bastariff där
  källan till effektfältet är leverantörens 36-månadersberäkning i stället för
  -15 °C-regressionen.
- **Obligatorisk indata:** debiterbar effekt (kW, fakturan — leverantörens
  36-månadersberäkning), medelframledningstemp `Tf` (°C, fakturan) OCH flöde (m³, fakturan)
  — SAMMA tre fält som batch 3:s huvudformel, ingen fjärde.
- **Filer:** 8× ny variant-`Tariffpolicy` (leverantörsvärde-mönstret, samma kod som redan
  används för Sandviken/batch 5). INGEN ny formelkod i `justeringar.py` (speglad inline i `fjarrvarme.ts`).
- **Teststrategi:** kontraktsfasadtest att debiterbar effekt tas emot rakt av som
  leverantörsvärde utan intern 36-månadersberäkning, regressionstest att bas-/
  delvärmevarianten inte påverkar fullvärme-batchens `snapshot`-resultat.
- **Visas för användaren:** mwh-läge, SAMMA tre fält som batch 3 (debiterbar effekt, `Tf`,
  flöde) — bara källan till effektvärdet skiljer sig; kr/schablon blockerade.

## Batch 4 — Egna flödesformler: Jämtkraft, Umeå (4 tariffer)

**Eskilstuna borttagen i v3** (flyttad till `blocked_external_info`, se inventeringens §4.2
— nätreferensen `monthly_mean_for_customers_covered_by_flow_tariff` är inte verifierad som
ett stabilt katalogvärde eller en fakturapost, till skillnad från Umeås statiska referens).

- **Tariffer:** `jamtkraft-ostersund-froson-as-2026`, `jamtkraft-brunflo-och-opevagen-2026`,
  `jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge-2026`
  (samtliga tre `flow_difference`), `umea-energi-umea-enkel-2026`
  (`asymmetric_flow_difference` OCH en ny `post_multiplier`-medveten kapacitetsmotor — se
  nedan, rättat i v5, granskning 2026-09-08-004, P1: v4 saknade kapacitetsdelen helt).
- **Modell:** TVÅ separata nya justeringstyper i `justeringar.py` (speglad inline i `fjarrvarme.ts`) —
  `flow_difference` (Jämtkraft, formel `3×(flöde_m3 − 19×energi_MWh)`, referensvärdet 19
  m³/MWh redan statiskt i katalogen) och `asymmetric_flow_difference` (Umeå, `bonus_rate: 3`,
  `fee_rate: 7`, `reference_m3_per_MWh: 17`, allt statiskt). DESSUTOM för Umeå ENSAM:
  **RÄTTAT P1 (granskning `2026-09-08-008`) — kompositgrinden körs INUTI `godkanda()`s egen
  loop, som ett tvåpassförsök.** Den NAKNA `grind()` (`katalog.py`) ändras INTE: den
  fortsätter avvisa varje post med `post_multiplier` (`kapacitetsformel med multiplikator`)
  för alla tariffer, oförändrat — Umeå passerar den ALDRIG ensam. En NY funktion
  `kontrollera_kompositgrind(tariff, policy)` anropas av `godkanda()` SJÄLV, direkt när
  `grind()`s returvärde är exakt `"kapacitetsformel med multiplikator"` — den tar policyn
  som explicit argument och godkänner multiplikatorn bara när det NYA `Tariffpolicy`-fältet
  `kapacitet_multiplikator_bindning` är satt och den bundna `KravPost` finns i `kravda_falt`.
  Om DEN kontrollen går igenom körs `grind()` en ANDRA gång på en kopia av tariffen där
  ENDAST `post_multiplier`-fältet är neutraliserat — annars kunde en dold andra blockering
  (okänd `issue`, okänd justeringstyp) ligga bakom det första fyndet utan att någonsin
  kontrolleras, eftersom `grind()` bara returnerar det FÖRSTA den hittar (inventeringens
  §6a.3 — Codex reproducerade att Umeås verkliga rad har alla tre problemen samtidigt). Bara
  om BÅDA passen ger `None` läggs raden till i `godkanda()`s resultat. `bygg_ts_fran_katalog()`
  för nu sitt eget `policyregister`-argument uttryckligen vidare till `godkanda()`, så ett
  testregister och produktregistret inte kan divergera. `B` valideras mot
  `minvarde=0.93`/`maxvarde=1.401` (omräknat tak — den publicerade formeln `1,34×U+0,330`
  ger `1,40066` vid `U=0,799`, ett exakt `1,4`-tak hade kunnat avvisa ett giltigt, olika
  avrundat leverantörsvärde, §6a.3). Umeå behöver DESSUTOM ett bekräftat effektband-ID
  (`supplier_confirmed_band_id`, §6a.2 — raden har `band_selection` PLUS `post_multiplier`
  samtidigt). Kalkylatorn räknar ALDRIG själv ut
  `U = normalårskorrigerad_energi_dec_jan_feb / energi_sep_apr` (bolagets normalårskorrigering
  är inte publicerad) — bara det redan beräknade `B`. Ingen väntar på leverantörsbesked.
- **Avvikande regler:** `okand_justering`-regression att `asymmetric_flow_difference` inte av
  misstag öppnar upp Vattenfalls BLOCKERADE variant av samma typnamn (Vattenfalls referens är
  `"network_average"`, dynamisk — Umeås är ett statiskt tal; koden får inte dela logik som
  antar det ena för det andra utan en explicit typkontroll). Umeås `issues`-text ("Hela
  effektkostnaden multipliceras med B...") TAS BORT — löst av A/B-kontraktet.
- **Obligatorisk indata:** Jämtkraft (tre tariffer): debiterbar effekt + flöde oktober–april
  (m³, `months: [1,2,3,4,10,11,12]`, 7 månader). Umeå (rättat i v7): bekräftat effektband-ID
  (§6a.2), debiterbar effekt, flöde okt–apr, OCH kapacitetsfaktorn `B` (leverantörens eget
  redan beräknade värde) — FYRA obligatoriska fält.
- **Filer:** katalograder ×4, `justeringar.py` (två nya formler, speglade inline i
  `fjarrvarme.ts` — ingen separat `justeringar.ts` finns), NY funktion
  `kontrollera_kompositgrind()`, den rättade `godkanda()`-tvåpassloopen (§6a.3 — den nakna
  `grind()` i `katalog.py` ändras INTE, bara `godkanda()` gör det), `generera.py`
  (`bygg_ts_fran_katalog()`/`main()` för sitt `policyregister`-argument uttryckligen till
  `godkanda()`), `faktura.py`/`fjarrvarme.ts` (ny kapacitetsberäkning för Umeå),
  `policyregister.py` ×4.
- **Teststrategi:** golden-värde per tariff, gränstest för respektive formels
  referensberoende, `okand_justering`-regression mot Vattenfalls/Sundsvall Matforss
  BLOCKERADE varianter av samma typnamn, samt Umeås `B`-intervall — golden-värden vid
  `B=0.93`, `B=1.401` och en mellanliggande punkt I KONTRAKTSFASADEN
  (`harled_resultatstatus`, via `minvarde`/`maxvarde`); ett negativt test för `B=14` ska
  blockera DÄR (inte i `kontrollera_kompositgrind`, som bara kan bevisa att bindningen är
  deklarerad, inte att ett framtida kundvärde är giltigt) — kallat `B-intervall`, inte
  "U-intervall", eftersom motorn aldrig räknar `U`. Separat: ett test att Umeå UTAN
  bindningen stoppas av `kontrollera_kompositgrind`, och att en annan tariff med okänd
  multiplikator (ingen policy/bindning) också stoppas av samma funktion. **Nytt (granskning
  `2026-09-08-008`):** ett test där Umeå har B-bindningen deklarerad MEN katalograden också
  har en okänd `issue` — bevisar att raden ändå INTE läggs till i `godkanda()`s resultat
  (det andra grindpasset fångar den); samma test upprepat med en okänd justeringstyp i
  stället för en issue; samt ett test att `godkanda(katalog, policyregister=X)` skiljer sig
  från `godkanda(katalog)` när `X` saknar Umeås policy.
- **Visas för användaren:** mwh-läge; Jämtkraft: effekt + flöde; Umeå: effekt + flöde + `B`;
  kr/schablon blockerade för alla fyra.

## Batch 5a — Leverantörsvärde, ingen ytterligare justeringspost (8 tariffer)

Effekt/band är leverantörens/fakturans enda obligatoriska värde. Katalogens
`adjustments: []` för samtliga åtta — verifierat direkt mot JSON, inte antaget.

- **Tariffer:** `c4-energi-kristianstad-2026`, `kils-energi-kil-2026`,
  `skovde-energi-skovde-2026`, `trollhattan-energi-trollhattan-2026`,
  `tekniska-verken-katrineholm-katrineholm-2026`,
  `oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024-2026`,
  `soderhamn-nara-soderhamn-taxa-11-och-12-2026`,
  `temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026`.
- **Obligatorisk indata:** debiterbar effekt/band (fakturan) — för C4 dessutom det NYA
  `supplier_confirmed_band_id`-fältet (inventeringens §6a.2): exakt 500 kW är den
  uttryckligen osäkra gränsen (band 5 `200–499` vs band 6 `>500`), så automatisk
  bandvalsautomatik (`_niva()`) accepteras INTE — kunden bekräftar band-ID direkt, och
  motorn validerar att det bekräftade ID:t faktiskt täcker det angivna kW-talet innan
  beräkning. KATALOGRÄTTELSE: C4, Kils (`kils-energi-kil-2026`, dessutom `fixed:0` på alla
  fyra band) och TEMAB (`temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026`) har var
  sin `issues`-text som INTE matchar grindens godkännandelista — normaliseras till den
  redan kända typen "Metod för debiterbar effekt/kapacitet är inte fullständigt mappad;
  använd leverantörens fakturavärde" (se inventeringens §6). Informationsförfrågningarna
  R05 (c4-energi), R12 (temab-fjarrvarme) TAS BORT — se inventeringens §7.
- **Filer:** 8× katalograd, `policyregister.py` (8 nya policyer, samma mönster),
  `remaining_information_requests` (R13 TAS BORT — Söderhamn passerar redan grinden,
  leverantörens debiterbara effekt används, se inventeringens §7).
- **Teststrategi:** en samlad `test_leverantorsvarde_batch5a_kontrakt.py`/`.ts`, golden-värde
  per tariff, C4:s 500 kW-gränsblockering testad explicit.
- **Visas för användaren:** mwh-läge, obligatorisk indata; kr/schablon blockerade.

## Batch 5b — Leverantörsvärde, fullårsflöde (6 bastariffer + 1 varianttäckning)

**Räkningsmodell (samma mönster som batch 6/Borås, §8):** bygger 6 BASTARIFFER plus
Jönköpings accessavgift som en RÄKNAD VARIANTTÄCKNING (`--accessavgift`, inventeringens §5)
i SAMMA commit — inte en sjunde fristående tariff. Räknas som "6 + 1" i Sammanfattningen.
**Jönköpings accessavgift flyttad till `ready_to_implement` i v7** (Codex/Roberts beslut,
granskning `2026-09-08-006`): synligt, obligatoriskt kundval 0/10/25/50 kr/mån, inget
standardvärde, okänt val blockerar, ingen dubblettprodukt.

**Rättat i v3:** dessa sex har en prissatt `volume`-post som gäller ALLA TOLV månader
(katalogens `months: [1..12]`) — v2 utelämnade flödet som obligatorisk indata för dem helt
(Codex granskning `2026-09-08-002`, P1). Ingen `months`-semantik saknas i motorn för dessa
(hela året, ingen säsongsgräns att missa) — bara ett nytt synligt fält, ingen ny motorkod.

- **Tariffer:** `borlange-energi-borlange-2026` (effektgrupp + flöde, 501 kW-gränsen
  blockerad), `falu-energi-vatten-falun-2026`,
  `falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo-2026`, `habo-energi-habo-2026`,
  `mjolby-svartadalen-energi-mjolby-2026`,
  `jonkoping-energi-jonkoping-och-granna-2026` (PLUS varianttäckningen
  `jonkoping-energi-jonkoping-och-granna-2026--accessavgift`, byggd i SAMMA commit —
  se ovan).
- **Obligatorisk indata:** debiterbar effekt/band + prissatt flöde i m³ (hela året,
  fakturan/avtalet) för samtliga sex. Borlänge behöver DESSUTOM det NYA
  `supplier_confirmed_band_id`-fältet (§6a.2, samma mekanism som C4 i batch 5a): källan
  skriver `>501` och 501 kW är den uttryckligen osäkra gränsen mellan band 4 (`251–500`) och
  band 5 (`>501`). Falu ytterorter behöver DESSUTOM `KravPost.maxvarde=500` (§6a.1): dess
  publicerade prisgrupper går bara till 500 kW — ett mekaniskt maxkrav ersätter att bara
  förlita sig på att `_niva()` råkar kasta `ValueError` för värden utan täckande band.
  KATALOGRÄTTELSE: båda har var sin `issues`-text som inte matchar grindens
  godkännandelista — normaliseras (se inventeringens §6). Informationsförfrågningarna R04
  (borlange-energi) TAS BORT; R15 (falu-energi-vatten) TAS BORT (löst mekaniskt av
  `maxvarde`, inte av request-processen) — se inventeringens §7.
- **Filer:** 6× katalograd, `policyregister.py` (6 nya policyer med två bundna fält),
  Jönköpings accessavgift: ny justeringstyp/UI-kundval (0/10/25/50 kr/mån, obligatoriskt val)
  i `justeringar.py`/`fjarrvarme.ts` + `KalkylatorPage.tsx`.
- **Teststrategi:** som 5a, plus golden-värde som inkluderar flödesavgiften för varje rad,
  plus Jönköpings fyra accessavgiftsvärden testade var för sig och ett negativt test att ett
  okänt/tomt val blockerar.
- **Visas för användaren:** mwh-läge, effekt/band + flöde (Jönköping dessutom det
  obligatoriska accessavgiftsvalet); kr/schablon blockerade.

## Batch 5c — Leverantörsvärde, säsongsflöde (8 tariffer, kräver `months`-motorsemantik)

**Rättat i v3:** v2:s batch 5b påstod att samtliga tolv rader hade oktober–april (7
månader) — fel för nio av dem. De faktiska `months`-listorna varierar 5–9 månader per
tariff (verifierat direkt mot katalog-JSON):

| Tariff | `months` | Antal |
|---|---|---:|
| `lulea-energi-lulea-2026` | jan–maj + sep–dec | 9 |
| `oresundskraft-helsingborg-normal-2026` | jan–mar + nov–dec | 5 |
| `oresundskraft-angelholm-normal-2026` | jan–mar + nov–dec | 5 |
| `piteenergi-pitea-centrala-natet-2026` | jan–mar + okt–dec | 6 |
| `piteenergi-norrfjarden-och-sjulnas-2026` | jan–mar + okt–dec | 6 |
| `nevel-gimo-osterbybruk-och-osthammar-2026` | jan–apr + okt–dec | 7 |
| `tekniska-verken-linkoping-linkoping-2026` (lågtemperaturvariant är en egen, blockerad variant, inte del av denna batch) | jan–apr + okt–dec | 7 |
| `malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026` (ingen kapacitetsdel — fast årsavgift + energi + säsongsflöde) | jan–apr + okt–dec | 7 |

- **Motorarbete:** bygg `months`-hänsyn för `volume`-justeringen i `faktura.py`/
  `fjarrvarme.ts` — motorn och testerna MÅSTE använda varje posts EGEN `months`-lista, inget
  generellt antagande. Detta motorarbete delas av alla åtta rader men skrivs EN gång.
  Regressionstesta mot redan implementerade legacy-tariffer med `volume` (t.ex. Mölndal,
  helårs-`volume`) för att bevisa att helårsfallet inte påverkas.
- **Obligatorisk indata:** debiterbar effekt/band + säsongsflöde i m³, exakt de månader
  tabellen ovan anger, för SJU av åtta tariffer. **Undantag, rättat i v4 (granskning
  2026-09-08-003, P1):** `malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026` har
  INGEN kapacitetsdel i katalogen (`capacity: null`) — v3:s batchtext krävde felaktigt
  effekt/band för alla åtta. Mälarenergi behöver i stället bara ENERGI (MWh) + säsongsflöde
  (m³, jan–apr + okt–dec) utöver katalogens fasta årsavgift; ingen effekt/band-fält alls.
- **Filer:** 8× katalograd, `months`-semantik i motorn (delad), `policyregister.py` (8 nya
  policyer — Mälarenergis policy binder INGEN kapacitetsnyckel, till skillnad från övriga
  sju), `remaining_information_requests` (R03 får `tariff_ids` satt till de två fortsatt
  blockerade Mälarenergi-tarifferna `storre-fastigheter`/`gruppanslutna-smahus` — INTE
  `24-lagenheter`, som frågan inte gäller, se inventeringens §7).
- **Teststrategi:** en samlad `test_leverantorsvarde_batch5c_sasongsflode.py`/`.ts` med ETT
  testfall per tariffs `months`-lista (inte ett delat antagande), regressionstest att
  helårs-`volume`-legacytariffer är oförändrade.
- **Visas för användaren (rättat i v5, granskning 2026-09-08-004, P2):** mwh-läge. SJU av åtta: effekt/band + säsongsflöde. Mälarenergi 2–4 lägenheter (ENDA undantaget): energi (MWh) + säsongsflöde — INGEN effekt/band, tariffen saknar kapacitetsdel helt. kr/schablon blockerade för alla åtta.

## Batch 6 — Nya kapacitetsformer (2 bastariffer + 1 varianttäckning, störst motorarbete)

**Räkningsmodell förtydligad i v4 (granskning 2026-09-08-003, P2):** denna batch bygger 2
BASTARIFFER (Borås, Finspång) plus Borås miljötillägg som en RÄKNAD VARIANTTÄCKNING
(`--miljotillagg`, inventeringens §5) i samma commit — inte en tredje fristående tariff.
Räknas som "2 + 1" i Sammanfattningen nedan, inte "2" eller "3".

**Finspångs spetsvärmetillägg borttaget från denna batch i v4** (flyttad till
`blocked_external_info` i inventeringens §5 — utlösande kunder/perioder är inte kartlagda,
vilket bröt mot `ready`-definitionen). Grundformeln (`piecewise_polynomial` +
`conditional_flow`, UTAN spetsvärmetillägget) byggs ändå i denna batch; tillägget läggs på
senare, se "Ej batchade" nedan.

- **Tariffer:** `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026`
  (`heterogeneous_bands`, Wn/Q-grupper — miljötillägget byggs som en kryssruta i SAMMA batch,
  se §5-varianten `--miljotillagg`), `finspangs-tekniska-verk-finspang-2026`
  (`piecewise_polynomial` PLUS `conditional_flow`, TVÅ separata nya motordelar — utan
  spetsvärmetillägget, som är blockerat).
- **Avvikande regler:** Borås — automatisk gruppindelning blockeras, leverantören/kunden
  anger grupp.
- **Obligatorisk indata:** Borås: prisgrupp + `Wn`/`Q` + valfritt miljötillägg (kundvalt
  UI-tillval, inget separat katalogfält). Finspång: `P`-värde, returtemperatur varje månad
  (avgör om `conditional_flow`s villkor >55 °C utlöses) OCH, när villkoret utlöses, månadens
  flöde i m³ (multipliceras med 20 kr/m³). Spetsvärmetillägget byggs INTE i denna batch.
- **Filer:** ny kapacitetsformelkod (`heterogeneous_bands`, `piecewise_polynomial`) i
  `faktura.py`/`fjarrvarme.ts`, `katalog.py` (`grind()` utökad med de nya
  kapacitetsformerna i sin godkännandelista — Python-sidans grind, ingen TS-tvilling),
  två nya justeringstyper (`optional_environmental_addon`, `conditional_flow`) i
  `justeringar.py` (speglade inline i `fjarrvarme.ts`), katalograder, policyer.
- **Teststrategi:** golden-värde per formel, gränstest vid gruppgränserna, regressionstest
  att kapacitetsformsutökningen inte påverkar `selected_band_affine`-tarifferna. Finspångs
  villkorade flöde testat både under och över 55 °C-tröskeln.
- **Visas för användaren:** mwh-läge, tariffspecifik obligatorisk indata; kr/schablon
  blockerade.

## Batch 7 — Stockholm Exergis årsprodukt (1 produkt, utökad leverantörsfilsadapter)

Skiljer sig från övriga batcher: `monthly_invoice`-kontraktet är redan implementerat och
fakturavaliderat — bara ÅRSVÄGEN saknar motsvarande bindning. **Katalograden aktiveras
INTE** (rättat i v6, granskning 2026-09-08-005, P1 — se inventeringens §6a.4 för fullständig
motivering).

- **Produkt:** leverantörsfilens redan verifierade `stockholm-exergi-2026` (INTE
  katalogens `stockholm-exergi-stockholm-exergi-normal-2026`).
- **RÄTTAD väg (v5:s "namngivna adapter" band fortfarande katalog-ID:t — VERIFIERAT FEL):**
  `_stabilt_tariff_id()` kördes mot den verkliga katalograden och gav
  `stockholm-exergi-stockholm-exergi-normal` — ett TREDJE, aldrig tidigare existerande
  produkt-ID, skilt från leverantörsfilens `stockholm-exergi`. Att binda adaptern till
  katalog-ID:t (v5:s plan) hade alltså skapat TVÅ valbara alternativ i UI för samma
  underliggande normalprodukt. **RÄTTAT P1 (granskning `2026-09-08-006`) — inte "en andra
  separat policy", `POLICYREGISTER` är `dict[str, Tariffpolicy]` och kan inte bära två
  poster med samma nyckel:** (1) leverantörsfilens BEFINTLIGA `Tariffpolicy` för
  `stockholm-exergi-2026` UTÖKAS (samma objekt, samma nyckel) med
  `tackning: {"monthly_invoice", "annual_forward"}` (i dag bara `{"monthly_invoice"}`) och
  ändamålsspecifika `kravs_for`-taggar per fält; (2) ett nytt `ADAPTERREGISTER`-register i
  `policyregister.py`, typat med `provider_id`/`tariff_id`/`kravd_tackning` (inte en bar
  `dict[str, str]`), mappar katalog-ID:t `stockholm-exergi-stockholm-exergi-normal-2026` →
  `{provider_id: "stockholm-exergi", tariff_id: "stockholm-exergi-2026", kravd_tackning:
  "annual_forward"}`; (3) `bygg_ts_fran_katalog()` läser registret och HOPPAR ÖVER
  katalograden EFTER att ha verifierat att målpolicyn har den krävda täckningen — kastar
  annars, i stället för att bara anta att adaptern finns. `katalog.py`/`grind()` rörs INTE —
  katalograden fortsätter korrekt visa `energiform` som avslagsorsak.
- **RÄTTAT P1 (granskning `2026-09-08-007`) — kontrollen måste köras mot den RÅA
  katalogen, inte den redan filtrerade mängden:** `bygg_ts_fran_katalog()` gör
  `ur_katalogen = godkanda(katalog)` FÖRST och itererar bara DE raderna — Stockholms
  katalograd (`utreds` + `energiform`) når aldrig dit. `ADAPTERREGISTER` kontrolleras därför
  i en SEPARAT, injicerbar funktion `kontrollera_adapterpreflight(rak_katalog,
  byggda_leverantorer, policyregister, adapterregister)` mot `katalog["tariffs"]` direkt,
  körd FÖRE `godkanda()` anropas — oberoende av om katalograden finns kvar i
  `ur_katalogen`. **Rättat P1 (granskning `2026-09-08-009`) — global registeranvändning och
  ett bokstavligt `pass` i den omvända kontrollen ersatta med en bijektion via ett nytt,
  explicit `Tariffpolicy.ersatter_katalograd`-fält:** Stockholms utökade policy sätter
  `ersatter_katalograd: "stockholm-exergi-stockholm-exergi-normal-2026"`, vilket gör den
  omvända regeln till en ren kontroll (varje policy med fältet satt måste ha en matchande
  `ADAPTERREGISTER`-post) utan historiska "redan godkänd"-undantag och utan att förbjuda en
  framtida, direkt leverantörsprodukt utan katalogmotsvarighet (inventeringens §6a.4 har
  full pseudokod).
- **RÄTTAT P1 (granskning `2026-09-08-007`) — dispatchen till kontraktsfasaden var
  obeskriven:** att bara lägga `annual_forward` i policyn ändrar INTE vilken kod som körs,
  eftersom `kontraktsgatadPolicy()` (`besparingsvarde.ts`) styr på den REDAN BEFINTLIGA
  `_kraver_kontrakt`-markören — samma mekanism som redan tvingar Sandviken m.fl. genom
  fasaden. `_bearbeta_leverantorsfil()` sätter därför `_kraver_kontrakt: True` på Stockholms
  prispost när policyn (efter utökningen nedan) täcker `annual_forward` — ingen ny,
  parallell dispatch-mekanism.
- **Modell (RÄTTAT P1, granskning `2026-09-08-008` — EN modell, inte "17 nya KravPost" OCH
  en tvåserielösning i olika stycken):** en NY, ÅTSKILD årsindatamodell (inte de befintliga
  `monthly`-skopade `kall_energi_mwh`/`returtemperatur_c`-kraven, som `Tariffpolicy`s förbud
  mot dubblerade nycklar hindrar från återanvändning i en enda årssamlad indata): EXAKT TVÅ
  serie-`KravPost` — `kall_energi_mwh_arsserie` (`vardetyp="number_series",
  antal_varden=12, rullande=True, kravs_for=("annual",)`) och
  `returtemperatur_c_vintermanader` (samma mönster, `antal_varden=5`, november–mars). PLUS
  två nya statiska `Tariffpolicy`-bindningar `kallenergi_arsserie_bindning`/
  `returtemperatur_arsserie_bindning` som pekar ut vilken av de två posterna som är motorns
  `mwh_kallt_per_manad`/`returtemp_c_per_manad` — utan dem hamnar serierna i årsfasadens
  generella `falt`-loop, som kastar för seriedata (samma bindningsmönster som
  `kapacitet_band_bindning`/`kapacitet_multiplikator_bindning`). Det befintliga
  `debiterbar_effekt_kw`-kravet breddas till `kravs_for=("monthly", "annual")` (samma
  post, inte ett dubblerat nytt fält) så årsfasaden kan använda samma leverantörsvärde.
  Kontraktsfasaden binder de två serierna till en NY, valfri `returtemp_c_per_manad`-
  parameter i den lågnivåkod som redan periodiserar per månad — det gamla enskalära
  `returtemp_c`-argumentet används INTE för denna väg. Bygg ett källverifierat
  årsreferensfall, motsvarande Sandvikens granskningskedja (`2026-09-06-004`→
  `2026-09-07-003`).
- **Fail-closed före/efter-regel för besparingsvärdering (nytt P1, granskning
  `2026-09-08-008`):** `beraknaBesparingsvardeKontrakt` använder i dag SAMMA `IndataPost`-
  karta för före- och efterkostnaden, medan de syntetiska månadsenergimängderna KRYMPER i
  efterfallet — oförändrad kallenergi skulle då kunna ge en negativ "normal energi" för en
  krympt månad. Ingen källa ger en verifierad före/efter-transformationsregel för
  kallenergin. Stockholm ger därför en UPPSKATTAD AKTUELL årskostnad (`noggrannhet: snapshot`,
  ETT kontraktsanrop, inga syntetiska efter-mängder inblandade), men EXKLUDERAS EXPLICIT
  från besparingsvärderingsflödet tills en källmässigt försvarbar regel finns — ett
  besparingsanrop för en tariff med `kallenergi_arsserie_bindning` satt kastar ett tydligt,
  typat fel, inte `KontraktBlockerat`.
- **Namngiven produktentry (nytt P1, granskning `2026-09-08-009`):** en bar
  `beraknaArskostnadMedKontrakt`-anrop djupt i motorn gör inget visningsbart för användaren.
  Ny, diskriminerad `ArsprodukResultat`-union (`{typ:'besparing',...} | {typ:
  'aktuell_arskostnad', kostnad, status}`) och funktionen `beraknaArsprodukt(args,
  onskadTyp)` i `besparingsvarde.ts` — den ENDA produktentrypunkten `calcResult` anropar för
  en kontraktsgated tariff (Batch 0, punkt 8). `KalkylatorPage.tsx` renderar en egen
  resultatsektion för `{typ:'aktuell_arskostnad'}`, helt utan besparingsfält.
- **Avvikande regler:** rör INTE det redan godkända `monthly_invoice`-kontraktet — dess
  `kravs_for=("monthly",)`-krav och period-/upplösningssemantik lämnas oförändrade.
- **Filer:** `resultatkontrakt.py`/`.ts` (2 nya serie-`KravPost`, 2 nya
  `Tariffpolicy`-bindningar, `returtemp_c_per_manad`-parametern, seriekravens
  `antal_varden`-validering), `policyregister.py` (utökad `_stockholm_exergi_policy` med
  breddat effektkrav, `ersatter_katalograd` + nytt `ADAPTERREGISTER`), `generera.py`
  (`kontrollera_adapterpreflight()`, injicerad genom `bygg_ts_fran_katalog()`/`bygg_ts()`, +
  `_bearbeta_leverantorsfil()`s `_kraver_kontrakt`-sättning), `besparingsvarde.ts`
  (`ArsprodukResultat`, `beraknaArsprodukt`, det typade besparings-exkluderingsfelet),
  `energiPotential.ts`/`KalkylatorPage.tsx` (dispatch och rendering av `aktuell_arskostnad`).
- **Teststrategi:** eget källverifierat referensfall (inte bara Åkermannen-fixturens
  månadsdata återanvänd rakt av för ett annat ändamål), kontraktsfasadtest för
  `annual_forward` med den nya seriemodellen (inkl. fel längd 11/13 respektive 4/6 element
  blockerar via `antal_varden`), regressionstest att `monthly_invoice`-vägen är oförändrad,
  ett test att `kontrollera_adapterpreflight` kastar på fel `provider_id`, fel `tariff_id`,
  saknad/stale mappning, ELLER en `ersatter_katalograd`-policy utan matchande adapterpost
  (den omvända regeln), ett test med TVÅ olika injicerade register som ger olika resultat,
  ett test att effektkravet nu gäller BÅDA `monthly`/`annual`, ett sidtest att
  `beraknaArsprodukt({onskadTyp:'aktuell_arskostnad'})` visar kostnad UTAN besparingssiffra
  medan `onskadTyp:'besparing'` kastar det typade exkluderingsfelet, OCH ett test att
  generatorn producerar EXAKT ETT UI-val för Stockholm Exergi (inte två) efter preflighten.
- **Visas för användaren:** mwh-läge med obligatoriska fält, en egen resultatsektion
  "uppskattad aktuell årskostnad" (ingen besparingssiffra), under leverantörs-ID:t
  `stockholm-exergi`; kr och schablon BLOCKERADE (frusen status, samma som inventeringens
  rad och §2:s generella regel).

## Batch 8 — Vattenfall (12 tariffer, kontingent)

**Codex svar (granskning `2026-09-08-001`, öppen fråga 1, bekräftat i `2026-09-08-002`):**
hela gruppen förblir `blocked` tills flödesreferensen (3.3, `asymmetric_flow_difference`) är
löst. Bygg INGA osynliga delkomponenter (3.1/3.2/3.4) i förväg. Denna batch schemaläggs
alltså inte förrän ett leverantörssvar finns — tas inte med i implementationsordningen ovan.

## Ej batchade — `blocked_external_info` (26 bastariffer + 4 variantrader)

Väntar på leverantörssvar (26 bastariffer, inkl. Eskilstuna) eller ett formulerat
leverantörssvar (4 variantrader: Södertörns överuttag, Kraftringens Brunnshög, Tekniska
Verken Linköpings lågtemperaturvariant, samt Finspångs spetsvärmetillägg — väntar på en
kartläggning av utlösande kunder/perioder) via processen i
[`todo-godkanna-fler-fjarrvarmetariffer.md` §7](todo-godkanna-fler-fjarrvarmetariffer.md).
**Rättat i v7:** Jönköpings accessavgift är INTE längre i denna lista — Codex/Robert beslöt
i granskning `2026-09-08-006` att den blir ett kundformulärfält, flyttad till
`ready_to_implement`, batch 5b ovan.

## Sammanfattning

| Batch | Tariffer/varianter | Ny motorkod? | Risk |
|---|---:|---|---|
| 1 — Familj 4 + Telge + Partille | 6 | Nej (Sandviken-mönstret) | Låg |
| 2 — Sundsvall Indal | 1 | Nej (motorn `EJ_TILLAMPLIG_KAPACITETSFORM` finns; ny minimal `Tariffpolicy` krävs) | Minst |
| 3 — E.ON/Navirum/Kraftringen | 9 | Ja (parametriserad flödeskorrigering, två regelvarianter, typad diskriminator §6a.5) | Medel |
| 3b — E.ON/Navirum 36-mån (variant) | 8 | Nej (leverantörsvärde, ingen ny motorkod) | Låg |
| 4 — Jämtkraft/Umeå | 4 | Ja (två nya justeringstyper + separat kompositgrind §6a.3) | Medel |
| 5a — Leverantörsvärde, ingen justering | 8 | Nej (bandkontrakt §6a.2 för samtliga åtta) | Låg |
| 5b — Leverantörsvärde, fullårsflöde (6 bas + 1 variant) | 6 + 1 | Nej (bandkontrakt + nytt fält + Jönköpings UI-kundval) | Låg |
| 5c — Leverantörsvärde, säsongsflöde | 8 | Ja (`volume`+`months`-semantik) | Medel |
| 6 — Nya kapacitetsformer (2 bas + 1 variant) | 2 + 1 | Ja (två nya kapacitetsformer + två justeringstyper) | Högst |
| 7 — Stockholm Exergi årsprodukt | 1 | Nej (kontraktsbindning, ingen ny formel) | Låg–medel |
| 8 — Vattenfall | 12 | Kontingent, ej schemalagd | Ej schemalagd |
| **Summa batchade (1–7, 3b)** | **55** | | |
| Blockerade bastariffer (ej batchade) | 26 | | |
| Blockerade variantrader (ej batchade) | 4 | | |
| Redan implementerade | 7 | | |
| **Totalt (bastariffer + varianter)** | **92** | | |

**RÄTTAT P2 (granskning `2026-09-08-007`):** den tidigare additiva uttrycksraden
(`6+1+9+8+4+8+7+8+3 = 54`) hade fel siffror OCH summerade fel — batch 7 saknades helt ur
uttrycket. Den korrekta, verifierade uppräkningen (varje batchs egen "Tariffer/varianter"-
kolumn ovan, adderad rad för rad): batch 1 (6) + 2 (1) + 3 (9) + 3b (8) + 4 (4) + 5a (8) +
5b (7, dvs 6 bas + 1 variant) + 5c (8) + 6 (3, dvs 2 bas + 1 variant) + 7 (1) = **55**,
exakt matchande §8:s 45 bastariffer + 10 variantrader. Stämmer mot inventeringens §8:
7 implementerade + 55 redo + 30 blockerade (26 bas + 4 variant) = 92. Batch 0 (grundkontrakt)
räknas inte i denna tabell — den innehåller inga egna tariffer eller varianter, bara
infrastruktur som samtliga bandbatcher (1, 3, 3b, 4, 5a, 5b, 5c, 6) beror av.

**Räkningsnot:** "Summa batchade" 55 = 45 bastariffer (batch 1:6 + 2:1 + 3:9 + 4:4 + 5a:8 +
5b:6 + 5c:8 + 6:2 + 7:1 = 45) + 10 räknade variantrader (3b:8 + 5b:1 Jönköping + 6:1 Borås =
10). 45 + 10 = 55, matchar §8:s 45 bastariffer/10 variantrader exakt.
