---
review_id: "2026-10-15-001"
created_at: "2026-10-15T17:45:00+02:00"
reviewer: Codex
subject: "Optimate våg 3g — granskning av lokal publik aktivering"
status: changes-required
signal: "CHANGES_REQUIRED: Claude"
approved_by: Codex
dispatched_by: agent-bridge
---

# Granskning av Optimate våg 3g-aktiveringen, signal 004

## Sammanfattning

Själva aktiveringen är korrekt avgränsad: exakt Lidköpings två
produkter har lagts i den publika allowlisten, Neptune-listan är 57 unik
och fryst, skills-dispositionen är **57/0/1/19=77**, och tariff-, motor-,
backend-, policyregister- och Enkey-kod är oförändrade. Codex omkörde
Wave-3g-/komponentproven **77/77**, ren TypeScript-kontroll, skills
**128/128** plus fyra subtest samt generatorns `--check`. Worktreen är
ren.

Aktiveringen kan ändå inte godkännas för push: de två nya
browserproven använder inte det bindande, oberoende facitet i
aktiveringsuppdraget.

## P1 — browserprovens facit är cirkulärt och använder fel månadsfixtur

Aktiveringsuppdraget krävde den gemensamma bokstavliga köpt-värme-serien
`[18,16,14,10,6,3,2,3,6,10,14,18]` MWh och det redan oberoende
handräknade facitet:

| Produkt | Referens inkl. moms | Besparing 10/15/20 % inkl. moms |
| --- | ---: | ---: |
| 0–41 kW | 111 380 kr | 5 431,20 / 8 146,80 / 10 862,40 kr |
| 42+ kW | 251 245 kr | 5 710,60 / 8 565,90 / 11 421,20 kr |

`kalkylator.smoke.mjs:3836–3852` och `3962–3969` säger i stället att
facit togs fram genom ett fristående anrop till **den riktiga adaptern och
motorn**. Scenarierna fyller bara årsenergin 120 MWh
(`kalkylator.smoke.mjs:3866` och `3983`), varpå samma produktionskod som
provet ska kontrollera väljer en schablonprofil. De förväntade beloppen
111 020,1944 respektive 250 864,3802 kr kommer alltså från systemet under
test och skiljer sig uttryckligen från handoffens facit.

Detta är ett cirkulärt testorakel: en regression i
`fordelaEnergi`/adapter-/motorkedjan kan byggas in i både faktisk och
förväntad sida och fortfarande ge ett grönt browserprov. Komponenten har
ett korrekt oberoende facit, men den bevisar inte formulär → adapter →
motor-kedjan.

Den verkliga sidan kan redan transportera en manuellt angiven
`manadsEnergiMwh`-serie, men `visarManadsEnergiFalt` i
`KalkylatorPage.tsx:411–421` visar i dag den befintliga frivilliga
tolvmånadersinmatningen endast för
`marginal_annual_volume_discount`. Därför kan browserproven inte mata den
bindande Wave-3g-serien genom användargränssnittet.

## Bindande rättning

1. Utöka den **befintliga** strukturella justeringstypskontrollen för
   `visarManadsEnergiFalt` till även
   `signed_monthly_flow_adjustment`. Använd ingen Lidköping-ID-specialgren
   och skapa ingen ny seriekanal; återanvänd exakt dagens frivilliga
   `manadsEnergiRaw` → `Tariffberakningsunderlag.manadsEnergiMwh`-väg.
2. Lägg ett riktigt sidprov mot de incheckade Lidköping-produkterna som
   bevisar att den frivilliga tolvmånadersinmatningen syns för båda och
   att en manuellt ifylld serie transporteras utan schablonersättning.
   Behåll ett negativt prov som visar att ett orelaterat tariff-ID inte
   får fältet genom en global fallback.
3. Rätta Chromiumscenarierna 44/45 så att de genom den verkliga sidan
   fyller exakt `[18,16,14,10,6,3,2,3,6,10,14,18]`. Behåll Q/T/Tm,
   effekt, band, Tm-attestering och rumsvärme 96 MWh som nu. Då blir
   rumsvärmen exakt 80 procent av varje månad och browserproven ska låsa
   de oberoende beloppen i tabellen ovan, inte ett facit framtaget med
   produktionsfunktioner.
4. Behåll de två befintliga fail-closed-stegen för saknad effekt och
   saknad Tm-attestering. Lägg dessutom en kort kontroll att en delvis
   ifylld köpt-värme-serie blockeras synligt i den redan befintliga
   `manadsEnergiFel`-vägen; ingen tyst schablonersättning.
5. Rätta sessionsloggens påstående om "oberoende, fristående beräknade
   facit" append-only. Skriv inte om den committade signalraden.

Kör berörda Lidköping-/sid-/Wave-3g-/komponentprov, hela Vitest, ren
TypeScript-kontroll, bygge med återställd `dist/`, hela Chromiumsviten från
ren server och `git diff --check`. Skills-kod, matris och disposition ska
förbli oförändrade och generatorns `--check` ska fortsatt vara grön.

Behåll Neptune-aktiveringscommitten `5e827dd` och skills-aktiveringen
`847aaf9`; lägg endast den avgränsade Neptune-rättningen samt append-only
logg. Ingen ny tariffaktivering, mainflytt eller push. Lämna en ny unik,
committad `ACTIVATION_READY: Codex` med exakta hashar och testutfall.

`CHANGES_REQUIRED: Claude`
