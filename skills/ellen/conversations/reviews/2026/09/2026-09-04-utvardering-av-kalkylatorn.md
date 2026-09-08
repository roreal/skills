---
review_id: "2026-09-04-001"
date: "2026-09-04"
reviewer: Codex
status: completed
scope:
  - Lokal utvärderingsversion på http://localhost:4173/kalkylator
  - Funktionella användarflöden, responsivitet och grundläggande tillgänglighet
reviewed_head:
  neptune_academy: "9429346"
remote_verified: true
---

# Utvärdering av energipotential-kalkylatorn

## Bedömning

Kalkylatorns kärnflöden är stabila och den lokala `dist-preview`-versionen
går att använda som utvärderingsunderlag. Jag hittade inga krascher eller
ohanterade konsolfel i testmatrisen. Samtliga fjärrvärmealternativ gav
resultat i MWh-läget, de fyra övriga energisystemen fungerade med schablon,
MWh och kronor, tidigare tariffspärrar fungerade och mobilvyn hade ingen
horisontell överrullning.

Jag hittar inget P1-fel. Däremot finns en ny konkret UX-kontraktslucka i
kronorläget, den tidigare uppskjutna kvalitetsmärkningen är tydligt
missvisande i verkliga scenarier, och några tillgänglighetsproblem bör
åtgärdas före en bred publik lansering.

## Fynd

### P2 — Energitypsväljaren visas i kronorläget men ignoreras

När användaren fyller i en värmekostnad visas väljaren "Vad avser den
angivna energin?", trots att användaren har angett kronor, inte energi:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.tsx:110`
- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.tsx:596`

Motorn tvingar samtidigt kronorläget till `total_incl_dhw` oavsett vad
användaren väljer:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/utils/energiPotential.ts:249`

Reproducerat med Göteborg Energi, 10 000 m², 1 000 000 kr/år och 125 kW.
Valen "Total köpt värme" och "Enbart rumsvärme" gav exakt samma resultat.
Efter att "Enbart rumsvärme" valts redovisade resultatets tabell ändå
"Total köpt värme inklusive varmvatten". Beräkningen väljer den säkra
tolkningen, men gränssnittet erbjuder en kontroll som inte har någon effekt.

Rekommendation: dölj energitypsväljaren i kronorläget och förklara att
årskostnaden måste avse hela värmefakturan. Om delkostnader ska stödjas
senare behöver de ett eget uttryckligt flöde.

### P2 — Kvalitetsmärkningen beskriver inte det verkliga underlaget

Den tidigare uppskjutna frågan om strukturerade kvalitetsorsaker syns
tydligt i den körbara produkten:

- Standardscenariot har frånluft och "Nej / vet ej" på extra
  värmeåtervinning men märks ändå "Låg precision — schablon med
  värmeåtervinning".
- Ett direkt angivet MWh-värde utan debiterbar effekt märks "baserad på
  schablon", trots att energin inte är en schablon.
- Ett kronorvärde som räknats baklänges ur tariffen märks "faktisk energi
  angiven", trots att användaren inte angav någon energi.

Orsaken är att tre fasta texter används för nivåerna `high`, `medium` och
`low`, medan nivåerna numera kan sänkas av flera oberoende orsaker:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/utils/energiPotential.ts:268`
- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/utils/energiPotential.ts:560`

Rekommendationen från omgranskning 002 kvarstår: returnera strukturerade
kvalitetsorsaker och bygg texten från de orsaker som faktiskt gäller.

### P2 — Motstridig Gotlandstaxa och årsenergi accepteras utan varning

Kalkylatorn accepterade 500 MWh med alternativet "Gotland taxa 17, under
50 MWh/år" och visade ett normalt resultat utan varning. Tariffnamnen gör
gränsen synlig, men någon konsistenskontroll finns inte när den faktiska
eller härledda energin är känd:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/data/tariffer.generated.ts:416`
- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.tsx:312`

En användare kan därför få ett trovärdigt resultat från en tariff som
motsäger den egna inmatningen. Rekommendation: lägg tariffens
giltighetsvillkor i strukturerad metadata och visa en blockerande kontroll
eller tydlig varning. Undvik leverantörsspecifik strängtolkning i UI:t.

### P3 — Grundläggande tillgänglighetsbrister

Positivt: alla testade formulärkontroller har kopplade `label`-element,
felmeddelandet använder `role="alert"`, och mobilvyn ryms inom 390 px.

Kvarstående brister:

- Sidan saknar ett semantiskt `main`-landmärke; `PageShell` använder en
  vanlig `div.main-container`.
- Vid tom area visas rätt feltext, men fokus flyttas inte till areafältet.
- Hjälptexten `#999` mot vitt har kontrast 2,85:1, friskrivningen `#aaa`
  2,32:1 och små mätetiketter `#888` mot `#f8f4ff` 3,27:1. Samtliga ligger
  under WCAG AA:s 4,5:1 för normal text.

Berörda ställen:

- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/components/layout/PageShell.tsx:10`
- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.module.css:113`
- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.module.css:245`
- `/Users/robertrennel/Code/neptune_academy/neptune-marketing/src/pages/KalkylatorPage.module.css:326`

## Miljöfynd — utvärderingsversionen kräver ett specialkommando

Adressen svarade inte när granskningen började. Standardkommandot
`npm run preview` startade sedan en tom sida, eftersom `dist/index.html`
refererar till hashade JS/CSS-filer som inte finns i `dist/assets`.
Den fungerande byggnaden ligger i den ospårade katalogen `dist-preview/`
och behövde startas med:

```text
npx vite preview --host 127.0.0.1 --outDir dist-preview
```

Detta är ett lokalt paketerings-/överlämningsproblem, inte ett fel i själva
kalkylatorlogiken. För att andra agenter ska kunna upprepa utvärderingen bör
projektet få ett dokumenterat script som bygger och startar en konsekvent
utvärderingskatalog. `dist-preview/` är fortfarande ospårad och har inte
ändrats eller tagits bort av Codex.

## Godkända kontroller

- Tom area ger begripligt fel och inget resultat.
- Standardschablonen ger resultat.
- Direkt MWh-inmatning ger resultat.
- Alla sju namngivna leverantörsalternativ samt riksgenomsnittet ger
  resultat i MWh-läge.
- Gotland taxa 21 utan föregående års MWh stoppas korrekt i kronorläget.
- Samma Gotlandsfall fungerar när föregående års MWh anges.
- Göteborgs icke-konvergens visas som formulärfel utan `pageerror`.
- Göteborgsfallet fungerar när debiterbar effekt anges.
- Resultatet försvinner direkt när indata ändras.
- Övriga fyra energisystem fungerar i schablon-, MWh- och kronorläge.
- Mobilvy 390 px: formulär och resultat utan horisontell överrullning.
- Inga `pageerror` eller konsolfel under testmatrisen.
- 217 Vitest-tester godkända.
- `npx tsc --noEmit` godkänd.
- HEAD `9429346` matchar GitHubs `origin/main`.

Kontaktformuläret skickades inte, eftersom det hade skapat extern data.
Tariffresultaten jämfördes inte mot verkliga kundfakturor i denna
användbarhetsutvärdering.
