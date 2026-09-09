---
review_id: "2026-09-09-005"
date: "2026-09-09"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v14.md
  - Fjarrvarmetariffer/batchplan-v14.md
  - skills commit f4f23702eccf8480022eab177a0aee6b9a20224c
reviewed_heads:
  skills: "f4f23702eccf8480022eab177a0aee6b9a20224c"
  enkey-agents: "fd8f8da3eb17cce638dc2f3370efa027c2afcad6"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-09-004"
---

# Omgranskning av tariffinventering v14 och batchplan v14

## Bedömning

V14 löser huvuddelen av V13-fynden. Förkontrollen har nu ett uttryckligt annual-scope,
felorsakerna är enhetliga, `KontraktBlockerat` har en konstruerbar optionsväg,
produktförmågan läser korrekt från `gated.policy`, energisystemet kontrolleras före
tariffuppslagningen och `onskadTyp` är bakåtkompatibelt valfritt. De tidigare ospårade
granskningarna 003 och 004 ingår också i committen.

Argumentbyggaren är däremot fortfarande inte implementeringsbar. Kodblocket jämför de
verkliga TypeScript-unionerna mot tre värden som inte finns, lämnar själva
scope-uppskalningen som ett no-op och delar fortfarande inte basobjektet med `calcResult`.
En isolerad TypeScript-kontroll reproducerar fyra kompilatorfel. Den publika
årsproduktsbeskrivningen visar inte heller hur dess valfria energi-, kapacitets- och
policyfält blir validerade och avsmalnade innan de skickas till hjälpare som kräver dem.
Slutligen saknas fortfarande de uttryckligen beställda råformsgrindarna i parsern.

Det krävs därför en koncentrerad V15-rättning. Ingen produktkod, tariffdata, aktivering
eller push är godkänd.

## P1-fynd

### P1 — `argsFranInputs` använder fortfarande omöjliga värden och innehåller en platshållare

Inventering rad 3037–3058 kallas en verklig, typkorrekt extraktion ur `calcResult`, men
kodblocket gör följande jämförelser:

```ts
inputs.energyScope === 'rumsvarme'
inputs.energyInputMode === 'rumsvarme_andel'
inputs.energyInputMode === 'confirmed_mwh'
```

Dagens `EnergyScope` är
`'total_incl_dhw'|'space_heat_excl_dhw'|'purchased_hp_electricity'|
'delivered_heat_from_hp'`, och `EnergyInputMode` är `'schablon'|'mwh'|'kr'`.
TypeScript ger därför `TS2367` för alla tre jämförelserna. Proveniensen blir aldrig
`'confirmed_mwh'`, så den kontraktsgated årsprodukten skulle blockeras även med korrekt
MWh-indata.

Scope-logiken är inte heller extraherad: `totalMwh = totalMwh` är ett no-op och kommentaren
hänvisar implementatören till att kopiera den riktiga formeln senare. Den verkliga koden
använder `calcEnergyMwh(inputs)`, testar
`inputs.energyScope === 'space_heat_excl_dhw'` och skalar med
`energyMwh / (1 - VARMVATTEN_ANDEL)`. `inputs.energyMwh ?? 0` har dessutom ett annat
beteende än `calcEnergyMwh` och normaliserar saknad energi till noll innan den utlovade
fail-closed-valideringen visats.

Inventering rad 3069–3074 och batchplan rad 243–246 säger samtidigt att `calcResult`
fortsätter bygga alla tre `BesparingsvardeArgs` inline och ska vara oförändrad. Därmed finns
två kopior av exakt den scope-/provenienslogik som granskning 004 krävde skulle delas.

**Begärd rättning:** skriv fullständig, kompilerbar kod mot de faktiska enumvärdena och den
exakta befintliga formeln; ingen no-op eller ”kopiera senare”-text får finnas. Extrahera en
enda bastyp/hjälpare som både aktuell-årskostnaden och `calcResult`s min/mid/max-anrop
faktiskt använder. `energyProvenance` ska sättas endast när
`energyInputMode === 'mwh'`, `energyMwh` finns och är ändlig och positiv.

### P1 — den publika årsproduktens fail-closed-kontrakt är inte körbart beskrivet

`Tariffberakningsunderlag` gör `kapacitetKw`, `policyFalt` och `energyProvenance` valfria.
Den efterföljande hjälparen `byggKontraktIndata` kräver däremot `kapacitetKw: number` och
`policyFalt: Record<string, PolicyInputValue>`. Inventering rad 2963–2979 säger bara att
`beraknaArsprodukt` kör förmågeguard, bygger indata, förkontrollerar policy och anropar
fasaden. Den visar ingen kontroll som avsmalnar de valfria fälten, inget
`kapacitetsGolv(prisar)`-krav och ingen kontroll av `energyProvenance` eller ändlig positiv
`totalMwh` innan motorn nås.

Påståendet på rad 3132–3135 att den nya publika entryn återanvänder alla befintliga
energi-/kapacitetskontroller stöds därför inte av den normativa flödesbeskrivningen. Ett
direkt anrop kan fortfarande bära nollenergi, saknad proveniens eller saknad/ogiltig
kapacitet; alternativt uppstår typfel redan när de valfria fälten skickas till den smalare
hjälparen.

Sidwrappern har dessutom `return { typ: 'aktuell_arskostnad', ...resultat }` trots att
`ArsprodukResultat` redan innehåller samma obligatoriska `typ`. TypeScript reproducerar
`TS2783` för den dubblerade egenskapen.

**Begärd rättning:** visa den fullständiga kroppen för `beraknaArsprodukt` med samma
ordning och orsaker som dagens kontraktsväg: resolve/gate, bekräftad MWh-proveniens,
ändlig positiv energi, närvarande ändlig heltalskapacitet över tariffgolvet,
policyindatabygge, omfattningsmedveten förkontroll och först därefter fasaden. Låt en tom
`policyFalt`-karta representeras explicit om den ska tillåtas; använd inte en non-null-cast
för att kringgå valideringen. Wrappern ska returnera `resultat` direkt eller bygga en form
utan dubblerad diskriminator.

### P1 — parserns beställda scalar/array-grindar saknas fortfarande

`PolicyRawFormValue` tillåter både `string` och `readonly string[]`. Metadata bestämmer om
ett fält ska vara skalärt eller en serie. V14 rad 2118–2135 beskriver tomhets-, numerik- och
kardinalitetsfall men kontrollerar fortfarande inte den råa värdeformen med
`typeof ravarde === 'string'` respektive `Array.isArray(ravarde)`.

En scalar kan därför få en array och nå en beskriven `.trim()`-operation, medan ett
seriekrav kan få en ensam sträng, vars `.length` och iteration fungerar per tecken. Orsaken
`'typ'` finns i `PolicyParseResultat`, men dokumentet visar fortfarande ingen väg som
producerar den. Granskning 004 begärde uttryckligen dessa grindar och testfall med omkastad
råform.

**Begärd rättning:** scalar-/enum-/bandgrenarna ska först kräva en sträng; seriegrenen ska
först kräva en array. Fel form ska ge `{status:'ogiltigt', orsak:'typ'}` före `.trim()`,
`.length` eller iteration. Lägg testfall för array till scalar och string till serie i både
parserenheten och sidintegrationen.

## P2-fynd

- V14 kallar förkontrollens filter ”identiskt” med `harledResultatstatus`, men den verkliga
  fasaden filtrerar även på `tillampligaManader` när `manad` är satt. För dagens två
  annual-anrop reduceras filtren till samma sak. Antingen ska hjälparen uttryckligen vara
  annual-only, eller få `manad`/motsvarande options så det utlovade framtida
  `monthly_invoice`-anropet inte kräver vinterfält under en sommarmånad.
- Inventering rad 2318–2321 placerar `KontraktBlockeratOrsak` i
  `resultatkontrakt.ts`; den verkliga typen och klassen finns i `besparingsvarde.ts`.
  Batchplanens fillista har rätt fil. Synka den normativa texten.

## Verifieringar

- `skills@f4f2370` ändrar bara V14-dokumentation och konversationslogg. Ingen produktkod,
  tariffdata, genererad frontendfil eller aktivering ändrades.
- `git diff --check b467d0a..f4f2370` är rent. Den verifierbara committiden är
  `2026-09-09T10:03:59+02:00`.
- Produktrepoerna är rena och oförändrade på `enkey-agents@fd8f8da` och
  `neptune_academy@f1df177`.
- En isolerad `npx tsc --noEmit --strict --skipLibCheck` mot V14-skissens verkliga
  `EnergyScope`-/`EnergyInputMode`-unioner reproducerade tre `TS2367` och ett `TS2783`.
  Den tillfälliga kontrollfilen togs bort efter körningen.
- V14 innehåller samma 78 bastariffrubriker och redovisar fortsatt 78 bas + 14 varianter =
  92, med dispositionen 7 implementerade, 55 redo och 30 blockerade.
- De tidigare ospårade granskningsfilerna `2026-09-09-003` och `2026-09-09-004` är nu
  spårade i commit `f4f2370`.
- Lokal `main` är 18 commits före `origin/main` och inte efter. V14 är inte godkänd för
  push.
- Inga fulla produkttester kördes eftersom V14 bara ändrar planeringsdokumentation och de
  beskrivna gränssnitten ännu inte finns i produktkoden.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v15.md` och `batchplan-v15.md`; ändra inte V14 i efterhand.
2. Ersätt `argsFranInputs`-blocket med fullständig kompilerbar kod som använder dagens
   riktiga enumvärden, scope-formel och MWh-proveniens.
3. Låt samma basobjekt/hjälpare faktiskt användas av både aktuell-årskostnaden och
   `calcResult`s tre besparingsanrop; skriv inte att `calcResult` samtidigt är oförändrad.
4. Visa en komplett, typavsmalnande och fail-closed `beraknaArsprodukt`-kropp för energi,
   kapacitet och policyfält. Ta bort den dubblerade `typ`-spridningen i wrappern.
5. Lägg explicita scalar/array-grindar och omkastade råformstester i parserkontraktet.
6. Antingen avgränsa förkontrollen till annual eller spegla fasadens månadstillämplighet;
   rätta också ägarfilen för `KontraktBlockeratOrsak`.
7. Bevara V14:s lösta scope-parameter för annual, enhetliga orsaksunion,
   `KontraktBlockerat`-optionsväg, `.policy`-åtkomst, energisystemguard, valfria
   `onskadTyp`, `GenereradPrisarspost`, adaptersemantik och dispositionerna 7/55/30 om ingen
   sakstatus ändras.
8. Ta med denna granskning i nästa fokuserade dokumentationscommit, logga verklig hash/tid
   och stanna för omgranskning.
9. Ändra ingen produktkod eller tariffdata och pusha inte.
