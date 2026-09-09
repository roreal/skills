---
review_id: "2026-09-09-009"
date: "2026-09-09"
reviewer: Codex
status: archive-inventoried-and-replayed
scope:
  - Brf Åkermannen 33:s Stockholm Exergi-fakturaarkiv
  - 22 PDF-filer, januari 2025–augusti 2026
  - Python- och TypeScriptmotorernas direkta månads- och kontraktsvägar
reviewed_heads:
  skills: "2326adcc27d9a294277bcc89a19ecb2ab9ddc7e8"
  enkey-agents: "fd8f8da3eb17cce638dc2f3370efa027c2afcad6"
  neptune_academy: "f1df177b7157590c7b8a47988f2ca3c81c52c603"
implementation_changed: false
raw_invoices_committed: false
feeds_next_version: "v16 documentation; later separate archive fixture"
---

# Inventering och återspelning av Åkermannens fakturaarkiv

## Samlad bedömning

Arkivet innehåller **22 PDF-filer men 20 unika fakturaperioder**, en för varje
kalendermånad januari 2025–augusti 2026. Mars och april 2026 finns i två kopior vardera.
PDF-filernas bytehashar skiljer sig, men normaliserad extraherad text är identisk inom
respektive par. De ska därför räknas som kopior, inte fyra fakturor.

Detta löser den äldre dokumentationsmotsägelsen:

- till och med juli 2026 finns 21 PDF-filer men 19 unika fakturaperioder;
- med augusti finns 22 PDF-filer men 20 unika fakturaperioder;
- uppgiften ”18 fakturor januari 2025–juli 2026” är inte korrekt för det nu kompletta
  arkivet;
- uppgiften ”21 fakturor maj 2025–juli 2026” har räknat samtliga fysiska filer till och
  med juli men anger fel startmånad och skiljer inte kopior från unika perioder.

Den frysta baslinjefixturen maj 2025–april 2026 är fortfarande korrekt avgränsad till tolv
unika månader och ska inte ändras. Arkivet ger därutöver fyra tidigare månader, en
preliminär-/avräkningskedja maj–juli 2026 och augustis redan separat verifierade månad.

## Resultat mot beräkningsmotorerna

Följande sju fakturor utanför den befintliga tolvmånadersfixturen återspelades som
enkelfall i både Python och TypeScript, genom både den direkta månadsfunktionen och
`monthly_invoice`-kontraktsvägen:

| Period | Fakturastatus | Faktura inkl. moms | Motor inkl. moms | Motor − faktura |
| --- | --- | ---: | ---: | ---: |
| 2025-01 | avläst | 83 734,19 kr | 83 734,166312 kr | −0,023688 kr |
| 2025-02 | avläst | 76 535,59 kr | 76 535,581459 kr | −0,008541 kr |
| 2025-03 | avläst | 67 432,05 kr | 67 432,039562 kr | −0,010438 kr |
| 2025-04 | avläst | 28 615,27 kr | 28 615,256027 kr | −0,013973 kr |
| 2026-05 | preliminär | 24 076,36 kr | 24 076,362603 kr | +0,002603 kr |
| 2026-06 | preliminär | 18 704,71 kr | 18 704,714212 kr | +0,004212 kr |
| 2026-08 | avläst | 18 562,43 kr | 18 562,440103 kr | +0,010103 kr |

Direkt- och kontraktsvägen gav samma komponenter i båda språken. Kontraktsresultaten var
`complete`/`exact`; här betyder `exact` att tariffens matematik återspelas exakt för
angiven fakturaindata. Det gör inte en preliminär energivolym till avläst förbrukning.
Samtliga kvarvarande differenser ligger i fakturaavrundningen, som mest cirka 2,4 öre.

## Maj–juli 2026 är en avräkningskedja

Maj- och junifakturorna använder preliminär energi. Julifakturan ersätter den preliminära
delen med avlästa värden och innehåller därför energirader från tre månader samt en
negativ återföringsrad. Sanitiserat samband:

- majfakturan debiterar 20,368 MWh, varav 11,711 MWh redan är avläst för 1–14 maj och
  resterande 8,657 MWh är preliminärt;
- junifakturan debiterar 8,705 MWh preliminärt;
- julifakturan återför 17,362 MWh, exakt `8,657 + 8,705`;
- julifakturan debiterar avläst 5,461 MWh för 15–31 maj, 9,172 MWh för juni och
  7,190 MWh för juli;
- slutligt avlästa kalendermånader blir maj 17,172 MWh, juni 9,172 MWh och juli
  7,190 MWh, sammanlagt 33,534 MWh.

Återspelning med dessa tre verkliga kalendermånader ger:

| Kontroll | Inklusive moms |
| --- | ---: |
| Motorns tre månadskostnader | 60 216,266918 kr |
| De tre fakturorna maj–juli | 60 216,25 kr |
| Differens | +0,016918 kr |

Samma resultat och samma `complete`/`exact`-status erhölls i Python och TypeScript. Detta
är starkare verifiering än att jämföra julifakturan som ett ensamt månadsfall.
`Periodens användning (A) 21,823 MWh` på julifakturan är summan av de tre nytillkomna
avlästa delperioderna; den är **inte** julis kalendermånadsförbrukning. Om 21,823 MWh läggs
in som juliindata skapas ett felaktigt kontrollfall.

## Bindande test- och datamodellråd

1. Behåll `akermannen-baslinje.json` fryst till maj 2025–april 2026.
2. Skapa senare en separat sanitiserad arkiv-/out-of-sample-fixtur i båda produktrepona.
3. Skilj i fixturen mellan:
   - fakturans huvudperiod;
   - avläst (`A`) respektive preliminär (`P`) energistatus;
   - faktisk förbrukningsperiod för varje energirad;
   - återföring av tidigare preliminärdebitering;
   - fakturabelopp och kalendermånadens tariffkostnad.
4. Testa januari–april 2025 och augusti 2026 som vanliga enkelfakturor.
5. Testa maj–juli 2026 som en sammanhållen avräkningskedja. Ett enskilt julitest får bara
   använda 7,190 MWh som fysisk juliförbrukning; tidigare månaders justeringsrader ska
   representeras separat.
6. Märk aldrig preliminär fakturaenergi som avläst eller `confirmed_mwh`. Motorns
   `exact` beskriver formelåterspelningen, inte mätvärdets kvalitet.
7. Dubblettkopiorna för mars/april 2026 ska dedupliceras via fakturaperiod och semantiskt
   innehåll, inte enbart via PDF-filens bytehash.

Efter att den separata fixturen har lagts till och testerna passerar kan
leverantörsmetadata anges som exempelvis:

> Verifierad mot 20 unika månadsfakturor/fakturaperioder januari 2025–augusti 2026
> (22 PDF-filer inklusive två dubblettkopior).

V16 får rätta motsvarande dokumentationsrad och hänvisa till denna bedömning, men ska
fortfarande inte ändra produktfixtur, leverantörsdata, tariffdata eller produktkod.

## Körda kontroller

- normaliserad textjämförelse av de två marskopiorna och de två aprilkopiorna: identisk;
- temporär Pythonåterspelning av sju enkelfall samt avräkningskedjan: godkänd;
- temporär TypeScript/Vitest-återspelning av samma fall: `1 passed`;
- befintliga fokuserade Pythonregressioner: `65 passed`;
- befintliga fokuserade TypeScriptregressioner: `133 passed`;
- inga produktfiler, råfakturor eller kundidentifierare kopierades eller ändrades.

