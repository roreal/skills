---
session_id: "2026-09-21-003"
started_at: "2026-09-21T15:58:09+02:00"
last_updated: "2026-09-21T16:08:49+02:00"
timezone: "Europe/Stockholm"
participants:
  - Robert
  - Codex
status: locally-verified-not-pushed
topics:
  - Stockholm Exergi
  - Optimate
  - besparingspotential
source: visible-conversation
transcript_fidelity: summarized
---

# Stockholm Exergi: preliminär Optimate-potential

## Roberts önskemål

> Nästa steg blir att uppskatta besparingspotentialen med Optimate. Optimate sparar mellan 15-25% av årsvärmen på värmesystem såsom radiatorer, golvvärme, konvektorer. Vidare finns potential att sänka toppeffekten med uppskattat ca 20%.

> Bygg vidare på en version som presenterar besparingspotential.

## Lokal leverans

En separat, preliminär scenariovy visas under Stockholm Exergis uppskattade
årskostnad. Den räknar om samma 2026-tariff för 15, 20 och 25 procent lägre
styrbar rumsvärme och visar uppskattad kostnadsskillnad per år, sparade MWh
och årskostnad efter. Om användaren har angett rumsvärme per månad används
den serien. Vid bara totalvärme skattas rumsvärmen utifrån en jämn
18-procentig tappvarmvattenbaslast och märks som uppskattad. Baslasten
minskas inte. Rättningen av månadsfältens energiomfattning från föregående
session ingår i samma opushade arbetskopia.

Huvudscenarierna håller debiterbar effekt, returtemperatur och skattad
kölddygnsvolym oförändrade. En separat hopfälld känslighetsanalys visar vad
20 procent lägre **debiterbar** kW skulle betyda om Stockholm Exergi senare
fastställer det; den läggs inte till i huvudtalen. Minskad fysisk toppeffekt
är inte automatiskt minskad fakturerad effekt. Energi- och effektandelarna
är Roberts antaganden, inte uppmätta/garanterade resultat. Bevarad
inomhuskomfort måste kontrolleras separat. Beloppen visas inklusive moms.

Tariffens befintliga `stodjer_besparing=false` är oförändrad: vyn är en
utforskande kalkyl, inte en ny godkänd kontraktsstyrd besparingsprodukt.
Inga andra leverantörer aktiveras. Metod och begränsningar är tillagda i
`Fjarrvarmetariffer/stockholm-exergi-schablonunderlag-2026.md`.

## Verifiering och nästa steg

- 2 270/2 270 TypeScript-test gröna i 68 testfiler; `tsc` och isolerat
  `dist-eval`-bygge gröna; hela Chromium-E2E 1–29 grön. Scenario 26
  kontrollerar både totalvärme och ren rumsvärme, scenariotexter,
  effektreservationer och mobilbredd utan horisontell overflow.
- `git diff --check` rent i Neptune och skills. Spårad `dist/` är orörd.
  Lokal förhandsvisning startad på `http://127.0.0.1:4174/kalkylator`.
- Ingen commit, push eller tariffaktivering gjord. Övriga arbetskopieändringar
  bevarade.
- För en verifierad besparingsprognos behövs byggnadens uppmätta
  rumsvärmeandel, dygns-/effektdata, en faktisk omräkning av debiterbar
  effekt och kontroll av komfortkravet (exempelvis 22 °C inomhus).

## Paus 2026-09-21 16:08

Robert vill stoppa här tills vidare. Förhandsvisningen på port 4174 har
stoppats. Inga ytterligare produktändringar, commits eller pushar görs nu.
Exakt Git-scope och återstartskontroll finns i
`conversations/handoffs/2026/09/2026-09-21-paus-stockholm-optimate.md`.
