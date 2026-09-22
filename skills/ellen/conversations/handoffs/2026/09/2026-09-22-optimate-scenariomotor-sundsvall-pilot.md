---
handoff_id: "2026-09-22-007"
created_at: "2026-09-22T13:42:30+02:00"
from: Codex
to: Claude
status: "APPROVED_FOR_IMPLEMENTATION: Claude"
approved_by: Codex
requested_by: Robert
skills_local_head_before_signal: "fd23ba74f2a9073976dd6990af3d0fc9d8aefaeb"
neptune_local_head: "86be35ae4c5e3f021c97c40d0473ab3d3427b127"
enkey_local_head_untouched: "2e30bb200d1831b8ca7461f67e0d958870ba6867"
activation_allowed: false
push_allowed: false
---

# Uppdrag till Claude: gemensam scenariomotor, Sundsvall som första pilot

Robert har godkänt att Claude startar nästa avgränsade etapp. Läs först
[genomförandeplanen](../../../proposals/2026/09/2026-09-22-besparingspotential-alla-godkanda-tariffer.md),
[arkitekturgranskningen](../../../reviews/2026/09/2026-09-22-arkitekturgranskning-besparingspotential-etapp-0.md)
och [75-radersmatrisen](../../../../Fjarrvarmetariffer/besparingspotential-tackningsmatris-2026.md).
Matrisen är inventering, inte ett godkännande av nya efter-scenarier.

## Nuläge och gränser

- Neptune `main@86be35a` innehåller en separat lokal Stockholm-prototyp.
  Den har `stodjer_besparing=false` och får fortsätta vara separerad från
  den formella besparingsprodukten. Neptune-arbetskopian var ren vid
  överlämningen; lokala `main` ligger före `origin/main`, så **ingen push**.
- Skills `main@fd23ba7` innehåller matris, metod och logg. Arbetskopian
  har redan orelaterade ändringar i bl.a. `conversations/automation/`,
  leverantörsfrågorna och `skills/milesight` samt ospårade underlag.
  Bevara dem. Ändra inte bryggans script eller protokoll i detta uppdrag.
- Enkey `main@2e30bb2` har orelaterad Milesight-historik och är inte
  del av scenariomotoruppdraget. Ändra, mergea, rebasea eller pusha inte
  det repot. Gör ingen kataloggenerering eller tariffaktivering.
- Ett 2026-produktval är inte nödvändigtvis ett bolag. Nuvarande mål är
  74 verkliga val samt separat syntetiskt riksgenomsnitt; denna etapp är
  endast infrastrukturen och en **spärrad** pilot, inte portföljutrullningen.

## Implementera inom detta scope

1. Bygg en liten typad, tariffneutral före/efter-kärna i Neptune. Indata
   ska skilja tolv värden köpt fjärrvärme, tolv värden styrbar rumsvärme,
   övrig last/proveniens, tariffversion, kundens aktuella policyunderlag
   och historiskt faktureringstillstånd. Validera månadsserier, enheter,
   summor, icke-negativitet och scenarioandelar. Ett saknat värde får
   blockera/markeras, inte tyst bli noll.
2. Beräkna referens och energiscenario med **samma befintliga tariffmotor**,
   prisår, momsgrund och tariffprodukt. Exponera nödvändiga kostnadsled
   från domänlagret så resultatet kan ange energi, fast/kapacitet,
   retur/flöde/justeringar och total. Kopiera inte prisformler till UI.
   Visa kostnadsskillnad även när den är noll eller negativ.
3. Håll historisk/debiterbar effekt, kontraktsband, flöde, temperatur,
   kölddygnsserie och behörighet oförändrade i **huvudscenariot**, med
   tydlig metadata om detta antagande. En fysisk effektförändring eller
   20 procent lägre topp får inte automatiskt bli lägre faktura.
   Använd inte Stockholms kundexempel på 18 procent tappvarmvatten som
   generell standard. Fortsätt skilja preliminärt scenario från uppmätt
   eller garanterad Optimate-besparing och från bevarat komfortkrav.
4. Pilotera enbart `sundsvall-energi-indal-liden-och-lucksta` bakom en
   separat, initialt avstängd scenarioförmåga/testgrind. Ingen ny synlig
   produktionseffekt eller bred flaggändring. Om kostnadsmotorn inte
   kan ge spårbara prisled inom rimlig avgränsning, stoppa och logga
   det konkreta arkitekturbeslut som behövs; skapa ingen parallell motor.

## Acceptans och överlämning

- Testa 15/20/25 procent av **styrbar rumsvärme**, oförändrad övrig
  last, noll sommarrumsvärme, ogiltig/negativ/otillräcklig serie och
  oförändrad debiterbar effekt. Referensens årskostnad ska vara exakt
  samma som `beraknaArsprodukt` för samma underlag. Års- och
  månadsprisled ska summera, och ingen dold kapacitets-, flödes- eller
  temperaturbonus får uppstå. Lägg regressionsprov för Stockholm och
  säkerställ att Vattenfalls specialprofil/behörighet inte tyst går
  genom ett generiskt månadsserieflöde.
- Kör relevanta TypeScript-/bygg-/E2E-test och matrisens `--check`.
  Dokumentera faktiskt utfall, avvikelser och vilka prisled som ännu
  saknar verifierat eftervärde. Ingen kundfaktura behövs som generellt
  krav; använd publicerat eller oberoende handräknat årsreferensfacit
  där det passar piloten.
- Gör avgränsade **lokala commits**. Skriv i `conversations/sessions/`
  och en ny, globalt unik toppost i `conversations/index.md` märkt
  `REVIEW_READY: Codex`, med exakta Neptune-/skills-HEAD:ar och tester.
  Om ett verkligt tekniskt vägval blockerar arbetet, använd i stället
  `BLOCKED: Codex` med alternativ. Ingen tariff-/scenarioaktivering,
  inget pushsteg, ingen force-push och inga orelaterade filer.
