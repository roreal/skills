# Tariffinventering v19.0 — fullständig kontrollmängd för kalkylator v1

Upprättad 2026-09-09 av Claude. Ersätter `tariffinventering-v18.md` i sin helhet (v18 ändras
INTE i efterhand — kvar som historik), som svar på omgranskning
[2026-09-09-012](../conversations/reviews/2026/09/2026-09-09-omgranskning-tariffinventering-v18.md)
(`status: changes-required`, supersedes `2026-09-09-011`) av v18/`batchplan-v18.md`. Ingen
produktkod, tariffdata eller genererad fil är ändrad av detta dokument. Ingen tariff
aktiveras. Dispositionerna är OFÖRÄNDRADE sedan v16: **7 implementerade / 57 redo / 28
blockerade / 92 totalt** (bas 7/47/24, variant 0/10/4; se §4.2 och §8) — v19 gör bara
Lidköpings implementationsplan körbar, flyttar ingen post. Alla kodpåståenden nedan är
verifierade genom att läsa den verkliga koden i
`neptune_academy@HEAD` (`besparingsvarde.ts`, `resultatkontrakt.ts`, `energiPotential.ts`) —
bl.a. `harledResultatstatus`s faktiska `blocked`-retur (bara för SAKNADE fält, rad 378–380,
listan själv aldrig returnerad) mot dess `Error`-kastande valideringsloop (rad 385–420),
`Resultatstatus` (rad 262–266, bara omfattning/noggrannhet/fullständighet, inga fältnycklar),
`BesparingsvardeArgs`s obligatoriska `totalMwh`/`paverkbarMwh`/`besparingsgrad` (rad 204–208),
`KontraktBlockerat`s 5 befintliga `orsak`-värden och dess 8 verkliga anropsställen (inget
skickar ett tredje positionellt argument i dag), `KontraktsgatadPolicy = { policy:
Tariffpolicy; harAnnualInverse: boolean }` och `kontraktsgatadPolicy(prisar)`s signatur,
`Omfattning`-filtreringsmönstret `policy.kravdaFalt.filter(f =>
f.kravsFor.includes(omfattning))` (rad ~373–374, ~555), `KalkylatorInputs`s verkliga fält
(`energySystem`, `energyMwh?`, `energyScope?`, `energyInputMode?`, `leverantorId?`,
`kapacitetKw?`, `falt?` — inget `rumsvarmeAngiven`/`totalMwh`), och `calcResult`s fullständiga
kropp (rad ~405–545) — inte bara omskrivna från granskningen.

**Vad som är nytt i v19, i korthet** (se granskning `2026-09-09-012` för fullständig
motivering till varje punkt):

1. **De två säkerhetskritiska policyfälten transporteras nu HELA vägen** (§6a.1, rättar P1
   #1): `Tariffpolicy.stodjer_besparing`/`stodjerBesparing` och
   `KravPost.krav_attestering`/`kravAttestering` tillagda i transporttabellen (16 fält, inte
   14), OCH i `skapaTariffpolicy()`s options-typ OCH returvärde — den plats v18 helt
   missade. Negativa transporttester bevisar att explicit `false`/`true` överlever
   generering, och att frånvaro ger `false` (fail-closed), aldrig `undefined`.
2. **Tm-attesteringen är nu auktoritativ även för direkta anrop** (§6a.7.6, rättar P1 #2):
   ny `IndataPost.attesterad`-fält, kontrollerat i den auktoritativa
   `harledResultatstatus`/`harled_resultatstatus` för VARJE krav med `kravAttestering=true`
   — inte bara en UI-kryssruta. Ett direkt fasadanrop utan attestering blockeras nu i test.
3. **`Produktbegransning`-guarden flyttad in i den verkliga femparametersfunktionen**
   (§6a.4, rättar P1 #3): `beraknaBesparingsvardeKontrakt(args, leverantor, prisar,
   kapacitetGolv, policy)`, oförändrad signatur, guard som första sats. Testtexten använder
   nu rätt entry/typ (`BesparingsvardeArgs`, inte `onskadTyp` på fel objekt). Den fiktiva
   `besparingsvarde.py` borttagen — ingen Python-produktkonsument av detta slag finns.
4. **Besparingsförmågan är nu fail-closed** (§6a.4, rättar P1 #4): `stodjer_besparing`s
   Python-default ändrad `True`→`False`; TypeScript-resolvern `!== false`→`=== true`.
   Sandviken explicit `True`; Stockholm och Lidköping explicit `False`; legacyvägen
   oförändrad.
5. **Äldre normativa capability-/"oförändrad"-stycken ERSATTA, inte kompletterade** (§6a.4,
   rättar P1 #5): den tidigare korrigeringskedjan är nu tydligt märkt historik/motivering,
   inte normativ text; EN gällande tabell och resolver för båda förmågorna.
6. **Batch 5d:s fillista rättad** (rättar P1 #6): den verkliga
   `optimate-fjarrvarme-2026.json`-katalogfilen, `katalog.py`-schema/grind och sex namngivna
   test-filer, med dokument- vs. implementationsscope explicit åtskilt.
7. **P2: delade elementvisa validatorns ägare/import konkretiserad** (§6a.1): exporterad
   `vardefelForKrav` i `resultatkontrakt.ts`, importerad av `besparingsvarde.ts`; Python-
   motsvarigheten i samma modul, ingen korsimport.
8. Samtliga P1/P2-fynd t.o.m. granskning `2026-09-09-011` (v18:s Tm-käll-/noggrannhetsmodell,
   den elementvisa min-/max-/heltalsalgoritmen, `Produktbegransning`s felmodell, Batch 5d:s
   katalogfil m.fl.) är BEVARADE oförändrade i sak.

**Vad som var nytt i v18, i korthet** (se granskning `2026-09-09-011` för fullständig
motivering till varje punkt):

1. **`Tm_m`s källtyp återanvänder befintlig `supplier_value`, ingen ny `KALLTYPER`-/
   `Noggrannhet`-medlem** (§6a.7.6, rättar P1 #1): `noggrannhet: 'snapshot'` kommer
   AUTOMATISKT av att alla tre serie-krav redan måste ha `rullande=True`
   (→ `ar_ej_helt_verifierbar`) — v17:s ogiltiga `kallaTyp: 'snapshot'`/interna
   `noggrannhet: 'uppskattat'` är borttagna. Ny, separat `kravAttestering`-UI-metadataflagga
   löser källattesteringsbehovet utan att röra käll-/noggrannhetskontraktet.
2. **`minExklusiv`/min-/max-/heltalskontroll är elementvis och delad mellan förkontroll och
   ordinarie validator, i BÅDA språken** (§6a.1/§6a.7.5, rättar P1 #2): ny delad
   `vardefelForKrav`/`_vardefel_for_krav`-funktion ersätter den skalära
   `post.varde < f.minvarde`-jämförelsen v17 skrev; verifierad via BÅDE
   `forkontrolleraPolicyIndata` och ett direkt fasadanrop.
3. **Ett konkret produktbegränsningsfel, `Produktbegransning`** (§6a.4, rättar P1 #3): egen
   klass/orsak/konstruktor, en explicit guard i `beraknaBesparingsvardeKontrakt`, egen
   UI-mappning skild från `KontraktBlockerat`, tester för Stockholm och Lidköping. Ersätter
   v17:s självmotsägande "inte `KontraktBlockerat`"/"`KontraktBlockerat`/motsvarande"-text.
4. **Äldre `kallenergiArsserieBindning`-baserad capability-text ERSATT i stället för
   kompletterad** (Batch 0 punkt 9 och Batch 7 i batchplanen, §6a.4 i inventeringen, rättar
   P1 #4): all text läser nu förmågan från `stodjer_aktuell_arskostnad`/
   `stodjerAktuellArskostnad`, nämner Lidköping i tabeller/tester, och §6a.5-hänvisningarna
   till förmågekontraktet är rättade till §6a.4 (Lidköpings egen sektion är §6a.7).
5. **Batch 5d:s fillista rättad och uppdelad i dokument- vs. implementationsscope** (rättar
   P1 #5): katalogens `adjustments`-post ligger i `Fjarrvarmetariffer/
   optimate-fjarrvarme-2026.json` (läst av `katalog.py`), inte i `generera.py`; namngivna
   Python-/TypeScript-testfiler tillagda.
6. **P2: `stodjer_aktuell_arskostnad`/`stodjer_besparing` separerade som två oberoende
   deklarativa fält** (§6a.4) — en framtida tariff kan nu i princip stödja båda produkterna
   utan kodundantag. Batch 5d:s testfiler namngivna explicit (andra P2-fyndet).
7. Samtliga P1/P2-fynd t.o.m. granskning `2026-09-09-010` (v17:s motortransport, kanoniska
   `type`-diskriminator, `faltSerier`-kanal, Lidköpings källgodkännande, Åkermannen-underlag,
   m.fl.) är BEVARADE oförändrade i sak.

**Vad som var nytt i v17, i korthet** (se granskning `2026-09-09-010` för fullständig
motivering till varje punkt):

1. **Lidköpings tre serier når nu den verkliga tariffmotorn** (§6a.7.1–§6a.7.3, rättar P1
   #1): kanonisk `type: "signed_monthly_flow_adjustment"`-diskriminator (inte `typ`),
   registrering i BÅDA språkens `JUSTERINGSTYPER`/`JUSTERING_BERAKNING`, och en additiv
   `faltSerier`/`falt_serier`-kanal trädd genom hela kedjan `beraknaArskostnadMedKontrakt` →
   `_arskostnadForKontraktfasad` → `justeringar()` → `Kostnad.justering` — extraherad ur
   `inrapporteradIndata` per `KravPost.vardetyp` i stället för att kasta. Isolerat
   compile-verifierad.
2. **Lidköpings "aktuell årskostnad" är nu explicit nåbar, besparingsvägen explicit
   blockerad** (§6a.4, rättar P1 #2): nytt `Tariffpolicy.stodjer_aktuell_arskostnad`-fält,
   satt av `policyregister.py`, ersätter den indirekta Stockholmsspecifika
   `kallenergiArsserieBindning`-kontrollen. Samma flagga blockerar Lidköpings besparingsväg
   med ett typat produktbegränsningsfel tills en källförsvarbar före/efter-regel finns.
   Ändrar inte `ready_to_implement`-status för Stockholm eller Lidköping.
3. **`KravPost.minvarde_exklusiv`/`minExklusiv` vald mekanism** (§6a.1/§6a.7.5, rättar P1
   #3): fältnära `invalid_policy_fields`/`'min'` för `Tm_m ≤ 0`, kontrollerat FÖRE division.
4. **`BesparingsvardeArgs`/`calcResult`-motsägelsen eliminerad** (rättar P1 #4): ett enda
   konsekvent språk i BÅDA dokumenten — `BesparingsvardeArgs` ändras additivt, `calcResult`
   behåller publikt returkontrakt/beteende men ändrar intern argumentbyggnad.
5. **P2:** `Tm_m`s proveniens preciserad till `kallaTyp: 'snapshot'` med obligatorisk
   källhjälptext (§6a.7.6, ersätter det självmotsägande `'supplier_value'`-språket); tio
   felaktiga §6a.6→§6a.7-hänvisningar rättade (§6a.6-mönstret vid Batch 5d:s inledning
   kvarstår, avsiktligt); EOF-blankraden `git diff --check` fann i granskning 009-filen
   rättad.
6. Samtliga P1/P2-fynd t.o.m. granskning `2026-09-09-007`/bedömning `2026-09-09-006`
   (v16:s `beraknaArsprodukt`, `policyFalt`-transport, Lidköpings källgodkännande,
   Åkermannen-underlag, m.fl.) är BEVARADE oförändrade i sak.

**Vad som var nytt i v16, i korthet** (se granskning `2026-09-09-007` och bedömning
`2026-09-09-006` för fullständig motivering till varje punkt):

1. **`beraknaArsprodukt`s kropp är omskriven och strikt typkontrollerad som en HELHET**
   (§6a.4, rättar P1 #1, granskning `2026-09-09-007`): sex oberoende fel i v15:s skiss
   rättade — `prisar.tariff_id` (inte `.id`), `byggKontraktIndata` körs FÖRE förkontrollen så
   `forkontrolleraPolicyIndata` får den byggda `ReadonlyMap<string, IndataPost>` (inte det
   råa `Record`), två SEPARATA `KontraktBlockerat`-kast utan `as any`
   (`missing_policy_fields`/`invalid_policy_fields`), rätt argumentordning/antal till
   `beraknaArskostnadMedKontrakt(prisar, policy, indata, ar, mwhPerManad)` med
   `fordelaEnergi(totalMwh).totalt` som femte argument, `KontraktResultat` avsmalnad
   (`status.fullstandighet === 'blocked'`/`kostnad === null`) innan kostnaden läses, och
   `leverantor.namn` från `valjLeverantorOchPrisar`-destruktureringen i stället för det
   obefintliga `prisar.leverantor`. Verifierat med en isolerad `npx tsc --noEmit --strict
   --skipLibCheck --target es2020` mot de verkliga typerna/funktionerna i
   `neptune-marketing` — se §6a.4 för kommandot och resultatet.
2. **`policyFalt`-kontraktet är nu entydigt genom hela besparingsvägen** (§6a.4, rättar P1
   #2): `policyFalt?: Record<string, PolicyInputValue>` är ett additivt, valfritt fält på
   `BesparingsvardeArgs` — `beraknaBesparingsvarde` skickar redan (verifierat,
   `besparingsvarde.ts` rad 361) HELA `args` vidare till `beraknaBesparingsvardeKontrakt`,
   som nu anropar `byggKontraktIndata(policy, prisar, kapacitetKw, args.policyFalt ?? {})`
   och kör `forkontrolleraPolicyIndata` på den BYGGDA kartan, i stället för att bara lägga in
   kapacitetsbindningen ensam. Legacyvägen (`beraknaBesparingsvarde`s icke-kontraktsgren)
   fortsätter ignorera fältet — samma bakåtkompatibla mönster som `energyProvenance` redan
   har. Samma beslut i BÅDA v16-dokumenten.
3. **P2: `calcResult`s publika kontrakt vs. dess interna implementation är nu
   otvetydigt.** `calcResult`s publika resultat och beräkningsbeteende förblir OFÖRÄNDRADE;
   det som ändras är enbart INTERN argumentbyggnad (anropar den delade `argsFranInputs` i
   stället för att duplicera scope-/provenienslogiken inline).
4. **Lidköping Energis två bastariffer flyttade från `blocked_external_info` till
   `ready_to_implement`** (§4.2, §8, bedömning `2026-09-09-006`): leverantörens skriftliga
   svar 2026-09-09 bekräftar flödesprisfaktorn `N = 5 kr/m³` och hur `Tm` bestäms.
   Dispositionen ändras 7/55/30 → **7/57/28** av 92 (bas 7/47/24, variant oförändrat 0/10/4).
   Ny batch 5d i `batchplan-v17.md` och en ny deklarativ, signerad
   nätmedelavkylningsjustering — se §6a.7.
5. Samtliga P1/P2-fynd t.o.m. granskning `2026-09-09-005` (v15:s scope-/provenienslogik,
   parsergrindar, `KontraktBlockerat`-optionsväg, m.fl., se historiken nedan) är BEVARADE
   oförändrade — bara de tre punkterna ovan och Lidköping-tillägget skiljer v16 från v15.

**Vad som är nytt i v14, i korthet** (se granskning `2026-09-09-004` för fullständig
motivering till varje punkt; samtliga fyra är P1-fynd, plus två bekräftade P2-relaterade
poster oförändrade):

1. **`forkontrolleraPolicyIndata` är nu omfattningsmedveten** (§6a.2): ny parameter
   `omfattning: Omfattning`, filtrerar `policy.kravdaFalt` med EXAKT samma mönster som
   `harledResultatstatus` redan använder, i stället för att iterera ALLA krav oavsett
   anroparens scope.
2. **`PolicyValideringsOrsak` har EN modell överallt: dedikerade `'min'`/`'max'`/`'heltal'`**
   (§6a.2) — den tidigare kollapsade `orsak: 'numerik'`-varianten för gräns-/heltalsbrott är
   borttagen från förkontrollen; `'numerik'` reserveras nu för icke-ändliga tal.
3. **En konkret, konstruerbar `KontraktBlockerat`-väg** (§6a.2): två nya `orsak`-värden
   (`missing_policy_fields`, `invalid_policy_fields`) och ett tredje, valfritt
   options-argument till konstruktorn (`{ status?, saknadeFalt?, ogiltigaFalt? }`) — verifierat
   säkert eftersom inget av de 8 verkliga anropsställena i dag skickar ett tredje argument.
4. **`stodjerAktuellArskostnad` läser rätt objektsväg** (§6a.4): `gated?.policy.
   kallenergiArsserieBindning` i stället för `gated?.kallenergiArsserieBindning` (fel objekt,
   alltid `undefined`) — buggen fanns i BÅDA v13-dokumenten oberoende av varandra.
5. **`calcResultForOnskadTyp` kontrollerar energisystem FÖRE tariffuppslagning** (§6a.4): ett
   icke-fjärrvärmesystem kortsluts till `false` innan någon kontraktspolicy ens slås upp.
6. **`argsFranInputs` bygger bara på fält som verifierat finns på `KalkylatorInputs`** (§6a.4):
   ersätter den påhittade `rumsvarmeAngiven`/`totalMwh`/`skalaUppRumsvarmeTillTotal`/
   `mwhProvenansBekraftad(inputs)`-skissen med en extraktion ur `calcResult`s verkliga,
   verifierade fältnamn (`energyMwh`, `energyScope`, `energyInputMode`).
7. **`onskadTyp` är valfritt med implicit default `'besparing'`** (§6a.4), inte obligatoriskt
   — undviker en samtidig, brytande ändring av ~85 befintliga typade anropsställen.
8. **`GenereradPrisarspost` är nu definierad** (§6a.1, bekräftat P2): tidigare bara använd,
   aldrig deklarerad i v9–v13; ny, smal `interface` som ersätter `any` på just de positioner
   §6a:s funktioner läser.

**Historik — vad som var nytt i v13** (bevarat för spårbarhet, INTE en beskrivning av v14:s
aktuella design — samtliga punkter nedan rättades vidare i v14, se ovan):

1. **Parserkontraktet uttrycker nu genuint en frånvarande state-nyckel, och den gamla
   `PolicyValideringsFel`/`'saknat'`-språket är helt borttaget ur parserbeskrivningen**
   (§6a.2, rättat P1, granskning `2026-09-09-003`): `parsaPolicyIndata(metadata,
   ravarde: PolicyRawFormValue | undefined)` accepterar nu uttryckligen `undefined`
   (en `Record`-uppslagning på en aldrig initierad nyckel ger `undefined` vid runtime,
   vilket v12:s signatur `ravarde: PolicyRawFormValue` inte kunde ta emot). En enda
   deklarerad orsaksunion (`PolicyValideringsOrsak = 'typ' | 'numerik' | 'kardinalitet' |
   'min' | 'max' | 'heltal' | 'okant_val'`) delas nu mellan parsern OCH domänvalidatorn i
   BÅDA dokumenten — v12 hade parsern återanvända den gamla `PolicyValideringsFel`-typen
   för fel kardinalitet/tomt serieelement (inklusive den obefintliga orsaken `'saknat'`)
   samtidigt som batchplanen använde en odefinierad alias `PolicyValideringsOrsak` med
   `'min'|'max'|'heltal'` medan inventeringen valde `'numerik'` för samma tre — nu ETT
   exakt utfall per fall: frånvarande nyckel/blank skalär/blankt serieelement →
   `{status:'saknat'}`; fel kardinalitet/icke-numeriskt värde → `{status:'ogiltigt',
   orsak:'kardinalitet'|'numerik'}`; explicit `"0"` → `{status:'parsed', varde:0}`.
2. **`saknadeFalt` är nu verkligen nåbart för ett direkt produktanrop, inte bara för
   formuläret** (§6a.2, rättat P1, granskning `2026-09-09-003`): v12 påstod att den
   BEFINTLIGA `blocked`-vägen redan härledde `saknadeFalt` ur `harledResultatstatus`s
   status — **verifierat FALSKT mot verklig kod:** `Resultatstatus`
   (`resultatkontrakt.ts` rad 262–266) innehåller bara omfattning/noggrannhet/
   fullständighet, och `harledResultatstatus` (rad 378–380) bygger en lokal `saknade`-
   lista men returnerar bara generiskt `blocked` — nycklarna försvinner. Ny, sluten
   förkontroll `forkontrolleraPolicyIndata(policy, prisar, indata): { saknadeFalt:
   string[]; ogiltigaFalt: PolicyValideringsFel[] }` kontrollerar BÅDA närvaro (mot
   `policy.kravdaFalt`) OCH värde för varje relevant krav i vald omfattning, körs i BÅDA
   publika produktvägarna (`beraknaBesparingsvardeKontrakt`/`beraknaArsprodukt`) FÖRE
   fasaden — domänlagret äger nu spärren självt, oberoende av om anropet kom via
   formuläret eller direkt.
3. **En enda produktförmågetabell, en auktoritativ rådatagrind, och en upprepad guard
   INUTI `beraknaArsprodukt`** (§6a.4, rättat P1, granskning `2026-09-09-003`): v12 hade
   TRE olika, motsägande definitioner av `stodjerAktuellArskostnad` spridda över båda
   dokumenten (`sann för varje kontraktsgated tariff` mot `sann bara när
   kallenergiArsserieBindning finns`), och läste `prisar.policy?.kallenergiArsserieBindning`
   DIREKT i stället för via den enda tillåtna resolvern `kontraktsgatadPolicy(prisar)` —
   samt lade guarden ENDAST i sidwrappern, med `beraknaArsprodukt` uttryckligen
   odokumenterat oskyddad som en ny PUBLIK domänentry. Nu: EN tabell (icke-fjärrvärmesystem
   → `false`; legacytariff → `false`; Sandviken → `false`; Stockholm → `true`), funktionen
   använder `kontraktsgatadPolicy(prisar)` som enda rådatagrind, och den auktoritativa
   kontrollen upprepas INUTI `beraknaArsprodukt` — wrapperns kontroll är en UX-förkontroll,
   inte den enda spärren.
4. **`argsFranInputs` är en faktisk, typkorrekt funktion utan ellips, och
   `beraknaArsprodukt` kräver inte längre påhittade besparingsfält** (§6a.4, rättat P1,
   granskning `2026-09-09-003`): v12:s kodexempel hade FORTFARANDE en tom `...`-kropp —
   samma hål v11-granskningen redan bad om att stänga. Ny delad
   `Tariffberakningsunderlag`-basstyp (total MWh efter scope-normalisering, leverantör,
   kapacitet, `falt`, `policyFalt`, proveniens) byggs av `argsFranInputs` med FAKTISK
   pseudokod extraherad ur `calcResult`s befintliga, verifierade logik (rumsvärme-scope-
   uppskalning, `mwhProvenansBekraftad`) — besparingsvägen lägger EFTERÅT till
   `paverkbarMwh` och respektive min/mid/max-grad för att bilda `BesparingsvardeArgs`,
   medan `beraknaArsprodukt` nu tar den SMALARE `Tariffberakningsunderlag` direkt, utan
   ett enda påhittat `paverkbarMwh: 0`/`besparingsgrad: 0`.

**Historik — vad som var nytt i v12** (bevarat för spårbarhet, INTE en beskrivning av v13:s
aktuella design — flera av punkterna nedan beskrivs som v12 löste dem, men samtliga fyra
rättades sedan YTTERLIGARE i v13 — se "Vad som är nytt i v13" ovan och §6a.2/§6a.4 för den
gällande designen):

1. Parserns felresultat blev en diskriminerad union (`parsed`/`saknat`/`ogiltigt`) — men
   signaturen kunde ännu inte ta emot `undefined`, och `PolicyValideringsFel`/`'saknat'`-
   språket levde kvar i samma avsnitts elementvisa serie-beskrivning. Se punkt 1 ovan.
2. `valideraPolicyIndata` täckte `minVarde`/`maxVarde`/`heltal`, men bara för fält som
   redan FANNS i indatakartan — saknade fält förblev onåbara för ett direkt produktanrop.
   Se punkt 2 ovan.
3. `bygg_ts()` fick ett körbart, avgränsat anropskontrakt (rättningen KVARSTÅR oförändrad
   i v13, se §6a.4 nedan) — den enda P1-delen av v12 som INTE fick ett nytt fynd i
   granskning `2026-09-09-003`.
4. Årsproduktdispatchen fick EN källa till `onskadTyp`, men produktförmågan
   (`stodjerAktuellArskostnad`) definierades motsägande på fyra olika ställen och
   `argsFranInputs` var fortfarande en `...`-platshållare. Se punkt 3–4 ovan.

**Historik — vad som var nytt i v11** (bevarat för spårbarhet, INTE en beskrivning av v13:s
aktuella design; se "Vad som är nytt i v13" och "v12" ovan samt §6a.2/§6a.4 för den gällande
designen):

1. **Rått formulärstate skilt från den parsade policy-DTO:n.** v10 lät
   `Record<string, PolicyInputValue>` VARA React-state, men ett HTML-talfält bär en STRÄNG
   medan användaren skriver — en delvis ifylld serie är `string[]`, som den föreslagna
   state-typen inte kan bära. Ett `Number('')===0`-fail-open hade dessutom gjort en tom eller
   delvis tom serie till en giltig nollserie. §6a.2 inför ett SEPARAT rått formulärstate
   (`PolicyRawFormValue = string | readonly string[]`) och en enda strikt parser till
   `PolicyInputValue` som trimmar/klassificerar tomma rutor FÖRE `Number(...)`, kräver
   samtliga serieelement, och konverterar Jönköpings NUMERISKA enum till tal medan band-ID
   förblir sträng — de kan inte längre delas av regeln "enum/band parsas aldrig", eftersom
   Jönköpings `tillatna_varden` uttryckligen är `tuple[float, ...]`.
2. **En körbar, typad felkanal för ogiltig indata — inte ett läsförsök i ett
   `blocked`-resultat som aldrig returneras.** Verifierat att `harledResultatstatus` bara
   returnerar `blocked` för SAKNADE fält; ogiltig typ/numerik/serieform/gräns kastar `Error`
   i valideringsloopen, så det finns inget statusobjekt att läsa ur efter ett ogiltigt värde.
   §6a.2 inför i stället en separat `valideraPolicyIndata(policy, prisar, indata)`-funktion
   som körs FÖRE fasadanropet och returnerar `{nyckel, orsak}[]` (inklusive banduppslag mot
   vald prispost) — `beraknaBesparingsvardeKontrakt` mappar en icke-tom lista till
   `KontraktBlockerat.ogiltigaFalt` i stället för att låta valideringsloopens `Error` nå
   anroparen okontrollerat.
3. **`beraknaArsprodukt` får tre grenar, inte två, så besparingsflödet för vanliga
   kontraktstariffer bevaras.** v10:s enda `annars`-gren gjorde att VARJE besparingsanrop
   (inklusive Sandviken och de 44 framtida kontraktstarifferna) föll igenom till samma enkla
   `beraknaArskostnadMedKontrakt`-anrop som Stockholms `aktuell_arskostnad`-väg, och returnerade
   alltid `{typ:'aktuell_arskostnad'}` — v10:s egen `{typ:'besparing'}`-gren konstruerades
   aldrig. §6a.4 delar upp dispatchen i tre uttryckliga grenar och låter besparingsgrenen bära
   HELA det befintliga `Besparingsvarde`-kontraktet.
4. **Stockholms aktuell-årskostnad-väg blir end-to-end nåbar, med en helt egen resultattyp
   i stället för en omöjlig retrofit av `KalkylatorResult`.** v10 lade kapacitetsinlägget bara
   i `beraknaBesparingsvardeKontrakt`, så den nya vägen fick aldrig en `IndataPost` för
   Stockholms annual-skopade effektkrav. Verifierat att `KalkylatorResult` har OBLIGATORISKA
   numeriska besparings-/paybackfält — "lämna dem `null`" kompilerar inte. §6a.4 låter EN delad
   indatabyggare (som alltid lägger in kapaciteten, oavsett gren) betjäna alla tre
   dispatch-grenarna, och inför en HELT SEPARAT, diskriminerad resultattyp på
   `calcResult`/sidnivå (inte en ändring av `KalkylatorResult`) för `aktuell_arskostnad`, med
   en egen renderingsgren i `KalkylatorPage.tsx` och ett deterministiskt `onskadTyp`-fält i
   `KalkylatorInputs`.
5. **Adapterpreflighten får ETT anropskontrakt för `bygg_ts()`, inte en låtsad tom kontext.**
   v10 sa att `bygg_ts()` skulle köra preflighten med tom katalog/adapterregister "när inga
   adapterposter är relevanta" — men Stockholms `ersatter_katalograd`-markör byggs OVILLKORAT
   in i leverantörsfilens policy, så ett tomt adapterregister skulle få reverse-loopen att se
   markören men ett tomt `adapterade_mal` och kasta. §6a.4 tar bort undantaget: `bygg_ts()`
   får ALLTID det verkliga, injicerade produktionsregistret. Reverse-nyckeln byts från
   `set(entry.tariff_id)` till hela `(provider_id, tariff_id, ersatter_katalograd)`-relationen,
   så två leverantörer med samma `tariff_id` inte kan dela en adaptermarkör.
6. **P2 rättat:** etikett/hjälptext har EN källa (policyregistret, transporterad genom
   `_policy_till_json()`/`policyFranGenererad()` — INTE dubblerad med `indatafalt_for()`).
   Batch 0 säger nu uttryckligen TRE värdetyper (`enum_val` är ett UI-LÄGE för ett numeriskt
   `number`-krav, inte en fjärde typ). `beraknaArsprodukt(args)` har EN signatur
   (`onskadTyp` inne i `args`), och `kontrollera_adapterpreflight` ägs av `generera.py` i
   ALLA batchar (batch 0:s referens till `katalog.py` var fel).
7. **Oförändrat från v10 (redan korrekt och återverifierat):** Umeås tvåpassgrind och
   registerinjektion (§6a.3), 78 katalog-ID:n, 14 variant-ID:n (10/4 efter Jönköping),
   42-raders bandtabell, Borlänge/C4/Falus gränsfallsbugg, Lidköpings kända metodavvikelse,
   Kraftringens `flodeskorrigering_variant`-lösning, Jönköpings `tillatna_varden`-allow-list,
   `IndataVarde`/`Varde`-uppdelningen, dispositionerna 7/55/30/92 — inga nya produktbeslut
   från Robert krävs för dessa tekniska rättningar, per granskningens egen instruktion
   (punkt 8).

## Frusen kontrollmängd (proveniens)

| Källa | Version/commit | Antal produkter i denna inventering |
|---|---|---|
| `Fjarrvarmetariffer/optimate-fjarrvarme-2026.json` | `schema_version 0.1.3`, `skills`-repo commit `7ba9ec1b6245a72a4720f11b11beec6692af6196` (sha256 `a35fc95b741c6af9a3d1462dbd3e23c12577e2f1f1b75bd05b6ab6f484b52bcd`) | 78 katalograder (53 leverantörer) |
| `enkey-agents/skills/ellen/leverantor-stockholm-exergi.md` | fakturavaliderad t.o.m. juli 2026, Brf Åkermannen 33 (`monthly_invoice`-kontraktet, granskning `2026-09-06-003`); leverantörsfilens angivna fakturaantal är ännu inte synkat mot arkivinventeringen — se korrigering nedan | Samma produkt som katalogens `stockholm-exergi-stockholm-exergi-normal-2026` — räknas EN gång, se §4 |
| `enkey-agents/skills/ellen/leverantor-riksgenomsnitt.md` | Nils Holgersson-rapporten 2025 | 1 syntetisk schablon, egen tabell §9 — inte ett tariffprodukt |

**Korrigering av fakturaantal (granskning
[2026-09-09-009](../conversations/reviews/2026/09/2026-09-09-inventering-akermannen-fakturaarkiv.md)):**
den tidigare uppgiften "18 fakturor" (för perioden januari 2025–juli 2026) är inte korrekt
för det nu kompletta arkivet. Arkivet innehåller 22 PDF-filer men endast **20 unika
fakturaperioder**, en per kalendermånad januari 2025–augusti 2026 — mars och april 2026 finns
i två kopior vardera (identisk normaliserad text, olika bytehash, ska dedupliceras via period
och innehåll, inte enbart bytehash). Leverantörsfilens egna verifieringsmetadata ("18
fakturor", verifierat t.o.m. juli 2026) ändras INTE i denna dokumentationsrunda — det är en
produktfil i `enkey-agents` och V16 är dokumentation-only. Korrigeringen till "Verifierad mot
20 unika månadsfakturor/fakturaperioder januari 2025–augusti 2026 (22 PDF-filer inklusive två
dubblettkopior)" sker först när en separat arkivfixtur implementeras och testerna passerar.

**Nytt godkänt out-of-sample-kontrollfall (granskning
[2026-09-09-008](../conversations/reviews/2026/09/2026-09-09-verifiering-akermannen-augusti-2026.md)):**
Åkermannens augustifaktura 2026 verifierades separat mot både Python- och
TypeScript-motorernas direkta månadsfunktion och `monthly_invoice`-kontraktsvägen: motorns
`18 562,440103 kr` inkl. moms mot fakturans `18 562,43 kr` (differens ~1 öre,
fakturaavrundning). Ingen tariffstatus eller 7/57/28-räkning ändras av detta. Den frysta
baslinjefixturen `akermannen-baslinje.json` (maj 2025–april 2026) förblir oförändrad och ska
inte utökas eller återanvändas för augustifallet.

Bindande råd för en framtida, separat arkivfixtur (INTE byggd i V16, per samma två
granskningar): skilj fakturans huvudperiod, avläst (`A`)/preliminär (`P`)-status, faktisk
förbrukningsperiod per energirad, återföring av tidigare preliminärdebitering samt
fakturabelopp vs. kalendermånadens tariffkostnad. Maj–juli 2026 utgör en avräkningskedja
(majfakturan delvis preliminär, junifakturan preliminär, julifakturan återför 17,362 MWh och
redovisar avlästa maj/juni/juli, sammanlagt 33,534 MWh över de tre månaderna). Ett fristående
julitest får bara använda **7,190 MWh** som fysisk julikonsumtion — inte julifakturans rad
"Periodens användning (A) 21,823 MWh", som är summan av tre nytillkomna avlästa delperioder
och skulle skapa ett felaktigt kontrollfall om den användes som julis kalendermånadsvärde.
Preliminär fakturaenergi ska aldrig märkas avläst eller `confirmed_mwh`.

**Explicit utanför denna frusna version:** `Fjarrvarmetariffer/optimate-fjarrvarme-2027.json`
(prisår 2027, `skills`-repo commit `62181a1`, endast 2 av 53 medlemmar ifyllda hittills).
Nästa prisårs katalog är förvaltning av den färdiga produkten, inte en del av v1:s
slutkriterium — se [PROJECT_CHARTER §4](../PROJECT_CHARTER.md).

## 1. Metod och källhierarki

Denna inventering bygger på fyra redan granskade underlag i stigande detaljnivå:

1. [`verifieringslista-fjarrvarmebolag.md`](verifieringslista-fjarrvarmebolag.md) — Codex
   källgranskning av samtliga 78 katalograder mot leverantörernas 2026-underlag
   (2026-09-04). Ger käll-status per rad, och den exakta frågetexten för varje
   `blocked_external_info`-post (§4).
2. [`teknisk-kartlaggning-28-tariffer.md`](teknisk-kartlaggning-28-tariffer.md) v4 —
   Claudes tekniska analys av de 28 rader som hade fullständigt källunderlag även för
   månadsmodell, godkänd av Codex (`2026-09-04-006`). Auktoritativ där den och
   verifieringslistan motsäger varandra (Sundsvall Matfors, se §4).
3. `enkey-agents/tools/tariffer/justeringar.py` (`JUSTERINGSTYPER`, `okand_justering`)
   och `katalog.py` (`grind()`) — läst DIREKT ur koden för denna v2, inte antaget. Detta är
   den faktiska godkännandelistan: en katalograd vars `adjustments`-lista innehåller en typ
   som inte står i `JUSTERINGSTYPER` blockeras av `grind()` och kan inte aktiveras utan ny
   motorkod, oavsett om formeln i övrigt är helt källverifierad. v1 underskattade detta
   systematiskt (granskning `2026-09-08-001`, P1).
4. `enkey-agents/tools/tariffer/policyregister.py` — den faktiska kontraktsstatusen.

**Disposition per produkt** följer PROJECT_CHARTER §4:

- `implemented_source_verified_annual` — valbar i kalkylatorn i dag, årsverifierad.
- `ready_to_implement` — samtliga prisdelar och regler är källverifierade; återstående
  arbete är internt (katalogmappning, motorstöd för en känd men ej implementerad
  justeringstyp/kapacitetsform, eller produktintegration) — inget nytt leverantörsbesked
  krävs. Motorstatusen anger EXPLICIT om ny motorkod krävs (se §1 punkt 3 ovan).
- `blocked_external_info` — minst en materiell uppgift saknas, är tvetydig eller motsägs
  av källorna; kräver ett leverantörssvar eller ett nytt beslut innan implementation.
- `not_applicable` — inte ett tariffprodukt att implementera (schablonmekanism); används
  ALDRIG som uppskjutningsstatus för en känd, verklig produktvariant (se §5).

**Leverantörsvärde-mönstret (Sandviken-precedent):** när en tariffs debiterbara effekt/band
inte kan beräknas automatiskt av en fullständigt publicerad formel, men leverantören ändå
kan uppge/fakturera värdet, klassas tariffen ändå `ready_to_implement` — med det värdet som
obligatorisk, synlig användarindata, inte som en extern blockering. Codex har accepterat
mönstret i princip (granskning `2026-09-08-001`, svar på öppen fråga 3) men kräver en
tariffvis kontroll av VARJE kostnadspåverkande fält — inte bara kapacitetsdelen. §4 nedan
härleder fälten från samtliga prisdelar (kapacitet OCH `adjustments`), inte bara kapacitet.

## 2. Inmatningslägen — generell regel

Per [PROJECT_CHARTER §2](../PROJECT_CHARTER.md): ett inmatningsläge utan entydig,
verifierad modell blockeras, det gissas aldrig.

- **De sex legacy-tarifferna samt Riksgenomsnittet:** mwh, kr och schablon fungerar redan
  (ingen kontraktsgated obligatorisk indata).
- **`sundsvall-energi-indal-liden-och-lucksta-2026` (§4.1, batch 2):** samma som ovan — mwh,
  kr OCH schablon, eftersom den aktiveras via den befintliga `EJ_TILLAMPLIG_KAPACITETSFORM`-
  legacymekanismen och aldrig blir kontraktsgated (rättat i v4, granskning 2026-09-08-003,
  P2 — v3 tillämpade nästa punkts regel på den av misstag).
- **Sandviken och varje ÖVRIG `ready_to_implement`-tariff nedan (samtliga som blir
  kontraktsgated via `POLICYREGISTER`, inklusive Stockholm Exergis årsprodukt):** mwh-läge
  kräver den obligatoriska indatan; kr och schablon blockeras tills en egen, verifierad
  invers/schablonmodell byggs och godkänns separat — detta gäller ÄVEN under
  implementationen av respektive batch, inte bara efter. Ett nytt läge öppnas aldrig som ett
  beslut som "avgörs vid implementation".

## 3. Redan implementerade (7 produkter)


#### `goteborg-energi-goteborg-2026`
- **Leverantör / nät / kundkategori:** Göteborg Energi — Göteborg — näring/brf
- **Prisår/giltighet:** 2026, legacy-tariff sedan uppgift 7 (2026-09-03)
- **Primärkälla:** `goteborg-web` (https://www.goteborgenergi.se/foretag/fjarrvarme/fjarrvarmepriser)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** godkänd | **Katalogstatus:** legacy, `contract_required` ej satt | **Motorstatus:** klar (`temperature_difference`, redan i JUSTERINGSTYPER) | **Kontraktsstatus:** ej kontraktsgated (legacy) | **Teststatus:** i generella regressions-/godkanda-sviterna | **UI-status:** valbar
- **Årsreproducerbar:** Ja, redan i produktion
- **Obligatorisk indata:** Returtemperaturavvikelse har ett neutralt default (0 °C); ingen indata är formellt obligatorisk för legacy-vägen
- **Inmatningslägen:** mwh, kr, schablon — alla tre
- **Disposition:** `implemented_source_verified_annual`

#### `gotlands-energi-gotland-taxa-17-under-50-mwh-ar-2026`
- **Leverantör / nät / kundkategori:** Gotlands Energi — Taxa 17, under 50 MWh/år — näring/brf
- **Prisår/giltighet:** 2026, legacy | **Källstatus:** godkänd | **Katalogstatus:** legacy | **Motorstatus:** klar (ingen kapacitetsdel, `capacity: null`) | **Kontraktsstatus:** ej kontraktsgated | **Teststatus:** i generella sviterna | **UI-status:** valbar
- **Primärkälla:** `10_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Geab-Prisdialogen-2025.pdf); `web-review-geab-final` (https://geab.se/wp-content/uploads/2026/01/Prislista-fjarrvarme-2026.pdf); `web-review-geab-model` (https://geab.se/fjarrvarme/priser/)
- **Giltighet:** valid_from=2026-01-01, valid_to=unknown (katalogens `valid_to` är null)
- **Årsreproducerbar:** Ja | **Obligatorisk indata:** ingen för mwh-läget. `foregaende_ars_mwh` krävs bara för kr-läget — inte som en `volume_discount`-justeringspost på DENNA katalograd (den har `adjustments: []`), utan för att välja rätt TARIFF (denna Taxa 17 vs. `gotlands-energi-gotland-taxa-21-over-50-mwh-ar-2026`) baserat på föregående kalenderårs förbrukning, i den befintliga volymrabatt-bandvalslogiken i `fjarrvarme.ts`/`faktura.py` (granskning 2026-09-08-002, P2 — rättad beskrivning av en redan korrekt implementerad mekanism)
- **Inmatningslägen:** mwh, kr, schablon
- **Disposition:** `implemented_source_verified_annual`

#### `gotlands-energi-gotland-taxa-21-over-50-mwh-ar-2026`
- **Leverantör / nät / kundkategori:** Gotlands Energi — Taxa 21, över 50 MWh/år — näring/brf
- **Prisår/giltighet:** 2026, legacy | **Källstatus:** godkänd | **Katalogstatus:** legacy | **Motorstatus:** klar (`cooling_deadband`, `volume_discount`, båda i JUSTERINGSTYPER) | **Kontraktsstatus:** ej kontraktsgated | **Teststatus:** i generella sviterna | **UI-status:** valbar
- **Primärkälla:** `10_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Geab-Prisdialogen-2025.pdf); `web-review-geab-final` (https://geab.se/wp-content/uploads/2026/01/Prislista-fjarrvarme-2026.pdf); `web-review-geab-model` (https://geab.se/fjarrvarme/priser/)
- **Giltighet:** valid_from=2026-01-01, valid_to=unknown (katalogens `valid_to` är null)
- **Årsreproducerbar:** Ja | **Obligatorisk indata:** föregående kalenderårs energi (volymrabatt); avkylning har neutralt default
- **Inmatningslägen:** mwh, kr, schablon
- **Disposition:** `implemented_source_verified_annual`

#### `halmstads-energi-och-miljo-halmstad-2026`
- **Leverantör / nät / kundkategori:** Halmstads Energi och Miljö — Halmstad — näring/brf
- **Prisår/giltighet:** 2026, legacy | **Källstatus:** godkänd | **Katalogstatus:** legacy | **Motorstatus:** klar (inga justeringar) | **Kontraktsstatus:** ej kontraktsgated | **Teststatus:** i generella sviterna | **UI-status:** valbar
- **Primärkälla:** `12_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-HEM_2025.pdf); `web-review-hem-prices` (https://www.hem.se/foretag/fjarrvarme/avtal-och-priser); `web-review-hem-terms` (https://www.hem.se/globalassets/dokument/villkor-gallande-normalprislista_naringsidkare.pdf)
- **Giltighet:** valid_from=2026-01-01, valid_to=unknown (katalogens `valid_to` är null)
- **Årsreproducerbar:** Ja | **Obligatorisk indata:** ingen
- **Inmatningslägen:** mwh, kr, schablon
- **Disposition:** `implemented_source_verified_annual`

#### `molndal-energi-molndal-kallered-och-lindome-2026`
- **Leverantör / nät / kundkategori:** Mölndal Energi — Mölndal, Kållered och Lindome — näring/brf
- **Prisår/giltighet:** 2026, legacy | **Källstatus:** godkänd | **Katalogstatus:** legacy | **Motorstatus:** klar (`volume`, kWh/dygn-kapacitetsform, redan stödd) | **Kontraktsstatus:** ej kontraktsgated | **Teststatus:** i generella sviterna | **UI-status:** valbar
- **Primärkälla:** `24_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Molndal-Energi-2025.pdf); `web-review-molndal-final` (https://www.molndalenergi.se/hubfs/MolndalEnergi_Foretag_Prislista_Fjarrvarme_260101.pdf?hsLang=sv-se)
- **Giltighet:** valid_from=2026-01-01, valid_to=unknown (katalogens `valid_to` är null)
- **Årsreproducerbar:** Ja | **Obligatorisk indata:** flöde och högsta dygnsenergi har dynamiska gissningsdefault (`ar_gissning: true`) — kan anges för exakthet men är inte formellt obligatoriska
- **Inmatningslägen:** mwh, kr, schablon
- **Disposition:** `implemented_source_verified_annual`

#### `norrenergi-norrenergi-2026`
- **Leverantör / nät / kundkategori:** Norrenergi — Norrenergi — näring/brf
- **Prisår/giltighet:** 2026, legacy | **Källstatus:** godkänd | **Katalogstatus:** legacy | **Motorstatus:** klar (`low_utilization`, `incremental_return_temperature`, båda i JUSTERINGSTYPER) | **Kontraktsstatus:** ej kontraktsgated | **Teststatus:** i generella sviterna | **UI-status:** valbar
- **Primärkälla:** `28_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Norrenergi-2025.pdf); `web-review-norrenergi-final` (https://www.norrenergi.se/media/livhhhgq/normalprislista-fj%C3%A4rrv%C3%A4rme-2026.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Årsreproducerbar:** Ja | **Obligatorisk indata:** normalårskorrigerad energi och returtemperatur har dynamiska default (egen uppskattad förbrukning respektive 30 °C-tröskeln)
- **Inmatningslägen:** mwh, kr, schablon
- **Disposition:** `implemented_source_verified_annual`

#### `sandviken-energi-sandviken-normal-2026`
- **Leverantör / nät / kundkategori:** Sandviken Energi — Helleverans — näring/brf
- **Prisår/giltighet:** 2026 | **Källstatus:** godkänd, granskning `2026-09-07-003` | **Katalogstatus:** `contract_required: true` | **Motorstatus:** klar (ingen kapacitetsdel utöver effekt) | **Kontraktsstatus:** `POLICYREGISTER`, `annual_forward`, `minvarde=3`/`heltal=True` | **Teststatus:** `test_sandviken_kontrakt.py`, `besparingsvardeSandviken.test.ts` | **UI-status:** valbar, pushad `origin/main`
- **Primärkälla:** `sandviken-2026-priser` (https://sandvikenenergi.se/fjarrvarme/priserforfjarrvarme.7681.html); `sandviken-2026-effektmodell` (https://sandvikenenergi.se/fjarrvarme/priserforfjarrvarme/saberaknasdineffekt.7682.html)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Årsreproducerbar:** Ja, i produktion | **Obligatorisk indata:** debiterbar effekt (kW, fakturan), heltal ≥3 kW
- **Inmatningslägen:** mwh (obligatorisk effekt); kr och schablon blockerade (`unsupported_input_mode`/`missing_energy`/`invalid_energy`)
- **Disposition:** `implemented_source_verified_annual`

## 4. Per-produktmatris — samtliga 71 icke-implementerade tariffprodukter

En normaliserad post per unik tariff-ID (inte grupptext). 45 är `ready_to_implement` (§4.1),
26 är `blocked_external_info` (§4.2) — Eskilstuna flyttad från redo till blockerad i v3
(granskning 2026-09-08-002, P1: nätreferensen är inte verifierad, `ready` får inte vara
villkorat av en framtida extern verifiering). Fälten följer exakt vad överlämning `2026-09-08-001`
begärde: leverantör, nät, produkt, kundkategori, prisår/giltighet+källa, käll-/katalog-/
motor-/kontrakts-/test-/UI-status separat, årsreproducerbarhet, obligatorisk indata med
fyndplats, inmatningsläge, tariffamilj/adapter, kvarstående arbete, disposition.

### 4.1 Redo att implementera (45 produkter)


#### `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026`
- **Leverantör / nät / kundkategori:** Borås Energi och Miljö — Borås, Sjömarken, Sandared, Dalsjöfors, Fristad — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `00_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Boras.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE — ny kapacitetsform `heterogeneous_bands` + optional_environmental_addon
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens prisgrupp (1–6) OCH `Wn` eller `Q` beroende på grupp (fakturan). Miljötillägget "Bra Miljöval" (31 SEK/MWh) är ett SYNLIGT KUNDVAL, inte automatiskt — måste bli ett explicit UI-alternativ (checkbox/produktval), annars måste det uttryckligen avgränsas bort tills UI-arbetet görs.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Borås — ny kapacitetsform + valfritt tillägg
- **Kvarstående arbete:** `heterogeneous_bands` (ny kapacitetsform) OCH `optional_environmental_addon` (ny justeringstyp, dessutom kräver kundvalsUI, inte bara ett fält) — v1 nämnde bara kapacitetsformen.
- **Disposition:** `ready_to_implement`


#### `borlange-energi-borlange-2026`
- **Leverantör / nät / kundkategori:** Borlänge Energi — Borlänge — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `borlange-web` (https://www.borlange-energi.se/kontakta-oss/priser/fjarrvarmepris-for-naringsidkare)
- **Giltighet:** valid_from=2026-01-01, valid_to=2026-12-31
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effektgrupp (fakturan/avtalet) — automatisk gruppindelning vid gränsen (501 kW) BLOCKERAS. DESSUTOM prissatt flöde i m³ hela året (fakturan/avtalet, `volume`-justering) — inte bara effektgruppen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (som Borås effektgrupp)
- **Kvarstående arbete:** Ingen ny motorkod — `volume` gäller alla tolv månader (inget säsongsarbete krävs). `Tariffpolicy` med leverantörsvärde-krav OCH ett nytt obligatoriskt flödesfält.
- **Disposition:** `ready_to_implement`


#### `c4-energi-kristianstad-2026`
- **Leverantör / nät / kundkategori:** C4 Energi — Kristianstad — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `02_0` (https://www.prisdialogen.se/wp-content/uploads/2025/08/Prisandringsmodell-2026-C4-Energi.pdf); `web-review-c4-current` (https://c4energi.se/foretag/varmekyla/priservillkor.793.html)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effektgrupp (fakturan/avtalet) — automatisk gruppindelning vid gränsen (501 kW Borlänge, 500 kW C4) BLOCKERAS.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (som Borås effektgrupp)
- **Kvarstående arbete (utökat i v5, granskning 2026-09-08-004, P1):** Ingen ny motorkod. `Tariffpolicy` med leverantörsvärde-krav, samma mönster som redan godkända leverantörsvärde-tariffer. KATALOGRÄTTELSE av `issues`: ersätt nuvarande text med den redan godkända issue-typen "Metod för debiterbar effekt/kapacitet är inte fullständigt mappad; använd leverantörens fakturavärde för bandval vid exakt 500 kW." Informationsförfrågan R05 (medlem `c4-energi`) TAS BORT — bolaget har bara denna enda tariff.
- **Disposition:** `ready_to_implement`


#### `e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026`
- **Leverantör / nät / kundkategori:** E.ON - Järfälla — Järfälla och Upplands-Bro – Bostäder — bostäder
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `03_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--bro-balsta-jarfalla-kungsangen-2026.pdf) — rättad till den aktuella officiella 2026-källan, granskning 2026-09-08-003 (v3 citerade av misstag 2025-URL:en)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04; teknisk-kartläggning v4)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (supply_temperature_adjusted_flow)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW), medelframledningstemp `Tf` (°C) OCH flöde (`flode_m3`, m³) — alla tre fakturan/avtalet. Endast fullvärmekunder i denna disposition; 36-månadersmetoden för bas-/delvärmekunder är EN EGEN VARIANT, se särfallstabellen.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** E.ON/Navirum — rullande högutväxling, ny motortyp
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1, gäller samtliga åtta E.ON/Navirum-rader): `fixed: null` och `rate_period: null` — verifieringslistan anger att ingen separat fast avgift finns och att effektpriset är per kW och MÅNAD; sätt `fixed: 0`, `rate_period: "month"`. Utan denna rättelse riskerar en framtida feltolkning en 12× fel årskostnad (motorn ×12:ar bara när rate_period="month"). Golden-test: ett handräknat helår bekräftar korrekt ×12-periodisering och att `fixed=0` inte tillför en dold stående kostnad. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Effektprisets tidsenhet måste bekräftas. Flödespris korrigeras för framledningstemperatur; full formel saknas." är fullt löst av kombinationen `rate_period`-rättelsen ovan OCH den nya `supply_temperature_adjusted_flow`-motorn (batch 3) — TA BORT issue-raden. E.ON Järfälla (bostäder).
- **Disposition:** `ready_to_implement`


#### `e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter-2026`
- **Leverantör / nät / kundkategori:** E.ON - Järfälla — Järfälla och Upplands-Bro – Övriga fastigheter — övriga fastigheter
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `03_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--bro-balsta-jarfalla-kungsangen-2026.pdf) — rättad till den aktuella officiella 2026-källan, granskning 2026-09-08-003 (v3 citerade av misstag 2025-URL:en)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04; teknisk-kartläggning v4)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (supply_temperature_adjusted_flow)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW), medelframledningstemp `Tf` (°C) OCH flöde (`flode_m3`, m³) — alla tre fakturan/avtalet. Endast fullvärmekunder i denna disposition; 36-månadersmetoden för bas-/delvärmekunder är EN EGEN VARIANT, se särfallstabellen.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** E.ON/Navirum — rullande högutväxling, ny motortyp
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1, gäller samtliga åtta E.ON/Navirum-rader): `fixed: null` och `rate_period: null` — verifieringslistan anger att ingen separat fast avgift finns och att effektpriset är per kW och MÅNAD; sätt `fixed: 0`, `rate_period: "month"`. Utan denna rättelse riskerar en framtida feltolkning en 12× fel årskostnad (motorn ×12:ar bara när rate_period="month"). Golden-test: ett handräknat helår bekräftar korrekt ×12-periodisering och att `fixed=0` inte tillför en dold stående kostnad. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Effektprisets tidsenhet måste bekräftas. Flödespris korrigeras för framledningstemperatur; full formel saknas." är fullt löst av kombinationen `rate_period`-rättelsen ovan OCH den nya `supply_temperature_adjusted_flow`-motorn (batch 3) — TA BORT issue-raden. E.ON Järfälla (övriga fastigheter).
- **Disposition:** `ready_to_implement`


#### `e-on-malmo-malmo-och-burlov-bostader-2026`
- **Leverantör / nät / kundkategori:** E.ON - Malmö — Malmö och Burlöv – Bostäder — bostäder
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `04_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser-malmo-2026.pdf) — rättad till den aktuella officiella 2026-källan, granskning 2026-09-08-003 (v3 citerade av misstag 2025-URL:en)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04; teknisk-kartläggning v4)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (supply_temperature_adjusted_flow)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW), medelframledningstemp `Tf` (°C) OCH flöde (`flode_m3`, m³) — alla tre fakturan/avtalet. Endast fullvärmekunder i denna disposition; 36-månadersmetoden för bas-/delvärmekunder är EN EGEN VARIANT, se särfallstabellen.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** E.ON/Navirum — rullande högutväxling, ny motortyp
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1, gäller samtliga åtta E.ON/Navirum-rader): `fixed: null` och `rate_period: null` — verifieringslistan anger att ingen separat fast avgift finns och att effektpriset är per kW och MÅNAD; sätt `fixed: 0`, `rate_period: "month"`. Utan denna rättelse riskerar en framtida feltolkning en 12× fel årskostnad (motorn ×12:ar bara när rate_period="month"). Golden-test: ett handräknat helår bekräftar korrekt ×12-periodisering och att `fixed=0` inte tillför en dold stående kostnad. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Effektprisets tidsenhet måste bekräftas. Flödespris korrigeras för framledningstemperatur; full formel saknas." är fullt löst av kombinationen `rate_period`-rättelsen ovan OCH den nya `supply_temperature_adjusted_flow`-motorn (batch 3) — TA BORT issue-raden. E.ON Malmö (bostäder, −15→−8 °C katalogrättelse).
- **Disposition:** `ready_to_implement`


#### `e-on-malmo-malmo-och-burlov-ovriga-fastigheter-2026`
- **Leverantör / nät / kundkategori:** E.ON - Malmö — Malmö och Burlöv – Övriga fastigheter — övriga fastigheter
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `04_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser-malmo-2026.pdf) — rättad till den aktuella officiella 2026-källan, granskning 2026-09-08-003 (v3 citerade av misstag 2025-URL:en)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04; teknisk-kartläggning v4)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (supply_temperature_adjusted_flow)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW), medelframledningstemp `Tf` (°C) OCH flöde (`flode_m3`, m³) — alla tre fakturan/avtalet. Endast fullvärmekunder i denna disposition; 36-månadersmetoden för bas-/delvärmekunder är EN EGEN VARIANT, se särfallstabellen.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** E.ON/Navirum — rullande högutväxling, ny motortyp
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1, gäller samtliga åtta E.ON/Navirum-rader): `fixed: null` och `rate_period: null` — verifieringslistan anger att ingen separat fast avgift finns och att effektpriset är per kW och MÅNAD; sätt `fixed: 0`, `rate_period: "month"`. Utan denna rättelse riskerar en framtida feltolkning en 12× fel årskostnad (motorn ×12:ar bara när rate_period="month"). Golden-test: ett handräknat helår bekräftar korrekt ×12-periodisering och att `fixed=0` inte tillför en dold stående kostnad. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Effektprisets tidsenhet måste bekräftas. Flödespris korrigeras för framledningstemperatur; full formel saknas." är fullt löst av kombinationen `rate_period`-rättelsen ovan OCH den nya `supply_temperature_adjusted_flow`-motorn (batch 3) — TA BORT issue-raden. E.ON Malmö (övriga fastigheter, −15→−8 °C katalogrättelse).
- **Disposition:** `ready_to_implement`


#### `falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo-2026`
- **Leverantör / nät / kundkategori:** Falu Energi & Vatten — Bjursås, Grycksbo, Sundborn, Svärdsjö — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `06_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Falu-Energi-och-Vatten.pdf); `web-review-falu-final` (https://fev.se/varme--kyla/fjarrvarme/avtal-och-priser-foretag.html)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Bekräftat effektband-ID (`supplier_confirmed_band_id`, §6a.2 — en av de 42 raderna). Automatisk bandval BLOCKERAS strukturellt via bandkontraktet. DESSUTOM `KravPost.maxvarde=500` (§6a.1 — publicerad prislista täcker bara till och med 500 kW, mekaniskt fail-closed över gränsen) OCH prissatt flöde i m³ hela året (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående) + bandkontraktet (§6a.2) + `KravPost.maxvarde` (§6a.1)
- **Kvarstående arbete (utökat i v5, granskning 2026-09-08-004, P1 och P2/fail-closed-krav 6):** Ingen ny motorkod — `volume` gäller alla tolv månader. Bara ett nytt synligt, obligatoriskt flödesfält i `Tariffpolicy`/UI. KATALOGRÄTTELSE av `issues`: ersätt nuvarande text med "Metod för debiterbar effekt/kapacitet är inte fullständigt mappad ovanför 500 kW; publicerad prislista täcker endast till och med 500 kW — begränsa beräkningen till detta intervall, hantera högre effekt som specialavtal (fail-closed, ingen automatisk extrapolering över gränsen)." Informationsförfrågan R15 (medlem `falu-energi-vatten`, avgränsad till just ytterorterna >500 kW) TAS BORT ur `remaining_information_requests` — dess fråga täcks nu av den normaliserade issue-texten ovan. Falu-Falun (`falu-energi-vatten-falun-2026`) delar medlem men har ingen egen öppen fråga och berörs inte.
- **Disposition:** `ready_to_implement`


#### `falu-energi-vatten-falun-2026`
- **Leverantör / nät / kundkategori:** Falu Energi & Vatten — Falun — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `06_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Falu-Energi-och-Vatten.pdf); `web-review-falu-final` (https://fev.se/varme--kyla/fjarrvarme/avtal-och-priser-foretag.html)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet. DESSUTOM prissatt flöde i m³ hela året (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod — `volume` gäller alla tolv månader för denna tariff (inget säsongs-/`months`-arbete krävs, till skillnad från §4.1-tarifferna med säsongsflöde). Bara ett nytt synligt, obligatoriskt flödesfält i `Tariffpolicy`/UI.
- **Disposition:** `ready_to_implement`


#### `finspangs-tekniska-verk-finspang-2026`
- **Leverantör / nät / kundkategori:** Finspångs Tekniska Verk — Finspång — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `07_1` (https://www.prisdialogen.se/wp-content/uploads/2025/10/Normalprislista-Finspang-2025.pdf); `web-review-finspang-final` (https://d2sabnli7hsonp.cloudfront.net/finspangs-tekniska/image/upload/fl_attachment/v1762179931/zvwzbdzlxxtsl15nsxrd.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE — ny kapacitetsform `piecewise_polynomial` + conditional_flow
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens P-värde (kapacitetsformelns bas), returtemperatur varje månad (°C, fakturan — avgör om `conditional_flow`s villkor >55 °C utlöses) OCH, när villkoret utlöses, MÅNADENS flöde i m³ (fakturan — multipliceras med 20 kr/m³). Spetsvärmetillägget (20 %) är en EGEN VARIANT, se särfallstabellen.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Finspång — ny kapacitetsform + ny motortyp
- **Kvarstående arbete:** `piecewise_polynomial` (ny kapacitetsform) OCH `conditional_flow` (ny justeringstyp, villkorad på månatlig returtemperatur) — TVÅ separata nya motordelar, större arbete än enbart kapacitetsformen som v1 angav.
- **Disposition:** `ready_to_implement`


#### `habo-energi-habo-2026`
- **Leverantör / nät / kundkategori:** Habo Energi — Habo — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `11_0` (https://www.prisdialogen.se/wp-content/uploads/2023/10/Prisandringsmodell-2025-Habo-Energi.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet. DESSUTOM prissatt flöde i m³ hela året (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod — `volume` gäller alla tolv månader för denna tariff (inget säsongs-/`months`-arbete krävs, till skillnad från §4.1-tarifferna med säsongsflöde). Bara ett nytt synligt, obligatoriskt flödesfält i `Tariffpolicy`/UI.
- **Disposition:** `ready_to_implement`


#### `jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge-2026`
- **Leverantör / nät / kundkategori:** Jämtkraft — Åre, Järpen, Mörsil, Duved, Kall, Hallen, Krokom, Nälden, Föllinge — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `15_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Jamtkraft.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (flow_difference)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW) OCH flöde okt–apr (m³, fakturan). Formeln `3×(flöde_m3 − 19×energi_MWh)` är känd (katalog), referensvärdet 19 m³/MWh är redan ett statiskt katalogvärde (Åre m.fl.).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Jämtkraft — ny motortyp `flow_difference`
- **Kvarstående arbete:** `flow_difference` finns INTE i JUSTERINGSTYPER — kräver ny motorkod i justeringar.py (speglad inline i fjarrvarme.ts) innan aktivering, trots att formeln och referensvärdet redan är kända och statiska.
- **Disposition:** `ready_to_implement`


#### `jamtkraft-brunflo-och-opevagen-2026`
- **Leverantör / nät / kundkategori:** Jämtkraft — Brunflo och Opevägen — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `15_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Jamtkraft.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (flow_difference)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW) OCH flöde okt–apr (m³, fakturan). Formeln `3×(flöde_m3 − 19×energi_MWh)` är känd (katalog), referensvärdet 19 m³/MWh är redan ett statiskt katalogvärde (Brunflo/Opevägen).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Jämtkraft — ny motortyp `flow_difference`
- **Kvarstående arbete:** `flow_difference` finns INTE i JUSTERINGSTYPER — kräver ny motorkod i justeringar.py (speglad inline i fjarrvarme.ts) innan aktivering, trots att formeln och referensvärdet redan är kända och statiska.
- **Disposition:** `ready_to_implement`


#### `jamtkraft-ostersund-froson-as-2026`
- **Leverantör / nät / kundkategori:** Jämtkraft — Östersund, Frösön, Ås — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `15_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Jamtkraft.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (flow_difference)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW) OCH flöde okt–apr (m³, fakturan). Formeln `3×(flöde_m3 − 19×energi_MWh)` är känd (katalog), referensvärdet 19 m³/MWh är redan ett statiskt katalogvärde (Östersund/Frösön/Ås).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Jämtkraft — ny motortyp `flow_difference`
- **Kvarstående arbete:** `flow_difference` finns INTE i JUSTERINGSTYPER — kräver ny motorkod i justeringar.py (speglad inline i fjarrvarme.ts) innan aktivering, trots att formeln och referensvärdet redan är kända och statiska.
- **Disposition:** `ready_to_implement`


#### `jonkoping-energi-jonkoping-och-granna-2026`
- **Leverantör / nät / kundkategori:** Jönköping Energi — Jönköping och Gränna — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `16_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Jonkoping-Energi-2025-till-2026-Prisandringsmodell.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet. DESSUTOM prissatt flöde i m³ hela året (fakturan/avtalet, `volume`-justering, 3,7 SEK/m³) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1). Den avtalsberoende accessavgiften (0/10/25/50 kr/mån) ingår INTE i denna disposition — se specialvariant i §5.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod — `volume` gäller alla tolv månader (inget säsongsarbete krävs). Bara ett nytt synligt, obligatoriskt flödesfält i `Tariffpolicy`/UI. Accessavgiften byggs INTE i denna delbatch.
- **Disposition:** `ready_to_implement`


#### `karlstads-energi-karlstad-2026`
- **Leverantör / nät / kundkategori:** Karlstads Energi — Karlstad — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `17_1` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Normalprislista-Karlstads-Energi-AB-20260101.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW, fakturan).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Familj 4 — Sandviken-mönstret
- **Kvarstående arbete:** `capacity.rate_period: month` — dela INTE årsavgiften med 12 automatiskt.
- **Disposition:** `ready_to_implement`


#### `kils-energi-kil-2026`
- **Leverantör / nät / kundkategori:** Kils Energi — Kil — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `18_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-for-fjarrvarme-i-Kils-Energi-AB-2025.pdf); `web-review-kil-vat` (https://kilsenergi.kil.se/download/18.1b9e2707199c916c9d91010c/1761112730710/Kils_Energi_normalprislista.pdf); `kil-user-supplied-pricelist` ((url saknas))
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod (redan stödd `selected_band_affine` + ev. säsongsenergi). KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1): samtliga fyra band har `fixed: null` — verifierat besked är att ingen separat fast avgift finns, så `fixed` sätts till `0` på alla fyra. Golden-test: ett handräknat helår med `fixed=0` ger samma årsbelopp som enbart `variable × band`. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "null i fast avgift betyder ej extraherad/separat angiven, inte verifierad noll" är den PRECISA varning `fixed:0`-rättelsen ovan besvarar — TA BORT issue-raden när `fixed:0` sätts, den är inaktuell efter rättelsen, inte en kvarstående öppen fråga.
- **Disposition:** `ready_to_implement`


#### `kraftringen-kraftringen-2026`
- **Leverantör / nät / kundkategori:** Kraftringen — Kraftringen — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `19_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Kraftringens-Prisandringsmodell-2025.pdf); `web-review-kraftringen-model` (https://www.kraftringen.se/brf/varme-och-kylalosningar/fjarrvarme/fjarrvarmepriser/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (supply_temperature_adjusted_flow)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Bekräftat effektband-ID (`supplier_confirmed_band_id`, §6a.2 — en av de 42 raderna), debiterbar effekt (kW), förbrukningsvägd MÅNADSMEDEL-framledningstemperatur `Tf` (°C, fakturan/nätdata — formeln själv använder `Tf` varje månad, inte bara flödet) OCH flöde (m³, fakturan). Formeln `flöde_m3×10,40×max(0,2; 0,2+(Tf−60)×0,02)` känd (katalog) — GOLVBEGRÄNSAD, skild från E.ON/Navirums golvfria formel (§6a.5); Brunnshögs nätdel är en EGEN VARIANT, se särfallstabellen — endast ordinarie nät ingår här.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Kraftringen — samma parametriserade motortyp som E.ON/Navirum, med `flodeskorrigering_variant: "golvbegransad"` som explicit, typad diskriminator (§6a.5) — INTE härledd implicit från leverantörs-ID
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` som en parametriserad motortyp delad med E.ON/Navirum, med Kraftringens regelvariant explicit diskriminerad (§6a.5). Bör byggas i SAMMA batch/commit som dem. Bandkontraktet (§6a.2) tillkommer som ett separat obligatoriskt fält. KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1): `fixed: null` och `rate_period: null` — verifieringslistan anger redan `fixed: 0`, `rate_period: "year"`; sätt båda explicit. Golden-test: ett handräknat helår bekräftar att kapacitetsdelen inte periodiseras om (year, ingen ×12), att `fixed=0` inte tillför en dold stående kostnad, OCH att golvet vid exakt `Tf=60` ger faktorn `0,2` (§6a.5). YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Nätavgränsning, effektprisperiod och flödeskorrektion behöver bekräftas..." är fullt löst av kombinationen `rate_period`-rättelsen ovan OCH den nya `supply_temperature_adjusted_flow`-motorn (batch 3) — TA BORT issue-raden.
- **Disposition:** `ready_to_implement`


#### `lulea-energi-lulea-2026`
- **Leverantör / nät / kundkategori:** Luleå Energi — Luleå — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `21_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Lulea-Energi.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan). DESSUTOM prissatt säsongsflöde i m³, januari–maj samt september–december (9 månader) (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** `volume` gäller ENDAST januari–maj samt september–december (9 månader) för DENNA tariff (katalogens egen `months`-lista, inte ett generellt okt–apr-antagande) — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik (motorn och testerna måste använda postens egen `months`-lista) innan aktivering.
- **Disposition:** `ready_to_implement`


#### `malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026`
- **Leverantör / nät / kundkategori:** Mälarenergi — Västerås och Hallstahammar, 2–4 lägenheter — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `22_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Malarenergi.pdf); `web-review-malar-price` (https://www.malarenergi.se/foretag/varme-kyla-foretag/fjarrvarme-foretag/priser-fjarrvarme/); `web-review-malar-flow` (https://www.malarenergi.se/foretag/varme-kyla-foretag/fjarrvarme-foretag/flodespremie/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Ingen kapacitetsdel. Fast årsavgift (katalog), energi (MWh, kund anger), säsongens verkliga flöde i m³, januari–april samt oktober–december (7 månader, katalogens egen `months`-lista) — fakturans flödesvärde, INTE härlett ur MWh×antagen ΔT.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Mälarenergi, ren energitariff (2–4 lgh)
- **Kvarstående arbete (utökat i v5, granskning 2026-09-08-004, P1):** `volume`-justeringen finns i motorn men appliceras i dag på ett enda årsflöde, inte postens egen `months`-lista (jan–apr + okt–dec, INTE okt–apr). Kräver månadssemantik i faktura.py/fjarrvarme.ts innan aktivering. INFORMATIONSFÖRFRÅGAN R03 (medlem `malarenergi`) SKA DELAS, INTE TAS BORT: dess text ("Vilka nät hör sidans två olika tabeller till? Bekräfta fast avgift 2217/2117 för 25–79 kW samt sommarperiod/flödesvillkor") gäller uttryckligen `malarenergi-vasteras-och-hallstahammar-storre-fastigheter-2026` och `malarenergi-vasteras-och-hallstahammar-gruppanslutna-smahus-2026` (båda `blocked_external_info`) — inte 2–4 lägenheter, som saknar kapacitetsdel helt och därmed ingen effekt-/fast avgifts-tvetydighet att lösa. Omskopa R03 till just de två övriga Mälarenergi-tarifferna. Grindtest: `grind()` på 2–4 lägenheter ska passera med tom `utredda`-mängd, medan de två övriga fortsatt ger `utreds (medlem)`.
- **Disposition:** `ready_to_implement`


#### `mjolby-svartadalen-energi-mjolby-2026`
- **Leverantör / nät / kundkategori:** Mjölby Svartådalen Energi — Mjölby — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `23_0` (https://www.prisdialogen.se/wp-content/uploads/2022/10/Prisandringsmodell-for-MSE-i-Mjolby-2025.pdf); `web-review-mjolby-final` (https://mse.se/foretag/fjarrvarme/priser)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet. DESSUTOM prissatt flöde i m³ hela året (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod — `volume` gäller alla tolv månader för denna tariff (inget säsongs-/`months`-arbete krävs, till skillnad från §4.1-tarifferna med säsongsflöde). Bara ett nytt synligt, obligatoriskt flödesfält i `Tariffpolicy`/UI.
- **Disposition:** `ready_to_implement`


#### `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader-2026`
- **Leverantör / nät / kundkategori:** Navirum Energi - Norrköping och Söderköping — Norrköping och Söderköping – Bostäder — bostäder
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `25_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--norrkoping-soderkoping-2026.pdf) — rättad till den aktuella officiella 2026-källan, granskning 2026-09-08-003 (v3 citerade av misstag 2025-URL:en)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04; teknisk-kartläggning v4)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (supply_temperature_adjusted_flow)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW), medelframledningstemp `Tf` (°C) OCH flöde (`flode_m3`, m³) — alla tre fakturan/avtalet. Endast fullvärmekunder i denna disposition; 36-månadersmetoden för bas-/delvärmekunder är EN EGEN VARIANT, se särfallstabellen.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** E.ON/Navirum — rullande högutväxling, ny motortyp
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1, gäller samtliga åtta E.ON/Navirum-rader): `fixed: null` och `rate_period: null` — verifieringslistan anger att ingen separat fast avgift finns och att effektpriset är per kW och MÅNAD; sätt `fixed: 0`, `rate_period: "month"`. Utan denna rättelse riskerar en framtida feltolkning en 12× fel årskostnad (motorn ×12:ar bara när rate_period="month"). Golden-test: ett handräknat helår bekräftar korrekt ×12-periodisering och att `fixed=0` inte tillför en dold stående kostnad. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Effektprisets tidsenhet måste bekräftas. Flödespris korrigeras för framledningstemperatur; full formel saknas." är fullt löst av kombinationen `rate_period`-rättelsen ovan OCH den nya `supply_temperature_adjusted_flow`-motorn (batch 3) — TA BORT issue-raden. Navirum Norrköping/Söderköping (bostäder).
- **Disposition:** `ready_to_implement`


#### `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter-2026`
- **Leverantör / nät / kundkategori:** Navirum Energi - Norrköping och Söderköping — Norrköping och Söderköping – Övriga fastigheter — övriga fastigheter
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `25_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--norrkoping-soderkoping-2026.pdf) — rättad till den aktuella officiella 2026-källan, granskning 2026-09-08-003 (v3 citerade av misstag 2025-URL:en)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04; teknisk-kartläggning v4)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (supply_temperature_adjusted_flow)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW), medelframledningstemp `Tf` (°C) OCH flöde (`flode_m3`, m³) — alla tre fakturan/avtalet. Endast fullvärmekunder i denna disposition; 36-månadersmetoden för bas-/delvärmekunder är EN EGEN VARIANT, se särfallstabellen.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** E.ON/Navirum — rullande högutväxling, ny motortyp
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1, gäller samtliga åtta E.ON/Navirum-rader): `fixed: null` och `rate_period: null` — verifieringslistan anger att ingen separat fast avgift finns och att effektpriset är per kW och MÅNAD; sätt `fixed: 0`, `rate_period: "month"`. Utan denna rättelse riskerar en framtida feltolkning en 12× fel årskostnad (motorn ×12:ar bara när rate_period="month"). Golden-test: ett handräknat helår bekräftar korrekt ×12-periodisering och att `fixed=0` inte tillför en dold stående kostnad. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Effektprisets tidsenhet måste bekräftas. Flödespris korrigeras för framledningstemperatur; full formel saknas." är fullt löst av kombinationen `rate_period`-rättelsen ovan OCH den nya `supply_temperature_adjusted_flow`-motorn (batch 3) — TA BORT issue-raden. Navirum Norrköping/Söderköping (övriga fastigheter).
- **Disposition:** `ready_to_implement`


#### `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader-2026`
- **Leverantör / nät / kundkategori:** Navirum Energi - Örebro, Kumla och Hallsberg — Örebro, Kumla och Hallsberg – Bostäder — bostäder
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `26_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--hallsberg-kumla-orebro-2026.pdf) — rättad till den aktuella officiella 2026-källan, granskning 2026-09-08-003 (v3 citerade av misstag 2025-URL:en)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04; teknisk-kartläggning v4)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (supply_temperature_adjusted_flow)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW), medelframledningstemp `Tf` (°C) OCH flöde (`flode_m3`, m³) — alla tre fakturan/avtalet. Endast fullvärmekunder i denna disposition; 36-månadersmetoden för bas-/delvärmekunder är EN EGEN VARIANT, se särfallstabellen.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** E.ON/Navirum — rullande högutväxling, ny motortyp
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1, gäller samtliga åtta E.ON/Navirum-rader): `fixed: null` och `rate_period: null` — verifieringslistan anger att ingen separat fast avgift finns och att effektpriset är per kW och MÅNAD; sätt `fixed: 0`, `rate_period: "month"`. Utan denna rättelse riskerar en framtida feltolkning en 12× fel årskostnad (motorn ×12:ar bara när rate_period="month"). Golden-test: ett handräknat helår bekräftar korrekt ×12-periodisering och att `fixed=0` inte tillför en dold stående kostnad. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Effektprisets tidsenhet måste bekräftas. Flödespris korrigeras för framledningstemperatur; full formel saknas." är fullt löst av kombinationen `rate_period`-rättelsen ovan OCH den nya `supply_temperature_adjusted_flow`-motorn (batch 3) — TA BORT issue-raden. Navirum Örebro/Kumla/Hallsberg (bostäder).
- **Disposition:** `ready_to_implement`


#### `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter-2026`
- **Leverantör / nät / kundkategori:** Navirum Energi - Örebro, Kumla och Hallsberg — Örebro, Kumla och Hallsberg – Övriga fastigheter — övriga fastigheter
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `26_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--hallsberg-kumla-orebro-2026.pdf) — rättad till den aktuella officiella 2026-källan, granskning 2026-09-08-003 (v3 citerade av misstag 2025-URL:en)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04; teknisk-kartläggning v4)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (supply_temperature_adjusted_flow)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW), medelframledningstemp `Tf` (°C) OCH flöde (`flode_m3`, m³) — alla tre fakturan/avtalet. Endast fullvärmekunder i denna disposition; 36-månadersmetoden för bas-/delvärmekunder är EN EGEN VARIANT, se särfallstabellen.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** E.ON/Navirum — rullande högutväxling, ny motortyp
- **Kvarstående arbete:** `supply_temperature_adjusted_flow` finns INTE i JUSTERINGSTYPER — delad ny motorkod för samtliga åtta E.ON/Navirum-tariffer plus Kraftringen (samma typ). Resultat blir `noggrannhet: snapshot` (rullande effekt ersatt av ett enskilt leverantörsvärde), aldrig `exact`. KATALOGRÄTTELSE krävs FÖRE aktivering (granskning 2026-09-08-004, P1, gäller samtliga åtta E.ON/Navirum-rader): `fixed: null` och `rate_period: null` — verifieringslistan anger att ingen separat fast avgift finns och att effektpriset är per kW och MÅNAD; sätt `fixed: 0`, `rate_period: "month"`. Utan denna rättelse riskerar en framtida feltolkning en 12× fel årskostnad (motorn ×12:ar bara när rate_period="month"). Golden-test: ett handräknat helår bekräftar korrekt ×12-periodisering och att `fixed=0` inte tillför en dold stående kostnad. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "Effektprisets tidsenhet måste bekräftas. Flödespris korrigeras för framledningstemperatur; full formel saknas." är fullt löst av kombinationen `rate_period`-rättelsen ovan OCH den nya `supply_temperature_adjusted_flow`-motorn (batch 3) — TA BORT issue-raden. Navirum Örebro/Kumla/Hallsberg (övriga fastigheter).
- **Disposition:** `ready_to_implement`


#### `nevel-gimo-osterbybruk-och-osthammar-2026`
- **Leverantör / nät / kundkategori:** Nevel — Gimo, Österbybruk och Östhammar — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `27_0` (https://www.prisdialogen.se/wp-content/uploads/2024/10/Prisandringsmodell-2025-Nevel.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan). DESSUTOM prissatt säsongsflöde i m³, januari–april samt oktober–december (7 månader) (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** `volume` gäller ENDAST januari–april samt oktober–december (7 månader) för DENNA tariff (katalogens egen `months`-lista, inte ett generellt okt–apr-antagande) — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik (motorn och testerna måste använda postens egen `months`-lista) innan aktivering.
- **Disposition:** `ready_to_implement`


#### `oresundskraft-angelholm-normal-2026`
- **Leverantör / nät / kundkategori:** Öresundskraft — Ängelholm normal — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `29_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/FV-Prisandringsmodell-2025-Oresundskraft.pdf); `oresund-web` (https://www.oresundskraft.se/foretag/fjarrvarme/priser-fjarrvarme/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan). DESSUTOM prissatt säsongsflöde i m³, januari–mars samt november–december (5 månader) (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** `volume` gäller ENDAST januari–mars samt november–december (5 månader) för DENNA tariff (katalogens egen `months`-lista, inte ett generellt okt–apr-antagande) — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik (motorn och testerna måste använda postens egen `months`-lista) innan aktivering.
- **Disposition:** `ready_to_implement`


#### `oresundskraft-helsingborg-normal-2026`
- **Leverantör / nät / kundkategori:** Öresundskraft — Helsingborg normal — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `29_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/FV-Prisandringsmodell-2025-Oresundskraft.pdf); `oresund-web` (https://www.oresundskraft.se/foretag/fjarrvarme/priser-fjarrvarme/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan). DESSUTOM prissatt säsongsflöde i m³, januari–mars samt november–december (5 månader) (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** `volume` gäller ENDAST januari–mars samt november–december (5 månader) för DENNA tariff (katalogens egen `months`-lista, inte ett generellt okt–apr-antagande) — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik (motorn och testerna måste använda postens egen `months`-lista) innan aktivering.
- **Disposition:** `ready_to_implement`


#### `oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024-2026`
- **Leverantör / nät / kundkategori:** Öresundskraft — Helsingborg Totalvärme, central installerad före 2024 — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `29_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/FV-Prisandringsmodell-2025-Oresundskraft.pdf); `oresund-web` (https://www.oresundskraft.se/foretag/fjarrvarme/priser-fjarrvarme/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod (redan stödd `selected_band_affine` + ev. säsongsenergi).
- **Disposition:** `ready_to_implement`


#### `ovik-energi-ornskoldsvik-2026`
- **Leverantör / nät / kundkategori:** Övik Energi — Örnsköldsvik — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `30_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Naringsfastighet-Ovik-Energi.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW, fakturan).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Familj 4 — Sandviken-mönstret
- **Kvarstående arbete (utökat i v5):** Katalogrättelse krävs FÖRE aktivering: `fixed: null`→0, `monthly_proration`→kalenderdagsviktning. YTTERLIGARE KATALOGRÄTTELSE upptäckt av v5:s egen grindverifiering: `issues`-texten "null i fast avgift betyder ej extraherad/separat angiven, inte verifierad noll" TAS BORT när `fixed:0` sätts — den är den precisa varning rättelsen besvarar, inte en kvarstående öppen fråga.
- **Disposition:** `ready_to_implement`


#### `partille-energi-partille-2026`
- **Leverantör / nät / kundkategori:** Partille Energi — Partille — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `31_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Partille-Energi-2025.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW, fakturan) OCH returtemperaturavvikelse (`avvikelse_c`, °C — `temperature_difference`, redan i JUSTERINGSTYPER, formeln `energi_MWh×7×avvikelse`).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Familj 4-liknande — temperaturfält, redan stödd typ
- **Kvarstående arbete:** Ingen ny motorkod (samma indatafält som Göteborg/Södertörn). v1 utelämnade felaktigt detta obligatoriska temperaturfält för Partille.
- **Disposition:** `ready_to_implement`


#### `piteenergi-norrfjarden-och-sjulnas-2026`
- **Leverantör / nät / kundkategori:** PiteEnergi — Norrfjärden och Sjulnäs — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `pite-small` (https://www.piteenergi.se/fjarrvarme/priser-2-foretag/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan). DESSUTOM prissatt säsongsflöde i m³, januari–mars samt oktober–december (6 månader) (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** `volume` gäller ENDAST januari–mars samt oktober–december (6 månader) för DENNA tariff (katalogens egen `months`-lista, inte ett generellt okt–apr-antagande) — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik (motorn och testerna måste använda postens egen `months`-lista) innan aktivering.
- **Disposition:** `ready_to_implement`


#### `piteenergi-pitea-centrala-natet-2026`
- **Leverantör / nät / kundkategori:** PiteEnergi — Piteå centrala nätet — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `pite-central` (https://www.piteenergi.se/fjarrvarme/priser-foretag/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan). DESSUTOM prissatt säsongsflöde i m³, januari–mars samt oktober–december (6 månader) (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** `volume` gäller ENDAST januari–mars samt oktober–december (6 månader) för DENNA tariff (katalogens egen `months`-lista, inte ett generellt okt–apr-antagande) — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik (motorn och testerna måste använda postens egen `months`-lista) innan aktivering.
- **Disposition:** `ready_to_implement`


#### `skovde-energi-skovde-2026`
- **Leverantör / nät / kundkategori:** Skövde Energi — Skövde — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `35_0` (https://www.prisdialogen.se/wp-content/uploads/2025/10/Skovde-Energi-prisandringsmodell-2025.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod (redan stödd `selected_band_affine` + ev. säsongsenergi).
- **Disposition:** `ready_to_implement`


#### `soderhamn-nara-soderhamn-taxa-11-och-12-2026`
- **Leverantör / nät / kundkategori:** Söderhamn Nära — Söderhamn företag, taxa 10–13 — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `36_1` (https://www.prisdialogen.se/wp-content/uploads/2024/10/Normalprislista-Soderhamn-Nara-2025.pdf); `web-review-soderhamn-final` (https://www.soderhamnnara.se/sidor/fjarrvarme/foretagskunder/priser-foretag.html)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod (redan stödd `selected_band_affine` + ev. säsongsenergi).
- **Disposition:** `ready_to_implement`


#### `sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026`
- **Leverantör / nät / kundkategori:** Södertörns Fjärrvärme — Södertörns Fjärrvärme — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `37_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-SFAB.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW, fakturan) OCH temperaturavvikelse mot nätets returmedel (`avvikelse_c`, °C, fakturan — `temperature_difference`, redan i JUSTERINGSTYPER). Kundvald effekt med överuttagsavgift är EN EGEN VARIANT, se särfallstabellen — endast SFAB:s rekommenderade effekt ingår i denna disposition.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Familj 4 — Sandviken-mönstret + temperaturfält
- **Kvarstående arbete:** `Tariffpolicy` (effekt) + befintligt `temperature_difference`-indatafält. Ingen ny motorkod för normalfallet.
- **Disposition:** `ready_to_implement`


#### `stockholm-exergi-stockholm-exergi-normal-2026`
- **Leverantör / nät / kundkategori:** Stockholm Exergi — Stockholm Exergi normal — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `stockholm-2026` (https://www.stockholmexergi.se/wp-content/uploads/2026/04/Normalprislista_fjarrvarme_2026-1.pdf); `web-review-stockholm-clarification` (https://www.stockholmexergi.se/wp-content/uploads/2025/09/Fortydligande-av-prisvillkor-2026.pdf)
- **Giltighet:** valid_from=2026-01-01, valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** **RÄTTAT P1 (granskning `2026-09-08-006`) — katalograden AKTIVERAS INTE.** v6:s plan om ett namngivet grindundantag i `katalog.py` OCH en andra, separat `Tariffpolicy` för samma nyckel `stockholm-exergi-2026` var strukturellt omöjlig (`POLICYREGISTER` är `dict[str, Tariffpolicy]`, en andra post med samma nyckel skriver tyst över den första). Se §6a.4 för den vidtagna vägen: leverantörsfilens redan fakturavaliderade `stockholm-exergi-2026` får sin BEFINTLIGA policy UTÖKAD med `annual_forward`-täckning (inte duplicerad), och katalograden hoppas över via ett nytt, typat `ADAPTERREGISTER`. `grind()`/`katalog.py` rörs INTE — katalograden fortsätter korrekt visa `energiform` som avslagsorsak. Årsindata (kall energi 12 månader, returtemp nov–mar 5 månader, debiterbar effekt — samma tre fält och period-/upplösningskontrakt som `monthly_invoice`) är oförändrade jämfört med v5/v6.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Stockholm Exergi — en konsoliderad policy på leverantörsfilens `stockholm-exergi-2026` (§6a.4), ej Sandviken-mönstret, ej katalogaktivering
- **Kvarstående arbete (rättat i v7, §6a.4):** Berörda filer: `policyregister.py` (BEFINTLIGA `_stockholm_exergi_policy` utökas med `annual_forward` i `tackning` och ändamålsspecifika `kravs_for`, PLUS nytt `ADAPTERREGISTER: dict[str, AdapterEntry]`), `generera.py` (`bygg_ts_fran_katalog` läser `ADAPTERREGISTER`, hoppar över katalograden EFTER att ha verifierat att målpolicyn har `annual_forward`-täckning — kastar annars). `katalog.py` rörs INTE. Bygg ett eget källverifierat årsreferensfall för `annual_forward` (motsvarande Sandvikens granskningskedja `2026-09-06-004`→`2026-09-07-003`). Regressionstest: `monthly_invoice`-kontraktet och dess 18 fakturarader rörs inte och ger identiskt resultat före/efter tillägget. Katalogradens egen `issues`-text ("Förtydligande av prisvillkor 2026 finns...") är redan självlöst men irrelevant — raden aktiveras aldrig, oavsett issue-status.
- **Disposition:** `ready_to_implement` (via leverantörsfilen, INTE via denna katalograd — se §6a.4)


#### `sundsvall-energi-indal-liden-och-lucksta-2026`
- **Leverantör / nät / kundkategori:** Sundsvall Energi — Indal, Liden och Lucksta — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `39_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodellen-2025-Sundsvall.pdf); `web-review-matfors-final` (https://sundsvallenergi.se/paket/foretag---fjarrvarme/2022-08-15-matfors); `web-review-sundsvall-flow` (https://sundsvallenergi.se/images/200.4b4928d418529a086ba40321/1674462914778/Fl%C3%B6despremie.JPG)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Ingen utöver energimängd (MWh).
- **Inmatningslägen:** **RÄTTAT P1 (granskning `2026-09-08-006`) — mwh ENDAST; kr och schablon BLOCKERAS.** v5/v6:s "alla tre lägen via legacy-vägen" var strukturellt fel: tariff-ID:t `sundsvall-energi-indal-liden-och-lucksta-2026` finns INTE i `LEGACY_UNDANTAGNA_TARIFF_ID` (verifierat: bara de sex ursprungliga uppgift-7-tarifferna står i den frozensetten) — `bygg_ts_fran_katalog()` hade KASTAT om tariffen byggts på legacy-vägen utan `contract_required`/policy. Den ska i stället kontraktsgatas med samma minimala mönster som Sandviken: `contract_required: true` + en `Tariffpolicy` med `capacity.type: not_applicable` (inga kapacitetsbundna krav). Kontraktsgated betyder MWh-only (§2:s generella regel), samma blockering av kr/schablon som alla andra `ready_to_implement`-rader.
- **Tariffamilj/adapter:** Ren energitariff — Sandviken-mönstret (minimal kontraktsgated policy, `capacity.type: not_applicable`), INTE legacy-vägen
- **Kvarstående arbete (rättat i v7):** Sätt `capacity.type: "not_applicable"` på katalograden. Mekanismen (`EJ_TILLAMPLIG_KAPACITETSFORM`) är byggd och testad mot fixture sedan etapp 1–4 (2026-09-04), bara inte aktiverad mot denna rad. Sätt `contract_required: true` och registrera en minimal `Tariffpolicy` i `policyregister.py` (inga kravda_falt utöver den vanliga MWh-energin) — samma mönster Sandviken redan bevisat i produktion, ingen ny mekanism. INFORMATIONSFÖRFRÅGAN R14 (medlem `sundsvall-energi`) FÅR `tariff_ids` satt till de två `blocked_external_info`-tarifferna (`sundsvall-energi-sundsvall-normal-2026`, `sundsvall-energi-matfors-och-kvissleby-normal-2026` — Matfors hålls blockerad per granskning 2026-09-08-003, följer teknisk-kartläggning v4) i stället för det medlemsomfattande `member_ids` (§7) — INTE Indal/Liden/Lucksta, som frågan uttryckligen inte gäller. Grindtest: `grind(tariff, blockerade_tariff_ider)` på Indal/Liden/Lucksta ska passera EFTER denna omskopning, medan Sundsvall-normal/Matfors fortsatt blockeras via sina egna tariff-ID:n i `blockerade_tariff_ider`.
- **Disposition:** `ready_to_implement`


#### `tekniska-verken-katrineholm-katrineholm-2026`
- **Leverantör / nät / kundkategori:** Tekniska Verken - Katrineholm — Katrineholm — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `40_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-for-Tekniska-verken-i-Katrineholm-AB-Linkoping-2026.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod (redan stödd `selected_band_affine` + ev. säsongsenergi).
- **Disposition:** `ready_to_implement`


#### `tekniska-verken-linkoping-linkoping-2026`
- **Leverantör / nät / kundkategori:** Tekniska Verken - Linköping — Linköping — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `41_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-for-Tekniska-verken-i-Linkoping-AB-Linkoping-2026.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Leverantörens effekt/band (fakturan). DESSUTOM prissatt säsongsflöde i m³, januari–april samt oktober–december (7 månader) (fakturan/avtalet, `volume`-justering) — inte bara kapacitetsdelen (granskning 2026-09-08-002, P1).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret
- **Kvarstående arbete:** `volume` gäller ENDAST januari–april samt oktober–december (7 månader) för DENNA tariff (katalogens egen `months`-lista, inte ett generellt okt–apr-antagande) — dagens motor applicerar ett enda årsflöde utan `months`-hänsyn. Kräver verifierad säsongsindata och motorsemantik (motorn och testerna måste använda postens egen `months`-lista) innan aktivering.
- **Disposition:** `ready_to_implement`


#### `telge-nat-telge-foretag-och-bostadsrattsforeningar-2026`
- **Leverantör / nät / kundkategori:** Telge Nät — Telge företag och bostadsrättsföreningar — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `telge-attachment` (https://www.telge.se/foretag/fjarrvarme-energi/kundservice/fjarrvarmepris/); `telge-terms` (https://www.prisdialogen.se/wp-content/uploads/2020/11/TN-prislista-fjarrvarme-2025_Foretag.pdf)
- **Giltighet:** valid_from=2026-01-01, valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW, fakturan), normalårskorrigerad energi juli–juni (`normalarskorrigerad_energi_mwh`, MWh, begärs av leverantören — `low_utilization`) OCH returtemperatur (`returtemperatur_c`, °C, fakturan — `incremental_return_temperature`). Tre obligatoriska fält, inte ett.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Familj 4 — Sandviken-mönstret + låg utnyttjning + returtemp
- **Kvarstående arbete (utökat i v5, granskning 2026-09-08-004, P1):** Alla tre justeringstyper redan i JUSTERINGSTYPER. `Tariffpolicy` med tre bundna fält, ingen ny motorkod. KATALOGRÄTTELSE: `issues`-texten är en INAKTUELL kontrollpost — verifieringslistan bekräftar redan att 2025-bilagans tillsvidarevillkor fortsatt gäller 2026. TA BORT issue-raden helt (inte normalisera — frågan är redan besvarad, inte bara känd). Informationsförfrågan R11 (medlem `telge-nat`) TAS BORT ur `remaining_information_requests` av samma skäl.
- **Disposition:** `ready_to_implement`


#### `temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026`
- **Leverantör / nät / kundkategori:** TEMAB Fjärrvärme — Tierp, Karlholmsbruk och Örbyhus — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `43_0` (https://www.prisdialogen.se/wp-content/uploads/2024/10/Prisandringsmodell-TEMAB-Fjarrvarme-AB-2025.pdf); `web-review-temab-final` (https://temab.tierp.se/download/18.7fa3d20319a7bbd966d1fe/1763023016779/Taxa%20f%C3%B6r%20Fj%C3%A4rrv%C3%A4rmeleveranser%202026.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete (utökat i v5, granskning 2026-09-08-004, P1):** Ingen ny motorkod (redan stödd `selected_band_affine` + ev. säsongsenergi). KATALOGRÄTTELSE av `issues`: ersätt nuvarande text med den redan godkända issue-typen "Metod för debiterbar effekt/kapacitet är inte fullständigt mappad; använd leverantörens fakturavärde" — R12:s egen text medger redan att "annars räcker leverantörens debiterbara effekt". Informationsförfrågan R12 (medlem `temab-fjarrvarme`) TAS BORT — bolaget har bara denna enda tariff.
- **Disposition:** `ready_to_implement`


#### `trollhattan-energi-trollhattan-2026`
- **Leverantör / nät / kundkategori:** Trollhättan Energi — Trollhättan — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `44_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Trollhattan.pdf); `web-review-trollhattan-final` (https://www.trollhattanenergi.se/foretag/fjarrvarme/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Prisgrundande effekt/band (fakturan). Automatisk bandval BLOCKERAS — leverantören/fakturan anger bandet.
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Leverantörsvärde-mönstret (fristående)
- **Kvarstående arbete:** Ingen ny motorkod (redan stödd `selected_band_affine` + ev. säsongsenergi).
- **Disposition:** `ready_to_implement`


#### `umea-energi-umea-enkel-2026`
- **Leverantör / nät / kundkategori:** Umeå Energi — Umeå Enkel — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `45_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodellen_2025-Umea-Energi.pdf); `web-review-umea-terms` (https://a.storyblok.com/f/162274/x/bed500e2ec/prisvillkor-fjarrvarme.pdf); `web-review-umea-enkel` (https://www.umeaenergi.se/foretag/varme/priser/prisavtal-enkel)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** NYTT MOTORARBETE (asymmetric_flow_difference)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata (rättat i v7, §6a.2/§6a.3):** Bekräftat effektband-ID (`supplier_confirmed_band_id`, §6a.2 — verifierat: raden har `band_selection` PLUS `post_multiplier` samtidigt, kräver BÅDA nya kontraktsfälten), debiterbar effekt (kW), flöde okt–apr (m³, fakturan, `asymmetric_flow_difference`), OCH kapacitetsfaktorn `B` — katalogens `post_multiplier` är en piecewise-formel av kvoten `U = normalårskorrigerad_energi_dec_jan_feb / energi_sep_apr`, men bolagets normalårskorrigering är INTE publicerad, så `U` kan inte räknas ut ur rå mätdata. Valt kontrakt: leverantörens EGET redan beräknade `B`-värde (fakturan/leverantörsbesked) tas emot som ett obligatoriskt leverantörsvärde — INGEN kalkylatorberäkning av `U`/`B` från energidata. `Tariffpolicy.kapacitet_bindning` binder `billing_basis` (leverantörens årseffekt), `Tariffpolicy.kapacitet_band_bindning` binder det bekräftade bandet, och `Tariffpolicy.kapacitet_multiplikator_bindning` binder `B` (intervall `[0,93; 1,401]`, §6a.3).
- **Inmatningslägen:** mwh (samtliga fält krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Umeå — ny motortyp `asymmetric_flow_difference`, bandkontraktet (§6a.2) OCH en arkitektoniskt separat `post_multiplier`-medveten kompositgrind (§6a.3, INTE en ändring av den nakna `grind()`)
- **Kvarstående arbete (rättat i v7):** (1) `asymmetric_flow_difference` finns INTE i JUSTERINGSTYPER — byggs separat från Vattenfalls blockerade variant av samma typnamn (Umeås formel är komplett och byggbar, Vattenfalls är det inte). (2) **RÄTTAT P1 (granskning `2026-09-08-006`):** den NAKNA `grind()` ändras INTE och fortsätter avvisa `post_multiplier` för alla tariffer. I stället körs en NY, separat `kontrollera_kompositgrind(tariff, policy)` (§6a.3) EFTER `grind()`, som bara godkänner `post_multiplier` när `policy.kapacitet_multiplikator_bindning` är satt och verifierad. (3) Handräknade testfall vid `B=0,93`, `B=1,401` (§6a.3s omräknade tak, inte det tidigare gissade `1,4`) och en punkt mellan brytpunkterna — testet heter `B-intervall`, inte "U-intervall", eftersom motorn aldrig räknar `U`. Ett negativt test för `B=14` ska blockera via kompositgrinden. (4) Bandkontraktet (§6a.2) läggs till som ett fjärde, separat obligatoriskt fält. (5) Katalogradens `issues`-text ("Hela effektkostnaden multipliceras med B...") är fullt löst av leverantörsvärdekontraktet ovan — TA BORT issue-raden.
- **Disposition:** `ready_to_implement`


#### `vanerenergi-mariestad-och-toreboda-2026`
- **Leverantör / nät / kundkategori:** VänerEnergi — Mariestad och Töreboda — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json` (se proveniens)
- **Primärkälla:** `46_0` (https://vanerenergi.se/fjarrvarme/priser-fjarrvarme-foretag-2026, PDF: https://vanerenergi.se/download/18.76bfc4fd19a0f6d5c0785f/1761289418005/Pris%C3%A4ndringsmodellen%20Mariestad%20T%C3%B6reboda%20%202026-2028.pdf) — rättad till den aktuella officiella 2026-källan, granskning 2026-09-08-003 (v3 citerade av misstag 2025-URL:en)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad (verifieringslistan 2026-09-04)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` — väntar på denna implementationsomgång, inte på nytt leverantörsbesked
- **Motorstatus:** Befintlig (`selected_band_affine`/säsongsenergi)
- **Kontraktsstatus:** ej i `POLICYREGISTER` ännu
- **Teststatus:** inga tariffspecifika automattester ännu
- **UI-status:** inte valbar i kalkylatorn ännu
- **Årsreproducerbar med nuvarande underlag:** Ja
- **Obligatorisk indata:** Debiterbar effekt (kW, fakturan) OCH flöde (`flode_m3`, m³/år, fakturan — `volume`, gäller alla 12 månader för denna tariff, ingen `months`-begränsning).
- **Inmatningslägen:** mwh (obligatorisk indata krävs); kr och schablon BLOCKERAS (ingen verifierad invers/schablonmodell)
- **Tariffamilj/adapter:** Familj 4 — Sandviken-mönstret + flöde
- **Kvarstående arbete:** `volume` redan i JUSTERINGSTYPER och tillämpar redan hela året för denna tariff (inga säsongsmånader att missa). `Tariffpolicy` med två bundna fält.
- **Disposition:** `ready_to_implement`

### 4.2 Blockerade av extern information (26 produkter)

Endast produkter där prisbestämningen själv är tvetydig, motsägs, eller där en obligatorisk
prisdel helt saknar publicerat värde. Frågan i sista fältet är den som ska skickas till
leverantören (ordagrant eller nästan ordagrant från verifieringslistan/teknisk-kartläggningen
— inte omformulerad här).


#### `eskilstuna-energi-och-miljo-eskilstuna-2026`
- **Leverantör / nät / kundkategori:** Eskilstuna Energi och Miljö — Eskilstuna — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `05_1` (https://www.prisdialogen.se/wp-content/uploads/2025/10/Normalprislista-EEM-2025.pdf); `web-review-eem-price` (https://www.eem.se/foretag/fjarrvarme/priser/fjarrvarmepris-2026); `web-review-eem-model` (https://www.eem.se/foretag/fjarrvarme/priser/prismodell); `web-review-eem-flow` (https://www.eem.se/foretag/fjarrvarme/redan-fjarrvarmekund/flodestaxa)
- **Giltighet:** valid_from=2026-01-01, valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** källgranskad för formeln, men nätreferensen olöst (verifieringslistan 2026-09-04; granskning 2026-09-08-002, P1 — flyttad hit från `ready_to_implement`)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst (`network_flow_difference` skulle ändå krävt ny motorkod)
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej — formeln `(kundens_m3 − nätreferens_m3_per_MWh × kundens_MWh) × 4` är känd, men nätreferensen `monthly_mean_for_customers_covered_by_flow_tariff` är INTE ett statiskt katalogvärde och inte beskriven som en fakturapost kunden kan läsa av. Samma typ av blockering som Vattenfalls `asymmetric_flow_difference` (nätreferensen där är också "beräknad för aktuell månad", inte publicerad).
- **Exakt saknad uppgift/fråga:** Är nätets `monthly_mean_for_customers_covered_by_flow_tariff`-referens ett fast, publicerat värde per prisår (och i så fall vilket, och var står det), eller varierar det per faktisk kalendermånad? Om det varierar per månad: hur ska kunden hitta/verifiera det värde som gällde för sin faktura, månad för månad?
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`


#### `gavle-energi-gavle-2026`
- **Leverantör / nät / kundkategori:** Gävle Energi — Gävle — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `08_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-naringsidkare-2025-Gavle-Energi.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Beräknas volymavdraget marginalt eller på hela månadens volym efter uppnådd nivå?
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `harnosand-energi-miljo-harnosand-2026`
- **Leverantör / nät / kundkategori:** Härnösand Energi & Miljö — Härnösand — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `13_1` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prislista-flerbostadshus-2025-Harnosand.pdf); `web-review-hemab-final` (https://www.hemab.se/download/18.727ad6af19ac23cdb98120ae/1764247260203/Prislista%20flerbostadshus%202026.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Prislistans räkneexempel (1750 MWh) motsäger den publicerade intervalltabellen — vilken är korrekt?
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `hassleholm-miljo-hassleholm-2026`
- **Leverantör / nät / kundkategori:** Hässleholm Miljö — Hässleholm — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `14_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Hassleholm-2025.pdf); `web-review-hassleholm-model` (https://hassleholmmiljo.se/foretag/fjarrvarme/fjarrvarmepriser-prismodell-och-prisdialogen/prismodell); `web-review-hassleholm-final` (https://hassleholmmiljo.se/foretag/fjarrvarme/fjarrvarmepriser-prismodell-och-prisdialogen/fjarrvarmepriser/fjarrvarmepriser-2026-hassleholm); `web-review-tyringe-final` (https://hassleholmmiljo.se/foretag/fjarrvarme/fjarrvarmepriser-prismodell-och-prisdialogen/fjarrvarmepriser/fjarrvarmepriser-2026-tyringe)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Beräknas effektrabatten intervallvis eller på hela effekten?
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `hassleholm-miljo-tyringe-2026`
- **Leverantör / nät / kundkategori:** Hässleholm Miljö — Tyringe — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `14_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Hassleholm-2025.pdf); `web-review-hassleholm-model` (https://hassleholmmiljo.se/foretag/fjarrvarme/fjarrvarmepriser-prismodell-och-prisdialogen/prismodell); `web-review-hassleholm-final` (https://hassleholmmiljo.se/foretag/fjarrvarme/fjarrvarmepriser-prismodell-och-prisdialogen/fjarrvarmepriser/fjarrvarmepriser-2026-hassleholm); `web-review-tyringe-final` (https://hassleholmmiljo.se/foretag/fjarrvarme/fjarrvarmepriser-prismodell-och-prisdialogen/fjarrvarmepriser/fjarrvarmepriser-2026-tyringe)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Beräknas effektrabatten intervallvis eller på hela effekten?
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `lidkoping-energi-lidkoping-041-kw-2026`
- **Leverantör / nät / kundkategori:** Lidköping Energi — Lidköping 0–41 kW — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `20_1` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Normalprislista-2025-Lidkoping-Energi.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus (rättat i v16, bedömning `2026-09-09-006`):** externt källunderlag GODKÄNT
  2026-09-09. Lidköping Energis värmenätschef bekräftade skriftligt (svarsdatum 2026-09-09
  10:07) samtliga åtta öppna punkter: moms exkluderad är korrekt; flödesavgift/-premie
  gäller prisgrupp 2–5; flödesprisfaktorn `N = 5 kr/m³`; formeln `N × Q × (1 − T/Tm)`; `Tm` =
  nätets månadsvisa medel av samtliga anläggningars `T_in − T_ut`; komponenten gäller alla
  månader, debiteras/krediteras månadsvis; debiterbar effekt i första hand via
  effektsignatur vid −10 °C (i andra hand högsta uppmätta dygnsmedeleffekt) — den redan
  beslutade `selected_band_affine`-vägen kan fortsatt kräva leverantörens fastställda effekt
  i stället; fasta års-/effektavgifter periodiseras 1/12 per månad. Lokal källa:
  `Fjarrvarmetariffer/Sv Förtydligande av fjärrvärmetaxa för företagskunder 2026.pdf`,
  `source_sha256:
  93b47766933ba2cd6c841db982cc0981a4b44ec39fe08ff543b3c707746e8f34` (rå PDF INTE tillagd i
  git — innehåller kontaktuppgifter, väntar på Roberts separata beslut, se
  `verifieringslista-fjarrvarmebolag.md`). **Källgodkännande ≠ implementation/
  fakturavalidering:** `Tm`s tolv faktiska månadsutfall är ett RUNTIMEKRAV (leverantörssvaret
  ger metoden, inte de faktiska talen) — se §6a.7.
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` (kvarstår
  tills adjustments-posten §6a.7 beskriver är byggd — planeras, inte genomförd av detta
  dokument)
- **Motorstatus:** N/A tills batch 5d (§6a.7, `batchplan-v17.md`) är implementerad
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Ja, källmässigt (metoden är komplett
  specificerad); Nej för ett konkret kundfall förrän `Tm`s tolv månadsvärden finns (faktura
  eller direkt leverantörsbesked) — se §6a.7:s runtime-krav.
- **Exakt saknad uppgift/fråga:** LÖST källmässigt (var: 2026 års flödesprisfaktor N och
  nätmedelvärde Tm). Kvarstår: konkreta `Tm`-månadsvärden per kundfall (runtime, inte
  katalogstatiskt) och fakturaverifiering av resultatet (visas `uppskattat` tills dess).
- **Inmatningslägen:** blockerade tills batch 5d är implementerad; därefter blockerat
  fail-closed per kundfall om någon av de tre 12-månadersserierna (`Q_m`, `T_m`, `Tm_m`)
  saknas eller har fel längd
- **Disposition (ändrad i v16):** `ready_to_implement` (var `blocked_external_info`)

#### `lidkoping-energi-lidkoping-42-kw-2026`
- **Leverantör / nät / kundkategori:** Lidköping Energi — Lidköping 42+ kW — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `20_1` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Normalprislista-2025-Lidkoping-Energi.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus (rättat i v16, bedömning `2026-09-09-006`):** identisk källgodkänning som
  `lidkoping-energi-lidkoping-041-kw-2026` ovan (samma leverantörssvar, samma
  `source_sha256`, samma åtta bekräftelser, samma runtime-krav på `Tm`). Se raden ovan för
  fullständig text.
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds` (planerat,
  inte genomfört av detta dokument)
- **Motorstatus:** N/A tills batch 5d (§6a.7, `batchplan-v17.md`) är implementerad
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Ja, källmässigt; Nej per konkret kundfall
  förrän `Tm`s tolv månadsvärden finns — se §6a.7.
- **Exakt saknad uppgift/fråga:** LÖST källmässigt. Kvarstår: konkreta `Tm`-månadsvärden per
  kundfall och fakturaverifiering.
- **Inmatningslägen:** blockerade tills batch 5d är implementerad; därefter fail-closed per
  kundfall om `Q_m`/`T_m`/`Tm_m` saknas eller har fel längd
- **Disposition (ändrad i v16):** `ready_to_implement` (var `blocked_external_info`)

#### `malarenergi-vasteras-och-hallstahammar-gruppanslutna-smahus-2026`
- **Leverantör / nät / kundkategori:** Mälarenergi — Västerås och Hallstahammar, gruppanslutna småhus — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `22_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Malarenergi.pdf); `web-review-malar-price` (https://www.malarenergi.se/foretag/varme-kyla-foretag/fjarrvarme-foretag/priser-fjarrvarme/); `web-review-malar-flow` (https://www.malarenergi.se/foretag/varme-kyla-foretag/fjarrvarme-foretag/flodespremie/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Samma frågor, plus om flödespremien alls gäller gruppanslutna småhus.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `malarenergi-vasteras-och-hallstahammar-storre-fastigheter-2026`
- **Leverantör / nät / kundkategori:** Mälarenergi — Västerås och Hallstahammar, större fastigheter — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `22_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-2025-Malarenergi.pdf); `web-review-malar-price` (https://www.malarenergi.se/foretag/varme-kyla-foretag/fjarrvarme-foretag/priser-fjarrvarme/); `web-review-malar-flow` (https://www.malarenergi.se/foretag/varme-kyla-foretag/fjarrvarme-foretag/flodespremie/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Sommarperiodens avgränsning, överuttagsavgiftens debitering, flödesavgiftens sats över nätmedel; ny energiform (base_peak_summer).
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `skelleftea-kraft-boliden-burea-burtrask-byske-jorn-kage-lovanger-norsjo-robertsfors-stensele-storuman-vindeln-anaset-2026`
- **Leverantör / nät / kundkategori:** Skellefteå Kraft — Boliden, Bureå, Burträsk, Byske, Jörn, Kåge, Lövånger, Norsjö, Robertsfors, Stensele, Storuman, Vindeln, Ånäset — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `34_2` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prislista_Fjarrvarmepriser_FORETAG_Pelletsorter-2025-Skelleftea-Kraft.pdf); `web-review-skelleftea-final` (https://www.skekraft.se/wp-content/uploads/2025/12/Prislista_fjarrvarme_ftg_kraftvarmeort_2026.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Samma, dimensionerande temperatur för Stensele.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `skelleftea-kraft-skelleftea-skelleftehamn-ursviken-lycksele-mala-2026`
- **Leverantör / nät / kundkategori:** Skellefteå Kraft — Skellefteå, Skelleftehamn, Ursviken, Lycksele, Malå — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `34_1` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prislista_Fjarrvarmepriser_FORETAG_Kraftvarmeorter-2025-Skelleftea-Kraft.pdf); `web-review-skelleftea-final` (https://www.skekraft.se/wp-content/uploads/2025/12/Prislista_fjarrvarme_ftg_kraftvarmeort_2026.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Valutaenhet för energirabatten (Qnorm×A+B) samt dimensionerande temperatur för Ursviken.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `sundsvall-energi-matfors-och-kvissleby-normal-2026`
- **Leverantör / nät / kundkategori:** Sundsvall Energi — Matfors och Kvissleby normal — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `39_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodellen-2025-Sundsvall.pdf); `web-review-matfors-final` (https://sundsvallenergi.se/paket/foretag---fjarrvarme/2022-08-15-matfors); `web-review-sundsvall-flow` (https://sundsvallenergi.se/images/200.4b4928d418529a086ba40321/1674462914778/Fl%C3%B6despremie.JPG)
- **Giltighet:** valid_from=2026-01-01, valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `network_m3_per_MWh` (nätreferens för flödesjusteringen) saknas helt som katalogdata — teknisk-kartläggning v4 överprövar verifieringslistans äldre ✅ här.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `sundsvall-energi-sundsvall-normal-2026`
- **Leverantör / nät / kundkategori:** Sundsvall Energi — Sundsvall normal — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `39_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodellen-2025-Sundsvall.pdf); `web-review-matfors-final` (https://sundsvallenergi.se/paket/foretag---fjarrvarme/2022-08-15-matfors); `web-review-sundsvall-flow` (https://sundsvallenergi.se/images/200.4b4928d418529a086ba40321/1674462914778/Fl%C3%B6despremie.JPG)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Hur får kunden nätvärdet Qalla/Walla för flödespremien varje månad (formeln i övrigt känd)? Blockera dessutom automatisk prissättning ≥2000 kW.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-haninge-tyreso-alta-och-gustavsberg-gustavsberg-spetsig-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Haninge, Tyresö, Älta och Gustavsberg — Gustavsberg – Spetsig — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `47_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Haninge-Tyreso-Alta-och-Gustavsberg-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-haninge-tyreso-alta-och-gustavsberg-gustavsberg-standard-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Haninge, Tyresö, Älta och Gustavsberg — Gustavsberg – Standard — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `47_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Haninge-Tyreso-Alta-och-Gustavsberg-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-haninge-tyreso-alta-och-gustavsberg-haninge-tyreso-och-alta-spetsig-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Haninge, Tyresö, Älta och Gustavsberg — Haninge, Tyresö och Älta – Spetsig — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `47_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Haninge-Tyreso-Alta-och-Gustavsberg-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-haninge-tyreso-alta-och-gustavsberg-haninge-tyreso-och-alta-standard-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Haninge, Tyresö, Älta och Gustavsberg — Haninge, Tyresö och Älta – Standard — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `47_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Haninge-Tyreso-Alta-och-Gustavsberg-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-motala-och-askersund-motala-och-askersund-spetsig-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Motala och Askersund — Motala och Askersund – Spetsig — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `48_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Motala-och-Askersund-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-motala-och-askersund-motala-och-askersund-standard-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Motala och Askersund — Motala och Askersund – Standard — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `48_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Motala-och-Askersund-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-nykoping-nykoping-spetsig-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Nyköping — Nyköping – Spetsig — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `49_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Nykoping-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-nykoping-nykoping-standard-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Nyköping — Nyköping – Standard — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `49_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Nykoping-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-uppsala-uppsala-spetsig-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Uppsala — Uppsala – Spetsig — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `50_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Uppsala-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-uppsala-uppsala-standard-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Uppsala — Uppsala – Standard — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `50_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Uppsala-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-vanersborg-vanersborg-spetsig-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Vänersborg — Vänersborg – Spetsig — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `51_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Vanersborg-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vattenfall-vanersborg-vanersborg-standard-2026`
- **Leverantör / nät / kundkategori:** Vattenfall - Vänersborg — Vänersborg – Standard — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `51_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-Vanersborg-2025.pdf); `vattenfall-model` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/); `web-review-vattenfall-model-current` (https://www.vattenfall.se/foretag/varme-kyla/fjarrvarme/priser/prismodell/)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** `asymmetric_flow_difference` (delproblem 3.3): nätreferensen (`reference: "network_average"`) är inte verifierad som ett statiskt katalogvärde — källan beskriver den som beräknad för aktuell månad. Hela tariffgruppens resultat förblir `blocked` tills 3.3 är löst, per teknisk-kartläggning v4 — oavsett att delproblemen 3.1 (produktval), 3.2 (säsongsvolymrabatt) och 3.4 (`capacity_overrun`-spärr) är byggbara internt.
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

#### `vb-energi-normal-2026`
- **Leverantör / nät / kundkategori:** VB Energi — Ludvika, Björnmossen, Grängesberg, Fagersta och Norberg — näring/brf
- **Prisår/giltighet:** 2026, `optimate-fjarrvarme-2026.json`
- **Primärkälla:** `52_0` (https://www.prisdialogen.se/wp-content/uploads/2021/01/Prisandringsmodell-Vasterbergslagens-Energi-AB-2025.pdf)
- **Giltighet:** valid_from=unknown (katalogens `valid_from` är null), valid_to=unknown (katalogens `valid_to` är null)
- **Källstatus:** villkorat godkänd/motsägelsefull (verifieringslistan 2026-09-04, teknisk-kartläggning v4 för Vattenfall/Sundsvall Matfors)
- **Katalogstatus:** `production_ready: false`, `investigation.status: utreds`
- **Motorstatus:** N/A tills källfrågan är löst
- **Kontraktsstatus:** ej i `POLICYREGISTER`
- **Teststatus:** inga
- **UI-status:** inte valbar
- **Årsreproducerbar med nuvarande underlag:** Nej
- **Exakt saknad uppgift/fråga:** Effektperiod november–mars eller december–mars (två officiella källor motsäger varandra); vilket mät-/normalår och omprövningsdag styr prisgrupp; plus ny energiform (annual_volume_band_monthly).
- **Inmatningslägen:** samtliga blockerade tills källfrågan är löst
- **Disposition:** `blocked_external_info`

## 5. Tariffvarianter — integrerade i den räknade kontrollmängden

Enligt granskning `2026-09-08-002` (P1): dessa sju kända variantfamiljer får INTE stå
utanför totalen längre. Var och en är nu en egen, räknad, stabil variant-ID i kontrollmängden
— ingen väntar på en "framtida inventeringsversion". `not_applicable` används aldrig för en
verklig, källkänd variant.

E.ON/Navirums 36-månadersmetod gäller samtliga åtta bastariffer separat — den räknas
därför som ÅTTA variant-ID:n (en per bastariff), inte en enda ospecificerad post, enligt
granskningens explicita krav på en modelleringsregel per bastariff.

**Rättat i v4 (granskning `2026-09-08-003`, P1):** E.ON/Navirums 36-månadersvariant beskrev
tidigare fel fysisk storhet (framledningstemperatur i stället för dygnsmedeleffekt) och fel
kontrakt. Verifieringslistans exakta regel (rad "E.ON - Järfälla", verifierad 2026-09-04):
*"För kunder där en annan värmekälla levererar bas- eller delvärme används i stället
medelvärdet av de tre högsta dygnsmedeleffekterna under de senaste 36 månaderna, inklusive
fakturamånaden."* — detta är effekt (kW), inte temperatur. Flödeskorrigeringens
medelframledningstemperatur `Tf` är ett HELT SEPARAT fält som redan finns i bastariffens
huvuddisposition (§4.1, batch 3).

**Valt kontrakt (av två möjliga, se granskningens rättningskrav):** leverantörens egna,
redan beräknade debiterbara effekt tas emot som obligatorisk MÅNADSVÄRDESINDATA — SAMMA
leverantörsvärde-mönster som bastariffens huvudfall redan använder (huvudfallets
effektsignatur vid −15 °C är också ett leverantörsberäknat värde, inte en kalkylator-
regression). Kalkylatorn bygger INGEN egen tidsserie-/topp-tre-motor för 36 månader — det
vore en betydligt större motorinsats utan dokumenterad kund-/prospektprioritet. Resultatet
blir `noggrannhet: snapshot` (ett leverantörsvärde, inte en verifierad kalkylatorberäkning),
aldrig `exact` — samma klassificering som huvudfallet.

| Variant-ID | Bastariff | Källa | Vad den kräver | Obligatorisk indata | Inmatningsläge | Batch | Disposition |
|---|---|---|---|---|---|---|---|
| `e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026--bas-delvarme` | `e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026` | `03_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--bro-balsta-jarfalla-kungsangen-2026.pdf) | 36-månadersmetoden för kunder med bas-/delvärmekälla i stället för fullvärme — leverantörens medelvärde av de TRE HÖGSTA DYGNSMEDELEFFEKTERNA (kW) senaste 36 månaderna inkl. fakturamånaden (verifieringslistan) | Debiterbar effekt (kW, fakturan — leverantörens 36-månadersberäkning, samma fält som huvudfallet men annan beräkningskälla), medelframledningstemp `Tf` (°C, fakturan, hör till den separata flödeskorrigeringen) OCH flöde (`flode_m3`, m³, fakturan) — SAMMA tre fält som bastariffens huvuddisposition | mwh; kr/schablon blockerade | 3b (efter batch 3) | `ready_to_implement` |
| `e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter-2026--bas-delvarme` | samma, övriga fastigheter | `03_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--bro-balsta-jarfalla-kungsangen-2026.pdf) | samma | samma | samma | 3b | `ready_to_implement` |
| `e-on-malmo-malmo-och-burlov-bostader-2026--bas-delvarme` | samma, Malmö/Burlöv bostäder | `04_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser-malmo-2026.pdf) | samma | samma | samma | 3b | `ready_to_implement` |
| `e-on-malmo-malmo-och-burlov-ovriga-fastigheter-2026--bas-delvarme` | samma, övriga fastigheter | `04_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser-malmo-2026.pdf) | samma | samma | samma | 3b | `ready_to_implement` |
| `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader-2026--bas-delvarme` | samma | `25_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--norrkoping-soderkoping-2026.pdf) | samma | samma | samma | 3b | `ready_to_implement` |
| `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter-2026--bas-delvarme` | samma | `25_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--norrkoping-soderkoping-2026.pdf) | samma | samma | samma | 3b | `ready_to_implement` |
| `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader-2026--bas-delvarme` | samma | `26_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--hallsberg-kumla-orebro-2026.pdf) | samma | samma | samma | 3b | `ready_to_implement` |
| `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter-2026--bas-delvarme` | samma | `26_0` (https://www.eon.se/content/dam/eon-se/swe-documents/swe-jamfor-fjarrvarmepriser--hallsberg-kumla-orebro-2026.pdf) | samma | samma | samma | 3b | `ready_to_implement` |
| `sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026--kundvald-effekt` | `sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026` | `sfab-prislista-2026` (https://sfab.se/media/33mnnexa/prislista-normal-2026.pdf) — rättad till aktuell officiell 2026-källa, granskning 2026-09-08-004, P2 | Kundvald effekt (i stället för SFAB:s rekommenderade) med egen överuttagsavgift; formeln är inte kartlagd i detalj och skiljer sig från katalogschemats `capacity_overrun`-typ | Okänt tills källfrågan är löst | samtliga blockerade | Ej batchad | `blocked_external_info` — fråga: "Vilken exakt formel/sats gäller för överuttagsavgiften vid kundvald effekt, och skiljer den sig från standardschemats `capacity_overrun`?" |
| `kraftringen-kraftringen-2026--brunnshog` | `kraftringen-kraftringen-2026` | `19_0` (https://www.kraftringen.se/brf/varme-och-kylalosningar/fjarrvarme/fjarrvarmepriser/) | Brunnshögs egen nätdel/prisstruktur, inte kartlagd — bara ordinarie nät är verifierat i §4.1 | Okänt tills källfrågan är löst | samtliga blockerade | Ej batchad | `blocked_external_info` — fråga: "Vilken är Brunnshögs egen prislista/formel, och skiljer den sig från Kraftringens ordinarie nät?" |
| `tekniska-verken-linkoping-linkoping-2026--lagtemperatur` | `tekniska-verken-linkoping-linkoping-2026` | `41_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Prisandringsmodell-for-Tekniska-verken-i-Linkoping-AB-Linkoping-2026.pdf) | Lågtemperaturleveransens egen tariffstruktur, inte kartlagd i detalj | Okänt tills källfrågan är löst | samtliga blockerade | Ej batchad | `blocked_external_info` — fråga: "Vilken är lågtemperaturleveransens fullständiga prisstruktur (kapacitet, energi, ev. justeringar)?" |
| `finspangs-tekniska-verk-finspang-2026--spetsvarmetillagg` | `finspangs-tekniska-verk-finspang-2026` | `web-review-finspang-final` (https://d2sabnli7hsonp.cloudfront.net/finspangs-tekniska/image/upload/fl_attachment/v1762179931/zvwzbdzlxxtsl15nsxrd.pdf) — rättad till aktuell officiell 2026-källa, granskning 2026-09-08-004, P2 (v4 citerade av misstag 2025-dokumentet) | Spetsvärmetillägget (20 %) — det procentuella villkoret är källkänt, men VILKA kunder/perioder som utlöser tillägget och om 20 % gäller samtliga prisdelar (effekt, energi OCH flöde, eller bara en delmängd) är INTE mappat mot en entydig kund-/avtalsregel. Detta strider mot `ready`-definitionen (samtliga regler verifierade, inget nytt besked krävs) — flyttad till blockerad i v4 (granskning 2026-09-08-003, P1) | Okänt tills källfrågan är löst | samtliga blockerade | Ej batchad | `blocked_external_info` — fråga: "Vilka kunder/perioder utlöser spetsvärmetillägget på 20 %, och gäller procentsatsen samtliga tre prisdelar (effekt, energi, flöde) eller bara en delmängd?" |
| `jonkoping-energi-jonkoping-och-granna-2026--accessavgift` | `jonkoping-energi-jonkoping-och-granna-2026` | `16_0` (https://www.prisdialogen.se/wp-content/uploads/2020/11/Jonkoping-Energi-2025-till-2026-Prisandringsmodell.pdf) | Avtalsberoende accessavgift — verifierade värden 0/10/25/50 kr/mån, ett synligt, obligatoriskt kundval | Kundval i UI (radioknappar/dropdown, 0/10/25/50 kr/mån), inget standardvärde — okänt/tomt val BLOCKERAR beräkningen | mwh; kr/schablon blockerade (som bastariffen) | Samma batch som Jönköpings bastariff (§8 batchplan) | `ready_to_implement` — **beslut fattat av Codex/Robert i granskning `2026-09-08-006`:** en fakturerbar, källkänd och kundkänd avtalsuppgift ska kunna ingå som ett synligt obligatoriskt val. Ingen dubblettprodukt exponeras. |
| `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026--miljotillagg` | `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026` | `borasem-2026` (https://borasem.se/webb/foretag/fjarrvarme/priserochvillkor2026.4.3b2618bc1976272a99c471fd.html) — rättad till aktuell officiell 2026-källa, granskning 2026-09-08-004, P2 | Miljötillägget "Bra Miljöval" (31 SEK/MWh) — ett kundvalt UI-tillval, inte en automatisk prisdel | Kryssruta/kundval i UI, inget nytt fält utöver bastariffens | mwh; kr/schablon blockerade | 6 (samma batch som grundformeln — se §8:s räkningsnot om hur denna variant räknas separat trots att den byggs i samma commit) | `ready_to_implement` |

**14 variant-ID:n totalt, rättat i v7 (Codex/Roberts beslut i granskning `2026-09-08-006`):**
10 `ready_to_implement` (åtta E.ON/Navirum-varianter, Borås tillägg, Jönköpings accessavgift
— flyttad från blockerad), 4 `blocked_external_info` (Södertörn, Kraftringen Brunnshög,
Tekniska Verken Linköping lågtemperatur, Finspångs spetsvärmetillägg).

## 6. Sammansatt aktiveringspreflight — samtliga 45 `ready`-ID:n (granskning 2026-09-08-005/-006/-007, P1)

En bar `grind()`-körning bevisar bara STEG 2 av en riktig aktivering. `grind()` har inget
policyregisterparameter, ingen kännedom om `contract_required`, ingen adapterregistrering,
och ingen åtkomst till leverantörsvalt band eller Umeås framtida multiplikatorbindning
(bekräftat genom att läsa signaturen `grind(tariff: dict, utredda: set[str]) -> str | None`
i `katalog.py` — bara två argument, ingen policy). Ett `grind() is None`-resultat kan alltså
inte i sig bevisa att `bygg_ts_fran_katalog()` (generatorn) faktiskt kommer producera en
selectable rad i kalkylatorn.

**De fyra verifierbara stegen i den sammansatta preflighten:**

1. **Utrednings-/request-status — konkret mutation, inte bara "inte utreds":**
   `investigation.status: "utreds"` → `null` (mekaniskt verifierat: 45/45 rader har i dag
   `"utreds"`, 0/45 har `contract_required` satt) SAMTIDIGT som `contract_required: true`
   sätts för var och en av de 44 katalograder som faktiskt aktiveras (Stockholms
   katalogdubblett förblir explicit `"utreds"`/blockerad, se §6a.4 — den 45:e raden aktiveras
   aldrig via katalogvägen). Detta ÄR den tariffvisa mutationen v6 bara beskrev som ett krav
   utan att namnge den. Samtidigt: tariffens ID får inte längre finnas i
   `blockerade_tariff_ider(katalog)` (§7, den nya sammanslagna `tariff_ids`/`member_ids`-
   upplösningen).
2. **`grind(tariff, blockerade_tariff_ider)` → `None`** — den strukturella kontrollen i
   `katalog.py`, med signaturens andra argument bytt (§7) från medlems-ID-mängden `utredda`
   till en förberäknad tariff-ID-mängd `blockerade_tariff_ider(katalog)`. Grindens jämförelse
   blir därmed `tariff.get("id") in blockerade` — en enda, entydig strängjämförelse, i
   stället för v6:s tvetydiga `grind(tariff, utredda)`-signatur som inte kunde skilja
   tariff-ID:n från medlems-ID:n (granskning `2026-09-08-006`, P1).
3. **Generatorns kontraktsgrind** — `kontrollera_aktiveringsgrind(tariff_id,
   contract_required, register=POLICYREGISTER)` (`policyregister.py`) måste returnera en
   giltig `Tariffpolicy`, VERIFIERAT LÄST: en katalogtariff utanför de sex
   `LEGACY_UNDANTAGNA_TARIFF_ID` MÅSTE ha `contract_required: true` OCH en registrerad,
   komplett policy — annars `raise`:er `bygg_ts_fran_katalog()` i stället för att generera
   en tom rad. Detta steg saknades helt i v5:s tabell.
4. **Ett minimalt giltigt `annual_forward`-anrop** — `beraknaArskostnadMedKontrakt`/
   `berakna_arskostnad_med_kontrakt` med policyns kravda_falt ifyllda av rimliga
   leverantörsvärden ska returnera `status.fullstandighet == "complete"`, inte `"blocked"`.

**Resultat, steg för steg, mot den verkliga katalogen/koden (`enkey-agents@fd8f8da`,
`neptune_academy@f1df177`, skrivskyddat — inget ändrat):**

- **Steg 1+2 (grind-nivå):** FÖRE alla rättningar: 21/45 passerar. **Rättat P2 (granskning
  `2026-09-08-008`):** "45/45 passerar `grind()`" är FEL som ett påstående om den NAKNA
  grinden — Stockholm stoppas fortsatt av `utreds`/`energiform` (den aktiveras aldrig via
  katalogvägen, §6a.4) och Umeå ger fortsatt `"kapacitetsformel med multiplikator"` i den
  nakna grinden (bara den sammansatta `godkanda()`-loopen, §6a.3, kan öppna den raden). Rätt
  beviskedja EFTER v5–v9:s katalog-/motor-/kontraktsrättningar: **43 rader passerar den
  NAKNA `grind()` direkt + Umeå passerar via den sammansatta `godkanda()`-loopen (§6a.3) =
  44 katalogaktiveringar, PLUS Stockholm via en separat leverantörsfilsadapter (§6a.4) = 45
  `ready`-bastariffer totalt.** Detta är ENDAST steg 2 av 4 för de 44 katalograderna — samma
  resultat v5 redan visade för grindnivån, nu korrekt uppdelat i stället för felaktigt
  sammanslaget till en enda "45/45"-siffra.
- **Steg 3 (generatorns kontraktsgrind):** samtliga 45 saknar I DAG en registrerad
  `Tariffpolicy`. `POLICYREGISTER` innehåller i verkligheten TRE poster — Stockholm Exergi
  2025, Stockholm Exergi 2026 och Sandviken; de sex ÖVRIGA redan implementerade
  legacy-produkterna (Göteborg, Gotland ×2, Halmstad, Mölndal, Norrenergi) har INGEN policy
  alls, eftersom de aktiverades före resultatkontraktet fanns och står i
  `LEGACY_UNDANTAGNA_TARIFF_ID`. **Rättat P2 (granskning `2026-09-08-007`, motsade tidigare
  sin egen §6a.4):** slutsatsen är INTE att alla 45 kräver en ny registerpost — Stockholm
  Exergis rad aktiveras inte via katalogvägen alls (§6a.4) och dess ANNUAL-täckning läggs på
  den REDAN BEFINTLIGA `stockholm-exergi-2026`-policyn som en utökning. Rätt räkning: **44
  katalograder kräver EN NY policyregisterpost vardera + 1 (Stockholm) kräver en UTÖKNING av
  en befintlig post.** Detta gäller ÄVEN de 38 av de 42 bandraderna (§6a.2, exklusive
  Stockholm) som inte behöver ytterligare motorarbete, vilket tidigare rundor förväxlade med
  "ingen ny policy krävs". `sundsvall-energi-indal-liden-och-lucksta-2026` är INTE i
  `LEGACY_UNDANTAGNA_TARIFF_ID` (verifierat: bara de sex ursprungliga uppgift-7-tarifferna
  finns i den frozensetten) — v5:s batch 2 hade fått `bygg_ts_fran_katalog()` att kasta om
  den byggts. Sundsvall Indal behöver samma minimala policymekanism som Sandviken
  (`contract_required: true` + en `Tariffpolicy` med `capacity.type: not_applicable`, inga
  kapacitetsbundna krav) — inte legacy-vägen.
- **Steg 4 (minimalt annual_forward-anrop):** kräver att varje rads `Tariffpolicy` faktiskt
  binder ett giltigt, källverifierat leverantörsvärde för samtliga `kravda_falt`. Detta
  steg är i dag OTESTAT för alla 45 — inget skript kördes mot fasaden i denna runda
  eftersom det förutsätter policyregisterposter som ännu inte finns (steg 3). Flaggat
  explicit som ÅTERSTÅENDE arbete i implementationsfasen, inte påstått klart. **Rättat P1
  (granskning `2026-09-08-007`):** ett fälts NUMERISKA gränsvärdestest (t.ex. Umeås
  `B=14`-fall) hör hemma HÄR — i `harled_resultatstatus`/kontraktsfasaden, via `minvarde`/
  `maxvarde` på den bundna `KravPost` — eftersom bara steg 4 faktiskt har en riktig
  `IndataPost` att validera. Steg 3 (den statiska aktiveringsgrinden/`kontrollera_
  kompositgrind`) kan bara bevisa att en BINDNING är deklarerad, aldrig att ett framtida
  KUNDVÄRDE kommer vara giltigt — de två kontrollerna är åtskilda med avsikt, se §6a.3.

**Kontraktstillägg krävda innan steg 3–4 kan bevisas för VISSA rader** — se §6a för den
fullständiga specifikationen:

| Tariff-ID/grupp | Saknat kontraktselement | Se §6a |
|---|---|---|
| **42 rader** — samtliga `ready`-rader UTOM Finspång, Mälarenergi 2–4 lgh och Sundsvall Indal (verifierat mekaniskt mot katalogens `capacity.band_selection`, exakt Codex tal) | `supplier_confirmed_band_id`-bindning: bandvalet ska SJÄLVT peka ut prisraden — `_niva()`s automatiska intervalltolkning får aldrig överpröva ett bekräftat band-ID. Full 42-radslista, mekanism och per-band-ID-data i §6a.2. | 6a.2 |
| `falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo-2026` (en av de 42) | DESSUTOM `KravPost.maxvarde` (500 kW-tak; dagens `KravPost` har bara `minvarde`/`heltal`) — bandkontraktet ensamt räcker inte för Falu ytterorter eftersom källan helt saknar ett publicerat band över 500 kW | 6a.1 |
| `kraftringen-kraftringen-2026` (en av de 42) | DESSUTOM en explicit, typad regelvariant-diskriminator (parametriserad motortyp, inte implicit härledd från leverantörs-ID) — golvbegränsad faktor skild från E.ON/Navirums golvfria formel | 6a.5 |
| `umea-energi-umea-enkel-2026` (en av de 42 — verifierat, har BÅDE `band_selection` och `post_multiplier`) | DESSUTOM namngiven `kapacitet_multiplikator_bindning` för `B`, min/max `[0,93; 1,401]`, egen aktiveringsgrind skild från den strukturella | 6a.3 |
| `stockholm-exergi-stockholm-exergi-normal-2026` (en av de 42 — verifierat, katalograden har `band_selection`, men `energiform` stoppar den strukturellt FÖRE bandkontrollen ens nås) | Bandkontraktet är MOOT för denna rad — den EXKLUDERAS explicit från katalogaktivering, se §6a.4 för vald väg (en konsoliderad policy på leverantörsfilens `stockholm-exergi-2026`, inte katalogaktivering) | 6a.4 |
| Övriga 38 av de 42 band-rader | Bandkontraktet (6a.2) + en ny `Tariffpolicy`-post (steg 3) — inget ytterligare nytt kontraktsfält | 6a.2 |
| `finspangs-tekniska-verk-finspang-2026`, `malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026`, `sundsvall-energi-indal-liden-och-lucksta-2026` | De enda 3 av 45 UTAN `band_selection` — se respektive rads egna motorbehov i tabellen nedan (kapacitetsform/`not_applicable`-mekanism) | — |

**Per-tariffrad, dagens verifierade läge:**

| Tariff-ID | Steg 1–2 idag | Planerad åtgärd (utöver ny policyregisterpost, steg 3) | Berörda filer |
|---|---|---|---|
| `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026` | kapacitetsform | Ny kapacitetsform `heterogeneous_bands` + ny justeringstyp `optional_environmental_addon` (kundvalt UI-tillval) | `katalog.py` (grind), `justeringar.py` + inline i `fjarrvarme.ts`, `KalkylatorPage.tsx` |
| `borlange-energi-borlange-2026` | okänd issue (501 kW) | Normalisera issue; TA BORT R04 (§7); `supplier_confirmed_band_id`-bindning (§6a.2) | katalog-JSON, `resultatkontrakt.py`/`.ts`, `remaining_information_requests` |
| `c4-energi-kristianstad-2026` | okänd issue (500 kW) | Normalisera issue; TA BORT R05 (§7); `supplier_confirmed_band_id`-bindning (§6a.2) | katalog-JSON, `resultatkontrakt.py`/`.ts`, `remaining_information_requests` |
| `e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026` | null i band | fixed:0, rate_period:month; TA BORT normaliserad issue; ny `supply_temperature_adjusted_flow`-motor; TA BORT R10 (§7) | katalog-JSON, `justeringar.py`/`fjarrvarme.ts`, `policyregister.py`, `remaining_information_requests` |
| `e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter-2026` | null i band | Samma som Järfälla bostäder | samma |
| `e-on-malmo-malmo-och-burlov-bostader-2026` | null i band | Samma + Malmö/Burlöv −15→−8 °C rättelse (redan i v4) | samma |
| `e-on-malmo-malmo-och-burlov-ovriga-fastigheter-2026` | null i band | Samma | samma |
| `falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo-2026` | okänd issue (>500 kW) | Normalisera issue; `KravPost.maxvarde=500` (§6a.1); TA BORT R15 (§7) | katalog-JSON, `resultatkontrakt.py`/`.ts`, `remaining_information_requests` |
| `falu-energi-vatten-falun-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `finspangs-tekniska-verk-finspang-2026` | kapacitetsform | Ny kapacitetsform `piecewise_polynomial` + ny justeringstyp `conditional_flow` | `katalog.py`, `justeringar.py`/`fjarrvarme.ts` |
| `habo-energi-habo-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge-2026` | okänd justeringstyp | Ny justeringstyp `flow_difference` | `justeringar.py`/`fjarrvarme.ts` |
| `jamtkraft-brunflo-och-opevagen-2026` | okänd justeringstyp | Samma | samma |
| `jamtkraft-ostersund-froson-as-2026` | okänd justeringstyp | Samma | samma |
| `jonkoping-energi-jonkoping-och-granna-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `karlstads-energi-karlstad-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `kils-energi-kil-2026` | null i band | fixed:0 på alla fyra band; TA BORT normaliserad issue | katalog-JSON |
| `kraftringen-kraftringen-2026` | null i band | fixed:0, rate_period:year; TA BORT normaliserad issue; delad `supply_temperature_adjusted_flow` MED golv (0,2) | katalog-JSON, `justeringar.py`/`fjarrvarme.ts`, `policyregister.py` |
| `lulea-energi-lulea-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `mjolby-svartadalen-energi-mjolby-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader-2026` | null i band | Samma som E.ON | samma |
| `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter-2026` | null i band | Samma | samma |
| `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader-2026` | null i band | Samma | samma |
| `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter-2026` | null i band | Samma | samma |
| `nevel-gimo-osterbybruk-och-osthammar-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `oresundskraft-angelholm-normal-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `oresundskraft-helsingborg-normal-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `ovik-energi-ornskoldsvik-2026` | null i band | fixed:0 på alla band, monthly_proration→kalenderdagsviktning (redan i v4); TA BORT normaliserad issue | katalog-JSON |
| `partille-energi-partille-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `piteenergi-norrfjarden-och-sjulnas-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `piteenergi-pitea-centrala-natet-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `skovde-energi-skovde-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `soderhamn-nara-soderhamn-taxa-11-och-12-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `stockholm-exergi-stockholm-exergi-normal-2026` | energiform | **EXKLUDERAS från aktivering** — se §6a.4. Katalogdubblett av den redan verifierade leverantörsfilsposten `stockholm-exergi-2026`; ID-kollisionsrisken (`_stabilt_tariff_id` ger `stockholm-exergi-stockholm-exergi-normal`) gör att katalogvägen inte väljs i denna plan | `resultatkontrakt.py`/`.ts` (ny adapter på leverantörsfilssidan), `policyregister.py` (`ADAPTERREGISTER`) |
| `sundsvall-energi-indal-liden-och-lucksta-2026` | kapacitetsform | `capacity.type: "not_applicable"` (redan byggd mekanism, oaktiverad); NY minimal `Tariffpolicy` (Sandviken-mönstret, INTE legacy — tariff-ID:t finns inte i `LEGACY_UNDANTAGNA_TARIFF_ID`); TA BORT R14 (§7) | katalog-JSON, `policyregister.py`, `remaining_information_requests` |
| `tekniska-verken-katrineholm-katrineholm-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `tekniska-verken-linkoping-linkoping-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `telge-nat-telge-foretag-och-bostadsrattsforeningar-2026` | okänd issue (inaktuell) | TA BORT issue helt (redan besvarad); TA BORT R11 (§7) | katalog-JSON, `remaining_information_requests` |
| `temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026` | okänd issue | Normalisera issue; TA BORT R12 (§7) | katalog-JSON, `remaining_information_requests` |
| `trollhattan-energi-trollhattan-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |
| `umea-energi-umea-enkel-2026` | kapacitetsformel med multiplikator | Ny `post_multiplier`-medveten kapacitetsmotor; `kapacitet_multiplikator_bindning` för `B` (§6a.3); TA BORT normaliserad issue; ny `asymmetric_flow_difference` | `katalog.py` (grind), `faktura.py`/`fjarrvarme.ts`, `resultatkontrakt.py`/`.ts`, `policyregister.py` |
| `vanerenergi-mariestad-och-toreboda-2026` | passerar redan idag (steg 1–2) | Ny policyregisterpost (steg 3), inget motorarbete | `policyregister.py` |

**Metodnot (bekräftad på nytt i v6):** att lösa den FÖRSTA grindorsaken avslöjar ibland en
ANDRA, tidigare dold bakomliggande orsak — 13 av de 45 raderna hade en YTTERLIGARE `okänd
issue`- eller `okänd justeringstyp`-blockering bakom den förstnämnda (t.ex. samtliga åtta
E.ON/Navirum-rader hade, utöver `null i band`, en andra issue-text om effektprisperiod/
flödeskorrigering). Tabellen ovan är uppdaterad för BÅDA leden.

**Känd avvikelse (Lidköping, historik t.o.m. v15 — LÖST i v16, bedömning `2026-09-09-006`):**
`lidkoping-energi-lidkoping-041-kw-2026` och `-42-kw-2026` (nu `ready_to_implement`, §4.2)
passerade MEKANISKT `grind()` (steg 2) redan i v15 när `investigation.status` simulerades
löst — deras `issues`-texter matchade redan kända, godkända mönster. De förblev ändå
KORREKT blockerade t.o.m. v15: den publika källan saknade HELT 2026 års flödesprisfaktor N
och nätmedelvärde Tm — ett verkligt prissättande fält som aldrig kodats som en
`adjustments`-post i katalogen och som varken `grind()` eller den sammansatta preflighten
strukturellt kan upptäcka utan att fältet finns i JSON. Lidköping Energis skriftliga
leverantörssvar 2026-09-09 (bedömning `2026-09-09-006`, §6a.7) löser nu den externa
sakfrågan: `N = 5 kr/m³` och hur `Tm` bestäms är källbelagda. Iakttagelsen om att
mekaniska/strukturella kontroller INTE ensamma räcker för att upptäcka ett fält som saknas
helt i JSON-katalogen kvarstår som en generell lärdom — ett mänskligt omdöme om KÄLLANS
fullständighet krävs alltid utöver den maskinella kedjan, det var bara ETT specifikt
fall (just Lidköping) som är löst.

## 6a. Kontraktstillägg som krävs (granskning 2026-09-08-005/-006/-007, P1)

Fyra nya bindningar krävs i policykontraktet innan de rader som är beroende av dem kan bevisa
steg 3–4 (§6). Samtliga speglar det redan etablerade mönstret från Sandvikens
`minvarde`/`heltal`-tillägg (samma session, tidigare runda) — generiska, deklarativa fält på
`KravPost`/`Tariffpolicy`, kontrollerade av den delade fasaden i BÅDA språken, aldrig
hårdkodade mot ett enskilt tariff-ID i motorn.

### 6a.1 `KravPost.maxvarde` (mirror av `minvarde`)

Python (`resultatkontrakt.py`, `KravPost`): nytt fält `maxvarde: float | None = None`,
validerat i `__post_init__` (ändligt tal) och kontrollerat i `harled_resultatstatus` bredvid
den befintliga `minvarde`-kontrollen (`post.varde > f.maxvarde` → `raise ValueError`).
TypeScript-spegel: `maxVarde?: number` på `KravPost`-interfacet, samma kontroll i
`harledResultatstatus`. `_policy_till_json`/`dataclasses.asdict` behöver ingen ändring på
PYTHON-JSON-sidan — det nya fältet serialiseras automatiskt, precis som `minvarde`/`heltal`
gjorde för Sandviken.

**Tillägg, granskning `2026-09-09-010` (§6a.7.5): `KravPost.minvarde_exklusiv`.** Samma
mönster som `maxvarde` ovan: nytt fält `minvarde_exklusiv: bool = False` (Python)/
`minExklusiv?: boolean` (TS), FÅR bara vara satt (`True`/`true`) tillsammans med
`minvarde`/`minVarde` — `__post_init__`/`skapaKravPost` kastar annars
(`ValueError`/`Error`: "minvarde_exklusiv kräver att minvarde också är satt").

**Rättat P1 (granskning `2026-09-09-011`) — kontrollen jämförde en HEL `number_series` mot
gränsen som om den vore ett tal.** v17 skrev kontrollen som `post.varde < f.minvarde`
oavsett fälttyp. I den verkliga `harledResultatstatus`/`harled_resultatstatus` körs dagens
`minvarde`/`heltal`-kontroll bara inuti `if (!arSerie(post.varde))`
(TypeScript rad 412–421)/`if not _ar_serie(post.varde):` (Python rad 436–445) — en rak
implementation av v17:s text hade alltså antingen gett en ogiltig array–tal-jämförelse eller
tyst hoppat över precis de serie-fält (`Tm_m`/`T_m`/`Q_m`) kontrollen är till för. Löst med
EN delad, elementvis hjälpfunktion som körs för BÅDA formerna (skalär eller serie), i BÅDA
validatorerna (`harledResultatstatus`/`harled_resultatstatus` OCH
`forkontrolleraPolicyIndata`s fältnära motsvarighet, §6a.2) och BÅDA språken.

**Rättat P1 (granskning `2026-09-09-012`) — ägare/importväg var oangiven och byggde på en
privat funktion.** v18 skrev bara kommentaren "`besparingsvarde.ts / resultatkontrakt.ts` —
delad av båda validatorerna" utan att ange VILKEN av de två filerna som äger funktionen. Den
använder `arSerie`, som i den verkliga `resultatkontrakt.ts:67` är en modulprivat (icke
exporterad) funktion — `besparingsvarde.ts` kan alltså inte importera en `vardefelForKrav`
som i sin tur anropar `arSerie` om `vardefelForKrav` låg i `besparingsvarde.ts`. Exakt EN
ägare, ingen importcykel:

- **TypeScript:** `vardefelForKrav` definieras och EXPORTERAS i `resultatkontrakt.ts`
  (samma fil som redan äger `arSerie`, `harledResultatstatus` och `KravPost`), och
  `besparingsvarde.ts` importerar den i sin befintliga importrad:
  `import { beraknaArskostnadMedKontrakt, policyFranGenererad, vardefelForKrav, type
  IndataPost, type Resultatstatus, type Tariffpolicy } from './resultatkontrakt';` — samma
  riktning `besparingsvarde.ts` redan importerar `beraknaArskostnadMedKontrakt` från, alltså
  ingen ny beroenderiktning och ingen cykel.
- **Python:** `_vardefel_for_krav` definieras i `resultatkontrakt.py` och den planerade
  `forkontrollera_policy_indata`-motsvarigheten (§6a.2) läggs i SAMMA fil, inte i en separat
  modul — enda Python-produktmodulen som idag känner till `KravPost`/`Tariffpolicy` är
  `resultatkontrakt.py` själv (`policyregister.py` bygger policyer men importerar
  valideringslogik FRÅN `resultatkontrakt.py`, aldrig tvärtom), så en enda-fil-lösning har
  inget korsimportsproblem att undvika. Namnet behåller sitt enkla understreck (modulprivat
  konvention, inte språkligt tvingande) eftersom ingen extern modul behöver importera den.

```ts
// resultatkontrakt.ts — enda ägare; exporteras och importeras av besparingsvarde.ts
export function vardefelForKrav(f: KravPost, varde: Varde): PolicyValideringsOrsak | null {
  const varden: readonly number[] = arSerie(varde) ? varde : [varde];
  for (const v of varden) {
    if (f.heltal && !Number.isInteger(v)) return 'heltal';
    if (f.minVarde !== undefined) {
      const brott = f.minExklusiv ? !(v > f.minVarde) : v < f.minVarde;
      if (brott) return 'min';
    }
    if (f.maxVarde !== undefined && v > f.maxVarde) return 'max';
  }
  return null;
}
```

```python
# resultatkontrakt.py — enda ägare; harled_resultatstatus och den nya
# forkontrollera_policy_indata definieras i SAMMA modul, ingen import behövs
def _vardefel_for_krav(f: KravPost, varde: Varde) -> str | None:
    varden = varde if _ar_serie(varde) else [varde]
    for v in varden:
        if f.heltal and not float(v).is_integer():
            return "heltal"
        if f.minvarde is not None:
            brott = not (v > f.minvarde) if f.minvarde_exklusiv else v < f.minvarde
            if brott:
                return "min"
        if f.maxvarde is not None and v > f.maxvarde:
            return "max"
    return None
```

`vardefelForKrav`/`_vardefel_for_krav` ersätter de tidigare separata, guardade
`if (!arSerie(...))`-blocken i `harledResultatstatus`/`harled_resultatstatus` — anropas
UTAN den villkorliga arSerie-spärren, så samma regel gäller nu identiskt för ett skalärt
`Tf`-krav och Lidköpings tolvelements `Tm_m`-serie. `forkontrolleraPolicyIndata`s fältnära
`ogiltiga`-uppbyggnad (§6a.2) anropar SAMMA funktion i stället för att duplicera logiken,
så UI-förkontrollen och ett direkt fasadanrop ger identiskt `orsak`. Används av Lidköpings
`Tm_m`-krav (`minVarde: 0, minExklusiv: true`, §6a.7.5) — första fältet i katalogen som
behöver en strikt undre gräns PÅ ETT SERIEFÄLT. Isolerat compile-verifierad (`npx tsc
--noEmit --strict --skipLibCheck --target es2020`, kontrollfil i `/tmp`, borttagen efter
körning), testat både via `forkontrolleraPolicyIndata` (UI-förkontroll) OCH via ett direkt
`beraknaArskostnadMedKontrakt`-anrop som kringgår UI:t (§6a.7.5 nedan för testlistan):
`[-1, 5, 5, ...]` (ett negativt element bland elva giltiga) → `'min'`; en serie med `0` på
en enda av tolv månader (`minExklusiv: true`) → `'min'`; samma serie med `0` på ett vanligt
`minVarde: 0`-fält (`minExklusiv` osatt) → OK; en serie med bara positiva tal → OK i båda
fallen.

**Rättat P1 (granskning `2026-09-08-006`):** TypeScripts `policyFranGenererad()`
(`resultatkontrakt.ts`) mappar KravPost-fälten FÖR HAND (verifierat genom att läsa
funktionen) — den läser i dag `minvarde`/`heltal` från den genererade JSON:en men INTE
`maxvarde`. Utan en explicit rad `maxVarde: k.maxvarde` i den mappningen skulle Falus
500 kW-gräns serialiseras korrekt av Python men tyst försvinna i frontend. Samma explicita
mappningsrad krävs för VARJE nytt fält i denna sektion — automatisk TypeScript-mappning
finns inte, den måste skrivas för hand varje gång:

| Python-fält (`KravPost`/`Tariffpolicy`) | JSON-namn (genererad fil) | TypeScript-fält | Krävd rad i `policyFranGenererad()` |
|---|---|---|---|
| `KravPost.maxvarde` | `maxvarde` | `KravPost.maxVarde` | `maxVarde: k.maxvarde ?? undefined` (rättat P1, granskning `2026-09-09-002`: föregående rad saknade null-normaliseringen alla andra optionella fält i denna tabell redan har, vilket hade kunnat föra igenom ett bokstavligt `null` i stället för `undefined`) |
| `KravPost.vardetyp` (§6a.2) | `vardetyp` | `KravPost.vardetyp` | `vardetyp: k.vardetyp ?? 'number'` |
| `KravPost.antal_varden` (§6a.2, nytt granskning `2026-09-08-008`) | `antal_varden` | `KravPost.antalVarden` | `antalVarden: k.antal_varden ?? undefined` |
| `KravPost.tillatna_varden` (§6a.6) | `tillatna_varden` | `KravPost.tillatnaVarden` | `tillatnaVarden: k.tillatna_varden ?? undefined` |
| `KravPost.minvarde_exklusiv` (§6a.1, nytt granskning `2026-09-09-010`) | `minvarde_exklusiv` | `KravPost.minExklusiv` | `minExklusiv: k.minvarde_exklusiv ?? undefined` |
| `Tariffpolicy.kapacitet_band_bindning` (§6a.2) | `kapacitet_band_bindning` | `Tariffpolicy.kapacitetBandBindning` | `kapacitetBandBindning: json.kapacitet_band_bindning ?? undefined` |
| `Tariffpolicy.kapacitet_multiplikator_bindning` (§6a.3) | `kapacitet_multiplikator_bindning` | `Tariffpolicy.kapacitetMultiplikatorBindning` | `kapacitetMultiplikatorBindning: json.kapacitet_multiplikator_bindning ?? undefined` |
| `Tariffpolicy.flodeskorrigering_variant` (§6a.5) | `flodeskorrigering_variant` | `Tariffpolicy.flodeskorrigeringVariant` | `flodeskorrigeringVariant: json.flodeskorrigering_variant ?? undefined` |
| `Tariffpolicy.kallenergi_arsserie_bindning` (§6a.4, nytt granskning `2026-09-08-008`) | `kallenergi_arsserie_bindning` | `Tariffpolicy.kallenergiArsserieBindning` | `kallenergiArsserieBindning: json.kallenergi_arsserie_bindning ?? undefined` |
| `Tariffpolicy.stodjer_aktuell_arskostnad` (§6a.4, nytt granskning `2026-09-09-010`) | `stodjer_aktuell_arskostnad` | `Tariffpolicy.stodjerAktuellArskostnad` | `stodjerAktuellArskostnad: json.stodjer_aktuell_arskostnad ?? false` |
| `Tariffpolicy.returtemperatur_arsserie_bindning` (§6a.4, nytt granskning `2026-09-08-008`) | `returtemperatur_arsserie_bindning` | `Tariffpolicy.returtemperaturArsserieBindning` | `returtemperaturArsserieBindning: json.returtemperatur_arsserie_bindning ?? undefined` |
| `KravPost.etikett` (§6a.2, nytt granskning `2026-09-08-009`) | `etikett` | `KravPost.etikett` | `etikett: k.etikett` (kastar i `policyFranGenererad` om `undefined` — fail-closed, `etikett` är obligatoriskt satt av `policyregister.py` på varje krav) |
| `KravPost.hjalptext` (§6a.2, nytt granskning `2026-09-08-009`) | `hjalptext` | `KravPost.hjalptext` | `hjalptext: k.hjalptext` (samma fail-closed-krav som `etikett`) |
| `Tariffpolicy.ersatter_katalograd` (§6a.4, nytt granskning `2026-09-08-009`) | `ersatter_katalograd` | `Tariffpolicy.ersatterKatalograd` | `ersatterKatalograd: json.ersatter_katalograd ?? undefined` |
| `Tariffpolicy.stodjer_besparing` (§6a.4, nytt granskning `2026-09-09-012`, P1) | `stodjer_besparing` | `Tariffpolicy.stodjerBesparing` | `stodjerBesparing: json.stodjer_besparing ?? false` — FAIL-CLOSED default, se §6a.4: en policy som saknar fältet i genererad JSON ger `stodjerBesparing === false`, aldrig `undefined` tolkat som tillåtet |
| `KravPost.krav_attestering` (§6a.7.6, nytt granskning `2026-09-09-012`, P1) | `krav_attestering` | `KravPost.kravAttestering` | `kravAttestering: k.krav_attestering ?? false` — samma fail-closed-mönster: ett krav utan explicit attesteringsflagga kräver INGEN attestering (skiljer sig från `etikett`/`hjalptext`, som i stället kastar) |

Negativa test krävs för samtliga SEXTON fält ovan (rättat räkning, granskning
`2026-09-09-012`, P1 — v18 sa "fjorton" och saknade två av dem): en genererad policy med
fältet satt som TypeScript läser tillbaka korrekt (inte `undefined`), och en policy UTAN
fältet som fortsatt ger `undefined` (inte t.ex. tomsträng eller `null` feltolkat som ett
giltigt bandval) — utom `etikett`/`hjalptext`, som är OBLIGATORISKA på varje `KravPost` och
därför testas med ett kastat fel vid genereringstillfället i stället för ett tillåtet
`undefined`-fall, och utom `stodjer_besparing`/`krav_attestering`, vars frånvaro INTE ger
`undefined` utan det explicita, fail-closed default-värdet `false` — testa uttryckligen att
frånvaro ger `false` (inte `undefined`, inte kastat fel).

**Kompletta konstruktionskedjan för de två säkerhetskritiska fälten (rättar P1, granskning
`2026-09-09-012`, punkt 1 — hela kedjan Python-dataklass → JSON → TypeScript-interface →
`policyFranGenererad()` → `skapaTariffpolicy()`s options OCH returvärde → `PolicyFaltMetadata`,
inte bara raden i transporttabellen ovan):**

1. **Python-dataklass** (`resultatkontrakt.py`): `Tariffpolicy.stodjer_besparing: bool = False`
   och `KravPost.krav_attestering: bool = False` — samma explicita `False`-default i Python
   som i TypeScript-mappningen, så genereringen aldrig producerar ett fält vars frånvaro
   betyder något annat än "nej".
2. **Genererad snake_case-JSON** (`generera.py`s `dataclasses.asdict`): fälten serialiseras
   som `stodjer_besparing`/`krav_attestering` precis som alla andra `Tariffpolicy`/`KravPost`-
   fält — ingen särbehandling i generatorn.
3. **TypeScript-interface** (`resultatkontrakt.ts`): `Tariffpolicy.stodjerBesparing?: boolean`
   läggs till i `Tariffpolicy`-interfacet (nuvarande fält: `tariffId`, `kravdaFalt`,
   `tackning`, `kapacitetBindning`, `kallenergiBindning`, `returtemperaturBindning`);
   `KravPost.kravAttestering?: boolean` läggs till i `KravPost`-interfacet på samma sätt som
   `minVarde`/`heltal` idag.
4. **`policyFranGenererad()`** (rad ~247 i dagens `resultatkontrakt.ts`, i `kravdaFalt`-
   mappningen): ny rad `kravAttestering: k.krav_attestering ?? false` bredvid `heltal: k.heltal
   ?? false`. I `skapaTariffpolicy`-anropet: ny rad `stodjerBesparing: json.stodjer_besparing ??
   false` bredvid `kapacitetBindning`/`kallenergiBindning`/`returtemperaturBindning`.
5. **`skapaTariffpolicy()`s options-typ OCH returvärde** (rad ~187–225 i dagens
   `resultatkontrakt.ts`) — den plats v18 helt missade: dagens funktionssignatur
   ```ts
   export function skapaTariffpolicy(
     tariffId: string,
     kravdaFalt: readonly KravPost[],
     opts: {
       tackning?: readonly Tackningsomrade[];
       kapacitetBindning?: string;
       kallenergiBindning?: string;
       returtemperaturBindning?: string;
     } = {}
   ): Tariffpolicy
   ```
   får ett nytt fält i `opts`: `stodjerBesparing?: boolean;`. Returobjektet
   `{ tariffId, kravdaFalt, tackning, kapacitetBindning, kallenergiBindning,
   returtemperaturBindning }` får motsvarande rad: `stodjerBesparing: opts.stodjerBesparing ??
   false`. Utan denna ändring skulle `policyFranGenererad()` kunna skicka
   `stodjerBesparing: true` i sitt anrop, men `skapaTariffpolicy()` skulle tyst kasta bort det
   eftersom options-typen inte känner igen fältet och TypeScripts strukturella typning inte
   klagar på ett extra objektfält i ett vanligt (icke-`exactOptionalPropertyTypes`-strikt)
   anrop — motsvarande Python-konstruktören (`Tariffpolicy.__init__`/dataklassfält) behöver
   samma fält på samma sätt.
6. **`KravPost`-konstruktören `skapaKravPost()`** (rad ~120–150): motsvarande passthrough,
   `kravAttestering` läggs bara till i returtypen (inget separat valideringsvillkor behövs —
   ett booleskt fält utan gräns/enum har ingen konstruktionsvalidering att lägga till).
7. **`PolicyFaltMetadata`** (§6a.2, den UI-riktade listan `policyFaltMetadata()` bygger):
   ny egenskap `kravAttestering: boolean` i formen, satt från `f.kravAttestering ?? false` för
   varje krav — se §6a.7.6 nedan för hur UI:t använder den.

**Negativa transporttester (nya, krävda av granskning `2026-09-09-012`):** (a) en genererad
policy med `stodjer_besparing=True` i Python ger `policy.stodjerBesparing === true` i
TypeScript efter `policyFranGenererad()` — inte `undefined`; (b) en genererad policy UTAN
fältet ger `policy.stodjerBesparing === false` — inte `undefined`, som annars skulle tolkas
som "tillåtet" av en naiv `!== false`-resolver (se §6a.4:s fail-closed-resolver nedan); (c)
motsvarande par för `krav_attestering` på ett enskilt `KravPost`; (d) ett direkt
`skapaTariffpolicy(id, falt, {})`-anrop UTAN `stodjerBesparing` i `opts` ger
`policy.stodjerBesparing === false` — bevisar att fail-closed-defaulten sitter i
konstruktören själv, inte bara i `policyFranGenererad()`s anropsplats.

**Används av:** `falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo-2026`
(`maxvarde=500` på dess `debiterbar_effekt_kw`-krav) — mekaniskt fail-closed i stället för
att förlita sig på att `_niva()` råkar kasta `ValueError` för värden utan täckande band.

**Ny typ `GenereradPrisarspost` (rättat P2, granskning `2026-09-09-004`): tidigare bara
använd, aldrig definierad.** Varje avsnitt i §6a refererar `prisar: GenereradPrisarspost`,
men ingen av de föregående versionerna (v9–v13) deklarerade typen — den dagens verkliga kod
har på just den positionen är `any` (`LeverantorOchPrisar.prisar: any` i `besparingsvarde.ts`,
oförändrat sedan innan denna etapp). Det finns alltså ingen befintlig härledd pristyp att
återanvända; `GenereradPrisarspost` är en NY, explicit `interface` som denna etapp inför,
begränsad till exakt de fält §6/§6a:s funktioner faktiskt läser — den ersätter `any` på just
dessa signaturer utan att röra `LeverantorOchPrisar`s befintliga, oförändrade typ någon
annanstans i koden:

```ts
// resultatkontrakt.ts, ny exporterad typ
export interface GenereradPrisarspost {
  tariff_id: string;
  ar: number;
  _kraver_kontrakt?: boolean;
  policy?: unknown; // rå, ännu odeserialiserad JSON — policyFranGenererad() läser denna
  kapacitet?: { nivaer?: readonly { id?: string; min: number; max: number | null }[] };
}
```

Samtliga nya funktioner i §6a (`policyFaltMetadata`, `forkontrolleraPolicyIndata`,
`stodjerAktuellArskostnad`, `byggIndataFranPolicy`, `beraknaArsprodukt`) tar denna typ i
stället för `any` — en strikt SKÄRPNING av dagens signatur, inte en breddning, eftersom
`any` redan tillåter allt `GenereradPrisarspost` tillåter. Ingen befintlig anropare bryts:
`prisar`-objekt som redan flyter genom `valjLeverantorOchPrisar()` bär redan alla dessa fält
i praktiken (verifierat mot `tariffer.generated.ts`s faktiska struktur), typen bara namnger
vad som redan är sant.

### 6a.2 `supplier_confirmed_band_id`-bindning (omkonstruerad, granskning 2026-09-08-006, P1)

**Rättat designfel (P1):** v6:s design bekräftade ett band-ID och kastade sedan om det
INTE stämde med vad `_niva()` skulle ha valt automatiskt — vilket gör leverantörens besked
verkningslöst i EXAKT de tvetydiga gränsfall bindningen finns till för att lösa (dagens
autoväljare tar Borlänge band 5 vid 501 kW och C4 band 6 vid 500 kW; om leverantören
bekräftar ett ANGRÄNSANDE band skulle v6:s design felaktigt blockera det korrekta beskedet
i stället för att använda det). Det bekräftade band-ID:t ska i stället VÄLJA prisraden
direkt.

**Katalogens normativa kontrakt (ordagrant, `optimate-fjarrvarme-2026.json`s
integrationsanvisning):** *"Originalintervall bevaras. Välj `supplier_confirmed_band_id`;
intervallsträngar får inte automatiskt parsas till produktionsgränser."* — detta gäller inte
bara Borlänge/C4 utan samtliga rader vars `capacity.band_selection` är
`supplier_confirmed_band_id_required`.

**Omfattning, verifierad mekaniskt mot den checkade-in katalogen (skrivskyddat script,
`enkey-agents@fd8f8da`):** exakt **42 av de 45 `ready`-raderna** bär markören — de enda tre
undantagen är `finspangs-tekniska-verk-finspang-2026`,
`malarenergi-vasteras-och-hallstahammar-24-lagenheter-2026` (ingen kapacitetsdel) och
`sundsvall-energi-indal-liden-och-lucksta-2026` (ren energitariff). v6 specificerade bara
Borlänge/C4 och kallade detta "en ny policy räcker" för resten — fel, se §6-tabellen ovan.

**Diskriminerad värdetyp — INTE en global vidgning av `Varde` (rättat P1, granskning
`2026-09-08-007`):** v7:s `Varde = float | Sequence[float] | str` skulle ha försvagat VARJE
befintligt numeriskt fält samtidigt — verifierat att `_validera_varde`/`valideraVarde`
(resultatkontrakt.py/.ts) i dag avvisar varje sträng, att kontraktsfasaden gör
`float(post.varde)` för varje relevant skalär, att TypeScript lägger varje sådan post i
`Record<string, number>`, och att kalkylatorsidan konverterar med `parseFloat`. En global
strängtillåtelse hade tyst öppnat alla dessa vägar för ogiltig indata, inte bara bandfältet.

Nytt `KravPost`-fält `vardetyp: Literal["number", "number_series", "band_id"] = "number"`
(mirror `vardetyp?: 'number' | 'number_series' | 'band_id'` i TS, default `'number'` för
bakåtkompatibilitet med alla befintliga krav). `__post_init__`/`skapaKravPost` validerar:
`vardetyp == "band_id"` FÖRBJUDER `minvarde`/`maxvarde`/`heltal`/`tillatna_varden` (§6a.6) på
samma post — ett band-ID har ingen numerisk gräns.

**Rättat P1 (granskning `2026-09-08-008`) — `vardetyp` på `KravPost` räcker inte ensamt:**
`IndataPost.varde` (`resultatkontrakt.py`/`.ts`) är fortfarande typad `Varde = float |
Sequence[float]` (Python) / `number | readonly number[]` (TypeScript) — verifierat genom att
läsa typdefinitionen. En `band_id`-post med strängvärde kan alltså INTE konstrueras
typkorrekt utan att `IndataPost.varde`s egen typ också utökas. Fixet lägger till en NY typ
för `IndataPost.varde` specifikt (se P2-rättningen nedan för varför `Varde` självt inte
vidgas):

- **Rättat P2 (terminologikrock, granskning `2026-09-08-009`):** v8/v9 sa "inte en global
  vidgning" men definierade sedan om SAMMA delade `Varde`-alias till att inkludera `str` —
  verifierat att `Varde` (`resultatkontrakt.py:120`/`resultatkontrakt.ts:65`) redan är
  parametertypen för `_validera_varde`/`valideraVarde` SJÄLVA (den generiska numeriska
  validatorn, oberoende av `IndataPost`) — en omdefiniering av `Varde` hade alltså bokstavligen
  vidgat den funktionens egen signatur, även om `_validera_varde`s KROPP fortsatt skulle
  avvisa `str` vid anrop. Löst genom att INTE röra `Varde` alls — `Varde` förblir exakt
  `float | Sequence[float]` (Python) / `number | readonly number[]` (TypeScript), oförändrad,
  och är fortsatt den enda typ `_validera_varde`/`valideraVarde` accepterar. En NY, separat
  typ bär bandvärdet: Python `IndataVarde = Varde | str` (bara på `IndataPost.varde`s egen
  typannotering, `Varde` självt orört); TypeScript `IndataVarde = Varde | string` (samma
  princip, exporterad separat i `resultatkontrakt.ts`). `KravPost` fortsätter sakna `str` i
  sin egen typannotering av vad ett krav KAN uttrycka numeriskt, eftersom kravet inte bär ett
  värde, bara en beskrivning av vilket värde det förväntar sig.
- `harled_resultatstatus`/`harledResultatstatus` grenar på `f.vardetyp` INNAN den anropar
  `_validera_varde`/`valideraVarde`: för `"band_id"` kräver den att `post.varde` är en
  icke-tom `str` (kastar annars, kastar även om ett tal skickas som "band-ID") — bandkravet
  hamnar alltså ALDRIG i vägen för `_validera_varde`s numeriska kontroll, som bara anropas
  för `"number"`/`"number_series"`-fält, där `post.varde` (trots sin bredare `IndataVarde`-
  deklaration) alltid faktiskt är av typen `Varde` vid den punkten — verifierat genom
  grenlogikens ordning, inte genom att vidga vad `_validera_varde` självt accepterar.
- **`number_series` görs till en verklig diskriminator, inte bara en tillåten möjlighet
  (rättat P1, granskning `2026-09-08-008`):** verifierat att dagens `rullande=True` TILLÅTER
  en serie men INTE KRÄVER en — ett fält märkt `number_series` kunde alltså fortfarande få
  ett bart skalärt tal genom, medan `"number"` bara avvisade en serie via en separat
  `rullande`-kontroll på ANNAT håll i koden. `harled_resultatstatus`/`harledResultatstatus`
  kräver nu explicit, i samma `vardetyp`-gren: `"number"` → `post.varde` MÅSTE vara ett
  skalärt ändligt tal (kastar om det är en `Sequence`/array); `"number_series"` → `post.varde`
  MÅSTE vara en icke-tom `Sequence`/array av ändliga tal (kastar om det är ett bart skalärt
  tal). E.ON/Navirums rullande men SKALÄRA leverantörseffekt (ett enda tal, uppdaterat en
  gång per kalenderår — se `rullande=False`-kommentaren i `policyregister.py` från
  Sandviken-etappen) förblir korrekt modellerad som `vardetyp="number", rullande=True` — inte
  genom att låta `"number_series"` acceptera ett skalärt värde som en genväg.
- **Nytt kardinalitetsfält `KravPost.antal_varden: int | None = None`** (mirror
  `antalVarden?: number` i TS) — deklarativt, GENERISKT (ingen fältnamns- eller
  tariff-specifik hårdkodning i valideraren): satt bara meningsfullt tillsammans med
  `vardetyp="number_series"`, kastar i `__post_init__`/`skapaKravPost` om satt på
  `"number"`/`"band_id"`. `harled_resultatstatus`/`harledResultatstatus` kräver, när satt,
  `len(post.varde) == f.antal_varden` exakt — annars kastar (fel längd är ett strukturellt
  indatafel, inte ett "nästan rätt"-läge som ska accepteras). Stockholms kallenergiserie
  sätter `antal_varden=12`, returtemperaturserien `antal_varden=5` (§6a.4) — det generiska
  fältet uttrycker BÅDA utan att motorn känner till "Stockholm" eller "12"/"5" som
  hårdkodade konstanter någonstans i valideraren själv.

**Mekanism (Python `resultatkontrakt.py`/`katalog.py`/`faktura.py`, TS-speglar likadant):**

1. `till_prisar()` (`katalog.py`) bevarar källans `band["id"]` in i varje `nivaer`-post:
   `{"id": band.get("id"), "min": ..., "max": ..., "avgift_kr_ar": ..., "pris_kr_per_enhet_ar": ...}`
   — i dag tappas `id` helt (verifierat genom att läsa funktionen, se §4 P1-citaten).
2. Nytt `Tariffpolicy`-fält `kapacitet_band_bindning: str | None = None` (mirror
   `kapacitetBandBindning?: string` i TS) pekar ut vilket krävt fält (en NY, separat
   `KravPost`, t.ex. `nyckel="effektband_id"`, `vardetyp="band_id"`) som bär det
   leverantörsbekräftade band-ID:t. Skilt från det befintliga numeriska fältet bakom
   `kapacitet_bindning` — bandvalet och det numeriska debiteringsunderlaget är två oberoende
   krävda fält, och den delade fasadens `falt`-uppbyggnad SKA uttryckligen hoppa över
   `policy.kapacitet_band_bindning` när den bygger den numeriska `falt`-dictionaryn (samma
   mönster som den redan hoppar över `kb`/`policy.kapacitet_bindning` i dag) — ett
   band-ID får aldrig försöka bli `float(...)`.
3. Ny fasadparameter i den lågnivåkoden `arskostnad`/`manadskostnad`
   (`faktura.py`/`fjarrvarme.ts`): `vald_niva_id: str | None = None`. När satt, hoppar
   motorn över `_niva()`s automatiska intervall-uppslagning HELT och använder i stället
   `next(n for n in nivaer if n["id"] == vald_niva_id)` — kastar `ValueError` om ID:t inte
   finns bland `prisar.kapacitet.nivaer`. Kontraktsfasaden
   (`beräkna_arskostnad_med_kontrakt`/`beraknaArskostnadMedKontrakt`) läser
   `indata[policy.kapacitet_band_bindning].varde` och skickar det vidare som
   `vald_niva_id` när `kapacitet_band_bindning` är satt på policyn — annars oförändrat
   beteende (`_niva()` auto-väljer, som i dag, för de tre rader som saknar markören).
4. `_niva()` självt ändras INTE — den fortsätter vara den automatiska fallback-vägen för
   allt som inte har en `supplier_confirmed_band_id`-bindning.
5. Saknat, tomt eller okänt band-ID på en markerad tariff BLOCKERAR
   (`harled_resultatstatus` avvisar via samma mekanism som andra saknade obligatoriska
   fält) — gissas aldrig.

**Grundarbete: en gemensam produktingång för ALLA policykrav (nytt P1, granskning
`2026-09-08-007`) — inte bara kapacitet.** Verifierat genom att läsa
`beraknaBesparingsvardeKontrakt` (`besparingsvarde.ts`): den bygger i dag `IndataPost` ENDAST
för `policy.kapacitetBindning`. Varje policy med ett band-, flödes-, temperatur-, B- eller
annat extra krav utöver kapacitet ger därför i dag ett `blocked`-resultat som (per den
befintliga felhanteringen där `beraknaBesparingsvardeKontrakt` tolkar ETT oväntat
`blocked`-fynd som ett konfigurationsfel) skulle kasta i stället för att räkna — detta gäller
ALLA 41 av de 45 `ready`-raderna som har mer än ett krävt fält, inte bara bandraderna.

Detta MÅSTE lösas som grundarbete FÖRE första tariffbatchen (ny batch 0, se
`batchplan-v14.md`), inte något Sandvikens nuvarande kapacitets-only-adapter redan täcker:

1. **Rättat P1 (granskning `2026-09-08-009`) — separat, typad produkt-DTO i stället för att
   återanvända det numeriska `falt`-objektet.** Verifierat genom att läsa den verkliga koden
   att detta INTE redan var löst: `KalkylatorPage.tsx` bygger `faltForBerakning: Record<string,
   number>` från formulärets råa `Record<string, string>`-tillstånd via `Number.isFinite`/
   `parseFloat` INNAN något skickas vidare; `KalkylatorInputs.falt` och
   `BesparingsvardeArgs.falt` är fortfarande `Record<string, number>` i den checkade-in
   koden. Den befintliga `falt`-kedjan är och FÖRBLIR numerisk-only — den bär i dag Gotlands
   `foregaende_ars_mwh`, returtemperaturavvikelser m.fl. fria fakturafält för LEGACY-vägens
   (icke-kontraktsgated) `arskostnad()`-anrop, och rörs INTE av detta tillägg.

   **Rättat P1 (granskning `2026-09-09-001`) — rått formulärstate skilt från den parsade
   DTO:n; v10 lät dem VARA samma typ.** v10:s `Record<string, PolicyInputValue>` som
   React-state antog att talkonvertering sker "vid inskick", men ett HTML `<input
   type="number">` bär en STRÄNG i varje render medan användaren skriver — en delvis ifylld
   serie är alltså `string[]` under hela ifyllnaden, ett värde `PolicyInputValue` (`number |
   string | readonly number[]`) inte kan representera typkorrekt. Skulle implementationen
   köra `Number(...)` per ruta ÄNDÅ (t.ex. vid varje `onChange` i stället för vid submit)
   uppstår ett fail-open-hål: `Number('')` och `Number('   ')` är båda `0` i JavaScript — en
   tom eller delvis tom serie med rätt antal UI-rutor skulle då tyst bli en komplett
   `number[]` av nollor, passera både ändlighets- och `antalVarden`-kontrollen, och påverka
   kostnaden som om kunden uttryckligen rapporterat noll. Det motsäger punkt 3 nedan, som
   kräver att en delvis ifylld serie ger ett fältnära användarfel, inte en tyst nolla.

   Samma stycke i v10 sa dessutom att BÅDE band-ID och enum ska skickas som oförändrade
   strängar — men Jönköpings allow-list (§6a.6) är uttryckligen NUMERISK:
   `tillatna_varden: tuple[float, ...]`/`tillatnaVarden?: readonly number[]`, med exakt
   medlemskap mot `0`/`10`/`25`/`50`. Ett val UI:t skickar som strängen `"10"` skulle avvisas
   av ett `number`-krav som jämför mot talet `10`. Band-ID och Jönköpings enum kan alltså
   INTE dela regeln "parsas aldrig" — bara band-ID är genuint sträng-typat.

   **Löst med två separata typer:**
   - `PolicyRawFormValue = string | readonly string[]` (`resultatkontrakt.ts`) — det RÅA
     React-state-formatet. `KalkylatorPage.tsx` får ett NYTT state `policyFaltRavarden:
     Record<string, PolicyRawFormValue>` (skilt från BÅDE det befintliga
     `faltVarden: Record<string, string>` OCH det parsade `policyFalt` nedan): ett skalärt
     fält (number/band_id/enum) är en enskild sträng, ett `number_series`-fält är en
     `readonly string[]` med exakt `antalVarden` rutor (en sträng per seriemånad, tom sträng
     tills ifylld — INGEN `Number()`-konvertering sker i state-uppdateringen).
   - `PolicyInputValue = number | string | readonly number[]` (oförändrad typ, men nu ENDAST
     den PARSADE domän-DTO:n, aldrig React-state) skapas av EN ny, strikt funktion
     `parsaPolicyIndata(metadata: PolicyFaltMetadata, ravarde: PolicyRawFormValue |
     undefined): PolicyParseResultat` (`resultatkontrakt.ts`), anropad först vid submit
     (samma tidpunkt som `faltForBerakning` redan byggs i dag).

     **Rättat P1 (granskning `2026-09-09-003`) — signaturen tar nu genuint emot en
     frånvarande state-nyckel, och det gamla `PolicyValideringsFel`/`'saknat'`-språket är
     borttaget ur HELA denna beskrivning.** v12:s signatur `ravarde: PolicyRawFormValue`
     (utan `| undefined`) kunde inte kompilera mot punkt 2 nedan, som kräver att sidan
     itererar HELA `policyFaltMetadata`-listan och slår upp respektive nyckel i
     `policyFaltRavarden` — en `Record`-uppslagning på en aldrig initierad nyckel ger
     `undefined` vid runtime, ett värde den gamla signaturen avvisade. v12 blandade
     dessutom två feltyper: kardinalitets-/serieelementfelet ovan sades bli
     `PolicyValideringsFel` med (den obefintliga) orsaken `'saknat'`, trots att
     `PolicyValideringsFel` (§6a.2 punkt 6, `forkontrolleraPolicyIndata`s `ogiltiga`-fält) är en HELT
     ANNAN typ än denna funktions egen `PolicyParseResultat`.

     **Löst med EN delad orsaksunion, deklarerad EN gång och återanvänd överallt:**
     `type PolicyValideringsOrsak = 'typ' | 'numerik' | 'kardinalitet' | 'min' | 'max' |
     'heltal' | 'okant_val'` (`resultatkontrakt.ts`, samma namn i batchplanen — v12:s
     batchplan använde denna alias UTAN att den någonsin deklarerades, medan inventeringen
     samtidigt valde bara `'numerik'` för min/max/heltal-brott: nu är `'min'`/`'max'`/
     `'heltal'` egna, explicita medlemmar i unionen, använda konsekvent i BÅDA dokumenten).
     `type PolicyParseResultat = {status: 'parsed'; varde: PolicyInputValue} |
     {status: 'saknat'} | {status: 'ogiltigt'; orsak: 'typ' | 'numerik' | 'kardinalitet'}`
     (en STRIKT DELMÄNGD av `PolicyValideringsOrsak` — parsern kan bara ge dessa tre orsaker,
     eftersom `'min'`/`'max'`/`'heltal'`/`'okant_val'` kräver domänpolicyn/prispostens
     `nivaer` som `parsaPolicyIndata` inte har tillgång till, se nedan).

     Klassningen görs OBEROENDE av hur React-statet initialiserades — `parsaPolicyIndata`
     itererar `PolicyFaltMetadata`-listan (punkt 5), inte de råa state-nycklarna, så ett fält
     som aldrig fått en `onChange` alls klassas identiskt med ett fält vars ruta uttryckligen
     tömts av användaren (båda ger `{status:'saknat'}` — en `undefined`-`ravarde` normaliseras
     till samma utfall som en tom sträng, allra först i funktionskroppen, INNAN någon
     `inmatningstyp`-specifik logik körs). `'okant_val'` ingår MEDVETET inte i denna
     funktions möjliga orsaker — bandvalets giltighet mot `prisar.kapacitet.nivaer[].id`
     kräver prisdata som `parsaPolicyIndata` (bara `metadata`+`ravarde`) inte har tillgång
     till, och avgörs i stället av `forkontrolleraPolicyIndata` (punkt 6) i nästa steg:
     **Rättat P1 (granskning `2026-09-09-005`) — de utlovade scalar/array-formgrindarna
     saknades: en scalar-gren kunde nå `.trim()`/`Number(...)` på en array (fel
     per-tecken/`NaN`-beteende), och seriegrenen kunde nå `.length`/iteration på en ensam
     sträng (räknar TECKEN, inte serieelement).** Löst genom att varje gren FÖRST kräver rätt
     rå form och returnerar `{status:'ogiltigt', orsak:'typ'}` omedelbart vid fel form, INNAN
     någon `.trim()`/`.length`/iteration:
     - `inmatningstyp: 'number'` (inklusive Jönköpings `enum_val`, som är ETT UI-läge för ett
       numeriskt `number`-krav, se P2-rättningen nedan) och `inmatningstyp: 'band_id_val'`:
       om `ravarde === undefined` → `{status:'saknat'}`. Om `ravarde !== undefined` och
       `typeof ravarde !== 'string'` (dvs. en array skickad till ett skalärt fält) →
       `{status:'ogiltigt', orsak:'typ'}` DIREKT, `.trim()` anropas aldrig på en array. Annars
       (bekräftat `string`): om den trimmade strängen är tom → `{status:'saknat'}`.
       För `'number'`/`'enum_val'`: avvisar icke-ändligt/icke-parsbart tal med
       `{status:'ogiltigt', orsak:'numerik'}`, och konverterar annars med `Number(...)` till
       `{status:'parsed', varde}` — Jönköpings värde blir alltså TALET `10`, inte strängen
       `"10"`, och kan jämföras mot `tillatnaVarden: readonly number[]`. För
       `'band_id_val'`: `{status:'parsed', varde}` med strängen OFÖRÄNDRAD — `Number(...)`
       anropas ALDRIG för band-ID.
     - `inmatningstyp: 'number_series'`: om `ravarde === undefined` → `{status:'saknat'}`. Om
       `ravarde !== undefined` och `!Array.isArray(ravarde)` (dvs. en ensam sträng skickad
       till ett seriefält) → `{status:'ogiltigt', orsak:'typ'}` DIREKT — `.length` och
       iteration på strängen (vilket annars räknar TECKEN, inte serieelement) körs aldrig.
       Annars (bekräftat `readonly string[]`): om `ravarde.length !== antalVarden` →
       `{status:'ogiltigt', orsak:'kardinalitet'}` OMEDELBART, ingen elementvis parsning
       påbörjas. Annars trimmas och kontrolleras VARJE element enligt det skalära
       `number`-fallet ovan: om NÅGOT element är tomt (efter trim) → HELA serien
       `{status:'saknat'}`; om NÅGOT element (som inte är tomt) är icke-ändligt/icke-parsbart
       → HELA serien `{status:'ogiltigt', orsak:'numerik'}`; annars `{status:'parsed', varde:
       number[]}` — ALDRIG en delvis parsad serie med nollor på de tomma platserna.

     **Testfall (parserenhet + sidintegration, Batch 0:s end-to-end-test):** en array
     (`['10']`) skickad till ett `number`/`band_id_val`-fält ska ge `{status:'ogiltigt',
     orsak:'typ'}`, ALDRIG ett kastat undantag eller ett värde härlett från arrayens första
     element. En ensam sträng (`'10'`) skickad till ett `number_series`-fält ska likaså ge
     `{status:'ogiltigt', orsak:'typ'}`, ALDRIG en serie sammansatt av enskilda tecken.
   - Explicit `0` (en ifylld ruta med texten "0") skiljs alltså strukturellt från en tom ruta
     redan i `PolicyRawFormValue` (`""` vs `"0"`) — ingen `Number()`-tvetydighet uppstår,
     eftersom parsningen körs EFTER att tom-kontrollen redan avgjort "saknat" kontra
     "ifyllt".
2. `KalkylatorPage.tsx` bygger `policyFalt: Record<string, PolicyInputValue>` VID SUBMIT
   genom att köra `parsaPolicyIndata` (punkt 1) över VARJE post i `policyFaltMetadata`-listan
   (punkt 5) — inte över `policyFaltRavarden`s nycklar, se punkt 1s oberoende-av-
   initialisering-motivering — och slå upp respektive `PolicyRawFormValue` i
   `policyFaltRavarden` (frånvarande nyckel behandlas identiskt med en tom sträng, dvs.
   `{status:'saknat'}`) — precis samma tidpunkt som `faltForBerakning` redan byggs i dag. Ett
   `PolicyParseResultat` med `status:'saknat'` läggs i en `saknade: string[]`-lista (samma
   fältnamn som `harledResultatstatus`s befintliga `saknade`); `status:'ogiltigt'` läggs i en
   `ogiltiga: PolicyValideringsFel[]`-lista (`{nyckel, orsak}` — samma form
   `forkontrolleraPolicyIndata` i punkt 6 självständigt producerar i domänlagret, så BÅDA
   felkällorna münnar ut i EN gemensam `PolicyValideringsFel[]`-typ). Finns NÅGON post i
   endera listan visar `KalkylatorPage.tsx` fältnära formulärfel DIREKT vid submit, UTAN att
   ens anropa `besparingsvarde.ts` — en ren UX-genväg, INTE den enda spärren: ett anrop som
   kringgår detta UI-steg fångas ändå av `forkontrolleraPolicyIndata` i domänlagret (punkt 6),
   som beräknar exakt samma `saknade`/`ogiltiga` oberoende av UI:t. `byggIndataFranPolicy`
   (nästa) tar därför bara emot fält där VARJE `PolicyParseResultat` var `status:'parsed'`,
   och bygger `Record<string, PolicyInputValue>` genom att packa upp `.varde` från just de
   posterna.
   Ny hjälpfunktion i `besparingsvarde.ts`, `byggIndataFranPolicy(policy: Tariffpolicy,
   policyFalt: Record<string, PolicyInputValue>): Map<string, IndataPost>`: itererar
   `policy.kravdaFalt`, slår upp varje `nyckel` i `policyFalt` (INTE det numeriska `falt`),
   och bygger en `IndataPost` per TRÄFF med `kallaTyp: 'supplier_value'` och exakt det
   `PolicyInputValue`-formade värdet — ingen ytterligare typkonvertering sker i denna
   funktion, den ANTAR att anroparen redan levererat rätt form (punkt 1s parser garanterar
   det); `harled_resultatstatus`/`harledResultatstatus` gör kvarvarande strukturell
   validering (saknade fält, källtyp) som redan fanns innan detta tillägg. Ett
   policydeklarerat fält UTAN motsvarande `policyFalt`-nyckel byggs INTE — det blir korrekt
   `saknade`/`blocked` i `harled_resultatstatus`, inte en tyst `undefined`. En
   `policyFalt`-nyckel UTAN motsvarande policykrav IGNORERAS — extra, ovaliderad indata når
   aldrig motorn.
3. `beraknaBesparingsvardeKontrakt` anropar den nya funktionen i stället för att bara sätta
   ETT `Map`-inlägg för `kapacitetBindning` — kapacitetsbindningen (redan validerad separat
   ovanför i samma funktion, heltal/golv) läggs in i samma karta EFTER den generiska
   uppbyggnaden, så dess redan skärpta valideringsregler (§ befintlig kod) inte försvagas.
4. Python-sidans motsvarande produktväg (i dag bara Sandvikens direkta
   `berakna_arskostnad_med_kontrakt`-anrop i tester, ingen egen produktsida) får samma
   generiska byggfunktion `bygg_indata_fran_policy(policy, policy_falt:
   Mapping[str, float | str | Sequence[float]])` i förberedelse för framtida
   Python-produktkonsumenter, för att hålla mekanismen synkad i båda språken redan nu.
5. **Genererad UI-metadata — prispost- och omfattningsmedveten (rättat P1, granskning
   `2026-09-08-009`, ersätter v9:s `policyFaltMetadata(policy)`).** v9:s signatur tog BARA
   `Tariffpolicy`, men bandalternativen finns i den VALDA prispostens egen
   `prisar.kapacitet.nivaer[].id` (punkt 1 i §6a.2:s mekanism-avsnitt) — en funktion utan
   tillgång till `prisar` kan alltså inte bygga sitt eget `band_id_val`. `KravPost` har
   `enhet`/`tillamplighet`/`kalla` men inga `etikett`-/`hjalptext`-fält, och "en post per
   `KravPost`" med `obligatorisk: true` skulle (a) blanda Stockholms `monthly`- och
   `annual`-krav i samma årskalkylsvy, och (b) visa debiterbar effekt DUBBELT eftersom
   `KalkylatorPage` redan har ett separat, obligatoriskt `kapacitetKw`-fält.

   Ny signatur: `policyFaltMetadata(policy: Tariffpolicy, prisar: GenereradPrisarspost,
   omfattning: 'monthly' | 'annual'): PolicyFaltMetadata[]` i `resultatkontrakt.ts`. Filtrerar
   `policy.kravdaFalt` till (a) `f.kravsFor.includes(omfattning)` — bara krav som gäller den
   EFTERFRÅGADE omfattningen renderas, aldrig hela policyn oavsett kalkylläge — och (b)
   `f.nyckel !== policy.kapacitetBindning` — kapacitetsbindningens fält äger redan sin egen
   dedikerade `kapacitetKw`-inmatning och exkluderas EXPLICIT ur den generiska listan, i
   stället för att förlitas på en implicit ordning där det råkar läggas till en andra gång.
   En post per KVARVARANDE `KravPost`, med:
   `{ nyckel, inmatningstyp: 'number' | 'band_id_val' | 'enum_val' | 'number_series',
   etikett, hjalptext, obligatorisk: true, tillatnaVarden?, antalVarden? }`.
   **Rättat P2 (granskning `2026-09-09-001`) — EN källa för etikett/hjälptext.** `KravPost`
   (`resultatkontrakt.py`/`.ts`) får två nya, valfria fält `etikett: str | None = None`/
   `hjalptext: str | None = None`, satta AUKTORITATIVT av `policyregister.py` när en
   policy-post deklareras (samma ansvar som redan sätter `kalla`) — INTE härledda via
   `indatafalt_for()`/`generera.py`, som är en helt annan mekanism för de BEFINTLIGA,
   numeriska `indatafalt`-posterna och inte känner till `KravPost` alls. `_policy_till_json()`
   (Python) respektive `policyFranGenererad()` (TypeScript) är TRANSPORTEN — de serialiserar
   redan hela `KravPost` och behöver bara föra de två nya fälten igenom oförändrat, ingen ny
   katalogmappning. Ett `KravPost` utan uttrycklig `etikett` kastar i
   `skapaKravPost`/`__post_init__` (fail-closed, ingen tyst fallback-text). Band-ID-
   alternativen (`inmatningstyp: 'band_id_val'`) hämtas från `prisar.kapacitet.nivaer[].id` —
   varje bevarat band-ID valideras (`skapaTariffpolicy`/motsvarande katalogbyggnadssteg) vara
   en ICKE-TOM sträng och UNIK inom prispostens `nivaer`-lista INNAN motorn (`vald_niva_id`s
   `next(...)`-uppslagning) eller UI:t får använda dem — ett dubblerat eller tomt `id` kastar
   redan vid katalogbyggnad/generering, inte tyst vid runtime-uppslagning (annars skulle två
   prisrader med samma ID göra leverantörens bekräftade val tvetydigt, eftersom `next(...)`
   bara returnerar den FÖRSTA träffen). Enum-alternativ (`inmatningstyp: 'enum_val'`) hämtas
   från `KravPost.tillatnaVarden` (§6a.6) — **rättat P2:** kontraktet har TRE värdetyper
   (`number`, `number_series`, `band_id`); `enum_val` är ett UI-LÄGE för ett numeriskt
   `number`-krav med en allow-list, inte en fjärde `vardetyp`. Varken enum- eller bandvärden
   får någonsin passera `Number(...)` för band-ID, medan enum (Jönköping) uttryckligen SKA
   parsas till tal — se punkt 1s uppdelning mellan `PolicyRawFormValue` och den parsade
   `PolicyInputValue`.

   **Batch 0:s end-to-end-test:** renderar den VERKLIGA `KalkylatorPage`-komponenten (React
   Testing Library eller motsvarande, inte en fristående testkomponent som kan drifta bort
   från produktsidan) med en vald syntetisk prispost som bär alla TRE `vardetyp` (`number`,
   `number_series`, `band_id`) plus ett Jönköping-liknande `enum_val`-läge på ett av de
   numeriska kraven, väljer ett band-ID, fyller en 12-elements serie inklusive en medveten
   tom ruta (ska ge fältnära fel, inte en nolla) och ett giltigt Jönköpingsval, och
   verifierar att det beräknade resultatet matchar en handräknad referens — inte bara att
   `byggIndataFranPolicy` kan anropas isolerat.
6. **Felklassning — både saknad OCH ogiltig kundindata som typade användarfel, genom en
   KÖRBAR felkanal (rättat P1, granskning `2026-09-09-001`, ersätter v10:s
   icke-implementerbara "läs det ur ett `blocked`-resultat"-design).** v10 sa att
   `beraknaBesparingsvardeKontrakt` skulle sätta `ogiltigaFalt` när
   `status.fullstandighet === 'blocked'` OCH `harled_resultatstatus`/`harledResultatstatus`
   avvisat typ/numerik/kardinalitet/allow-list. **Verifierat mot verklig kod att det inte är
   dagens kontrakt:** `harledResultatstatus` returnerar `blocked` ENDAST för fält som helt
   SAKNAS i den inrapporterade indatan (`resultatkontrakt.ts` rad 378–380, `saknade.length >
   0`-kontrollen). Allt annat — fel typ, numerik utanför gräns, fel serieform, brutet
   heltalskrav — kastar `Error` mitt i valideringsloopen (rad 385–420), och v10 planerade att
   lägga de NYA `vardetyp`-/`antalVarden`-/`tillatnaVarden`-kontrollerna i EXAKT samma
   kastande loop. Det finns alltså aldrig ett `status`-objekt att läsa `orsak` ur efter ett
   ogiltigt värde — bara ett kastat undantag som redan har lämnat funktionen. Ett okänt
   band-ID upptäcks dessutom ÄNNU senare, av motorns `next(...)`-uppslagning, eftersom
   statusvalidatorn inte har tillgång till prispostens `nivaer` — det blir alltså ett tredje,
   ospecificerat kastställe, inte ett namngivet `'okant_val'`.

   **Löst med en separat valideringsfunktion FÖRE fasadanropet (Codex alternativ A),** i
   stället för att försöka omtolka `harledResultatstatus`s befintliga kastbeteende: ny
   `forkontrolleraPolicyIndata(policy: Tariffpolicy, prisar: GenereradPrisarspost, indata:
   ReadonlyMap<string, IndataPost>, omfattning: Omfattning): { saknade: readonly string[];
   ogiltiga: readonly PolicyValideringsFel[] }` (`resultatkontrakt.ts`, mirror
   `forkontrollera_policy_indata` i Python) — körs av
   `beraknaBesparingsvardeKontrakt`/`beraknaArsprodukt` (§6a.4) OMEDELBART efter
   `byggIndataFranPolicy` men INNAN `beraknaArskostnadMedKontrakt`/`harledResultatstatus`
   någonsin anropas.

   **Omfattningsmedveten (rättat P1, granskning `2026-09-09-004`): v13 saknade
   `omfattning`-parametern helt.** Funktionen itererade tidigare över HELA
   `policy.kravdaFalt`, oavsett om anroparen ville räkna en annan- eller
   `monthly`-omfattning eller en `annual`-omfattning. Stockholms konsoliderade policy
   (§6a.4) bär BÅDE de befintliga `monthly`-kraven (kall energi, returtemperatur, effekt
   för `monthly_invoice`) OCH de nya `annual`-serierna — en årsberäkning hade alltså
   riskerat att få de irrelevanta månadsfälten i `saknade` och blockerats INNAN
   `harledResultatstatus` (vars riktiga kod, rad 373–374, redan filtrerar
   `f.kravsFor.includes(omfattning)`) ens nås. Funktionen filtrerar nu IDENTISKT:
   `const relevanta = policy.kravdaFalt.filter(f => f.kravsFor.includes(omfattning))`,
   och itererar bara `relevanta`. Båda årsproduktvägarna (`beraknaBesparingsvardeKontrakt`,
   `beraknaArsprodukt`) skickar uttryckligen `'annual'`; en framtida `monthly_invoice`-väg
   skulle skicka `'monthly'`. En syntetisk testpolicy med SAMTIDIGA `monthly`- och
   `annual`-krav ska bevisa att varje produktväg bara kräver sitt eget scope.

   **Rättat P2 (granskning `2026-09-09-005`) — "filtrerar nu IDENTISKT" med
   `harledResultatstatus` stämde bara delvis.** Den verkliga fasaden filtrerar på BÅDE
   `f.kravsFor.includes(omfattning)` OCH — när ett `manad`-argument är satt —
   `f.tillampligaManader === undefined || f.tillampligaManader.includes(manad)`
   (`resultatkontrakt.ts` rad 374–375). `forkontrolleraPolicyIndata` har ENDAST
   `omfattning`-parametern, ingen `manad`. Detta ger IDENTISKT resultat för dagens två
   anropsställen eftersom BÅDA alltid skickar `'annual'` och aldrig ett `manad`-värde — en
   årsberäkning har inget vinterfönster att smalna mot. Funktionen är därför MEDVETET
   avgränsad till att vara omfattnings- men INTE månadsmedveten: en framtida
   `monthly_invoice`-väg som behöver `tillampligaManader`-filtrering (t.ex. undvika att kräva
   ett vinterfält under en sommarmånad) måste antingen utöka signaturen med samma valfria
   `manad?: number`-parameter och samma villkor som `harledResultatstatus` ovan, eller
   uttryckligen dokumenteras som körd EFTER en separat månadsfiltrering — inte antas
   "identisk" utan denna reservation.

   - Fält i `relevanta` som INTE finns i `indata` läggs i `saknade` (bara nyckelnamnet —
     samma form som `KontraktBlockerat.saknadeFalt`, se nedan) och får ALDRIG någon vidare
     värdekontroll (det finns inget värde att kontrollera).
   - Fält i `relevanta` som FINNS i `indata` kontrolleras och kan hamna i `ogiltiga`:
     `vardetyp` (skalärt tal för `number`, icke-tom talserie för `number_series`, icke-tom
     sträng för `f.vardetyp === 'band_id'`) → orsak `'typ'`; `antalVarden` för seriekrav →
     orsak `'kardinalitet'`; `tillatnaVarden`-medlemskap för enum → orsak `'okant_val'`;
     `f.minVarde` (samtliga element för en serie) → EGEN orsak `'min'`; `f.maxVarde` → EGEN
     orsak `'max'`; `f.heltal` (`Number.isInteger` på samtliga element) → EGEN orsak
     `'heltal'` (**rättat P1, granskning `2026-09-09-004`: v13 mappade tidigare alla tre
     gräns-/heltalsbrott till den delade orsaken `'numerik'` HÄR, trots att §6a.2:s
     deklaration av `PolicyValideringsOrsak` uttryckligen listar `'min'`/`'max'`/`'heltal'`
     som egna, namngivna medlemmar — två motsägande modeller i samma dokument. Denna
     sektion är nu rättad till att använda EXAKT samma tre dedikerade orsaker
     `PolicyValideringsOrsak` deklarerar, `'numerik'` reserveras för icke-ändliga tal**;
     samma kontroller `harledResultatstatus`s kastande loop, rad 385–420, redan gör i dag —
     bara flyttade hit FÖRE den kastande loopen nås), och — för fält där
     `f.vardetyp === 'band_id'` (samma diskriminator som resten av §6a.2 använder för att
     peka ut bandfält, INTE en separat `band_id_val`-UI-metadataegenskap denna funktion
     aldrig tar emot; `forkontrolleraPolicyIndata` ser bara `Tariffpolicy`/`prisar`/
     `IndataPost`, inte `PolicyFaltMetadata`) — slår upp värdet mot
     `prisar.kapacitet.nivaer[].id` och lägger till `{nyckel, orsak: 'okant_val'}` om ingen
     träff finns.

   **Rättat P1 (granskning `2026-09-09-003`) — `saknadeFalt` var i praktiken oåtkomlig för
   ett direkt produktanrop som kringgår formuläret.** v12 påstod att detta redan var löst,
   eftersom `harledResultatstatus`s befintliga `blocked`-status "redan" exponerar vilka
   nycklar som saknas — verifierat FALSKT mot `resultatkontrakt.ts` (rad 262–266, 365–400):
   `Resultatstatus`-gränssnittet har INGET fältnamnlistfält (bara `omfattning` / `noggrannhet`
   / `fullstandighet`), och `harledResultatstatus` bygger visserligen en lokal `saknade`-lista
   internt men KASTAR BORT den — returnerar bara den generiska statusen `'blocked'`, aldrig
   fältnamnen. Så länge `saknadeFalt` var tänkt att härledas UR den vägen, kunde den alltså
   aldrig fyllas i för ett anrop som byggde sin egen `IndataPost`-karta direkt (t.ex. ett
   framtida serverdrivet batch-jobb) utan att passera `KalkylatorPage.tsx`s egen,
   UI-specifika saknad-fält-bokföring.

   **Löst genom att `forkontrolleraPolicyIndata` själv beräknar BÅDA listorna** direkt ur
   `policy.kravdaFalt` mot den mottagna `indata`-kartan — en beräkning som inte har NÅGOT
   beroende av React-state eller av `harledResultatstatus`s interna, kastade `saknade`-lista,
   och därför fungerar identiskt oavsett om anroparen är `KalkylatorPage.tsx` (som redan har
   byggt `indata` från formuläret) eller ett direkt produktanrop som byggt sin `indata`-karta
   för hand.

   **Konkret, konstruerbar `KontraktBlockerat`-väg (rättat P1, granskning `2026-09-09-004`):
   v13 beskrev bara VART fälten skulle "fyllas i" utan att visa någon faktisk
   konstruktoranropspunkt eller någon ny `orsak`.** **Rättat P2 (granskning
   `2026-09-09-005`): `KontraktBlockeratOrsak`-typen och `KontraktBlockerat`-klassen ligger
   verifierat i `besparingsvarde.ts`, INTE i `resultatkontrakt.ts` — v14 sa fortfarande fel
   fil här trots att batchplanens fillista redan hade rätt fil; denna sats är nu synkad med
   batchplanen.** `KontraktBlockeratOrsak` (`besparingsvarde.ts`) utökas från dagens 5 medlemmar (`missing_capacity`,
   `invalid_capacity`, `unsupported_input_mode`, `missing_energy`, `invalid_energy`) med
   TVÅ nya: `'missing_policy_fields'` och `'invalid_policy_fields'`. Konstruktorn
   `KontraktBlockerat(tariffId: string, orsak: KontraktBlockeratOrsak, status?:
   Resultatstatus)` byts till ett tredje, valfritt OPTIONS-argument i stället för det rena
   `status?`-läget:
   `KontraktBlockerat(tariffId: string, orsak: KontraktBlockeratOrsak, tillagg?: {
   status?: Resultatstatus; saknadeFalt?: readonly string[]; ogiltigaFalt?: readonly
   PolicyValideringsFel[] })` — verifierat mot alla 8 riktiga anropsställen i
   `besparingsvarde.ts` att INGET av dem i dag skickar ett tredje positionellt argument,
   så denna ombyggnad är en säker, icke-brytande utökning, inte en breddning av en
   redan använd position. Konstruktorn skriver `tillagg?.saknadeFalt` till instansens
   `saknadeFalt`-fält och `tillagg?.ogiltigaFalt` till `ogiltigaFalt`-fältet.

   Konkret anropsexempel i `beraknaBesparingsvardeKontrakt`/`beraknaArsprodukt`, direkt efter
   `forkontrolleraPolicyIndata`:
   ```ts
   const { saknade, ogiltiga } = forkontrolleraPolicyIndata(policy, prisar, indata, 'annual');
   if (saknade.length > 0) {
     throw new KontraktBlockerat(prisar.tariff_id, 'missing_policy_fields', { saknadeFalt: saknade });
   }
   if (ogiltiga.length > 0) {
     throw new KontraktBlockerat(prisar.tariff_id, 'invalid_policy_fields', { ogiltigaFalt: ogiltiga });
   }
   ```
   `saknade`- och `ogiltiga`-kontrollerna körs som två separata `if`-block (inte ett
   kombinerat kast) eftersom de har olika `orsak`-värden — ett anrop kan bara bära EN
   orsak. Om båda listorna är icke-tomma vinner `saknade` (kastas först), samma prioritet
   `harledResultatstatus`s befintliga kastordning redan följer för andra fält.
   `harledResultatstatus` anropas ALDRIG i något av dessa två fall — den gröna vägen
   (`saknade`/`ogiltiga` båda tomma) fortsätter oförändrat till
   `beraknaArskostnadMedKontrakt`/`harledResultatstatus` precis som i dag, så det befintliga
   `blocked`-beteendet för ANDRA orsaker (t.ex. datakvalitet i motorn, inte i indata) förblir
   opåverkat.

   Interna kontrakts-/konfigurationsfel (fortsatt en kastad `Error`, aldrig
   `KontraktBlockerat`) reserveras för fall UTAN ett specifikt användarinmatat fält att peka
   på: en saknad bindningsmålpost i policyn själv, fel bindningstyp (t.ex.
   `kapacitet_band_bindning` som pekar på ett `"number"`-krav i stället för `"band_id"`), en
   omöjlig policykombination, eller trasig genererad metadata (punkt 5) — dessa upptäcks
   redan under `forkontrolleraPolicyIndata`s iteration men klassas som `Error`, inte
   `PolicyValideringsFel`, eftersom de inte är kundens fel att rätta.

   `KalkylatorPage.tsx` visar `saknadeFalt`/`ogiltigaFalt` som fältnära formulärfel (samma
   mönster som `kapacitetsfelText` redan använder för det befintliga kapacitetsfältet), inte
   det generiska felmeddelandet. Ska testas identiskt i BÅDA språken (fortsatt öppet, P2,
   granskning `2026-09-09-002`: v11 påstod detta redan var gjort — ingen sådan testsvit
   existerar ännu i den checkade-in koden, detta är ett åtagande för Batch 0, inte en
   genomförd verifiering): tom/delvis ifylld serie, icke-ändligt tal, okänt band-ID mot en
   verklig prisposts `nivaer`, ett Jönköpingsvärde utanför `tillatnaVarden` — via BÅDE UI:t
   (punkt 5:s end-to-end-test) OCH ett direkt produktanrop som kringgår formuläret helt (nu
   möjligt att faktiskt testa, se ovan).

**Numerisk rimlighetskontroll (frivillig, källbaserad — inte `_niva()` återinförd som
sanningskälla):** om en tariffs källa publicerar entydiga, normaliserade gränser (t.ex.
Borlänges "band 5 gäller `>501` kW") kan policyn DESSUTOM kräva att det numeriska
kapacitetsvärdet ligger inom det bekräftade bandets `min`/`max` — men det bekräftade
band-ID:t vinner alltid över vad `_niva()` skulle valt; kontrollen finns bara för att fånga
en uppenbar felskrivning (t.ex. band-ID 3 ihopparat med ett kW-tal som uppenbart hör till
band 6), inte för att överpröva ett korrekt, tvetydigt gränsfallsbesked. Öppna gränspunkter
(">N" utan explicit övre gräns, "<N" utan explicit undre gräns) hanteras genom att helt
enkelt inte sätta den saknade gränsen — ingen implicit ±1-justering.

**De 42 berörda raderna** (tariff-ID, antal band, källans band-ID:n — verifierat mekaniskt):

| Tariff-ID | Band | Band-ID:n i källan |
|---|---:|---|
| `boras-energi-och-miljo-boras-sjomarken-sandared-dalsjofors-fristad-2026` | 6 | 1–6 |
| `borlange-energi-borlange-2026` | 5 | 1–5 |
| `c4-energi-kristianstad-2026` | 6 | 1–6 |
| `e-on-jarfalla-jarfalla-och-upplands-bro-bostader-2026` | 1 | 1 |
| `e-on-jarfalla-jarfalla-och-upplands-bro-ovriga-fastigheter-2026` | 1 | 1 |
| `e-on-malmo-malmo-och-burlov-bostader-2026` | 1 | 1 |
| `e-on-malmo-malmo-och-burlov-ovriga-fastigheter-2026` | 1 | 1 |
| `falu-energi-vatten-bjursas-grycksbo-sundborn-svardsjo-2026` | 4 | 1–4 |
| `falu-energi-vatten-falun-2026` | 7 | 1–7 |
| `habo-energi-habo-2026` | 1 | 1 |
| `jamtkraft-are-jarpen-morsil-duved-kall-hallen-krokom-nalden-follinge-2026` | 5 | 1–5 |
| `jamtkraft-brunflo-och-opevagen-2026` | 5 | 1–5 |
| `jamtkraft-ostersund-froson-as-2026` | 5 | 1–5 |
| `jonkoping-energi-jonkoping-och-granna-2026` | 4 | 1–4 |
| `karlstads-energi-karlstad-2026` | 5 | 1–5 |
| `kils-energi-kil-2026` | 4 | 1–4 |
| `kraftringen-kraftringen-2026` | 4 | 1–4 |
| `lulea-energi-lulea-2026` | 7 | 1–7 |
| `mjolby-svartadalen-energi-mjolby-2026` | 4 | 1–4 |
| `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-bostader-2026` | 1 | 1 |
| `navirum-energi-norrkoping-och-soderkoping-norrkoping-och-soderkoping-ovriga-fastigheter-2026` | 1 | 1 |
| `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-bostader-2026` | 1 | 1 |
| `navirum-energi-orebro-kumla-och-hallsberg-orebro-kumla-och-hallsberg-ovriga-fastigheter-2026` | 1 | 1 |
| `nevel-gimo-osterbybruk-och-osthammar-2026` | 3 | 1–3 |
| `oresundskraft-angelholm-normal-2026` | 5 | 1–5 |
| `oresundskraft-helsingborg-normal-2026` | 5 | 1–5 |
| `oresundskraft-helsingborg-totalvarme-central-installerad-fore-2024-2026` | 5 | 1–5 |
| `ovik-energi-ornskoldsvik-2026` | 16 | 1–16 |
| `partille-energi-partille-2026` | 7 | 1–7 |
| `piteenergi-norrfjarden-och-sjulnas-2026` | 4 | 1–4 |
| `piteenergi-pitea-centrala-natet-2026` | 4 | 1–4 |
| `skovde-energi-skovde-2026` | 1 | 1 |
| `soderhamn-nara-soderhamn-taxa-11-och-12-2026` | 4 | 10–13 |
| `sodertorns-fjarrvarme-sodertorns-fjarrvarme-2026` | 4 | 1–4 |
| `stockholm-exergi-stockholm-exergi-normal-2026` | 5 | 1–5 (rad exkluderad, se §6a.4 — bandkontraktet moot) |
| `tekniska-verken-katrineholm-katrineholm-2026` | 4 | 1–4 |
| `tekniska-verken-linkoping-linkoping-2026` | 4 | 1–4 |
| `telge-nat-telge-foretag-och-bostadsrattsforeningar-2026` | 3 | 1–3 |
| `temab-fjarrvarme-tierp-karlholmsbruk-och-orbyhus-2026` | 3 | 1–3 |
| `trollhattan-energi-trollhattan-2026` | 5 | 1–5 |
| `umea-energi-umea-enkel-2026` | 7 | 1–7 (dessutom `kapacitet_multiplikator_bindning`, §6a.3) |
| `vanerenergi-mariestad-och-toreboda-2026` | 4 | 1–4 |

**Ambiguösa exakta gränsfall (kräver leverantörsbekräftelse, inte bara ett vilket-som-helst
band-ID):** `borlange-energi-borlange-2026` (band 5, `>501`) och
`c4-energi-kristianstad-2026` (band 6, `>500`) är de två rader där ett exakt gränsvärde
(501 respektive 500 kW) är den uttryckligen osäkra punkten källan själv flaggar. De övriga
40 raderna har inte en känd tvetydig gräns i källan, men bandkontraktet gäller ändå
strukturellt för alla 42 — katalogens integrationskontrakt gör ingen skillnad mellan "känt
tvetydiga" och "inte kända som tvetydiga", och en framtida gränsförskjutning ska inte kunna
smyga sig förbi en rad som råkade vara icke-ambiguös vid detta skrivtillfälle.

### 6a.3 Umeås `kapacitet_multiplikator_bindning` — arkitektoniskt separerad grind (rättat P1, granskning 2026-09-08-007)

**Rättat ordningsfel (P1, granskning `2026-09-08-007`):** v7 påstod att
`kontrollera_kompositgrind(tariff, policy)` skulle köras EFTER steg 2+3 i §6 — men den
VERKLIGA generatorn (`bygg_ts_fran_katalog()` i `generera.py`) anropar
`ur_katalogen = godkanda(katalog)` FÖRST och itererar sedan BARA de rader `grind()` gav
`None` för. En kontroll som körs "efter" kan alltså aldrig återinföra en rad `godkanda()`
redan filtrerat bort — Codex reproducerade exakt detta: med Umeås status/issues
neutraliserade gav `grind(...)` fortsatt `"kapacitetsformel med multiplikator"` och
`godkanda()` returnerade noll rader.

Löst genom att flytta kompositkontrollen IN I `godkanda()`s egen loop, som ett andra försök
begränsat till EXAKT ett fynd — **rättat P1 (granskning `2026-09-08-008`):** v8:s version
lade till raden så fort `kontrollera_kompositgrind()` godkände multiplikatorbindningen, UTAN
att därefter kontrollera om ett ANNAT strukturellt fynd (okänd `issue`, okänd
`okand_justering()`) låg dolt bakom multiplikatorfyndet. `grind()` returnerar bara det FÖRSTA
fyndet den hittar, och kontrollen av `post_multiplier` ligger FÖRE kontrollen av `issues`/
`okand_justering()` — Codex reproducerade att Umeås verkliga katalograd har SAMTLIGA tre
problem samtidigt (`post_multiplier`, en ännu okänd `issue`, och `asymmetric_flow_difference`
som `okand_justering()` inte känner igen), så v8:s design skulle ha lagt till raden utan att
de två sistnämnda någonsin kontrollerades. Fixet: efter att multiplikatorbindningen är
verifierad, körs `grind()` EN GÅNG TILL på en kopia av tariffen där ENDAST det fynd som redan
är kvitterat (`post_multiplier`) är neutraliserat — alla andra fält, inklusive `issues` och
`adjustments`, är oförändrade. Bara om ÄVEN detta andra pass ger `None` läggs raden till:

```python
def _neutralisera_post_multiplier(tariff: dict) -> dict:
    """Returnerar en YTLIG kopia av tariffen där ENDAST det redan kvitterade
    post_multiplier-fyndet är borttaget — kapacitetsobjektet kopieras separat
    så den ursprungliga katalogposten aldrig muteras. Alla andra fält
    (issues, adjustments, investigation, m.m.) är OFÖRÄNDRADE, så grind()s
    andra pass fortsatt kan hitta och blockera på dem."""
    kapacitet = dict(tariff.get("capacity") or {})
    kapacitet.pop("post_multiplier", None)
    return {**tariff, "capacity": kapacitet}


def godkanda(katalog: dict, policyregister: dict = POLICYREGISTER) -> list[dict]:
    resultat = []
    blockerade = blockerade_tariff_ider(katalog)  # §7
    for t in katalog["tariffs"]:
        avslag = grind(t, blockerade)
        if avslag is None:
            resultat.append(t)
            continue
        # NYTT: kompositgrindens ENDA konsumerbara fynd. Varje annat fynd
        # ("null i band", "okänd issue", "energiform", ...) faller igenom
        # och tariffen förblir blockerad — ingen generell undantagsväg.
        if avslag == "kapacitetsformel med multiplikator":
            policy = policyregister.get(t["id"])
            if policy is not None and kontrollera_kompositgrind(t, policy) is None:
                # Multiplikatorfyndet är kvitterat — men grind() returnerade
                # bara DET FÖRSTA fyndet; kör grinden igen med bara det
                # kvitterade fältet neutraliserat, för att avslöja en
                # eventuell DOLD andra blockering (samma "metodnot"-mönster
                # som redan gällde 13 av de 45 raderna, §6).
                t_neutraliserad = _neutralisera_post_multiplier(t)
                if grind(t_neutraliserad, blockerade) is None:
                    resultat.append(t)
                # annars: fortfarande blockerad av ett dolt strukturellt fynd
        # annars: förblir blockerad (fortsätter loopen utan att lägga till t)
    return resultat
```

**Rättat P1 (registerdivergens, granskning `2026-09-08-008`):** v8:s pseudokod introducerade
`godkanda(katalog, policyregister=POLICYREGISTER)` men sa att `bygg_ts_fran_katalog()` inte
behövde ändras — verifierat att generatorn i dag anropar `godkanda(katalog)` UTAN registret,
medan den redan har ett injekterbart `policyregister`-argument som förs vidare till
`kontrollera_aktiveringsgrind(..., register=policyregister)` längre ner i samma funktion. Utan
en ändring skulle den sammansatta grinden läsa det GLOBALA registret medan resten av
generatorn läser det INJICERADE — ett testregister och produktregistret kunde då ge olika
svar. `bygg_ts_fran_katalog()` ändras därför till att uttryckligen föra sitt egna
`policyregister`-argument vidare till `godkanda(katalog, policyregister=policyregister)`, och
`main()`s räkningslogik (som anropar `godkanda()` separat för statistik) gör detsamma.

Detta ÄR den körbara ordningen — kompositkontrollen är en del av samma filtreringspassage
`godkanda()` redan gör, inte ett separat steg efteråt. `bygg_ts_fran_katalog()` behöver
föra sitt egna `policyregister`-argument uttryckligen vidare till `godkanda(katalog,
policyregister=policyregister)` (se ovan) — annars läser den sammansatta grinden det globala
`POLICYREGISTER` medan resten av funktionen kan läsa ett injicerat register. Utöver den ena
raden ligger hela fixet i `godkanda()` själv.

1. Den nakna `grind()` (`katalog.py`) ändras INTE — den fortsätter avvisa varje
   `capacity.post_multiplier` som `"kapacitetsformel med multiplikator"`, oförändrat för
   alla tariffer inklusive Umeå. Umeå passerar alltså ALDRIG steg 2 (§6) ensamt — bara den
   sammansatta `godkanda()`-loopen ovan kan öppna raden, och först efter att BÅDA
   grindpassen (det ursprungliga och det neutraliserade) gett `None`.
2. `kontrollera_kompositgrind(tariff: dict, policy: Tariffpolicy) -> str | None`
   (`policyregister.py`) tar policyn som explicit argument. Om
   `tariff["capacity"].get("post_multiplier") is not None`, kräver funktionen att
   `policy.kapacitet_multiplikator_bindning is not None` OCH att den bundna `KravPost`
   finns i `policy.kravda_falt` — annars avslagsorsak. Detta ÄR den explicita, typade
   capability-kontrollen v6 saknade; den nakna grinden godkänner aldrig en okänd
   multiplikator på egen hand, och kompositkontrollen kan bara YTTERLIGARE godkänna, aldrig
   ytterligare blockera, en rad `grind()` redan släppte igenom.
3. Motorn (`faktura.py`/`fjarrvarme.ts`) läser det bundna värdet som `B` och multiplicerar
   in det i kapacitetsformeln — motorn räknar ALDRIG `U` (normalårskorrigerat förhållande),
   bara `B` som ett direkt leverantörsvärde. Python: `kapacitet_multiplikator_bindning: str
   | None = None` på `Tariffpolicy`, validerat mot `kravda_falt` precis som
   `kapacitet_bindning`/`kallenergi_bindning`. TypeScript-spegel:
   `kapacitetMultiplikatorBindning?: string` — mappningsraden i §6a.1s tabell.

**Intervallkrav, omräknat:** den publicerade mellanformeln `1,34×U+0,330` ger `1,40066` vid
`U=0,799` (katalogens övre brytpunkt) — ett absolut, avrundat tak `maxvarde=1,4` hade därför
kunnat avvisa ett giltigt leverantörsvärde beroende på HUR leverantören själv avrundar sin
egen publicerade formel. Kravet sätts i stället till `minvarde=0.93`, `maxvarde=1.401` —
fyra värdesiffror, en (1) enhet extra marginal på sista decimalen mot den exakta
formelutledda gränsen `1,40066`, med regeln dokumenterad explicit i policykommentaren i
stället för att gissa ett exakt tak.

**Rättat P1 (granskning `2026-09-08-007`) — B-värdesvalideringen flyttad till rätt lager:**
`kontrollera_kompositgrind` tar bara `(tariff, policy)` — den kan bevisa att bindningen är
DEKLARERAD, men har ingen `IndataPost` att kontrollera det faktiska kundvärdet mot. Testet
för `B=14` (uppenbart utanför intervallet) hör därför INTE hemma i
`kontrollera_kompositgrind`, utan i `harled_resultatstatus`/kontraktsfasaden via den bundna
`KravPost`s `minvarde=0.93`/`maxvarde=1.401` — exakt samma mekanism som redan validerar
Sandvikens effektgolv. Test: golden-värden vid `B=0.93`, `B=1.401` och en punkt mellan
brytpunkterna (kontraktsfasaden, steg 4 i §6); ett negativt test för `B=14` blockerar via
`harled_resultatstatus` (INTE `kontrollera_kompositgrind`, som aldrig ser det faktiska
värdet); och ett separat test att Umeå UTAN bindningen fortsatt stoppas av
`kontrollera_kompositgrind` (steg 3, den statiska kontrollen) samt att en ANNAN tariff med
okänd multiplikator (ingen policy alls, eller policy utan bindningen) fortsatt stoppas av
samma funktion. Testet kallas `B-intervall`, inte "U-intervall" — motorn räknar aldrig `U`.

**Nya test (granskning `2026-09-08-008`, `godkanda()`s tvåpassdesign ovan):** Umeå läggs
till i `godkanda()`s resultat FÖRST när issue-rättelsen, den kända justeringstypen
(`asymmetric_flow_difference` registrerad) OCH B-bindningen samtliga finns; lägg tillbaka en
okänd `issue` (allt annat rättat) och bevisa att raden ändå blockeras av det andra
`grind()`-passet; lägg tillbaka en okänd justeringstyp (allt annat rättat) och bevisa samma
sak. Ett separat test kör `godkanda(katalog, policyregister=ett_annat_register)` och bevisar
att resultatet skiljer sig från `godkanda(katalog)` (globalt register) när det injicerade
registret saknar Umeås policy — bevisar att registret faktiskt förs igenom, inte bara läses
globalt av misstag.

**Används av:** `umea-energi-umea-enkel-2026` — enda tariffen med `post_multiplier` i dagens
kontrollmängd. Kräver BÅDE detta OCH bandkontraktet (§6a.2) — verifierat att raden har både
`band_selection` och `post_multiplier` samtidigt.

### 6a.4 Stockholm Exergi — nåbar adapterkontroll, verklig dispatch och en typad årsindatamodell (rättat P1, granskning 2026-09-08-007/-008/-009, 2026-09-09-001)

**Rättat P1 #1 — adapterkontrollen var inte nåbar:** v7 beskrev `ADAPTERREGISTER` som
kontrollerat "när generatorn behandlar en katalogtariff" — men den VERKLIGA
`bygg_ts_fran_katalog()` gör `ur_katalogen = godkanda(katalog)` FÖRST och itererar sedan
BARA de rader som kom igenom. Stockholms katalograd har `investigation.status: utreds` OCH
stoppas av `energiform` (`monthly_with_peak_volume_replacement` finns inte i
`FAS1_ENERGIFORMER`) — den når alltså ALDRIG in i den filtrerade loopen där v7 tänkte sig
kontrollen. Löst genom att köra adapterkontrollen som en SEPARAT preflight mot den RÅA
`katalog["tariffs"]`-listan, direkt efter `ur_katalogen = godkanda(katalog)` i
`bygg_ts_fran_katalog()` — oberoende av om katalograden finns kvar i `ur_katalogen`:

**Rättat P1 (granskning `2026-09-08-009`) — injicerbar tvåvägsfunktion i stället för globala
register och ett bokstavligt `pass`.** v9:s pseudokod läste fortfarande de globala
`POLICYREGISTER`/`ADAPTERREGISTER` trots att `godkanda()` (§6a.3) redan gjorts injicerbar för
`policyregister`, och den omvända kontrollen innehöll bokstavligen `pass  # se
produktionskoden` — kunde alltså inte bevisa det test planen lovade. Den efterföljande
textregeln var dessutom självmotsägande: den förbjöd `annual_forward` om policyn "inte var
adaptermål ELLER inte redan var godkänd före denna etapp" — ett `eller` som även skulle
förbjuda en NY, korrekt adaptermappad Stockholm-policy — samtidigt som pseudokodens
kommentar tillät framtida direkta leverantörsprodukter utan katalogmotsvarighet. "Redan
godkänd före denna etapp" är dessutom historiskt tillstånd, inte data en ren, reproducerbar
generator kan kontrollera.

Löst med en EXPLICIT, maskinläsbar markör på policyn själv i stället för ett historiskt
undantag: nytt, valfritt `Tariffpolicy`-fält `ersatter_katalograd: str | None = None`
(mirror `ersatterKatalograd?: string` i TS) — satt till katalog-ID:t på RAD som en
leverantörsfilspolicy avsett ERSÄTTER (Stockholms fall: `ersatter_katalograd:
"stockholm-exergi-stockholm-exergi-normal-2026"`). En policy UTAN detta fält gör inget
dedupliceringsanspråk alls och omfattas inte av reverse-regeln — det är den legitima vägen
för en framtida, direkt leverantörsprodukt utan katalogmotsvarighet, utan att förlita sig på
"redan godkänd"-historik. Kontrollen blir då en ren bijektion utan undantag:

**Rättat P1 (granskning `2026-09-09-002`) — `bygg_ts()`s anropskontrakt var logiskt
omöjligt.** v11 löste #1 ovan genom att `bygg_ts()` alltid skulle anropa
`kontrollera_adapterpreflight` med det RIKTIGA, icke-tomma `adapterregister=ADAPTERREGISTER`
men en TOM katalog (`{"tariffs": []}`) — och sedan i samma stycke (nedan, "korrekt och
avsiktligt") medgav att riktning 1 DÅ ALLTID kastar för Stockholms post, eftersom
`next((t for t in rak_katalog["tariffs"] if t["id"] == katalog_id), None)` mot en tom lista
per definition aldrig hittar en träff. Det fanns alltså inget sätt att anropa `bygg_ts()`
utan att den kastade — funktionen hade inget körbart läge, trots att den redan är den
etablerade testvägen (`test_stockholm_exergi_kontrakt.py`, `test_generera.py` — verifierat
att `bygg_ts()` bara anropas från dessa tre testställen, aldrig från produktionskod).

**Löst genom att göra riktning 1 uttryckligen VILLKORAD på om en riktig katalog finns, i
stället för att låtsas ha en:** `rak_katalog` typas om till `dict | None`. Riktning 1
(katalogberoende: "pekar `ADAPTERREGISTER` på en verklig katalograd") körs BARA när
`rak_katalog is not None`. Riktning 2 (bijektionen: "gör varje policy med
`ersatter_katalograd` anspråk på en matchande adapterpost") körs ALLTID, oavsett
`rak_katalog`, eftersom den bara läser de byggda leverantörsfilernas egna policyer.
`bygg_ts_fran_katalog()` skickar den RIKTIGA katalogen och får därmed kvar den fulla
tvåvägskontrollen precis som i dag; `bygg_ts()` skickar `rak_katalog=None` och får en
UTTRYCKLIGEN SNÄVARE garanti (bara riktning 2) — inte en låtsad full bijektion som aldrig
kunde köras klart:

```python
def kontrollera_adapterpreflight(
    rak_katalog: dict | None,
    byggda_leverantorer: dict[str, dict],
    policyregister: dict[str, Tariffpolicy],
    adapterregister: dict[str, AdapterEntry],
) -> None:
    """Separat, injicerbar, körbar tvåvägskontroll — anropas EN gång av
    bygg_ts_fran_katalog() (rak_katalog=riktig katalog, full tvåvägskontroll)
    OCH bygg_ts() (rak_katalog=None, bara riktning 2 — se motivering ovan).
    Båda vägar delar _bearbeta_leverantorsfil(), se nedan, med SAMMA register
    hela vägen. Kastar ValueError på första fel; ändrar ingen katalog- eller
    leverantörsdata."""
    # Riktning 1: varje ADAPTERREGISTER-post pekar på en verklig, sammanhängande
    # kedja. Körs BARA när en riktig katalog finns — bygg_ts() (utan katalog)
    # kan per definition inte bevisa detta och hoppar över riktning 1 helt,
    # se den snävare-garanti-motiveringen ovan.
    for katalog_id, entry in (adapterregister.items() if rak_katalog is not None else []):
        rad = next((t for t in rak_katalog["tariffs"] if t["id"] == katalog_id), None)
        if rad is None:
            raise ValueError(f"ADAPTERREGISTER: {katalog_id} finns inte i katalogen")
        leverantor = byggda_leverantorer.get(entry.provider_id)
        if leverantor is None:
            raise ValueError(
                f"ADAPTERREGISTER: {katalog_id} anger provider_id={entry.provider_id!r}, "
                "men ingen sådan leverantörsfil är byggd"
            )
        prisarspost = next((p for p in leverantor["prisar"] if p.get("tariff_id") == entry.tariff_id), None)
        if prisarspost is None:
            raise ValueError(
                f"ADAPTERREGISTER: {katalog_id} anger tariff_id={entry.tariff_id!r} hos "
                f"{entry.provider_id!r}, men leverantören har ingen sådan prisårspost"
            )
        malpolicy = policyregister.get(entry.tariff_id)
        if malpolicy is None or entry.kravd_tackning not in malpolicy.tackning:
            raise ValueError(
                f"ADAPTERREGISTER: {katalog_id} pekar på {entry.tariff_id}, men "
                f"målpolicyn saknas eller täcker inte {entry.kravd_tackning!r}"
            )
        if prisarspost.get("policy", {}).get("ersatter_katalograd") != katalog_id:
            raise ValueError(
                f"ADAPTERREGISTER: {entry.tariff_id} saknar (eller har fel) "
                f"ersatter_katalograd — måste peka tillbaka på {katalog_id!r}"
            )

    # Riktning 2 (bijektionen): varje policy som GÖR anspråk på att ersätta en
    # katalograd (via ersatter_katalograd) måste ha EXAKT en matchande
    # ADAPTERREGISTER-post — annars kunde annual_forward-täckning aktiveras
    # utan att adapterkontrollen i riktning 1 någonsin kört för den.
    #
    # Rättat P1 (granskning 2026-09-09-001): nyckeln var tidigare bara
    # entry.tariff_id — AdapterEntry bär uttryckligen provider_id också,
    # men det tappades i denna riktning. Två byggda leverantörer med SAMMA
    # tariff_id, där bara den ena (provider_id, tariff_id)-posten faktiskt
    # är adaptermappad, skulle ha fått den ANDRA leverantörens markör
    # felaktigt kvitterad av samma tariff-ID. Nyckla i stället på HELA
    # (provider_id, tariff_id, ersatt_katalog_id)-relationen.
    adapterade_mal = {
        (entry.provider_id, entry.tariff_id, katalog_id)
        for katalog_id, entry in adapterregister.items()
    }
    for provider_id, leverantor in byggda_leverantorer.items():
        for prisarspost in leverantor["prisar"]:
            policy = prisarspost.get("policy") or {}
            ersatt_id = policy.get("ersatter_katalograd")
            if ersatt_id is None:
                # En policy UTAN ersatter_katalograd gör inget
                # dedupliceringsanspråk — en framtida direkt
                # leverantörsprodukt med annual_forward men utan
                # katalogmotsvarighet är alltså uttryckligen TILLÅTEN,
                # utan historiska "redan godkänd"-undantag.
                continue
            nyckel = (provider_id, prisarspost.get("tariff_id"), ersatt_id)
            if nyckel not in adapterade_mal:
                raise ValueError(
                    f"{provider_id}/{prisarspost.get('tariff_id')}: policy har "
                    f"ersatter_katalograd={ersatt_id!r} men ingen ADAPTERREGISTER-post "
                    "pekar på exakt denna (provider_id, tariff_id, katalog_id)-relation"
                )


def bygg_ts_fran_katalog(katalog, ..., policyregister=POLICYREGISTER, adapterregister=ADAPTERREGISTER):
    leverantorer = _bygg_leverantorer(filer, policyregister=policyregister)  # redan byggd tidigare i funktionen
    kontrollera_adapterpreflight(katalog, leverantorer, policyregister, adapterregister)
    ur_katalogen = godkanda(katalog, policyregister=policyregister)  # §6a.3, samma injicerade register
    # ... resten av funktionen oförändrad; leverantörsfilerna (inkl.
    # stockholm-exergi-2026, nu med utökad policy) byggs som i dag i
    # _bygg_leverantorer(), FÖRE katalogloopen och FÖRE preflighten.


def bygg_ts(filer, ..., policyregister=POLICYREGISTER, adapterregister=ADAPTERREGISTER):
    leverantorer = _bygg_leverantorer(filer, policyregister=policyregister)
    kontrollera_adapterpreflight(None, leverantorer, policyregister, adapterregister)
    # ... resten av funktionen oförändrad.
```

**Rättat P1 (granskning `2026-09-09-002`, ersätter v11:s självmotsägande "korrekt och
avsiktligt"-resonemang) — `bygg_ts()` har nu ett körbart, uttryckligen SNÄVARE
anropskontrakt.** `bygg_ts()` anropas ALLTID med det verkliga, injicerade
`adapterregister=ADAPTERREGISTER` (produktionsdefault) precis som `bygg_ts_fran_katalog()` —
men med `rak_katalog=None` i stället för en låtsad tom katalog. Riktning 1 hoppas då över
HELT (ovan) i stället för att iterera noll katalograder och oundvikligen kasta
`"finns inte i katalogen"` för Stockholms adapterpost, som v11:s design gjorde. Riktning 2
körs OFÖRÄNDRAT och läser bara de byggda leverantörsfilernas egna policyer — den upptäcker
alltså fortfarande en policy som gör anspråk på `ersatter_katalograd` utan en matchande
adapterpost, oavsett om anropet kom via `bygg_ts()` eller `bygg_ts_fran_katalog()`.

Konsekvensen är en MEDVETET avgränsad garanti, inte en fullständig bijektion: `bygg_ts()`
(leverantörsfiler utan katalog) kan inte självständigt bevisa att en `ADAPTERREGISTER`-post
pekar på en verklig katalograd, eftersom den katalograden per definition inte finns i dess
anrop — det ansvaret vilar helt på `bygg_ts_fran_katalog()`, som är den enda vägen som någonsin
kör riktning 1 mot produktionsregistret (och därmed den enda vägen som får leverera en
katalogberoende adapter som Stockholms).

**Rättat P2 (granskning `2026-09-09-003`) — "FULLT verifierad (båda riktningarna, ingen
avgränsning)" var en överdrift.** v12 påstod att `bygg_ts()` var fullt verifierad i BÅDA
riktningarna för leverantörsfiler UTAN `ersatter_katalograd` — men riktning 1
(`kontrollera_adapterpreflight(rak_katalog=...)`s katalog-mot-adapterregister-genomgång)
hoppas OVILLKORLIGEN ÖVER när `rak_katalog=None`, oavsett vad den enskilda leverantörsfilens
policy innehåller — det finns ingen leverantörsfilsberoende gren som "aktiverar" riktning 1
för `bygg_ts()`. Korrekt formulering: `bygg_ts()` kör ENDAST riktning 2
(`_bearbeta_leverantorsfil()`s egen policykontroll, nedan) — för HELA sin leverantörsfilsmängd,
inte bara filer utan `ersatter_katalograd`. Riktning 1 är och förblir `bygg_ts_fran_katalog()`s
ensamma ansvar.

`_bearbeta_leverantorsfil()` (den funktion som faktiskt bygger en leverantörs `prisar`-lista,
och som VERIFIERAT används av BÅDE `bygg_ts()` och `bygg_ts_fran_katalog()`) läser INTE
`ersatter_katalograd` från katalog-JSON — den läser policyn för varje prispost via
`kontrollera_leverantorsfilsgrind(tariff_id, aktiveringslage, register=policyregister)`
(`generera.py` rad 46–63, `_policy_till_json()`), dvs. från det injicerade `policyregister`
(`policyregister.py`), precis som §6a.3 redan kräver för `kravda_falt`/`tackning`. **Rättat P2
(granskning `2026-09-09-003`) — v12 påstod felaktigt att `ersatter_katalograd` lästes "från
katalog-JSON:s policydeklaration".** Katalog-JSON:n är inte ens ett parameter till
`_bearbeta_leverantorsfil()` — `ersatter_katalograd` når funktionen uteslutande som ett fält
på den `Tariffpolicy`-instans `policyregister.py` returnerar, samma väg som varje annat
policyfält. Inget separat kodpar krävs för de två anropsvägarna, eftersom `ersatter_katalograd`
är REN DATA på policyn, inte ett kontrollflöde.

Kastar (`raise`) om registret pekar på en katalograd som inte finns, en leverantör/prisårspost
som inte finns, en målpolicy som saknas/inte täcker `annual_forward`, eller en policy som gör
anspråk på att ersätta en katalograd utan en matchande, provider-specifik adapterpost
(riktning 2) — aldrig en tyst utebliven rad. `godkanda()`/katalogloopen rörs INTE av
`ADAPTERREGISTER`-kontrollen i sig — den körs som en separat preflight FÖRE `godkanda()`
anropas, med samma injicerade `policyregister` som §6a.3 redan kräver.

**Rättat P1 #2 — ingen verklig dispatch fanns:** v7 sa att leverantörsfilens prispost
"visserligen" får policyn bifogad men inte `_kraver_kontrakt` — så `kontraktsgatadPolicy()`
(`besparingsvarde.ts`) skulle fortsätta returnera `undefined` och `beraknaBesparingsvarde`
fortsätta på legacyvägen, HELT OAVSETT att policyn nu (via 6a.4 #1) har `annual_forward`.
Att bara lägga täckningen i policyn ändrar alltså inte vilken kod som faktiskt körs.

Lösningen ÅTERANVÄNDER den redan befintliga `_kraver_kontrakt`-markören — samma mekanism
som redan tvingar VARJE annan kontraktsgated tariff (Sandviken m.fl.) genom
`beräkna_arskostnad_med_kontrakt`-fasaden i stället för den nakna motorn — i stället för
att hitta på ett nytt, parallellt dispatch-fält: `_bearbeta_leverantorsfil()`
(`generera.py`) sätter `_kraver_kontrakt: True` på Stockholms prispost NÄR dess policy (efter
6a.4 #1s utökning) täcker `annual_forward`, precis som katalogvägens
`kontrollera_aktiveringsgrind` redan gör för nya katalogtariffer. Detta är den enda
ändringen som krävs för dispatch: `kontraktsgatadPolicy()` returnerar då policyn i stället
för `undefined`, och `beraknaBesparingsvarde` väljer automatiskt kontraktsgrenen — ingen ny
`AdapterEntry`-diskriminator eller `annual_inverse`-krav behövs för själva dispatchen (den
löser bara vilken KATALOGRAD som ska hoppas över, se #1 ovan).

**Rättat P1 #3 — årsindatan var inte representerad:** dagens årsfasad tar
`mwh_kallt_per_manad` och ETT enda `returtemp_c` som fria argument — ett tal används för
ALLA vintermånader, och `Tariffpolicy` förbjuder dubblerade `kravda_falt.nyckel`, så de
befintliga månadsvisa `kall_energi_mwh`/`returtemperatur_c`-kraven (redan bundna till
`monthly`-omfattningen) kan inte återanvändas rakt av för en ENDA årsvis samlad indata.

**Rättat P1 (granskning `2026-09-08-008`) — EN modell, inte två motsägande.** v8 kallade
modellen omväxlande "17 nya `KravPost`" (denna sektions rubrik) och rekommenderade samtidigt
tvåserielösningen nedan — batchplanen upprepade "17 nya KravPost" separat. Det är den
tvåskalar-plus-tolvskalar-modellen (17 enskilda `KravPost`) OCH tvåserielösningen som är TVÅ
OLIKA API:n med olika UI-/validerings-/bindningsbehov; de kan inte båda stå kvar som möjliga
val. **Vald modell, den enda: två serie-`KravPost`**, inte 17 skalära:

- `KravPost(nyckel="kall_energi_mwh_arsserie", vardetyp="number_series", antal_varden=12,
  rullande=True, kravs_for=("annual",))` — `IndataPost.varde` är en 12-elements
  `Sequence[float]` i kalenderordning (januari–december). `antal_varden=12` (§6a.2) gör
  längdkravet deklarativt i stället för att förlita sig på att `rullande=True` råkar tillåta
  serier.
- `KravPost(nyckel="returtemperatur_c_vintermanader", vardetyp="number_series",
  antal_varden=5, rullande=True, kravs_for=("annual",))` — exakt 5 element, ordnade
  november–mars (samma vintermånader som redan gäller för det befintliga `monthly`-kravet).
- Båda seriekraven valideras i `harled_resultatstatus` via `antal_varden` (§6a.2) INNAN de
  binds — en serie av fel längd BLOCKERAR, mappas aldrig till fel månad genom att bara
  zippa index.
- **Två nya statiska `Tariffpolicy`-bindningar (saknades helt i v8, P1):**
  `kallenergi_arsserie_bindning: str | None = None` och
  `returtemperatur_arsserie_bindning: str | None = None` (mirror
  `kallenergiArsserieBindning`/`returtemperaturArsserieBindning` i TS — mappningsraderna i
  §6a.1s tabell). Utan dessa skulle serierna träffa årsfasadens GENERELLA `falt`-loop, som
  uttryckligen kastar för seriepost — precis samma princip som `kapacitet_band_bindning`
  (§6a.2) och `kapacitet_multiplikator_bindning` (§6a.3): en bindning pekar UT vilket
  validerat fält som är motorns specialargument, den generiska `falt`-loopen hoppar
  uttryckligen över alla tre bindna fälten (`kb`, `kapacitet_band_bindning`,
  `kapacitet_multiplikator_bindning`, och nu `kallenergi_arsserie_bindning`/
  `returtemperatur_arsserie_bindning`) när den bygger den numeriska `falt`-dictionaryn.
- **Effektkravets omfattning breddad (saknades i v8, P1):** det befintliga
  `debiterbar_effekt_kw`-kravet (redan bundet via `kapacitet_bindning` för
  `monthly_invoice`) är i dag märkt ENDAST `kravs_for=("monthly",)`. Stockholms utökade
  policy lägger `"annual"` till SAMMA post (`kravs_for=("monthly", "annual")`) i stället för
  att duplicera ett nytt, separat effektkrav med en annan nyckel — samma leverantörsvärde
  gäller båda omfattningarna, och `Tariffpolicy` förbjuder ändå dubblerade nycklar.
- Kontraktsfasadens `berakna_arskostnad_med_kontrakt`-motsvarighet för Stockholm läser de
  två bundna serierna (via `kallenergi_arsserie_bindning`/`returtemperatur_arsserie_bindning`,
  ALDRIG genom att fritt läsa en hårdkodad nyckel eller "Stockholm-motsvarigheten läser vissa
  nycklar" — det generiska bindningsmönstret gäller identiskt för alla framtida tariffer med
  samma behov) och konstruerar `mwh_kallt_per_manad`/en NY
  `returtemp_c_per_manad: dict[int, float]`-parameter till den lågnivåkod som redan
  periodiserar per månad — det befintliga enskalär-`returtemp_c`-argumentet ANVÄNDS INTE
  för denna väg; `_arskostnad_for_kontraktfasad`/TS-motsvarigheten får en ny, valfri
  `returtemp_c_per_manad`-parameter som (när satt) används i stället för det enskalära
  argumentet för exakt de fem vintermånaderna. Inga parallella fria argument får kringgå
  policyn för denna tariff.

**Fail-closed regel för före/efter i besparingsberäkningen (saknades helt i v8, P1):**
`beraknaBesparingsvardeKontrakt` (`besparingsvarde.ts`) använder i dag SAMMA `IndataPost`-
karta för både före- och efterkostnaden, medan de syntetiska månadsmängderna (`fordelaEnergi`)
KRYMPER i efterfallet med den påverkbara energins minskning. Om Stockholms 12 kallenergivärden
hölls OFÖRÄNDRADE mellan de två anropen skulle ett eftermånads totalenergi kunna bli MINDRE än
den ursprungliga kallenergin för samma månad — motorn skulle då räkna en NEGATIV mängd normal
(varm) energi, ett fysiskt orimligt resultat. Ingen leverantörskälla ger en verifierad regel
för hur kallenergin ska skalas om mellan ett fiktivt före- och eftertillstånd (kallenergin är
en fastighetsspecifik mätserie, inte en tariffparameter som kan härledas ur besparingsgraden).
**Beslut:** Stockholms årsprodukt kan ge en UPPSKATTAD AKTUELL årskostnad (ett enda
`beraknaArskostnadMedKontrakt`-anrop med de verkliga 12 kallenergivärdena, `noggrannhet:
snapshot`, ingen krympning inblandad), men EXKLUDERAS explicit från
besparingsvärderingsflödet (`kostnadFore`/`kostnadEfter`-paret i `beraknaBesparingsvarde`)
tills en källmässigt försvarbar transformationsregel finns — `beraknaBesparingsvardeKontrakt`
kastar ett tydligt, typat fel (`Produktbegransning`, se nedan — inte `KontraktBlockerat`,
eftersom detta inte är en kunddatalucka utan en produktbegränsning) om anroparen efterfrågar
en besparingsberäkning för en tariff vars policy inte stödjer besparing. `0 <= kallenergi[m]
<= totalenergi[m]` valideras ändå för VARJE månad `m` i det enkla uppskattningsflödet, som
ett generellt, icke-Stockholm-specifikt sanity-krav på alla framtida `number_series`-bundna
kallenergikrav.

**Rättat P1 (granskning `2026-09-09-011`) — det utlovade "typade felet" hade ingen klass,
konstruktor, guard eller UI-mappning, och dokumenten motsade varandra om huruvida det VAR
`KontraktBlockerat`.** Löst med en egen, konkret feltyp — `KontraktBlockerat` betyder
"kunden kan lösa detta genom att fylla i fler/rättare fält"; `Produktbegransning` betyder
"produkten stödjer inte alls denna beräkning för den här tariffen ännu, oavsett kundindata":

```ts
// besparingsvarde.ts
export type ProduktbegransningOrsak = 'besparing_ej_stodd';

export class Produktbegransning extends Error {
  constructor(
    public readonly tariffId: string,
    public readonly orsak: ProduktbegransningOrsak
  ) {
    super(`${tariffId}: produkten stöder inte denna beräkning (${orsak})`);
    this.name = 'Produktbegransning';
  }
}
```

**Rättat P1 (granskning `2026-09-09-012`) — ingen Python-produktkonsument av det här slaget
finns.** v18 uppfann en Python-klass i en påstådd `besparingsvarde.py`, men ingen sådan
Python-produktmodul finns i vare sig `enkey-agents` eller `neptune_academy` — Python-sidans
tariffmotor (`resultatkontrakt.py`/`faktura.py`/`justeringar.py`) exponerar
kostnadsberäkning, inte en besparingsvärderare med före/efter-fakturor; det produktbeteendet
existerar bara i `besparingsvarde.ts` (kalkylatorns frontend-lager). `Produktbegransning`
är därför TYPESCRIPT-ONLY i den här planen. Om en verklig Python-konsument av samma
besparingsmodell senare införs (utanför denna dokumentationsetapps scope) ska den då få sin
egen, verkligt existerande fil och sina egna tester — inte en fiktiv fil i förväg.

**Konkret guard, i den BEFINTLIGA, verkliga femparametersfunktionen
`beraknaBesparingsvardeKontrakt` (`besparingsvarde.ts` rad 251–259:
`(args: BesparingsvardeArgs, leverantor: any, prisar: any, kapacitetGolv: number, policy:
Tariffpolicy)`, anropad med alla fem argument av `beraknaBesparingsvarde` rad 361), FÖRST —
innan indata byggs eller valideras (spärren gäller produkten, inte kundens data). v18:s
tvåparametersskiss `(args, prisar)` tappade `leverantor`/`kapacitetGolv`/`policy`, som resten
av funktionskroppen redan behöver — guarden läggs i stället in som första sats i den
OFÖRÄNDRADE signaturen, och använder parametern `policy` som redan finns upplöst (ingen ny
`kontraktsgatadPolicy(prisar)`-uppslagning krävs, till skillnad från fristående funktioner
som `stodjerAktuellArskostnad` nedan som INTE har `policy` som parameter):**

```ts
function beraknaBesparingsvardeKontrakt(
  args: BesparingsvardeArgs,
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  leverantor: any,
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  prisar: any,
  kapacitetGolv: number,
  policy: Tariffpolicy
): Besparingsvarde {
  if (policy.stodjerBesparing !== true) {
    throw new Produktbegransning(prisar.tariff_id, 'besparing_ej_stodd');
  }
  // ... befintlig kropp (energyProvenance/kapacitet-validering, före/efter-anrop),
  // oförändrad i övrigt — se resten av funktionen ovan i besparingsvarde.ts
}
```

`policy.stodjerBesparing !== true` (inte `!== false`) är AVSIKTLIGT fail-closed — se
`stodjerBesparing`-resolvern nedan (rättar P1, granskning `2026-09-09-012`, fynd 4: den
tidigare `!== false`-varianten var fail-open).

**UI-mappning:** `KalkylatorPage.tsx` fångar `Produktbegransning` SEPARAT från
`KontraktBlockerat` och visar ett eget, icke fältnära meddelande ("Den här tariffen stödjer
ännu inte en besparingsberäkning — kontakta Enkey för mer information") i stället för
`KontraktBlockerat`s fältnära "fyll i X"-formulärfel, eftersom det inte finns något fält
användaren kan fylla i för att lösa det.

**Test (rättat P1, granskning `2026-09-09-012` — v18:s testtext använde `onskadTyp` på fel
typ):** ett DIREKT anrop till `beraknaBesparingsvarde({ totalMwh, paverkbarMwh,
besparingsgrad, leverantorId: 'stockholm-exergi', ... } satisfies BesparingsvardeArgs)` (INTE
`onskadTyp` — det fältet tillhör `KalkylatorInputs`, ett SKILT, sidnivå-objekt som
`calcResult`/`calcResultForOnskadTyp` bygger `BesparingsvardeArgs` UR, inte en egenskap på
`BesparingsvardeArgs` självt) kastar `Produktbegransning('stockholm-exergi-2026',
'besparing_ej_stodd')`; samma för Lidköping (§6a.7.7). Ett SEPARAT, sidnivå-test använder
`KalkylatorInputs.onskadTyp === 'besparing'` för att bevisa att `KalkylatorPage.tsx`s
`Produktbegransning`-fångst faktiskt nås via den riktiga sidvägen. Ett anrop för Sandviken
(kontraktsgated, `stodjerBesparing` explicit `true`, §6a.4 nedan) genomförs OFÖRÄNDRAT, utan
att kasta.

**GÄLLANDE KONTRAKT (rättat P1/P4/P5, granskning `2026-09-09-012`) — de två förmågorna är nu
helt oberoende, explicita `Tariffpolicy`-fält, båda EXPLICIT OPT-IN (fail-closed) för
kontraktsgatade tariffer.** Den tidigare kedjan av korrigeringar (granskningarna
`2026-09-08-009` genom `2026-09-09-011`, bevarad NEDANFÖR som historik/motivering, men INTE
längre normativ) prövade flera modeller — en enda `stodjerAktuellArskostnad`-flagga som även
agerade besparingsspärr (rättat 010), och sedan ett andra fält `stodjer_besparing` med
FAIL-OPEN default `True` (rättat HÄR, 012). Det gällande, aktuella kontraktet är:

```python
# resultatkontrakt.py, Tariffpolicy — GÄLLANDE fält (ersätter alla tidigare varianter ovan)
@dataclass(frozen=True)
class Tariffpolicy:
    ...
    stodjer_aktuell_arskostnad: bool = False  # explicit opt-in: kan denna policy besvara
                                               # "aktuell uppskattad årskostnad" i ETT anrop?
    stodjer_besparing: bool = False           # explicit opt-in: kan denna policy köra
                                               # kontraktsgated besparingsberäkningen (bär
                                               # DEN NYA IndataPost-kartan i sig)? FAIL-CLOSED
                                               # default (rättat P1, granskning
                                               # `2026-09-09-012`, fynd 4 — den tidigare
                                               # `True`-defaulten hade gett en ny
                                               # kontraktsgatad tariff besparingsstöd så fort
                                               # en utvecklare glömde deklarera fältet, tvärt
                                               # emot Ellens grundregel att bara faktiskt
                                               # påverkade kostnadskomponenter får räknas som
                                               # besparing)
```

```ts
// resultatkontrakt.ts, Tariffpolicy — GÄLLANDE mirror
export interface Tariffpolicy {
  ...
  stodjerAktuellArskostnad?: boolean; // default false vid frånvaro
  stodjerBesparing?: boolean;         // default false vid frånvaro — FAIL-CLOSED
}
```

```ts
export function stodjerAktuellArskostnad(prisar: GenereradPrisarspost): boolean {
  const gated = kontraktsgatadPolicy(prisar); // enda tillåtna rådatagrind
  return gated?.policy.stodjerAktuellArskostnad === true;
}

export function stodjerBesparing(prisar: GenereradPrisarspost): boolean {
  const gated = kontraktsgatadPolicy(prisar);
  if (!gated) return true; // icke-kontraktsgatade/legacy-tariffer: helt opåverkade av detta
                            // fält, de går sin egen väg och frågar aldrig policy.stodjerBesparing
  return gated.policy.stodjerBesparing === true; // FAIL-CLOSED: `undefined`/`false` blockerar,
                                                  // bara ett explicit `true` öppnar
}
```

`policyregister.py` sätter EXPLICIT värde på båda fälten för VARJE kontraktsgatad policy —
inget kontraktsgatad tariff får förlita sig på ett underförstått default:

| Tariff | `stodjer_aktuell_arskostnad` | `stodjer_besparing` |
|---|---|---|
| Sandviken (`sandviken-energi-*`) | `False` (default, ingen "aktuell årskostnad"-väg) | **`True`** (explicit opt-in — redan i produktion, källförsvarbar besparingsmodell) |
| Stockholm Exergi (`stockholm-exergi-2026`) | **`True`** (via `kallenergiArsserieBindning`, §6a.4 nedan) | `False` (explicit opt-out — ingen källförsvarbar före/efter-regel för kallenergiserien, §6a.4 "Beslut") |
| Lidköping Energi (båda raderna, §6a.7) | **`True`** (via de tre serierna) | `False` (explicit opt-out — samma skäl som Stockholm, §6a.7.7) |
| Icke-kontraktsgatad/legacy-tariff | N/A — `kontraktsgatadPolicy()` returnerar `undefined`, ingen av flaggorna läses | N/A — `stodjerBesparing()` returnerar `true` direkt utan att läsa policy |

De två fälten är helt oberoende: en framtida tariff kan i princip ha
`stodjer_aktuell_arskostnad=True` OCH `stodjer_besparing=True` samtidigt utan att någon
kodgren behöver särskiljas för det fallet — de facto redan sant för en tariff som INTE är
serie-baserad (varken Sandviken, Stockholm eller Lidköping är i det läget i dag, men
mekanismen lägger ingen hake i vägen för en framtida sådan tariff).

**Test (fail-closed, krävt av granskning `2026-09-09-012`, fynd 4):** en policy där
`stodjer_besparing` HELT SAKNAS i genererad JSON → `stodjerBesparing() === false`
(inte `true`); en policy med `stodjer_besparing: false` explicit → `false`; en policy med
`stodjer_besparing: true` explicit → `true`; Sandvikens genererade policy (verklig data) →
`true`; Stockholms/Lidköpings genererade policyer → `false`. Samma par upprepas för
`stodjerAktuellArskostnad`, och ett test bevisar att de två fälten kan sättas oberoende av
varandra (fyra kombinationer, alla giltiga).

Ny, namngiven funktion `beraknaArsprodukt(underlag: Tariffberakningsunderlag):
ArsprodukResultat` i `besparingsvarde.ts` (parametertypen smalnas nedan, se
`argsFranInputs`) — den GEMENSAMMA produktentrypunkten för "aktuell årskostnad", i dag
använd av Stockholm OCH Lidköping (§6a.7.7); den tar INGEN `onskadTyp`-parameter, eftersom
den bara har en gren att dispatcha till, och den kontrollerar `stodjerAktuellArskostnad`
(INTE `stodjerBesparing` — de två guarderna sitter på sina respektive entrypunkter:
`beraknaArsprodukt` kontrollerar bara "aktuell årskostnad"-förmågan, medan
`beraknaBesparingsvardeKontrakt` ovan kontrollerar bara besparingsförmågan; att blanda dem
skulle fela precis det P1-fynd, granskning `2026-09-09-012`, punkt 5, som identifierade att
en tidigare batchplansskiss lät `beraknaArsprodukt` kontrollera `stodjerBesparing` — det
hade blockerat precis den aktuella årskostnad Stockholm/Lidköping SKA kunna få trots att de
har `stodjerBesparing=False`).

```ts
export type ArsprodukResultat =
  { typ: 'aktuell_arskostnad'; kostnad: number; leverantor: string; prisar: number;
    kapacitetKw: number; status: Resultatstatus }; // Stockholm- OCH Lidköpingsfallet —
                                                     // samma resultattyp för båda, ingen
                                                     // tariffspecifik gren i returtypen
```

Ny, delad hjälpfunktion `byggKontraktIndata(policy: Tariffpolicy, prisar: GenereradPrisarspost,
kapacitetKw: number, policyFalt: Record<string, PolicyInputValue>):
Map<string, IndataPost>` i `besparingsvarde.ts` — anropar `byggIndataFranPolicy` (§6a.2, punkt
2) och lägger DÄREFTER in kapacitetsbindningen i SAMMA karta (samma ordning/validering
`beraknaBesparingsvardeKontrakt` redan hade). Denna hjälpfunktion används av BÅDA
`beraknaArsprodukt` (nedan) och `beraknaBesparingsvardeKontrakt` — den enda delade
byggnadslogiken, ingen tredje parallell dispatch.

---

*Historik/motivering bevarad för spårbarhet (INTE normativ — det gällande kontraktet står
ovan). Reglerna nedan citerar tidigare, sedan ERSATTA modeller och gäller inte längre
bokstavligt; de förklarar VARFÖR den gällande designen ser ut som den gör.*

De tidigare granskningarna `2026-09-08-009` (namngiven produktentry saknades),
`2026-09-09-001` (tre-grensdispatch gjorde besparing onåbar), `2026-09-09-002` (v11:s
tre-grensdesign var ouppnåelig eftersom `calcResult` aldrig anropar `beraknaArsprodukt`),
`2026-09-09-003` (`stodjerAktuellArskostnad` hade tre-fyra motsägande definitioner och läste
rådata direkt), `2026-09-09-004` (`gated?.kallenergiArsserieBindning` läste fel objektsväg —
ska vara `gated?.policy.kallenergiArsserieBindning`) och `2026-09-09-010` (förmågan var en
indirekt kontroll av Stockholms specifika bindning, vilket gjorde Lidköpings "aktuell
årskostnad" onåbar — löst genom det EXPLICITA `stodjer_aktuell_arskostnad`-fältet) ledde
tillsammans fram till: en enda, delad `beraknaArsprodukt`-entrypunkt; en delad
`byggKontraktIndata`-hjälpare; och ett explicit policyfält i stället för en indirekt
bindningskontroll. Granskning `2026-09-09-011` identifierade därefter (P2) att SAMMA flagga
inte borde betyda både "stödjer aktuell årskostnad" och "stödjer inte besparing" — löst med
det andra, oberoende fältet `stodjer_besparing`. Granskning `2026-09-09-012` (denna version)
rättade sedan att det andra fältets FÖRSTA utkast hade fail-open default `True` i stället
för fail-closed `False`, och att en tidig batchplansskiss lät `beraknaArsprodukt` kontrollera
fel förmåga (`stodjerBesparing` i stället för `stodjerAktuellArskostnad`).

fälten är nu helt oberoende: en framtida tariff kan i princip ha
`stodjer_aktuell_arskostnad=True` OCH `stodjer_besparing=True` samtidigt, utan att någon
kodgren behöver särskiljas för det fallet.

Ny, namngiven funktion `beraknaArsprodukt(underlag: Tariffberakningsunderlag):
ArsprodukResultat` i `besparingsvarde.ts` (parametertypen smalnas nedan, se
`argsFranInputs`) — den GEMENSAMMA produktentrypunkten för "aktuell årskostnad", i dag
använd av Stockholm OCH Lidköping (§6a.7.7); den tar
INGEN `onskadTyp`-parameter, eftersom den bara har en gren att dispatcha till.

**Rättat P1 igen (granskning `2026-09-09-007`) — den utskrivna kroppen kompilerade
INTE.** En isolerad `npx tsc --noEmit --strict --skipLibCheck` mot de verkliga produkttyperna
gav fem fel (`TS2339` ×2, `TS2345`, `TS2554`, `TS18047`): `prisar.id` finns inte (fältet
heter `tariff_id`); `forkontrolleraPolicyIndata` fick den råa `Record<string,
PolicyInputValue>` i stället för den byggda `ReadonlyMap<string, IndataPost>` —
`byggKontraktIndata` måste köras FÖRE förkontrollen, inte efter; det kombinerade felkastet
använde `'invalid_capacity'` med `{ saknade, ogiltiga } as any`, vilket motsäger §6a.2 punkt
6:s egna, redan beslutade tvåkasts-modell (`'missing_policy_fields'`/`'invalid_policy_fields'`,
inga casts); `beraknaArskostnadMedKontrakt` anropades med fel ordning/antal argument (tre i
stället för `(prisar, policy, indata, ar, mwhPerManad, opts?)`, och årsenergin fördelades
aldrig över tolv månader); `resultat.kostnad.summaInkl` dereferererade `Kostnad | null` utan
att först hantera `status.fullstandighet === 'blocked'`/`kostnad === null`; och
`prisar.leverantor` finns inte på `GenereradPrisarspost` — `leverantor.namn` måste komma
från `valjLeverantorOchPrisar`-destruktureringen.

**Löst genom att skriva hela kroppen på nytt, verifierad som EN kompilerbar helhet** (inte
bara en isolerad kontroll av `argsFranInputs`): destrukturerar `{ leverantor, prisar }`,
använder `prisar.tariff_id`, bygger `indata` via `byggKontraktIndata` FÖRE förkontrollen,
gör de två fältnära förkontrollkasten utan cast, fördelar årsenergin över tolv månader med
`fordelaEnergi(totalMwh).totalt` innan fasaden anropas, och avsmalnar `KontraktResultat`
innan kostnaden läses — i SAMMA ordning och med SAMMA orsaker som den befintliga
`beraknaBesparingsvardeKontrakt` redan använder (verifierat, `besparingsvarde.ts` rad
250–300+: gate → energyProvenance → ändlig positiv energi → kapacitet närvarande → kapacitet
ändlig/heltal/≥golv → policyns fältnära förkontroll → fasadanrop → blocked-guard):

```ts
export function beraknaArsprodukt(underlag: Tariffberakningsunderlag): ArsprodukResultat {
  const { leverantor, prisar } = valjLeverantorOchPrisar(underlag.leverantorId) as {
    leverantor: { namn: string };
    prisar: GenereradPrisarspost;
  };
  const tariffId = prisar.tariff_id;

  // 1. Gate: samma auktoritativa spärr som §6a.4 "Beslut" — domänlagret litar
  // aldrig på att anroparen (sidwrappern) redan kontrollerat detta.
  if (!stodjerAktuellArskostnad(prisar)) {
    throw new KontraktBlockerat(tariffId, 'unsupported_input_mode');
  }
  const gated = kontraktsgatadPolicy(prisar)! as { policy: Tariffpolicy; harAnnualInverse: boolean };
  // icke-null: stodjerAktuellArskostnad === true garanterar gated !== undefined
  // (samma reglerorsak, ingen ny risk).

  // 2. Bekräftad MWh-proveniens FÖRST (samma ordning som beraknaBesparingsvardeKontrakt).
  if (underlag.energyProvenance !== 'confirmed_mwh') {
    throw new KontraktBlockerat(tariffId, 'missing_energy');
  }
  // 3. Ändlig, positiv energi.
  if (!Number.isFinite(underlag.totalMwh) || underlag.totalMwh <= 0) {
    throw new KontraktBlockerat(tariffId, 'invalid_energy');
  }
  // 4. Kapacitet närvarande.
  if (underlag.kapacitetKw === undefined) {
    throw new KontraktBlockerat(tariffId, 'missing_capacity');
  }
  // 5. Kapacitet ändlig, heltal, och ≥ tariffgolvet (kapacitetsGolv, besparingsvarde.ts
  // rad 55 — samma golvfunktion beraknaBesparingsvardeKontrakt redan anropar).
  const golv = kapacitetsGolv(prisar);
  if (!Number.isFinite(underlag.kapacitetKw) || !Number.isInteger(underlag.kapacitetKw)
      || underlag.kapacitetKw < golv) {
    throw new KontraktBlockerat(tariffId, 'invalid_capacity');
  }
  // Från denna punkt är underlag.kapacitetKw avsmalnat till `number` (inte `number |
  // undefined`) — TypeScript's control-flow-analys accepterar det direkt nedan utan cast.
  const kapacitetKw: number = underlag.kapacitetKw;

  // 6. Bygg indata FÖRST — samma delade hjälpfunktion som
  // beraknaBesparingsvardeKontrakt använder (§6a.4, "Löst genom att smalna..."-stycket).
  // En tom karta representeras EXPLICIT (inte en non-null-cast) om formuläret inte
  // skickat några policyfält.
  const policyFalt = underlag.policyFalt ?? {};
  const indata = byggKontraktIndata(gated.policy, prisar, kapacitetKw, policyFalt);

  // 7. Policyns fältnära förkontroll (§6a.2, punkt 6) körs på den BYGGDA
  // `ReadonlyMap<string, IndataPost>`, INTE på det råa `policyFalt`-objektet — två
  // separata kast, eftersom varje anrop bara kan bära EN orsak (samma prioritetsordning
  // som §6a.2 punkt 6 redan beskriver: `saknade` vinner om båda listorna är icke-tomma).
  const { saknade, ogiltiga } = forkontrolleraPolicyIndata(gated.policy, prisar, indata, 'annual');
  if (saknade.length > 0) {
    throw new KontraktBlockerat(tariffId, 'missing_policy_fields', { saknadeFalt: saknade });
  }
  if (ogiltiga.length > 0) {
    throw new KontraktBlockerat(tariffId, 'invalid_policy_fields', { ogiltigaFalt: ogiltiga });
  }

  // 8. Fördela årsenergin över tolv månader (samma fördelningsfunktion
  // beraknaBesparingsvardeKontrakt redan använder, varmeprofil.ts) och anropa fasaden —
  // enda anropet till motorn.
  const mwhPerManad = fordelaEnergi(underlag.totalMwh).totalt;
  const resultat = beraknaArskostnadMedKontrakt(prisar, gated.policy, indata, prisar.ar, mwhPerManad);

  // 9. Samma mönster som beraknaBesparingsvardeKontrakt (besparingsvarde.ts rad 308–317):
  // energi/kapacitet/policyfält är redan förkontrollerade ovan, så ett 'blocked'-resultat
  // härifrån är ett oväntat konfigurationsfel i policyn, inte ett användarfel — kastas som
  // Error, inte KontraktBlockerat, och läses aldrig som en dereferens av `null`.
  if (resultat.status.fullstandighet === 'blocked' || resultat.kostnad === null) {
    throw new Error(
      `${tariffId}: kontraktet blockerade (${JSON.stringify(resultat.status)}) trots ` +
        'validerad energi, kapacitet och policyindata — kontrollera policyns kravdaFalt'
    );
  }
  const kostnad = resultat.kostnad;

  return {
    typ: 'aktuell_arskostnad',
    kostnad: kostnad.summaInkl,
    leverantor: leverantor.namn,
    prisar: prisar.ar,
    kapacitetKw,
    status: resultat.status, // status.noggrannhet bär 'snapshot'-proveniensen,
    // §6a.2:s harledResultatstatus-regler, ingen ny logik
  };
}
```

**Verifierat kompilerbart som helhet:** skissen ovan skrevs till en fristående scratch-fil
i `neptune-marketing`-katalogen (importerande de VERKLIGA `valjLeverantorOchPrisar`,
`kontraktsgatadPolicy`, `kapacitetsGolv`, `beraknaArskostnadMedKontrakt`, `fordelaEnergi`,
`Tariffpolicy`, `IndataPost`, `Resultatstatus`, `KontraktResultat`, `Kostnad`, med lokala
`interface`/`type`-deklarationer bara för de ännu ej implementerade planerade byggstenarna:
`GenereradPrisarspost`, `PolicyInputValue`, `PolicyValideringsFel`, den utökade
`KontraktBlockerat`, `stodjerAktuellArskostnad`, `forkontrolleraPolicyIndata`,
`byggKontraktIndata`, `Tariffberakningsunderlag`, `ArsprodukResultat`), och kontrollerad med
`npx tsc --noEmit --strict --skipLibCheck --target es2020` från
`neptune_academy/neptune-marketing` — **noll fel**. Scratch-filen låg i `neptune-marketing`
under körningen och togs bort direkt efteråt (`git status` bekräftat rent i det repot efter
borttagningen); ingen produktfil i något av de tre repona ändrades av kontrollen.

Steg 9:s exakta blocked-hantering och steg 7:s tvåkasts-`KontraktBlockerat`-väg följer §6a.2
punkt 6:s redan beslutade felform — koden ovan visar ORDNINGEN och att kartan avsmalnas
explicit, inte en ny orsakskod.

Besparing för Stockholm förblir uttryckligen BLOCKERAD, men genom den befintliga
`beraknaBesparingsvardeKontrakt`-guarden (§6a.4, "Beslut"-stycket) — INTE genom en gren i
`beraknaArsprodukt` som aldrig anropas av produktsidan. Besparing för Sandviken och alla
framtida kontraktstariffer UTAN Stockholms serie fortsätter gå genom `calcResult`s tre
`beraknaBesparingsvarde`-anrop, HELT OFÖRÄNDRAT av detta tillägg.

**Sidnivå-dispatch, en HELT SEPARAT resultattyp i stället för en omöjlig retrofit av
`KalkylatorResult`.** Verifierat att `KalkylatorResult` (`energiPotential.ts`) har
OBLIGATORISKA, icke-valfria numeriska fält `savingsMin`/`savingsMax`/`annualSavingsKr` samt
payback-/nettovärden som sidan renderar OVILLKORLIGT — "lämna dem `null`/utelämnade"
kompilerar inte mot dagens interface och stoppar inte den befintliga resultatsidan från att
FÖRSÖKA visa besparing. **Rättat P2 (granskning `2026-09-09-007`) — dokumenten växlade
mellan "`calcResult` självt ändras inte" och att beskriva en intern refaktorering till att
anropa `argsFranInputs`.** `calcResult`s PUBLIKA resultat och beräkningsbeteende
(fullständig poäng-/besparings-/rekommendationsberäkning, exakt samma utdata för samma
indata) förblir OFÖRÄNDRADE av detta tillägg — det är detta kontrakt som är stabilt, inte
funktionskroppen ordagrant. Dess INTERNA argumentbyggnad ändras (anropar den delade
`argsFranInputs` i stället för att duplicera scope-/provenienslogiken tre gånger inline, se
nedan). I stället en NY, tunn wrapper-funktion i `energiPotential.ts`:

**Rättat P1 (granskning `2026-09-09-002`) — `onskadTyp` hade TVÅ källor.** v11:s
`calcResultForOnskadTyp(inputs, onskadTyp)` tog `onskadTyp` som en EGEN parameter, SAMTIDIGT
som samma stycke krävde ett `KalkylatorInputs.onskadTyp`-fält satt av formuläret — två
källor till samma beslut som kunde säga emot varandra (anroparen kunde skicka
`onskadTyp:'aktuell_arskostnad'` medan `inputs.onskadTyp` var `'besparing'`, med odefinierat
vilken som gällde). **Löst genom att göra `KalkylatorInputs.onskadTyp` till den ENDA källan**
(kvarstår oförändrat i v13).

**Rättat P1 (granskning `2026-09-09-003`) — `argsFranInputs` var FORTFARANDE bara en
`...`-platshållare i v12, samma hål v11-granskningen redan bett om att stänga, och dess
deklarerade returtyp (`BesparingsvardeArgs`) tvingade fram påhittade besparingsfält för en
funktion som inte behöver dem.** Verifierat mot `besparingsvarde.ts` (rad 204–208):
`BesparingsvardeArgs` kräver `totalMwh`, `paverkbarMwh` OCH `besparingsgrad` som
icke-valfria fält — men Stockholms aktuella-årskostnad-beräkning behöver VARKEN
`paverkbarMwh` (det finns ingen "efter"-beräkning) ELLER `besparingsgrad` (det finns ingen
grad att applicera). Att låta `argsFranInputs` returnera `BesparingsvardeArgs` hade alltså
antingen krävt påhittade nollvärden (`paverkbarMwh: 0`, `besparingsgrad: 0` — data utan
mening, som denna agentinstruktion uttryckligen förbjuder att gissa fram) eller en
typomskrivning.

**Rättat P1 (granskning `2026-09-09-004`) — `argsFranInputs`-skissen refererade FYRA fält/
funktioner som inte finns i verklig kod.** Verifierat direkt mot `KalkylatorInputs`
(`energiPotential.ts`): interfacet har `energySystem`, `energyMwh?`, `energyScope?`,
`energyInputMode?`, `leverantorId?`, `kapacitetKw?`, `falt?` — INGET `rumsvarmeAngiven`,
INGET `totalMwh`, ingen fristående funktion `skalaUppRumsvarmeTillTotal(inputs)` och ingen
fristående funktion `mwhProvenansBekraftad(inputs)`; scope-uppskalningen och
proveniens-flaggan är i verkligheten INLINE-logik inuti `calcResult`s kropp (rad ~405–545),
inte separata, anropbara hjälpfunktioner.

**Rättat P1 igen (granskning `2026-09-09-005`) — v14:s skiss innehöll fortfarande tre
värden som inte finns i de verkliga unionerna (`energyScope === 'rumsvarme'`,
`energyInputMode === 'rumsvarme_andel'`, `energyInputMode === 'confirmed_mwh'`;
`EnergyScope` är i verkligheten `'total_incl_dhw'|'space_heat_excl_dhw'|
'purchased_hp_electricity'|'delivered_heat_from_hp'` och `EnergyInputMode` är
`'schablon'|'mwh'|'kr'` — TypeScript ger `TS2367` för alla tre) samt ett bokstavligt
no-op (`totalMwh = totalMwh`) i stället för den faktiska uppskalningsformeln. Provenienser
skulle därför ALDRIG bli `'confirmed_mwh'`, vilket hade blockerat Stockholm-produkten även
med korrekt MWh-indata. `calcResult`/batchplanen sa dessutom fortfarande att `calcResult`
"förblir oförändrat" och bygger alla tre argument INLINE — två separata kopior av exakt den
scope-/provenienslogik som skulle delas.

**Löst genom att skriva den VERKLIGA, kompilerbara koden** (kopierad ordagrant ur
`calcResult`s befintliga kropp, `energiPotential.ts` rad ~447–490 — samma variabelnamn,
samma villkor, ingen ny logik) och genom att låta `calcResult` faktiskt ANROPA
`argsFranInputs` i stället för att duplicera blocket:

```ts
export interface Tariffberakningsunderlag {
  totalMwh: number;
  leverantorId?: string;
  kapacitetKw?: number;
  falt?: Record<string, number>;
  policyFalt?: Record<string, PolicyInputValue>;
  energyProvenance?: 'confirmed_mwh';
}

// Verifierad kompilerbar mot dagens riktiga KalkylatorInputs/EnergyScope/
// EnergyInputMode/calcEnergyMwh/VARMVATTEN_ANDEL (npx tsc --noEmit --strict
// --skipLibCheck mot en skiss med samma import- och typkedja, 2026-09-09) — ENDA
// lokala tillägget är de PLANERADE, ännu ej implementerade fälten policyFalt/
// onskadTyp på KalkylatorInputs (samma status som i övriga §6a).
export function argsFranInputs(inputs: KalkylatorInputs): Tariffberakningsunderlag {
  const energyMwh = calcEnergyMwh(inputs); // exakt calcResults egen rad, oförändrad
  const userProvidedEnergy = inputs.energyMwh != null && inputs.energyMwh > 0;
  const anvanderTariff = inputs.energySystem === 'fjarrvarme';

  // Verbatim ur calcResult (energiPotential.ts rad ~447–460): scope
  // 'space_heat_excl_dhw' ger redan HELA rumsvärmetalet från
  // calcPåverkbarEnergi; beraknaBesparingsvarde/fordelaEnergi förutsätter i
  // stället TOTAL köpt värme inkl. varmvatten och drar av VARMVATTEN_ANDEL
  // som en del av sin egen uppdelning — därför skalas rumsvärmetalet upp
  // till motsvarande totalenergi (dela med (1 - VARMVATTEN_ANDEL)) innan det
  // skickas vidare, så fordelaEnergi ger tillbaka exakt det angivna talet.
  const rumsvarmeAngiven =
    anvanderTariff && userProvidedEnergy && inputs.energyScope === 'space_heat_excl_dhw';
  const totalMwh = rumsvarmeAngiven ? energyMwh / (1 - VARMVATTEN_ANDEL) : energyMwh;

  // Verbatim ur calcResult (rad ~480–487): proveniensen sätts ENDAST när
  // energyInputMode uttryckligen är 'mwh' OCH talet är ändligt och positivt
  // — inte bara "något positivt tal finns" (granskning 2026-09-07-001/-002).
  const mwhProvenansBekraftad =
    inputs.energyInputMode === 'mwh'
    && inputs.energyMwh != null && Number.isFinite(inputs.energyMwh) && inputs.energyMwh > 0;
  const energyProvenance = mwhProvenansBekraftad ? ('confirmed_mwh' as const) : undefined;

  return {
    totalMwh,
    leverantorId: inputs.leverantorId,
    kapacitetKw: inputs.kapacitetKw,
    falt: inputs.falt,
    policyFalt: inputs.policyFalt,
    energyProvenance,
  };
}
```

**`calcResult` ANROPAR nu `argsFranInputs` i stället för att duplicera blocket** (rättar
P1:s andra del: "två kopior av scope-/provenienslogiken"). Dess tre befintliga
`beraknaBesparingsvarde`-anrop (min/mid/max) lägger `paverkbarMwh`/respektive
besparingsgrad OVANPÅ samma bas i stället för att räkna om `totalMwh`/`energyProvenance`
separat tre gånger:

```ts
// I calcResult, EFTER poäng-/tier-beräkningen, i STÄLLET för det tidigare inline-blocket:
const bas = argsFranInputs(inputs);
const besparingsvarde = anvanderTariff
  ? beraknaBesparingsvarde({ ...bas, paverkbarMwh: påverkbarMwh, besparingsgrad: mid / 100 })
  : null;
const besparingsvardeMin = anvanderTariff
  ? beraknaBesparingsvarde({ ...bas, paverkbarMwh: påverkbarMwh, besparingsgrad: min / 100 })
  : null;
const besparingsvardeMax = anvanderTariff
  ? beraknaBesparingsvarde({ ...bas, paverkbarMwh: påverkbarMwh, besparingsgrad: max / 100 })
  : null;
// resten av calcResult (annualSavingsKr, andelAvNotanMin/Max, m.m.) OFÖRÄNDRAT.
```

`Tariffberakningsunderlag` är en STRUKTURELL DELMÄNGD av `BesparingsvardeArgs` (samma
fältnamn/typer för de fält de har gemensamt: `totalMwh`, `leverantorId`, `kapacitetKw`,
`falt`, `policyFalt`, `energyProvenance`) — `{ ...bas, paverkbarMwh, besparingsgrad }` är
därför ett typkorrekt `BesparingsvardeArgs`-objekt, inte ett separat, inkompatibelt schema.

**Rättat P1 (granskning `2026-09-09-007`) — `policyFalt` motsades mellan dokumenten.**
`batchplan-v15.md` (Batch 0, punkt 5) sa uttryckligen `KalkylatorInputs.policyFalt →
BesparingsvardeArgs.policyFalt`, nödvändigt för att `beraknaBesparingsvardeKontrakt` ska
kunna anropa `byggIndataFranPolicy`/`byggKontraktIndata` — medan DENNA sektion i v15 sa att
`BesparingsvardeArgs` var oförändrad och att `policyFalt` ignorerades tyst av
`beraknaBesparingsvarde`. Om fältet inte deklareras typsäkert på interfacet kan varken
`beraknaBesparingsvarde` eller dess kontraktsgren läsa det, och alla framtida
kontraktsgatade besparingsprodukter med band-/serie-/temperaturkrav (inklusive Lidköpings
nya nätmedelavkylningsjustering, §6a.7) saknar sin planerade indatakanal.

**Löst genom att göra `policyFalt` till ett ADDITIVT fält på `BesparingsvardeArgs`, samma
beslut i BÅDA dokumenten:**

```ts
export interface BesparingsvardeArgs {
  totalMwh: number;
  paverkbarMwh: number;
  besparingsgrad: number;
  leverantorId?: string;
  kapacitetKw?: number;
  falt?: Record<string, number>;
  energyProvenance?: 'confirmed_mwh';
  policyFalt?: Record<string, PolicyInputValue>; // NYTT, additivt fält, §6a.4/Batch 0
}
```

`beraknaBesparingsvarde(args)` skickar redan (verifierat, `besparingsvarde.ts` rad 361: `if
(gated !== undefined) { return beraknaBesparingsvardeKontrakt(args, leverantor, prisar,
kapacitetGolv, gated.policy); }`) HELA `args`-objektet vidare till kontraktsgrenen — inget
nytt anropsställe krävs, bara det nya fältet på interfacet. `beraknaBesparingsvardeKontrakt`
byter sitt nuvarande, ensamma `new Map([[policy.kapacitetBindning, ...]])`-inlägg
(`besparingsvarde.ts` rad 302–304) mot samma delade `byggKontraktIndata(policy, prisar,
kapacitetKw, args.policyFalt ?? {})` som `beraknaArsprodukt` använder, och kör
`forkontrolleraPolicyIndata(policy, prisar, indata, 'annual')` på den byggda kartan innan
`beraknaArskostnadMedKontrakt` anropas — identisk sekvens som §6a.4:s
`beraknaArsprodukt`-kropp ovan. Legacyvägen (`beraknaBesparingsvarde`s icke-kontraktsgren)
fortsätter ignorera fältet helt — exakt samma bakåtkompatibla mönster som `energyProvenance`
redan har, bara legacygrenen som inte känner till det, inte hela funktionen.

### Sidnivå-dispatch och en HELT SEPARAT resultattyp

`KalkylatorResult` (`energiPotential.ts`) har verifierat OBLIGATORISKA, icke-valfria
numeriska fält `savingsMin`/`savingsMax`/`annualSavingsKr` samt payback-/nettovärden som
sidan renderar OVILLKORLIGT — "lämna dem `null`/utelämnade" kompilerar inte mot dagens
interface. `calcResult`s PUBLIKA resultat och beräkningsbeteende ändras därför INTE (se P2-
rättningen ovan för distinktionen mot dess interna argumentbyggnad). I stället en NY, tunn
wrapper-funktion:

```ts
export type KalkylatorResultUnion =
  | { typ: 'fullstandig'; resultat: KalkylatorResult }
  | { typ: 'aktuell_arskostnad'; kostnad: number; leverantor: string; prisar: number;
      kapacitetKw: number; status: Resultatstatus };

export function calcResultForOnskadTyp(inputs: KalkylatorInputs): KalkylatorResultUnion {
  // Energisystem-grinden FÖRST (rättat P1, granskning 2026-09-09-004): icke-fjärrvärme
  // → alltid false, kortsluts INNAN någon tariff/policy-uppslagning görs.
  if (inputs.onskadTyp === 'aktuell_arskostnad') {
    if (inputs.energySystem !== 'fjarrvarme') {
      throw new Error('Aktuell årskostnad stödjs bara för fjärrvärme');
    }
    const { prisar } = valjLeverantorOchPrisar(inputs.leverantorId);
    if (!stodjerAktuellArskostnad(prisar)) {
      throw new Error('Denna tariff stödjer inte aktuell årskostnad'); // UX-förkontroll,
      // INTE den enda spärren — beraknaArsprodukt upprepar samma kontroll (se nedan)
    }
    // Rättat P1 (granskning 2026-09-09-005): `beraknaArsprodukt`s resultat är REDAN
    // ett `ArsprodukResultat` med det obligatoriska fältet `typ: 'aktuell_arskostnad'`
    // ifyllt — `{ typ: 'aktuell_arskostnad', ...resultat }` sprider alltså samma
    // egenskap två gånger (TypeScript TS2783, verifierat). Returnera resultatet direkt.
    return beraknaArsprodukt(argsFranInputs(inputs));
  }
  return { typ: 'fullstandig', resultat: calcResult(inputs) }; // OFÖRÄNDRAD väg
}
```

**Bakåtkompatibel som valfritt fält, inte obligatoriskt (rättat P1, granskning
`2026-09-09-004`).** Ett nytt fält `onskadTyp?: 'besparing' | 'aktuell_arskostnad'` läggs
till i `KalkylatorInputs` — DEN ENDA KÄLLAN till detta beslut, aldrig en separat
funktionsparameter — men som VALFRITT med implicit default `'besparing'` när det saknas
(`calcResultForOnskadTyp` läser `inputs.onskadTyp === 'aktuell_arskostnad'`, vilket redan är
`false` för `undefined`, så ingen explicit `?? 'besparing'`-defaultering behövs i koden).
v13:s tidigare formulering ("läggs till... DEN ENDA KÄLLAN") lämnade öppet om fältet var
obligatoriskt; ett obligatoriskt fält hade krävt en samtidig, brytande ändring av samtliga
~85 verifierade, redan typade anropsställen till `KalkylatorInputs` i kodbasen (formulär,
tester, batch-verktyg) i SAMMA release som denna etapp — en betydligt större och riskablare
ändring än vad denna etapp beställer. Valfritt+default håller ändringen additiv: alla
befintliga anropsställen fortsätter kompilera och bete sig identiskt (implicit
`'besparing'`), och bara det nya UI-flödet för Stockholm sätter fältet uttryckligen. Källan
i UI:t är ett explicit kundval i formuläret (en radioknapp/växel bredvid leverantörsvalet,
synlig bara när den valda tariffen faktiskt stödjer `aktuell_arskostnad` via
`stodjerAktuellArskostnad`, annars osatt/`'besparing'`).

`KalkylatorPage.tsx` anropar `calcResultForOnskadTyp(inputs)` (inte `calcResult` direkt) och
grenar PÅ RESULTATETS `.typ` INNAN några besparings-/paybackfält läses: `typ: 'fullstandig'`
renderar den befintliga, HELT OFÖRÄNDRADE resultatsidan (via `calcResult`, som denna
omkonstruktion inte rör); `typ: 'aktuell_arskostnad'` renderar en EGEN resultatsektion
(kostnad + "uppskattning" per verifieringsspråket i `PROJECT_CHARTER.md` §3) UTAN
besparingsfält — ingen tom eller påhittad `besparingKr` visas någonsin, eftersom den grenens
typ strukturellt SAKNAR fältet. Kr- och schablonlägena förblir blockerade som redan beskrivet
(§2, generell regel: ett läge utan verifierad modell blockeras).

Den nya publika entryn (`beraknaArsprodukt`/`calcResultForOnskadTyp`) återanvänder samma
fail-closed-kontroller som dagens kontraktsadapter redan har (bekräftad MWh-proveniens,
ändligt positivt energital, exakt debiterbar kapacitet, korrekt energifördelning) — inget
nytt, parallellt valideringsspår som skulle kunna kringgås av ett direkt anrop.

**Sidtest (rättat P1, granskning `2026-09-09-002`, ersätter v11:s tre-grenstest mot en
funktionssignatur som inte längre finns):** väljer Stockholm i den RIKTIGA `KalkylatorPage`,
fyller de 12/5-serierna via det genererade UI:t (§6a.2, punkt 5), sätter
`inputs.onskadTyp: 'aktuell_arskostnad'`, och verifierar att `calcResultForOnskadTyp` (INTE
en `onskadTyp`-parameter till `beraknaArsprodukt`, som avskaffats) ger `typ:
'aktuell_arskostnad'` och att sidan visar kostnaden UTAN någon besparingssiffra synlig. Ett
separat test sätter `inputs.onskadTyp: 'besparing'` för Stockholm och verifierar att den
BEFINTLIGA, oförändrade `calcResult`-vägen kastar `Produktbegransning` via
`beraknaBesparingsvardeKontrakt`s egen guard (§6a.4, "Beslut"-stycket) — inte en gren i
`beraknaArsprodukt`, som aldrig anropas för detta fall. Ett TREDJE test (regression) sätter
`inputs.onskadTyp: 'besparing'` för Sandviken och verifierar att `calcResultForOnskadTyp`
returnerar `typ: 'fullstandig'` med en komplett `KalkylatorResult` — den BEFINTLIGA vägen är
bevisligen oberörd av detta tillägg (Sandviken har `stodjerBesparing !== false`, alltså
`true`, och kastar inte). Ett FJÄRDE test verifierar att `stodjerAktuellArskostnad(prisar)`
är `false` för Sandviken (`stodjer_aktuell_arskostnad` osatt) och `true` för Stockholm, och
att `calcResultForOnskadTyp` kastar fail-closed INNAN `beraknaArsprodukt` ens anropas om
`onskadTyp:'aktuell_arskostnad'` begärs för en tariff där förmågan är `false`.

**Preflighten (§6) rapporterar 44 katalogaktiveringar + 1 leverantörsfilsutökning** — inte
45 identiska `grind()`-vägar. Stockholms rad i §6:s per-tariffrad-tabell markeras
`EXKLUDERAS` (oförändrat), men mekanismen som gör den tillgänglig i UI:t ligger helt
utanför den katalogdrivna aktiveringskedjan.

**Bevisat genom körning:** `_stabilt_tariff_id()` på katalograden ger
`stockholm-exergi-stockholm-exergi-normal` — en tredje, aldrig tidigare existerande
produkt-ID skild från leverantörsfilens `stockholm-exergi-2026`. Utan
`ADAPTERREGISTER`-preflighten skulle en katalogaktivering (om den någonsin nådde grinden)
skapa TVÅ val i UI för samma underliggande normalprodukt, vilket bryter inventeringens
egen dedupliceringsregel (§1).

**Test (utöver v7:s lista, kompletterat granskning `2026-09-08-008`/`-009`/`-2026-09-09-001`):**
saknad/stale `ADAPTERREGISTER`-mappning kastar; fel `provider_id` (leverantören finns inte i
den byggda leverantörsmängden) kastar; fel `tariff_id` (leverantören finns, men har ingen
sådan prisårspost) kastar; en policy med `ersatter_katalograd` satt men UTAN matchande
`ADAPTERREGISTER`-post kastar (riktning 2/bijektionen, ersätter den tidigare `pass`-skissen);
**samma `tariff_id` byggd hos TVÅ olika `provider_id`, där bara den ena
(provider_id, tariff_id)-kombinationen är adaptermappad, kastar för den ANDRA i stället för
att felaktigt kvittera den via ett tariff_id-only-uppslag (regressionstest mot den tappade
leverantörsidentiteten, granskning `2026-09-09-001`);** `bygg_ts()` anropad med det VERKLIGA
produktionsregistret (Stockholms markör, inte ett tomt register) passerar preflighten utan
att kasta, och `bygg_ts_fran_katalog()`/`bygg_ts()` ger identisk reverse-kontroll för samma
leverantörsfilsdata (regressionstest mot v10:s "tom kontext"-design som aldrig kunde lyckas
mot produktionsregistret); `kontrollera_adapterpreflight` anropad med två OLIKA injicerade
register ger två olika resultat (bevisar att registren faktiskt förs igenom, inte läses
globalt av misstag); en
seriekrav-post med 11 eller 13 element (kall energi) resp. 4 eller 6 element (returtemp)
blockerar via `antal_varden`; effektkravets `kravs_for` innehåller nu `"annual"` OCH
`"monthly"` samtidigt (ett test per omfattning, samma `KravPost`); ett anrop till den
uppskattade årskostnaden med giltiga 12/5-serier ger `noggrannhet: snapshot`; ett anrop till
besparingsvärderingen för Stockholm kastar det nya typade felet (inte `KontraktBlockerat`);
`0 <= kallenergi[m] <= totalenergi[m]` blockerar för ett medvetet ogiltigt värde; oförändrad
`monthly_invoice`-väg (regressionstest att den befintliga fakturaåterspelningen inte
påverkas av utökningen); exakt ETT Stockholm-val genereras i UI:t (ingen katalogdublett).

### 6a.5 Kraftringens parametriserade motortyp — domänriktigt namn och en verklig motorväg (rättat P1, granskning 2026-09-08-007)

Codex/Roberts beslut i granskning `2026-09-08-006` (öppen fråga 4): en parametriserad
motortyp för E.ON/Navirums flödeskorrigering delad med Kraftringen är godkänd, UNDER
FÖRUTSÄTTNING att regelvarianten är en explicit, typad diskriminator — INTE implicit
härledd från leverantörs-ID.

**Rättat P1 (granskning `2026-09-08-007`), två fel i v7:s förslag:**

1. **Fel namn.** `kapacitet_bindning_variant` antyder en kapacitetsbindning, men fältet
   väljer i verkligheten en variant av justeringstypen `supply_temperature_adjusted_flow`
   (en FLÖDESKORRIGERING, inte kapacitet). Döpt om till det domänriktiga
   `flodeskorrigering_variant: Literal["golvfri", "golvbegransad"]` — mirror
   `flodeskorrigeringVariant?: 'golvfri' | 'golvbegransad'` i TS. Tillagt i §6a.1s
   mappningstabell (Python-fält/JSON-namn/TS-fält/mappningsrad) tillsammans med `maxvarde`
   och de två bindningsfälten — v7:s tabell saknade denna rad helt.
2. **Ingen väg till motorn.** Verifierat att den delade fasaden (`beräkna_arskostnad_med_
   kontrakt`/`beraknaArskostnadMedKontrakt`) i dag bara bygger den numeriska
   `falt`-dictionaryn och att `faktura.py`/`fjarrvarme.ts` ALDRIG får policyn som argument —
   motorn kan alltså inte grena på en strängdiskriminator som stannar i `Tariffpolicy` och
   aldrig når fram. Löst genom en ny, explicit motorparameter:
   - `Tariffpolicy.flodeskorrigering_variant: Literal["golvfri", "golvbegransad"] | None =
     None`, satt per tariff-ID i `policyregister.py` — E.ON/Navirums åtta rader
     `"golvfri"` (`volym × base_rate × (0,02 × (Tf − 60) + 0,2)`), Kraftringen
     `"golvbegransad"` (`volym × base_rate × max(0,2; 0,2 + (Tf − 60) × 0,02)`).
   - Kontraktsfasaden (`_arskostnad_for_kontraktfasad`/`_arskostnadForKontraktfasad`, den
     interna wrapper bara `resultatkontrakt.py`/`.ts` får anropa) läser
     `policy.flodeskorrigering_variant` och skickar det vidare som en NY, valfri
     keyword-parameter `flodeskorrigering_variant` till den underliggande
     justeringsfunktionen för `supply_temperature_adjusted_flow` i `justeringar.py`
     (speglad inline i `fjarrvarme.ts`) — INTE via `falt`-dictionaryn (samma princip som
     band-ID:t i §6a.2: en diskriminator är inte ett numeriskt fält och ska aldrig försöka
     bli `float(...)`).
   - Justeringsfunktionen grenar på parametern: `"golvfri"` kör den ursprungliga formeln
     utan golv, `"golvbegransad"` kör `max(0,2; ...)`-varianten. En OKÄND eller SAKNAD
     diskriminator på en tariff vars `adjustments` faktiskt innehåller
     `supply_temperature_adjusted_flow` BLOCKERAR (`harled_resultatstatus`/en explicit
     kontroll i justeringsfunktionen) — motorn gissar aldrig vilken regel som gäller. En
     tariff UTAN den justeringstypen kräver inte fältet alls (`None` är giltigt och
     ignoreras säkert).

Minst ett golden-/gränstest per variant, inklusive Kraftringens golv vid exakt `Tf=60`
(faktorn ska vara `0,2`, av att `max(0,2; 0,2) == 0,2`, inte av en slump), ett
serialiseringsrundturstest (`policyregister.py` → genererad JSON →
`policyFranGenererad()` → `flodeskorrigeringVariant` läses tillbaka oförändrat) och ett
direkt fasadanrop som bevisar att diskriminatorn faktiskt styr vilken formelgren som körs.

### 6a.6 Jönköpings fyrvärdesval — en domänmässig allow-list (nytt P1, granskning 2026-09-08-007)

Beslutet 0/10/25/50 kr/mån utan default (§10) är rätt återgivet i v7, men v7 angav bara
UI-val och en ny justeringstyp — ingen domängrind. `KravPost` kan i dag uttrycka `minvarde`/
`maxvarde`/`heltal`, inte en DISKRET mängd tillåtna värden; ett direkt API-/fasadanrop kunde
alltså skicka t.ex. 17 kr/mån och få en beräkning, trots löftet att ett okänt värde ska
blockera. UI-begränsning är per definition inte en domängrind (den kan kringgås av vilken
annan anropare som helst), och värdet `0` måste kunna skiljas från SAKNAD indata (annars
tolkas en kund som uttryckligen valt "inget tillägg" som om fältet inte fyllts i alls).

Ny `KravPost`-fält `tillatna_varden: tuple[float, ...] | None = None` (samma mönster som
`minvarde`/`maxvarde` — mirror `tillatnaVarden?: readonly number[]` i TS). `__post_init__`/
`skapaKravPost` validerar att listan (när satt) inte är tom och att varje element är ett
ändligt tal; FÅR kombineras med `heltal` men inte meningsfullt med `minvarde`/`maxvarde`
(en explicit mängd gör ett intervall överflödigt — `__post_init__` kastar om båda är satta,
för att undvika två motsägande regler på samma fält). `harled_resultatstatus`/
`harledResultatstatus` kontrollerar, när `tillatna_varden` är satt: `post.varde in
f.tillatna_varden` (exakt medlemskap, flyttalsjämförelse mot den EXAKTA katalogsiffran —
0/10/25/50 kr har ingen avrundningsrisk) — annars `raise`/kastar, aldrig en tyst
avrundning till närmaste tillåtna värde.

**Explicit `0` skilt från saknad indata:** löses av grundarbetets `byggIndataFranPolicy`
(§6a.2) — en `IndataPost` byggs bara när `falt`-objektet FAKTISKT har en nyckel för fältet.
UI:t (`KalkylatorPage.tsx`) får därför INTE förifylla Jönköpings accessavgiftsfält med `0`
som ett vanligt formulärdefault (vilket skulle göra "inget val gjort" oskiljbart från "0
kr valt") — fältet börjar tomt/`undefined`, och en explicit `0`-knapptryckning sätter
`falt["jonkoping_accessavgift_kr"] = 0` precis som `10`/`25`/`50` skulle. Ett fortsatt tomt
val ger INGEN `falt`-nyckel, vilket `byggIndataFranPolicy` korrekt tolkar som saknad
obligatorisk indata (`blocked`), inte som "0 kr".

**Test:** samtliga fyra giltiga värden (0, 10, 25, 50) räknar; tomt/saknat blockerar (saknad
`IndataPost`); 17 kastar (`harled_resultatstatus`); negativa och icke-ändliga värden kastar
(befintlig `_validera_varde`, oförändrad); ett uttryckligt `0`-val ger `complete`, inte
`blocked` (bevisar att `0` inte feltolkas som frånvaro). Kontraktsfilerna
(`resultatkontrakt.py`/`.ts`, `policyregister.py`, `KalkylatorPage.tsx`) läggs i batch 5b:s
fillista (`batchplan-v14.md`), där Jönköpings basrad redan ligger.

### 6a.7 Lidköpings signerade nätmedelavkylningsjustering (nytt, bedömning `2026-09-09-006`, planerat för batch 5d)

**Källa:** Lidköping Energis skriftliga leverantörssvar 2026-09-09 (bedömning
`2026-09-09-006`, se §4.2 för de två tariffradernas fullständiga källgodkänningstext och
`source_sha256`). Lidköping passar INTE i batch 5b:s enkla `volume`-modell — komponenten kan
vara både en avgift OCH en kreditering (tvåsidig, inte klämd till noll), och kräver TRE
parallella 12-månadersserier i stället för ett enda leverantörsvärde. Detta avsnitt
specificerar bara DESIGNEN; ingen katalog-JSON, `adjustments`-post, `POLICYREGISTER`-post,
UI eller motorkod ändras av detta dokument (se §6a.6-mönstret ovan för samma
planerings-/implementationsgräns).

**Rättat P1 (granskning `2026-09-09-010`) — v16:s `SignedMonthlyFlowAdjustment` och dess två
fristående beräkningsfunktioner var en skiss utan anropskedja till den verkliga
motorn.** Verifierat direkt mot källan (`fjarrvarme.ts` rad 725–733, `faktura.py` rad
628–632, `resultatkontrakt.ts` rad 576–586, Pythonfasaden rad 600–609):

1. `beraknaArskostnadMedKontrakt`/den motsvarande Pythonfasaden bygger motorns `falt` som
   SKALÄRA tal och kastar uttryckligen för varje icke-kapacitetsbunden serie — Lidköpings
   `Q_m`/`T_m`/`Tm_m` hade alltså stoppats innan `_arskostnadForKontraktfasad`/
   `_arskostnad_for_kontraktfasad` någonsin nåddes.
2. Den verkliga justeringsmotorn dispatchar på katalogfältet `post.type` (TS) resp.
   `post["type"]` (Python) — v16:s skiss använde i stället `typ` och beskrev ingen
   serialisering mellan formerna.
3. Python kräver att typen finns i BÅDE `JUSTERINGSTYPER` och `_JUSTERING_BERAKNING`;
   TypeScript kräver en post i `JUSTERING_BERAKNING`. Ingen av dessa register nämndes i
   batchens fillista.

V17 ersätter skissen med en komplett, speglad integrationsväg (nedan): kanonisk
`type`-diskriminator, en explicit seriekanal genom hela kedjan katalog → policy → fasad →
motor, och uppdaterade register i BÅDA språken — se den kompletta fillistan i
`batchplan-v17.md` Batch 5d. Designen är compile-verifierad isolerat
(`npx tsc --noEmit --strict --skipLibCheck --target es2020` mot en fristående kontrollfil
som mirrorar de verkliga signaturerna nedan; filen låg i `/tmp` och togs bort efter
körningen).

**Formel (bekräftad av leverantören, oförändrad från källan):**

```text
flödesjustering_m = 5 × Q_m × (1 − T_m / Tm_m)   för varje kalendermånad m = 1..12
årsjustering = Σ (m=1..12) flödesjustering_m
```

- `Q_m`: kundens uppmätta fjärrvärmevolym i m³ för månaden — ändlig, ≥ 0.
- `T_m`: kundens månadsmedelavkylning `T_in − T_ut` i °C — ändlig (kan vara negativ vid en
  ovanlig drifthändelse; ingen artificiell nedre gräns eftersom källan inte anger någon).
- `Tm_m`: Lidköpingsnätets månadsmedelavkylning i °C, ETT SUPPLIER-VÄRDE (nätets, inte
  kundens) — ändlig och STRIKT större än noll, så division med noll aldrig kan ske.
- `N = 5 SEK/m³ exkl. moms`: statisk tariffparameter, samma för båda Lidköpings bastariffer.
- Resultatet klämmas INTE till noll: positivt belopp är en avgift, negativt är en
  premie/kreditering — den bekräfta tvåsidiga modellen (leverantörssvarets punkt 6).

**§6a.7.1 Steg 1 — katalogpost och register (kanonisk `type`-diskriminator):**

```ts
// fjarrvarme.ts, planerat tillägg vid övriga AdjustmentSpec-varianter — SAMMA
// diskriminatorfält (`type`) och SAMMA katalogplats (`prisar.justeringar`) som de sex
// befintliga typerna, ingen egen dispatchmekanism.
export interface SignedMonthlyFlowAdjustment {
  type: 'signed_monthly_flow_adjustment'; // rättat P1 (granskning 010): INTE `typ` — måste
                                           // matcha post.type som justeringar() dispatchar på
  faktor_n: number; // 5, SEK/m³, exkl. moms, statisk katalogparameter
  kund_volym_falt: string;      // policyFalt-nyckel för Q_m (number_series, 12 värden, m³)
  kund_avkylning_falt: string;  // policyFalt-nyckel för T_m (number_series, 12 värden, °C)
  nat_avkylning_falt: string;   // policyFalt-nyckel för Tm_m (number_series, 12 värden, °C)
}
```

```python
# justeringar.py, planerat tillägg
SIGNED_MONTHLY_FLOW_ADJUSTMENT = "signed_monthly_flow_adjustment"
JUSTERINGSTYPER[SIGNED_MONTHLY_FLOW_ADJUSTMENT] = Justering(beraknas=True, indatafalt=None)
# indatafalt=None: till skillnad från de sex befintliga typerna har denna INGET enda
# ifyllbart falt-värde med ett default — den har tre OBLIGATORISKA serier utan default,
# validerade av policykontraktet (§6a.2/nedan), inte av `resolvera_falt`.
```

Katalogens `prisar.justeringar`-post för Lidköping blir alltså (planerad, ändrar ingen JSON
i denna etapp):

```json
{ "type": "signed_monthly_flow_adjustment", "faktor_n": 5,
  "kund_volym_falt": "lidkoping_kund_volym_m3",
  "kund_avkylning_falt": "lidkoping_kund_avkylning_c",
  "nat_avkylning_falt": "lidkoping_nat_avkylning_c" }
```

**§6a.7.2 Steg 2 — motorns beräkningsfunktion och registrering i BÅDA
`JUSTERING_BERAKNING`-registren.** De sex befintliga funktionerna i `fjarrvarme.ts`/
`faktura.py` har signaturen `(post, mwhPerManad, kapacitet, falt) -> number`, där `falt` är
`Record<string, number>` (SKALÄRER) — samma typ `beraknaArskostnadMedKontrakt` bygger och
som första P1-fyndet ovan visar INTE kan bära Lidköpings tre serier. Lösningen är INTE en
sjunde parallell mekanism utan en additiv, tom-som-default trailing-parameter
`faltSerier`, given till ALLA sju funktioner (de sex befintliga ignorerar den — mekaniskt,
ingen logikändring i dem):

```ts
// fjarrvarme.ts — JUSTERING_BERAKNING-signaturen får en NY trailing-parameter,
// bakåtkompatibel (defaultar till {} vid varje annat anropsställe).
type JusteringsFn = (
  post: any, mwhPerManad: Record<number, number>, kapacitet: number,
  falt: Record<string, number>, faltSerier: Record<string, Record<number, number>>
) => number;

function signedMonthlyFlowAdjustment(
  post: SignedMonthlyFlowAdjustment, _mwhPerManad: Record<number, number>,
  _kapacitet: number, _falt: Record<string, number>,
  faltSerier: Record<string, Record<number, number>>
): number {
  const q = faltSerier[post.kund_volym_falt];
  const t = faltSerier[post.kund_avkylning_falt];
  const tm = faltSerier[post.nat_avkylning_falt];
  if (q === undefined || t === undefined || tm === undefined) {
    // Ska inte kunna inträffa: forkontrolleraPolicyIndata (§6a.2) har redan bevisat att
    // alla tre serierna finns med rätt kardinalitet innan fasaden extraherar dem
    // (§6a.7.3). Fail-closed andra skydd, samma mönster som justeringar()s egen
    // "okänd justeringstyp"-kastvakt.
    throw new Error(`${post.type}: en eller flera serier saknas i faltSerier`);
  }
  let arsjustering = 0;
  for (let m = 1; m <= 12; m++) {
    const tmM = tm[m];
    if (!(tmM > 0)) {
      // Andra skydd mot division med 0 — FÖRSTA skyddet är det fältnära minExklusiv-kravet
      // i §6a.7.4, som ska stoppa detta redan i forkontrolleraPolicyIndata.
      throw new Error(`${post.type}: Tm_m måste vara > 0, fick ${tmM} (månad ${m})`);
    }
    arsjustering += post.faktor_n * q[m] * (1 - t[m] / tmM);
  }
  return arsjustering; // INTE Math.max(0, ...) — tvåsidigt resultat, avgift eller kreditering
}

const JUSTERING_BERAKNING: Record<string, JusteringsFn> = nollprototyp({
  volume_discount: volymrabatt, volume: flodesavgift, low_utilization: lagutnyttjandeavgift,
  temperature_difference: returtemperaturjusteringGoteborg,
  cooling_deadband: kylningsdodbandGotland,
  incremental_return_temperature: stegvisReturtemperaturNorrenergi,
  signed_monthly_flow_adjustment: signedMonthlyFlowAdjustment, // NY
});
```

```python
# faktura.py — _JUSTERING_BERAKNING och de sex befintliga funktionerna får samma additiva
# trailing-parameter falt_serier: dict[str, dict[int, float]] | None = None.
def _signed_monthly_flow_adjustment(post, mwh_per_manad, kapacitet, falt,
                                     falt_serier=None):
    falt_serier = falt_serier or {}
    q = falt_serier.get(post["kund_volym_falt"])
    t = falt_serier.get(post["kund_avkylning_falt"])
    tm = falt_serier.get(post["nat_avkylning_falt"])
    if q is None or t is None or tm is None:
        raise ValueError(f"{post['type']}: en eller flera serier saknas i falt_serier")
    summa = 0.0
    for m in range(1, 13):
        if not (tm[m] > 0):
            raise ValueError(f"{post['type']}: Tm_m måste vara > 0, fick {tm[m]!r} (månad {m})")
        summa += post["faktor_n"] * q[m] * (1 - t[m] / tm[m])
    return summa  # INTE max(0, ...) — tvåsidigt resultat


_JUSTERING_BERAKNING[SIGNED_MONTHLY_FLOW_ADJUSTMENT] = _signed_monthly_flow_adjustment
```

Dispatchloopen `justeringar()`/`_justeringar()` (fjarrvarme.ts rad 725, faktura.py rad 628)
får samma additiva `faltSerier`/`falt_serier`-parameter och skickar den vidare oförändrad
till `JUSTERING_BERAKNING[post.type](post, mwhPerManad, kapacitet, falt, faltSerier)` — ETT
extra argument på ett redan existerande anrop, ingen ny kontrollväg. `arskostnad()`/
`_arskostnadForKontraktfasad()`/motsvarande Pythonfunktion trär samma parameter vidare från
sin egen (nya, defaultande-till-`{}`) trailing-parameter till `justeringar()`, så att
Lidköpings bidrag når fram till `Kostnad.justering` — SAMMA fält övriga sex typer redan
skriver till, ingen ny utdatakanal.

**§6a.7.3 Steg 3 — fasaden extraherar serierna FÖRE den skalära `falt`-loopen, i stället
för att kasta.** `beraknaArskostnadMedKontrakt`/Pythonmotsvarigheten itererar i dag
`inrapporteradIndata` och kastar för varje `arSerie(post.varde) === true`. Rättat till att
avgöra per fält, med samma `KravPost.vardetyp` som redan avgör
`forkontrolleraPolicyIndata`s (§6a.2) kontroll av samma fält — ingen ny klassificeringsregel:

```ts
const falt: Record<string, number> = {};
const faltSerier: Record<string, Record<number, number>> = {};
for (const [nyckel, post] of inrapporteradIndata) {
  if (!relevantaNycklar.has(nyckel) || nyckel === kb) continue;
  const krav = policy.kravdaFalt.find((f) => f.nyckel === nyckel)!; // finns garanterat:
                                                                      // relevantaNycklar
                                                                      // härleds ur samma lista
  if (krav.vardetyp === 'number_series') {
    // arSerie(post.varde) är redan bevisat sant här: forkontrolleraPolicyIndata (§6a.2)
    // har kastat 'invalid_policy_fields'/'typ' om ett number_series-fält fick ett skalärt
    // värde, INNAN denna funktion nås.
    const serie: Record<number, number> = {};
    (post.varde as readonly number[]).forEach((v, i) => { serie[i + 1] = v; });
    faltSerier[nyckel] = serie;
    continue;
  }
  if (arSerie(post.varde)) {
    throw new Error(
      `${nyckel}: kan inte bindas till motorns falt-dict som en serie — ` +
        'ingen reduceringsregel till ett enda värde finns'
    ); // OFÖRÄNDRAT beteende för alla fält som INTE deklarerats number_series
  }
  falt[nyckel] = post.varde;
}
const kostnad = _arskostnadForKontraktfasad(
  prisar, ar, mwhPerManad, kapacitet,
  opts.returtempC ?? null, opts.moms, opts.mwhKalltPerManad ?? {}, falt, faltSerier
);
```

Python-mirroret gör samma sak i `berakna_arskostnad_med_kontrakt`, byggd på samma
`vardetyp`-fält. Ingen befintlig tariff (samtliga har `vardetyp: "number"` idag, §6a.1) byter
beteende — grenen för `number_series` är obesökt kod tills Lidköping aktiveras.

**§6a.7.4 Fail-closed-validering, återanvänder batch 0:s befintliga seriekontrakt +
det NYA `minExklusiv`-fältet (§6a.7.5) i stället för en tredje mekanism:**
- Samtliga tre `policyFalt`-nycklar deklareras som `KravPost.vardetyp = "number_series"`
  med `antal_varden = 12` (§6a.1:s befintliga kardinalitetskontroll i
  `harled_resultatstatus`/`harledResultatstatus`, ingen ny motorkod).
- `Tm_m` (nät-avkylningsserien) märks `kallaTyp: 'supplier_value'` — SAMMA källtyp som
  `Q_m`/`T_m`, ingen ny/annan diskriminator (§6a.7.6 nedan för det RÄTTADE
  proveniensbeslutet: `rullande=True`, som ALLA tre serie-krav redan måste ha för att bära
  ett `number_series`-värde, gör resultatets `Resultatstatus.noggrannhet` till `'snapshot'`
  AUTOMATISKT — ingen kod ändras för det).
- Om NÅGON av de tre serierna saknas helt: `forkontrolleraPolicyIndata` lägger nyckeln i
  `saknade` (§6a.2, punkt 8) → `KontraktBlockerat(tariffId, 'missing_policy_fields', {
  saknadeFalt })`, precis som §6a.4:s `beraknaArsprodukt` redan gör för Stockholm.
- Om en serie har fel längd, ett icke-ändligt element, eller (för `Tm_m` specifikt) något
  element `≤ 0`: `ogiltiga` (`orsak: 'kardinalitet'` för fel längd, `'numerik'` för
  icke-ändligt, `'min'` för `Tm_m ≤ 0` via `minVarde: 0, minExklusiv: true`, §6a.7.5) →
  `KontraktBlockerat(tariffId, 'invalid_policy_fields', { ogiltigaFalt })`. Ingen serie får
  ersättas med noll, ett upprepat värde eller ett gissat medeltal.
- `Q_m` kräver `minVarde: 0` (inkluderande — noll förbrukning en enskild månad är giltigt).
  `T_m` har inget deklarerat min/max (källan anger ingen gräns). `Tm_m` kräver
  `minVarde: 0, minExklusiv: true` (§6a.7.5) — kontrollerat FÖRE
  `signedMonthlyFlowAdjustment` någonsin anropas; funktionens egen `tmM > 0`-kontroll
  (§6a.7.2) är ett andra, aldrig det första, skyddet.
- Övrig obligatorisk produktindata (bekräftad energi i MWh, leverantörens debiterbara
  effekt, det bekräftade effektband `selected_band_affine`-mekanismen kräver) följer samma
  redan planerade band-/kapacitetskontrakt som resten av §6a.2 — ingen ny mekanism.

**§6a.7.5 Rättat P1 (granskning `2026-09-09-010`, elementvisheten rättad `2026-09-09-011`)
— vald `Tm_m > 0`-mekanism.** v16 lovade resultatet (`invalid_policy_fields`/`'min'`) men
sköt upp VALET av mekanism till implementationstillfället, trots att dagens `minVarde` är
inkluderande. v17 valde `minvarde_exklusiv: bool = False` (Python)/`minExklusiv?: boolean`
(TS), FÅR bara sättas tillsammans med `minvarde`/`minVarde` (`__post_init__`/`skapaKravPost`
kastar annars — samma valideringsmönster §6a.1 redan använder för `maxvarde`), men skrev
kontrollen som en skalär jämförelse (`post.varde < f.minvarde`) — ogiltig för `Tm_m`, som är
en tolvmånadersserie. Kontrollen är nu i stället den DELADE, elementvisa
`vardefelForKrav`/`_vardefel_for_krav`-funktionen (§6a.1 ovan), anropad IDENTISKT av
`harledResultatstatus`/`harled_resultatstatus` OCH `forkontrolleraPolicyIndata`s fältnära
motsvarighet (§6a.2) — ingen separat mekanism för serier. `Tm_m` sätts till `minVarde: 0,
minExklusiv: true`; `Q_m` förblir `minVarde: 0` (inkluderande, `minExklusiv` osatt/`false`).
Testat isolerat (`npx tsc --noEmit --strict --skipLibCheck --target es2020`, `/tmp`-fil
borttagen efter körning) OCH via ett direkt `beraknaArskostnadMedKontrakt`-anrop som
kringgår UI-förkontrollen: en tolvelementserie med ETT negativt element → `'min'`; samma
serie med ETT element exakt `0` (`minExklusiv: true`) → `'min'`; samma serie med `0`
(`minExklusiv` osatt) → OK; en serie med bara positiva tal → OK i båda fallen. Kontrollerat
FÖRE divisionen i `signedMonthlyFlowAdjustment`/`_signed_monthly_flow_adjustment` (§6a.7.2)
kan nås.

**§6a.7.6 Rättat P1 (granskning `2026-09-09-011`) — `'snapshot'`/`'uppskattat'` som
källtyp finns inte i det verkliga käll-/noggrannhetskontraktet.** v17 föreslog ett NYTT,
tredje `kallaTyp`-värde (`'snapshot'`) och ett internt `Resultatstatus.noggrannhet`-värde
`'uppskattat'`. Ingen av dem existerar: TypeScript/Python har exakt
`KALLTYPER = ['supplier_value', 'calculated', 'estimated']`, och BÅDA konstruktorerna
(`skapaIndataPost`/`IndataPost.__post_init__`) avvisar allt annat; `NOGGRANNHETER` är
`exact | snapshot | estimated` — `'uppskattat'` är UI-text, aldrig ett internt värde. Att
införa en fjärde källtyp hade krävt att utöka HELA den speglade unionen, konstruktions-
valideringen i båda språken, policykällorna, `byggIndataFranPolicy`, JSON-serialiseringen,
statushärledningen och samtliga tester som redan antar tre värden — en onödigt stor ändring
för ett rent proveniensbehov.

**Löst genom att återanvända den befintliga modellen i stället för att utöka den.** `Tm_m`
märks `kallaTyp: 'supplier_value'` — SAMMA källtyp som `Q_m`/`T_m`, ingen
fält-specifik gren i `byggIndataFranPolicy` (§6a.2) behövs. Resultatets
`Resultatstatus.noggrannhet` blir `'snapshot'` (det BEFINTLIGA, riktiga enumvärdet, inte
`'uppskattat'`) HELT AUTOMATISKT: `harled_resultatstatus`/`harledResultatstatus` sätter
redan `noggrannhet='snapshot'` så snart minst ett relevant krav är
`ar_ej_helt_verifierbar`/`arEjHeltVerifierbar` (`resultatkontrakt.py` rad 218–220,
`resultatkontrakt.ts` rad 125–127) — en COMPUTED egenskap, `rullande OR
kalperiod_definition`. `Tm_m`, `T_m` och `Q_m` MÅSTE redan ha `rullande=True` för att
över huvud taget få bära ett serievärde (samma villkor `harled_resultatstatus` redan kastar
på: `f.rullande`-kravet för `_ar_serie(post.varde)`, §6a.1) — de tre kraven ger alltså
`noggrannhet: 'snapshot'` UTAN någon ny kod, precis av samma mekanism som redan gör Stockholms
kallenergiserie till `'snapshot'` (§6a.4). Ingen ändring av `KALLTYPER`, `NOGGRANNHETER`,
konstruktörerna, serialiseringen eller statushärledningen krävs.

**Kvarstående, genuint nytt behov: obligatorisk källattestering.** Att `Tm_m` tekniskt kan
märkas `supplier_value` (som `Q_m`/`T_m`) löser INTE att ett fritt inmatat tal automatiskt
skulle påstå sig vara ett verifierat leverantörsvärde — samma risk v17 identifierade.

**Rättat P1 (granskning `2026-09-09-012`) — attesteringen var UI-only och kunde kringgås av
ett direkt produkt-/domänanrop.** v18 gjorde `kravAttestering`/`krav_attestering` till en
REN UI-nivå-spärr: `KalkylatorPage.tsx` blockerade submit tills en bekräftelseruta var
ikryssad, men domänlagret (`beraknaArskostnadMedKontrakt`/motsvarande direkta anrop) märkte
värdet `supplier_value` OAVSETT om attesteringen någonsin ägt rum — ett anrop som helt
kringgick UI:t kunde alltså fortfarande producera ett resultat som ser lika trovärdigt ut
som ett verkligt fakturaverifierat värde.

**Löst genom att bära den FAKTISKA attesteringen i den typade produktindatan, inte bara i
formulärstate.** `IndataPost` (resultatkontrakt.ts/.py) får ett nytt, valfritt fält
`attesterad?: boolean` (`attesterad: bool = False` i Python) — satt av ANROPAREN, inte
härlett i efterhand. `harledResultatstatus`/`harled_resultatstatus` (§6a.1) kräver, för
VARJE `KravPost` där `kravAttestering === true`, att den mottagna `IndataPost.attesterad ===
true` — annars `fullstandighet: 'blocked'`, precis som ett saknat fält. Detta är alltså en
NY, generisk regel i den auktoritativa validatorn (inte hårdkodad på Lidköpings fältnamn):
"ett krav med `kravAttestering=true` kräver en `IndataPost` med `attesterad=true`", som
gäller lika för Lidköpings `Tm_m` idag som för en framtida tariffs eget attesteringskrav.

`byggIndataFranPolicy` (§6a.2) bygger `IndataPost.attesterad` från formulärstatets
kryssruta-värde — kryssrutan förblir alltså UI:ts sätt att SÄTTA attesteringen, men den
auktoritativa kontrollen sitter nu i `harledResultatstatus` och gäller identiskt för ett
direkt fasadanrop som inte går via UI:t alls: `beraknaArskostnadMedKontrakt(prisar, policy,
new Map([['tm_m', { nyckel: 'tm_m', varde: [...], kallaTyp: 'supplier_value', attesterad:
false }]]), ...)` ger `fullstandighet: 'blocked'`, medan samma anrop med `attesterad: true`
passerar (givet att övriga krav också är uppfyllda).

`KalkylatorPage.tsx` renderar fortsatt en obligatorisk bekräftelseruta ("Jag intygar att
värdet är hämtat från Lidköpings faktura eller ett direkt skriftligt besked, inte ett eget
uppskattat tal") intill `Tm_m`-fältet — nu bara som UI:ts sätt att fylla i det typade
`attesterad`-fältet, inte som ensam spärr. `Q_m`/`T_m` kräver ingen sådan attestering
(`kravAttestering` osatt/`false` på deras `KravPost`) — de är kundens egna, direkt avlästa
fakturavärden utan samma risk för ett gissat tal, så deras `IndataPost.attesterad` läses
aldrig av validatorn.

**Test (nytt, krävt av granskning `2026-09-09-012`):** ett direkt `beraknaArskostnadMedKontrakt`-
anrop med `Tm_m` som `kallaTyp: 'supplier_value'` men `attesterad: false`/osatt →
`fullstandighet: 'blocked'`; samma anrop med `attesterad: true` → `complete` (givet övriga
krav uppfyllda). Samma par upprepas i Python. Mekanismen är generisk — testad även med ett
syntetiskt andra `KravPost` med `kravAttestering=true` för att bevisa att den inte är
hårdkodad på Lidköpings fältnamn `tm_m`.

**Runtime- vs. katalogkrav:** `Tm_m`s tolv faktiska månadsvärden är INTE kända statiskt —
leverantörssvaret ger METODEN (nätets månadsmedel av samtliga anläggningars `T_in − T_ut`),
inte de tolv siffrorna, och bekräftar inte att de alltid visas på kundfakturan. `Tm_m` är
därför ett RUNTIMEKRAV som matas in per kundfall (`kallaTyp: 'supplier_value'` +
`kravAttestering`, §6a.7.6), inte ett statiskt katalogvärde i `adjustments`. Saknas det för
ett givet kundfall ska HELA Lidköpings fullständiga tariff blockeras för det fallet — inte
räknas med ett gissat eller senast kända `Tm`. Resultatet visas märkt `snapshot` i UI:t
(samma `Resultatstatus.noggrannhet`-språk som Stockholms uppskattade årskostnad redan
använder, §6a.4) tills ett konkret kundfall har fakturaverifierats.

**§6a.7.7 Rättat P1 (granskning `2026-09-09-010`) — Lidköpings "aktuell årskostnad" var
onåbar, och besparingsvägen saknade en före/efter-regel.** Se §6a.4 ovan (INTE §6a.5, som är
Kraftringens motorvariant — rättad referens, granskning `2026-09-09-011`) för det explicita
förmågekontraktet (`stodjerAktuellArskostnad`/`stodjerBesparing`) som nu gör Lidköpings
estimerade årskostnad nåbar via `beraknaArsprodukt`, och `Produktbegransning` som blockerar
Lidköpings besparingsväg tills en källförsvarbar före/efter-transformation finns. Ändrar
INTE Lidköpings `ready_to_implement`-status (§4.2, §8) — källunderlaget är fortsatt komplett.

**Testplan (golden/gräns/negativ, båda språken — planerad för batch 5d, inte skriven av
detta dokument):**
1. Positiv avgift: `T_m < Tm_m` för samtliga tolv månader → positivt årsbelopp.
2. Nollresultat: `T_m = Tm_m` för samtliga månader → `flödesjustering_m = 0` varje månad,
   `årsjustering = 0` (inte `blocked` — ett giltigt, räknat nollresultat).
3. Negativ premie/kreditering: `T_m > Tm_m` för samtliga månader → negativt årsbelopp, INTE
   klämt till noll.
4. Blandat (vissa månader avgift, andra kreditering) → summan är nettot, inte summan av
   absolutbelopp.
5. `Tm_m = 0` för minst en månad → blockerar (`invalid_policy_fields`), aldrig en
   `Infinity`/`NaN`-division.
6. Fel serielängd (11 eller 13 värden i någon av de tre serierna) → blockerar
   (`kardinalitet`).
7. En hel serie saknas → blockerar (`missing_policy_fields`).
8. Momshantering: `N = 5 SEK/m³` är exkl. moms (leverantörssvarets punkt 1) — testa att
   utdata är konsekvent momsexkluderad genom hela kedjan, samma mönster som övriga
   Lidköpings-fält.
9. 1/12-periodisering av de fasta års-/effektavgifterna (leverantörssvarets punkt 8) —
   separat från flödesjusteringen, men samma kundfall ska testas end-to-end.
10. **Nytt (granskning `2026-09-09-010`):** `Q_m`/`T_m`/`Tm_m` extraheras korrekt till
    `faltSerier`/`falt_serier` av fasaden (§6a.7.3) och `justeringar()`/`_justeringar()`
    dispatchar `signed_monthly_flow_adjustment` till motorfunktionen (§6a.7.2) — ett
    end-to-end-test mot `Kostnad.justering`, inte bara ett direkt anrop av
    beräkningsfunktionen.
11. **Nytt:** `minExklusiv`/`minvarde_exklusiv` (§6a.7.5) testas isolerat i BÅDA språken:
    negativt element → `'min'`; exakt `0` på ett `minExklusiv: true`-fält → `'min'`; `0` på
    ett vanligt (inkluderande) `minVarde: 0`-fält → OK; ett `KravPost` som sätter
    `minExklusiv` UTAN `minvarde`/`minVarde` → konstruktionsfel.
12. **Nytt:** Lidköpings "aktuell årskostnad" (§6a.4/§6a.7.7) = ett fasadanrop via
    `beraknaArsprodukt`, samma mönster som Stockholm; Lidköpings besparingsväg kastar
    `Produktbegransning('...lidkoping...', 'besparing_ej_stodd')` (§6a.4) — aldrig
    `KontraktBlockerat`, och aldrig ett syntetiskt oförändrat före/efter-par.

## 7. Livscykel för `remaining_information_requests` som berör `ready`-raderna (granskning 2026-09-08-005/-006/-007, P1)

**Vald representation, rättad för att matcha en körbar `grind()`-signatur (granskning
`2026-09-08-006`, P1):** v6:s förslag behöll `grind(tariff, utredda)` samtidigt som det
introducerade en separat `oppna_tariff_ider(katalog)`-funktion `grind()` inte själv kunde
anropa eller skilja tariff-ID:n från medlems-ID:n i. Löst genom att göra UPPLÖSNINGEN till
ett steg FÖRE grindanropet, inte en del av grindens egen signatur:

`remaining_information_requests` i katalog-JSON:et får ett NYTT, valfritt fält
`tariff_ids: list[str] | null` VID SIDAN AV det befintliga `member_ids`. En ny funktion
`blockerade_tariff_ider(katalog) -> set[str]` (ersätter `utredda_medlemmar()`, körs EN gång
per `godkanda()`/preflight-anrop, inte per tariff) itererar samtliga requests och bygger EN
platt mängd tariff-ID:n: för en request med `tariff_ids` satt läggs EXAKT de angivna
ID:na till; för en request UTAN `tariff_ids` (bakåtkompatibelt, medlemsomfattande) expanderas
`member_ids` till samtliga tariff-ID:n den/de medlemmarna har i katalogen VID
LADDNINGSTILLFÄLLET. Resultatet är EN mängd av bara tariff-ID:n, aldrig en blandning av
tariff- och medlems-ID:n. `grind()`s signatur byts till `grind(tariff: dict, blockerade:
set[str]) -> str | None` (§6, steg 2), och dess enda jämförelse blir `tariff.get("id") in
blockerade` — en enda, entydig strängjämförelse, ingen specialkod för att skilja ID-typer
åt. Samma representation används för SAMTLIGA 14 requests nedan — inget "eller", ingen
`oppna_tariff_ider`/`grind()`-signaturkrock kvar i arbetsordern.

Katalogen har 14 `remaining_information_requests` totalt. De 10 nedan berör minst en av de
45 `ready`-raderna — övriga 4 (R02, R07, R08, R09) gäller enbart redan
`blocked_external_info`-tariffer och rörs inte av denna etapp.

| ID | Medlem(mar) | Fråga | Disposition (EN livscykel per request) | Motivering |
|---|---|---|---|---|
| R03 | `malarenergi` | Vilka nät hör sidans två olika tabeller till? Bekräfta fast avgift 2217/2117 för 25–79 kW samt sommarperiod/flödesvillkor. | **`tariff_ids` sätts** till de två `blocked_external_info`-tarifferna (`storre-fastigheter`, `gruppanslutna-smahus`) | `24-lagenheter` har ingen kapacitetsdel och ingen effekt-/avgiftstvetydighet — request-posten begränsas till de tariff-ID:n frågan faktiskt gäller, `member_ids` tas bort från posten samtidigt. |
| R04 | `borlange-energi` | Bekräfta september–oktober 559 kr/MWh och vilken effektgrupp exakt 501 kW tillhör. | **TAS BORT** | Höstpriset är verifierat; 501 kW-gränsen löses av `supplier_confirmed_band_id` (§6a.2), inte av request-processen. |
| R05 | `c4-energi` | Vilken prisgrupp gäller exakt 500 kW? | **TAS BORT** | Löses av `supplier_confirmed_band_id` (§6a.2). |
| R06 | `kraftringen` | Hur används temperaturens korrigeringsfaktor på flödespriset? Behöver explicit slutformel samt effektprisets tidsenhet och periodisering. | **TAS BORT** | Formeln är källverifierad (verifieringslistan, golv vid 0,2) och effektprisperioden rättas i katalogen (`rate_period: year`) — frågan är besvarad. |
| R10 | `e-on-jarfalla, e-on-malmo, navirum-energi-norrkoping-och-soderkoping, navirum-energi-orebro-kumla-och-hallsberg` | Aktuell prisbilaga och särskilda prisvillkor: effektprisets periodisering och temperaturkorrigerat flödespris. | **TAS BORT** | Samtliga fyra medlemmars enda tariffer är `ready_to_implement`; periodiseringen rättas i katalogen (`rate_period: month`) och flödesformeln är källverifierad (§6, batch 3). Ingen `tariff_ids`-begränsning behövs — alla berörda produkter blir redo samtidigt. |
| R11 | `telge-nat` | Fullständig villkorsbilaga som gäller tillsammans med 2026 års prislista, alternativt bekräftelse att tillsvidarevillkoren i 2025-bilagan fortsatt gäller. | **TAS BORT** | Verifieringslistan bekräftar redan att tillsvidarevillkoren gäller — frågan är redan besvarad, katalogens kontroll-issue är inaktuell. |
| R12 | `temab-fjarrvarme` | Kategorital och historik bakom debiteringseffekten, om Optimate ska beräkna den själv; annars räcker leverantörens debiterbara effekt. | **TAS BORT** | Löses av den normaliserade issue-texten (leverantörens fakturavärde används, ingen egen beräkning). |
| R13 | `soderhamn-nara` | Byggnadstypens omräkningsindex, om Optimate ska beräkna effekten själv; annars leverantörens debiterbara effekt. | **TAS BORT** | Tariffen passerar redan grinden idag — leverantörens debiterbara effekt används, ingen egen beräkning. |
| R14 | `sundsvall-energi` | Leveransvillkor för abonnemang från 2000 kW i Sundsvall/Matfors. Krävs endast för kunder i dessa grupper. | **`tariff_ids` sätts** till de två `blocked_external_info`-tarifferna (`sundsvall-normal`, `matfors-och-kvissleby`) | `indal-liden-och-lucksta` (ren energitariff, ingen effektdel alls) är inte berörd av frågan — request-posten begränsas, `member_ids` tas bort samtidigt. |
| R15 | `falu-energi-vatten` | Prisgrupp över 500 kW i Bjursås, Grycksbo, Sundborn eller Svärdsjö, endast om sådana kunder ingår. | **TAS BORT** | Löses mekaniskt av `KravPost.maxvarde=500` på ytterorternas rad (§6a.1). Falun berörs inte och har ingen egen öppen fråga. |

**Sammanfattning:** 8 förfrågningar (`R04, R05, R06, R11, R12, R13, R15`, plus R10 utan
begränsning) TAS BORT helt — deras frågor är redan besvarade av verifieringslistan eller
löses mekaniskt av ett nytt kontraktsfält (§6a), inte av request-processen. 2 förfrågningar
(`R03, R14`) FÅR `tariff_ids` satt till exakt de `blocked_external_info`-tariffer frågan
gäller, så `blockerade_tariff_ider(katalog)` (**rättat P2, granskning `2026-09-08-007`**: v7
skrev av misstag kvar det borttagna v6-namnet `oppna_tariff_ider()` här — den faktiska
funktionen är `blockerade_tariff_ider()`, se §7:s inledning) aldrig råkar exkludera en
produkt som ska förbli redo — samma representation, inget "delas eller läggs till" kvar som
öppet val.


## 8. Räkningskontroll

| Disposition | Bastariffer (§3–4) | Varianter (§5) | Summa |
|---|---:|---:|---:|
| `implemented_source_verified_annual` | 7 | 0 | 7 |
| `ready_to_implement` | 47 | 10 | 57 |
| `blocked_external_info` | 24 | 4 | 28 |
| `not_applicable` | 0 | 0 | 0 |
| **Summa** | **78** | **14** | **92** |

**Rättat i v16 (bedömning `2026-09-09-006`):** Lidköping Energis två bastariffer
(`lidkoping-energi-lidkoping-041-kw-2026`, `lidkoping-energi-lidkoping-42-kw-2026`) flyttade
från `blocked_external_info` till `ready_to_implement` — leverantörens skriftliga svar
2026-09-09 löste den externa sakfrågan (flödesprisfaktor `N` och hur `Tm` bestäms), se §4.2
och §6a.7. Basfördelningen ändras 45/26 → **47/24**; variantfördelningen 10/4 är oförändrad;
totalen 78 bas + 14 variant = 92 är oförändrad. Dispositionen 7 + 55 + 30 = 92 blir därmed
**7 + 57 + 28 = 92**.

**Oförändrat i v17/v18 (granskning `2026-09-09-010`/`2026-09-09-011`):** V17/V18 rättar
Lidköpings implementationsPLAN (§6a.7, §6a.4) och gör den körbar och konsekvent — INGEN
dispositionsflytt i någon av rundorna. Räkningen förblir **7 + 57 + 28 = 92** (bas 7/47/24,
variant 0/10/4), oförändrad sedan v16. Lidköpings två bastariffer är fortsatt
`ready_to_implement`.

**Oförändrat i v8/v9 (granskning `2026-09-08-007`/`-008`):** enbart tekniska
kontraktsrättningar (aktiveringsordning, värdetyp/kardinalitet, produktingång/UI-metadata,
Stockholm-dispatch/adapterpreflight/serier, Kraftringens motorväg, Jönköpings allow-list) —
ingen post flyttar mellan dispositioner i någon av de två rundorna. 7 + 55 + 30 = 92 var
oförändrat t.o.m. v15, precis som respektive gransknings egen instruktion föreskrev
(v8-rundans punkt 7, v9-rundans punkt 7) — se rättningen ovan för v16:s enda dispositionsflytt
sedan dess.

**Rättat i v7 (granskning `2026-09-08-006`, Codex/Roberts beslut):** Jönköpings
accessavgiftsvariant flyttad från `blocked_external_info` till `ready_to_implement` (§5) —
varianternas fördelning ändras från 9/5 till 10/4, totalen 14 variant-ID:n oförändrad.
Verifierat: 7 + 55 + 30 = 92, och 78 (bas) + 14 (variant) = 92.

Rättat i v4 (granskning `2026-09-08-003`, P1/P2): Finspångs spetsvärmetillägg flyttad från
`ready_to_implement` till `blocked_external_info` (utlösningsvillkoret inte kartlagt, se §5).

**Oförändrat i v5/v6 (granskning `2026-09-08-004`/`-005`):** v5 lade till en verklig, körd
grindpreflight (§6) och fördjupade obligatorisk-indata-/motorbedömningar för 16 av de 45
`ready`-raderna. v6 bytte grind-only-preflighten mot en fyrstegs sammansatt
aktiveringspreflight, specificerade fyra konkreta kontraktstillägg (§6a) och bytte
requestens datastruktur till `tariff_ids` (§7). Ingen av dessa två rundor flyttade någon
post mellan dispositioner — bara v7:s Jönköping-beslut ändrar räkningen sedan v4.

**Modell för kontrollmängden, uttryckligt (granskning 2026-09-08-003, P2):** kontrollmängden
är **78 bastariffer + 14 räknade varianttäckningskrav = 92**, inte 78 fristående produkter.
En variant byggs ofta i SAMMA implementationscommit som sin bastariff (t.ex. Borås
miljötillägg i batch 6) — det är en räknad TÄCKNINGSKRAV, inte en andra, fristående tariff.
Batch 6:s tabellrad i `batchplan-v4.md` visar därför uttryckligen "2 bastariffer + 1
varianttäckning", inte "2 tariffer", för att undvika att miljötillägget räknas två gånger
eller inte alls (v3:s batchsumma 54 i stället för 55 berodde exakt på denna otydlighet).

Rättat i v3 (granskning `2026-09-08-002`): Eskilstuna flyttad från `ready_to_implement` till
`blocked_external_info` (P1 — nätreferensen inte verifierad, se §4.2). Samtliga sju
variantfamiljer (14 variant-ID:n, se §5) är nu räknade i totalen i stället för att stå
utanför den — kontrollmängden är därför nu **92 räknade enheter**, inte 78.

**Härledning av 79 unika råenheter innan variantutbrytningen (oförändrad från v2):** 78
katalograder + 1 separat förvaltad leverantörsfil (Stockholm Exergi, samma produkt som
katalograden, räknas en gång) + 1 separat förvaltad schablonfil (Riksgenomsnittet, §9,
`not_applicable`) = 80 råa kontrollposter → 79 unika enheter = 78 tariffprodukter + 1
syntetisk schablon. Variantutbrytningen i §5 lägger sedan till 14 räknade variant-ID:n
UTAN att ändra denna 79-härledning — varianterna är delar av redan räknade bastariffer, inte
nya råa katalogposter.

**Leverantörer vs. tariffprodukter (oförändrat från v2):** katalogens 53 `members`-poster
inkluderar redan Stockholm Exergi. **53 fjärrvärmeleverantörer + 1 syntetisk
schablonentitet** (Riksgenomsnittet) = 54 unika leverantörsentiteter, inte 55.

**Dubbletter funna:** exakt en — Stockholm Exergis katalograd mot dess leverantörsfil
(räknas EN gång, som `ready_to_implement`, se §4.1).

## 9. Syntetiska schabloner (separat tabell, inte tariffprodukter)

| Post | Källa | Vad den är | Motivering till `not_applicable` |
|---|---|---|---|
| Riksgenomsnittet | `enkey-agents/skills/ellen/leverantor-riksgenomsnitt.md`, Nils Holgersson-rapporten 2025 | Syntetisk nationell schablon som används när ingen namngiven leverantör är vald eller känd | Inte ett tariffprodukt att implementera — en beräkningsmekanism för det generiska fallet. Se produktdirektivets öppna beslut ([PROJECT_CHARTER §8](../PROJECT_CHARTER.md)) om hur den ska presenteras när en namngiven leverantör saknas: som ett tydligt märkt separat val, inte tyst som om den vore leverantörens egen tariff. |

## 10. Öppna frågor till Codex/Robert

**v7:s runda (granskning `2026-09-08-006`) lämnade inga nya öppna frågor, och v8:s runda
(granskning `2026-09-08-007`) var uteslutande tekniska kontraktsfynd — Codex instruerade
uttryckligen att inga nya Robert-beslut behövs för dem (rättningsbeställning, punkt 7). De
fyra frågorna v6 lämnade öppna är besvarade av Codex i granskning `2026-09-08-006`s avsnitt
"Beslut på V6:s öppna frågor" och tillämpade rakt av, oförändrat i v8:**

1. **Jönköpings accessavgift:** Roberts redan beslutade mål (samtliga möjliga tariffer ska
   implementeras) omfattar en fakturerbar, källkänd, kundkänd avtalsuppgift. Modellerad som
   ett synligt, obligatoriskt kundval på Jönköpings basprodukt (0/10/25/50 kr/mån, inget
   standardvärde, okänt val blockerar), ingen dubblettprodukt. **Beslut tillämpat:** flyttad
   till `ready_to_implement`, se §5 och §8:s uppdaterade räkning (7/55/30 av 92).
2. **E.ON/Navirums batch 3b-ordning:** godkänd oförändrad — en egen, mindre delbatch EFTER
   batch 3:s grundformel.
3. **Batch 5-uppdelningen** (5a/5b/5c): godkänd som rätt arbetsstorlek, men UNDER
   FÖRUTSÄTTNING att det gemensamma bandkontraktet (§6a.2) specificeras för samtliga
   berörda produkter FÖRST. **Beslut tillämpat:** §6a.2 specificerar nu bandkontraktet för
   alla 42 berörda rader innan batch 5 kan starta.
4. **Kraftringens parametriserade motortyp:** godkänd, UNDER FÖRUTSÄTTNING att
   regelvarianten är en explicit, typad diskriminator (inte implicit härledd från
   leverantörs-ID). **Beslut tillämpat:** §6a.5 specificerar det domänriktigt namngivna
   `flodeskorrigering_variant`-diskriminatorn (**rättat P2, granskning `2026-09-08-008`**:
   denna rad hade fortfarande kvar det gamla, missvisande namnet `kapacitet_bindning_variant`
   trots att §6a.5 redan bytt namn — synkroniserat).

Samtliga öppna frågor från v1–v5 är besvarade av Codex i granskningarna `2026-09-08-001`
till `-005` och tillämpade rakt av i tidigare versioner: Vattenfall helt `blocked` som grupp
(batch 8), Sundsvall Matfors följer teknisk-kartläggning v4, leverantörsvärde-mönstret
kräver tariffvis kontroll av VARJE prisdel (genomfört i §4), kända specialvarianter får
aldrig bli `not_applicable` (genomfört i §5 — samtliga 14 integrerade), och E.ON/Navirums
36-månadersmetod är korrekt beskriven som ett dygnsmedeleffekt-leverantörsvärde (§5).

**Ingen ny öppen fråga identifierad i v8-rundan.** Samtliga P1-fynd i granskning
`2026-09-08-007` var körbarhets-/typningsfel i redan beslutade kontraktsdesigner — inga nya
sakfrågor för Robert.
