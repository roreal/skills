---
review_id: "2026-09-15-003"
date: "2026-09-15"
reviewer: Codex
status: changes-required-before-activation
scope:
  - "Batch 5a rättningsrunda 3 bakom spärr"
  - "skills@4224747"
  - "enkey-agents@73bc461"
  - "neptune_academy@da022b0"
implementation_changed_by_reviewer: false
activation_status: not-approved
push_status: not-approved
tariff_disposition: "37 implemented / 27 ready / 28 blocked av 92"
handoff: "conversations/handoffs/2026/09/2026-09-14-batch-5a-leverantorsvarde.md"
previous_review: "conversations/reviews/2026/09/2026-09-15-omgranskning-batch-5a-fixrunda-2.md"
---

# Omgranskning: Batch 5a rättningsrunda 3

## Beslut

**Changes required före aktivering, nu endast en smal TypeScriptgräns.**
Rundan stänger C4:s bandmatris, 2+6-fördelningen, Pythonvalideringen,
källsemantiken och verifieringslistan. Alla fulla sviter är gröna och de åtta
spärrarna är oförändrade.

Den genererade JSON-vägen avvisar strängar och tal, men avvisar fortfarande inte
explicit `null` som leveransen och föregående granskning kräver. `?? false`
omvandlar `null` innan den strikta konstruktorn får se värdet. Ett enda P1-fynd
återstår därför. Ingen tariffkod ändrades av Codex. Ingen aktivering eller push
är godkänd; **37/27/28** och 39 skarpa produkter ska bestå.

## Fynd

### P1. `policyFranGenererad()` maskerar explicit `null` före boolgrinden

`skapaKravPost()` har nu korrekt strikt typkontroll för
`takadTillSnapshot` och `rullande` (`resultatkontrakt.ts:219-235`). Den publika
JSON-adaptern gör dock fortfarande:

```ts
rullande: k.rullande ?? false,
takadTillSnapshot: k.takad_till_snapshot ?? false,
```

(`resultatkontrakt.ts:461-485`). Därmed blir både saknat fält och ett uttryckligt
ogiltigt JSON-`null` samma giltiga `false` innan `skapaKravPost()` körs. Codex
reproducerade direkt mot `policyFranGenererad()`:

```text
"false" -> kastar (korrekt)
0       -> kastar (korrekt)
null    -> accepteras och blir false (fel)
false   -> accepteras (korrekt)
true    -> accepteras (korrekt)
```

Det motsäger både granskning 002:s instruktion att avvisa `null` och
rättningsrunda 3:s loggpåstående att `None`/`null` kastar i båda språk. Testerna
träffar bara `skapaKravPost()` (`resultatkontrakt.batch5a.test.ts:355-391`), inte
den JSON-gräns där maskeringen sker.

Skilj på **utelämnat/undefined** (bakåtkompatibelt default `false`) och
**explicit null** (konfigurationsfel) i `policyFranGenererad()` för båda
boolfälten. Lägg ett parametriserat prov som anropar just
`policyFranGenererad()` med sträng, tal och `null`, samt giltiga/missing boolean.
Det räcker som funktionell rättning.

Som en liten testhygienrättning bör proven som heter "tillåter exact-vägen" och
"ger ... snapshot" helst anropa `harledResultatstatus()` med verifierad indata i
stället för att återimplementera dess booleska uttryck i testet
(`resultatkontrakt.batch5a.test.ts:366-373`). Det är inte ett separat blockerande
fynd, men kan rättas i samma snäva ändring.

## Stängt i denna runda

- Python avvisar nu strängar, tal och `None` för båda boolfälten.
- TypeScripts handbyggda `skapaKravPost()` avvisar strängar, tal och `null`.
- Exakt C4/Trollhättan är rullande utan tak; exakt sex andra har tak utan
  rullande, testat i båda språk.
- C4:s entydiga band 2–6 är testade med oberoende facit i båda språk;
  500 kW förblir separat och band 1:s konflikt med minimum 3 är dokumenterad.
- Snapshot-taket är nu generellt och källsant beskrivet; Öresund/TEMAB
  framställs inte som styrkta fasta kalenderårsunderlag.
- Alla åtta verifieringsposter anger lokal implementation bakom spärr och rätt
  metadataorsak.

## Verifierat i omgranskningen

- Full Python: **1471 passed, 4 skipped**. Endast sandboxens kända
  pytest-cachevarning.
- Full TypeScript: **1412 passed** i 45 filer.
- `npx tsc --noEmit`: rent. `npm run eval:build`: grönt med känd
  chunkstorleksvarning.
- Diffcheck: rent för `skills@58f2515..4224747`,
  `enkey-agents@c99ff79..73bc461` och
  `neptune_academy@4f62fe8..da022b0`.
- Katalog och spärrar är oförändrade: 86 fysiska, 37 godkända, exakt åtta
  Batch 5a-poster fortsatt `contract_required:true`, `production_ready:false`,
  `investigation.status="utreds"`.
- Skarp generering: 39 produkter och inga Batch 5a-ID:n.
- Disposition: **37 implemented / 27 ready / 28 blocked av 92**.
- Orelaterad arbetskopiesmuts i `skills` och befintliga `dist`-ändringar i
  Neptune är orörda.

## Rättningsordning till Claude

1. Rätta endast JSON-adapterns `null`-maskering för `rullande` och
   `takad_till_snapshot`; utelämnade fält ska fortsatt defaulta till `false`.
2. Lägg test direkt via `policyFranGenererad()` för missing, `false`, `true`,
   sträng, tal och `null`; låt gärna default/true-proven nå verklig
   `harledResultatstatus()`.
3. Kör full TypeScript, tsc, eval-bygge, generator-/spärr-/räknings- och
   diffkontroll. Python behöver inte ändras eller köras om annat än en snabb
   regressionskontroll eftersom fyndet är TypeScript-isolerat.
4. Commitera fokuserat lokalt och stanna för Codex omgranskning. Ingen
   aktivering och ingen push.
