---
proposal_id: "2026-09-22-003"
version: 2
date: "2026-09-22"
author: Codex
status: "Mål beslutat av Robert; Etapp 0-inventering lokal, scenariomotor ännu ej byggd"
relates_to: "Lokal Stockholm-prototyp 2026-09-21-003; Git-paus 2026-09-21-004"
---

# Plan: preliminär Optimate-potential för alla godkända fjärrvärmeprodukter

## Mål och mätbar omfattning

Robert har bestämt att funktionen som nu prövas för Stockholm Exergi ska
byggas ut till **samtliga godkända och valbara fjärrvärmeprodukter** i
kalkylatorn. Täckning mäts på nät-/produkt-/tariffnivå, inte bara på
bolagsnamn: ett bolag kan ha flera nät eller taxor med skilda regler.
Framtida godkända produkter ska omfattas av samma täckningsgrind.

Den lästa 2026-snapshoten i
`neptune-marketing/src/data/tariffer.generated.ts` innehåller 75 valbara
produkt-ID:n: 74 verkliga nät-/produktval och ett syntetiskt
riksgenomsnitt. Generatorns huvud anger 73 källgodkända katalograder;
**katalograder och produktval är olika mått**. Av de 75 produktvalen har
åtta en äldre besparingsväg (inklusive riksgenomsnitt och Sandviken) och
67 kontraktsstyrda produkter är satta till `stodjer_besparing=false`.
Stockholms nya Optimate-vy ligger separat ovanpå dess
`aktuell_arskostnad` och är ännu bara en lokal, opushad prototyp.

Mått för leverans: **74/74 verkliga valbara 2026-produkter** ska kunna ge
ett meningsfullt, tydligt märkt energibesparingsscenario när det nödvändiga
underlaget finns; riksgenomsnittet behålls som tydligt syntetisk referens.
Ett ”kan inte beräknas” utan konkret databehov räknas inte som uppnådd
täckning. Kommande år och nygodkända tariffer ska läggas till genom samma
produktgrind, inte genom kopierade React-grenar.

Detta mål innebär **inte** att 15–25 procent är ett uppmätt Optimate-utfall,
att 20 procent lägre fysisk toppeffekt ger 20 procent lägre fakturerad effekt,
eller att temperatur-/flödesavgifter automatiskt förbättras. Alla belopp är
uppskattningar tills de kan verifieras med kundens data och jämförbar komfort.

## Produktkontrakt för varje tariff

Kunden ska kunna börja med årsenergi och leverantör, men fylla på med
fakturans månads-/effekt-/flödesuppgifter när de finns. Resultatet ska visa:

1. Nuvarande uppskattad årskostnad med vald 2026-tariff, inklusive moms,
   prisår, nät/produkt och antagna eller angivna underlag.
2. Tre **preliminära energiscenarier**: 15, 20 och 25 procent mindre
   *styrbar rumsvärme*, sparade MWh, skattad kostnadsskillnad samt
   årskostnad efter. Tappvarmvatten och andra icke styrbara laster ska inte
   minskas. Enbart totalvärme kräver en redovisad, ändringsbar skattning av
   den styrbara andelen; Stockholms 18-procentiga kundexempel får inte
   tyst göras till universell regel.
3. Separata, **villkorade** känsligheter för debiterbar effekt, flöde och
   returtemperatur endast där tariffregel, mätupplösning och ett fysiskt
   rimligt eftervärde finns. De adderas inte automatiskt till huvudtalet.
4. Skillnad mellan fysisk toppeffekt, historiskt/avtalat debiteringsunderlag
   och årskostnad. Visa när en möjlig effektändring först kan slå igenom.
5. Kvalitetsstatus för varje storhet: angiven/leverantörsverifierad,
   schablonskattad, villkorad eller saknad. Komfortkravet (t.ex. avtalat
   inomhusklimat) ska anges som förutsättning, inte som redan verifierat.

De två befintliga förmågorna `stodjer_aktuell_arskostnad` och
`stodjer_besparing` ska inte slås ihop eller massändras till `true`.
Inför en **egen förmåga för preliminärt Optimate-scenario**, som kan
aktiveras tariff för tariff efter test. Den formella befintliga
besparingsprodukten förblir spärrad där dess kontrakt inte är uppfyllt.

## Genomförande i fyra etapper

### 0. Lås baslinjen och inventera beroenden

- Granska och bevara de två opublicerade Stockholm-ändringarna enligt
  `conversations/handoffs/2026/09/2026-09-21-paus-stockholm-optimate.md`.
  Gör ingen bred tariffaktivering eller blind Git-commit av den smutsiga
  arbetskopian.
- Generera en **75-raders täckningsmatris** ur skarp tariffdata med ID,
  nät/produkt, prisår, källa, aktuell kostnadsförmåga, nuvarande
  besparingsförmåga, erforderliga fakturafält, mätupplösning, historik,
  energi-/effekt-/flödes-/temperaturregler, dokumenterade exkluderingar
  och scenarioförmåga. Matrisen ska vara reproducerbar i test, inte ett
  handskrivet statuspåstående.
- Klassificera varje prisleds beroenden: ändras med köpt energi, är låst
  under aktuell fakturaperiod, beror på historik/avtal eller kräver ny
  mätning. Frys inte exempelvis flöde eller returtemperatur i en
  före/efter-jämförelse utan att namnge det antagandet.

### 1. Bygg en gemensam scenariomotor

- Lyft den återanvändbara delen ur `stockholmOptimatePotential.ts` till
  ett typat, tariffneutralt scenariokontrakt. Återanvänd samma
  deterministiska tariffmotor, prisår, momsgrund och validerade
  `Tariffberakningsunderlag` som dagens årskostnad; kopiera inte prisformler
  till React eller en parallell procentmotor.
- Definiera två kompletta jämförelsescenarier vid **samma tariffversion**:
  referens och 15/20/25-procentig ändring av en explicit styrbar
  månadsserie. Lagra separat köpt totalvärme, rumsvärme, varmvatten,
  historiskt `billing_state` och scenarioantaganden. Avvisa negativ eller
  ofullständig månadsenergi.
- Utöka kostnadsresultatet med spårbara prisled så energiförändring kan
  särredovisas och icke påverkade avgifter hållas vid referensvärdet.
  Tariffberoende omräkning av effekt, flöde, retur eller prisgrupp ska bara
  göras av en uttrycklig regel/adapter. Visa även negativ eller noll
  kostnadsskillnad; kläm inte till en positiv besparing.
- Behåll existerande specialregler som historisk rabatt/effektgrupp och
  Vattenfalls Standard/Spetsig-behörighet. En hypotetisk energiminskning
  får inte tyst byta kundens nuvarande tariffprodukt mitt i året.

### 2. Aktivera familjevis, inte bolag för bolag med kopierad kod

Följande ordning är en **föreslagen teknisk ordning**, inte en ny
godkännandesignal eller tariffaktivering:

1. Ren energi och befintliga besparingsval: bevara/regressionstesta
   riksgenomsnittet, legacyprodukterna och Sandviken; prova en
   energienkel kontraktsprodukt som Sundsvall Indal/Liden/Lucksta.
2. Energi + kapacitet/band: håll debiterbar kapacitet och historiskt
   gruppval konstant i huvudscenariot; lägg eventuella effektfall i
   separat villkorad vy.
3. Energi + flöde/retur/avkylning: inför explicita flödes- och
   temperaturantaganden, med Lidköping/Stockholm som testfall. Ingen
   gratis bonus från ett ogrundat eftervärde.
4. Historik-, profil- och behörighetsstyrda produkter: bland annat
   Vattenfalls energiprofil/Standard/Spetsig och flera nätvarianter.
   Bevisa att kundens aktuella kontrakt och tidigare års mätperiod inte
   råkar räknas om som om scenariot redan hade inträffat.

Varje våg avslutas med en uppdaterad täckningsmatris: fungerande
huvudscenario, villkorade delkomponenter, krav på ytterligare kunddata
och konkreta avvikelser. Utrednings-/icke-godkända tariffer ligger utanför
scope tills de har passerat sin vanliga källa- och aktiveringsgrind.

### 3. Verifiera och publicera

- För varje godkänd produkt: ett automatiskt före/efter-test där
  referenskostnaden är samma som den redan godkända årskostnadsvägen;
  seriens summa och mätgräns bevaras; sparad rumsvärme är 15/20/25 procent
  av *styrbar* last; prisledsummeringen är konsistent; inga dolda
  kapacitets-/flödes-/temperaturvinster uppstår.
- Oberoende handräknade eller publicerade årsexempel för varje tariffamilj,
  gränsfall för band, rabatter, säsong, noll sommarvärme, historiska toppar,
  behörighet och saknade data. Kundfaktura används när en kund lämnar den
  eller uttryckligen ber om kontroll — den krävs inte generellt för
  källverifierad, tydligt uppskattad årskalkyl.
- Komponent-, generator-/policy-, React- och Chromiumtester. UI ska visa
  samma semantik i mobil och desktop, även när ett delscenario blockeras.
  En regression i en produkt ska inte sänka hela portföljens resultatsida.
- Separat granskningsgrind per familj, därefter lokal aktivering och
  normal fast-forward-push enligt projektets befintliga flöde. Ingen
  massaktivering genom att ändra alla `stodjer_besparing`-flaggor.

## Definition av klart

En aktuell godkänd verklig produkt räknas som täckt först när dess
preliminära energiscenario går att köra genom vald tariff med rimlig,
redovisad styrbar andel; beräknad referenskostnad matchar den befintliga
årskostnaden; alla nödvändiga uppgifter kan fyllas i eller skattas med
synlig osäkerhet; tariffspecifika undantag är testade; och användaren ser
vilka kostnadsled som **inte** har antagits minska. Portföljgrinden är
74/74 nuvarande verkliga produktval samt särskilt testat syntetiskt
riksgenomsnitt, och ska följa med när fler produkter godkänns.

Planen beslutar mål och arbetssätt men startar **ingen** ny kodändring,
tariffaktivering, automatisk Claude-signal eller push. Nästa konkreta
leverans är etapp 0:s maskinellt reproducerbara täckningsmatris och en
kort arkitekturgranskning av den gemensamma scenariomotorn.

## Statusuppdatering 2026-09-22

Texten ovan beskriver planens läge när den skrevs. Efter Roberts klartecken
har Stockholm-prototypen lokalt committats i Neptune som
`86be35ae4c5e3f021c97c40d0473ab3d3427b127`; ingen push eller
tariffaktivering har gjorts. En [maskingenererad täckningsmatris](../../../../Fjarrvarmetariffer/besparingspotential-tackningsmatris-2026.md)
och en [arkitekturgranskning](../../../reviews/2026/09/2026-09-22-arkitekturgranskning-besparingspotential-etapp-0.md)
finns lokalt. Matrisens tekniska sortering är inte den kausala
prisledsklassning som krävs innan nya scenarioförmågor kan godkännas.
