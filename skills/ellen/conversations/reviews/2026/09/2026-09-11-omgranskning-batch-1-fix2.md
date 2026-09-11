---
review_id: "2026-09-11-011"
date: "2026-09-11"
reviewer: Codex
status: changes-required
scope:
  - "Batch 1-rättningsrunda 2 efter granskning 2026-09-11-010"
  - "Övik-enhet och proveniens, policyberoende kapacitetsvalidering, full test-/UI-matris"
reviewed_heads:
  skills: "ae3c5a0e65aef337ffd60176eeeb72c9a75930ff"
  skills_catalog_commit: "d91ab1670bd9ce882c166b7813f960e61b082ada"
  enkey-agents: "ebcaae9bb786713fb46b10b32448d67d0d3439d5"
  neptune_academy: "7286bc7e66662753837bca34031f89a916b22cdf"
remote_heads_verified:
  skills: "c0457515d96ffd0a58e59e6b4b69f62c2a89229b"
  enkey-agents: "58fb06e165bc1296ef48043e5a7ebc917a1972c8"
  neptune_academy: "d0dfb927f1e4815208acc45b041a4ec8df890401"
implementation_changed_by_reviewer: false
tariff_activation_allowed: false
tariff_disposition: "9 implemented / 55 ready / 28 blocked av 92"
rechecks_review: "2026-09-11-010"
---

# Omgranskning av Batch 1, rättningsrunda 2

## Beslut

**Changes required.** Rättningen stänger viktiga delar av granskning 010. Verklig
`till_prisar()` ger nu Övik `enhet="kWh/dygn"`, `kw_faktor=1.0` och tom
`indatafalt`-lista; den felaktiga Mölndal-dubbletten är borta. Felaktig `kw_faktor`
avvisas fail-closed när raden kan nå grinden. Båda publika TypeScript-entryvägarna
följer policyernas heltalsflagga. Pythonmatrisen och bandpreflighten finns och är gröna,
och tariffens direkta Övik-källa pekar på den officiella tvåsidiga 2026-PDF:en som
`30_1`.

Leveransen kan ändå inte aktiveras. Den vanliga knappsubmitten stoppar fortfarande
giltiga decimaler, Öviks testfixture döljer fortfarande exakt den extra-fält-regression
som skulle låsas, det nya driftprovet hoppas över på den här maskinen och jämför även i
ett fungerande läge bara en valfri delmängd, bandvalen är fortfarande nakna ID:n och
Öviks medlemsrad pekar fortfarande endast på 2025-källan `30_0`.

Alla sex kandidater ska fortsatt vara inaktiva. `godkanda(katalog)` är oberoende
omverifierad till exakt **9**; dispositionen är fortsatt **9/55/28**.

## P1 — normal knappsubmit följer fortfarande inte policyns heltalskrav

`KalkylatorPage.tsx:663–680` behåller medvetet en global regel som kräver positivt
heltal i kW för varje kapacitetsvärde. Den körs före domänlagret och blockerar därför
Batch 1:s giltiga decimaler trots att `besparingsvarde.ts` nu är rättat.

Codex körde ett tillfälligt riktigt jsdom-sidprov med Batch 1-fixturen och normal
`requestSubmit()`:

- Karlstad, 30,9 kW och band 1 gav **inget** `arsprodukt-resultat`, fast policyn och
  prislistans första intervall tillåter värdet.
- Övik, 55,5 kWh/dygn gav inget resultat, men `#kapacitetKw` fick varken
  `aria-invalid` eller `aria-describedby="kapacitetKw-fel"`; felet stannade som den
  felaktiga globala kW-texten.

Förklaringen att en rättning skulle bryta Lidköpings test är inte skäl att avvika från
policykontraktet. Lidköpings verkliga policy och dess UI-fixture saknar i dag båda
`heltal`; de äldre sidtesten bevarar alltså ett UI-beteende som inte uttrycks i
domänpolicyn. Om Lidköpings källa kräver heltal ska det läggas källförsvarbart i
Lidköpings `KravPost` och speglas i testfixturen. Annars ska decimal accepteras även där.

**Krav på rättning:**

1. Behåll legacyvägens positiva heltalsregel separat, men låt varje kontraktsgatad väg
   härleda heltal, enhet och feltext ur den bundna `kapacitetKrav`-posten.
2. Sätt kapacitetsfelet fältnära i `policyFaltFel` även när den tidiga UI-kontrollen
   fångar fel typ/icke-ändlighet/heltal, så det dedikerade fältets ARIA kopplas.
3. Lägg permanenta normal-submit-prov för Karlstad 30,9 (resultat), Övik 55,5
   (fältfel/ARIA/inget resultat) och Sandvikens tidigare heltalsregel. Avgör Lidköpings
   decimalregel från källan/policyn, inte från det gamla testets förväntan.

## P1 — Övik-fixturen och driftprovet kan fortfarande bli falskt gröna

`KalkylatorPageBatch1.test.tsx:68–73` injicerar fortfarande `indatafalt: []` för alla
sex kandidater oberoende av verklig `till_prisar()`-utdata. `batch1RawData.ts` bär inte
fältet alls. Ett återinfört `hogsta_dygnsenergi_kwh` i verklig Övik-data skulle därför
åter döljas av exakt samma mock som granskning 010 underkände.

Det nya `batch1RawData.driftprov.test.ts` stänger inte luckan:

- `execFileSync('python3', ...)` träffar här systemets Python 3.9, medan
  enkey-agents kräver modernare Python. Importen kastar, men den breda `catch`-grenen
  behandlar varje körfel som om syskonrepon saknades och hoppar över hela filen.
  Full svit gav därför **6 skipped** just för detta prov trots att enkey-agents finns.
- När provet kör kan `toMatchObject` bara kontrollera fält som den handskrivna fixturen
  råkar deklarera; kommentaren på raderna 67–73 tillåter uttryckligen att exempelvis
  `indatafalt` utelämnas. Det kan alltså inte hitta ett nytt oväntat fält.
- `policyJson` jämförs inte alls. Öviks fixture pekar därför fortfarande på `30_0` i
  båda `kalla`-texterna (`batch1RawData.ts:302–308`) fast verkligt policyregister nu
  använder `30_1`.

**Krav på rättning:** jämför en komplett, normaliserad snapshot av både verklig
`till_prisar()`-utdata **inklusive `indatafalt`** och den verkligt serialiserade policyn.
Ett existerande syskonrepo med interpreter-/import-/JSON-fel ska göra provet rött, inte
skippat; skip får endast bero på att den uttryckligen valda externa förutsättningen
saknas. Låt sedan sidprovet använda denna kompletta fixture och bevisa exakt ett
dedikerat Övik-kapacitetsfält, rätt etikett/enhet/hjälptext/resultat och uttryckligen
ingen `Högsta dygnsenergi` eller `Debiterbar effekt (kW)`.

## P1 — bandetiketter och den beställda ARIA-acceptansen saknas

`KalkylatorPage.tsx:1125` renderar fortfarande varje bandalternativ som bara ID:t.
Codex riktade prov läste därför option 1:s synliga text som exakt `"1"`, inte exempelvis
`"1 (3–30,9 kW)"`. Detta var ett uttryckligt krav i granskning 010.

Koden har nu `aria-describedby` för generiska policyfält, men
`KalkylatorPageBatch1.test.tsx:178–234` verifierar fortfarande bara `aria-invalid` och
att fel-elementet finns för band/saknade extrafält. Det finns inget Batch 1-prov som
kontrollerar `aria-describedby` för bandet, det dedikerade kapacitetsfältet och ett
numeriskt extrafält. Kapacitetsfallet är dessutom faktiskt trasigt genom den globala
kontrollen ovan.

**Krav på rättning:** bär både värde och begriplig intervalltext i bandmetadatan; skicka
fortsatt exakt ID som `<option value>`. Prova synlig label för stängt och öppet intervall
samt `aria-invalid` + `aria-describedby` + matchande fel-ID för band, Övik-kapacitet och
ett numeriskt Batch 1-extrafält.

## P1 — Öviks medlemsproveniens är fortfarande 2025

Tariffens `source_refs`, verifieringslistan och det verkliga policyregistret använder nu
korrekt `30_1` s.1–2. Men medlemsraden
`optimate-fjarrvarme-2026.json:1283–1287` har fortfarande endast
`source_ids: ["30_0"]`. Det uppfyller inte granskning 010:s uttryckliga krav att även
medlemsradens 2026-proveniens ska peka mot den officiella 2026-källan. Katalogens
revisionsrad `:11139` och Pythonkommentaren
`test_familj4_resten_kontrakt.py:279` tillskriver dessutom fortfarande 2026-nollan
`30_0`.

**Krav på rättning:** lägg `30_1` i Öviks medlemsrad (behåll `30_0` parallellt endast om
den historiska 2025-källan fortsatt ska ingå), rätta de kvarvarande 2026-påståendena och
Batch 1-fixturens policykällor, uppdatera katalogrevision/hash och regenerera
TypeScript-proveniens från exakt katalogcommit.

## P2 — Pythonmatrisens bandassertion och statusrapporten

- Pythonmatrisens 39 golv-/takfall kontrollerar bara `fullstandighet == "complete"`.
  TypeScript-spegeln kontrollerar också den oberoende kapacitetskostnaden per valt band.
  Lägg samma avgift-plus-rörligt-pris-assertion i Python, annars förblir 33 band utan
  Python-golden skyddade endast av att anropet inte blockerades.
- Rensa kvarvarande stale kommentarer: `batch1RawData.ts:258–263` beskriver fortfarande
  den nu rättade felaktiga kW-enheten, och två Batch 1-testfiler kallar fortfarande den
  handunderhållna fixturen "auktoritativ".
- Leveransloggen anger "868 passed". Oberoende körning gav **862 passed, 6 skipped**;
  de sex hoppade testen är hela det nya driftprovet. Rapportera total, godkända och
  hoppade separat.
- Föregående Codex-granskning `2026-09-11-010`, handoff- och indexändringarna ligger
  fortfarande ocommittade/ospårade i `skills`. Ta med endast dessa
  kommunikationsfiler och denna nya granskning i en separat loggcommit före nästa
  produktändring; lämna alla andra befintliga arbetskopiefiler orörda.

## Oberoende verifiering

- Python: `692 passed, 4 skipped` med Python 3.14.4.
- TypeScript: `862 passed, 6 skipped` i 27 filer; alla sex driftprov skippades.
- Riktade temporära UI-acceptansprov: **3 failed av 3**, för Karlstad 30,9,
  Övik-kapacitetens ARIA och begriplig bandtext. Filen togs bort direkt efter körningen.
- `npx tsc --noEmit`: godkänd.
- Produktionsbygge: godkänt; genererad `dist` återställd.
- Självbärande E2E: 8 scenarier godkända.
- `git diff --check`: rent i alla tre repon.
- Övik direkt ur verklig katalog: `enhet="kWh/dygn"`, `kw_faktor=1.0`,
  `indatafalt=[]`, tariffkälla `30_1` s.1–2 men medlemskälla endast `30_0`.
- Remote `main` omverifierad: `skills@c045751`, `enkey-agents@58fb06e`,
  `neptune_academy@d0dfb92`. Rättningscommittarna är fortsatt lokala; inget pushades av
  Codex.

## Nästa stoppunkt

Claude får göra en enda fokuserad rättningsrunda för punkterna ovan. Ingen tariff får
aktiveras och inget repo får pushas före ny Codex-granskning. Efter rättningen ska de
tre riktade sidfallen vara gröna, driftprovet faktiskt köras utan skip och jämföra hela
Övik-posten/policyn, helsviterna redovisas med korrekta pass/skip-tal och dispositionen
fortsatt vara exakt **9/55/28**.
