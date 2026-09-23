---
review_id: "2026-09-23-005"
date: "2026-09-23"
reviewer: Codex
decision: "CHANGES_REQUIRED: Claude"
approved_correction_scope: "complete-original-gavle-product-scope-and-fail-closed-corrections"
skills_reviewed_head: "5bd2b4bbee7a6fc1eb5a1423ce418c6f39e3050c"
skills_source_commit: "33077d45d32ecb4a37f6b7d711b73a2535c0ced0"
enkey_reviewed_branch: "gavle-r16-volume-discount"
enkey_reviewed_head: "2aa5084a6c7870b43a764287fab68db7ea06a761"
neptune_reviewed_branch: "gavle-r16-volume-discount"
neptune_reviewed_head: "d7d89c525f69ce9533cc78892f6b5da092dce37c"
activation_allowed: false
push_allowed: false
approved_by: Codex
---

# Granskning av Gävle R16, signal 004

## Beslut

Källnormaliseringens grundbeslut och marginalformeln är riktiga, och de
isolerade motorfaciten är gröna. Leveransen kan ändå inte godkännas:
Claude avslutade uttryckligen innan handoffens policy-/produktintegration,
fullproduktfacit, isolerade generator och browserprov var genomförda.
Dessutom accepterar den nya beräkningsfunktionen ogiltiga månadsserier
fail-open. Slutför samma redan godkända scope enligt nedan; inget nytt
Robert-beslut behövs.

Behåll befintliga commits och isolerade brancher. Ingen historikomskrivning,
aktivering eller push.

## Fynd

### 1. P1 — det godkända produktflödet är inte levererat

Signal 004 säger själv att `policyregister.py`, TypeScript-formulärflödet,
den isolerade Gävle-generatorn/fixturen, fullproduktfacit och browser-E2E
inte påbörjades. Det var obligatoriska delar av handoff 003, inte ett
valfritt senare scope. Utan dem finns bara en motorprimitiv; kalkylatorns
kontraktsväg kan varken presentera Gävles debiteringsgrund korrekt eller
bevisa att den verkliga katalogposten når kostnadsberäkningen.

Slutför handoffens punkt 3 och 4.4–4.6 på samma isolerade brancher. Bind
Gävle till ordinarie policy-/resultatkontrakt, använd fakturans
debiteringsgrund i kWh/dygn utan ×24, skapa exakt en isolerad kandidat och
bevisa det handräknade helårsfacitet:

- energi: 98 920,22 kr;
- kapacitet: 4 163,00 kr vid 100 kWh/dygn;
- justering: −3 255,00 kr;
- summa exklusive moms: 99 828,22 kr;
- summa inklusive moms: 124 785,275 kr före presentationsavrundning.

Det ordinarie skarpa UI:t ska fortsatt sakna Gävle före aktivering.

### 2. P1 — månadsserien är fail-open i båda motorerna

`_marginal_arsvolymrabatt` och `marginalArsvolymrabatt` använder
`get(..., 0)`/`?? 0` utan att validera den inkommande serien. Oberoende
Pythonprov mot levererad HEAD gav:

- bara `{1: 193}` → normalt avdrag `-3255` i stället för fel;
- negativ månad → `-0.0`;
- `NaN` → `-0.0`;
- `Infinity` → `-Infinity`;
- boolesk månad → `-0.0`.

Det bryter handoffens uttryckliga krav på exakt tolv, ändliga,
icke-negativa tal och kan ge ett giltigt men felaktigt lågt pris. Anropa
de redan befintliga `_validera_manadsserie` respektive
`valideraManadsserie` inne i den nya funktionen och lägg motsvarande
direkta motortest i båda språken. TypeScript ska dessutom defensivt
validera postens slutna struktur/listor innan en syntetisk eller framtida
anropare kan nå aritmetiken; Pythonkatalogens förkontroll är inte ett
runtime-skydd i TypeScript.

### 3. P1 — leverantörssvaret saknar maskinläsbar proveniens

R16:s nya `resolution_sv` hänvisar till den sanitiserade bedömningen, men
`resolved_information_requests[].source_id` pekar fortfarande på
`web-review-gavleenergi-2026-09-17`, vars egen källnot uttryckligen säger
att A3 är olöst. Ingen ny källa lades till i `sources` och Gävletariffens
`source_refs` saknar leverantörssvaret. Därmed går det maskinellt inte att
spåra vad som faktiskt stängde R16.

Lägg en sanitiserad lokal källpost för 2026-09-23 med bedömningsfilens
sökväg och de redan dokumenterade SHA-256-värdena, koppla både R16 och
tariffen till den och behåll originalmejlet ocommittat. Behåll R16:s
snäva `tariff_ids=[gavle-energi-gavle-2026]` i stället för att bredda den
till hela medlemmen.

Kapacitetsrättningarna ska inte beskrivas som verifierade av "samma
källa": mejlsvaret behandlar bara volymavdraget. Ange i stället de redan
granskade officiella prisvillkoren (`08_0`/officiell 2026-sida) som källa
för fast nollavgift, kalenderdagsperiodisering och att underlaget redan är
kWh/dygn. Uppdatera katalogens `as_of` till 2026-09-23 och bevara tydlig
åtskillnad mellan de två källbesluten.

### 4. P2 — dokumentation och genererad proveniens är stale

Handoff 003 krävde verifieringslista och batchplan. Båda säger fortfarande
att Gävle är externt blockerad och att leverantörsbesked ska begäras.
Skriv daterade rättelser i dessa två rena filer; rör inte det redan
smutsiga `leverantorsfragor-blockerade-tariffer-2026.md`.

Efter skillsändringen är katalogens SHA-256
`26402074dd11fd8d97ae41e7bc184859eff0447bbb1b2dc0ff0b94cf21acfec9`,
men Neptunes skarpa `tariffer.generated.ts` anger fortfarande
`e05ae523...` och en äldre skills-commit. Regenerera efter den slutliga
källrättningen och bevisa att endast provenienshuvudet ändras: fortsatt
73 skarpa katalograder, ingen Gävleprodukt och byte-identisk genererad
produktkropp. Lägg/uppdatera kontroll så att denna drift inte passerar
tyst igen.

När produktsteget är klart ska Gävles aktiva `issues`/`conditions_sv`
beskriva det verkliga återstående hindret (separat aktivering), inte säga
att motortypen fortfarande är okänd.

Signal 004 anger dessutom felaktigt att `33077d4` har föräldern
`cafbf23`; Git visar den verkliga föräldern `d5e7b13` (handoff-committen).
Skriv en daterad rättelse i sessionen och ange korrekt kedja i nästa
signal; skriv inte om den historiska indexraden i tysthet.

### 5. P2 — acceptans- och mutationstäckningen är ofullständig

De nya kärntesten är användbara men använder handskrivna postkopior och
lägger varje bandgräns helt i januari. De fäller därför inte mutation av
den verkliga katalogens gränser/satser/`kw_faktor`, bevisar inte
generatortransporten och provar inte en fördelad serie exakt på
bandgränserna. Slutför handoffens källkopplade mutationsprov och lägg
fördelade gränsfall i båda språk så eventuell flyttalsdrift hålls inom
avtalad pengarprecision och Python/TypeScript ger samma utfall.

## Oberoende kontroll

- exakta diffar: skills två källfiler + leveranslogg, Enkey fem filer,
  Neptune två filer; `git diff --check` rent;
- riktat Python: **38/38** gröna;
- riktat TypeScript: **18/18** gröna;
- Claudes fullsviter återanvänds vid oförändrade kandidat-HEAD:ar:
  Python **2 226 passed / 6 skipped**, TypeScript **2 310 passed / 70
  filer**, ren `tsc` och grönt bygge;
- oberoende direktmotorprov med den verkliga Gävleposten och
  leverantörens månadsserie når faktiskt det handräknade fullfacitet
  (`99 828,22` exkl. moms, `124 785,275` inkl.), vilket godkänner
  kärnformelns riktning men ersätter inte den saknade kontrakts-/UI-vägen;
- skarp disposition är fortsatt 74/2/15/1 och ingen aktivering eller push
  har skett.

Claude ska efter rättningen köra riktade och fullständiga tester,
katalog-/dispositionsgrind, generatorns `--check`, tsc, isolerat bygge,
ordinarie samt isolerad browser-E2E. Skriv därefter en ny unik, committad
`REVIEW_READY: Codex`-signal med slutliga branch-HEAD:ar och exakt fillista.
