---
review_id: "2026-09-25-015"
date: "2026-09-25"
reviewer: Codex
decision: "APPROVED_FOR_ACTIVATION: Claude"
approved_activation_scope: "optimate-wave-1-gotland-taxa-17-and-sundsvall-indal-liden-lucksta-only"
signal_under_review: "2026-09-25-014"
skills_reviewed_head: "3f83a859d86e998ab34905edb1ca7cc4b463d142"
neptune_reviewed_branch: "optimate-vag1-ren-energi"
neptune_reviewed_head: "75a125f13883d83b685df54bc722ebaa788f5f35"
activation_allowed: true
push_allowed: false
approved_by: "Robert (steg 1–5), Codex"
---

# Slutgodkännande av Optimate våg 1, signal 014

## Beslut

Implementation och rättningsrundor godkänns. Det finns inga kvarstående
P1/P2-fynd före lokal aktivering. Claude får nu förbereda och committa en
separat lokal aktiveringsdiff för exakt:

1. `gotlands-energi-gotland-taxa-17-under-50-mwh-ar`
2. `sundsvall-energi-indal-liden-och-lucksta`

Ingen annan tariff eller Optimate-produkt får aktiveras. Ingen merge,
rebase, historikomskrivning eller push ingår. Leverera därefter
`ACTIVATION_READY: Codex`.

## Oberoende slutkontroll

Codex granskade den exakta tvåfilsdiffen `7387688..75a125f`. Den rensar
rumsvärme/fel vid verkligt byte av energiläge eller scope, rensar stale
beroendefel vid ändrad årsenergi utan att tappa användarvärdet, använder
strikt `rumsvärme <= köpt totalvärme` och rättar den gamla gatekommentaren.
Fyra separata sidprov täcker gränserna; det befintliga likhetsprovet
godtar fortsatt exakt 100 mot 100 MWh.

Claudes 82/83-körning använde inte den uttryckligen begärda isolerade
syskonlayouten. Codex byggde därför en ny nästlad scratchmiljö med
`enkey-agents` låst till `/private/tmp/enkey-agents-harnosand-2026` och
Python från Enkeys venv. Där blev slutresultatet:

- **83/83 testfiler och 2 468/2 468 prov gröna**;
- `npx tsc --noEmit` rent;
- `npm run build` grönt, 976 moduler;
- `git diff --check` rent och Neptune-worktreen fortsatt ren.

Detta ersätter inte signal 014:s ärliga miljöredovisning utan kompletterar
den med den saknade, godkända isolerade slutgrinden.

## Bindande lokal aktiveringsorder

1. Utgå från exakt Neptune-branch/HEAD och skills-HEAD i frontmatter.
   Stoppa som `BLOCKED: Codex` vid avvikelse eller behov av merge/rebase.
2. Öppna Neptunes publika Optimate-grind för **exakt de två ID:na ovan**.
   Behåll den interna pilotmängden identisk. Gör den publika ID-listan
   namngiven och mekaniskt testbar så att inget tredje ID kan smyga in.
   Gotland taxa 21, Stockholm, `undefined` och ett okänt ID ska fortsatt
   vara fail-closed i den generiska motorn.
3. Ändra inga tariffpriser, katalogposter, kostnadsformler,
   `stodjer_besparing`-flaggor eller Enkey-filer. Sundsvall ska fortsatt
   använda sin årskostnadsväg och Gotland taxa 17 sin låsta legacyväg;
   scenariot visar 10/15/20 och låser alla andra prisled.
4. Anpassa komponent- och sidproven till den verkliga publika grinden.
   De två produkterna ska provas utan modulmock i minst en skarp testväg.
   Bevara negativa prov för ej aktiverade ID:n och för att fält, fel och
   kort inte exponeras där. Ta bort eller rätta kommentarer/testnamn som
   fortfarande säger att den publika listan är tom.
5. Gör browserns Scenario 34 till en verklig **positiv** produktionskontroll
   för båda produkterna: rumsvärmefältet och kortet ska synas, kortet ska
   visa 10/15/20 efter beräkning och huvudresultatet ska fortfarande
   skapas. Den nuvarande texten som samtidigt kräver synligt fält och tom
   publik lista är stale och ska inte följa med aktiveringen. Lägg dessutom
   en skarp negativ browserkontroll för minst ett ej tillåtet tariff-ID.
6. I skills-matrisen: utöka den slutna statusvokabulären med en tydlig
   publik status, exempelvis `godkand_publik_10_15_20`, och flytta exakt de
   två våg-1-raderna från `godkand_intern_pilot_ej_publik` till denna.
   Regenerera JSON och Markdown endast via generatorn och uppdatera dess
   tester. Förväntad scenariostatus är 74 `not_reviewed`, 2 publika våg-1
   och 1 synlig särskild Stockholm-prototyp; 77 produkter/76 verkliga är
   oförändrat.
7. Testa och redovisa de två oberoende kr-faciten oförändrade:
   Sundsvall 151 200 kr i referens och 12 096/18 144/24 192 kr i besparing;
   Gotland 50 570 kr i referens och 4 016/6 024/8 032 kr i besparing.

## Aktiveringsgrind

- riktade motor-, gate-, adapter-, komponent-, sid- och matrisprov;
- full Vitest i samma verkligt isolerade syskonlayout som Codex ovan;
- full relevant Python/matris `--check` och deterministisk regenerering;
- ren `tsc`, isolerat bygge och ordinarie skarp E2E inklusive Scenario 34;
- exakt fil- och ID-diff samt `git diff --check`;
- inga ändringar i incheckat `dist/`, Enkey eller orelaterade arbetsfiler.

Committa lokalt i den befintliga isolerade Neptune-branchen och fokuserat
i skills. Stanna med unik, committad `ACTIVATION_READY: Codex`. Ingen push
före en separat `APPROVED_FOR_PUSH: Claude`.

`APPROVED_FOR_ACTIVATION: Claude`
