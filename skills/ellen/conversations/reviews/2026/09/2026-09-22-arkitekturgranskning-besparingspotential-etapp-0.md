---
review_id: "2026-09-22-004"
date: "2026-09-22"
reviewer: Codex
scope: "Preliminär Optimate-potential för alla valbara 2026-tariffer; Etapp 0"
decision: "Inventering och Stockholmsprototyp lokalt verifierade; ingen portföljaktivering godkänd"
---

# Arkitekturgranskning: från Stockholm till hela tariffportföljen

## Beslut och underlag

Etapp 0 har en reproducerbar [2026-matris](../../../../Fjarrvarmetariffer/besparingspotential-tackningsmatris-2026.md)
och [maskinläsbar JSON](../../../../Fjarrvarmetariffer/besparingspotential-tackningsmatris-2026.json).
Den utgår från Neptunes genererade 2026-snapshot, har källhash och täcks av
sex riktade tester. Det finns 75 valbara produkt-ID:n: 74 verkliga och ett
syntetiskt riksgenomsnitt. Åtta har en befintlig besparingsväg, medan 67
kontraktsstyrda produkter endast har aktuell årskostnad. Det är **inte**
75 nygodkända Optimate-scenarier. Varje rad har därför status `not_reviewed`.

Den mekaniska granskningsordningen är 2 produkter utan identifierat
effekt-/flödesberoende, 13 med effektberoende, 48 med flöde, temperatur
eller månadsserie och 12 med behörighetsregel. Grupperna är disjunkta som
arbetsvågor men beroendena överlappar: 71 produkter har debiterbar
kapacitetsdel, 60 flödes-/temperaturberoende, 61 historik-/bandmarkeringar,
12 kräver nummerserie och 12 har behörighetsregel. Fyra saknar
kapacitetsdebitering: Gotlands båda taxor, Mälarenergis 2–4 lägenheter och
Sundsvall Indal/Liden/Lucksta. Att en produkt är enkel i matrisen säger
inget om hur mycket Optimate faktiskt sparar där.

Stockholms separata lokala prototyp är testad och committad i Neptune som
`86be35ae4c5e3f021c97c40d0473ab3d3427b127`. Den är inte pushad och
ändrar inte `stodjer_besparing=false`. Den prissätter 15/20/25 procent
mindre styrbar rumsvärme i samma tariff; lägre debiterbar effekt visas
endast som separat, villkorad känslighet. Tappvarmvattenantagandet på 18
procent kommer från ett kundexempel och får inte användas som generell
portföljstandard.

## Arkitekturfynd

1. **Årskostnadsvägen är rätt beräkningskärna, men resultatet är för grovt.**
   `beraknaArsprodukt` i `neptune-marketing/src/utils/besparingsvarde.ts`
   validerar kontraktsindata, väljer energiprofil och använder befintlig
   tariffmotor. Den publika returtypen lämnar dock främst ett totalbelopp.
   Ett gemensamt scenario behöver prisled från samma motor: energi,
   fast/kapacitet, retur/flöde och övriga justeringar. Då kan UI visa
   exakt vilka led som ändrats, hållits kvar eller inte går att skatta.
   Här ska motorns interna kostnadsled exponeras säkert, inte nya
   prisformler kopieras till React.
2. **Befintlig besparingsväg är inte ett portföljkontrakt.**
   `beraknaBesparingsvardeKontrakt` kräver `stodjer_besparing=true` och
   fördelar energi med den generiska `fordelaEnergi`-profilen, medan
   `beraknaArsprodukt` accepterar en uttrycklig månadsserie för de flesta
   kontraktsprodukter. Att massändra flaggan skulle kringgå skillnaden
   mellan faktiskt stöd och ett preliminärt scenario. Lägg en egen,
   tariffgranskad scenarioförmåga utan att öppna den formella besparingsvägen.
3. **Fysik och fakturering har olika klockor.** Samma referens- och
   efterår ska använda identiskt prisår, produkt och historiskt
   `billing_state`. Endast styrbar rumsvärme ändras i huvudscenariot.
   Leverantörens debiterbara effekt kan bygga på tidigare mätperiod,
   valt band eller avtal; en skattad 20-procentig fysisk toppminskning
   får därför inte direkt minska effektavgiften. Flöde, returtemperatur,
   kölddygnsvolym och kontraktsgrupp behöver uttryckliga eftervärden
   eller ska förbli oförändrade med synlig reservation.
4. **Vissa produkter kan inte behandlas med en generell månadsserie.**
   Vattenfalls tolv Standard/Spetsig-varianter använder en särskild
   energiprofil och behörighetsregel i `beraknaArsprodukt`; den vägen
   kan inte få ett nytt månadsfält som motorn sedan ignorerar. Produkten
   får inte bytas automatiskt om hypotetisk energi skulle ändra
   behörighetskvoten. Dokumenterade exkluderingar för överuttag och
   industriavdrag måste visas även i ett efter-scenario.
5. **Matrisen är inventering, inte kausal analys.** JSON fångar
   källreferens, mätupplösning, fält, historikmarkörer, specialregler och
   dokumenterade exkluderingar. Den avgör ännu inte för varje enskilt
   prisled om det ska ändras, hållas låst eller blockeras vid en
   rumsvärmeändring. Den klassningen och oberoende facit hör till nästa
   implementeringsgrind. `katalog` i källfältet är en proveniens till
   den hashade källkatalogen, inte en direktlänk till leverantörens sida.

## Rekommenderat nästa avgränsade arbete

Bygg ett tariffneutralt, typat före/efter-kontrakt med samma prisår och
produkt för båda tillstånden: tolv värden köpt värme, tolv värden styrbar
rumsvärme, övrig last, proveniens, fryst faktureringshistorik och
scenarioantaganden. Resultatet ska innehålla före-/efterkostnad per
prisled, sparad MWh, differens även om den är noll/negativ, och en
orsak till varje spärr. Avvisa negativa värden och serier som inte
summerar. Återanvänd befintlig tariffmotor och befintliga
policy-/behörighetskontroller.

Gör därefter en liten pilot med Sundsvall Indal/Liden/Lucksta, som
saknar kapacitets- och flödesdebitering i snapshoten. Verifiera att
referensbeloppet är **exakt samma** som dagens årskostnad och att
efter-scenariot bara ändrar styrbar energi. Behåll Stockholm som ett
separat regressionstest för månadsserie, returavgift och villkorad
effekt. Fortsätt sedan i matrisens familjeordning; varje ny produkt får
egen beroendeklassning och test innan scenarioförmågan öppnas.

Ingen ny tariff har aktiverats, ingen annan leverantör har fått ett
Optimate-resultat och ingen push är gjord genom denna granskning.
