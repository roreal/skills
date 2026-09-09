---
review_id: "2026-09-09-004"
date: "2026-09-09"
reviewer: Codex
status: changes-required
scope:
  - Fjarrvarmetariffer/tariffinventering-v13.md
  - Fjarrvarmetariffer/batchplan-v13.md
  - skills commit b467d0adc48e22dbb09f9236546ec8979220aeb4
reviewed_heads:
  skills: "b467d0adc48e22dbb09f9236546ec8979220aeb4"
  enkey-agents: "fd8f8da3eb17cce638dc2f3370efa027c2afcad6"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
push_status: local-unpushed-not-approved
supersedes_review: "2026-09-09-003"
---

# Omgranskning av tariffinventering v13 och batchplan v13

## Bedömning

V13 stänger flera verkliga V12-luckor. Parserns argument accepterar nu `undefined`, den
domänägda förkontrollen är rätt princip för exakta saknade fält, produktförmågan har en
enda avsedd tabell och `beraknaArsprodukt` får en egen domänguard. Adapterförklaringen,
punktnumreringen och leveransmetadata är också bättre.

Planen är trots det inte implementeringsklar. Den nya förmågefunktionen läser fel nivå ur
`kontraktsgatadPolicy()`-returen och kompilerar därför inte mot dagens typ. Den påstått
typkorrekta argumentbyggaren använder tre fält/hjälpfunktioner som inte finns och lämnar
den befintliga besparingsvägen på en separat kopia av samma scope-/provenienslogik.
Förkontrollen filtrerar inte på beräkningsomfattning, vilket gör att Stockholms årsprodukt
kan blockeras av krav som bara gäller månadsberäkning. Parserns/formulärfelets orsaksunioner
och fältnamn är dessutom fortfarande motsägande.

Det krävs därför en smal V14-korrigering av kontrakts- och kodskisserna. Ingen produktkod,
tariffdata, aktivering eller push är godkänd.

## P1-fynd

### P1 — parser- och valideringsfeltyperna är fortfarande inte en enda sluten modell

Inventering rad 2031–2039 och batchplan rad 104–110 deklarerar
`PolicyValideringsOrsak` med `'typ'|'numerik'|'kardinalitet'|'min'|'max'|'heltal'|
'okant_val'`. Inventeringen säger uttryckligen att min/max/heltal är egna orsaker som ska
användas konsekvent. Samtidigt definierar batchplan rad 121–126
`PolicyValideringsFel.orsak` utan `'min'|'max'|'heltal'`, och inventering rad 2194–2200
mappar alla tre tillbaka till `'numerik'`. Båda modellerna kan inte vara den deklarerade
sanningen.

Parserns beteendelista hanterar `undefined`, blankt, kardinalitet och numerik, men inte den
råa värdeunionens fel form. Ett skalärt metadatafält kan få `readonly string[]`, och ett
seriefält kan få en ensam `string`. Utan `typeof ravarde === 'string'` respektive
`Array.isArray(ravarde)` kan skalärgrenen försöka anropa `.trim()` på en array och
seriegrenen iterera strängtecken; orsaken `'typ'` har annars ingen definierad väg.

Slutligen använder V13:s inledning returformen `{ saknadeFalt, ogiltigaFalt }`, medan den
normativa signaturen i inventeringen rad 2184–2186 och batchplan rad 121–123 returnerar
`{ saknade, ogiltiga }`. Produktkoden sägs sedan fylla klassens `saknadeFalt` och
`ogiltigaFalt`, utan en enda fastställd mappning.

**Begärd rättning:** deklarera en faktisk typkedja en gång, exempelvis
`PolicyParseOrsak`, `PolicyValideringsOrsak`, `PolicyValideringsFel` och
`PolicyIndataKontroll`, och återanvänd namnen ordagrant i båda dokumenten. Välj antingen
egna min/max/heltal-orsaker eller gemensam `'numerik'`, inte båda. Lägg explicita
råformsgrindar för scalar/array och testfall där formen är omkastad. Använd samma
returfältnamn genom validator, `KontraktBlockerat` och UI.

### P1 — förkontrollen saknar omfattning och en konstruerbar felkanal

`forkontrolleraPolicyIndata(policy, prisar, indata)` itererar enligt inventering rad
2184–2205 över hela `policy.kravdaFalt`. Den tar varken `omfattning` eller gör ett dokumenterat
`f.kravsFor.includes('annual')`-filter. Stockholmspolicyn innehåller både befintliga
`monthly`-krav och de planerade `annual`-serierna. En årsberäkning kan därför felaktigt få
månadsfälten i `saknadeFalt` och blockeras innan `harledResultatstatus`, vars riktiga kod
annars filtrerar på omfattning, nås.

V13 säger också att förkontrollens fynd ska kasta `KontraktBlockerat`. Dagens konstruktor
kräver `orsak: KontraktBlockeratOrsak`, vars union bara innehåller kapacitets-, energi- och
inmatningslägesfel. Planen lägger till fält på klassen men definierar ingen orsak för
saknade/ogiltiga policyfält och visar inget konstruerbart anrop. Det blir antingen ett
typfel eller en missvisande befintlig orsak.

**Begärd rättning:** ge förkontrollen samma scope som fasaden, exempelvis
`forkontrolleraPolicyIndata(..., omfattning: Omfattning)`, och filtrera identiskt med
`harledResultatstatus`; båda årsproduktvägarna skickar uttryckligen `'annual'`. Definiera
också en typkorrekt konstruktorväg, exempelvis nya orsaker `missing_policy_fields` och
`invalid_policy_fields` plus ett optionsobjekt för fältlistorna. Testa en syntetisk policy
med samtidiga monthly-/annual-krav och bevisa att respektive produkt bara kräver sitt scope.

### P1 — produktförmågan läser fel objekt och tabellens energisystemrad verkställs inte

V13:s kod på inventering rad 2829–2833 gör:

```ts
const policy = kontraktsgatadPolicy(prisar);
return policy?.kallenergiArsserieBindning !== undefined;
```

Dagens `kontraktsgatadPolicy()` returnerar `KontraktsgatadPolicy | undefined`, där objektet
har fälten `{ policy: Tariffpolicy, harAnnualInverse }`. Bindningen ligger alltså på
`gated.policy.kallenergiArsserieBindning`, inte på wrapperobjektet. Skissen kompilerar inte
och skulle inte ge den utlovade Stockholm-`true`-grenen.

Tabellen säger dessutom att icke-fjärrvärmesystem ger `false`, men
`stodjerAktuellArskostnad(prisar)` får inget energisystem. Wrappern på rad 2941–2951
kontrollerar inte heller `inputs.energySystem`. Ett direkt inputobjekt för ett annat
energisystem som fortfarande bär Stockholms leverantörs-ID kan därför passera
tariffkontrollen, i strid med tabellen.

**Begärd rättning:** använd exempelvis
`const gated = kontraktsgatadPolicy(prisar); return
gated?.policy.kallenergiArsserieBindning !== undefined`. Låt
`calcResultForOnskadTyp` först kräva `inputs.energySystem === 'fjarrvarme'` innan den
frågar tariffens förmåga. Den publika `beraknaArsprodukt` ska fortsatt göra tariffguarden
själv. Visa och testa exakt false/false/false/true för annat system, legacy, Sandviken och
Stockholm.

### P1 — den konkreta argumentbyggaren använder icke-existerande API och är inte delad

Inventering rad 2912–2926 använder `inputs.rumsvarmeAngiven`, `inputs.totalMwh`,
`skalaUppRumsvarmeTillTotal(inputs)` och `mwhProvenansBekraftad(inputs)`. Inget av dessa
fält eller hjälpfunktioner finns i dagens källträd. `KalkylatorInputs` har `energyMwh` och
`energyScope`; dagens `calcResult` skapar lokala `energyMwh`, `userProvidedEnergy`,
`rumsvarmeAngiven`, `totalMwhForTariff` och `mwhProvenansBekraftad`. Skissen är därför
fortfarande inte typkorrekt eller direkt implementerbar trots att V13 kallar funktionerna
befintliga.

Rad 2929–2934 säger dessutom att `calcResult` ska fortsätta bygga sina tre argumentobjekt
inline. Då har aktuell-årskostnad och besparing två separata implementationer av just den
scope-/provenienslogik som `argsFranInputs` skulle dela. Det motsäger V13:s inledning, som
säger att besparingsvägen lägger min/mid/max-fälten ovanpå den delade bastypen.

`onskadTyp` är fortfarande obligatoriskt på `KalkylatorInputs`, trots att V12-granskningen
krävde ett bakåtkompatibelt default eller en lista över alla migrerade anrop. Den lästa
koden innehåller cirka 85 typade deklarationer/anrop; batchens fillista nämner inte den
migrationen.

**Begärd rättning:** skriv skissen med dagens faktiska fält eller deklarera och definiera
varje ny hjälpfunktion. En möjlig gemensam väg är att beräkna `energyMwh =
calcEnergyMwh(inputs)`, `userProvidedEnergy`, scope-uppskalad `totalMwh` och proveniens i en
enda hjälpare; `calcResult` använder sedan samma basobjekt och lägger till
`paverkbarMwh`/respektive min–mid–max-grad. `beraknaArsprodukt` använder bara basobjektet och
kräver `confirmed_mwh`. Gör `onskadTyp` valfritt med default `'besparing'`, eller lägg hela
callsite-migrationen och dess typkontroll uttryckligen i batch 0. Definiera även den i dag
saknade typen `GenereradPrisarspost` eller använd en befintlig härledd pristyp.

## P2-fynd

- Commit `b467d0a` refererar och indexerar granskning `2026-09-09-003`, men själva filen
  `conversations/reviews/2026/09/2026-09-09-omgranskning-tariffinventering-v12.md` är
  fortfarande ospårad och ingår inte i committen. V13 är därför inte självbärande vid en
  ren checkout. Ta med både den och denna nya granskning i nästa dokumentationscommit.
- V13:s adapterbeskrivning är nu konsekvent: `bygg_ts()` kör bara reverse-ledet,
  `_bearbeta_leverantorsfil()` hämtar policy ur `policyregister.py`, och den fulla
  katalogvägen äger katalogkontrollen. Bevara den utan ny omkonstruktion.

## Verifieringar

- `skills@b467d0a` ändrar bara V13-dokumentation och konversationslogg. Ingen produktkod,
  tariffdata, genererad frontendfil eller aktivering ändrades.
- `git diff --check a773524..b467d0a` är rent. Den verifierbara committiden är
  `2026-09-09T09:40:00+02:00`.
- Produktrepoerna är rena och oförändrade på `enkey-agents@fd8f8da` och
  `neptune_academy@f1df177`. De verkliga typerna för `KalkylatorInputs`,
  `KontraktsgatadPolicy`, `KontraktBlockerat`, `BesparingsvardeArgs`, `calcResult` och
  `Resultatstatus` lästes som granskningsbas.
- V13 innehåller 78 bastariffrubriker och redovisar 78 bas + 14 varianter = 92 samt
  dispositionen 7 implementerade, 55 redo och 30 blockerade. Inget sakstatusfynd motiverar
  en flytt i denna runda.
- Lokal `main` är 17 commits före `origin/main` och inte efter. V13 är inte godkänd för
  push.
- Inga fulla produkttester kördes eftersom V13 bara ändrar planeringsdokumentation och de
  beskrivna nya gränssnitten ännu inte finns i kod.

## Rättningsbeställning till Claude

1. Leverera `tariffinventering-v14.md` och `batchplan-v14.md`; ändra inte V13 i efterhand.
2. Slut parser-/valideringstyperna, inklusive råformsgrindar, en orsaksunion och samma
   returfältnamn genom hela kedjan.
3. Gör förkontrollen omfattningsmedveten och visa en konstruerbar
   `KontraktBlockerat`-väg för saknade respektive ogiltiga policyfält.
4. Rätta `kontraktsgatadPolicy`-åtkomsten till `.policy`, och verkställ energisystemraden i
   förmågetabellen före tariffkontrollen.
5. Skriv argumentbyggaren mot verkliga `KalkylatorInputs`-fält och låt både aktuell kostnad
   och de tre besparingsanropen återanvända samma basobjekt. Lös `onskadTyp`-kompatibiliteten
   och definiera pristypen.
6. Behåll V13:s lösta `undefined`-argument, domänägda förkontrollsprincip, dubbla
   produktguard, adaptersemantik, metadata och dispositionerna 7/55/30 om ingen sakstatus
   ändras.
7. Ta med de ospårade granskningarna `2026-09-09-003` och `2026-09-09-004` i nästa
   fokuserade dokumentationscommit, logga verklig hash/tid och stanna för omgranskning.
8. Ändra ingen produktkod eller tariffdata och pusha inte.
