---
review_id: "2026-09-11-006"
date: "2026-09-11"
reviewer: Codex
status: changes-required
scope:
  - "Omgranskning av Lidköpings lokala aktiveringsrättning efter 2026-09-11-005"
  - "Katalogrevision, genererad proveniens och permanent omockad sidacceptans"
reviewed_heads:
  skills: "183e4f24c0f0e48204604f38b4e5bad0e33b671e"
  skills_catalog: "1143a0fc255a9940cc92263f0915181f46275cd0"
  enkey-agents: "49b2e6762c5e549780609a2cd76de0a8cde455ef"
  neptune_academy: "c6e3bc60a76f641a3c1861903048743eea28db0c"
implementation_changed_by_reviewer: false
push_status: not-approved
local_activation_status: "functionally-correct; keep active locally"
tariff_disposition: "9 implemented / 55 ready / 28 blocked av 92"
follows_review: "2026-09-11-005"
---

# Omgranskning av Lidköpings aktiveringsrättning 1

## Beslut

**Changes required före push, endast i testbevisningen.** De två materiella fynden från
`2026-09-11-005` är rättade i produkten: katalogrevisionen skiljer nu korrekt mellan
obligatoriskt effektvärde och `Tm`-attestering, den genererade proveniensen matchar den
nya katalogcommitten och ett omockat komponentprov renderar den verkliga
`KalkylatorPage` för båda Lidköpingsprodukterna.

Aktiveringen, tariffdata, beräkning och disposition 9/55/28 är fortsatt riktiga och ska
inte ändras. Två små men konkreta luckor gör att det permanenta acceptansbeviset ännu
inte uppfyller den beställda matrisen fullt ut.

## Fynd

### P2 — produktnamnsassertionen är inte bunden till resultatet

I `KalkylatorPageLidkopingAktiverad.test.tsx` hämtas det förväntade produktnamnet efter
submit, men assertionen använder `screen.getAllByText(forvantatNamn)`. Den kan alltid
träffa produktens redan befintliga `<option>` i leverantörsväljaren. Testet fortsätter
därför att passera även om årskostnadsresultatet skulle sluta visa produktnamnet.

Bind assertionen till det redan hittade resultelementet, exempelvis genom att kontrollera
att `resultat.textContent` innehåller `forvantatNamn`. Behåll kontrollen av båda
tarifferna via vanlig `requestSubmit()`.

### P2 — blockeringsmatrisen saknar fortfarande 42+ kW i schablonläget

Det verkliga entrytestet för `unsupported_input_mode` itererar över `kr` och `schablon`,
men använder bara `TARIFF_041`. Det nya sidprovet provar kr-läget för båda produkterna,
men provar inte schablon för 42+ och kontrollerar inte den typade orsaken där. Det
uttryckliga kravet i `2026-09-11-005` var kr, schablon och besparing för **båda** verkliga
poster med avsedda orsaker.

Utöka entrymatrisen till korsprodukten av båda tariff-ID:na och båda indataformaten.
Besparingsmatrisen täcker redan båda och behöver inte ändras. Sidprovet kan fortsatt
kontrollera att kr-submit inte ger resultat, men dess testnamn bör inte påstå att det
självt bevisar den typade orsaken.

### P3 — testkommentaren pekar på den tidigare genereringscommitten

Det nya sidtestet beskriver den incheckade `tariffer.generated.ts` som hämtad från
`skills@4b01d26`. Efter revisionsrättningen anger artefakten korrekt
`skills@1143a0f...`. Uppdatera kommentaren till den nuvarande genereringsproveniensen;
`4b01d26` kan fortfarande nämnas separat som den ursprungliga aktiveringscommitten.

## Stängda fynd och oberoende verifiering

- Katalogens revision `0.1.4` anger nu korrekt att effektvärdet är obligatoriskt från
  faktura/leverantör utan attestering och att attesteringen gäller nätets `Tm`-serie.
- Katalogens aktuella SHA-256 är
  `4a635244a117c8172e26de2c87305872b1434fde7e45d40db37db1275fd34572`. Samma SHA och
  full commit `1143a0fc255a9940cc92263f0915181f46275cd0` finns i den genererade filen.
- Det nya komponentprovet saknar `vi.mock` av tariffkatalogen, hittar båda verkliga
  alternativ och får resultat via komplett MWh-submit med band, effekt, Q/T/Tm och
  `Tm`-attestering för respektive produkt.
- Python: **510 passed**.
- TypeScript: **23 testfiler, 612 tester passerade**.
- `npx tsc --noEmit`: godkänd.
- Produktionsbygge: godkänt; endast den befintliga bundlevarningen.
- Självbärande E2E: samtliga **åtta befintliga** scenarier passerade.
- Bygggenererat `dist` återställdes. Produktrepona är rena och `git diff --check` är rent.
- Ingen ny tariff släpptes igenom; dispositionen är fortsatt exakt 9/55/28.

## Exakt rättningsuppdrag till Claude

1. Committera Codex nya `conversations`-filer separat utan orelaterade arbetskopiefiler.
2. Gör en enda fokuserad, test-only commit i `neptune_academy`:
   - bind produktnamnet till `arsprodukt-resultat`,
   - prova `kr` och `schablon` med `unsupported_input_mode` för båda verkliga
     tariff-ID:na,
   - rätta de två missvisande testkommentarerna/-namnen.
3. Ändra inte katalog, genererad artefakt, produktkod, tariffdata eller aktiveringsstatus.
4. Kör full TypeScript-svit, typkontroll, bygge och E2E; återställ `dist`, kör
   `git diff --check`, logga full HEAD och stanna. Python behöver bara köras igen om
   Python- eller katalogbytes ändå ändras. Ingen push.

Codex ändrade ingen produktkod, katalogdata, testkod eller git-historik i denna
omgranskning.
