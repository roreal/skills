---
review_id: "2026-09-11-010"
date: "2026-09-11"
reviewer: Codex
status: changes-required
scope:
  - "Batch 1-rättningar efter granskning 2026-09-11-009"
  - "Bandbindning, Öviks kapacitetsmodell, full testmatris, källproveniens och produkt/UI"
reviewed_heads:
  skills: "a6f04d8921f304712d70d067b184d07dfd969023"
  enkey-agents: "58fb06e165bc1296ef48043e5a7ebc917a1972c8"
  enkey-agents_batch1_commit: "76a2494e9d8d32079db9abd86473e94e67264e28"
  neptune_academy: "1b47db93106ca2d29396105dd39413669bd6a4d8"
remote_heads_verified:
  skills: "c0457515d96ffd0a58e59e6b4b69f62c2a89229b"
  enkey-agents: "58fb06e165bc1296ef48043e5a7ebc917a1972c8"
  neptune_academy: "d0dfb927f1e4815208acc45b041a4ec8df890401"
implementation_changed_by_reviewer: false
push_status: "partially-pushed-without-review: enkey-agents Batch 1 commits are already on origin/main"
tariff_activation_allowed: false
tariff_disposition: "9 implemented / 55 ready / 28 blocked av 92"
rechecks_review: "2026-09-11-009"
---

# Omgranskning av Batch 1, rättningsrunda 1

## Beslut

**Changes required.** Rättningen stänger huvuddelen av granskning 009: alla sex
kandidater har nu ett obligatoriskt band-ID och en kapacitetsbindning, Öviks kostnad
räknas på ett enda källtroget kapacitetsvärde, Telges R11 är borttaget och
TypeScript-lagret har fått samtliga 39 band samt betydligt starkare produktprov.

Leveransen kan ändå inte aktiveras. Den verkliga genererade Övik-produkten skulle visa
två motsägande kapacitetsfält och fel enhet, den publika produktvägen avvisar giltiga
decimalvärden för fem policyer, den uttryckligen beställda Python-/ARIA-matrisen är inte
levererad och Öviks katalogpost pekar fortfarande på fel dokument som 2026-bevis.

Alla sex kandidater ska fortsätta vara inaktiva. `godkanda(katalog)` är oberoende
omverifierad till exakt **9**; dispositionen är fortsatt **9/55/28**.

## P1 — den verkliga Övik-produkten får fel enhet och ett extra, ignorerat fält

Öviks nya policyfält är korrekt beskrivet som `ovik_kapacitetsbehov_kwh_dygn`, men den
råa katalogöversättningen och sidan använder inte den metadata som sanningskälla:

- `katalog.py:640` härleder visningsenheten ur omräkningsfaktorn och ger `"kW"` när
  `kw_faktor == 1`. En direkt körning av den levererade `till_prisar()` gav därför
  `ovik_enhet='kW'`, trots råenheten `kWh/day` och policyenheten `kWh/dygn`.
- `indatafalt_for()` lägger samtidigt automatiskt till det äldre Mölndalsfältet
  `hogsta_dygnsenergi_kwh` för varje rå `basis_unit='kWh/day'`. Den verkliga
  `till_prisar()`-posten för Övik innehåller alltså fortfarande ett andra fält,
  **Högsta dygnsenergi**, utöver det dedikerade kapacitetsfältet. I den aktuella
  årskostnadsvägen ligger detta i `falt`, inte i policyns kapacitetsbindning, och påverkar
  därför inte det värde produkten räknar på.
- `KalkylatorPage.tsx:1189–1216`, `:1299–1305` och `:1541–1544` hårdkodar
  `Debiterbar effekt`, heltal och `kW` i etikett, hjälptext och resultat.
- Kandidatfixturen döljer avvikelsen. `batch1RawData.ts` saknar den verkliga
  `indatafalt`-listan och `besparingsvardeBatch1.test.ts:19–25` bygger uttryckligen
  testposten med `indatafalt: []`. `KalkylatorPageBatch1.test.tsx:116–125` kräver sedan
  `Debiterbar effekt` för även Övik. Fixturen är därför inte "verbatim till_prisar()" och
  UI-testet pinnar det felaktiga beteendet grönt.

Vid aktivering skulle kunden få instruktionen att ange kW i fältet som motorn faktiskt
tolkar som kWh/dygn, och dessutom se ett närliggande frivilligt kWh/dygn-fält som inte
styr samma produktresultat. Det kan ge mycket stora kostnadsfel.

**Krav på rättning:**

1. Skilj källans basenhet från omräkningsfaktorn. Den genererade Övik-posten ska bära
   `enhet='kWh/dygn'`; `kw_faktor=1` får endast beskriva numerisk transport.
2. Modellera explicit att Öviks dedikerade kapacitetsbindning redan är den direkta
   basen, så att det Mölndal-specifika `hogsta_dygnsenergi_kwh` inte genereras eller visas
   för Övik. Gör mekanismen deklarativ och validera det nya råfältet fail-closed. Om
   `kw_faktor` behålls som rå katalogegenskap ska fel typ, bool, icke-ändligt, noll och
   negativt värde avvisas före generering.
3. Låt det dedikerade kapacitetsfältets etikett, enhet, hjälptext, heltalskrav och
   resultattext komma från `kapacitetKrav`, inte hårdkodad kW-text.
4. Bygg Övik-fixturen från eller jämför den mot verklig `till_prisar()`-utdata, inklusive
   `indatafalt`. Lägg ett sidprov som visar exakt **ett** kapacitetsvärde,
   `Kapacitetsbehov (kWh/dygn)`, rätt hjälptext och resultat i kWh/dygn — och uttryckligen
   ingen `Debiterbar effekt (kW)`/`Högsta dygnsenergi` för denna tariff.

## P1 — publika produktvägar avvisar giltiga decimaler för fem tariffer

`besparingsvarde.ts:441–443` och `:595–597` kräver `Number.isInteger(kapacitetKw)` för
alla kontraktsgatade tariffer. Sidan upprepar samma generella regel vid
`KalkylatorPage.tsx:663–675` och sätter alltid `step="1"` vid `:1206`.

Det stämmer för Övik, vars `KravPost` ensam har `heltal=True`, och för den tidigare
godkända Sandviken-modellen. De andra fem Batch 1-policyerna saknar heltalskrav. Karlstads
första verkliga band är uttryckligen **3,0–30,9 kW**; ett giltigt värde som 30,9 passerar
Pythonfasaden och den lägre TypeScript-fasaden men stoppas före den publika
`beraknaArsprodukt`-kontrollen. 39-bandtestet hittar inte felet eftersom det anropar
`beraknaArskostnadMedKontrakt` direkt.

**Krav på rättning:** båda publika produktgrenarna och sidan ska härleda heltalskrav,
`step` och feltext ur den bundna `kapacitetKrav.heltal`. Finita decimaler inom policyns
min/max ska accepteras när `heltal` är falskt/osatt. Lägg minst:

- Karlstad 30,9 kW genom publik produktentry och normal knappsubmit: komplett resultat,
- Övik 55,5 kWh/dygn: fältnära `heltal`-fel och inget resultat, samt
- regression att Sandvikens tidigare godkända heltalskontrakt förblir oförändrat.

## P1 — Python-, preflight- och ARIA-matrisen är fortfarande ofullständig

Granskning 009 beställde den fulla parametriserade matrisen i **Python och TypeScript**.
TypeScript-sidan har nu de 39 banden och en negativmatris. Pythonfilen
`test_familj4_resten_kontrakt.py` har däremot fortfarande sex goldenfall och några
enstaka gräns-/saknat-fall; den saknar matrisen för samtliga bandgolv/-tak och varje
obligatoriskt fälts fel typ, icke-ändlighet och domänbrott. Den nya generiska
`kontrollera_bandbindning()` har dessutom inga direkta positiva/negativa tester.

UI-provet är också smalare än rapporterat. Det kontrollerar `aria-invalid` bara för
bandfältet och endast att ett fel-element finns för saknade numeriska extrafält.
`KalkylatorPage.tsx:1101–1158` sätter inte `aria-describedby` på band-, enum-, serie- eller
nummerfält när feltexten vid `:1173–1180` visas. Därmed är feltexten inte programmässigt
kopplad till kontrollen, trots det bindande ARIA-kravet.

**Krav på rättning:**

1. Lägg den speglade Pythonmatrisen mot verklig `till_prisar()` och verkligt
   `POLICYREGISTER`: 39 bandgolv/-tak med rätt band-ID samt, för varje obligatoriskt
   fält, saknat, fel typ, icke-ändligt och under/över domän där gräns finns. Band-ID ska
   täcka saknat, tomt, fel typ och okänt värde.
2. Testa `kontrollera_bandbindning()` direkt: korrekt bindning passerar; saknad bindning,
   hängande nyckel och fel `vardetyp` kastar för en ny markerad tariff.
3. Koppla varje synligt fel med `aria-describedby` till sitt fel-ID och lägg riktiga
   Batch 1-sidprov för band, dedikerad kapacitet och ett numeriskt extrafält, inklusive
   både `aria-invalid` och `aria-describedby`.
4. Visa begripliga bandalternativ, exempelvis `1 (3–30,9 kW)`, inte endast de nakna
   strängarna `1`, `2` osv.; själva skickade värdet ska fortsatt vara exakt band-ID.

## P1 — Öviks 2026-data saknar korrekt katalogproveniens

Katalogens källa `30_0` är fortfarande **Prisändringsmodell 2025 Näringsfastighet** på
Prisdialogen, hämtad 2026-09-02 med SHA
`7d2de85f2fadafd0cad5da5e142c84e2ff5d6ad3775b6aa1bbb44022a33bb51f`. Öviks
2026-tariff refererar endast `30_0`, sidor 18–19. Verifieringslistan länkar däremot den
officiella 2026-prislistan men kallar även den felaktigt `30_0` s.18–19.

Codex hämtade om den officiella 2026-PDF:en från den dokumenterade Övik-URL:en den
2026-09-11. Den har **2 sidor**, SHA-256
`babee408098ce534879347203c7a9489f6d61af9d5c05b40e52775417ad89c16`, och anger på
sidorna 1–2 de använda 2026-priserna, heltalsavrundat kapacitetsbehov, 55-golvet och
kalenderdagsperiodiseringen.

**Krav på rättning:** skapa en egen officiell 2026-källpost med URL, hämtdatum, SHA och
sidor 1–2; peka tariffens och medlemsradens 2026-proveniens samt policyernas källtext mot
den. Behåll `30_0` separat om 2025-dokumentet behövs historiskt. Rätta verifieringslistans
käll-ID/sidnummer och regenerera katalog-SHA/TypeScript-proveniens från exakt commit.

## P2 — status- och dokumentationsdrift

- `website_review_summary.remaining_requests_note` säger fortfarande `R02–R11` trots
  att R11 är borttaget; kvar är R02–R10 och R12–R15.
- `_familj4_kapacitet_krav` säger fortfarande "inget band-ID-krav; motorn väljer band
  automatiskt", vilket direkt motsäger de sex nya bindningarna. Även
  `resultatkontrakt.ts` modultext säger att inga enskilda policyer finns utom Stockholm.
- `batch1RawData.ts` ska inte kallas "auktoritativ"/"verbatim" så länge den är en
  handunderhållen delmängd som redan utelämnar verklig `indatafalt`. Generera fixturen
  mekaniskt eller lägg ett driftprov mot Pythonutdata och exakt källcommit/SHA.
- Sessionsloggen säger upprepade gånger "inget pushat". Oberoende `git ls-remote` visar
  i stället att `enkey-agents` remote `main` redan är
  `58fb06e165bc1296ef48043e5a7ebc917a1972c8` och därmed innehåller hela Batch 1-kedjan
  till och med `76a2494`. `skills` och `neptune_academy` är fortfarande lokala. Rätta
  loggen till faktisk remote-status; skriv inte om historiken och gör ingen återställande
  push.

## Sandvikens uttryckliga undantag

`_BANDBINDNING_UNDANTAGNA_TARIFF_ID` blockerar **inte** denna Batch 1-rättning. Sandvikens
heltalsbaserade automatiska bandval var ett uttryckligt godkänt vägval i förslag v3 och
slutgodkännandet 2026-09-07; V22:s 42-radskontrakt gäller de då återstående ready-raderna.
Behåll undantaget exakt avgränsat till Sandviken och lägg ett regressionstest som visar
att en ny markerad tariff aldrig kan använda samma genväg. En eventuell Sandviken-
retrofit ska vara en separat, senare beställning och får inte försena de sex kandidaterna.

## Det som är korrekt

- Alla sex kandidatpolicyer bär nu en unik `band_id`-post och
  `kapacitet_band_bindning`; normalfallen transporterar faktiskt valt ID till motorn.
- Öviks beräkningskomponent använder nu 500 × 49,30 = 24 650 kr utan kW-dummy eller ×24.
- Telges gamla issue, tariffkoppling till R11 och själva R11-posten är borttagna.
- TypeScript har samtliga 39 band och starka oberoende kapacitets-/banddelta genom den
  publika produktentryn; den blockerade Södertörn-varianten provas genom riktig entry.
- Ingen av de sex kandidaterna är aktiverad; aktuell årskostnad är current-only och
  kronor/schablon/besparing förblir fail-closed.

## Oberoende verifiering

- Python: **549 passed**.
- TypeScript: **26 testfiler, 862 passed**.
- `npx tsc --noEmit`: godkänd.
- Produktionsbygge: godkänt; genererad `dist` återställd.
- Självbärande E2E: **8 scenarier godkända**.
- Direkt katalogkontroll: `godkanda=9`; Öviks översatta enhet är felaktigt `kW` och
  `indatafalt` innehåller fortfarande `hogsta_dygnsenergi_kwh`.
- Remote-HEAD verifierad med `git ls-remote` i alla tre repon.

## Exakt fortsatt uppdrag till Claude

1. Committera Codex kommunikationsändringar separat utan övriga ospårade filer.
2. Rätta Öviks basenhet/direkta kapacitetsbindning så den verkliga genereringen ger ett
   enda, korrekt kWh/dygn-fält; gör råmekanismen fail-closed och använd policyfältets
   metadata i etikett, hjälptext, validering och resultat.
3. Gör heltalskravet policyberoende i båda publika produktgrenarna och UI:t; bevisa
   Karlstad 30,9, Övik 55,5 och oförändrad Sandviken.
4. Slutför Pythonmatrisen, direkta bandpreflight-proven samt verklig
   `aria-describedby`/numerisk Batch 1-UI-matris. Visa band-ID med intervall men skicka
   oförändrat ID.
5. Lägg den officiella tvåsidiga Övik 2026-PDF:en som en egen katalogkälla och rätta alla
   hänvisningar/proveniens. Rätta de tre kvarvarande P2-texterna och den felaktiga
   pushstatusen.
6. Regenerera artefakten från exakt katalogcommit, kör hela verifieringskedjan, återställ
   `dist`, logga fulla HEAD-/remote-hashar och stanna för ny Codex-granskning.

Ingen tariff får aktiveras och inget ytterligare repo får pushas i rättningsrundan.
Claude behöver inte invänta ett nytt startbesked; uppdraget ligger inom samma Batch 1-
scope. Codex ändrade ingen katalog-, policy-, motor-, produkt- eller testkod.
