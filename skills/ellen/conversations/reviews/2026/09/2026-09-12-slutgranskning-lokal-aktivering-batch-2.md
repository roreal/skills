---
review_id: "2026-09-12-022"
date: "2026-09-12"
reviewer: Codex
status: approved-for-push
scope: "Lokal aktivering av Batch 2 — Sundsvall Energi Indal/Liden/Lucksta"
reviewed_heads:
  skills: "71b5d1b0d5ddb49bfd0afea8e993bdc36d36b591"
  skills_catalog_commit: "a133719e58da2713d670addc1be3f1dedeac05ab"
  enkey_agents: "5da3b74cc7b4a22c4ce268b5d3670465bd68e4cc"
  neptune_academy: "297e4f04093dc68084dfa0f026ad9590155ba2b7"
activation_allowed: false
push_allowed: true
tariff_disposition: "16 implemented / 48 ready / 28 blocked av 92"
---

# Slutgranskning av Batch 2-aktiveringen

## Bedömning

**Godkänd för normal fast-forward-push.** Inga blockerande eller övriga
kodgranskningsfynd återstår i den lokala aktiveringen.

Godkännandet gäller exakt katalogtariffen
`sundsvall-energi-indal-liden-och-lucksta-2026` och kalkylatorns uppskattade
årskostnad med bekräftad MWh. Det utökar inte godkännandet till fakturagaranti,
månadsredovisning, kronor, schablon eller besparingsprodukten.

## Verifierat av Codex

- Katalogcommitten tar endast bort målpostens `investigation`-spärr, höjer
  revisionen `0.1.9` → `0.1.10` och lägger en avgränsad ändringslogg. Pris,
  `capacity.type="not_applicable"`, `contract_required:true`, källor och övriga
  beräkningsfält är oförändrade.
- R14 omfattar fortsatt exakt Sundsvall normal och Matfors/Kvissleby normal.
  Båda ger fortsatt grindorsaken `utreds`; ingen av dem har aktiverats.
- Mekanisk omräkning ger 16 godkända katalogtariffer från 14 medlemmar och
  dispositionen **16/48/28 av 92**. Målposten är den enda nya godkända tariffen.
- Katalogfilens SHA-256 är
  `df10dd3db1e85991a362b636c58dc0e1eb949f6bbd70356bee919973fd836fa2`.
  En oberoende regenerering från `skills@a133719` blev byte-för-byte identisk med
  den incheckade `tariffer.generated.ts`; proveniensen anger 16 godkända och 62
  filtrerade katalogtariffer.
- Den verkliga genererade posten har produkt-ID
  `sundsvall-energi-indal-liden-och-lucksta`, tolv priser om 1 008 SEK/MWh
  exklusive moms, tom kapacitetsdel, ingen fast avgift och endast
  `annual_forward`.
- Den publika produktvägen ger för 100 MWh status `annual/exact/complete`,
  **126 000 kr inklusive moms** och ingen `kapacitetKw`. Komponentfacit visar noll
  i fast-, kapacitets-, justerings- och returdel. Kronor och schablon blockeras med
  `unsupported_input_mode`; besparing blockeras med `besparing_ej_stodd`.
- Den omockade komponenttesten och den byggda sidans E2E använder normal
  formulärsubmit. Sundsvall är valbar, inga kapacitets- eller policyfält visas och
  resultatet är 126 000 kr.
- `git diff --check` är rent för alla tre aktiveringscommits. De redan befintliga,
  orelaterade ändringarna i `neptune-marketing/dist` är inte del av committen.

## Oberoende verifieringskörning

- Riktad Batch 2-svit: **29 passed**.
- Full tariffsvit: **729 passed, 4 skipped**. Pytests enda varning gäller att
  sandlådan inte får skriva sin cache; den påverkar inte testresultatet.
- Full TypeScript-svit: **952 passed** i 33 filer.
- `npx tsc --noEmit`: godkänd.
- `npm run eval:build`: godkänd; endast den redan kända
  bundelstorleksvarningen.
- E2E mot det isolerade bygget: **10/10 scenarier godkända**.

Pythonantalet 730 → 729 är korrekt och inte en regression: aktiveringen ersätter
de två separata preaktiveringsproven "genereras ännu inte" och "genereras från
isolerad kopia" med ett enda prov mot den verkliga aktiverade katalogen.

## Nästa steg för Claude

1. Commitera Codex kommunikationsändringar separat i `skills`.
2. Pusha `skills`, `enkey-agents` och `neptune_academy` normalt utan force.
3. Verifiera alla tre `origin/main` med `git ls-remote` mot exakt de pushade
   lokala HEAD:arna.
4. Logga de verifierade fulla hashvärdena i sessionsfilen, commitera och pusha den
   sista verifieringsloggen i `skills`, och verifiera därefter även den nya
   `skills`-remote-HEAD:en.

Batch 3 får starta först när dessa fyra steg är genomförda och loggade.
