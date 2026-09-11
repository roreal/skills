---
review_id: "2026-09-11-005"
date: "2026-09-11"
reviewer: Codex
status: changes-required
scope:
  - "Granskning av den lokala aktiveringen av exakt två Lidköpingstariffer efter slutgranskning 2026-09-11-004"
  - "Katalogändring, genererad proveniens, produktkedja, faktisk sida, permanenta tester och disposition 9/55/28"
reviewed_heads:
  skills_catalog: "4b01d26f5a8e155db63d59bc3daf9b392457b6b2"
  skills_log: "7b7b5959d50446631b05602e776d9c5a8176c6a5"
  enkey-agents: "4f4e3b979bea8af6f85b8a071dd596f17a14b82b"
  neptune_academy: "f99576c9443809602c168bbb0e5a7b77690f5262"
implementation_changed_by_reviewer: false
push_status: not-approved
local_activation_status: "functionally-correct; keep active locally"
tariff_disposition: "9 implemented / 55 ready / 28 blocked av 92"
follows_review: "2026-09-11-004"
---

# Aktiveringsgranskning av Lidköping Batch 5d

## Beslut

**Changes required före push.** Själva lokala aktiveringen är funktionellt riktig och
ska inte återställas: exakt de två beställda Lidköpingstarifferna passerar grinden,
dispositionen är 9/55/28 och de två produkterna fungerar i den riktiga kalkylatorsidan.
Katalogens bytes, den genererade artefaktens katalog-SHA och provenienscommit stämmer.

Två avgränsade P2-fynd återstår. Det första gäller ett uttryckligt permanent
acceptanskrav från `2026-09-11-004`; det andra är en felaktig revisionsuppgift i den
styrande katalogen. Ingen motor-, pris-, tariff- eller beräkningsändring är beställd.

## Fynd

### P2 — den verkliga aktiverade produkten går inte genom en permanent sidrendering

Den nya filen `besparingsvardeLidkopingKatalogaktivering.test.ts` importerar visserligen
den riktiga `TARIFFER`-exporten och provar motorns och `calcResultForOnskadTyp` rena
funktionsgränser. Den renderar däremot inte `KalkylatorPage`. Formuleringen "hela sidans
entry" i testnamnet är därför starkare än vad testet faktiskt bevisar.

Den befintliga `KalkylatorPageLidkoping.test.tsx` renderar sidan men ersätter fortfarande
`tariffer.generated` med `vi.mock` och en testlokal prispost. Dess inledande kommentar
säger dessutom felaktigt att Lidköping fortfarande är `utreds`. Den självbärande
E2E-sviten har fortsatt åtta scenarier och inget av dem väljer en Lidköpingsprodukt.

Codex eget browserprov bekräftade att funktionen fungerar nu, men ett manuellt
granskningsprov skyddar inte nästa ändring. Lägg ett permanent, omockat sid-/E2E-prov
mot den incheckade genererade katalogen som minst:

1. bekräftar båda exakta Lidköpingsalternativen i väljaren,
2. skickar ett komplett MWh-formulär med band, effekt, alla tre tolvmånadersserier och
   `Tm`-attestering för vardera tariffen via vanlig knappsubmit,
3. bekräftar resultattypen aktuell uppskattad årskostnad samt rätt produktnamn utan
   `pageerror`, och
4. bekräftar i den riktiga sidan att ostödda indata-/produktval inte erbjuds och provar
   i de permanenta verkliga entrytesten att kr, schablon och besparing blockeras för
   båda produkterna med avsedda orsaker.

Behåll de åtta befintliga E2E-scenarierna och de syntetiska komponentproven. Rätta även
den inaktuella toppkommentaren i `KalkylatorPageLidkoping.test.tsx`; den filen är nu ett
isolerat mekanismprov, inte bevis för att de verkliga posterna är avstängda.

### P2 — katalogens revisionsnot påstår en attestering som inte finns

Revision `0.1.4` i `optimate-fjarrvarme-2026.json` säger att kalkylatorn kräver
leverantörens fakturerade effektvärde "med obligatorisk attestering". Det är inte det
implementerade kontraktet: effektvärdet är obligatoriskt och ska hämtas från faktura
eller leverantör, medan den obligatoriska attesteringen hör till nätets `Tm`-serie.

Rätta revisionsnoten så att dessa två krav hålls isär. Eftersom katalogens bytes då
ändras ska rätt ordning följas igen: commit av katalogkorrigeringen först, därefter
regenerering med just den fulla commit-hashen och kontroll av ny katalog-SHA/proveniens.
Tariffdata, statusspärrar och disposition ska vara oförändrade.

## Oberoende verifiering

- `.venv/bin/python -m pytest tools/tariffer/tests -q -p no:cacheprovider`:
  **510 passed**.
- `npm test -- --run`: **22 testfiler, 607 tester passerade**.
- `npx tsc --noEmit`: godkänd.
- `npm run build`: godkänd; endast den befintliga bundlevarningen.
- `npm run test:e2e`: samtliga **åtta befintliga** scenarier passerade.
- Bygggenererade `neptune-marketing/dist` återställdes; båda produktrepona är rena och
  `git diff --check` är rent.
- Katalogen har SHA-256
  `63a4d44c56f73e7dd8cfea178c146358987a1dd51910aae6504531afc4f11cfc`; exakt samma
  SHA finns i den genererade filen tillsammans med full katalogcommit
  `4b01d26f5a8e155db63d59bc3daf9b392457b6b2`.
- Mekanisk jämförelse mot den tidigare katalogen visar att endast de två angivna
  Lidköpingsposterna ändrar grindutfall. `godkanda()` går från 7 till 9; övriga
  avvisningsutfall är oförändrade.
- I en ren, verklig Chromium-session fanns båda produkterna i väljaren. Komplett MWh-
  knappsubmit gav resultat för både 0–41 kW och 42+ kW utan sidfel. Kronläget blockerades
  utan resultat. Detta visar att fyndet ovan gäller permanent regressionsbevisning, inte
  ett påvisat körfel.

## Exakt rättningsuppdrag till Claude

1. Committera först de redan skrivna Codex-filerna under `conversations` separat; ta
   inte med orelaterade arbetskopiefiler.
2. Rätta endast den felaktiga attesteringstexten i katalogens revision `0.1.4` och gör en
   fokuserad katalogcommit. Aktiveringen och 9/55/28 ska ligga kvar.
3. Regenerera `tariffer.generated.ts` från den nya katalogcommitten och uppdatera
   provenienstestet. Handredigera inte den genererade filen.
4. Lägg det omockade permanenta sid-/E2E-beviset ovan och rätta den gamla testkommentaren.
5. Kör 510+ Python, 607+ TypeScript, typkontroll, bygge, den utökade självbärande E2E-
   sviten och `git diff --check`. Återställ `dist` efteråt och verifiera åter exakt
   9/55/28 samt att bara de två avsedda produkterna är aktiva.
6. Logga fulla HEAD-hashar och stanna för Codex omgranskning. Pusha inget repo.

Codex ändrade ingen produktkod, katalogdata, aktiveringsstatus eller git-historik i
denna granskning.
