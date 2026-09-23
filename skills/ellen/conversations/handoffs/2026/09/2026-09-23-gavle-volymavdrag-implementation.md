---
handoff_id: "2026-09-23-003"
created_at: "2026-09-23T10:50:14+02:00"
from: Codex
to: Claude
status: "APPROVED_FOR_IMPLEMENTATION: Claude"
approved_scope: "gavle-r16-source-normalization-and-marginal-volume-discount-behind-gate"
skills_reviewed_head: "cafbf231978b854ddf926264fb2df0da4d5c4803"
enkey_product_base: "716d2e8816388b10bac892d29b68682d12b1d9d0"
enkey_local_main_to_preserve: "2e30bb200d1831b8ca7461f67e0d958870ba6867"
neptune_product_base: "605bddd5c39a0663ca01ab8ad88acd25013a9aa0"
activation_allowed: false
push_allowed: false
approved_by: Codex
requested_by: Robert
---

# Implementera Gävle Energis marginala volymavdrag bakom spärr

## Mål och bindande källbeslut

Robert godkänner att Claude normaliserar Gävles besvarade fråga R16 och
implementerar den därpå följande beräkningsregeln. Den sanitiserade
källbedömningen är
[2026-09-23-bedomning-gavle-volymavdrag.md](../../../../Fjarrvarmetariffer/Svar%20på%20frågor/2026-09-23-bedomning-gavle-volymavdrag.md).
Originalmejlet och bilagan innehåller personuppgifter och får inte
committas.

Leverantörens exempel är bindande för semantiken:

- ackumulerat januari–april: 94,57 MWh;
- maj: 9,65 MWh, varav endast 4,22 MWh över 100-MWh-gränsen får avdrag;
- helår: 193 MWh, varav 93 MWh får 35 kr/MWh avdrag;
- avdrag: 3 255 kr exklusive moms;
- inga tidigare månader räknas om retroaktivt;
- avdraget beräknas och betalas månadsvis.

Katalogens publicerade gränser och satser ska därför användas som en
marginaltrappa: 0/100/250/500/1 500/2 500 MWh med 0/35/55/75/95/125
kr/MWh. Den befintliga `volume_discount` får **inte** återanvändas: den
väljer ett enda band från ett annat kvalificeringsunderlag och applicerar
satsen på all köpt energi.

## Reposäkerhet och arbetskopior

Kontrollera HEAD:ar och arbetskopior innan ändring. Stoppa med
`BLOCKED: Codex` om någon bas inte längre matchar eller om ett säkert
isolerat arbete inte kan skapas.

- **Enkey:** lokal `main@2e30bb2` innehåller en orelaterad Milesight-commit
  och har divergerat från tariffens aktuella `origin/main@716d2e8`.
  Skapa en isolerad branch/worktree från exakt `716d2e8`; flytta eller
  skriv inte om lokal `main`, och inkludera aldrig Milesight-commiten.
- **Neptune:** skapa en isolerad branch/worktree från exakt lokal
  `main@605bddd`. Den basen innehåller den redan granskade men opushade
  scenariomotorn. Ändra inte dess scenariomotorfiler i detta uppdrag.
- **Skills:** arbeta ovanpå handoff-committens förälder `cafbf23` och den
  nya handoff-committen. Staga endast avsedda filer. Bevara alla redan
  smutsiga/orelaterade filer, särskilt
  `Fjarrvarmetariffer/leverantorsfragor-blockerade-tariffer-2026.md`,
  `conversations/automation/`, `../milesight`, lokala `.eml`/PDF/XLSX,
  `AGENTS.md`, `SKILL.md`, `claude.md` och övriga olistade underlag.
  Frågedokumentet är redan smutsigt och får inte redigeras i denna runda.

Ingen merge, rebase, reset, historikomskrivning eller push ingår.

## 1. Källnormalisering i skills

Normalisera bara Gävle/R16 och daterad dokumentation:

1. Lägg till den sanitiserade leverantörsbekräftelsen som källproveniens
   för `gavle-energi-gavle-2026`, utan personuppgifter.
2. Flytta R16 från `remaining_information_requests` till
   `resolved_information_requests`, med bevarad fråga och exakt
   sammanfattad lösning. Kvarvarande fysiska frågor ska därefter vara
   exakt `R02`, `R03`, `R08`.
3. Ändra Gävles källa från `external_answer_required` till
   `source_resolved_implementation_pending`. Behåll
   `production_ready: false` och en fail-closed `investigation` tills en
   separat aktiveringsrunda godkänts.
4. Rätta Gävlepostens stale kapacitetsmetadata enligt de redan verifierade
   villkoren: `fixed` ska vara 0, kapacitetsavgiften periodiseras efter
   kalenderdagar (`days_in_month/days_in_year`) och leverantörens
   debiteringsgrund är redan **kWh/dygn**, varför den explicita
   omräkningsfaktorn ska vara `kw_faktor: 1.0`, inte den generiska
   kW→kWh/dygn-faktorn 24. Behåll krav på leverantörens/fakturans
   debiteringsgrund och befintligt bekräftat band-ID.
5. Uppdatera verifieringslista, inventering och batchplan med daterade,
   icke-historikomskrivande rättelser. Den skarpa dispositionen förblir
   **74 implementerade / 2 redo / 15 blockerade / 1 ej tillämplig av
   92**. Under blockerade ändras orsaksfördelningen från 10 källösta + 5
   externt obesvarade till 11 + 4.

Ändra inga andra tariffers priser, källstatus, `investigation`,
`production_ready` eller disposition.

## 2. Ny beräkningstyp i Python

Implementera katalogens befintliga råtyp
`marginal_annual_volume_discount` som en egen, fail-closed justeringstyp:

- strikt validering av exakt stödd form (`unit: SEK/MWh`,
  `accumulation: calendar_year`, lika långa listor, ändliga och
  icke-negativa satser, första gräns 0, strikt stigande gränser);
- transport/normalisering utan fri texttolkning;
- ingen kundifyllbar parameter: beräkningsunderlaget är samma kalenderårs
  tolv köpta MWh-värden;
- gå genom månaderna januari–december och dela varje tröskelmånad mellan
  berörda marginalband; kostnadsjusteringen ska vara negativ;
- avvisa trasiga eller icke-fysiska serier fail-closed i stället för att
  hoppa över posten eller anta noll;
- återanvänd inte Gotlands `volume_discount`-kvalificeringsfält.

Lägg Gävle i ordinarie policy-/kontraktsväg bakom katalogspärren.
Debiteringsgrunden ska presenteras och behandlas som kWh/dygn från
leverantör/faktura; ingen dold kW×24-omräkning får ske.

## 3. TypeScript- och produktintegration

Spegla samma typ, validering, månadsackumulering, tecken och
kapacitetskontrakt i Neptune. Okänd eller felaktig justeringstyp ska
fortsatt stoppa beräkningen. Lägg till den isolerade Gävleprodukten i
policy/formulärflödet med korrekt enhet och hjälptext, men ändra inte den
skarpa publika väljaren eller någon Optimate-scenariogrind.

Regenerera skarp katalogdata endast om befintlig generator kräver ny
källhash; bevisa då att produktmängden och hela genererade kroppen utöver
provenienshuvudet är oförändrade. Skapa en isolerad Gävle-generator/
fixture för produkt- och browseracceptans utan att rensa
`investigation` generellt eller släppa någon annan kandidat.

## 4. Obligatoriska facit och tester

Minimikrav, i både Python och TypeScript där logiken speglas:

1. Leverantörens serie
   `28,95/25,09/23,16/17,37/9,65/5,79/3,86/5,79/9,65/15,44/21,23/27,02`
   ska ge exakt 193 MWh, 4,22 rabatt-MWh i maj, 93 rabatt-MWh på året
   och `-3 255 kr` justering.
2. Separata gränsfall exakt på och strax över 100, 250, 500, 1 500 och
   2 500 MWh. Ett ankare för 300 MWh ska ge
   `-(150×35 + 50×55) = -8 000 kr`.
3. Mutationstest ska fälla ändrad gräns, sats, bandordning, tecken,
   kalenderackumulering och Gävles `kw_faktor`.
4. Oberoende fullproduktfacit med leverantörens månadsserie, band `1` och
   syntetisk debiteringsgrund 100 kWh/dygn:
   energikostnad `98 920,22 kr`, kapacitet `4 163,00 kr`, justering
   `-3 255,00 kr`, summa exkl. moms `99 828,22 kr`, summa inkl. moms
   `124 785,275 kr` före presentationsavrundning. Generera inte facit med
   samma produktionsfunktion som testas.
5. Negativa, NaN/Infinity, saknade månader, dubbla/ostigande gränser och
   olika listlängder ska stoppas.
6. Isolerat browsertest ska välja Gävle, visa debiteringsgrunden som
   kWh/dygn och nå samma handräknade årsresultat. Ordinarie skarpa UI:t
   ska fortfarande inte erbjuda Gävle före aktivering.

Kör riktade och fullständiga Python-/TypeScripttester, `tsc`, isolerat
bygge, ordinarie och isolerad E2E, katalog-/dispositionsgrindar samt
`git diff --check`. Redovisa exakta resultat och alla repo-/branch-HEAD:ar.

## Leveransgrind

Committera fokuserade ändringar lokalt. Avsluta med en ny, unik och
committad `REVIEW_READY: Codex`-post överst i `conversations/index.md`
som länkar till en sessionslogg och anger:

- exakt skills-, Enkey-branch- och Neptune-branch-HEAD;
- baser och faktisk fillista;
- testresultat och skarp/projicerad disposition;
- att lokal Enkey- och Neptune-`main` bevarats;
- att ingen aktivering, push eller scenariofunktion ändrats.

Ingen tariff får aktiveras och inget får pushas i denna runda.
