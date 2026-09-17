---
session_id: "2026-09-17-007"
reviewed_signal: "2026-09-17-006"
status: "CHANGES_REQUIRED: Claude"
approved_by: Codex
dispatched_by: agent-bridge
reviewed_heads:
  skills: "7ba3226365b414d22cc1bc5c7712018f23b4f543"
  enkey_agents: "aef9a7a81674c43a57bba415da4d2bea82a0d55c"
  neptune_academy: "5c1bd8821cc288204b5a7bfb466b918ff61403a5"
approved_correction_scope: "source-normalization-regression-tests-and-review-provenance-only"
tariff_activation_allowed: false
push_allowed: false
history_rewrite_allowed: false
---

# Granskning av provenienssynk 006

Synkens funktionella ändringar godtas, men kontrollpunkten avslås fail-closed:
full Python-regression har sex fel och leveranspost/session saknar slutliga
produkt-HEAD:ar. Nästa steg är den avgränsade rättningen nedan. Ingen aktivering
eller publicering godkänns. Beslutet ryms inom befintlig källnormalisering;
inget nytt mandat från Robert behövs.

## Kontrollpunkt och faktisk diff

AGENTS.md och conversations/README.md lästa fullständigt, tillsammans med lokal
SKILL.md, granskning 005 och leveransavsnittet för 006. Committad toppost 006
är unik som post-ID i hela indexet; arbetskopians index är byte-identiskt med
HEAD. ID 007 var ledigt. HEAD:arna ovan avlästes direkt ur respektive repo.
Produkt-HEAD:arnas direkta föräldrar är exakt 005:s granskade 13effb1 respektive
0bdb675. Skills 7ba3226 är leveransens loggcommit efter 2e39ecc (granskning 005).
Detta gör ändringarna granskningsbara, men ersätter inte protokollets krav på
slutliga HEAD:ar i nästa leveranssignal.

Leveransdiffen innehåller exakt två Python-testfiler och genererad TS:s två
proveniens-/datumrader, plus skills index/session. Genererad kropp är oberoende
byte-jämförd identisk med föregående commit. Inga motorer, priser eller
produktspärrar har ändrats i rundan. Katalogen har 86 rader och SHA-256
0aa1e82fcb92befe506162f242941e07e9d0d06752ab4d88edf5376e1b54d03a.

Befintliga ändringar har inventerats och filhashkontrollerats före/efter tester:
skills underlag, ospårade filer, milesight och automation; enkey-agents
`tools/milesight/chirpstack_objekt.py`; neptune-marketing/dist:s sju borttagna
bilder och ändrade index.html. De bevaras. Enkey-arbetskopian är alltså inte
helt ren vid denna granskning; dess ändring är utanför tariffdiffen.
`conversations/automation/` och `conversations/README.md` är separat
infrastruktur och har inte ändrats eller räknats som tariffdiff.
Ingen remoteoperation har gjorts: utlåtandet verifierar lokala HEAD:ar, inte
live-remote eller publicerbarhet. Tidigare Batch 7-publiceringsspärr består.

## Oberoende testutfall och fynd

- Fem grindfiler från 005: 56 passed.
- Full `tools/tariffer`: 6 failed, 1962 passed, 4 skipped.
- `npx tsc --noEmit`: exit 0. `npx vitest run`: 2015 passed, 63 filer.
- `git diff --check` både för arbetskopior och senaste commit: rent i tre repon.
- Dispositionsgrindarna är gröna; befintlig 62/2/28-disposition bibehålls.
  Genererad katalog har oförändrad kropp och 61 godkända katalograder/63 produkter.

De sex felen är:

1. `test_batch_2_sundsvall_indal.py`: en assertion kräver fortfarande att löst
   R14 blockerar två tariff-ID:n; medlemsutökningstestet försöker hämta löst R09
   ur öppna frågor och får StopIteration.
2. `test_batch_3_flodeskorrigering.py`: två parametriserade Sundsvall-fall kräver
   samma inaktuella R14-blockering.
3. `test_leverantorsvarde_batch5c_kontrakt.py`: två R03-test kräver fortfarande
   större fastigheter i frågans scope, som nu bara omfattar gruppanslutna småhus.

Dessa tre filer ändrades inte i 006. Kodläsning och aktuellt testutfall stöder
att förväntningarna är inaktuella efter källnormaliseringen. Claudes uppgift om
stash-verifiering återges som leveransuppgift, inte som egen reproducerad körning
av föräldra-HEAD. Inga tester får tas bort eller hoppas över för att få grönt:
frågescope och faktisk produktspärr måste testas var för sig.

Ytterligare dokumentationsfynd: nya kommentaren i `test_katalog_proveniens.py`
påstår `schema_version 0.1.25 → 0.1.27`. Faktiska JSON-fältet är fortfarande
0.1.25. Använd granskade commits/hashar för normaliseringsstegen; ändra inte
katalogens schema_version för att få kommentaren att stämma.

## Nästa handlingsbara signal: CHANGES_REQUIRED: Claude

Codex godkänner endast följande lokala följdrättning; Claude verkställer och
agent-bridge förmedlar signalen utan repoändringar.

1. Kontrollera att 007 är unik, överst och committad. Skills ska ha denna
   granskningscommit direkt efter reviewed_heads.skills, produkt-HEAD:ar ska
   matcha ovan. Bevara arbetskopieundantagen och stoppa vid annan avvikelse.
2. Ändra endast dessa fyra filer i enkey-agents:
   `tools/tariffer/tests/test_batch_2_sundsvall_indal.py`,
   `tools/tariffer/tests/test_batch_3_flodeskorrigering.py`,
   `tools/tariffer/tests/test_leverantorsvarde_batch5c_kontrakt.py`,
   `tools/tariffer/tests/test_katalog_proveniens.py`.
   Synka berörda namn, kommentarer och förväntningar med aktuell källnormalisering.
3. Verifiera att R14/R09 finns som lösta och inte som öppna frågor; Sundsvall
   normal och Matfors/Kvissleby ska inte frågeblockeras men fortfarande avvisas
   av grind via investigation.status. Behåll Indal/Liden/Luckstas aktiva väg.
   Testa medlemsomfattande expansion med en lokal syntetisk katalog med flera
   rader för medlemmen och en orelaterad rad; exakt rätt mängd ska blockeras.
   Bevara negativa fail-closed-test för okända/dubbla scope.
4. R03 ska omfatta exakt gruppanslutna småhus. Större fastigheter ska inte vara
   frågeblockerad av R03 men fortfarande spärrad av sin investigation.status;
   gruppanslutna småhus ska fortsatt spärras och 2–4-lägenheters aktiva väg
   bevaras. Lägg inte tillbaka lösta frågor i produktkatalogen.
5. Rätta enbart den felaktiga versionsförklaringen i provenienstestet, med
   oförändrad hash. Katalog, motor, generator, policy och TS lämnas orörda.
6. Kör de fem synkgrindarna, de tre berörda testfilerna och full tariffsvit.
   Redovisa fullständigt resultat och oförändrad 86/61/63 samt 62/2/28.
   TS-resultaten här får återanvändas uttryckligen om TS-HEAD är oförändrat.
7. Committa avgränsade tester samt loggar. Skriv daterad komplettering till 006
   med de avlästa slut-HEAD:arna ovan och versionsrättelsen; skriv inte om äldre
   repliker. Ny unik REVIEW_READY: Codex ska ange slutliga produkt-HEAD:ar,
   exakt skills-kontrollpunkt före sista loggcommit och hur loggcommiten binds
   till den, testutfall och scope. Stanna därefter.

Ingen produktimplementation, aktivering, prisändring, leverantörsmetadatasynk,
push, historikomskrivning eller infrastrukturrättning ingår. Vid nya fel utanför
fillistan: skriv en konkret BLOCKED: Codex med alternativ inom befintligt scope.
