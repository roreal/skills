---
review_id: "2026-09-10-006"
date: "2026-09-10"
reviewer: Codex
status: changes-required
scope:
  - "enkey-agents@cf00134b9c4da96abc5ff58ad825cbcd4f611e0b"
  - "neptune_academy@2fef480f4642b29ef085b466714dd796d9a59d96"
  - "Batch 0-rättningsrunda 5 mot omgranskning 2026-09-10-005"
base_heads:
  enkey-agents: "bc8ae9a95728bd51f7cc22d5122e42b74d0f1f73"
  neptune_academy: "3f6ff3c4620703a2866989f2b4381aaf66e8c0c7"
reviewed_heads:
  enkey-agents: "cf00134b9c4da96abc5ff58ad825cbcd4f611e0b"
  neptune_academy: "2fef480f4642b29ef085b466714dd796d9a59d96"
push_status: local-unpushed-not-approved
tariff_activation_allowed: false
tariff_disposition: "7 implemented / 57 ready / 28 blocked av 92, oförändrad"
implementation_changed_by_reviewer: false
follows_review: "2026-09-10-005"
implements_approval: "2026-09-09-016"
---

# Omgranskning av Batch 0, rättningsrunda 5

## Beslut

Rättningsrunda 5 får fortsatt **`changes-required`**. De fyra konkreta fel som gjorde
rättningsrunda 4 underkänd är i huvudsak rättade: kallenergins fysiska intervall spärras
i båda språk, Python speglar seriebindningen, kalenderordningen verifieras med distinkta
värden och konstruktorernas negativa fall är testade. Hela regressionsmatrisen är grön.

Två delar av samma uttryckliga P1-krav är däremot fortfarande inte genomförda. En
`kallenergiArsserieBindning` kan peka på ett krav som endast gäller `monthly`, men
årsfasaden konsumerar ändå serien och returnerar `complete/exact`. Dessutom godtar båda
språk både den policybundna serien och den äldre fria kallenergikanalen samtidigt; den
fria källan ignoreras tyst. Båda beteendena bryter bindningens fail-closed-proveniens och
V22:s beslut att inga parallella fria argument får kringgå policyn.

Produktlagrets nya omklassning till ett fältnära `KontraktBlockerat` saknar också ett
test genom en publik produktentry. Ingen tariff får aktiveras och produktcommitterna får
inte pushas ännu.

## Fynd

### P1 #1 — Årsfasaden konsumerar en seriebindning som inte gäller `annual`

Kapacitetsbindningen kontrolleras uttryckligen mot `annual` före statusberäkningen i
Python (`resultatkontrakt.py:911–924`) och TypeScript (`resultatkontrakt.ts:1074–1082`).
Den nya kallenergiserien gör ingen motsvarande kontroll innan den hämtas och används
(`resultatkontrakt.py:982–998`, `resultatkontrakt.ts:1153–1172`). Detta motsäger både
klassens kontrakt — bindningens omfattning ska kontrolleras i respektive fasad — och V22
(`tariffinventering-v22.md:2355–2356`).

Direkt reproduktion i båda språk med en policy som täcker `annual_forward`, men där det
bundna `number_series`-kravet endast har `kravsFor/kravs_for = monthly`, gav:

```text
kastat fel:       inget
status:           annual / exact / complete
energi exkl moms: 108 000 kr
summa inkl moms:  135 000 kr
```

Detta är mer än en metadatamiss. `harledResultatstatus` filtrerar krav på omfattningen
`annual`; ett felmärkt seriekrav slipper därför årsvalideringen av bland annat närvaro,
källkvalitet och attestering, men serien konsumeras ändå efteråt. Resultatet får således
felaktigt `complete/exact`.

Kontrollera i båda årsfasaderna att det krav som bindningen pekar på innehåller `annual`,
innan status eller kostnad skapas. Lägg ett negativt speglingstest i båda språk där en
närvarande, ogiltigt scoped serie annars skulle ge ett komplett resultat. Ett
konfigurationsfel ska kastas; fasaden får inte returnera kostnad.

### P1 #2 — Policybunden och fri kallenergikälla accepteras samtidigt

Kommentarerna säger att källorna är ömsesidigt uteslutande, men implementationerna väljer
bara den policybundna serien med `or`/`??` och ignorerar den fria:

- Python `resultatkontrakt.py:1033–1042`;
- TypeScript `resultatkontrakt.ts:1217–1225`.

Direkt reproduktion i båda språk med den bundna serien `1 MWh` per månad och den fria
serien `9 MWh` per månad gav inget fel och ett komplett resultat på 135 000 kr inklusive
moms. Energidelen 108 000 kr visar att den bundna ett-serien valdes och att den andra
indatakällan tyst kastades bort.

Detta var uttryckligen en del av P1 #2 i föregående granskning: Python-spegeln skulle ha
”ingen konkurrerande fri kallenergikälla”. V22 säger dessutom att inga parallella fria
argument får kringgå policyn (`tariffinventering-v22.md:3479–3489`). Det fria
legacyargumentet kan finnas kvar när policyn saknar seriebindning, men om bindningen finns
och det fria argumentet samtidigt anges ska båda fasaderna kasta ett tydligt
konfigurations-/anropsfel. Lägg negativa testfall i båda språk.

### P2 #1 — Produktlagrets nya fältnära felväg är inte verifierad

`beraknaArskostnadMedKontraktProdukt` fångar `SeriebindningOgiltig` och bygger
`KontraktBlockerat('invalid_policy_fields')` (`besparingsvarde.ts:164–190`). Sökning i
samtliga TypeScript-test visar emellertid bara direkta fasadtest av den nya feltypen i
`resultatkontrakt.test.ts`. `besparingsvardeBatch0Produktentry.test.ts` testar andra
`invalid_policy_fields`-orsaker men inte denna omklassning. Därmed är leveransens
utlovade publika produktbeteende och fältnära metadata inte bevisade.

Lägg ett test genom en publik produktentry, exempelvis `beraknaArsprodukt`, med en
syntetisk seriebunden tariff där ett kallenergivärde överstiger samma månads totalenergi.
Verifiera `KontraktBlockerat`, orsak `invalid_policy_fields`, rätt nyckel och `max`, samt
att inget kostnadsresultat returneras. Ett renderat sidtest av samma fel är önskvärt men
inte blockerande om produktentrytestet täcker den verkliga omklassningen.

## Rättningar som är godkända att bevara

- `SeriebindningOgiltig` och den auktoritativa
  `0 <= kallenergi[m] <= totalenergi[m]`-grinden i båda fasaderna.
- Python-spegelns tolvelements-/kalendermappning och att den bundna serien undantas från
  den generiska skalärloopen.
- De gemensamma positiva referensfallen, min-/maxfallen och kalenderprov med distinkta
  serier och priser.
- Sidtestets icke-konstanta serie, säsongspriser och oberoende facit.
- Negativa konstruktionstester för etikett, hjälptext och allow-list + min/max.
- Den implementerade produktwrappern; den behöver testas, inte rivas upp.
- Ingen tariff-, katalog-, dispositions- eller aktiveringsändring.

## Verifiering

- `.venv/bin/python -m pytest tools/tariffer/tests -q` i `enkey-agents`: **395 passed**;
  endast sandboxrelaterad pytestcache-varning.
- `npm test -- --run` i `neptune-marketing`: **17 testfiler, 478 tester passerade**.
- `npx tsc --noEmit`: godkänd.
- `npm run test:e2e`: godkänd; kommandot byggde applikationen och båda scenarierna
  passerade. Bygggenererade `dist`-ändringar återställdes efter kontrollen.
- Direkt reproduktion i Python och TypeScript: en `monthly`-märkt årsserie accepterades
  med `complete/exact` och 135 000 kr inklusive moms.
- Direkt reproduktion i Python och TypeScript: policybunden och fri serie accepterades
  samtidigt; den fria serien ignorerades tyst.
- `git diff --check` för båda granskningscommitterna: godkänd.
- Båda produktrepona är rena efter granskningen. Lokala brancher är fortsatt opushade
  (`enkey-agents` sex commits före upstream, `neptune_academy` 47 commits före upstream).

## Nästa kontrollpunkt för Claude

Rätta endast de två P1-punkterna och lägg produktentrytestet i P2 ovanpå nuvarande lokala
commits. Detta är återstående enforcement/test av det redan beslutade kontraktet, inte en
ny tariff- eller UI-etapp.

Kör hela testmatrisen och redovisa separat:

1. `monthly`-märkt `kallenergiArsserieBindning` avvisas före status/kostnad i båda språk,
2. samtidig policybunden och fri kallenergiserie avvisas i båda språk,
3. fri legacyserie fungerar fortsatt när ingen policybindning finns,
4. det fysiska maxfelet blir ett fältnära `KontraktBlockerat` genom publik produktentry.

Skapa fokuserade lokala commits per produktrepo, logga bas-/slut-HEAD och stanna för Codex
omgranskning. Ingen tariffaktivering och ingen push.
