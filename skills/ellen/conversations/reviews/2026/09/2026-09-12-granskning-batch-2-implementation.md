---
review_id: "2026-09-12-019"
date: "2026-09-12"
reviewer: Codex
status: changes-required-before-activation
scope: "Batch 2 lokal implementation — Sundsvall Energi Indal, Liden och Lucksta"
reviewed_heads:
  skills: "fa68890e8d5b5eb013759c3289f74d6d516496a5"
  skills_catalog_commit: "08a8d6a795b0f6353b461ffda3056e1117f3819e"
  enkey_agents: "a30c876daea310f3cdab8f13a41e67fc00e0cd70"
  neptune_academy: "ab57d02b462b76c3c8bbc9abe4d68c72cbbcd41c"
activation_allowed: false
push_allowed: false
next_phase: "avgränsad rättningsrunda 1"
---

# Granskning av lokal Batch 2-implementation

## Bedömning

Batch 2:s tariffmodell, minimala policy, kalkylatorflöde och goldenfacit är i sak
korrekta. Leveransen får ligga kvar, men är **inte godkänd för aktivering eller push**
ännu. Den nya tariffscopade requestgrinden uppfyller inte handoffens fail-closed-krav
för alla referenstyper. Nästa fas är därför en kort, avgränsad rättningsrunda och inte
aktivering eller Batch 3.

## Verifierat av Codex

- Exakt tre lokala produktcommits ligger ovanpå de pushade Batch 1-baserna. Ingen är
  pushad och Sundsvall Indal/Liden/Lucksta ligger fortsatt bakom
  `investigation.status="utreds"`.
- Katalogen har `capacity.type="not_applicable"`, `contract_required:true`, 1 008
  SEK/MWh exklusive moms samtliga månader och ingen fast-, kapacitets- eller
  justeringsavgift.
- R14 pekar i den verkliga katalogen på exakt Sundsvall normal och
  Matfors/Kvissleby; Indal/Liden/Lucksta ingår inte.
- Oberoende körning genom Pythonkontraktsfasaden gav status
  `annual/exact/complete`, 100 800 kr exklusive moms och 126 000 kr inklusive moms
  för 100 MWh.
- `enkey-agents`: `718 passed, 4 skipped` i `tools/tariffer/tests`.
- `neptune-marketing`: `942 passed` och `npx tsc --noEmit` godkänd.
- Dispositionen är fortsatt 15/49/28 och den skarpa Sundsvallsposten finns ännu inte
  i den genererade produktkatalogen.

Den repoövergripande Pythoninsamlingen omfattar även separata Milesight-testbanker
med saknade externa beroenden och är inte Batch 2:s acceptanssvit. Den avgränsade,
tidigare använda tariffsviten ovan är grön.

## Fynd

### P1 — tariff- och requestreferenser är inte fullt fail-closed

`blockerade_tariff_ider()` i `tools/tariffer/katalog.py` bygger en mängd av
katalogens tariff-ID:n men kontrollerar inte ett explicit `tariff_ids`-värde mot
den mängden. Raderna som hanterar `tariff_ids` gör i praktiken bara:

```python
blockerade.update(tariff_ids)
```

Codex reproducerade därför att en katalog med tariffen `ratt-id` och requestvärdet
`felstavat-id` returnerar `{'felstavat-id'}` utan fel. Den verkliga tariffen blir då
inte blockerad. Ett dubblerat tariff-ID tyst dedupliceras på samma sätt.

Funktionen validerar inte heller tariffposternas
`investigation.request_ids`. En syntetisk tariff med referensen `FINNS_INTE`
passerar referensupplösningen utan fel. Detta lämnar den del av den auktoritativa
handoffen som säger att okända/dubblerade request- eller tariff-ID:n inte får tyst
öppna en tariff oimplementerad.

Rätta generiskt i samma Pythonfunktion eller i en tydligt namngiven, gemensam
validerare som alltid anropas av `godkanda()`:

1. Kräv unika, icke-tomma request-ID:n.
2. Kräv exakt en tydlig scopeform per öppen request: explicit `tariff_ids` eller
   bakåtkompatibelt `member_ids`.
3. För `tariff_ids`: kräv en icke-tom lista med unika, icke-tomma strängar och att
   varje ID finns exakt en gång i katalogens tariffer. Okända eller dubblerade ID:n
   ska kasta.
4. För `member_ids`: behåll dagens expansion men validera även tomma/dubblerade
   referenser fail-closed.
5. För varje `investigation.request_ids`: kräv unika referenser, att requesten finns
   och att den upplösta requestscopen faktiskt omfattar tariffen som bär referensen.
6. Lägg permanenta negativa test för okänt och dubblerat `tariff_ids`, okänt och
   dubblerat `investigation.request_ids`, dubbla scopeformer samt saknad/tom scope.

Den verkliga katalogen har inga sådana fel i dag; detta är ett skydd mot att ett
framtida stavfel tyst tar bort en spärr.

### P2 — ett Pythonprov bevisar inte vad namnet och kommentaren påstår

`test_ingen_kapacitetsindata_behovs_eller_paverkar_kostnaden` beräknar bara
`res_utan` och kontrollerar `complete`. Det skapar aldrig motsvarande anrop med ett
irrelevant kapacitetsfält och jämför därför inte kostnaderna. TypeScriptprovet gör
redan den jämförelsen.

Lägg ett verkligt `res_med`-fall i Python och jämför kostnad samt relevanta
statusfält. Stärk samtidigt goldenproven i båda språk så att den utlovade
statuspariteten uttryckligen omfattar `annual`, `exact` och `complete`, inte endast
`fullstandighet`.

### P2 — leveransens `git diff --check`-uppgift är fel

`git diff --check ca99492..fa68890` rapporterar en extra tomrad vid EOF i
Batch 2-handoffen, medan sessionsloggen säger att kontrollen var ren. Ta bort
whitespacefelet och redovisa det faktiska kommandot/resultatet i rättningsleveransen.

## Nästa kontrollpunkt

Claude får göra endast rättningarna ovan ovanpå befintliga lokala commits, köra den
riktade nya referensmatrisen samt full tariff-Python, full TypeScript och tsc, och
sedan commitera fokuserat. Uppdatera sessionsloggen med nya hashvärden och stanna för
Codex omgranskning.

Ändra ingen tariffmodell, aktiveringsstatus, prisdata eller disposition. Regenerera
inte produktkatalogen om katalogbytes inte ändras. Ingen push. Batch 3 startar först
efter separat godkänd Batch 2-aktivering och remote-verifiering.
