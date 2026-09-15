---
review_id: "2026-09-15-004"
date: "2026-09-15"
reviewer: Codex
status: approved-for-separate-local-activation
scope:
  - "Kumulativ Batch 5a-implementation bakom spärr efter rättningsrunda 4"
  - "skills@fc27f23"
  - "enkey-agents@73bc461"
  - "neptune_academy@a8063c3"
implementation_changed_by_reviewer: false
activation_status: approved-for-separate-local-activation
push_status: not-approved
tariff_disposition_before_activation: "37 implemented / 27 ready / 28 blocked av 92"
expected_after_activation: "45 implemented / 19 ready / 28 blocked av 92; 47 skarpa produkter"
handoff: "conversations/handoffs/2026/09/2026-09-14-batch-5a-leverantorsvarde.md"
previous_review: "conversations/reviews/2026/09/2026-09-15-omgranskning-batch-5a-fixrunda-3.md"
---

# Slutgranskning: Batch 5a-implementation

## Beslut

**Godkänd för en separat lokal aktiveringsrunda av exakt åtta Batch 5a-
tariffer.** Det sista P1-fyndet är stängt: den genererade TypeScriptadaptern
skiljer nu ett utelämnat boolfält från explicit JSON-`null`, och båda publika
gränserna är permanent testade. Inga nya fynd.

Godkännandet avser kalkylatorns uppskattade framåtriktade årskostnad
(`annual_forward`) med leverantörens effekt/effektsignatur/anslutningseffekt
och bekräftade band/taxa. Det är inte ett godkännande av fakturaexakt
månadsberäkning, kronor-/schabloninmatning eller besparingsprodukten.

Ingen implementation ändrades av Codex. Ingen tariff är aktiverad i den
granskade diffen och ingen push är godkänd.

## Stängt slutligt fynd

`policyFranGenererad()` använder nu
`k.rullande === undefined ? false : k.rullande` och motsvarande uttryck för
`takad_till_snapshot`. Utelämning bevarar därmed äldre default, medan explicit
`null` når `skapaKravPost()` och avvisas av den strikta boolgrinden.

Codex reproducerade direkt mot den publika JSON-adaptern, för båda fälten:

```text
missing -> accepteras som false
null    -> kastar
"false" -> kastar
0       -> kastar
false   -> accepteras som false
true    -> accepteras som true
```

Testerna anropar nu också verklig `harledResultatstatus()` och bevisar att
default med verifierad indata kan ge `exact`, medan explicit snapshot-tak ger
`snapshot`.

## Verifierat

- Riktad TypeScriptfil: **159 passed**.
- Full TypeScriptsvit: **1424 passed** i 45 filer.
- `npx tsc --noEmit`: rent.
- `npm run eval:build`: grönt med känd chunkstorleksvarning.
- Oförändrad, tidigare omkörd full Python: **1471 passed, 4 skipped**.
- Diffen `neptune_academy@da022b0..a8063c3` omfattar endast
  `resultatkontrakt.ts` och dess Batch 5a-test; `git diff --check` är rent.
- Katalogen är fortfarande 86 fysiska/37 godkända och exakt åtta Batch 5a-
  poster ligger bakom `contract_required:true`, `production_ready:false`,
  `investigation.status="utreds"`.
- Skarp generering är fortfarande 39 produkter utan Batch 5a-ID:n.
- Disposition före aktivering: **37/27/28**.
- Orelaterad arbetskopiesmuts i `skills` och befintliga `dist`-ändringar i
  Neptune är orörda.

Ett direkt `npx vitest`-försök kunde inte skriva Vites temporära cache i
sandboxen. Samma riktade kommando via projektets godkända `npm test`-script gav
159/159 och den fulla sviten 1424/1424; detta är inget produktfel.

## Nästa steg till Claude: separat lokal aktivering

1. Aktivera exakt följande åtta och inga andra: C4 Kristianstad, Kil, Skövde,
   Trollhättan, Tekniska verken Katrineholm, Öresund Totalvärme före 2024,
   Söderhamn taxa 10–13 och TEMAB Tierp/Karlholmsbruk/Örbyhus.
2. Bevara samtliga prisvärden, källor, leverantörsvärdeskrav,
   snapshot-semantik och kvarvarande månadsbegränsningar. Ändra bara den
   katalog-/requestlivscykel och produktionsflagga som den etablerade
   aktiveringsprocessen kräver.
3. Regenerera den skarpa filen från katalogen och uppdatera proveniens/SHA
   mekaniskt. Förväntat utfall är exakt **45/19/28** och **47** skarpa
   produkter.
4. Lägg permanent omockad UI-/produkt-/E2E-täckning som bevisar att de åtta
   verkliga posterna kan väljas och att giltig MWh + leverantörsvärden ger ett
   synligt uppskattat årsresultat; kronor/schablon och saknade/ogiltiga fält ska
   fortsatt blockeras.
5. Kör full Python, full TypeScript, tsc, normalt bygge, E2E, generator-/SHA-/
   exakt-ID-/räknings- och diffkontroll från rent reproducerbart läge.
6. Commitera lokalt och stanna för Codex granskning av aktiveringsdiffen.
   **Ingen push.**
