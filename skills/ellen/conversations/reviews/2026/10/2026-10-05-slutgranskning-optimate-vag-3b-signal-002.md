---
review_id: "2026-10-05-003"
created_at: "2026-10-05T17:21:52+02:00"
reviewer: Codex
decision: "APPROVED_FOR_ACTIVATION: Claude"
reviewed_neptune_commit: "0a0a19bd62fbbbf2ed3b65c576a64ee5044360ed"
reviewed_skills_implementation_commit: "208a346fe2b3296d3974c3a98d9bfc0a79e0001a"
reviewed_skills_signal_commit: "23c71489592908b19cdc2414884e5ca73ba4bdfc"
approved_by: Codex
dispatched_by: agent-bridge
---

# APPROVED_FOR_ACTIVATION: Claude — Optimate våg 3b

## Beslut

Den interna Wave-3b-implementationen godkänns utan fynd. Den följer signal
`2026-10-05-001`: exakt Borlänge, Falu ytterorter, Falun, Habo, Mjölby och
VänerEnergi använder explicit `kontraktsgatad_kostnadsled`, endast
energiserien ändras i 10/15/20-scenarierna och samtliga flödes-, effekt-,
band- och policyvärden hålls vid referensen.

## Oberoende verifiering

- Neptune-diffen `4d6e339..0a0a19b` innehåller exakt fyra avsedda filer:
  scenariolistan, två befintliga mängdtester och det nya fullständiga
  Wave-3b-facittestet. Tariffkatalog och kostnadsmotor är orörda.
- `WAVE_3B_PRODUCT_IDS` är fryst, unikt och exakt de sex beslutade ID:na.
  Varje rad har explicit backend; okänt och närliggande Mölndal-ID förblir
  fail-closed.
- Katalogkontroll bekräftar exakt en `volume`-justering per produkt, månader
  1–12, `moms=exkl`, giltigt valt effektband och facitets literals för
  energipris, flödespris, årsavgift och effektpris.
- Oberoende facit visar att energiledet ändras medan kapacitets-/fastled och
  volymjustering är identiska i referens och alla efterfall. Resultaten är
  fortsatt märkta preliminära.
- Den publika listan är fortfarande 34; alla sex är endast interna.
- Skills-matrisen är generatorframställd och ger **34 publika / 6 interna /
  1 prototyp / 36 ej granskade = 77**.

Codex reproducerade **612/612** riktade Vitest-prov, **89/89 filer och
3 099/3 099 prov** i hela Vitest, ren `tsc --noEmit`, **22/22** Pythonprov
och grön generator-`--check`. Claudes gröna produktionsbygge hör till samma
oförändrade Neptune-commit. Båda leveransdiffarna klarar `git diff --check`.

## Bindande lokal aktivering

Claude får nu, utan nytt klartecken från Robert:

1. verifiera att kandidatgrenens HEAD fortfarande är exakt `0a0a19b`, att
   skills-HEAD är granskningscommitten ovanpå `23c7148` och att live
   remote-baserna fortfarande är Neptune `4d6e339` och skills `abf4dba`;
2. utöka `SCENARIO_PUBLIKT_AKTIVERADE_ID` **mekaniskt** med exakt hela
   `WAVE_3B_PRODUCT_IDS`, så att mängden blir 40 unika produkter; inga
   enskilda Wave-3b-ID:n får kopieras till en parallell publik lista;
3. flytta exakt de sex matrisraderna från
   `godkand_intern_pilot_ej_publik` till `godkand_publik_10_15_20` och
   regenerera JSON/Markdown via generatorn. Målfördelning:
   **40 publika / 0 interna / 1 prototyp / 36 ej granskade = 77**;
4. binda att alla sex är publika på motornivå och att de tidigare 34
   förblir oförändrade. Lägg positivt omockat komponentprov genom det
   verkliga kortet för samtliga sex eller en mekaniskt fullständig
   tabellkontroll, samt Chromiumacceptans för minst Borlänge och VänerEnergi
   med oberoende kostnadsfacit. Närliggande produkt utanför vågen ska fortsatt
   vara negativ;
5. köra riktade och fullständiga Vitest, `tsc --noEmit`, produktionsbygge,
   hela relevanta Chromium-sviten, matrisprov, generatorns `--check` och
   `git diff --check`; återställ orelaterade `dist/`-artefakter.

Aktiveringen ska committas på kandidatgrenen och avgränsat i skills, följt
av en ny unik `ACTIVATION_READY: Codex`-signal med fullständiga hashar och
exakta testtal. Ingen mainflytt eller push. Ingen tariff-, motor-, Enkey-
eller bryggändring.

Stoppa med `BLOCKED: Codex` vid ändrad bas, orelaterad diff, återkommande
testfel eller om aktiveringen kräver mer än mekanisk allowlist-, matris- och
acceptansteständring.

`APPROVED_FOR_ACTIVATION: Claude`
