---
review_id: "2026-09-07-002"
date: "2026-09-07"
reviewer: Codex
status: changes-required
scope:
  - "Rättningar efter kodgranskning 2026-09-07-001"
  - "Sandviken Energi Helleverans, annual_forward och MWh-only"
reviewed_commits:
  skills: "7ba9ec1b6245a72a4720f11b11beec6692af6196"
  enkey-agents: "a5efb7a049e1f522f89cc073db76c7556f62f08b"
  neptune_academy: "a0e5a975c437e5875effe8f6bc85ed4ac977cbdb"
implementation_changed: false
push_status: not-approved
---

# Omgranskning av Sandviken-rättningarna

## Beslut

Rättningscommitsen stänger huvuddelen av fynden i granskning `2026-09-07-001`.
`calcResult` skiljer nu MWh från kronor och schablon, energinumeriken valideras,
kontraktsfasaderna upprätthåller effektens heltals-/minimikrav och katalogmetadata,
felorsaker samt dokumentation är rättade. Alla 362 Python- och 405 TypeScript-tester,
typkontrollen, produktionsbygget, korssynken och det giltiga webbläsarflödet passerar.

**Push är ändå inte godkänd ännu.** Två delar av samma tidigare P1-krav är fortfarande
kringgångbara: den exporterade produktentryn saknar maskinläsbar MWh-proveniens, och en
närvarande kontraktsmarkör med värdet `undefined` behandlas uttryckligen som frånvarande.
Båda rättningarna är små och avgränsade; ingen ny planversion eller modelländring behövs.

## Kvarvarande fynd

### P1 — den exporterade produktentryn kan fortfarande inte skilja faktisk MWh från härlett värde

`BesparingsvardeArgs` i
`neptune-marketing/src/utils/besparingsvarde.ts:198-214` bär bara talet `totalMwh`, inte
dess källa eller inmatningsläge. Den nya kontraktsgrenen på rad 241-250 verifierar korrekt
att talet är ändligt och större än noll, men kan fortfarande inte avgöra om det kommer
från användarens MWh-fält, en kroninvers eller en areabaserad schablon.

`calcResult` gör nu rätt kontroll på rad 470-482, men anropar därefter den exporterade
`beraknaBesparingsvarde` utan att föra kontrollens proveniens vidare. Ett annat gränssnitt
kan därför anropa samma publika produktentry direkt med ett positivt härlett tal.

Codex reproducerade mot `a0e5a97`:

```text
beraknaBesparingsvarde({
  totalMwh: 1200,
  paverkbarMwh: 900,
  besparingsgrad: 0.15,
  leverantorId: "sandviken-energi-sandviken-normal",
  kapacitetKw: 100
})

=> CALCULATED 898187.5
```

Anropet innehåller ingen maskinläsbar uppgift om att `1200` faktiskt angavs i MWh. Det
är exakt den exporterade kringgång som rättningskravet i `2026-09-07-001` bad att stänga;
numerikdelen är rättad, men proveniensdelen återstår.

**Begärd rättning:** låt den kontraktsgatade produktentryn kräva en explicit, typad
energikälla eller ett uttryckligt MWh-läge. För detta vidare från `calcResult` först efter
att `energyInputMode === "mwh"` och energitalet har validerats. Legacytariffernas publika
anropskontrakt kan förbli bakåtkompatibelt, men Sandviken-grenen ska blockera när
proveniens saknas eller inte betyder faktiskt angiven MWh. Lägg ett negativt direktanrop
utan proveniens och ett positivt direktanrop med godkänd MWh-proveniens.

### P1 — närvarande markör satt till `undefined` ger fortfarande naken fallback

Kommentaren ovanför `kontraktsgatadPolicy` säger korrekt att endast en helt frånvarande
egenskap får ge `undefined`. Implementationen på
`neptune-marketing/src/utils/besparingsvarde.ts:156-159` gör däremot ett extra undantag:

```ts
if (!("_kraver_kontrakt" in prisar) || prisar._kraver_kontrakt === undefined) {
  return undefined;
}
```

Codex reproducerade:

```text
kontraktsgatadPolicy({
  tariff_id: "test",
  _kraver_kontrakt: undefined,
  policy: null
})

=> undefined
```

Egenskapen finns alltså men skickas ändå till legacyvägen. `undefined` kan inte komma ur
ren JSON, men prisårsposten är ett JavaScript-objekt och resolverns publika kontrakt samt
kommentar lovar fail-closed för varje närvarande feltypad markör. De nya testerna täcker
`false`, `null`, sträng och tal, men utelämnar just detta specialfall.

**Begärd rättning:** returnera `undefined` endast när
`!("_kraver_kontrakt" in prisar)`. Om egenskapen finns ska även värdet `undefined`
avvisas av kravet på exakt boolean `true`. Lägg det värdet i det befintliga parametriserade
negativtestet.

## Bekräftat rättat

- `calcResult` blockerar nu `kr` och `schablon` även när ett positivt `energyMwh` råkar
  finnas, medan giltigt `mwh` räknar.
- Tomt MWh får `missing_energy`; 0, negativt, `NaN` och oändlighet får
  `invalid_energy` i domänkontraktet. Webbläsaren stoppar även 0/negativt via fältets
  `min=1` innan submit.
- Kontraktsgrenen avvisar 0, negativt, `NaN` och oändligt `totalMwh` innan fördelning och
  kostnadsberäkning.
- Feltypade markörer `false`, `null`, `"true"` och `1` kastar. Policy-ID måste matcha och
  `annual_forward` måste finnas; oväntat `blocked` klassas som konfigurationsfel.
- `KravPost.minvarde/heltal` speglas i Python och TypeScript. Sandvikens delade
  kontraktsfasader avvisar 2, 2,9 och 49,5 kW och accepterar heltal från 3 kW utan dold
  normalisering.
- UI-fältet är fortsatt obligatoriskt med `min=3` och `step=1`; giltigt 1 200 MWh/100 kW
  gav resultat utan synligt fel i den byggda applikationen.
- Katalogens `as_of` är `2026-09-06`. Den genererade filens SHA-256
  `a35fc95b741c6af9a3d1462dbd3e23c12577e2f1f1b75bd05b6ab6f484b52bcd` matchar katalogen
  och proveniensraden pekar på exakt `skills@7ba9ec1b6245a72a4720f11b11beec6692af6196`.
- Policyregisterkommentaren beskriver nu Sandviken som den första aktiverade
  katalogtariffen.

## Sista avgränsade rättningsbeställning till Claude

1. För MWh-proveniens genom den publika `beraknaBesparingsvarde`-gränsen och kräv den i
   kontraktsgrenen; bevara legacykompatibiliteten.
2. Lägg ett negativt direktanrop utan/med fel energiproveniens samt ett positivt med
   uttryckligen godkänd MWh-proveniens.
3. Ta bort specialfallet som behandlar en närvarande `_kraver_kontrakt: undefined` som
   frånvaro och lägg det i markörens negativtest.
4. Kör Vitest, `tsc --noEmit`, produktionsbygge och `git diff --check`; ingen ändring i
   `skills` eller `enkey-agents` förväntas för dessa två återstående fynd.
5. Skapa en fokuserad lokal commit i `neptune_academy` och stanna för slutomgranskning.

Ändra ingen tariffdata, effektmodell, `annual_inverse`, annan leverantör eller redan
fungerande legacyväg. Pusha inte före nästa Codex-kontroll.

## Utförda kontroller

```text
enkey-agents@a5efb7a: tools/tariffer        362 passed
neptune_academy@a0e5a97: Vitest             405 passed
TypeScript: npx tsc --noEmit                 godkänd
Produktionsbygge: npm run eval:build         godkänd
git diff --check, tre rättningscommits        godkänd
Playwright, byggd localhost-app              giltigt MWh-flöde godkänt
Direkt repro: kr/schablon + positiv energi   blockerade
Direkt repro: ogiltig energinumerik          blockerad
Direkt repro: positiv energi utan proveniens beräknades (P1)
Direkt repro: närvarande undefined-markör     gav legacy-fallback (P1)
```

Bygget gav endast den redan kända varningen om stora bundle-chunks. Python gav en
sandboxrelaterad varning om att pytest-cachen inte kunde skrivas, men samtliga tester
passerade. Implementationsrepona är rena och lokalt opushade; Ellen-repots befintliga
ospårade/orelaterade arbetsfiler har inte ändrats av granskningen.

Codex ändrade ingen implementation, tariffdata, commit eller push.
