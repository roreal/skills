---
review_id: "2026-09-09-007"
date: "2026-09-09"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v15.md
  - Fjarrvarmetariffer/batchplan-v15.md
  - skills commit 2326adcc27d9a294277bcc89a19ecb2ab9ddc7e8
reviewed_heads:
  skills: "2326adcc27d9a294277bcc89a19ecb2ab9ddc7e8"
  enkey-agents: "fd8f8da3eb17cce638dc2f3370efa027c2afcad6"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-09-005"
next_version_also_requires: "2026-09-09-006"
---

# Omgranskning av tariffinventering v15 och batchplan v15

## Bedömning

V15 löser två av V14:s tre blockerande områden. `argsFranInputs` använder nu de verkliga
enumvärdena och scope-formeln, och samma basobjekt är avsett för `calcResult`. Parserns
scalar-/array-grindar och de omkastade råformstesterna är också tydligt specificerade.

Den utskrivna `beraknaArsprodukt`-kroppen är däremot fortfarande inte implementeringsbar.
En isolerad strikt TypeScript-kontroll mot de verkliga produkttyperna gav fem fel, och
kodblocket kringgår dessutom den nyss beslutade fältnära felmodellen med `as any` och fel
orsakskod. Den generiska `policyFalt`-kanalen motsägs också mellan dokumenten: batchplanen
för in fältet i `BesparingsvardeArgs`, medan inventeringen säger att samma typ förblir
oförändrad och att fältet ignoreras av besparingsvägen. Därmed kan framtida kontraktsgated
besparingsberäkningar inte säkert få sina obligatoriska policyfält.

V16 krävs före implementation. V16 ska samtidigt införliva Lidköping Energis nya,
källgodkända regler enligt bedömning `2026-09-09-006`. Ingen produktkod, tariffdata,
aktivering eller push är godkänd.

## P1-fynd

### P1 — `beraknaArsprodukt` följer varken de egna typerna eller den verkliga årsfasaden

Kodblocket i inventeringen rad 3013–3068 innehåller flera oberoende fel:

1. `const tariffId = prisar.id` läser ett fält som inte finns i den egna
   `GenereradPrisarspost`; fältet heter `tariff_id`.
2. `forkontrolleraPolicyIndata(..., policyFalt, 'annual')` skickar en
   `Record<string, PolicyInputValue>`, trots att den beslutade signaturen kräver en
   `ReadonlyMap<string, IndataPost>`. `byggKontraktIndata` måste köras först och dess karta
   förkontrolleras.
3. Den kombinerade felgrenen kastar `'invalid_capacity'` med `{ saknade, ogiltiga } as any`.
   Det motsäger samma dokuments normativa kontrakt: två separata kast med
   `'missing_policy_fields'`/`{ saknadeFalt }` respektive
   `'invalid_policy_fields'`/`{ ogiltigaFalt }`. `as any` döljer just den typavvikelse som
   felmodellen ska förhindra.
4. `beraknaArskostnadMedKontrakt(indata, prisar, kapacitetKw)` har fel ordning och bara tre
   argument. Den verkliga signaturen kräver
   `(prisar, policy, indata, ar, mwhPerManad, opts?)`. Årsenergin måste först fördelas med
   den beslutade värmeprofilen och `fordelaEnergi(totalMwh).totalt` skickas som femte
   argument.
5. `resultat.kostnad.summaInkl` derefererar en typ som är `Kostnad | null` utan att först
   hantera `status.fullstandighet === 'blocked'`/`kostnad === null`.
6. `prisar.leverantor` finns inte i `GenereradPrisarspost`. Funktionen måste behålla
   `leverantor` från `valjLeverantorOchPrisar` och använda `leverantor.namn`.

Den isolerade kontrollen reproducerade `TS2339` två gånger, `TS2345`, `TS2554` och
`TS18047`. Kontrollfilen låg endast i `/tmp` och togs bort efter körningen.

**Begärd rättning:** skriv en komplett V16-kropp som kompileras som helhet, inte bara en
separat kontroll av `argsFranInputs`. Den ska välja `{ leverantor, prisar }`, använda
`prisar.tariff_id`, bygga `indata`, göra de två fältnära förkontrollkasten utan casts,
bygga en tolvmånaders energiprofil, anropa den verkliga fasadsignaturen och avsmalna
`KontraktResultat` innan kostnaden läses.

### P1 — `policyFalt` försvinner ur den kontraktsgated besparingsvägen

Batchplan rad 140–146 säger uttryckligen
`KalkylatorInputs.policyFalt → BesparingsvardeArgs.policyFalt`, vilket är nödvändigt för att
`beraknaBesparingsvardeKontrakt` ska kunna anropa `byggIndataFranPolicy`. Inventering rad
3209–3213 säger i stället att `BesparingsvardeArgs` är oförändrad och att `policyFalt` på
det spridda basobjektet ignoreras av `beraknaBesparingsvarde`.

Ett extra runtimefält kan följa med ett spritt objekt, men
`beraknaBesparingsvarde(args: BesparingsvardeArgs)` och dess kontraktsgren kan inte läsa
fältet typsäkert om interfacet inte deklarerar det. Då saknar alla nya
besparingsprodukter med band-, serie-, temperatur- eller andra policykrav sin planerade
indatakanal.

**Begärd rättning:** välj ett enda kontrakt. Den enklaste konsekventa vägen är att göra
`policyFalt?: Record<string, PolicyInputValue>` till ett additivt fält på
`BesparingsvardeArgs`, låta `beraknaBesparingsvarde` föra samma `args` till
kontraktsgrenen, och låta bara legacygrenen ignorera fältet. Visa anropet
`byggKontraktIndata(..., args.policyFalt ?? {})` och förkontrollen på den byggda
`IndataPost`-kartan. Spegla samma beslut i båda V16-dokumenten.

## P2-fynd

- Dokumenten växlar mellan ”`calcResult` självt ändras inte/oförändrat” och att
  implementationen faktiskt refaktoreras till att anropa `argsFranInputs`. Skriv i V16
  att `calcResult`s **publika resultat och beräkningsbeteende** ska vara oförändrade, medan
  dess interna argumentbyggnad ändras. Det undanröjer motsägelsen utan att backa den
  delade hjälparen.

## Lidköpingstillägg till V16

Bedömning [`2026-09-09-006`](2026-09-09-bedomning-lidkoping-energi-leverantorssvar.md)
är bindande för nästa version. De två Lidköpingstarifferna flyttas från
`blocked_external_info` till `ready_to_implement`. Dispositionen blir 7/57/28 av 92,
basfördelningen 7/47/24 och variantfördelningen fortsatt 0/10/4. Batchplanen får en separat
batch 5d för den signerade månadsvisa nätmedelavkylningsjusteringen. Saknade månadsserier
ska blockera; inga `Tm`-värden får gissas eller hårdkodas.

## Verifieringar

- `skills@2326adc` ändrar bara V15-dokumentation, granskning 005 och konversationslogg.
  Ingen produktkod, tariffdata, genererad frontendfil eller aktivering ändrades.
- `git diff --check f4f2370..2326adc` är rent. Verifierbar committid är
  `2026-09-09T10:34:11+02:00`.
- Produktrepoerna är oförändrade på `enkey-agents@fd8f8da` och
  `neptune_academy@f1df177`.
- V15 behåller 78 bastariffer + 14 varianter = 92 och den före leverantörssvaret korrekta
  snapshotfördelningen 7/55/30. Bedömning 006 flyttar två basposter i nästa version.
- Lokal `main` är 19 commits före `origin/main` och inte efter. Ingen push är godkänd.
- Inga fulla produkttester kördes eftersom V15 bara är dokumentation och de planerade
  gränssnitten ännu inte finns i produktkoden.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v16.md` och `batchplan-v16.md`; ändra inte V15 i efterhand.
2. Rätta hela `beraknaArsprodukt` enligt första P1-fyndet och visa en strikt TypeScript-
   kontroll av den fullständiga kroppen mot verkliga signaturer.
3. Gör `policyFalt`-transporten entydig och typsäker genom hela besparingsvägen enligt
   andra P1-fyndet; ingen dold extra property och ingen cast.
4. Behåll V15:s riktiga enumvärden/scope-formel, delade `argsFranInputs`, parsergrindar,
   råformstester, annual-avgränsning, felorsaksmodell, adaptersemantik och övriga tidigare
   lösta fynd.
5. Inför alla dokumentations- och planändringar för Lidköping i bedömning 006, inklusive
   verifieringslista, två statusflyttar, disposition 7/57/28, batch 5d och fail-closed
   månadsserie-/testkontrakt.
6. Lägg till bedömning 006 och denna granskning 007 i nästa fokuserade
   dokumentationscommit, logga verklig hash/tid och stanna för omgranskning.
7. Staga inte den råa e-post-PDF:en utan Roberts separata beslut. Ändra ingen produktkod,
   tariff-JSON, genererad fil eller aktiveringsgrind och pusha inte.
