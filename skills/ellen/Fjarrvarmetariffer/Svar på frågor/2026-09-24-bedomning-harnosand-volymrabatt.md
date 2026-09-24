---
datum: "2026-09-24"
bolag: "Härnösand Energi & Miljö"
fraga: "A2 / R02 — vilken av intervalltabellen och räkneexemplet styr volymrabatten 2026?"
bedomning: "besvarad"
produktblockerande_fore_svar: true
dispositionsandring: true
personuppgifter_publicerade: false
---

# Bedömning av HEMAB:s svar om volymrabatt

## Slutsats

Härnösand Energi & Miljö (HEMAB) bekräftar att volymrabatten beräknas
efter intervalltabellen i bolagets system och att tabellen används vid
fakturering. Det publicerade räkneexemplet är felaktigt.

Det stänger den externa frågan A2/R02 för
`harnosand-energi-miljo-harnosand-2026`. Ingen följdfråga till
leverantören behövs om 2026 års volymrabatt.

## Beräkningskontrakt

Den officiella prislistans intervall ska behandlas som en marginaltrappa:

| Årsvolymdel | Avdrag exkl. moms |
| --- | ---: |
| 0–500 MWh | 0 kr/MWh |
| över 500 till 750 MWh | 18,40 kr/MWh |
| över 750 till 1 000 MWh | 33,10 kr/MWh |
| över 1 000 till 1 500 MWh | 42,90 kr/MWh |
| över 1 500 till 2 000 MWh | 65,00 kr/MWh |
| över 2 000 MWh | 130,00 kr/MWh |

För prislistans 1 750 MWh-fall blir korrekt avdrag:

`250 × 18,40 + 250 × 33,10 + 500 × 42,90 + 250 × 65,00`

`= 4 600 + 8 275 + 21 450 + 16 250 = 50 575 kr` exklusive moms.

Prislistans redovisade 45 050 kr bygger i stället felaktigt på att hela
delen 1 001–1 750 MWh får 42,90 kr/MWh. Det beloppet får inte användas som
facit. Rabatten baseras på uppmätt energianvändning per kalenderår,
sammanställs och avräknas på årets sista faktura.

## Övriga verifierade prisregler

Den officiella 2026-prislistan anger dessutom följande, vilket ska ingå i
årsberäkningen:

- energipris 642 kr/MWh december–mars och 360 kr/MWh april–november;
- effektavgift 1 266 kr/kW och år, uppdelad i tolv månadsdelar;
- egenvald abonnerad effekt med lägsta värde 5 kW och tolv kalendermånaders
  bindningstid;
- vid ett debiteringsgrundande dygnsmedeluttag över vald effekt korrigeras
  hela bindningstidens effektavgift med
  `max(0, faktiskt effektuttag − vald effekt) × 1 266 × 1,3`.

Motorn ska inte själv gissa vilket dygnsvärde HEMAB lagt till grund för en
korrigering. Ett sådant tillägg ska beräknas från ett synligt,
leverantörs- eller kundangivet debiteringsgrundande effektuttag. Saknas
värdet ska beräkningen blockeras eller posten uttryckligen markeras som
exkluderad; ett tyst nollantagande är inte tillåtet.

## Konsekvens för implementation och disposition

Tariffen kan nu flyttas källmässigt från `external_answer_required` till
`source_resolved_implementation_pending`. Den ska inte aktiveras bara för
att källfrågan är stängd: motor-, policy-, UI- och acceptanstest måste
först granskas bakom befintlig `investigation`-spärr.

Den redan implementerade typen `marginal_annual_volume_discount` för
Gävle kan återanvändas för själva marginalaritmetiken. HEMAB skiljer sig
genom att avdraget avräknas på årets sista faktura, medan Gävles avdrag
betalas ut månadsvis. Den skillnaden ska uttryckas maskinläsbart och
valideras, även om båda ger samma avdrag i en ren årssumma.

Före källnormaliseringen är den skarpa dispositionen
**75 implementerade / 2 redo / 14 blockerade / 1 ej tillämplig av 92**.
Efter en ren källnormalisering blir den **75 / 3 / 13 / 1**. Först efter
separat granskad implementation och aktivering blir den **76 / 2 / 13 /
1**. Antalet fysiska katalograder ändras inte.

## Källkontroll och dataskydd

Originalmejlet ligger lokalt i samma mapp men innehåller personuppgifter
och ska inte committas. Denna bedömning är den sanitiserade,
versionsstyrningsbara källposten.

- mottaget: 2026-09-24;
- avsändardomän: `hemab.se`;
- transporthuvudet innehåller godkända SPF- och DMARC-resultat; inget
  godkänt DKIM-resultat har identifierats;
- originalfilens SHA-256:
  `a4434f7a07a58532a8e8ddd820e7557b9cf8a4b2a1e835317378214cda435de8`;
- officiell 2026-prislista hämtad från HEMAB 2026-09-24, SHA-256:
  `abb93a2c30be3d33fd6d30e8de6af1963b2bf7e507595abda806338320775db8`.

Den sistnämnda hashen är identisk med katalogkällan `13_1`, trots att
`13_1` har en inaktuell 2025-titel och Prisdialogen-URL. Källmetadata ska
normaliseras till den aktuella officiella HEMAB-filen utan att den äldre
proveniensen skrivs bort ur historiken.

## Uppföljning

Nästa steg är en avgränsad, spärrad implementation med ett oberoende
handräknat 1 750 MWh-facit, gränstester vid samtliga band, Python–
TypeScript-paritet och ett synligt kontrakt för effektkorrigeringen.
Aktivering och push får ske först efter separat Codex-granskning.
