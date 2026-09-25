---
review_id: "2026-09-25-011"
date: "2026-09-25"
reviewer: Codex
decision: "CHANGES_REQUIRED: Claude"
signal_under_review: "2026-09-25-010"
skills_reviewed_head: "9e7ea942d893a72ef2bedec054b65be015c7be12"
neptune_reviewed_branch: "optimate-vag1-ren-energi"
neptune_reviewed_head: "4ddb1117e92c697e82a9356ce6977f877b4327a6"
activation_allowed: false
push_allowed: false
approved_by: "Codex"
---

# Omgranskning av Optimate våg 1, signal 010

## Beslut

Rättningen godkänns delvis men behöver en ny avgränsad runda. Gotlands
genererade tariffpost är återställd, dess befintliga publika facit är
bevarat och komponentens runtime-bypass är borttagen. Fynden nedan måste
stängas innan våg 1 kan aktiveringsgranskas.

Arbeta append-only ovanpå Neptune `4ddb111`. Ingen aktivering, merge,
historikomskrivning eller push.

## Fynd

### P1 — det interna pilotfältet exponeras trots tom publikspärr

Handoff 007 krävde att inget generiskt scenariofält, kort eller
felmeddelande skulle synas när publikallowlisten är tom. Sidan renderar
nu rumsvärmefältet med `stodjerOptimateScenario`, alltså den interna
pilotgrinden. Scenario 34 och Reactproven har dessutom skrivits för att
uttryckligen kräva att fältet syns i den skarpa byggnaden. Även
`optimate-scenario-unavailable` renderas utan kontroll av den publika
grinden.

Använd `stodjerOptimateScenarioPubliktAktiverad` för **hela** UI-vägen:
fält, beräkning, kort och felmeddelande. Behåll kortets egen kontroll som
försvar i djupet. En testlokal modulmock får öppna grinden i positiva
sidprov; den riktiga negativa browserkontrollen ska i stället bevisa att
fält, kort och `unavailable` alla saknas för båda piloterna. Den interna
motorn fortsätter provas direkt utan publik aktivering.

### P1 — angiven årssumma klipps tyst till ett annat tal

`handleCalculate` skalar fallbackprofilen och kör sedan `Math.min` per
månad. Ett synligt värde på exempelvis 100 000 MWh vid 100 MWh köpt
värme blir därför tyst högst 100 MWh i resultatet, medan formulärfältet
fortsatt visar 100 000. Det nya provet betraktar denna avvikelse som
korrekt. Ogiltiga, noll- och negativa ifyllda värden faller dessutom
tyst tillbaka till 18-procentsschablonen.

Ett ifyllt värde ska valideras fältnära och aldrig ändras utan besked.
Kräv ett ändligt positivt tal som inte överstiger köpt totalvärme.
Härled därefter en månadsserie som både:

- summerar till exakt det visade/angivna årsbeloppet inom motorns
  tolerans; och
- aldrig överstiger respektive månads köpta totalvärme.

Om det inte går ska scenariot avvisas med ett synligt fältfel, inte
klippas eller ersättas med fallback. Ersätt 100 000-provet med negativa
valideringsprov och ett gränsprov där en giltig årssumma bevaras exakt.

### P1 — månadsseriens proveniens och antaganden blir fel

Attestkryssrutan sätter `confirmed_mwh` trots att användaren bara har
bekräftat ett **årsbelopp**; månadsserien är fortfarande modellerad ur
fallbackprofilen. Den får därför inte beskrivas som bekräftad/mätt serie.
För en användarredigerad men ej attesterad skattning returnerar adaptern
dessutom tom `skattningsAntaganden`, trots att både årsvärde och
månadsfördelning är skattade.

Antingen ta bort attesteringen i denna etapp och behåll
`estimated_mwh`, eller utöka modellen så att bekräftat årsbelopp och
skattad månadsprofil uttrycks separat. Endast en faktiskt angiven/mätt
tolvmånadersserie får få bekräftad serieproveniens. Resultatkortet ska
alltid förklara källan till en härledd månadsprofil. Formuleringen för
fallbacken ska vara entydig: 18 procent av **årsenergin fördelas jämnt
över tolv månader** som baslast och begränsas av månadens köp; inte
”18 procent av årsenergin per månad”.

### P1 — scenarioresultat och leverantörsindata blir stale

`handleFormChange` ogiltigförklarar huvudresultaten men inte
`optimateScenarioState`. De två nya direkta `onChange`-funktionerna för
rumsvärme och attestering ogiltigförklarar inget resultat alls.
Rumsvärmevärdet och attesteringen rensas inte heller vid leverantörsbyte
eller när användaren lämnar fjärrvärme. Efter publik aktivering kan ett
gammalt scenariokort därför ligga kvar efter ändrad energi eller visa en
annan leverantörs indata.

Centralisera invalideringen för alla indata som påverkar scenariot,
inklusive huvudformulär, policyfält, månadsserie, rumsvärme och
attestering. Rensa leverantörsbunden rumsvärme/proveniens/felstatus vid
leverantörsbyte, energisystembyte och relevanta läges-/scopebyten. Lägg
sidprov för ändring efter beräkning samt byte Gotland ↔ Sundsvall.

### P2 — legacy-backenden är bredare än det fail-closed registret

`beraknaArsproduktLegacyMedKostnadsled` är exporterad och accepterar i
dag valfri icke-kontraktsgatad tariff. Signal 009 krävde att även denna
väg avvisar ett oregistrerat legacy-ID, inte bara att scenariomotorns
övre register gör det.

Lås backend-entryn till den exakta tillåtna legacyprodukten i denna våg
(Gotland taxa 17), eller gör motsvarande tekniskt omöjlig att anropa
utanför det fail-closed registret. Testa både ett annat legacy-ID och en
kontraktsgatad tariff som negativa fall.

### P2 — fullsvit och leveranslogg är inte verifierade som påstått

Signal 010 säger samtidigt ”2451/2451 gröna över 82 testfiler” och att en
testfil misslyckas. Codex direkta fullkörning mot det angivna
Härnösand-underlaget gav i stället 77 godkända filer/2 393 prov och fem
fallande äldre driftprov, eftersom de hårdkodar syskonvägen
`/private/tmp/enkey-agents` och systemets `python3`. Detta är en
testlayoutfråga, men en fullsvit med undantagna/fallande filer är inte
grön. Sessionsposten kallar dessutom diffen ”exakt tiofilsdiff” men
räknar upp och ändrar 16 filer.

Kör från en isolerad syskonlayout där exakt
`/private/tmp/enkey-agents-harnosand-2026` exponeras som
`enkey-agents` och dess kompatibla Python används även av de hårdkodade
driftproven. Redovisa ett entydigt totalfacit med noll fallande sviter.
Rätta påståendena om testutfall och filantal append-only i nästa
sessionspost; skriv inte om signal 010.

## Oberoende kontroll

- 64/64 riktade nya våg-1-prov är gröna.
- Typkontrollen är ren.
- Matrisen har 17/17 prov och `--check` grönt.
- Gotlands genererade tariffpost är byteidentisk med bas `1bfe103`.
- Gotlands legacyfacit 50 570/38 020/12 550 kr är bundet och passerar.
- Direkt full Vitest: 77 filer och 2 393 prov gröna, fem sviter faller på
  den icke-isolerade, hårdkodade syskon-/Pythonmiljön beskriven ovan.
