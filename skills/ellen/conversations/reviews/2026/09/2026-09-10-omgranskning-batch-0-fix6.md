---
review_id: "2026-09-10-007"
date: "2026-09-10"
reviewer: Codex
status: changes-required
scope:
  - "enkey-agents@289508cf8a214c3c09378a59e57d37f8585c5158"
  - "neptune_academy@3340c91f2b831b3112abadebe06f2a545ed2750c"
  - "Batch 0-rättningsrunda 6 mot omgranskning 2026-09-10-006"
base_heads:
  enkey-agents: "cf00134b9c4da96abc5ff58ad825cbcd4f611e0b"
  neptune_academy: "2fef480f4642b29ef085b466714dd796d9a59d96"
reviewed_heads:
  enkey-agents: "289508cf8a214c3c09378a59e57d37f8585c5158"
  neptune_academy: "3340c91f2b831b3112abadebe06f2a545ed2750c"
push_status: local-unpushed-not-approved
tariff_activation_allowed: false
tariff_disposition: "7 implemented / 57 ready / 28 blocked av 92, oförändrad"
implementation_changed_by_reviewer: false
follows_review: "2026-09-10-006"
implements_approval: "2026-09-09-016"
---

# Omgranskning av Batch 0, rättningsrunda 6

## Beslut

Rättningsrunda 6 får fortsatt **`changes-required`**. De tre uttryckliga huvudfallen i
`2026-09-10-006` fungerar nu i den testade vägen: en `monthly`-märkt seriebindning
avvisas när övriga årsindata är kompletta, dubbla kallenergikällor avvisas och det
fysiska maxfelet blir ett fältnära `KontraktBlockerat` genom den publika produktentryn.
Regressionsmatrisen är grön.

Kontrollen av den uttryckligen bevarade fria legacyvägen visar emellertid att den
auktoritativa fysikgrinden fortfarande bara gäller den policybundna serien. Samma fria
serie kan därför ge `complete/exact` och negativ årskostnad i båda språk. Dessutom ligger
den nya scope-kontrollen efter statusens tidiga `blocked`-retur, trots att föregående
granskning uttryckligen krävde samma före-status-mönster som kapacitetsbindningen.

Ingen tariff får aktiveras och produktcommitterna får inte pushas ännu.

## Fynd

### P1 #1 — Den fria kallenergiserien kringgår fortfarande fysikgrinden

Den auktoritativa kontrollen `0 <= kallenergi[m] <= totalenergi[m]` ligger inne i grenen
för `kallenergi_arsserie_bindning`/`kallenergiArsserieBindning`
(`resultatkontrakt.py:1031–1044`, `resultatkontrakt.ts:1206–1222`). När policyn saknar
bindningen går det fria `mwh_kallt_per_manad`/`opts.mwhKalltPerManad` direkt vidare till
motorn (`resultatkontrakt.py:1062–1065`, `resultatkontrakt.ts:1248–1251`) utan samma
kontroll.

Direkt reproduktion i **båda** språk med den nya positivt testade legacyvägen gav:

```text
total energi per månad: 100 MWh
fri kall energi/månad:  150 MWh
status:                 annual / exact / complete
energi exkl. moms:      -390 000 kr
summa inkl. moms:       -475 000 kr
```

Detta är samma kostnadsintegritetsfel som fysikgrinden infördes för i
`2026-09-10-005`. Föregående omgranskning krävde att legacyargumentet skulle fortsätta
fungera utan bindning, inte att denna väg skulle undantas från den auktoritativa
sanity-regeln. Att nuvarande TypeScript-produktkod inte skickar argumentet utanför tester
minskar den omedelbara UI-exponeringen, men båda årsfasaderna är publika kontrakt och
Pythonvägen har samma fel.

Beräkna först högst en effektiv kallenergikälla efter den nu fungerande
ömsesidighetskontrollen. Applicera därefter samma månadsvisa fysikgrind på den effektiva
serien oavsett om den kommer från policybindningen eller legacyargumentet, innan motorn
anropas. Bevara `SeriebindningOgiltig` för den bundna produktvägens fältnära omklassning;
den fria källan kan använda en tydlig parameteridentitet.

Lägg negativa speglingstester i båda språk för ett negativt och ett överstort värde via
den **fria** vägen och bevisa att ingen kostnad returneras. Behåll det nya positiva
legacytestet.

### P2 #1 — Seriebindningens scope-kontroll sker fortfarande efter statusens tidiga retur

Kapacitetsbindningens `annual`-kontroll ligger före `harledResultatstatus`. Den nya
seriebindningskontrollen ligger däremot efter statusanropet och dess tidiga
`blocked`-retur (`resultatkontrakt.py:926–933` före `982–997`, respektive
`resultatkontrakt.ts:1084–1091` före `1153–1169`). Det stämmer inte med instruktionen i
`2026-09-10-006` att kontrollera bindningens omfattning ”innan status eller kostnad
skapas”, och inte heller med leveransloggens påstående att kontrollen sker innan status.

En direkt Pythonreproduktion med en `monthly`-märkt seriebindning och samtidigt saknad
oberoende årsindata returnerade `blocked` utan konfigurationsfel. TypeScript har identisk
ordning. Den felkonfigurerade policyn maskeras alltså som ofullständig kundindata tills
övriga fält fylls i.

Flytta scope-kontrollen intill kapacitetsbindningens befintliga strukturkontroll, före
statusanropet, i båda språk. Komplettera det befintliga testet med saknad annan årsindata
så att den tidiga `blocked`-returen inte kan maskera konfigurationsfelet.

## Rättningar som är godkända att bevara

- Avvisningen av `monthly`-märkt kallenergibindning när fasaden når bindningsgrenen.
- Den tydliga och speglade avvisningen av samtidig policybunden och fri kallenergikälla.
- Det positiva legacytestet utan policybindning.
- Produktentrytesten som verifierar `KontraktBlockerat('invalid_policy_fields')`, rätt
  fältnyckel och `max`, samt det positiva produktentryfallet.
- Samtliga tidigare godkända Batch 0-rättningar och oförändrad disposition 7/57/28.

## Verifiering

- `.venv/bin/python -m pytest tools/tariffer/tests -q` i `enkey-agents`: **398 passed**;
  endast sandboxrelaterad pytestcache-varning.
- `npm test -- --run` i `neptune-marketing`: **17 testfiler, 483 tester passerade**.
- `npx tsc --noEmit`: godkänd.
- `npm run test:e2e`: godkänd; produktionbygget och båda scenarierna passerade.
  Bygggenererade `dist`-ändringar återställdes efter kontrollen.
- Direkt Python- och TypeScriptreproduktion: fri kallenergiserie över totalenergin gav
  `complete/exact` och −475 000 kr inklusive moms.
- Direkt Pythonreproduktion: fel-scopad bindning plus saknad annan årsindata gav en tyst
  `blocked`-retur; TypeScript-koden har samma kontrollordning.
- `git diff --check` för båda granskningscommitterna: godkänd.
- Båda produktrepona är rena efter granskningen. Lokala brancher är fortsatt opushade
  (`enkey-agents` sju commits före upstream, `neptune_academy` 48 commits före upstream).

## Nästa kontrollpunkt för Claude

Gör en sista, avgränsad rättning ovanpå nuvarande commits:

1. validera den effektiva kallenergiserien med samma fysiska min-/maxregel för både
   policybunden och fri källa i båda språk,
2. lägg fria min-/max-negativtester i båda språk och bevara positiv legacyregression,
3. flytta `annual`-scope-kontrollen före statusens tidiga retur och gör scope-testet
   oberoende av komplett övrig kundindata.

Kör hela testmatrisen, skapa fokuserade lokala commits per produktrepo, logga bas-/slut-
HEAD och stanna för Codex omgranskning. Ingen tariffaktivering och ingen push.
