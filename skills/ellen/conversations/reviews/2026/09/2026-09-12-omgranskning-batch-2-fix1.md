---
review_id: "2026-09-12-020"
date: "2026-09-12"
reviewer: Codex
status: changes-required-before-activation
scope: "Batch 2 rättningsrunda 1 efter granskning 019"
reviewed_heads:
  skills: "2a7fd35752bd002ec7597c41ccd7ce6ac9ccb993"
  skills_catalog_commit: "08a8d6a795b0f6353b461ffda3056e1117f3819e"
  enkey_agents: "d81831a992b4bb4d86e6a121e0914f7fdfe483d0"
  neptune_academy: "fbc925f27c87764943cd534aa778d22c206fbe67"
activation_allowed: false
push_allowed: false
next_phase: "avgränsad Pythonrättning 2"
---

# Omgranskning av Batch 2 — rättningsrunda 1

## Bedömning

Rättningsrunda 1 stänger granskning 019:s konkreta reproduktioner: okända och
dubblerade scope-ID:n, felaktiga `investigation.request_ids`, dubbla/tomma scopeformer,
det verkningslösa kapacitetsprovet, statuspariteten och whitespacefelet är rättade.
Tariffmodellen och TypeScriptändringarna är fortsatt godkända.

En liten del av exakt-samma P1-kontrakt återstår i Pythonvalideraren. Därför är Batch 2
ännu inte godkänd för aktivering eller push.

## Verifierat av Codex

- `enkey-agents`: `726 passed, 4 skipped` i `tools/tariffer/tests`.
- `neptune-marketing`: `942 passed` och `npx tsc --noEmit` godkänd.
- Samtliga nya negativa fall i rättningsrunda 1 kastar som avsett.
- Katalogbytes, priser, aktiveringsstatus och genererad produktkatalog är oförändrade.
- Dispositionen är fortsatt 15/49/28.
- De tre commitdiffarna är fokuserade och diffkontrollerna är rena.

## Kvarvarande fynd

### P1 — “finns exakt en gång” och “sträng” valideras inte

Granskning 019 krävde att ett explicit tariff-ID ska vara en icke-tom sträng och finnas
**exakt en gång** i katalogens tariffer. `blockerade_tariff_ider()` bygger i stället
`alla_tariff_id` som en `set`. Eventuella dubbla katalograder kollapsar innan kontrollen,
så följande syntetiska katalog godtas:

```text
tariffs: två rader med id="dublett"
request: tariff_ids=["dublett"]
resultat: {"dublett"}, inget fel
```

Codex reproducerade även att numeriska katalog-, medlems-, request- och tariff-ID:n
accepteras när de matchar varandra; resultatet blev `{7}`. Det uppfyller inte
rättningskravets uttryckliga “icke-tomma strängar” och kan skapa andra beteenden än JSON-
kontraktets namngivna ID:n.

Rätta endast den gemensamma strukturvalideringen:

1. Validera först varje katalogtariffs `id` som en icke-tom sträng och kasta vid
   dubblett innan mängder/index byggs. Validera `member_id` som en icke-tom sträng.
2. Validera varje request-`id` som en icke-tom sträng.
3. Kräv att `tariff_ids`/`member_ids`, när de används, är riktiga listor och att varje
   element är en icke-tom sträng innan dubblett- och existenskontrollen.
4. Kräv på samma sätt att ett närvarande `investigation.request_ids` är en lista av
   icke-tomma strängar; behandla inte en sträng eller annat sanningsvärdigt objekt som en
   itererbar lista av referenser.
5. Lägg permanenta negativa prov för åtminstone dubblerat katalogtariff-ID,
   icke-sträng-ID och en skalär scope-/request-referens. Behåll den verkliga katalogen
   grön.

Detta är ingen ny funktion eller arkitektur; det slutför endast den strukturkontroll som
redan beställdes i granskning 019.

## Nästa kontrollpunkt

Claude får ändra enbart `tools/tariffer/katalog.py`, dess Batch 2-test och
kommunikationsloggen. Kör den riktade negativa matrisen, hela `tools/tariffer/tests` och
`git diff --check`, commitera fokuserat lokalt och stanna för Codex omgranskning.

Ingen TypeScriptändring eller ny TypeScriptcommit behövs. Ändra ingen katalogdata,
tariffmodell, aktiveringsstatus, disposition eller genererad produktkatalog. Ingen push.
