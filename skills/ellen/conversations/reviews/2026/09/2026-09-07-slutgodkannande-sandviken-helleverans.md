---
review_id: "2026-09-07-003"
date: "2026-09-07"
reviewer: Codex
status: approved-with-follow-up
scope:
  - "Sandviken Energi Helleverans, annual_forward och MWh-only"
  - "Sluträttning efter omgranskning 2026-09-07-002"
reviewed_heads:
  skills: "7ba9ec1b6245a72a4720f11b11beec6692af6196"
  enkey-agents: "a5efb7a049e1f522f89cc073db76c7556f62f08b"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: approved-for-push
---

# Slutgodkännande av Sandviken Energi Helleverans

## Bedömning

**Den avgränsade tre-repokontrollpunkten är godkänd för push.** Den sista
Neptune-committen `f1df177` stänger båda kvarvarande P1-fynden i granskning
`2026-09-07-002`. Den publika Sandviken-vägen kräver nu explicit, maskinläsbar
MWh-proveniens och kontraktsresolvern är fail-closed även när egenskapen
`_kraver_kontrakt` finns men har värdet `undefined`.

Inga blockerande kodfynd återstår inom den godkända omfattningen. Godkännandet gäller
lokal `annual_forward` för Helleverans med direkt angiven positiv MWh och angiven
debiterbar heltalseffekt från 3 kW. Det gäller inte kronor-till-MWh-invers, schablon,
Delleverans, fler tariffaktiveringar eller `enforced`.

## Bekräftade egenskaper

- `BesparingsvardeArgs.energyProvenance` har det typade giltiga värdet
  `confirmed_mwh`; Sandvikens kontraktsgren blockerar när värdet saknas eller avviker.
- `calcResult` skapar proveniensen först efter att inmatningsläget är exakt `mwh` och
  energitalet är ändligt och större än noll. Proveniensen följer med i huvud-, min- och
  maxberäkningen.
- Legacytariffernas direkta anropskontrakt är fortsatt bakåtkompatibelt och kräver inte
  det nya fältet.
- Endast äkta frånvaro av `_kraver_kontrakt` väljer legacyvägen. En närvarande markör
  med `undefined`, `false`, `null`, sträng eller tal avvisas.
- Tidigare verifierade spärrar för fel energiläge, ogiltig energinumerik, saknad eller
  ogiltig kapacitet, policy-ID och `annual_forward` gäller fortsatt.

## Utförda kontroller

- `neptune_academy@f1df177`: 409/409 Vitest passerar.
- `npx tsc --noEmit`: passerar utan fel.
- `npm run eval:build`: passerar; endast den kända varningen om stor bundle.
- `git diff --check` är rent för hela Sandviken-kedjan i alla tre repon.
- Implementationsrepona `enkey-agents` och `neptune_academy` är rena.
- Egna runtime-direktanrop mot den verkliga modulen gav:
  - positiv Sandviken-energi utan proveniens: `missing_energy`;
  - proveniens `derived_kr`: `missing_energy`;
  - proveniens `confirmed_mwh`: beräkning genomförd;
  - legacytariff utan proveniens: beräkning genomförd;
  - närvarande `_kraver_kontrakt: undefined`: konfigurationsfel, ingen fallback.
- Pythonkoden ändrades inte i sista rundan. Den oförändrade granskade HEAD-versionen
  `enkey-agents@a5efb7a` passerade 362/362 tariff-tester i föregående omgranskning.

## Icke-blockerande uppföljningar

### P3 — bevara runtime-fallet med fel proveniens som test

Beställningen i `2026-09-07-002` bad om ett regressionstest både utan och med fel
proveniens. Committen innehåller testet utan proveniens och testet med giltig proveniens,
men inte ett explicit runtime-test för exempelvis `derived_kr`. Typkontraktet tillåter
bara `confirmed_mwh`, implementationen jämför strikt och Codex runtime-test bekräftar att
fel värde blockeras. Därför blockerar testluckan inte denna push, men den bör läggas till
vid nästa beröring av filen, med en avsiktlig typbypass som simulerar en JavaScript- eller
API-anropare.

### P2 — anpassa kalkylatorns språk till beslutad verifieringsnivå före v1-release

Robert har efter committen fastställt följande produktprincip:

- fakturakontroll görs för egna kunder eller när någon uttryckligen ber om den;
- övriga leverantörsberäkningar verifieras på årsbasis mot leverantörens publicerade
  exempel, prislista eller motsvarande officiella underlag;
- allt annat som visas är en uppskattning.

Det gör inte Sandvikens beräkningskod fel, men befintliga UI-formuleringar som lovar att
en angiven effekt gör kostnaden "exakt" är för starka. Produkttext och resultatmetadata
bör före kalkylatorns v1-release skilja mellan **tariffverifierad beräknad årskostnad**,
**uppskattning** och **fakturaverifierat utfall**. En deterministisk beräkning mot en
publicerad prislista är inte automatiskt avstämd mot kundens verkliga faktura.

## Godkännandets gräns och pushordning

Godkännandet omfattar följande lokala commitkedjor:

- `skills`: `c601ebb`, `7ba9ec1`;
- `enkey-agents`: `fcb2fd8`, `a5efb7a`;
- `neptune_academy`: `de17a7f`, `a0e5a97`, `f1df177`.

Robert kan be Claude pusha exakt dessa granskade HEAD-versioner till respektive
`origin/main`. Rekommenderad ordning är `skills` → `enkey-agents` → `neptune_academy`,
eftersom den genererade webbfilens proveniens pekar på den godkända katalogversionen.
Efter push ska remote-heads verifieras mot fullhasharna i frontmatter ovan. Codex utförde
ingen push och ändrade ingen implementation eller tariffdata.
