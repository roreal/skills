---
handoff_id: "2026-09-16-002"
created_at: "2026-09-16T20:28:57+02:00"
from: Codex
to: Claude
status: ready-for-implementation
approved_by: Robert
implementation_directed_by: Codex
executed_by: null
dispatched_by: agent-bridge
dispatch_via: agent-bridge
implementation_allowed: true
approved_implementation_scope: "batch-7-stockholm-exergi-annual-forward-adapter-and-sanitized-invoice-regression"
tariff_activation_allowed: false
push_allowed: false
review_required_before_activation: true
review_required_before_push: true
required_parent_heads:
  skills: "0df504ed227126b5fd36f87f99b4e240001a99d5"
  enkey_agents: "9b5125dbb6f2b8188cf880a0619c841b4c10f001"
  neptune_academy: "22b473d30980051fb87a936b3d824c53b63d58e8"
baseline_remote_heads:
  skills: "0df504ed227126b5fd36f87f99b4e240001a99d5"
  enkey_agents: "9b5125dbb6f2b8188cf880a0619c841b4c10f001"
  neptune_academy: "22b473d30980051fb87a936b3d824c53b63d58e8"
tariff_disposition_before: "62 implemented / 2 ready / 28 blocked av 92"
tariff_disposition_during_implementation: "62 implemented / 2 ready / 28 blocked av 92"
tariff_disposition_after_future_activation: "63 implemented / 1 ready / 28 blocked av 92"
sharp_catalog_rows_before: 61
sharp_catalog_rows_after_future_activation: 61
sharp_products_before: 63
sharp_products_after_future_activation: 63
relates_to:
  - "conversations/reviews/2026/09/2026-09-16-beredskapskontroll-batch-7-stockholm-exergi.md"
  - "conversations/sessions/2026/09/2026-09-16-batch-7-stockholm-exergi.md"
  - "Fjarrvarmetariffer/batchplan-v22.md — Batch 7"
  - "Fjarrvarmetariffer/tariffinventering-v22.md §6a.4"
---

# Uppdrag till Claude: Batch 7 — Stockholm Exergis årsprodukt

## Mandat och stoppunkt

Robert har godkänt att Batch 7 implementeras nu. Läs beredskapskontroll
`2026-09-16-033` fullständigt; den är bindande för scope, kundintegritet,
adapterkontrakt, testmatris, räkningsgrind och arbetskopieundantag.

Implementera lokalt bakom spärr. **Aktivera inte katalograden, rensa inte
dess `investigation`, pusha inte och ändra inte brygginfrastrukturen.**
Avsluta med `REVIEW_READY: Codex` och stanna.

## Leveransens kärna

1. Utöka den befintliga policyn för leverantörsfilsprodukten
   `stockholm-exergi-2026` från enbart `monthly_invoice` till även
   `annual_forward`; skapa ingen dubblettpolicy och inget nytt produkt-ID.
2. Lägg exakt två årsserier: 12 kallenergimånader och fem
   vinterreturtemperaturer Nov–Mar. Bredda samma effektkrav till månad och
   år. Använd de redan införda statiska bindningarna.
3. Sätt `stodjer_aktuell_arskostnad=True`, `stodjer_besparing=False` och
   den explicita ersättningsmarkören för katalograden.
4. Implementera det typade, injicerbara och bijektiva
   `ADAPTERREGISTER`-preflightkontraktet exakt enligt Batch 7-planen:
   full tvåvägskontroll med rå katalog i `bygg_ts_fran_katalog()`, enbart
   reverse-led med `rak_katalog=None` i `bygg_ts()`.
5. Sätt `_kraver_kontrakt` på den befintliga leverantörsfilsprisposten när
   årstäckningen finns. Skapa exakt ett Stockholm-val i den genererade
   datan och UI:t.
6. Återanvänd den befintliga produktentryn för uppskattad aktuell
   årskostnad. Besparing, kronor och schablon ska fortsätta blockeras
   typat; Sandviken och övriga äldre produkter ska vara regressionstäckta.

## Två separata databevis

- Skapa en permanent, anonymiserad **fakturaregressionsfixtur** i båda
  produktrepona från de godkända sanitiserade uppgifterna i
  `2026-09-09-008` och `2026-09-09-009`. Behåll den frysta
  maj-2025–april-2026-fixturen orörd. Behandla maj–juli 2026 som en
  avräkningskedja och augusti som ett nytt out-of-sample-fall.
- Skapa separat ett **oberoende handräknat årsreferensfall** för
  `annual_forward`. Det ska vara källverifierat mot 2026-prislistan men
  får inte framställas som Åkermannens faktiska 2026-helår, eftersom
  fakturor för september–december saknas. Förväntat värde får inte
  genereras av produktionsmotorn.

Råfakturor och kundidentifierare får aldrig lämna SynologyDrive eller
hamna i repo/logg. Leverantörsmetadata får korrigeras till 20 unika
perioder/22 PDF-filer till augusti först efter att den anonymiserade
fixturen passerar i båda motorerna.

## Kontroll och redovisning

Kör hela acceptansmatrisen i beredskapskontrollen, inklusive 11/13- och
4/6-seriefel, samtliga adapterfelvägar, två injicerade register,
månadsvägsregression, publik produktentry, React, ordinarie och isolerad
browser-E2E, fulla språkssviter, typkontroll, bygge och diffkontroll.

Under implementationen ska skarpt läge förbli 62/2/28, 61 godkända
katalograder och 63 produkter. Den isolerade projektionen ska ge 63/1/28,
61 katalograder och fortfarande exakt 63 produkter. Katalograden för
Stockholm ska förbli spärrad även i framtida aktiveringssteget; det är
leverantörsfilsproduktens årsförmåga och dispositionsbokföring som senare
aktiveras.

Commitera fokuserat i varje repo. Bevara de dokumenterade, orelaterade
`skills`- och `neptune-marketing/dist/`-ändringarna ostagade. Skriv sedan
en ny unik indexpost med:

`REVIEW_READY: Codex`

och sammanfatta:

> Batch 7 är implementerad bakom spärr. Stockholms katalograd är fortsatt
> spärrad; exakt en leverantörsfilsprodukt finns kvar. Ingen aktivering och
> ingen push har utförts. approved_by: Robert; implementation_directed_by:
> Codex; executed_by: Claude; dispatched_by: agent-bridge. Väntar på Codex
> kodgranskning.
