---
datum: "2026-09-23"
bolag: "Gävle Energi"
fraga: "A3 / R16 — månad då ackumulerad kalenderårsvolym passerar ett rabattband"
bedomning: "besvarad"
produktblockerande_fore_svar: true
dispositionsandring: false
personuppgifter_publicerade: false
---

# Bedömning av Gävle Energis svar om volymavdrag

## Slutsats

Gävle Energis svar och bifogade kalkylblad bekräftar att avdraget är
**marginalt**. Under den månad då ackumulerad kalenderårsvolym passerar
100 MWh får bara delen över 100 MWh avdrag. Tidigare månaders volym
räknas inte om retroaktivt. Efter passagen får kommande volym avdrag med
satsen i det aktuella intervallet.

Leverantörens exempel har 94,57 MWh ackumulerat efter april och 9,65 MWh
i maj. Majs rabattgrundande volym blir därför 4,22 MWh, inte hela 9,65
MWh och inte noll. För 193 MWh helår blir den rabattgrundande volymen
93 MWh i intervallet 101–250 MWh:

`93 MWh × 35 kr/MWh = 3 255 kr` i avdrag exklusive moms.

Rabatten beräknas och utbetalas månadsvis. Detta stänger den externa
frågan R16 för `gavle-energi-gavle-2026`.

## Beräkningskontrakt

Katalogens publicerade nedre gränser och avdragssatser ska behandlas som
en marginaltrappa:

| Årsvolymdel | Avdrag exkl. moms |
| --- | ---: |
| 0–100 MWh | 0 kr/MWh |
| över 100 till 250 MWh | 35 kr/MWh |
| över 250 till 500 MWh | 55 kr/MWh |
| över 500 till 1 500 MWh | 75 kr/MWh |
| över 1 500 till 2 500 MWh | 95 kr/MWh |
| över 2 500 MWh | 125 kr/MWh |

För en årskostnad kan avdraget beräknas som summan av volymen inom
varje passerat intervall gånger intervallets sats. För en månadsvis
redovisning måste kalenderårets ackumulerade volym föras vidare och en
tröskelmånad delas mellan berörda intervall. Motorns kostnadsjustering
ska vara negativ.

Leverantörens bilaga demonstrerar gränsen 100 MWh. Tillämpningen vid
varje senare gräns följer samma marginalprincip tillsammans med den
publicerade bandtabellen, men ska bindas med separata gränstester vid
100, 250, 500, 1 500 och 2 500 MWh.

## Konsekvens för implementation och disposition

Den råa katalogposten använder redan typen
`marginal_annual_volume_discount`, men denna typ finns ännu inte i
Python- eller TypeScriptmotorns justeringsregister. Den befintliga typen
`volume_discount` får inte återanvändas: den väljer ett enda band från
föregående års energi och applicerar vald sats på all köpt energi, vilket
är en annan affärsregel.

Gävle flyttas därför källmässigt från `external_answer_required` till
`source_resolved_implementation_pending`. Den skarpa dispositionen är
fortsatt **74 implementerade / 2 redo / 15 blockerade / 1 ej tillämplig
av 92** tills en separat, granskad implementation och aktivering är
genomförd. Inom den blockerade mängden minskar de externt obesvarade
posterna från fem till fyra och de källösta implementationsposterna ökar
från tio till elva.

Implementationsrundan behöver även synkronisera Gävlepostens äldre,
motstridiga kapacitetsmetadata med den redan verifierade prisregeln:
ingen separat fast avgift och kalenderdagsperiodisering av
kapacitetspriset. Det är en källnormalisering, inte något som ska gissas
av motorn.

## Källkontroll och dataskydd

Originalmejlet ligger lokalt i samma mapp men innehåller personuppgifter
och ska inte committas. Denna bedömning är den sanitiserade,
versionsstyrningsbara källposten. Filnamnets ämnesförkortning "GEAB" ska
inte förväxlas med Gotlands Energi; avsändare och innehåll gäller Gävle
Energi.

- mottaget: 2026-09-23;
- avsändardomän: `gavleenergi.se`;
- SPF, DKIM och DMARC: godkända i mottagande transporthuvuden;
- originalfilens SHA-256:
  `5f34055e4ad704e81cca464cace4e203eaabc9fe0e7c3716673539cefde9a7a4`;
- tariffbilaga: `Volymrabatt.xlsx`, SHA-256
  `77c07371d88ddf9ff079b64c8b1362cea405ed42593befd999407d1801f59236`.

## Uppföljning

Ingen ny fråga till Gävle Energi behövs för 2026 års marginala
volymavdrag. Nästa steg är en avgränsad källnormalisering och därefter en
separat motor-/produktimplementation med oberoende handräknat facit,
Python–TypeScript-paritet och mutationstest för samtliga bandgränser.
