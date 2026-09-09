---
review_id: "2026-09-09-008"
date: "2026-09-09"
reviewer: Codex
status: invoice-replayed
scope:
  - Sthlm Exergi Aug 2026.pdf
  - Stockholm Exergi Normalprislista 2026
  - Brf Åkermannen 33, augusti 2026
  - Python- och TypeScript-motorernas månadsberäkning
source_sha256: "6d1f72b09fc78c1672259e7916c6a27e0a14c957dedda37c06fe7d88f12c0302"
reviewed_heads:
  skills: "2326adcc27d9a294277bcc89a19ecb2ab9ddc7e8"
  enkey-agents: "fd8f8da3eb17cce638dc2f3370efa027c2afcad6"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
raw_invoice_committed: false
feeds_next_version: "v16 documentation only; later separate test-data implementation"
---

# Verifiering av Åkermannens augustifaktura 2026

## Bedömning

Augustifakturan är ett användbart nytt **out-of-sample-kontrollfall** för Stockholm
Exergis 2026-tariff. Den ligger utanför den frysta baslinjefixturen maj 2025–april 2026 och
efter leverantörsfilens nuvarande verifieringsslut juli 2026. Den verifierar därför att
modellen fortsätter fungera på en ny fakturamånad, inte bara att den återspelar den data
som användes när modellen byggdes.

Både Pythonmotorns direkta månadsfunktion, TypeScriptmotorns direkta månadsfunktion och de
två språkens validerade `monthly_invoice`-kontraktsväg ger samma resultat. Beräknad kostnad
är `14 849,952082 kr` exklusive moms mot fakturans `14 849,95 kr`. Motorns
`18 562,440103 kr` inklusive moms ligger cirka **ett öre** över fakturans
`18 562,43 kr` före öresutjämning. Skillnaden kommer efter de redan matchande
exklusive-momsraderna och är fakturans avrundning, inte ett tariff- eller modellfel.

Ingen tariffstatus eller 7/57/28-räkning ändras. Fakturan stärker den redan implementerade
Stockholm Exergi-modellen och bör senare bli en separat regressionsfixtur, men ska inte
läggas in i den frysta tolvmånadersbaslinjen.

## Sanitiserat fakturafacit

Kund-, avtals-, betalnings-, adress- och fakturanummer återges inte här.

| Storhet | Faktura | Motor |
| --- | ---: | ---: |
| Period | 2026-08-01–2026-08-31 | 2026, månad 8 |
| Avläst energi | 7,161 MWh | 7,161 MWh |
| Debiterbar effekt | 125 kW | 125 kW |
| Årlig fast avgift | 3 435 kr/år | 3 435 kr/år |
| Årligt effektbelopp | 143 250 kr/år | 125 × 1 146 kr/kW,år |
| Fast + effekt, 31/365 | 12 458,18 kr | 12 458,178082 kr |
| Energipris april–oktober | 334 kr/MWh | 334 kr/MWh |
| Energikostnad | 2 391,77 kr | 2 391,774 kr |
| Returtemperatur | 32,7 °C | ej kostnadspåverkande i augusti |
| Returtemperaturpost | 0,00 kr | 0 kr |
| Summa exklusive moms | 14 849,95 kr | 14 849,952082 kr |
| Summa inklusive moms före öresutjämning | 18 562,43 kr | 18 562,440103 kr |
| Öresutjämning/att betala | −0,43 kr / 18 562 kr | utanför tariffmotorn |

Fakturan bekräftar dessutom leverantörens uppgifter om rekommenderad effekt 125 kW,
effektgräns 96 kW och uppskattad årsenergi 434 MWh. De tre uppgifterna är kundspecifika och
får inte flyttas till generell tariffdata.

## Vad kontrollfallet verifierar

1. Årsavgifterna periodiseras i denna Stockholmfaktura med `31/365`, vilket motorn redan
   gör; det är inte samma 1/12-regel som Lidköping Energi bekräftade för sin tariff.
2. Augusti använder sommarpriset 334 kr/MWh.
3. En returtemperatur redovisas även utanför november–mars, men prisfaktorn är 0 och
   kostnaden blir noll. Det stöder kontraktets `tillampliga_manader = {11,12,1,2,3}`:
   returtemperatur ska inte krävas för en komplett augustiberäkning.
4. Ingen rad för energi under −3 °C debiteras. Ett framtida fixturuttag kan normalisera den
   fullständigt specificerade fakturans uteblivna kallenergirad till `mwh_kallt = 0`, samma
   konvention som den befintliga Åkermannen-fixturen använder. Regeln ska dokumenteras i
   fixturen; nollan får inte uppstå som ett generellt motordefault när ett obligatoriskt
   fakturafält saknas.
5. Moms och fakturans slutliga öresutjämning ligger efter tariffkomponenterna. Motorn ska
   inte ändras för differensen på cirka ett öre.
6. Fakturans ”uppskattad årsenergi 434 MWh” är ett kundspecifikt leverantörsestimat, inte
   ett avläst årsvärde. Det får varken märkas `confirmed_mwh`, ersätta de faktiska
   månadsserier som Stockholms årsprodukt kräver eller användas som generell årsprofil.

## Rekommenderad framtida testdata

Skapa i en separat implementation efter dokumentationsetappen en ny, sanitiserad
out-of-sample-fixtur i båda produktrepoerna, exempelvis
`akermannen-verifiering-2026.json`. Återanvänd inte eller utöka inte
`akermannen-baslinje.json`, vars kontrakt uttryckligen är exakt tolv månader
maj 2025–april 2026.

Den sanitiserade augustiraden kan bära:

```json
{
  "ar": 2026,
  "manad": 8,
  "mwh": 7.161,
  "mwh_kallt": 0,
  "returtemp_c": 32.7,
  "kapacitet": 125,
  "korrigering_kr": 0,
  "faktura_inkl": 18562.43
}
```

Testet ska kontrollera:

- direkta månadsfunktionen och `monthly_invoice`-kontraktsvägen i Python och TypeScript;
- `complete`/`exact` med verifierad effekt och en uttrycklig, fakturahärledd nolla för kall
  energi;
- samma kostnad i båda språken;
- exklusive-momssumman mot 14 849,95 kr och inklusive-momssumman inom befintlig
  fakturatolerans;
- att returtemperaturfältet inte krävs i augusti och att dess kostnad är noll;
- att öresutjämningen inte blandas in i tariffmotorns kostnadskomponenter.

När kontrollfallet verkligen lagts till och testerna passerar kan leverantörsfilens
verifieringsmetadata uppdateras från ”till och med juli 2026” till ”till och med augusti
2026”. Den äldre rubrikens uppgift ”18 fakturor” och JSON-blockets ”21 fakturor” ska då
synkas till ett gemensamt, verifierat antal i samma ändring; antalet får inte gissas från
antal kalendermånader.

## Källhantering och V16

Råfakturan ligger i kundens SynologyDrive och innehåller person-/kund-, betalnings- och
avtalsuppgifter. Den ska inte kopieras till repositoriet, stagas eller pushas. SHA-256 ovan
gör bedömningen spårbar till originalet utan att återge identifierarna.

V16 är fortfarande en dokumentationsetapp. Claude ska i V16 endast hänvisa till denna
bedömning som ett nytt, godkänt framtida Stockholm-testfall och ta med granskningsfilen i
den fokuserade dokumentationscommitten. Ingen produktfixtur, leverantörsfil, genererad fil
eller produktkod ska ändras i V16.
