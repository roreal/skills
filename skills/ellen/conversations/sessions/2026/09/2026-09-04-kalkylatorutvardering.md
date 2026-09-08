---
session_id: "2026-09-04-001"
date: "2026-09-04"
status: active
participants:
  - Robert
  - Codex
  - Claude
topic: "Utvärdering av energipotential-kalkylatorn"
---

# Utvärdering av energipotential-kalkylatorn

## Sammanfattning

Robert gjorde den lokala kalkylatorn tillgänglig för utvärdering på port
4173. Codex körde en webbläsarbaserad testmatris av huvudflöden,
tariffalternativ, felhantering, responsivitet och grundläggande
tillgänglighet. Kärnflödena fungerade utan körfel. Tre P2-fynd och ett antal
P3-tillgänglighetsbrister dokumenterades i en separat granskningsrapport.

Den fungerande utvärderingsbyggnaden ligger i den ospårade katalogen
`dist-preview/`; standardkommandot `npm run preview` serverar i nuvarande
lokala arbetskopia en inkonsekvent `dist/` och ger en tom sida. Ingen
implementation eller byggkatalog ändrades av Codex.

## Konversation

### Robert — användare

> Nu finns det en utvärderingsfunktion av kalkylatorn här: http://localhost:4173/kalkylator

### Codex — assistent

Kalkylatorns kärnflöden fungerar stabilt och inga nya P1-fel hittades. Den
fullständiga utvärderingen finns här:

- [Utvärdering av energipotential-kalkylatorn](/Users/robertrennel/Code/skills/skills/ellen/conversations/reviews/2026/09/2026-09-04-utvardering-av-kalkylatorn.md:1)

Nya eller bekräftade P2-fynd är att kronorläget visar en energitypsväljare
som motorn ignorerar, att kvalitetsmärkningen beskriver fel orsak i flera
vanliga scenarier och att en motstridig Gotlandstaxa/årsenergi accepteras
utan varning. Dessutom saknas ett `main`-landmärke, fokus flyttas inte till
felaktig area och flera små texter har för låg kontrast.

### Claude — assistent

Gick igenom utvärderingen och åtgärdade fyra av fem punkter, i den ordning som lades fram och godkändes av Robert:

1. **Energitypsväljaren i kronorläget** — dold när `energyInputMode === 'kr'`, med en förklarande text vid kronorfältet i stället ("Ska avse hela värmefakturan, inklusive varmvatten.").
2. **Kvalitetsmärkningen** — byggdes tidigare av tre fasta strängar per nivå. `calcConfidence` returnerar nu nivån OCH en text byggd av de faktiska orsakerna (ett nytt `energyInputMode`-fält skiljer nu på direkt angiven och kr-löst energi). Verifierat i webbläsaren: kronorläget visar nu "Preliminär uppskattning — energi löst ur angivet kronbelopp, effekt uppskattad, ej angiven" i stället för det tidigare felaktiga "Hög precision — faktisk energi angiven".
3. **Tillgänglighet** — `<main>`-landmärke tillagt i `PageShell`, fokus flyttas nu till areafältet vid tomt-area-felet, tre textfärger bytta till `#6f6f6f` (4,64–5,02:1, tidigare 2,32–3,27:1).
4. **Miljöfyndet** — nytt `npm run eval`-script bygger och serverar en fräsch, gitignorerad `dist-eval/`-mapp varje gång, dokumenterat i README. Ersätter det improviserade `dist-preview/`-arbetssättet. Utvärderingsmiljön på `localhost:4173` är omstartad mot den nya katalogen med samtliga fyra fixar.

Punkt 5 (strukturerad giltighetsmetadata för Gotlands två taxor, så att en motsägande årsenergi kan varnas för) är avsiktligt inte gjord än — den ändrar källdata i katalogen, inte bara kod, och väntar på ett konkret förslag från Claude innan den rörs.

Under tiden har Codex redan börjat arbeta direkt i den verifieringslista Claude sammanställde tidigare (`Fjarrvarmetariffer/verifieringslista-fjarrvarmebolag.md`) — 16 tariffer kontrollerade mot leverantörernas 2026-underlag i en första omgång.

221 gröna vitest (upp från 217), `tsc --noEmit` rent. Pushat till `origin/main`: `c4d257d` (UX/datakvalitet/tillgänglighet), `f2dfe6c` (eval-scriptet).

### Claude — assistent

Sammanställde ett förslag för punkt 5, för Robert och Codex att utvärdera innan något implementeras:

- [Förslag: strukturerad giltighetsmetadata för tariffer med årsenergigräns](/Users/robertrennel/Code/skills/skills/ellen/conversations/proposals/2026/09/2026-09-04-tariff-giltighetsmetadata.md:1)

I korthet: ett generellt (inte Gotland-specifikt) `eligibility`-fält på katalognivå med `min_mwh`/`max_mwh` mot samma affärsvariabel som volymrabattens `foregaende_ars_mwh` redan använder, kontrollerat i webbkalkylatorns kod (inte den delade Python-motorn, av samma skäl som tidigare P1-fynd hölls där). Rekommenderar en varningsbanner, inte en blockering — resonemanget finns i förslaget. Fyra öppna frågor väntar på svar, viktigast: vilken sida av 50 MWh-gränsen som faktiskt hör till respektive taxa (bör läggas som ett villkor i verifieringslistan, inte gissas).

Inget implementerat än.

## Ändringslogg

- `2026-09-04T08:29:04+02:00` – Codex utvärderade kalkylatorn i lokal webbläsare och dokumenterade funktionella, UX- och tillgänglighetsrelaterade fynd.
- `2026-09-04T08:51:50+02:00` – Claude åtgärdade fyra av fem föreslagna punkter (energitypsväljaren, kvalitetsmärkningen, tillgänglighet, utvärderingsscript), pushade till origin/main och startade om utvärderingsmiljön.
- `2026-09-04T08:59:51+02:00` – Claude sammanställde ett designförslag för punkt 5 (giltighetsmetadata), inget implementerat.
