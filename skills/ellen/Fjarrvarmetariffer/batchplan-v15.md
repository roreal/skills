# Batchplan v15.0 — implementationsordning för `ready_to_implement`

Upprättad 2026-09-09 av Claude. Ersätter `batchplan-v14.md` i sin helhet (v14 ändras INTE i
efterhand — kvar som historik), som svar på Codex omgranskning
[2026-09-09-005](../conversations/reviews/2026/09/2026-09-09-omgranskning-tariffinventering-v14.md)
(supersedes `2026-09-09-004`). Bygger på dispositionerna i
[`tariffinventering-v15.md`](tariffinventering-v15.md) §4.1 (45 bastariffer) och §5 (10
`ready_to_implement`-varianter), samt §6/§6a:s sammansatta aktiveringspreflight och §7:s
`blockerade_tariff_ider`-baserade livscykel för informationsförfrågningar. Ingen batch är
påbörjad, ingen tariff aktiveras — detta är ett förslag till Codex granskning och Roberts
prioritering. Dispositionerna 7 implementerade / 55 redo / 30 blockerade / 92 totalt är
oförändrade.

**Vad som är nytt i v15** (se granskning `2026-09-09-005` för fullständig motivering; samma
tre P1-fynd + två P2-fynd som `tariffinventering-v15.md`, applicerade på batchplanens
motsvarande avsnitt):

1. **`argsFranInputs` använder nu faktiska enumvärden och den verkliga uppskalningsformeln**
   (batch 7, §6a.4): v14 jämförde mot tre värden som inte finns i `EnergyScope`/
   `EnergyInputMode` (`TS2367` ×3) och hade ett no-op (`totalMwh = totalMwh`) i stället för
   `calcEnergyMwh(inputs)` + `energyMwh / (1 - VARMVATTEN_ANDEL)`-uppskalningen.
   `energyProvenance` sätts nu bara när `energyInputMode === 'mwh'` och talet är ändligt och
   positivt. `calcResult` ANROPAR nu `argsFranInputs` (delad bas för min/mid/max-anropen) i
   stället för att duplicera scope-/provenienslogiken en andra gång, vilket denna batchplan
   tidigare (punkt 4 nedan, historik-v13/v14) felaktigt beskrev som "förblir oförändrad".
2. **`beraknaArsprodukt` har en fullständig, fail-closed kropp** (batch 7, §6a.4): gate →
   bekräftad MWh-proveniens → ändlig positiv energi → kapacitet närvarande → kapacitet
   ändlig/heltal/≥golv → policyns fältnära förkontroll → fasadanrop, samma ordning som
   `beraknaBesparingsvardeKontrakt` redan använder. De valfria fälten på
   `Tariffberakningsunderlag` avsmalnas EXPLICIT (ingen non-null-cast) innan de skickas till
   `byggKontraktIndata`s smalare, obligatoriska signatur. Sidwrapperns
   `{ typ: 'aktuell_arskostnad', ...resultat }` (dubblerad `typ`, `TS2783`) är borttagen —
   wrappern returnerar `beraknaArsprodukt`s resultat direkt.
3. **Parserns scalar/array-formgrindar är nu explicita** (batch 0, §6a.2): varje skalär gren
   (`number`/`band_id_val`/`enum_val`) kräver `typeof ravarde === 'string'` och varje
   seriegren (`number_series`) kräver `Array.isArray(ravarde)` INNAN `.trim()`/`.length`/
   iteration — fel form ger `{status:'ogiltigt', orsak:'typ'}` omedelbart.
4. **P2: `forkontrolleraPolicyIndata` är uttryckligen omfattnings- men INTE
   månadsmedveten** (batch 0, §6a.2) — den verkliga `harledResultatstatus` filtrerar även på
   `tillampligaManader` när `manad` är satt; dagens två annual-anrop skickar aldrig `manad`
   så resultatet är identiskt, men en framtida `monthly_invoice`-väg måste utöka signaturen.
5. **P2: `KontraktBlockeratOrsak`/`KontraktBlockerat` bor i `besparingsvarde.ts`** — denna
   batchplans fillista hade redan rätt fil (oförändrad); det var
   `tariffinventering-v14.md`s normativa text som fel angav `resultatkontrakt.ts`, nu synkad.
6. **Dispositionerna 7/55/30/92 oförändrade** — samtliga v15-fynd var körbarhets-/
   typnings-/konsistensfel i redan beslutade kontraktsdesigner, ingen post flyttar.

**Historik — vad som var nytt i v14** (se granskning `2026-09-09-004` för fullständig
motivering; samtliga punkter rättades vidare i v15, se ovan):

1. **`forkontrolleraPolicyIndata` är omfattningsmedveten** (batch 0, §6a.2): ny
   `omfattning: Omfattning`-parameter, filtrerar `policy.kravdaFalt` med samma mönster som
   `harledResultatstatus`.
2. **`PolicyValideringsFel`s orsaksunion har dedikerade `'min'`/`'max'`/`'heltal'`** (batch 0,
   §6a.2), i stället för den tidigare ofullständiga `'typ'|'numerik'|'kardinalitet'|
   'okant_val'`-listan som saknade dessa tre.
3. **Konkret, konstruerbar `KontraktBlockerat`-väg** (batch 0, §6a.2): två nya `orsak`-värden
   och ett tredje, valfritt options-argument på konstruktorn — säkert mot samtliga 8
   verkliga anropsställen.
4. **`stodjerAktuellArskostnad` läser `.policy.kallenergiArsserieBindning`** (batch 0 punkt 9
   OCH Stockholm-avsnittet, §6a.4) — samma fel-objekt-bugg fanns på BÅDA ställena i v13,
   oberoende av varandra; `calcResultForOnskadTyp` kontrollerar nu `energySystem ===
   'fjarrvarme'` FÖRST, och `argsFranInputs`/`onskadTyp` matchar det rättade,
   realfältsbaserade designen i `tariffinventering-v14.md` §6a.4.

**Historik — vad som var nytt i v13** (se granskning `2026-09-09-003` för fullständig
motivering, samtliga punkter rättades vidare i v14, se ovan):

1. **Parserns felresultat kan nu genuint uttrycka en oinitierad state-nyckel, och EN delad
   orsaksunion ersätter det spridda, delvis odeklarerade språket** (batch 0, §6a.2): v12
   hade `parsaPolicyIndata(metadata, ravarde: PolicyRawFormValue)` UTAN `| undefined`, trots
   att en `Record`-uppslagning på en aldrig initierad statenyckel ger `undefined` vid
   runtime — signaturen kunde alltså inte kompilera mot sin egen punkt 2. v12 blandade
   dessutom `PolicyParseResultat`s `{status:'ogiltigt', orsak}` med det GAMLA
   `PolicyValideringsFel`/`'saknat'`-språket i `number_series`-beskrivningen, och denna
   batchplan använde en odeklarerad alias `PolicyValideringsOrsak` med `'min'|'max'|
   'heltal'` medan inventeringen bara hade `'numerik'` för samma tre. Nu: EN
   `PolicyValideringsOrsak = 'typ' | 'numerik' | 'kardinalitet' | 'min' | 'max' | 'heltal' |
   'okant_val'`, deklarerad en gång i `resultatkontrakt.ts`, använd IDENTISKT i inventering
   och batchplan; `PolicyParseResultat` är en strikt delmängd (`'typ'|'numerik'|
   'kardinalitet'`) av samma union.
2. **`saknadeFalt` är nu nåbart för ett direkt produktanrop, inte bara för formuläret**
   (batch 0, §6a.2 punkt 6): v12 påstod att den BEFINTLIGA `blocked`-vägen redan härledde
   `saknadeFalt` ur `harledResultatstatus` — verifierat FALSKT (`Resultatstatus` har inget
   fältnamnlistfält, och `harledResultatstatus` kastar bort sin lokala `saknade`-lista). Ny
   `forkontrolleraPolicyIndata(policy, prisar, indata): { saknade: string[]; ogiltiga:
   PolicyValideringsFel[] }` beräknar BÅDA listorna direkt ur `policy.kravdaFalt`/`indata`,
   oberoende av anroparen, och körs FÖRE fasadanropet i BÅDA de publika produktvägarna.
3. **EN produktförmågetabell, en auktoritativ rådatagrind, och en upprepad guard INUTI
   `beraknaArsprodukt`** (batch 7, §6a.4): v12 hade TRE-FYRA motsägande definitioner av
   `stodjerAktuellArskostnad` (denna batchplan sa "sann för varje kontraktsgated tariff" på
   flera ställen, medan inventeringens EGEN kapacitetstabell och testkrav — Sandviken
   `false`, Stockholm `true` — beskrev en smalare definition), och läste
   `prisar.policy?.kallenergiArsserieBindning` direkt i stället för via
   `kontraktsgatadPolicy(prisar)`. Nu: EN tabell (icke-fjärrvärmesystem → `false`;
   legacytariff → `false`; Sandviken → `false`; Stockholm → `true`), funktionen använder
   `kontraktsgatadPolicy(prisar)` som enda rådatagrind, och `beraknaArsprodukt` upprepar
   samma kontroll internt (fail-closed i domänlagret, inte bara i sidwrappern).
4. **`argsFranInputs` är en faktisk, typkorrekt funktion utan ellips** (batch 7, §6a.4): v12
   hade FORTFARANDE en tom `...`-kropp — samma hål v11-granskningen redan bad om att stänga —
   och lät `argsFranInputs` returnera `BesparingsvardeArgs`, som kräver `paverkbarMwh`/
   `besparingsgrad` trots att en aktuell-årskostnadsberäkning inte har någon av dem. Ny,
   delad `Tariffberakningsunderlag`-basstyp (total MWh efter scope-uppskalning, leverantör,
   kapacitet, `falt`/`policyFalt`, proveniens) byggs av `argsFranInputs` med faktisk
   pseudokod ur `calcResult`s befintliga, oförändrade logik; `beraknaArsprodukt` tar denna
   smalare typ direkt, `calcResult` självt och `BesparingsvardeArgs` självt förblir
   oförändrade.
5. **P2 rättat:** alla normativa korsreferenser pekar nu på v13-dokumenten (inte v12/v11/
   v10); den dubbla numreringen "9." i batchplanens innehållslista är rättad (se batch 7
   nedan); `bygg_ts()`s garanti korrigerad från "FULLT verifierad (båda riktningarna)" till
   "kör ENDAST riktning 2, för hela sin leverantörsfilsmängd"; `_bearbeta_leverantorsfil()`s
   policykälla korrigerad från "katalog-JSON" till `policyregister.py` (`generera.py` rad
   46–63); framtida acceptanstest skrivs "ska testas" fram till en verifierad kodleverans.
6. **Dispositionerna 7/55/30/92 oförändrade** — samtliga v13-fynd var körbarhets-/
   typnings-/konsistensfel i redan beslutade kontraktsdesigner, ingen post flyttar.

## Batch 0 — Grundkontrakt: diskriminerad värdetyp, bandbindning, seriekardinalitet och en genererad produkt-/UI-ingång (granskning 2026-09-08-007/-008/-009, 2026-09-09-001, P1)

**Krävs FÖRE varje batch som bär ett bandkrav** (1, 3, 3b, 4, 5a, 5b, 5c, 6 — se
`tariffinventering-v15.md` §6a.2:s 42-radstabell) OCH före batch 7 (Stockholms seriekrav
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
  7. **Typkorrekt parserresultat, EN delad orsaksunion (rättat P1, granskning
     `2026-09-09-003`, ersätter v12:s ännu ofullständiga signatur):** `type
     PolicyValideringsOrsak = 'typ' | 'numerik' | 'kardinalitet' | 'min' | 'max' | 'heltal' |
     'okant_val'` deklareras EN gång (`resultatkontrakt.ts`) och används identiskt av BÅDA
     dokumenten (v12:s batchplan använde denna alias UTAN att den någonsin deklarerades).
     Diskriminerad union `PolicyParseResultat = {status:'parsed', varde: PolicyInputValue} |
     {status:'saknat'} | {status:'ogiltigt', orsak: 'typ' | 'numerik' | 'kardinalitet'}` (en
     strikt delmängd av `PolicyValideringsOrsak`) som `parsaPolicyIndata(metadata,
     ravarde: PolicyRawFormValue | undefined)`s returtyp — v12:s signatur saknade
     `| undefined` trots att en `Record`-uppslagning på en oinitierad statenyckel ger
     `undefined` vid runtime, och blandade `PolicyParseResultat` med det gamla
     `PolicyValideringsFel`/`'saknat'`-språket i sin `number_series`-beskrivning.
     `KalkylatorPage.tsx` kör parsern över HELA `policyFaltMetadata`-listan (inte bara
     nycklar som råkar finnas i `policyFaltRavarden`), så samma tomma ELLER aldrig
     initierade fält alltid klassas `saknat` identiskt. **Rättat P1 (granskning
     `2026-09-09-005`) — explicita scalar/array-formgrindar:** varje skalär gren
     (`number`/`band_id_val`/`enum_val`) kräver FÖRST `typeof ravarde === 'string'`, och
     seriegrenen (`number_series`) kräver FÖRST `Array.isArray(ravarde)` — fel rå form ger
     `{status:'ogiltigt', orsak:'typ'}` omedelbart, INNAN `.trim()`/`.length`/iteration körs
     (en array till ett skalärt fält, eller en ensam sträng till ett seriefält, gav
     tidigare fel per-tecken-/`NaN`-beteende i stället för ett typat fel). Testfall (parser +
     sidintegration): array given till `number`/`band_id_val`, sträng given till
     `number_series`.
  8. **Felklassning — saknad OCH ogiltig indata, nåbar även för ett direkt produktanrop,
     omfattningsmedveten och med en konstruerbar `KontraktBlockerat`-väg** (rättat P1,
     granskning `2026-09-08-009`/`2026-09-09-002`/`2026-09-09-003`/`2026-09-09-004`): ny
     `forkontrolleraPolicyIndata(policy, prisar, indata, omfattning: Omfattning): { saknade:
     readonly string[]; ogiltiga: readonly PolicyValideringsFel[] }` (`PolicyValideringsFel =
     { nyckel: string; orsak: 'typ' | 'numerik' | 'kardinalitet' | 'min' | 'max' | 'heltal' |
     'okant_val' }` — **rättat P1, granskning `2026-09-09-004`:** samma dedikerade
     `'min'`/`'max'`/`'heltal'`-orsaker som tariffinventeringens union, inte den tidigare
     kollapsade `'numerik'` för alla tre gräns-/heltalsfall) beräknar BÅDA listorna i EN
     iteration över `policy.kravdaFalt.filter(f => f.kravsFor.includes(omfattning))` (**rättat
     P1, granskning `2026-09-09-004`:** v13 saknade `omfattning`-parametern och itererade
     hela `kravdaFalt` oavsett scope — samma filtermönster `harledResultatstatus` redan
     använder, rad ~373–374) mot den mottagna `indata`-kartan. **Rättat P2, granskning
     `2026-09-09-005`:** "samma filtermönster" gäller bara `f.kravsFor.includes(omfattning)`
     — den verkliga fasaden filtrerar ÄVEN på `tillampligaManader` när ett `manad`-argument
     är satt, vilket `forkontrolleraPolicyIndata` inte tar emot. Identiskt resultat i dag
     eftersom BÅDA anropsställena alltid skickar `'annual'` och aldrig `manad`; en framtida
     `monthly_invoice`-väg måste antingen utöka signaturen med samma valfria `manad?:
     number`-parameter, eller köras efter en separat månadsfiltrering — funktionen är
     MEDVETET bara omfattningsmedveten, inte månadsmedveten. — `saknade` för fält som INTE
     finns i `indata`, `ogiltiga` (`minVarde`/`maxVarde`/`heltal` som EGNA orsaker,
     bandmedlemskap via `f.vardetyp === 'band_id'` → `'okant_val'`) för fält som finns men
     bryter en regel. **Rättat P1, granskning `2026-09-09-003`:** v12 påstod att den
     BEFINTLIGA `blocked`-vägen redan härledde `saknadeFalt` ur `harledResultatstatus` —
     verifierat FALSKT (`Resultatstatus` har inget fältnamnlistfält, `harledResultatstatus`
     kastar bort sin lokala `saknade`-lista och returnerar bara `blocked`), så `saknadeFalt`
     var i praktiken onåbart för ett anrop som byggde sin `indata`-karta direkt utan att
     passera `KalkylatorPage.tsx`. `forkontrolleraPolicyIndata` har INGET sådant beroende —
     den körs FÖRE fasadanropet i BÅDA de publika produktvägarna
     (`beraknaBesparingsvardeKontrakt` skickar `'annual'`, `beraknaArsprodukt` skickar
     `'annual'`) och en icke-tom `saknade`/`ogiltiga` kastas som ett konkret, konstruerbart
     `KontraktBlockerat`: två nya `orsak`-värden på `KontraktBlockeratOrsak`
     (`missing_policy_fields`, `invalid_policy_fields`) och ett tredje, valfritt
     options-argument på konstruktorn (`new KontraktBlockerat(prisar.tariff_id,
     'missing_policy_fields', { saknadeFalt: saknade })` respektive `'invalid_policy_fields',
     { ogiltigaFalt: ogiltiga }`) — **rättat P1, granskning `2026-09-09-004`:** verifierat
     säkert mot samtliga 8 verkliga anropsställen i `besparingsvarde.ts`, INGET av dem
     skickar i dag ett tredje positionellt argument. Båda felfälten visas fältnära i
     `KalkylatorPage.tsx` (en separat UI-nivå-förkontroll vid submit, som en UX-genväg —
     inte den enda spärren); interna kontrakts-/konfigurationsfel reserveras för fall UTAN
     ett specifikt användarfält att peka på (§6a.2 punkt 6).
  9. **Namngiven produktentry för Stockholms aktuella årskostnad, EN gren, EN
     produktförmågetabell (rättat P1, granskning `2026-09-09-002`/`2026-09-09-003`,
     ersätter v11:s ouppnåeliga `{typ:'besparing'}`-gren och v12:s motsägande
     `stodjerAktuellArskostnad`-definitioner):** ny `beraknaArsprodukt(underlag:
     Tariffberakningsunderlag): ArsprodukResultat` i `besparingsvarde.ts` har bara
     `aktuell_arskostnad`-formen — v11:s andra gren konstruerades aldrig av den verkliga
     sidan och var en onödig, ouppnåelig omkonstruktion av det `calcResult` redan gör korrekt
     för Sandviken via `kontraktsgatadPolicy()`. `stodjerAktuellArskostnad(prisar): boolean`
     läser `kontraktsgatadPolicy(prisar)?.policy.kallenergiArsserieBindning !== undefined`
     (**rättat P1, granskning `2026-09-09-004`:** v13 läste `gated?.kallenergiArsserieBindning`
     direkt på `KontraktsgatadPolicy`-objektet — men `kallenergiArsserieBindning` bor PÅ
     `Tariffpolicy`, dvs. under `.policy`, inte på `KontraktsgatadPolicy`s toppnivå
     (`KontraktsgatadPolicy = { policy: Tariffpolicy; harAnnualInverse: boolean }`); buggen
     gav alltid `undefined` och fanns i BÅDA v13-dokumenten oberoende) — den enda tillåtna
     rådatagrinden, ALDRIG `prisar.policy?.X` direkt — och är därmed `false` för
     icke-fjärrvärmesystem, legacytariffer OCH Sandviken (kontraktsgatad men UTAN
     `kallenergiArsserieBindning`), `true` bara för Stockholm; **rättat P1, granskning
     `2026-09-09-003`:** v12 sa på flera ställen "sann för varje kontraktsgated tariff",
     vilket motsade inventeringens egen tabell/testkrav för just Sandviken. Kontrollen
     körs BÅDE i sidnivå-wrappern (UX-förkontroll, tidigt fel) OCH INUTI
     `beraknaArsprodukt` självt (den auktoritativa spärren — en ny PUBLIK domänentry
     litar aldrig på att anroparen redan kontrollerat detta); wrappern
     `calcResultForOnskadTyp` kontrollerar dessutom `inputs.energySystem === 'fjarrvarme'`
     FÖRST, INNAN någon tariff/policy-uppslagning görs (**rättat P1, granskning
     `2026-09-09-004`:** v13 lät `stodjerAktuellArskostnad` ensam avgöra, utan att
     kortsluta icke-fjärrvärmesystem innan kapacitetsuppslagningen). `argsFranInputs(inputs):
     Tariffberakningsunderlag` extraheras ur `calcResult`s befintliga scope-/
     proveniensuppbyggnad, byggd ENBART av fält verifierat existerande på
     `KalkylatorInputs` (**rättat P1, granskning `2026-09-09-004`:** v13:s skiss refererade
     de PÅHITTADE fälten/funktionerna `inputs.rumsvarmeAngiven`, `inputs.totalMwh`,
     `skalaUppRumsvarmeTillTotal(inputs)`, `mwhProvenansBekraftad(inputs)` som fristående
     funktion — inget av detta finns; de riktiga fälten är `energyMwh`, `energyScope`,
     `energyInputMode`). **Rättat P1 igen, granskning `2026-09-09-005`:** v14:s skiss
     jämförde ändå mot tre värden som inte finns i `EnergyScope`/`EnergyInputMode`
     (`'rumsvarme'`, `'rumsvarme_andel'`, `'confirmed_mwh'` — `TS2367` ×3, reproducerat mot
     de verkliga unionerna) och hade `totalMwh = totalMwh` som no-op i stället för den
     riktiga formeln. Nu skriven mot de FAKTISKA enumvärdena
     (`inputs.energyScope === 'space_heat_excl_dhw'`, `inputs.energyInputMode === 'mwh'`) och
     den verkliga formeln (`calcEnergyMwh(inputs)`, uppskalning `energyMwh / (1 -
     VARMVATTEN_ANDEL)` när rumsvärme angivits, `energyProvenance: 'confirmed_mwh'` bara när
     `energyInputMode === 'mwh'` OCH talet är ändligt och positivt) — verifierat kompilerbar
     mot riktig `KalkylatorInputs`/`calcEnergyMwh`/`VARMVATTEN_ANDEL` (`npx tsc --noEmit
     --strict --skipLibCheck`), se tariffinventering-v15.md §6a.4 för den fullständiga koden.
     `beraknaArsprodukt` tar denna smalare bastyp i stället för
     `BesparingsvardeArgs` (som kräver `paverkbarMwh`/`besparingsgrad` — fält en
     aktuell-årskostnadsberäkning inte har) och har nu en FULLSTÄNDIG, fail-closed kropp
     (**rättat P1, granskning `2026-09-09-005`**, tariffinventering-v15.md §6a.4): gate →
     bekräftad MWh-proveniens → ändlig positiv energi → kapacitet närvarande → kapacitet
     ändlig/heltal/≥golv (`kapacitetsGolv(prisar)`) → policyns fältnära förkontroll
     (`forkontrolleraPolicyIndata`, tom `policyFalt`-karta representeras explicit, ingen
     non-null-cast) → ETT anrop till fasaden — samma ordning/orsaker som
     `beraknaBesparingsvardeKontrakt` redan använder. `BesparingsvardeArgs` självt förblir
     OFÖRÄNDRAT, men `calcResult` ANROPAR nu `argsFranInputs` för sina tre
     `beraknaBesparingsvarde`-anrop (**rättat P1, granskning `2026-09-09-005`:** v14 sa
     fortfarande att `calcResult` "förblir oförändrad" och bygger scope-/provenienslogiken
     en ANDRA gång inline — nu delas byggnaden av basobjektet mellan aktuell-årskostnaden och
     besparingsvägen). ETT nytt, VALFRITT fält `onskadTyp?: 'besparing' |
     'aktuell_arskostnad'` på `KalkylatorInputs` (**rättat P1, granskning `2026-09-09-004`:**
     valfritt med implicit default `'besparing'`, inte obligatoriskt — ett obligatoriskt
     fält hade krävt en samtidig, brytande ändring av ~85 befintliga typade anropsställen;
     ENDA källan till beslutet — v11 hade den även som en separat wrapper-parameter).
     `calcResultForOnskadTyp` i `energiPotential.ts` kastar fail-closed INNAN
     `beraknaArsprodukt` anropas om `stodjerAktuellArskostnad` är `false` (eller om
     `energySystem` inte är `fjarrvarme`, se ovan), och returnerar numera `beraknaArsprodukt`s
     resultat DIREKT i stället för `{ typ: 'aktuell_arskostnad', ...resultat }` (**rättat P1,
     granskning `2026-09-09-005`:** den dubblerade `typ`-spridningen gav `TS2783` eftersom
     `ArsprodukResultat` redan bär `typ: 'aktuell_arskostnad'`). Besparingsvägen är den
     BEFINTLIGA `calcResult`-vägen (dess tre `beraknaBesparingsvarde`-anrop, nu byggda på det
     delade basobjektet) — inte en gren i `beraknaArsprodukt`; `KalkylatorPage.tsx` renderar
     `{ typ: 'aktuell_arskostnad' }` utan besparingsfält (§6a.4) eller
     `{ typ: 'fullstandig' }` (den oförändrade resultatsidan).
  10. `KravPost.tillatna_varden` (§6a.6) och `KravPost.maxvarde`/`Tariffpolicy.kapacitet_
      multiplikator_bindning`/`Tariffpolicy.flodeskorrigering_variant`/`Tariffpolicy.
      kallenergi_arsserie_bindning`/`Tariffpolicy.returtemperatur_arsserie_bindning`/
      `Tariffpolicy.ersatter_katalograd` (§6a.1/6a.3/6a.4/6a.5) — samtliga nya
      kontraktsfält samlas i SAMMA commit som grundarbetet, eftersom de delar samma
      `policyFranGenererad()`-mappningsbehov (§6a.1s tabell). **Rättat P2, granskning
      `2026-09-09-003`:** denna post hade tidigare felaktigt samma nummer ("9.") som
      föregående punkt.
- **Filer:** `resultatkontrakt.py`/`.ts` (samtliga nya fält, `vardetyp`-/`antal_varden`-gren
  i `harled_resultatstatus`/`harledResultatstatus`, ny `IndataVarde`-typ, ny
  `policyFaltMetadata`-signatur, ny `forkontrolleraPolicyIndata` med fullständig
  regeltäckning för BÅDE `saknade`/`ogiltiga`, ny `parsaPolicyIndata`/`PolicyParseResultat`,
  ny delad `PolicyValideringsOrsak`), `katalog.py` (`till_prisar` bandbevaring +
  unikhetskontroll — **rättat P2, granskning `2026-09-09-001`:**
  `kontrollera_adapterpreflight` ägs av `generera.py`, tillagd i batch 7, INTE av
  `katalog.py`, konsekvent med batch 7:s fillista), `faktura.py`/`fjarrvarme.ts`
  (`vald_niva_id`-parameter),
  `besparingsvarde.ts` (`byggIndataFranPolicy`, `KontraktBlockerat.saknadeFalt`/
  `ogiltigaFalt`, `ArsprodukResultat`, `Tariffberakningsunderlag`, `beraknaArsprodukt` — EN
  gren, tar `Tariffberakningsunderlag`, `stodjerAktuellArskostnad` via
  `kontraktsgatadPolicy`), `energiPotential.ts` (`KalkylatorInputs.onskadTyp`,
  `argsFranInputs` extraherad ur `calcResult`s befintliga logik och returnerar
  `Tariffberakningsunderlag`, `calcResultForOnskadTyp` fail-closed-dispatch —
  besparingsvägen är `calcResult` OFÖRÄNDRAD, inte en gren i `beraknaArsprodukt`),
  `KalkylatorPage.tsx` (nytt `policyFaltRavarden`-state, renderar
  `policyFaltMetadata` i stället för att anta `type="number"` för allt, fältnära
  `saknadeFalt`/`ogiltigaFalt`-visning, egen resultatsektion för `aktuell_arskostnad`),
  genererad testdata.
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
- **RÄTTAT P1 (granskning `2026-09-09-002`) — `bygg_ts()` kastade ALLTID mot det verkliga
  registret:** v11 lät `bygg_ts()` köra HELA `kontrollera_adapterpreflight` (riktning 1 +
  riktning 2) mot en TOM katalog `{"tariffs": []}` men det RIKTIGA, icke-tomma
  `ADAPTERREGISTER` — riktning 1 itererar VARJE registerpost och slår upp dess katalog-ID i
  `rak_katalog["tariffs"]`, vilket ALLTID misslyckas mot en tom lista, oavsett vilka
  leverantörsfiler som faktiskt byggs. `kontrollera_adapterpreflight` tar nu
  `rak_katalog: dict | None` och kör riktning 1 BARA när `rak_katalog is not None`; riktning
  2 (bijektionens reverse-led, byggd bara på `byggda_leverantorer`/`adapterregister`) körs
  ALLTID. `bygg_ts_fran_katalog()` anropar med den riktiga katalogen (fullständig
  tvåvägskontroll, som i dag); `bygg_ts()` anropar med `rak_katalog=None` (bara riktning 2)
  — en uttryckligen SNÄVARE, avgränsad garanti: `bygg_ts()` kan bevisa att en byggd
  leverantörsfils policy med `ersatter_katalograd` har en matchande `ADAPTERREGISTER`-post,
  men INTE att den posten i sin tur pekar på en verklig katalograd (den garantin kräver
  alltid `bygg_ts_fran_katalog()`). Stockholms markör passerar därmed `bygg_ts()` utan att
  kasta, utan att låtsas vara samma fullständiga bijektion som katalogvägen ger.
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
- **Namngiven produktentry, EN gren, EN produktförmågetabell (rättat P1, granskning
  `2026-09-09-002`/`2026-09-09-003`, ersätter v11:s ouppnåeliga tre-grensdesign och v12:s
  motsägande `stodjerAktuellArskostnad`):** en bar `beraknaArskostnadMedKontrakt`-anrop
  djupt i motorn gör inget visningsbart för användaren. Ny, diskriminerad
  `ArsprodukResultat`-union med BARA `{typ:'aktuell_arskostnad', kostnad, leverantor,
  prisar, kapacitetKw, status}` och funktionen `beraknaArsprodukt(underlag:
  Tariffberakningsunderlag): ArsprodukResultat` i `besparingsvarde.ts` (Batch 0, punkt 9) —
  v11:s andra gren (`{typ:'besparing',...}` för kontraktsgated tariffer utan Stockholms
  serie) konstruerades ALDRIG av den verkliga sidan (`calcResult` känner inte till
  `beraknaArsprodukt`) och var en onödig omkonstruktion av det Sandvikens BEFINTLIGA väg
  redan gör korrekt. Besparing går nu uttryckligen via den OFÖRÄNDRADE `calcResult` (dess
  tre `beraknaBesparingsvarde`-anrop, som redan routar Sandviken till kontraktsgrenen via
  `kontraktsgatadPolicy()` och redan kommer blockera Stockholm via samma före/efter-guard
  så snart `_kraver_kontrakt` är satt — ingen ny dispatchkod krävs för den guarden). Ny
  `stodjerAktuellArskostnad(prisar): boolean` läser `kontraktsgatadPolicy(prisar)?.policy.
  kallenergiArsserieBindning !== undefined` (**rättat P1, granskning `2026-09-09-004`:**
  `kallenergiArsserieBindning` bor under `.policy` på `KontraktsgatadPolicy`, inte på dess
  toppnivå — v13 läste fel objekt här också, samma bugg som Batch 0 punkt 9, oberoende
  återskriven på detta ställe) — **rättat P1, granskning `2026-09-09-003`:** INTE "sann för
  varje kontraktsgated tariff" (v12:s påstående på detta ställe, som motsade Batch 0 punkt
  9:s tabell där Sandviken är `false`) — och kontrolleras BÅDE av `calcResultForOnskadTyp`
  (UX-förkontroll) OCH INUTI `beraknaArsprodukt` självt (den auktoritativa spärren, se
  Batch 0 punkt 9). `calcResultForOnskadTyp(inputs: KalkylatorInputs):
  KalkylatorResultUnion` i `energiPotential.ts` kontrollerar FÖRST `inputs.energySystem ===
  'fjarrvarme'` (**rättat P1, granskning `2026-09-09-004`:** kortsluts till avslag INNAN
  någon tariff-/policyuppslagning görs för ett icke-fjärrvärmesystem), läser sedan
  `inputs.onskadTyp` (ENDA källan, VALFRITT fält med implicit default `'besparing'`) och
  kastar fail-closed INNAN `beraknaArsprodukt` anropas om förmågan är `false`.
  `KalkylatorPage.tsx` renderar en egen resultatsektion för `{typ:'aktuell_arskostnad'}`,
  helt utan besparingsfält, eller den befintliga sidan för `{typ:'fullstandig'}`.
- **Avvikande regler:** rör INTE det redan godkända `monthly_invoice`-kontraktet — dess
  `kravs_for=("monthly",)`-krav och period-/upplösningssemantik lämnas oförändrade.
- **Filer:** `resultatkontrakt.py`/`.ts` (2 nya serie-`KravPost`, 2 nya
  `Tariffpolicy`-bindningar, `returtemp_c_per_manad`-parametern, seriekravens
  `antal_varden`-validering), `policyregister.py` (utökad `_stockholm_exergi_policy` med
  breddat effektkrav, `ersatter_katalograd` + nytt `ADAPTERREGISTER`), `generera.py`
  (`kontrollera_adapterpreflight(rak_katalog: dict | None, ...)`, `bygg_ts_fran_katalog()`
  anropar med den riktiga katalogen, `bygg_ts()` med `rak_katalog=None` och kör därmed
  ENDAST riktning 2 — se bijektionsfixet ovan — samt `_bearbeta_leverantorsfil()`s
  `_kraver_kontrakt`-sättning, oförändrat läst via `policyregister.py`, ALDRIG från
  katalog-JSON), `besparingsvarde.ts` (`ArsprodukResultat` med EN gren,
  `Tariffberakningsunderlag`, `beraknaArsprodukt` som tar den smalare typen,
  `stodjerAktuellArskostnad` via `kontraktsgatadPolicy`, det typade
  besparings-exkluderingsfelet i `beraknaBesparingsvardeKontrakt`, oförändrad),
  `energiPotential.ts` (`KalkylatorInputs.onskadTyp`, `argsFranInputs` extraherad ur
  `calcResult`s befintliga logik och returnerar `Tariffberakningsunderlag`,
  `calcResultForOnskadTyp` fail-closed-dispatch, `calcResult` självt OFÖRÄNDRAT och
  `BesparingsvardeArgs` självt OFÖRÄNDRAT), `KalkylatorPage.tsx` (anropar
  `calcResultForOnskadTyp`, rendering av `aktuell_arskostnad` respektive `fullstandig`).
- **Teststrategi:** eget källverifierat referensfall (inte bara Åkermannen-fixturens
  månadsdata återanvänd rakt av för ett annat ändamål), kontraktsfasadtest för
  `annual_forward` med den nya seriemodellen (inkl. fel längd 11/13 respektive 4/6 element
  blockerar via `antal_varden`), regressionstest att `monthly_invoice`-vägen är oförändrad,
  ett test att `kontrollera_adapterpreflight` kastar på fel `provider_id`, fel `tariff_id`,
  saknad/stale mappning, ELLER en `ersatter_katalograd`-policy utan matchande adapterpost
  (den omvända regeln), ett test med TVÅ olika injicerade register som ger olika resultat,
  ett test att `bygg_ts()` (kallad med det VERKLIGA produktionsregistret och Stockholms
  markör) passerar utan att kasta medan `bygg_ts_fran_katalog()` fortsatt ger den fullständiga
  tvåvägskontrollen för samma leverantörsfilsdata (regressionstest mot v11:s design, som
  aldrig kunde lyckas mot produktionsregistret), ett test att effektkravet nu gäller BÅDA
  `monthly`/`annual`, ett sidtest via `calcResultForOnskadTyp` att
  `inputs.onskadTyp:'aktuell_arskostnad'` för Stockholm visar kostnad UTAN besparingssiffra
  medan `inputs.onskadTyp:'besparing'` (den OFÖRÄNDRADE `calcResult`-vägen) kastar det typade
  exkluderingsfelet i `beraknaBesparingsvardeKontrakt`, ett tredje sidtest att
  `inputs.onskadTyp:'besparing'` för Sandviken fortsatt ger en komplett `Besparingsvarde`
  (regressionstest att omdesignen inte rör den redan godkända vägen), OCH ett test att
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
