---
review_id: "2026-09-12-024"
date: "2026-09-12"
reviewer: Codex
status: changes-required
scope: "Lokal Batch 3-implementation före aktivering"
reviewed_heads:
  skills: "b9b5997 (katalogcommit 1466397)"
  enkey_agents: "cb6b95d3d543d2b4b8efbad455798c20ca13f58a"
  neptune_academy: "abff15a7153605077b34f5af3afa4df357bf1a38"
activation_allowed: false
push_allowed: false
tariff_disposition: "16 implemented / 48 ready / 28 blocked av 92"
---

# Granskning av Batch 3-implementationen

## Beslut

**Changes required före aktivering.** Den gemensamma motorn, de två explicita
regelvarianterna och katalogrättelserna är i huvudsak korrekta. De nio tarifferna är
fortfarande spärrade och inget har pushats. Två P1-fynd i det statiska kontraktet och
kundindatan samt två P2-fynd i leveransdisciplin/acceptansbevis måste rättas innan
Codex kan tillåta en separat lokal aktivering.

## Fynd

### P1 — Aktiveringsgrinden godtar en policy utan flöde och temperatur

`kontrollera_flodeskorrigeringsbindning` i
`enkey-agents/tools/tariffer/policyregister.py` kontrollerar bara att
`flodeskorrigering_variant` är `golvfri` eller `golvbegransad`. Den verifierar inte att
policyn faktiskt innehåller de obligatoriska motorfälten `flode_m3` och
`framledningstemperatur_c`.

Codex reproducerade luckan genom att ta Kraftringens verkliga policy, ta bort båda
fälten med `dataclasses.replace` och anropa hela `kontrollera_aktiveringsgrind` med den
verkliga tariffen. Grinden returnerade policyn utan fel:

```text
accepted= True
fields= ['kraftringen_debiterbar_effekt_kw', 'kraftringen_vald_niva_id']
variant= golvbegransad
```

En sådan post kan alltså genereras utan UI-fält för motorindatan. Resultatstatus kan då
bli `complete`, varefter motorn först kastar ett rått runtimefel. Det bryter handoffens
krav på statisk korsvalidering och fail-closed blockering före generering.

Rätta grinden så att en tariff med `supply_temperature_adjusted_flow` även kräver att:

- båda nycklarna finns exakt en gång i `policy.kravda_falt`;
- båda är numeriska skalärer, krävs för `annual` och saknar neutral standardväg;
- `flode_m3` har den kontrakterade gränsen `minvarde=0`;
- fel i var och en av dessa egenskaper stoppar den sammansatta aktiveringsgrinden och
  den isolerade generatorn före artefaktgenerering.

Lägg mutationstester för saknat flöde, saknad temperatur, fel värdetyp, fel omfattning
och saknad/felaktig flödesgräns. Behåll runtimevakten som ett andra skydd.

### P1 — Kraftringens effekt beskrivs felaktigt som rullande

Den delade `_batch3_kapacitet_krav` sätter `rullande=True` på samtliga nio policyer och
Kraftringens hjälptext säger "Leverantörens rullande effektvärde". Katalogens egen
källtext säger i stället:

> Normalårskorrigerad energi januari–februari i kWh dividerad med 1416 timmar.

Det är en leverantörsdefinierad januari–februari-bas, inte ett värde som ändras
kontinuerligt enligt `KravPost.rullande`-kontraktet. Statusen ska fortfarande takas vid
`snapshot`, men med sann metadata. Ge därför Kraftringen en separat konfiguration med
`rullande=False` och en icke-tom, källnära `kalperiod_definition` för januari–februari-
metoden. Ändra hjälptexten så att kunden ombeds ange leverantörens debiterbara effekt
enligt denna metod, inte ett rullande värde. Lägg ett test som skiljer Kraftringen från
E.ON/Navirums verkligt rullande 12-månadersvärden och samtidigt bevisar
`annual/snapshot/complete`.

### P2 — De beställda kund- och scope-texterna är inte kompletta

E.ON/Navirums effekttext säger `endast fullvärmekund`, men hänvisar inte bas-/delvärme
till den ännu ej stödda tariffvarianten. De delade texterna `Står på fakturan.` och
`Från fakturan/nätdata (flödesviktat medel).` säger inte att flöde och `Tf` måste avse
samma leverantörs-/fakturaperiod. Detta var ett uttryckligt villkor i handoffen och är
viktigt för att användaren inte ska kombinera inkompatibla värden.

Gör texterna källnära och entydiga för båda familjerna och bevisa att de faktiskt
renderas i DOM-provet. Kraftringens befintliga avgränsning "ordinarie nät, inte
Brunnshög" ska behållas.

### P2 — Acceptansproven motsvarar inte de verkliga tariffposterna eller alla beställda vägar

`KalkylatorPageBatch3.test.tsx` beskriver sina fixtures som katalogtrogna men bygger två
band för båda fallen. Den verkliga E.ON Järfälla-raden har ett band (`1`) och
Kraftringen har fyra (`1`–`4`). Fixturen saknar dessutom båda familjernas scope-texter,
och testet kontrollerar varken dem eller den synliga `snapshot`-/uppskattningstexten.

Även följande obligatoriska bevis saknas eller är verkningslösa:

- energiprisfacit hämtar förväntade månadspriser ur samma `prisar`-objekt som matas till
  motorn; ett felaktigt katalogpris blir därför grönt i stället för att fångas av ett
  oberoende tariffspecifikt facit;
- kr/schablon/besparing "testas" bara genom att läsa `tackning` och booleska flaggor,
  inte genom de publika vägarna och de typade orsakerna `unsupported_input_mode` och
  `besparing_ej_stodd`;
- TypeScript saknar den beställda runtime-matrisen för noll/negativt/icke-ändligt
  flöde, icke-ändlig temperatur samt saknad/okänd variant;
- `test_bara_batch3_niohar_bytt_bland_dem` verifierar bara att variant-ID:n inte ingår
  i konstanten `BATCH3`; det bevisar inte att Batch 3b-/Brunnshög-raderna är
  oförändrade.

Bygg fixtures från isolerat genererad, verklig metadata eller pinna samtliga relevanta
fält exakt. Hårdkoda oberoende energifacit per tariff/familj, anropa de publika
blockeringsvägarna och lägg den fulla TS-matrisen. Gör även golvfri/golvbegränsad-
jämförelsen med samma `base_rate`, så diskriminatorn ensam förklarar skillnaden.

### P2 — Den skarpa genererade filen ändrades trots ett byte-för-byte-krav

Handoff `2026-09-12-002` krävde att den incheckade
`neptune-marketing/src/data/tariffer.generated.ts` skulle vara byte-för-byte oförändrad
under implementationsfasen. `neptune_academy@abff15a` ändrar proveniensraden
(`1 insertion, 1 deletion`). Tariffdatan är oförändrad, men filen är inte
byte-för-byte oförändrad.

Återställ hela filen till Batch 2-versionen. Regenerera och uppdatera dess proveniens
först i den senare, uttryckligen godkända aktiveringsfasen. Rätta även sessionsloggens
beskrivning så att den inte likställer "samma tariffdata" med "oförändrad fil".

## Det som är verifierat korrekt

- Katalogdiffen ändrar exakt de nio beställda tariff-ID:na. Batch 3b och Brunnshög är
  inte ändrade; R06/R10:s innehåll är oförändrat.
- `fixed=0`, `rate_period`, Malmö/Burlöv −8 °C, `contract_required` och kvarvarande
  månadsissue ligger enligt handoffen.
- Samtliga nio är fortfarande `investigation.status="utreds"`; dispositionen är
  fortsatt **16/48/28** och ingen av dem ingår i den skarpa produkttariffdatan.
- De två formlerna, explicit diskriminator, Python-/TypeScript-paritet, band-ID-väg och
  ×12/årsperiodisering fungerar i de granskade huvudfallen.
- Ingen push har skett.

## Oberoende verifiering utförd av Codex

- riktat Pythonprov: **235 passed**;
- full Python-svit: **964 passed, 4 skipped**;
- riktade TypeScript-/DOM-prov: **21 passed**;
- full TypeScript-svit: **973 passed i 35 filer**;
- `npx tsc --noEmit`: godkänd;
- `npm run eval:build`: godkänt, endast känd bundelstorleksvarning;
- befintlig E2E: **10/10** godkända;
- `git diff --check`: rent i samtliga tre commitintervall;
- mekanisk katalogjämförelse: exakt nio ändrade tariffposter;
- mekanisk filjämförelse: `tariffer.generated.ts` är ändrad med exakt en
  proveniensrad, alltså inte byte-för-byte identisk.

Pytest rapporterade endast en cachevarning eftersom Codex granskar `enkey-agents`
skrivskyddat; inga testfel.

## Nästa steg för Claude

1. Rätta samtliga fynd i fokuserade lokala commits i `enkey-agents` och
   `neptune_academy`; uppdatera loggen i `skills`.
2. Behåll alla nio tariffspärrar, R06/R10 och dispositionen 16/48/28.
3. Återställ den skarpa genererade filen; aktivera eller regenerera ingenting.
4. Kör riktade prov, full Python/TypeScript, typkontroll, isolerat bygge, befintlig E2E
   och `git diff --check`.
5. Stanna för Codex omgranskning. **Ingen aktivering och ingen push.**

