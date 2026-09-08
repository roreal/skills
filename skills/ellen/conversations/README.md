# Konversationslogg för Ellen

Den här mappen bevarar projektets synliga samtal med AI-assistenter. Syftet är att göra beslut, antaganden, frågor och överlämningar sökbara utan att blanda ihop konversationer med projektets tekniska källor.

## Struktur

```text
conversations/
├── README.md
├── index.md
├── handoffs/
│   └── ÅÅÅÅ/
│       └── MM/
│           └── ÅÅÅÅ-MM-DD-beskrivande-namn.md
├── proposals/
│   └── ÅÅÅÅ/
│       └── MM/
│           └── ÅÅÅÅ-MM-DD-beskrivande-namn.md
├── reviews/
│   └── ÅÅÅÅ/
│       └── MM/
│           └── ÅÅÅÅ-MM-DD-beskrivande-namn.md
├── sessions/
│   └── ÅÅÅÅ/
│       └── MM/
│           └── ÅÅÅÅ-MM-DD-beskrivande-namn.md
└── templates/
    └── session-template.md
```

- `index.md` är den gemensamma ingången till alla loggade sessioner.
- `handoffs/` innehåller daterade, beständiga tillståndsbilder för pauser och
  assistentbyten: aktuell beslutspunkt, repo-heads, spärrar och exakt nästa steg.
- `proposals/` innehåller separata, daterade designförslag (t.ex. ett
  schemaförslag eller en teknisk lösning) som väntar på utvärdering
  innan de genomförs — samma princip som `reviews/`, men för förslag
  i stället för avslutade granskningar.
- `reviews/` innehåller separata, daterade granskningsanteckningar som kan
  länkas från en session utan att blandas ihop med samtalsutskriften.
- `sessions/` innehåller en Markdown-fil per sammanhängande arbetssession.
- `templates/` innehåller mallen för nya sessionsfiler.

## Vad som loggas

- Användarens synliga meddelanden, ordagrant när de är tillgängliga.
- Assistentens slutliga, synliga svar, ordagrant när de är tillgängliga.
- Kort sammanfattning, fattade beslut och öppna frågor.
- Vem som deltog, till exempel Robert, Codex eller Claude.
- Tidpunkt och ändringshistorik när de är kända.

Statusmeddelanden under pågående verktygsarbete kan utelämnas för att hålla loggen läsbar. Viktiga resultat från arbetet ska däremot finnas i assistentens slutliga svar eller i sammanfattningen.

Om en äldre konversation måste rekonstrueras eller sammanfattas ska detta anges i sessionsfilens metadata. En sammanfattning får inte presenteras som ett ordagrant citat.

## Vad som inte loggas

- Systeminstruktioner, dolda resonemang eller intern agentkommunikation.
- Hemligheter, autentiseringsuppgifter, API-nycklar eller andra känsliga värden.
- Fullständiga verktygsloggar om de inte behövs för att förstå ett beslut.
- Innehåll från en annan assistants session som inte uttryckligen har delats i projektet.

Om känsligt innehåll måste omnämnas används markeringen `[REDACTED: orsak]` i stället för värdet.

## Arbetsregel för assistenter

1. Skapa eller fortsätt rätt sessionsfil.
2. Lägg till synliga meddelanden i kronologisk ordning och ange talare.
3. Uppdatera sammanfattning, beslut och öppna frågor när samtalet förändrar dem.
4. Uppdatera `index.md` när en session skapas eller byter status.
5. Ändra inte äldre repliker i tysthet. Lägg en daterad rättelse i filens ändringslogg om något måste korrigeras.
6. Påstå bara kännedom om andra assistants arbete när det finns i repositoryt eller har delats i den aktuella konversationen.
7. Vid en längre paus: skapa en daterad fil i `handoffs/`, länka den från
   `index.md` och ange uttryckligen om någon automatisk återstart/bevakning finns.

Konversationsloggar är historik och samarbetsunderlag. Kod, konfiguration, avtal, mätdata och beslutad teknisk dokumentation är fortfarande primära källor för hur Ellen faktiskt fungerar.

## Namngivning och status

Sessions-ID använder formatet `ÅÅÅÅ-MM-DD-NNN`. Filnamn använder datum och ett kort beskrivande namn med gemener och bindestreck.

Tillåtna statusvärden:

- `active` – sessionen pågår eller väntar på nästa naturliga steg.
- `completed` – sessionens uttryckliga uppgift är avslutad.
- `blocked` – arbetet kan inte fortsätta utan ny information eller extern förändring.
- `archived` – sessionen bevaras endast som historik.
