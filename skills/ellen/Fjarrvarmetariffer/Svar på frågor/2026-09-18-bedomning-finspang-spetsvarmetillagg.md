---
datum: "2026-09-18"
bolag: "Finspångs Tekniska Verk"
fraga: "A5 — omfattning och tillämpning av spetsvärmetillägg 2026"
bedomning: "besvarad — ej tillämplig 2026"
produktblockerande_fore_svar: true
dispositionsandring: true
personuppgifter_publicerade: false
---

# Bedömning av Finspångs svar om spetsvärmetillägg

## Slutsats

Finspångs Tekniska Verk bekräftar att texten om spetsvärmetillägg finns i
prislistan för 2026, men att något sådant tillägg inte har debiterats kunder
och att bolaget för närvarande saknar en tillämpad modell för debiteringen.
Bolaget avser att se över formuleringen inför kommande uppdateringar.

Den ej materialiserade variantposten
`finspangs-tekniska-verk-finspang-2026--spetsvarmetillagg` ska därför klassas
`not_applicable` för 2026, inte `blocked_external_info`,
`ready_to_implement` eller `implemented_source_verified_annual`. Det finns
ingen faktisk debiteringsregel att modellera för 2026 och kalkylatorn får
inte konstruera ett 20-procentigt påslag från prislistans oklara formulering.

Den redan implementerade bastariffen
`finspangs-tekniska-verk-finspang-2026` påverkas inte. Svaret medför ingen
ny katalograd, prisändring, implementation eller tariffaktivering.

## Dispositionskonsekvens

När källnormaliseringen genomförs flyttas exakt en av de 92 frusna
dispositionsposterna från `blocked_external_info` till `not_applicable`:

- före: **74 implementerade / 2 redo / 16 blockerade / 0 ej tillämpliga**;
- efter: **74 implementerade / 2 redo / 15 blockerade / 1 ej tillämplig**.

Antalet fysiska katalograder och produkter är oförändrat. Ändringen gäller
bara den separat spårade, ej materialiserade variantpostens källstatus.

## Källkontroll och dataskydd

Det mottagna originalmejlet ligger lokalt i samma mapp men innehåller
personuppgifter och ska inte committas. Denna bedömning är den sanitiserade,
versionsstyrningsbara källposten.

- mottaget: 2026-09-17;
- avsändardomän: `finspangstekniska.se`;
- SPF: godkänd i mejlets transporthuvud;
- DMARC: inget policyrecord fanns (`dmarc=none`), alltså ska svaret inte
  beskrivas som DMARC-godkänt;
- DKIM: inget verifierat resultat finns i det granskade transporthuvudet;
- originalfilens SHA-256:
  `8fbbbac67bbd681c0f324fceb7382e0c9672d596423a66ce0db5e8fa8a6952b9`;
- bilagor: inga tariffbilagor; två inbäddade PNG-bilder hör till
  mejlsignaturen.

## Uppföljning

Ingen följdfråga behövs för 2026 års kalkyl. Om en senare prislista eller
ett kundavtal inför ett faktiskt spetsvärmetillägg måste den nya
debiteringsmodellen källgranskas från början innan en variant får byggas
eller aktiveras.
