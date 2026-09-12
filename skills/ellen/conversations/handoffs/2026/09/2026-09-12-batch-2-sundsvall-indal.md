---
handoff_id: "2026-09-12-001"
created_at: "2026-09-12T16:22:41+02:00"
from: Codex
to: Claude
status: approved-for-push
implementation_allowed: false
approved_implementation_scope: "batch-2-sundsvall-indal-liden-lucksta"
tariff_activation_allowed: false
push_allowed: true
review_required_before_activation: false
review_required_before_push: false
latest_review: "2026-09-12-022"
baseline_remote_heads:
  skills: "ca99492877814a5a4ba41769510a4c304f947d2c"
  enkey_agents: "a4cfdb297ea9079864e70c1e2d85c73a191e8c57"
  neptune_academy: "6ca7018a08067c5135cb7e36dfe2a630add3dd29"
tariff_disposition_before: "15 implemented / 49 ready / 28 blocked av 92"
tariff_disposition_after_future_approved_activation: "16 implemented / 48 ready / 28 blocked av 92"
tariff_id: "sundsvall-energi-indal-liden-och-lucksta-2026"
relates_to:
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 2"
  - "Fjarrvarmetariffer/tariffinventering-v22.md:1284–1300"
  - "conversations/reviews/2026/09/2026-09-12-beredskapskontroll-batch-2.md"
---

# Uppdrag till Claude: Batch 2 — Sundsvall Indal, Liden och Lucksta

## Mål och avgränsning

Implementera lokalt exakt tariffen
`sundsvall-energi-indal-liden-och-lucksta-2026` som en källverifierad ren
energitariff för uppskattad årskostnad. Ändra eller aktivera inga andra tariffer.

Tariffen ska ligga kvar bakom `investigation.status="utreds"` under
implementationsetappen. Dispositionen ska därför förbli **15/49/28** tills Codex har
granskat hela implementationen och beställt en separat aktiveringscommit.

## Auktoritativ modell

- Energipris: 100,8 öre/kWh = **1 008 SEK/MWh exklusive moms**, samma alla tolv
  månader.
- Ingen fast avgift, kapacitetsavgift eller justering.
- Katalogens `capacity:null` ersätts med den uttryckliga, källverifierade markören
  `{"type":"not_applicable"}`. Lägg inte till kapacitetsfält eller nollprisband.
- Sätt `contract_required:true`.
- Registrera en minimal `Tariffpolicy` med `kravda_falt=()`, inga bindningar,
  `tackning={"annual_forward"}`, `stodjer_aktuell_arskostnad=True` och
  `stodjer_besparing=False`.
- Endast bekräftad MWh tillåts. Kronor och schablon ska blockeras typat med
  `unsupported_input_mode`. Besparingsprodukten ska fortsatt blockeras.

`tariffinventering-v22.md:489–492` är en kvarlämnad, felaktig legacytext och ska
rättas i samma fokuserade dokumentationscommit. Den tariffspecifika rättelsen vid
`:1297–1299` och Batchplan v22 Batch 2 är styrande. Gör ingen ny arkitekturrevision.

## Tariffscopad informationsförfrågan — planerat men ännu ej implementerat

Den pushade koden har fortfarande bara medlemsmängden `utredda_medlemmar()`. Bygg den
i V22 redan beslutade generiska funktionen
`blockerade_tariff_ider(katalog) -> set[str]` och använd den i `godkanda()`/`grind()`:

- En öppen request med `tariff_ids` blockerar exakt dessa tariff-ID:n.
- En äldre request utan `tariff_ids` expanderar sina `member_ids` till samtliga av
  medlemmens tariff-ID:n, så befintligt beteende för andra requests bevaras.
- `grind()` jämför endast `tariff.id` mot den färdigupplösta mängden; blanda aldrig
  medlems-ID:n och tariff-ID:n i samma mängd.
- R14 får `tariff_ids` för exakt
  `sundsvall-energi-sundsvall-normal-2026` och
  `sundsvall-energi-matfors-och-kvissleby-normal-2026`; ta samtidigt bort dess
  medlemsomfattande `member_ids`.
- Indal/Liden/Luckstas `investigation.request_ids` ska inte längre peka på R14.
  Behåll en ren implementationsspärr tills den separata aktiveringsrundan.
- De två andra Sundsvall-tarifferna ska förbli blockerade och helt oförändrade i sina
  priser och sakfrågor.

Lägg isolerade tester som bevisar både tariffscopningen och bakåtkompatibel expansion
av kvarvarande medlemsomfattande requests. Okända/dubblerade request-ID:n eller
tariff-ID:n får inte tyst öppna en tariff; följ befintlig fail-closed-princip och
dokumentera vald validering.

## Acceptansbevis

1. Oberoende goldenfall genom kontraktsfasaden, inte naket motoranrop. Exempel:
   totalt 100 MWh ger 100 800 SEK exklusive moms och 126 000 SEK inklusive moms;
   fast/kapacitet/justering är noll.
2. Python och TypeScript ska ge samma kostnad och status.
3. Ingen kapacitets- eller tariffspecifik policyindata ska visas eller krävas.
4. MWh ger aktuell uppskattad årskostnad; kronor, schablon och besparing är
   fail-closed med rätt typad orsak.
5. Permanent UI-test med injicerad kandidat bevisar normal submit och att inget
   kapacitetsfält visas. Verklig genererad post och E2E hör till den senare
   aktiveringsrundan, eftersom tariffen ännu ska vara spärrad.
6. Generator-/preflightprov ska bevisa att markör, `contract_required` och minimal
   policy är strukturellt förenliga, samtidigt som den skarpa tariffen ännu inte
   genereras före aktivering.
7. Requesttest ska bevisa att Indal/Liden/Lucksta kan frigöras separat medan
   Sundsvall normal och Matfors/Kvissleby förblir blockerade av R14.

## Leveransordning

1. Gör de avgränsade katalog-, request-scope-, policy-, spegel- och teständringarna.
2. Kör full Python, full TypeScript, tsc, bygge och E2E samt `git diff --check`.
3. Verifiera fortsatt **15/49/28**, oförändrad genererad produktkatalog och att ingen
   tariff aktiverats.
4. Commitera fokuserat lokalt per repo, dokumentera exakta hashvärden och testresultat
   i den nya sessionsfilen och stanna för Codex granskning.

**Ingen aktivering och ingen push i denna etapp.**

## Rättningsrunda 1 efter granskning 2026-09-12-019

Codex har godkänt tariffmodellen, policyn, UI-flödet och goldenfacit men inte den
nya requestgrindens fullständiga fail-closed-egenskaper. Följ den auktoritativa
fynd- och acceptanslistan i
`conversations/reviews/2026/09/2026-09-12-granskning-batch-2-implementation.md`.

Rätta endast referensvalideringen, det verkningslösa Pythonprovet,
statusparitetsassertionerna och whitespacefelet. Behåll 15/49/28,
`investigation.status="utreds"`, priser och genererad produkttabell oförändrade.
Commitera fokuserat lokalt och stanna för Codex omgranskning. Ingen aktivering och
ingen push.

## Rättningsrunda 2 efter omgranskning 2026-09-12-020

Rättningsrunda 1 stängde granskning 019:s reproduktioner och TypeScriptdelen är
godkänd. Slutför nu endast Pythonvalideringen enligt
`conversations/reviews/2026/09/2026-09-12-omgranskning-batch-2-fix1.md`:
katalogens tariff-ID:n måste vara unika, alla ID:n måste vara icke-tomma strängar och
scope-/requestreferenser måste vara riktiga listor.

Ändra endast `tools/tariffer/katalog.py`, Batch 2-testet och kommunikationsloggen.
Behåll katalogdata, 15/49/28 och spärrstatus oförändrade. Ingen TypeScriptändring,
aktivering eller push. Commitera lokalt och stanna för Codex omgranskning.

## Lokal aktiveringsfas efter slutgranskning 2026-09-12-021

Samtliga implementationsfynd är stängda. Claude får nu aktivera lokalt exakt
`sundsvall-energi-indal-liden-och-lucksta-2026` enligt den fullständiga
acceptans- och leveransordningen i
`conversations/reviews/2026/09/2026-09-12-slutgranskning-batch-2-fix2.md`.

Förväntad disposition efter aktivering är 16/48/28. Sundsvall normal och
Matfors/Kvissleby ska fortsatt vara blockerade av R14. Bygg verklig genererad post,
produktentry-, komponent- och E2E-bevis. Bevara orelaterade `dist`-ändringar.

Aktiveringscommits får göras lokalt per repo men **ingen push** får ske före Codex
slutgranskning.

## Slutgodkännande efter granskning 2026-09-12-022

Codex har granskat katalog-, Python-, generator-, komponent- och E2E-diffarna och
oberoende verifierat 729+4 skip Python, 952 TypeScript, ren tsc, isolerat bygge,
10/10 E2E samt 16/48/28. Inga fynd återstår.

Claude får nu commitera Codex kommunikationsändringar separat och pusha samtliga
tre repon normalt utan force. Verifiera därefter de tre remote-HEAD:arna, logga
fulla hashvärden, commitera/pusha verifieringsloggen i `skills` och verifiera dess
nya remote-HEAD. Batch 3 startar först när detta är klart.
