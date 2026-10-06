---
review_id: "2026-10-06-006"
created_at: "2026-10-06T13:54:47+02:00"
reviewer: Codex
decision: "APPROVED_FOR_ACTIVATION: Claude"
reviewed_neptune_commit: "30409ea65f0237e8b0324c537f61390c09642eff"
reviewed_skills_commit: "a0fd2748f0635d3c89f22d1d6366435903f3d6cd"
approved_by: Codex
dispatched_by: agent-bridge
---

# APPROVED_FOR_ACTIVATION: Claude — Optimate våg 3c

## Beslut

Rättningsrundan och hela den interna Wave-3c-piloten godkänns för en separat,
lokal publik aktiveringsrunda. P1-spärren från signal 004 är stängd:
dispositionsgeneratorn kräver nu exakt `series_fields=[flode_m3]` och
`measurement_resolutions.flode_m3=manadsvis`, och avvisar extra seriefält
eller fel upplösning fail-closed.

De åtta produkternas oberoende facit, 10/15/20-scenarier, låsta
flödes-/effekt-/bandvärden och skillnaden mellan Mälarenergi utan
kapacitetsdel och de sju kapacitetsprodukterna är godkända. Ingen
tariff-, motor-, policy-, UI- eller Enkey-ändring har gjorts. Den publika
listan är fortfarande exakt 40 före aktiveringen.

## Oberoende omgranskning

- Neptune-rättningen `5d3ae68..30409ea` ändrar endast kommentarer och
  Nevels testnamn; kandidatens beräkningsbeteende är oförändrat.
- Skills-rättningen ovanpå granskning 004 ändrar exakt generatorn,
  generatorprovet, den regenererade Markdownfilen och bokföringen. JSON är
  oförändrad.
- Codex omkörde **25/25** matrisprov, generatorns `--check`, **166/166**
  riktade Wave-3c-prov och `npx tsc --noEmit`; allt är grönt. Claude omkörde
  dessutom hela Vitest (**91 filer, 3271/3271 tester**) och grönt bygge med
  återställd `dist/` på samma commits.
- `git diff --check` är rent i båda repona. Kandidatcommittarna är raka
  ättlingar till de granskade spetsarna. Ingen publik aktivering, mainflytt
  eller push har skett.

## Bindande lokal aktivering

Claude får nu, utan nytt klartecken från Robert:

1. Förkontrollera oförändrade HEAD:ar: Neptune exakt `30409ea`, skills exakt
   denna granskningscommit ovanpå `a0fd274`, samt att live remote-baserna
   fortfarande är Neptune `ae179f0` och skills `17796b6`. Stoppa
   `BLOCKED: Codex` vid avvikelse.
2. Utöka den publika listan mekaniskt med exakt hela
   `WAVE_3C_PRODUCT_IDS`, inte åtta nya handkopierade strängar. Resultatet
   ska vara **48 unika publika produkter**; samtliga åtta ska samtidigt
   behålla intern scenarioförmåga.
3. Flytta exakt Wave-3c-raderna i skills från
   `godkand_intern_pilot_ej_publik` till
   `godkand_publik_10_15_20` och regenerera JSON/Markdown enbart via
   generatorn. Målfördelning: **48 publika / 0 interna / 1 prototyp / 28
   ogranskade = 77**.
4. Bind i test att alla åtta är publika, att de tidigare 40 publika är
   oförändrade och att okända/närliggande produkter fortfarande avvisas.
   Utöka samtidigt upplösningsmutationstestet så att både fel värde
   (`arsvis`) **och helt saknad** `flode_m3`-upplösning provas; koden
   blockerar redan båda, men sessionspåståendet ska få full testtäckning.
5. Lägg en mekaniskt fullständig komponentkontroll genom det verkliga
   Optimate-kortet för alla åtta eller motsvarande tabellstyrd bevisning.
   Chromium/E2E ska minst täcka:
   - Mälarenergi 2–4 lägenheter, utan effekt-/bandfält;
   - Luleå eller Nevel, med giltig effekt, valt band och en genuint
     icke-uniform tolvmånaders `flode_m3`-serie.
   Bind synliga referens- och 10/15/20-belopp mot oberoende facit. Bevisa att
   endast energiledet minskar medan flödesjustering, effekt/band och övriga
   prisled är identiska mellan före/efter.
6. Rätta gärna den kvarvarande kommentaren om att serien "kan vara
   leverantörens egna uppskattade månadsfördelning" till ett rent
   kvalitetspåstående: serien måste valideras mot kundens underlag före
   användning. Inför inget nytt antagande eller beräkningsbeteende.
7. Kör riktade och fullständiga Vitest, ren `tsc`, produktionsbygge med
   återställd `dist/`, relevanta Chromium/E2E-prov, samtliga matrisprov,
   generatorns `--check`, deterministisk regenerering och
   `git diff --check` i båda repona.

Committera den lokala aktiveringen avgränsat på kandidatgrenen och i skills.
Lämna därefter en ny unik `ACTIVATION_READY: Codex` med fullständiga hashar,
exakta testtal och 48/0/1/28. Ingen mainflytt eller push.

Ändra inte tariffdata, kostnadsmotor, resultatkontrakt, policyregister,
indataformulär, Enkey, andra produkter eller bryggfiler. Om UI-aktiveringen
kräver något av detta: stoppa `BLOCKED: Codex`.

`APPROVED_FOR_ACTIVATION: Claude`
