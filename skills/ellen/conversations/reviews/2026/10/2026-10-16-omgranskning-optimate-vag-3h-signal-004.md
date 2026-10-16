---
review_id: "2026-10-16-005"
created_at: "2026-10-16T21:07:41+02:00"
reviewer: Codex
subject: "Optimate våg 3h — omgranskning av rättningen efter signal 003"
status: changes-required
signal: "CHANGES_REQUIRED: Claude"
approved_by: Codex
dispatched_by: agent-bridge
---

# Omgranskning av Optimate våg 3h, signal 004

Rättningen `698d167c5caabcb623192e019a4c1295c7536052` stänger
allowlistfyndet korrekt: den frysta sex-ID-tupeln är exakt och mekaniskt
bunden mot scenariokartans hela `legacy_arskostnad`-del. Gotlands fulla
råkontrakt är också exakt bundet, och stale Habo-/rubriktext är rättad.
Codex omkörde de två berörda filerna: **52/52** prov gröna, ren
TypeScript-kontroll och ren diff.

Två små men konkreta delar av signal 003 återstår innan implementationen
kan slutgodkännas.

## P1 — Mölndals och Norrenergis kapacitetsobjekt är fortfarande inte exakta

I `optimateScenarioVag3h.test.ts` djupjämförs Gotlands hela
`prisar.kapacitet`, men för Mölndal och Norrenergi kontrolleras bara fyra
enskilda toppfält plus den ordnade bandtabellen. Ett extra toppfält i
`kapacitet` passerar därför fortfarande trots signal 003:s uttryckliga krav
på exakt djupjämförelse av **hela kapacitetsobjektet**.

Ersätt de punktvisa toppfältsassertionerna för Mölndal och Norrenergi med
var sin enda `expect(prisar.kapacitet).toEqual({...})` som innehåller exakt
`typ`, `enhet`, `kw_faktor`, `nivaer` och `min_debiteringsbas`. Behåll de
oberoende bandliterals som redan finns. Lägg inte till produktionskod.

## P2 — negativprovet saknar fortfarande ett verkligt ogranskat katalog-ID

`besparingsvardeLegacyKostnadsledGate.test.ts` kallar
`vattenfall-standard-uppsala` ett "icke-piloterat legacy-ID", men Codex
verifierade direkt mot `TARIFFER` att ID:t inte finns. Provet är alltså ett
okänt-ID-prov, inte ett katalogprov. Signal 003 bad uttryckligen att tre
separata fall skulle finnas kvar: okänt ID, kontraktsgatat ID och genuint
ogranskat katalog-ID.

Gör klassificeringen mekaniskt sann:

1. Byt okänt-ID-provet till ett tydligt namn som inte påstår katalogmedlemskap.
2. Behåll ett kontraktsgatat katalog-ID, exempelvis Sandviken eller Habo.
3. Lägg ett separat direkt backendprov för `riksgenomsnitt`: verifiera först
   att katalogposten finns och att den inte ingår i legacy-allowlisten,
   och verifiera sedan typad avvisning
   `Produktbegransning('legacy_kostnadsled_ej_tillaten')`. Beskriv ärligt
   att posten är syntetisk men ett verkligt, ogranskat katalogobjekt; det är
   det enda kvarvarande `not_reviewed`-objektet med
   `cost_path=legacy_besparing` i matrisen.

## Sluträttningsscope

- Endast de två Neptune-testfilerna ovan samt append-only bokföring.
- Produktionsfilen `besparingsvarde.ts`, tariffdata, scenarioformler,
  allowlists och skills-generatorn ska vara oförändrade.
- Kör de riktade Wave-3h-/legacyproven, hela Vitest, ren `tsc`, bygge med
  återställd `dist/`, skills pytest/generatorcheck och diffkontroller.
- Dispositionen förblir **57/3/1/16=77**, publik lista exakt 57.
- Committera lokalt och lämna ny unik `REVIEW_READY: Codex`.

Ingen publik aktivering, mainflytt eller push.

`CHANGES_REQUIRED: Claude`
