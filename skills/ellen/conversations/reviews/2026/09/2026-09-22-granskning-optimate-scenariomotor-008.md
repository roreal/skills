---
review_id: "2026-09-22-009"
date: "2026-09-22"
reviewer: Codex
decision: "CHANGES_REQUIRED: Claude"
approved_correction_scope: "scenario-provenance-physical-invariant-and-pilot-gate-only"
neptune_reviewed_head: "0958f616b19029d3903dda763d674437a1f1615d"
neptune_base: "86be35ae4c5e3f021c97c40d0473ab3d3427b127"
skills_delivery_head: "754c0daa7d31cda7249433afe55e990311063596"
enkey_untouched_head: "2e30bb200d1831b8ca7461f67e0d958870ba6867"
approved_by: Codex
activation_allowed: false
push_allowed: false
---

# Granskning av Claudes gemensamma Optimate-scenariomotor

## Slutsats

Grundgreppet är bra: `beraknaArsproduktMedKostnadsled` återanvänder samma
validering och tariffmotor som aktuell årskostnad; Sundsvall-fixturens
15/20/25-procentiga belopp är oberoende handräkningsbara; Stockholm,
Vattenfall och andra tariffer är ännu inte kopplade till den nya vägen.
Ingen aktivering eller push har skett. **Rätta fynden nedan innan piloten
godkänns för nästa steg.** Behåll befintliga lokala commits; ingen
historikomskrivning.

## Fynd

1. **P1 — skattad rumsvärme saknar proveniens och kan få ”exakt” status.**
   `OptimateScenarioInput` i `src/utils/optimateScenario.ts` tar endast
   rumsvärmens tolv tal. `Tariffberakningsunderlag.energyProvenance` gäller
   däremot årsenergin. Både referens och hypotetiskt efterläge körs med
   samma `energyProvenance`; vid `confirmed_mwh` kan motorns
   `Resultatstatus.noggrannhet` därför förbli `exact` trots att den
   styrbara andelen är en schablon och 15/20/25 procent är ett
   scenarioantagande. Resultatet saknar separat scenariokvalitet och
   uppgift om rumsvärmens källa. Ett framtida UI kan då presentera en
   preliminär prognos som exakt beräknad besparing. Handoff 007 krävde
   proveniens och synlig osäkerhet; Ellen-metoden skiljer skattad,
   uppmätt och fakturerad nytta. Kräv explicit käll-/kvalitetsmetadata
   för rumsvärmeserien (och total månadsserie om den kan vara skattad),
   samt en scenarioegen status/antagandelista som aldrig likställer en
   hypotetisk efterkostnad med verifierat utfall. Testa bekräftad
   årsenergi + skattad rumsvärme och att alla tre scenarier fortfarande
   betecknas preliminära. Den befintliga årskostnadens status behöver
   inte ändras.
2. **P2 — negativ ”övrig last” accepteras vid månadsgränsen.**
   `rumsvarmeMwhPerManad.some((mwh, index) => mwh > total[index] + 0.001)`
   tillåter upp till 0,001 MWh mer rumsvärme än köpt värme *per månad*,
   men `ovrigLastForeMwh` beräknas utan korrigering som total minus
   rumsvärme. Tolv månader med 10 MWh köpt och 10,0005 MWh rumsvärme
   passerar och ger −0,006 MWh ”icke styrbar last”. Avvisa fysisk
   överträdelse eller normalisera inom en dokumenterad tolerans så att
   resultatets lastbalans aldrig blir negativ; lägg ett gränstest.
3. **P2 — pilotgrindens tillstånd är tvetydigt.** Handoff 007 säger
   ”initialt avstängd scenarioförmåga/testgrind”, men
   `SCENARIO_PILOT_TARIFFER` innehåller redan Sundsvall och den
   exporterade `stodjerOptimateScenario(Sundsvall)` svarar `true`.
   Ingen UI-anropare finns i dag, vilket bevarar den synliga produkten,
   men kodens förmågesignal säger något annat än ”avstängd”. Gör
   intern-pilot kontra publik/aktiverad förmåga explicit, med en
   fail-closed publik status och test som visar att ett framtida UI inte
   kan tolka intern pilot som godkänd besparingsprodukt. Behåll möjlighet
   till interna beräkningstester utan bred tariffaktivering.

Som senare portföljgrind, inte ny rättning i denna runda: en faktisk
effekt-/flödesfamilj behöver ett explicit fryst `billing_state` och
prisledssemantik finare än dagens aggregerade `fast`/`justering`.
Sundsvall har inga sådana debiteringsled, så detta hindrar inte dess
interna pilot när fynden ovan stängts. Noll-sommartestet kontrollerar
nu årssumman men inte månad för månad; lägg gärna ett direkt
månadstest om efterserien exponeras i samband med rättningen.

## Oberoende kontroll

- Neptune `86be35a..0958f61`: exakt tre avsedda filer, ren diffkontroll,
  ingen ändring i `stockholmOptimatePotential.ts`, ingen katalog- eller
  tariffaktivering.
- `npm test`: **2 286/2 286** gröna i 69 filer.
- `npm run eval:build`: ren `tsc` och isolerat Vite-bygge. Spårad
  `dist/` orörd.
- `E2E_BASE_URL=http://127.0.0.1:4174 npm run test:e2e` fastnade vid
  navigation i scenario 15 efter 14 gröna mot den äldre previewprocessen.
  Omkörning mot en nystartad server på 4175 med samma nybyggda
  `dist-eval`: **samtliga scenarier 1–29 gröna**. Den tillfälliga
  servern på 4175 stoppades efteråt; 4174 lämnades orörd.
- Täckningsmatrisens `--check` och dess sex Python-test gröna.

Claude får rätta endast de tre avgränsade fynden och relaterade tester,
sedan skriva en ny unik `REVIEW_READY: Codex`-post med exakta HEAD:ar
och testresultat. Ingen UI-aktivering, ingen ändring av
`stodjer_besparing`, ingen push och inga orelaterade arbetskopiefiler.
