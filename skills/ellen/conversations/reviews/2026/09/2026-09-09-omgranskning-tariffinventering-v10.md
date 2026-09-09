---
review_id: "2026-09-09-001"
date: "2026-09-09"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v10.md
  - Fjarrvarmetariffer/batchplan-v10.md
  - skills commits 2b143789d417e25d054f0d70513961f18df1e2bb and ab38b79770d37202679c123553f61907948c43cc
reviewed_heads:
  skills: "ab38b79770d37202679c123553f61907948c43cc"
  enkey-agents: "fd8f8da3eb17cce638dc2f3370efa027c2afcad6"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-08-009"
---

# Omgranskning av tariffinventering v10 och batchplan v10

## Bedömning

V10 löser flera av V9-granskningens uttryckliga strukturproblem. Det nya `policyFalt`
ligger parallellt med legacyfältet i stället för att försöka pressa band och serier genom
`Record<string, number>`. Metadatasignaturen har nu tillgång till vald prispost och
omfattning, kapacitet filtreras bort från den generiska listan, etikett/hjälptext får en
deklarerad källa och adapterförslaget har både ett injicerat register och en uttrycklig
ersättningsmarkör. V10 bevarar också de tidigare godkända Umeå-, Stockholm-serie-,
Kraftringen-, Jönköping- och räkningsbesluten.

Planen är ändå inte implementeringsklar. Formulärstate och domän-DTO blandas fortfarande
ihop, vilket gör att tomma seriefält kan bli giltiga nollor och Jönköpings numeriska enum
skickas med fel typ. Den beskrivna vägen till `ogiltigaFalt` kan inte köras eftersom
kontraktsvalidatorn kastar innan ett `blocked`-resultat finns. Den nya årsproduktens
dispatch skickar dessutom vanliga kontraktstariffers besparingsanrop till fel resultatgren,
medan Stockholm-vägen saknar kapacitetsinlägget och en typ som faktiskt kan bäras genom
`KalkylatorResult`. Slutligen fungerar adapterpreflighten inte för `bygg_ts()` på det sätt
V10 påstår och dess reverse-mängd tappar leverantörsidentiteten.

Det krävs därför en avgränsad V11-rättning av planeringsdokumenten. Ingen produktkod,
tariffdata, aktivering eller push är godkänd.

## P1-fynd

### P1 — formulärets råvärden och den parsade policy-DTO:n är fortfarande samma state

V10 §6a.2 rad 1903–1915 definierar `PolicyInputValue = number | string | readonly number[]`
och använder samtidigt `Record<string, PolicyInputValue>` som React-state. Den säger att
tal konverteras först vid inskick och att en serie samlas från N separata talfält. Ett
HTML-talfält bär emellertid en sträng medan användaren skriver. En delvis ifylld serie är
därför `string[]`, vilket den föreslagna state-typen inte kan bära.

Om implementationen i stället kör `Number(...)` per ruta uppstår ett fail-open-fel:
`Number('')` och `Number('   ')` är `0`. En tom eller delvis tom serie med rätt antal
UI-rutor kan därmed bli en komplett `number[]` med nollor, passera både ändlighets- och
kardinalitetskontrollen och påverka kostnaden som om kunden uttryckligen rapporterat noll.
Det motsäger V10:s eget krav att en delvis ifylld serie ska ge ett fältnära användarfel.

Samma stycke säger att både band och enum ska skickas som oförändrade strängar. Jönköpings
allow-list är däremot uttryckligen numerisk: `tillatna_varden: tuple[float, ...]`,
`tillatnaVarden?: readonly number[]`, med exakt medlemskap mot `0/10/25/50` (§6a.6 rad
2565–2574). Ett val som UI:t skickar som `"10"` avvisas alltså av ett `number`-krav mot
värdet `10`. Band-ID ska vara sträng; Jönköpings numeriska enum ska vara tal. De kan inte
delas av regeln "enum/band parsas aldrig".

**Begärd rättning:** definiera ett separat rått formulärstate, exempelvis skalära strängar
och strängarrayer, och en enda strikt parser från metadata + råstate till
`PolicyInputValue`. Trimma och klassificera tomma rutor före `Number`, avvisa icke-ändliga
tal, kräv samtliga serieelement och konvertera numeriska enumvärden till tal medan band-ID
förblir sträng. Behåll uttryckligt `0` skilt från saknad nyckel. Testa tomt skalärfält,
blanksteg, delvis tom 12-/5-serie, explicit noll, samtliga fyra Jönköpingsval och ett
strängformat band-ID genom den riktiga sidan.

### P1 — `ogiltigaFalt` kan inte härledas från ett `blocked`-resultat

V10 §6a.2 rad 1993–2000 säger att `beraknaBesparingsvardeKontrakt` ska sätta
`ogiltigaFalt` när `status.fullstandighet === 'blocked'` och
`harled_resultatstatus`/`harledResultatstatus` har avvisat typ, numerik, kardinalitet eller
allow-list.

Det är inte dagens kontrakt. `harledResultatstatus` returnerar `blocked` för saknade fält
(`resultatkontrakt.ts` rad 378–380), men ogiltig typ, numerik, serieform, heltalskrav och
gränser kastar `Error` under valideringsloopen (rad 385–420). V10 planerar att lägga de nya
`vardetyp`-/`antalVarden`-/`tillatnaVarden`-kontrollerna i samma kastande loop. Det finns
alltså inget statusobjekt att undersöka efter ett ogiltigt värde. Okänt band-ID upptäcks
ännu senare av `next(...)` i motorn, eftersom statusvalidatorn inte har tillgång till
prispostens `nivaer`; även det blir ett generiskt kast, inte `okant_val`.

**Begärd rättning:** välj en körbar felkanal. Antingen returnerar en separat
policyindatavaliderare ett typat resultat med `{nyckel, orsak}` innan fasadanropet, inklusive
banduppslag mot vald prispost, eller så kastar validatorn en namngiven typad valideringsklass
som produktgränsen fångar och mappar till `KontraktBlockerat.ogiltigaFalt`. Saknade fält ska
fortsatt skiljas från ogiltiga, och policy-/bindnings-/metadatakonfigurationsfel ska fortsatt
vara interna fel. Beskriv och testa samma mekanism i både TypeScript och Python i stället
för att försöka läsa detaljer ur ett statusobjekt som aldrig returneras.

### P1 — årsproduktens dispatch gör besparingsgrenen onåbar för vanliga kontraktstariffer

V10 §6a.4 rad 2461–2466 lägger i samma `annars`-gren både
`onskadTyp === 'aktuell_arskostnad'` och en tariff utan
`kallenergiArsserieBindning` som efterfrågar besparing. Grenen gör ett enda
`beraknaArskostnadMedKontrakt`-anrop och returnerar alltid
`{typ:'aktuell_arskostnad'}`.

Det betyder att ett besparingsanrop för Sandviken och de 44 framtida kontraktstarifferna
utan Stockholms kallenergiserie inte längre gör före-/efterberäkningen. V10:s
`{typ:'besparing'}`-gren konstrueras aldrig av den beskrivna dispatchen. Det bryter det
sekundära produktmålet och den befintliga, godkända Sandviken-vägen.

**Begärd rättning:** ange tre separata grenar:

1. `besparing` + förbjudande kallenergiserie → typad produktbegränsning;
2. `besparing` + stödd tariff → befintlig kontraktsgated före-/efterfunktion, returnerad som
   en fullständig besparingsgren;
3. `aktuell_arskostnad` → exakt ett framåtriktat årsfasadanrop.

Besparingsgrenen bör bära hela det befintliga `Besparingsvarde`-kontraktet (leverantör,
prisår, kapacitet, andel av notan och status), inte bara tre kostnadstal som gör att
`calcResult` måste återskapa informationen.

### P1 — Stockholm-vägen är ännu inte representerbar genom den verkliga produktsidan

V10:s `beraknaArsprodukt` bygger enligt rad 2450–2451 indata via
`byggIndataFranPolicy(policy, policyFalt)`. Samtidigt filtrerar metadatan uttryckligen bort
`policy.kapacitetBindning`, och kapaciteten finns bara som `args.kapacitetKw`. Planen säger
att kapacitetsinlägget ska läggas till efter den generiska kartan endast i
`beraknaBesparingsvardeKontrakt` (rad 1928–1931). Den nya aktuell-årskostnadsvägen får
således ingen `IndataPost` för Stockholms annual-skopade effektkrav och blockeras.

Även resultatnivån saknas. Dagens `KalkylatorResult` kräver numeriska `savingsMin`,
`savingsMax`, `annualSavingsKr`, payback- och nettovärden, och sidan renderar dem
ovillkorligt. V10 säger bara att `calcResult` ska lämna besparingsfälten `null`/utelämnade;
det kompilerar inte mot dagens interface och räcker inte för att hindra den befintliga
resultatsidan från att visa besparing. Inte heller finns `onskadTyp` i den föreslagna
`KalkylatorInputs`-ändringen eller ett angivet UI-beslut som förklarar hur sidan begär
aktuell kostnad respektive besparing, trots att sidtesterna ska begära båda.

Den nya publika produktentryn måste dessutom återanvända samma fail-closed-kontroller som
dagens kontraktsadapter: bekräftad MWh-proveniens, ändligt positivt energital, exakt
debiterbar kapacitet och korrekt energifördelning. Annars kan ett direkt anrop kringgå den
säkerhet som i dag finns både i `calcResult` och `beraknaBesparingsvardeKontrakt`.

**Begärd rättning:** låt en gemensam indatabyggare validera och lägga in kapaciteten för
båda produktgrenarna. Definiera en diskriminerad resultattyp på `calcResult`-/sidnivå där
`aktuell_arskostnad` strukturellt saknar alla besparings-/paybackfält, och visa exakt hur
renderingen grenar innan dessa läses. Ange en deterministisk källa till `onskadTyp`
(produktförmåga eller ett uttryckligt kundval) och testa båda grenarna via den riktiga
sidan samt direkt produktanrop.

### P1 — adapterpreflightens två anropsvägar och reverse-nyckel är inte konsekventa

V10 §6a.4 rad 2321–2325 säger att `bygg_ts()` ska köra preflighten med tom katalog och tomt
adapterregister när inga adapterposter är relevanta. Efter Stockholms utökning bygger
`bygg_ts()` emellertid fortfarande leverantörsfilen och dess policy med
`ersatter_katalograd`. Reverse-loopen på rad 2292–2301 ser då markören men en tom
`adapterade_mal` och kastar. Den utlovade standalone-vägen kan alltså inte lyckas med
produktionsregistret.

Reverse-loopen använder dessutom bara `set(entry.tariff_id)`. `AdapterEntry` innehåller
uttryckligen `provider_id`, men den tappas i omvänd riktning. Två byggda leverantörer med
samma `tariff_id`, där bara den ena `(provider_id, tariff_id)`-posten är adaptermappad, får
den andra markören felaktigt kvitterad av samma tariff-ID. Mängden bevisar inte heller den
utlovade "exakt en"-relationen som en räknad mappning gör.

**Begärd rättning:** bestäm ett enda explicit anropskontrakt för `bygg_ts()`: antingen får
den verklig rå katalog + adapterregister när en byggd policy bär ersättningsmarkören, eller
så avvisar den tydligt att standalone-generation kan användas för en sådan leverans. Kör
inte en låtsad tom kontext som om den bevisade bijektionen. Nyckla reverse-kontrollen på
hela `(provider_id, tariff_id, ersatter_katalograd)`-relationen och verifiera exakt ett
framåt- och bakåtpar. Testa `bygg_ts()` med den verkliga Stockholmspolicyn, dubbelt mål,
samma tariff-ID hos två providers samt fel källa.

## P2-fynd

- V10 §6a.2 rad 1957–1963 säger både att etikett/hjälptext "redan finns i katalogen" och
  genereras genom `indatafalt_for()`, och att de är nya `KravPost`-fält satta av
  `policyregister.py`. Det är två olika källvägar. Ange policyregistret som auktoritativ
  källa och `_policy_till_json()`/`policyFranGenererad()` som transport, eller definiera en
  verklig katalogmappning; blanda inte mekanismerna.
- Batch 0 talar om en syntetisk prispost med "alla fyra `vardetyp`", men kontraktet har tre
  värdetyper (`number`, `number_series`, `band_id`); `enum_val` är ett UI-läge för ett
  numeriskt `number`-krav med allow-list. Samma dokument använder både
  `beraknaArsprodukt(args, onskadTyp)` och signaturen där `onskadTyp` ligger i `args`, samt
  placerar `kontrollera_adapterpreflight` i `katalog.py` i batch 0 men i `generera.py` i
  batch 7. Välj en terminologi, en signatur och en ägarfil.

## Verifieringar

- `skills@2b14378` och korrigeringscommitten `ab38b79` ändrar bara dokumentation och
  konversationslogg. Ingen produktkod, tariffdata eller genererad frontendfil ändrades.
- `git diff --check 2cfa3be..ab38b79` är rent. `ab38b79` ligger direkt ovanpå `2b14378`,
  vars verifierbara committid är `2026-09-08T23:32:03+02:00`.
- Produktrepoerna är rena och oförändrade på `enkey-agents@fd8f8da` och
  `neptune_academy@f1df177`. Deras verkliga validator, generator, produktadapter,
  `KalkylatorResult` och resultatsida lästes som granskningsbas.
- V10 innehåller fortsatt exakt 78 bastariffrubriker och 14 variant-ID:n. Den frysta
  kontrollmängden 92 och dispositionen 7 implementerade, 55 redo och 30 blockerade är
  oförändrade; inga nya sakstatusfynd motiverar en flytt i denna runda.
- Lokal `main` är 13 commits före `origin/main` och inte efter. V10 är inte godkänd för
  push.
- Inga fulla produkttester kördes eftersom V10 endast ändrar planeringsdokumentation och
  de beskrivna nya gränssnitten ännu inte finns i kod.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v11.md` och `batchplan-v11.md`; ändra inte V10 i efterhand.
2. Skilj rått formulärstate från parsad `PolicyInputValue`; behandla blankt/delvis ifyllt
   som saknat eller ogiltigt, bevara explicit noll och skicka numerisk enum som tal men
   band-ID som sträng.
3. Definiera en körbar typad valideringskanal för ogiltig kundindata, inklusive okänt
   band-ID mot vald prispost; försök inte läsa den ur ett `blocked`-resultat efter ett kast.
4. Rätta `beraknaArsprodukt` till tre grenar så stödda tariffers besparingsflöde bevaras och
   Stockholm fortsatt blockerar just besparingsförmågan.
5. Gör aktuell årskostnad end-to-end: gemensam kapacitets-/proveniensvalidering,
   diskriminerad `KalkylatorResult`-/renderingsgren och en definierad källa till
   `onskadTyp`.
6. Gör adapterpreflighten sann för både `bygg_ts` och `bygg_ts_fran_katalog`, och bevisa
   reverse-relationen med provider + tariff + katalograd och exakt kardinalitet.
7. Rätta P2-motsägelserna om etikettkälla, antal värdetyper, funktionssignatur och ägarfil.
8. Behåll V10:s lösta metadatafilter, nya fältmappningar, tidigare Umeå-/Stockholmserie-/
   Kraftringen-/Jönköpingbeslut samt dispositionerna 7/55/30 om ingen sakstatus ändras.
9. Skapa en fokuserad lokal dokumentationscommit ovanpå `ab38b79`, logga verklig hash/tid
   och stanna för ny Codex-granskning. Ändra ingen produktkod eller tariffdata och pusha
   inte.
