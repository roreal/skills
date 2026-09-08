---
proposal_id: "2026-09-06-001"
version: 3
date: "2026-09-06"
author: Claude
status: implementerad, godkänd i granskning 2026-09-07-003 och pushad till origin/main i alla tre repon 2026-09-07
relates_to: "Slutgodkännande 2026-09-07-003 (approved-for-push); Omgranskning 2026-09-07-002 (changes-required, rättad); Kodgranskning 2026-09-07-001 (changes-required, rättad); Godkännande 2026-09-06-006 (approved-with-conditions på v3); Granskning 2026-09-06-005 (changes-required på v2); Granskning 2026-09-06-004 (changes-required på v1)"
---

# Förslag v3: koppla Sandviken Energi Helleverans (Familj 4) till resultatkontrakt/policyregister

Ersätter v2 i sin helhet. Svarar på Codex fem P1- och tre P2-fynd i granskning
`2026-09-06-005`. Fortfarande ingen kod.

## Vad som var fel i v2, utan omskrivning

v2 antog att `prisar.policy` finns på prisårsposten för en katalogtariff — det gör den
INTE i dagens `bygg_ts_fran_katalog` (policyn hamnar på leverantörsobjektet,
`entry["policy"]`, medan `_kraver_kontrakt` ligger i prisårsposten). Grenlogiken
`if (policy)` skulle dessutom ha fångat Stockholm Exergis redan pushade `validated`-policy
(som finns på RÄTT ställe men bara täcker `monthly_invoice`) och felaktigt blockerat dess
redan levande årsprognos och kronorflöde. `resultatBlockerat`-returen passade inte
`Besparingsvarde`-typen eller `calcResult`s tre anrop, och jag skrev av misstag
`summaExkl` där produktionskoden konsekvent använder `summaInkl`. Jag körde också
användarens inmatade effekt genom `normaliseraKapacitet` (avrundning + golvklämning) INNAN
den märktes `supplier_value`/`verified` — exakt det granskning 004 redan förbjöd, och jag
beskrev dessutom `Math.round`s avrundningsregel fel (JavaScript rundar positiva halvtal
UPPÅT, inte "till jämnt" — tack för rättelsen). Etikettändringen skulle inte synas
(generatorn visar bara produktsuffixet när en medlem har FLERA godkända tariffer, och
Sandviken blir den enda), och jag glömde att spärra `schablon`-läget, bara `kr`-läget.
Baslinjen "62 godkända tariffer" var fel — det är 6 i dag, 7 efter denna pilot.

## 1. Policyplacering: flytta katalogvägens policy till prisårsposten

`bygg_ts_fran_katalog` (generera.py) ändras så `entry["prisar"][0]["policy"]` sätts, i
stället för `entry["policy"]` — samma plats Stockholm Exergis leverantörsfilspolicy redan
ligger på. En liten, väldefinierad ändring: policyn flyttar en nivå ner i samma dict som
redan byggs, ingen ny datastruktur.

```python
# generera.py, i loopen över godkanda katalogtariffer:
prisar_post = till_prisar(t)
if t["id"] not in legacy_undantagna:
    policy = kontrollera_aktiveringsgrind(t["id"], t.get("contract_required"), register=policyregister)
    prisar_post["policy"] = _policy_till_json(policy)  # FLYTTAD hit, inte på entry
entry = {"id": tid, "namn": etikett, "kalla": "katalog", "prisar": [prisar_post]}
```

## 2. Gate-logik i produktadaptern: `_kraver_kontrakt`, inte policyförekomst

Ny, delad hjälpfunktion i `besparingsvarde.ts` som BÅDA MWh-vägen och spärr-kontrollerna
använder:

```ts
function kontraktsgatadPolicy(prisar: any): Tariffpolicy | undefined {
  const kraverKontrakt = prisar._kraver_kontrakt === true;
  if (!kraverKontrakt) return undefined;  // Stockholm Exergis validated-fall: ingen markör -> orört
  if (!prisar.policy) {
    throw new Error(`Konfigurationsfel: ${prisar.tariff_id} har _kraver_kontrakt men ingen policy.`);
  }
  const policy = policyFranGenererad(prisar.policy);
  if (!policy.tackning.includes('annual_forward')) return undefined;  // t.ex. Stockholm Exergi om markören någonsin sattes utan årstäckning
  return policy;
}
```

`beraknaBesparingsvarde` grenar på `kontraktsgatadPolicy(prisar) !== undefined` — inte på
`prisar.policy` rått. Stockholm Exergis `validated`-fall har `_kraver_kontrakt` falskt (per
granskning 2026-09-06-003: "sätter aldrig markören i denna etapp") och lämnas därför
strukturellt oberört av denna gren, oavsett att den bär en policy. Kronor-spärren (punkt 5)
använder samma funktion: `kraverKontrakt=true` + policy utan `annual_inverse` → blockera.

## 3. Typkorrekt blockeringskontrakt: ett domänfel, inte ett partiellt resultatobjekt

`Besparingsvarde` och `calcResult`s tre anrop rörs INTE. I stället: en ny exporterad
felklass i `besparingsvarde.ts`, fångad i `KalkylatorPage.tsx`s REDAN BEFINTLIGA
`calcResult`-catch (rad ~368–374, samma ställe `kapacitetsfelText` redan hanteras) —
samma mönster, inte ett nytt.

```ts
export class KontraktBlockerat extends Error {
  constructor(public readonly tariffId: string, public readonly status: Resultatstatus) {
    super(`KONTRAKT_BLOCKERAT:${tariffId}`);
  }
}

// I beraknaBesparingsvarde, kontraktsgrenen:
const status = harledResultatstatus(policy, indata, { tackningsomrade: 'annual_forward' });
if (status.fullstandighet === 'blocked') {
  throw new KontraktBlockerat(prisar.tariff_id, status);
}
// annars: beraknaArskostnadMedKontrakt två gånger (före/efter), kostnad.summaInkl
// oförändrat — SAMMA fält den nakna vägen redan använder, inte summaExkl.
```

```ts
// KalkylatorPage.tsx, i den befintliga catch-blocket kring calcResult:
} catch (err) {
  if (err instanceof KontraktBlockerat) {
    setFormError('Debiterbar effekt måste anges för Sandviken Energi — Helleverans för att kunna räkna en besparing.');
    return;
  }
  const felText = form.energySystem === 'fjarrvarme' && err instanceof Error
    ? kapacitetsfelText(form.leverantorId, err)
    : null;
  ...
}
```

Ett blockerat kontraktsresultat når alltså aldrig `energiPotential.ts`s
`KalkylatorResult`-sammansättning — det stoppas vid samma punkt ett redan känt,
existerande domänfel stoppas.

## 4. Ingen normalisering på Sandvikens kontraktsväg — bara entydiga råa heltal

`normaliseraKapacitet`/`Math.round`/golvklämning används INTE för Sandvikens
`IndataPost`. I stället, i den nya kontraktsgrenen:

```ts
const kw = args.kapacitetKw;
if (kw === undefined || !Number.isInteger(kw) || kw < 3) {
  // Blockerar (via KontraktBlockerat), rör inte det inmatade talet, gissar inget band.
  throw new KontraktBlockerat(prisar.tariff_id, { omfattning: 'annual', noggrannhet: null, fullstandighet: 'blocked' });
}
// kw förs OFÖRÄNDRAT till IndataPost — exakt det talet användaren skrev in.
```

Decimaler och värden under 3 kW blockeras — inte avrundas, inte gissas. En riktig
band-ID-bindning (Codex alternativ 2) är en större, separat arkitekturändring som inte
ingår i denna pilot; jag väljer alternativ 1 (entydiga råa heltal) som den minsta
fail-closed lösningen.

**Gränstester (OFÖRÄNDRADE indata, ingen normalisering i testet heller):** 3, 49, 50, 199,
200 kW ska accepteras och ge rätt band i `_niva`/`nivaFor`, krontal identiska mellan
Python och TypeScript. 2.9, 49.4, 49.5, 49.6, 199.9 och 200.1 kW ska blockeras — testet
bevisar att blockeringen sker, inte vilket band ett avvisat värde "borde" fått.

## 5. Kronor- OCH schablonläge blockeras, med en verklig genererad etikett

`kontraktsgatadPolicy` (punkt 2) används i BÅDA `rawEnergyFranArskostnad` (kr-läget) OCH
direkt i `KalkylatorPage.tsx`s submit-hanterare för schablonläget: om
`form.energySystem === 'fjarrvarme'`, en leverantör med `kraverKontrakt` är vald, OCH
`form.energyInputMode` inte är det läge där ett faktiskt MWh-tal angetts (dvs. läget är
`kr` eller `schablon`) — blockera INNAN någon beräkning påbörjas, med samma
`KontraktBlockerat`-mönster och ett schablon-specifikt meddelande
("Sandviken Energi — Helleverans kan för närvarande bara räknas med angiven energi i MWh").

**Etiketten görs verklig i generatorn**, inte bara i katalogfältet: `bygg_ts_fran_katalog`s
villkor för att lägga till produktsuffixet ändras från "medlemmen har fler än en godkänd
tariff" till "medlemmen har fler än en godkänd tariff ELLER tariffens
`network_or_product` skiljer sig från medlemsnamnet":

```python
etikett = namn_per_medlem.get(medlem, medlem)
produktnamn = t["network_or_product"].strip()
if len(tariffer) > 1 or produktnamn.lower() != etikett.strip().lower():
    etikett = f"{etikett} — {produktnamn}"
```

Katalogens `network_or_product` för Sandviken sätts till `"Helleverans"` (inte upprepning
av bolagsnamnet, per Codex P2-fynd), vilket ger exakt `"Sandviken Energi — Helleverans"` i
den genererade dropdownen. Ingen befintlig enskild-tariff-medlem vars `network_or_product`
redan upprepar medlemsnamnet (t.ex. Norrenergi) påverkas, eftersom villkoret för dem redan
är falskt på båda sidor av `or`. Regressionstestet kör den RIKTIGA genererade
`tariffer.generated.ts`/motsvarande Python-utdata och läser dropdown-etiketten, inte bara
katalogfältet isolerat.

## 6. Fullständig `Tariffpolicy` och katalogmetadata

```python
KravPost(
    nyckel="debiterbar_effekt_kw", enhet="kW", kravs_for=("annual",),
    tillatna_kallor=("supplier_value",), matupplosning="arsvis",
    kalperiod_definition="", tillamplighet="samtliga manader",
    kalla="Sandviken Energis faktura (debiterbar effekt)",
    rullande=False,  # Codex svar: historikgrundad, uppdateras en gang per ar — inte löpande föränderlig
)
Tariffpolicy(
    tariff_id="sandviken-energi-sandviken-normal-2026",
    kravda_falt=(ovanstaende,), tackning=frozenset({"annual_forward"}),
    kapacitet_bindning="debiterbar_effekt_kw",
)
```

**Katalogändringen — exakt vad som ändras, inget annat:**

```json
{
  "investigation": null,
  "issues": [],
  "network_or_product": "Helleverans",
  "source_refs": [
    {"source_id": "sandviken-2026-priser", "pages": null},
    {"source_id": "sandviken-2026-effektmodell", "pages": null}
  ],
  "capacity": {
    "billing_basis_method": "Effektsignatur vid -16 C fran foregaende vinters dygnsvarden okt-apr; annars medel av de tva senaste arens hogsta dygnsmedeleffekt. Leverantorens fakturerade varde anvands tills metoden ar implementerad.",
    "monthly_proration": "days_in_month/days_in_year"
  },
  "contract_required": true
}
```

`investigation: null` matchar EXAKT vad de sex redan legacy-godkända tarifferna har — inget
nytt, odefinierat statusvärde som "kall_verifierad" (Codex P2-fynd). `production_ready`,
`calculation_status` och `component_completeness` lämnas UTAN ÄNDRING — samtliga sex
legacy-tariffer har fortfarande `production_ready: false` och
`calculation_status: "requires_engine_mapping_and_invoice_validation"`, så det är redan det
etablerade mönstret för en tariff som är godkänd nog för `godkanda()` men inte formellt
"färdigcertifierad" i katalogens egna, separata metadatafält. Jag ändrar alltså INGET av de
tre fälten v2 råkade lämna motstridiga. `sources`-listan får de två nya källorna (utan
`pages`, eftersom de är HTML-sidor).

## 7. Regressionsbaslinje och verklig katalog-till-UI-regression

Baslinjen är **6 → 7** godkända katalogtariffer (`godkanda(las_katalog())`), inte 62 — rättat
efter Codex direkta verifiering. Regressionsplanen kompletterar det befintliga,
mock-baserade produktentrytestet med ett test av den RIKTIGA Sandviken-posten genom hela
kedjan:

- katalog → `bygg_ts_fran_katalog` → policyn ligger på `prisar[0].policy`, `_kraver_kontrakt`
  på samma nivå, dropdown-etiketten är exakt `"Sandviken Energi — Helleverans"`;
- Stockholm Exergis `validated`-årsprognos och kronorflöde ger EXAKT samma resultat som
  innan denna ändring (regressionstest mot en sparad referens);
- MWh-läge + giltigt heltal (3–≥200 kW) ger momsinklusive före-/efterkostnad
  (`summaInkl`) och `complete`-status;
- saknad, decimal- eller under-3kW-effekt blockeras via `KontraktBlockerat`, aldrig en
  uppskattning eller ett rått numeriskt värde som smugit igenom;
- kronor- OCH schablonläge blockeras med respektive användartext när Sandviken är vald;
- generatorhuvudets räkneverk (`orsaker["utreds"]` minskar med ett) och ENDAST Sandvikens
  post ändras i den genererade datan — alla andra 5 legacy-tariffer och riksgenomsnittet
  byte-identiska.

## 8. Proveniens: tre samordnade lokala commits, inte en delad commit

"Samma commit" över tre repon är inte möjligt (rättat). I stället: TRE fokuserade lokala
commits, en per repo, som tillsammans utgör EN samordnad kontrollpunkt (inget delvis
pushat, ingen drift mellan repona tills alla tre är granskade):

1. **`skills`-repot:** `git add` av `optimate-fjarrvarme-2026.json` (redan där, ospårad
   idag) med katalogändringen från punkt 6.
2. **`enkey-agents`:** `policyregister.py` (Sandvikens `Tariffpolicy`), `generera.py`
   (policyplacering + etikettvillkor från punkt 1/5), en SHA-256-hash-pin av
   `optimate-fjarrvarme-2026.json` (samma mönster som `test_synk.py`s
   `_FORVANTAD_SHA256`), samt katalogens commit-hash från `skills`-repot skriven in i ett
   litet, spårat genereringsmanifest (t.ex. `tariffer.generated.ts`s kommentarhuvud
   utökas med `// Källkatalog: <skills-repots commit-hash>`) — så den incheckade
   TypeScript-artefakten kan knytas till exakt katalogversionen även när syskonrepot
   saknas lokalt, inte bara genom den redan uppskjutna hårdkodade sökvägen.
3. **`neptune_academy`:** produktadaptern (punkt 2–5), `KontraktBlockerat`, regenererad
   `tariffer.generated.ts`.

Den större omarkitekturen bort från den hårdkodade `KATALOG_SOKVAG` förblir uttryckligen
uppskjuten till en egen etapp.

## Oförändrat till nästa Codex-kontrollpunkt

Ingen kod, katalogdata eller genererad fil ändras förrän v3 är granskad. Övriga Familj
4-medlemmar, Telge, E.ON/Navirum, Sundsvall Matfors, Vattenfall, Stockholm Exergis
`validated`-pilot och kalkylatorns UI i övrigt rörs inte.
