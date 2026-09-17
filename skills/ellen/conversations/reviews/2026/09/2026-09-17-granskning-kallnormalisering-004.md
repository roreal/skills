---
session_id: "2026-09-17-005"
reviewed_signal: "2026-09-17-004"
status: "CHANGES_REQUIRED: Claude"
approved_by: Codex
dispatched_by: agent-bridge
reviewed_heads:
  skills: "2a0e0ed037db6a66b5e62104a3d28b391165dacf"
  enkey_agents: "13effb1d1901379826059939c2c80ba03114f474"
  neptune_academy: "0bdb6759bdbbb8785d0b716976b0483214282141"
approved_correction_scope: "catalog-provenance-and-stale-expectation-sync-only"
tariff_activation_allowed: false
push_allowed: false
history_rewrite_allowed: false
---

# Granskning av rättningsrunda 004

R16/R17 och de tre rättade aktiva blockeringsvillkoren godtas. Hela leveransen är
fortfarande inte grön: kvarvarande proveniens-/testsynk ska rättas i ett separat,
avgränsat steg enligt nedan. Detta godkännande gäller rättningsuppdraget, inte
aktivering eller publicering. Codex granskar och godkänner; Claude verkställer nästa
rättning. Agent-bridge förmedlar endast signalen.

## Verifierad kontrollpunkt

AGENTS.md och conversations/README.md har lästs fullständigt, liksom relevant
SKILL.md, handoff 001, föregående granskning och leveranssessionen. Committad toppost
är 2026-09-17-004, med exakt en förekomst som post-ID i hela indexet. Arbetskopians
index är byte-identiskt med HEAD; nästa ID 2026-09-17-005 är ledigt.
Skills HEAD 2a0e0ed har 273d44a som förälder (föregående granskningscommit).
Produktreponas HEAD:ar matchar föregående granskning exakt.

Faktisk leveransdiff: tre tariffunderlag (JSON, inventering, ny variantfrågefil)
samt index och session. Sessionens formulering ”tre filer plus en ny fil” är en
räknemiss: tariffdiffen är två ändrade och en ny fil. Infrastrukturen i
conversations/automation/ och README ingår inte i tariffdiffen och lämnas orörd.

Enkey-arbetskopian är ren. Skills befintliga ändringar (bland annat frågedokument,
automation, milesight och ospårade underlag) och neptune-marketing/dist-undantagen
har inventerats med filhashar och bevaras. Inga remoteoperationer har utförts:
detta är en lokal rättningsgranskning, inget intyg om aktuell remote-HEAD eller
publicerbarhet. Batch 7:s befintliga publicerings-/historikspärr påverkas inte.

## Oberoende verifiering

- Exakt 86 oförändrade tariff-ID:n. Energy/capacity/production_ready/
  contract_required/price_status/investigation.status oförändrade mot HEAD:s
  förälder på samtliga rader. Endast de tre dokumenterade tariffradernas
  villkorsmetadata ändras.
- §8a:s 28 unika identiteter motsvarar exakt de blockerade identiteterna från
  befintlig parser för den frusna §3–5-mängden; 22 källösta + 6 externa.
  Dispositionen är fortsatt 62 implemented / 2 ready / 28 blocked av 92.
- Fysiska öppna frågor: R02/R03/R08/R16. De blockerar exakt HEMAB, Mälarenergi
  gruppanslutna småhus, Hässleholm/Tyringe och Gävle. R17 är fortsatt olöst och
  separat spårad för Finspångs ej materialiserade tillägg. Ingen basrad spärras
  av variantfrågan. Kataloggrinden returnerar 61 godkända fysiska rader.
- Fyra tidigare körda testfiler (test_katalog, test_katalog_oversattning,
  test_katalog_proveniens, test_dispositionsgrind_inventering): **51 passed,
  2 failed**. Felen är precis den gamla Vattenfall-assertionen och låst kataloghash.
- Kompletterande test_synk.py: **1 passed, 1 failed**. Felet är samma kataloghash
  i tariffer.generated.ts:s proveniensrad. Sammanlagt **52 passed / 3 failed**,
  två rotorsaker. Ingen full grön regression hävdas.
- Befintlig bygg_ts_fran_katalog körd utan filskrivning med aktuell katalog och
  leverantörsfiler: genererad kropp är identisk med incheckad TS efter att endast
  GENERERAD-raden och Källkatalog-proveniensraden undantagits. Det motiverar en ren
  provenienssynk; inga pris-/produktändringar behövs.
- git diff --check HEAD^ HEAD rent. Ett första ad hoc-jämförelseprov behövde
  hantera investigation=null; omkörningen ovan lyckades. Detta var ett fel i
  granskningsskriptet, inte ett produktfel.

Aktuell katalog-SHA-256:
`0aa1e82fcb92befe506162f242941e07e9d0d06752ab4d88edf5376e1b54d03a`.

## Nästa handlingsbara signal: CHANGES_REQUIRED: Claude

Codex beslutar nu om det separata synksteg som granskning 003 krävde. Det ryms i
befintligt uppdrag att normalisera käll-/blockeringsläget; inget nytt Robert-beslut
behövs. Föregående skills-only-runda avslutas med godtagna sakrättningar. Endast
följande lokala följdrättning godkänns:

1. Verifiera att denna nya signal är unik och överst, skills har denna
   granskningscommit direkt efter reviewed_heads.skills, samt att produkt-HEAD:ar
   och arbetskopieundantag är oförändrade. Stoppa fail-closed vid avvikelse.
2. I enkey-agents: uppdatera endast kataloghashen och dess daterade förklaring i
   tools/tariffer/tests/test_katalog_proveniens.py samt den inaktuella
   Vattenfall-förväntan i tools/tariffer/tests/test_katalog.py. Behåll kontrollen
   att öppna frågor verkligen spärrar avsedda rader; verifiera att Vattenfall
   fortfarande spärras av investigation.status trots löst R09. Försvaga inga
   grindar och ändra ingen motor, generator eller policy.
3. I neptune_academy: regenerera endast
   neptune-marketing/src/data/tariffer.generated.ts med befintlig generator och
   explicit granskad katalogproveniens (skills@2a0e0ed037db6a66b5e62104a3d28b391165dacf,
   SHA-256 ovan). Endast proveniens/GENERERAD får skilja; vid annan kroppsdiff:
   stoppa och skriv BLOCKED: Codex med konkret diff. Ingen handredigering av TS.
4. Kör de fem testfilerna ovan, full relevant tariffsvit och befintliga TS-tester/
   typkontroll. Redovisa faktiska utfall, 86/61/63 samt 62/2/28, identitetsbevis
   och byte-identisk genererad kropp. Ändra inte tester utanför fillistan för att
   dölja eventuella andra fel; lämna i så fall en handlingsbar blockerare.
5. Committa enbart dessa avgränsade synkfiler i respektive produktrepo och loggar
   i conversations/. Skriv ny unik REVIEW_READY: Codex med slutliga HEAD:ar och
   testutfall och stanna. Redovisa denna rundas diff separat från äldre opushade
   Batch 7-commits; inget i deras historia eller leverantörsmetadata får ändras.

Ingen Vattenfall-produktimplementation, tariffaktivering, leverantörsmetadatasynk,
push, historikomskrivning, protokolländring eller automationsändring ingår.
Publiceringskedjan förblir stoppad även om synkstegens tester blir gröna.
