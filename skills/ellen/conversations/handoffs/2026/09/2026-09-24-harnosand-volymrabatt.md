---
handoff_id: "2026-09-24-001"
created_at: "2026-09-24T10:34:25+02:00"
from: "Codex"
to: "Claude"
status: "APPROVED_FOR_IMPLEMENTATION: Claude"
scope: "Härnösand Energi & Miljö 2026 — källnormalisering och spärrad årsprodukt"
approved_by: "Robert, Codex"
requested_by: "Robert"
skills_reviewed_head: "c25a809503fefdc4e9c78aaeec56302e79697fb0"
enkey_product_base: "451c85a0e19833e6607e109f44a30c0d54ef2815"
enkey_local_main_to_preserve: "2e30bb200d1831b8ca7461f67e0d958870ba6867"
neptune_product_base: "3cc527e895f95684d1aed9e553566b9578f075ca"
raw_email_allowed_in_git: false
activation_allowed: false
push_allowed: false
---

# Handoff: Härnösand 2026 efter leverantörssvar A2/R02

## Bindande källbeslut

Läs den sanitiserade bedömningen
[`2026-09-24-bedomning-harnosand-volymrabatt.md`](../../../../Fjarrvarmetariffer/Svar%20på%20frågor/2026-09-24-bedomning-harnosand-volymrabatt.md).

HEMAB har bekräftat att intervalltabellen är faktureringsgrundande och att
det publicerade räkneexemplet är fel. Vid 1 750 MWh är korrekt
volymrabatt **50 575 kr exklusive moms**, inte 45 050 kr. Tabellen är en
marginaltrappa med nedre gränser `[0, 500, 750, 1000, 1500, 2000]` och
satser `[0, 18.4, 33.1, 42.9, 65, 130]` kr/MWh. Rabatten avräknas på årets
sista faktura.

Rå `.eml` innehåller personuppgifter och får inte läggas till i Git.
Den sanitiserade bedömningsfilens SHA-256 är
`455f0684658c59101ff67aa0afb949fea66211fb4dcfe0729b3ac8097c5fe8d3`.

## Reposäkerhet och arbetskopior

Kontrollera HEAD:ar och arbetskopior före ändring. Stoppa med
`BLOCKED: Codex` om en angiven produktbas inte längre finns eller om ett
säkert isolerat arbete inte kan skapas.

- **Skills:** utgå från denna signalcommit ovanpå granskad
  `c25a809503fefdc4e9c78aaeec56302e79697fb0`. Staga bara uttryckligen
  avsedda filer. Bevara den redan smutsiga
  `Fjarrvarmetariffer/leverantorsfragor-blockerade-tariffer-2026.md`,
  `conversations/automation/`, `../milesight`, alla lokala `.eml`, PDF,
  XLSX och textClipping samt `AGENTS.md`, `SKILL.md`, `claude.md` och
  övriga olistade filer. De två lokala kopiorna av HEMAB-mejlet får inte
  stagas.
- **Enkey:** skapa en isolerad branch/worktree från exakt
  `451c85a0e19833e6607e109f44a30c0d54ef2815` (`origin/main`). Lokal
  `main@2e30bb200d1831b8ca7461f67e0d958870ba6867` har en orelaterad
  Milesight-commit och får inte flyttas, mergas, rebases eller skrivas om.
- **Neptune:** skapa en isolerad branch/worktree från exakt
  `3cc527e895f95684d1aed9e553566b9578f075ca` (`origin/main`). Spårad
  `neptune-marketing/dist/` ska lämnas identisk med basen efter tester.

Ingen merge, rebase, reset, historikomskrivning eller push ingår.

## Omfattning

Genomför källnormalisering och en komplett årsprodukt bakom befintlig
aktiveringsspärr för exakt tariff-ID
`harnosand-energi-miljo-harnosand-2026`.

1. Normalisera katalogkällorna, lägg till den sanitiserade bedömningen som
   källa, sätt `valid_from` till `2026-01-01`, flytta R02 från återstående
   till löst och uppdatera verifieringslista, inventering och batchplan
   append-only. Rätta `13_1`:s inaktuella titel/URL med en daterad
   proveniensnot; dess befintliga hash är identisk med HEMAB:s officiella
   2026-PDF. Äldre historikrader ska inte skrivas om.
2. Återanvänd `marginal_annual_volume_discount`, men gör
   avräkningssättet maskinläsbart och fail-closed. Gävle ska fortsatt
   uttrycka månadsvis avräkning; HEMAB ska uttrycka
   `last_invoice_of_calendar_year`. Årssumman är samma marginalaritmetik,
   men semantiken får inte tappas eller gömmas i fri text.
3. Implementera `capacity_overrun` i Python och TypeScript med sluten
   postform och formeln
   `max(0, debiteringsgrundande_effekt_kw − abonnerad_effekt_kw) × 1266 × 1,3`.
   Abonnerad effekt (minst 5 kW) är tariffens kapacitetsbindning.
   Debiteringsgrundande faktisk effekt ska vara ett separat, synligt och
   obligatoriskt policyfält från `supplier_value` eller `customer_value`;
   motorn får inte härleda eller tyst nollställa det. Om ett generiskt
   fältnamn används ska katalogpostens fältreferens och policybindning
   korsvalideras på samma sätt som befintliga fältrefererande
   justeringstyper.
4. Lägg till policy, generering och UI för `annual_forward`. Behåll
   `investigation.status: "utreds"` och `production_ready: false` under
   hela denna runda. Härnösand får inte bli valbar i skarp kalkylator och
   `godkanda()`-mängden får inte ändras före en separat aktiveringssignal.
   Sätt inte `stodjer_besparing: true` i denna leverans; Optimate-scenariot
   kräver ett separat produktbeslut om när abonnerad effekt får sänkas.

## Oberoende facit

Använd minst följande handräknade helproduktfall, utan att generera
förväntat värde genom produktionsfunktionen:

- månadsenergi: januari 500 MWh, april 500 MWh, december 750 MWh, övriga
  månader 0 MWh (summa 1 750 MWh);
- abonnerad effekt: 100 kW;
- debiteringsgrundande faktisk effekt: 120 kW;
- energi: `1 250 × 642 + 500 × 360 = 982 500 kr`;
- ordinarie effektavgift: `100 × 1 266 = 126 600 kr`;
- effektkorrigering: `20 × 1 266 × 1,3 = 32 916 kr`;
- volymrabatt: `−50 575 kr`;
- summa exklusive moms: **1 091 441 kr**;
- summa inklusive 25 procent moms: **1 364 301,25 kr**.

Testa dessutom bandgränserna 500, 750, 1 000, 1 500 och 2 000 MWh,
värden strax över varje gräns, sista obegränsade bandet, noll
effektöverskridande och ett positivt effektöverskridande. Mutationer av
enhet, avräkningssätt, gränsordning, satslängd, fältnamn, multiplikator
och period ska blockeras fail-closed i båda motorerna.

## Leveransgrind

- Katalogrevision, katalog-SHA och genererad TypeScript-proveniens ska
  synkas.
- Python/TypeScript-paritet, riktade enhetsprov, fulla testsviter, `tsc`,
  bygge och en isolerad browsergrind ska vara gröna.
- Browsergrinden ska bevisa facit ovan genom formuläret, men tariffen ska
  fortfarande saknas i den ordinarie skarpa leverantörslistan.
- Kontrollera mekaniskt dispositionen efter källnormalisering:
  **75 implemented / 3 ready / 13 blocked / 1 not_applicable av 92**.
- Ingen aktivering, merge/rebase/historikomskrivning eller push i denna
  runda. Lämna `REVIEW_READY: Codex` med exakta branch-/commit-hashar och
  testresultat.
