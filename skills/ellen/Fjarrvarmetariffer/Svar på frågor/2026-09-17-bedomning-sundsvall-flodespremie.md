---
datum: "2026-09-17"
bolag: "Sundsvall Energi"
berorda_nat:
  - "Matfors"
  - "Kvissleby/Njurunda"
fraga: "B2 — tillgång till månadsvis nätvärde Q/W för flödespremie"
bedomning: "besvarad"
produktblockerande_fore_svar: false
dispositionsandring: false
personuppgifter_publicerade: false
---

# Bedömning av Sundsvall Energis svar om flödespremie

## Slutsats

Sundsvall Energi bekräftar att företagskunden kan hämta både sitt eget
månadsvisa `Q/W` och nätets månadsmedel för `Q/W` på fakturan och på
[Mina sidor](https://minasidor.stadsbacken.se/login?path=/). Uppgifterna anges
i `m³/MWh`.

Svaret gäller den skickade frågan för både Matfors och Kvissleby/Njurunda.
Det löser den frivilliga precisionsfrågan B2. De två tarifferna var redan
klassade `source_resolved_implementation_pending`, så den skarpa
dispositionen och klassningen `22 källösta / 6 externt blockerade` ändras
inte av detta svar.

## Bindande produktkontrakt

Vid en uppskattad årsberäkning ska kalkylatorn för var och en av
debiteringsmånaderna januari–april och oktober–december kräva:

1. kundens faktiska månadsvärde `Q/W`, i `m³/MWh`; och
2. samma månads nätmedel `Q/W`, i `m³/MWh`.

Värdena ska anges från kundens faktura eller Mina sidor. Ingen publik eller
inbyggd nätserie ska användas som dold standard. Saknas något av de fjorton
värdena ska flödesdelen stoppas tydligt i stället för att anta noll eller ett
exempelvärde.

Mejlets exempelvärden ska inte användas som produktdata eller testfacit,
eftersom de kan avse en enskild kund och månad. En framtida golden-fixtur ska
i stället vara syntetisk och handräknad.

## Källkontroll och dataskydd

Det mottagna originalmejlet ligger lokalt i samma mapp men innehåller
personuppgifter och ska inte committas. Denna bedömning är den sanitiserade,
versionsstyrningsbara källposten.

- mottaget: 2026-09-17;
- avsändardomän: `sundsvallenergi.se`;
- SPF, DKIM och DMARC: godkända i mejlets transporthuvuden;
- originalfilens SHA-256:
  `3c5e6a4f90fad7566a22080397a9a4ca8b9c49bf7d48f3632790427745d13722`;
- bilagor: inga tariffbilagor; inbäddade bilder hör till mejlsignaturen.

## Uppföljning

Ingen följdfråga behövs för den avgränsade årskalkylen. En publik,
centralt lagrad nätserie skulle kunna förenkla inmatningen, men är inte
nödvändig när kundens faktura eller Mina sidor redovisar de
debiteringsgrundande värdena.
