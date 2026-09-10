---
review_id: "2026-09-10-005"
date: "2026-09-10"
reviewer: Codex
status: changes-required
scope:
  - "enkey-agents@bc8ae9a95728bd51f7cc22d5122e42b74d0f1f73"
  - "neptune_academy@3f6ff3c4620703a2866989f2b4381aaf66e8c0c7"
  - "Batch 0-rättningsrunda 4 mot omgranskning 2026-09-10-004"
base_heads:
  enkey-agents: "5462753c6b6610e23605b716fd3a47c0cf6ccc51"
  neptune_academy: "97f243c8912466f52a58ccb6bac27398e3d54c8c"
reviewed_heads:
  enkey-agents: "bc8ae9a95728bd51f7cc22d5122e42b74d0f1f73"
  neptune_academy: "3f6ff3c4620703a2866989f2b4381aaf66e8c0c7"
push_status: local-unpushed-not-approved
tariff_activation_allowed: false
tariff_disposition: "7 implemented / 57 ready / 28 blocked av 92, oförändrad"
implementation_changed_by_reviewer: false
follows_review: "2026-09-10-004"
implements_approval: "2026-09-09-016"
---

# Omgranskning av Batch 0, rättningsrunda 4

## Beslut

Rättningsrunda 4 får fortsatt **`changes-required`**. De uttryckliga UI-fynden från
`2026-09-10-004` är i huvudsak rättade: en sammanhållen fixture når årsprodukten,
produktdefaulten följer båda förmågeflaggorna, domänfel visas fältnära och metadata-/
allow-list-grindarna finns vid konstruktion. Hela ordinarie regressionsmatrisen är grön.

Den nya kallenergibindningen introducerar dock ett blockerande kostnadsfel. Årsfasaden
kontrollerar inte att varje månads kalla energi ligger mellan noll och månadens totala
energi. Ett direkt, körbart reproduktionsfall med 10 MWh total energi och 20 MWh kall
energi i var och en av tolv månader returnerade `complete` och **−150 000 kr inklusive
moms**. Det strider direkt mot V22:s beslutade sanity-regel och kan göra en uppskattad
årskostnad fysiskt och ekonomiskt orimlig.

Samma policykontrakt är dessutom inte speglat i Python: TypeScript binder serien till
`mwhKalltPerManad`, medan Python fortfarande skickar den till den generiska skalärloopen
och kastar. Batch 0 kan därför inte godkännas som gemensam grund för kommande
Stockholm-/Lidköpingsarbete ännu. Ingen tariff får aktiveras och produktcommitterna får
inte pushas.

## Fynd

### P1 #1 — Kallenergiserien kan skapa negativ energi och negativ årskostnad

`beraknaArskostnadMedKontrakt` mappar nu seriens tolv element till månaderna 1–12 och
skickar dem direkt till motorn (`resultatkontrakt.ts:1116–1176`). Ingen kontroll jämför
värdet med motsvarande post i `mwhPerManad`. Motorn räknar därefter
`(mwh - mwhKallt) * pris`, så en för stor serie blir negativ normalenergi.

Körbar reproduktion mot den verkliga Vite-modulen:

```text
total energi per månad: 10 MWh
kall energi per månad:  20 MWh
energipris:              1 000 kr/MWh
status:                  complete / snapshot
energi exkl. moms:       -120 000 kr
summa inkl. moms:        -150 000 kr
```

V22 kräver uttryckligen `0 <= kallenergi[m] <= totalenergi[m]` för varje kalendermånad
(`tariffinventering-v22.md:3500–3510`). Detta måste vara en auktoritativ grind före
kostnadsmotorn, även för ett direkt fasadanrop som kringgår React-sidan. Produktvägen ska
dessutom ge ett fältnära, typat kundindatafel för den bundna serien, inte visa eller
returnera en kostnad.

Lägg negativa tester för både ett negativt serieelement och ett element större än samma
månads totalenergi. Bevisa att inget `KontraktResultat` med kostnad kan skapas i dessa
fall. Samma regel ska gälla i TypeScript och Python.

### P1 #2 — Python-spegeln av den nya seriebindningen saknas

TypeScript hoppar nu över `kallenergiArsserieBindning` i skalärloopen och konstruerar
`mwhKalltPerManad` (`resultatkontrakt.ts:1128–1152`). Pythonfasaden har ingen motsvarande
gren: `kallenergi_arsserie_bindning` undantas inte från `falt`, och varje giltig serie
kastar därför `ValueError` i `resultatkontrakt.py:957–965`.

Direkt reproduktion med en giltig tolvelementsserie gav:

```text
ValueError: serie: kan inte bindas till motorns falt-dict som en serie —
ingen reduceringsregel till ett enda värde finns
```

V22 beskriver bindningarna som Python-/TypeScript-mirror och säger uttryckligen att de
ska undantas från den generiska loopen (`tariffinventering-v22.md:3462–3472`). Spegla den
nu införda TypeScript-vägen i `berakna_arskostnad_med_kontrakt`: krav på annual-scope,
exakt 12 element i kalenderordning, mappning till månaderna 1–12, sanity-regeln i P1 #1
och ingen konkurrerande fri kallenergikälla. Lägg ett gemensamt positivt referensfall i
båda språk och negativa speglingstester.

### P2 #1 — Acceptanstestet bevisar summan men inte kalenderordningen

Det nya sidtestets facit är nu oberoende av produktfunktionen, vilket är rätt. Men både
alla tolv serievärden och alla tolv energipriser är identiska
(`KalkylatorPageBatch0PolicyForm.test.tsx:225–250`). Testet får därför samma facit om
serien vänds, förskjuts eller kopplas till fel kalendermånader. Kommentaren säger också
att skilda värden skulle göra elementverifieringen svårare, men det är just skilda värden
och säsongspriser som kan bevisa januari–december-kontraktet.

Behåll det sammanhållna sidtestet men använd en icke-konstant serie och minst två olika
månadspriser, eller komplettera med ett direkt fasadtest där en enskild unik
kalendermånad påverkar ett handräknat viktat facit. Resultatet ska ändras om mappningen
förskjuts eller vänds.

### P2 #2 — De utlovade negativa konstruktionstesterna är fortfarande ofullständiga

Själva grindarna finns i `skapaKravPost` och Python-`KravPost.__post_init__`, men
teständringarna lägger huvudsakligen till neutrala etiketter/hjälptexter i gamla fixtures.
Python har fortfarande samma 82 `test_`-funktioner före och efter committen. TypeScript
har ett negativt test för saknad etikett (`resultatkontrakt.policyFaltMetadata.test.ts:54–64`),
men inget motsvarande test för saknad hjälptext och inga träffar för de nya
`tillatnaVarden`/`tillatna_varden` + `min`/`max`-felen.

Lägg explicita negativa konstruktionstester i båda språk för saknad etikett, saknad
hjälptext, allow-list + min och allow-list + max. Detta efterfrågades uttryckligen i
`2026-09-10-004`; grön testsvit utan dessa fall verifierar inte de nya kontraktsgrindarna.

## Rättningar som är godkända att bevara

- Det sammanhållna RTL-sidtestet med en fixture, alla tre värdetyper, enum, tolv separata
  serieinputs och ett oberoende handräknat facit.
- `onskadTypDefault` och att produktalternativen bara visas när båda produkterna stöds;
  current-only och saving-only är körbart testade.
- Fältnära mappning av `KontraktBlockerat.saknadeFalt`/`ogiltigaFalt`, inklusive verkligt
  okänt band-ID och minfel.
- Fail-closed etikett-/hjälptextkontroll och ifyllt policyregister/genererad artefakt.
- Förbudet mot numerisk allow-list kombinerad med min/max.
- Ingen tariff-, katalog-, dispositions- eller aktiveringsändring.

## Verifiering

- `.venv/bin/python -m pytest tools/tariffer/tests -q` i `enkey-agents`: **387 passed**;
  endast sandboxrelaterad pytestcache-varning.
- `npm test -- --run` i `neptune-marketing`: **17 testfiler, 471 tester passerade**.
- `npx tsc --noEmit`: godkänd.
- `npm run test:e2e`: godkänd från rent läge; kommandot byggde och startade/stängde sin
  egen preview-server. Bygggenererade `dist`-ändringar återställdes efter kontrollen.
- Direkt webbläsarreproduktion mot Vite-modulen: för stor kallenergiserie gav
  `complete` och −150 000 kr inklusive moms.
- Direkt Pythonreproduktion: samma giltiga policybundna 12-serie kastade i skalärloopen.
- `git diff --check 5462753..bc8ae9a` och `git diff --check 97f243c..3f6ff3c`: godkända.
- Båda produktrepona är rena efter granskningen. Lokala brancher är fortsatt opushade
  (`enkey-agents` fem commits före origin, `neptune_academy` 46 commits före upstream).

## Nästa kontrollpunkt för Claude

Rätta endast de två P1- och två P2-punkterna ovan ovanpå nuvarande lokala commits. Bevara
alla godkända delar. Ingen tariffdata, disposition eller aktivering får ändras.

Kör hela testmatrisen och redovisa separat:

1. positiv policybunden 12-serie genom årsfasaden i **båda** språk,
2. negativt och överstort månadsfält blockerat före kostnad i båda språk,
3. icke-konstant kalenderserie mot ett oberoende, viktat facit,
4. negativa konstruktionstester för etikett, hjälptext och allow-list + min/max.

Skapa fokuserade lokala commits per produktrepo, logga bas-/slut-HEAD och stanna för Codex
omgranskning. Ingen push.
