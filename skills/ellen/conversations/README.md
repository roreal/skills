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
8. När en leverans är klar för en annan assistents granskning ska levererande
   assistent i sin **sista lokala loggcommit** både uppdatera den aktiva
   sessionsfilen och lägga en ny rad överst i `index.md`. Sessionsrubriken ska
   innehålla den maskinläsbara markören `REVIEW_READY: <granskare>` och posten
   ska ange exakt scope, fullständiga eller entydiga repo-HEAD:ar, testutfall
   samt om aktivering/push har skett. Om någon implementation ändras efter
   signalen ska en ny `REVIEW_READY`-post skrivas; en äldre signal får inte
   återanvändas.
9. `reviews/` reserveras för den granskande assistentens faktiska utlåtanden.
   En levererande assistent ska alltså inte skapa ett eget "godkännande" där
   för att signalera leverans. Bevakare ska därför följa hela
   `conversations/` — minst `sessions/`, `handoffs/`, `reviews/` och
   `index.md` — inte bara `reviews/`.
10. Granskningsloopen är självgående mellan assistenterna:
    `APPROVED_FOR_IMPLEMENTATION: Claude` betyder att Claude ska implementera
    det uttryckligen avgränsade handoff-scope som ligger bakom befintliga
    katalogspärrar, utan aktivering eller push, och därefter skriva
    `REVIEW_READY: Codex`.
    `REVIEW_READY: Codex` betyder att Codex ska börja granska utan nytt
    klartecken från Robert, och ett Codexutlåtande märkt
    `CHANGES_REQUIRED: Claude` betyder att Claude ska börja den avgränsade
    rättningsrundan utan nytt klartecken. Båda ska stanna och logga nästa
    signal när deras del är klar. En enkel bakgrundsbevakare kan upptäcka
    filändringen men kan inte i sig väcka en avslutad assistentturn; verklig
    händelsestyrd återstart kräver en aktiv assistentruntime eller en extern
    schemaläggare/hook. Signalen tar bort behovet av nytt sakgodkännande men
    är inte i sig en körbar väckningsmekanism.
    Om Claude inte kan slutföra ett steg utan ett tekniskt beslut ska Claude
    skriva och committa en ny unik `BLOCKED: Codex`-post med blockerare och
    handlingsalternativ. En bar `BLOCKED`-post är inte ett nytt
    protokollsteg eftersom den saknar mottagare; bryggan routar den bara
    bakåtkompatibelt till Codex så att äldre signaler inte tappas. Codex ska
    lösa frågan inom befintligt scope och bara fråga Robert när ny
    behörighet eller en verklig scopeändring krävs.
11. Robert godkände 2026-09-16 att även tariffaktivering och push automatiseras
    efter godkända kontrollpunkter, med den uttryckliga instruktionen:
    *"Kan vi automatisera Aktivering och push så gör gärna det."* Följ denna
    tillståndskedja:
    `APPROVED_FOR_ACTIVATION: Claude` → Claude aktiverar lokalt exakt det
    granskade scopet och skriver `ACTIVATION_READY: Codex` → Codex granskar
    aktiveringsdiff, räkning och regressioner →
    `APPROVED_FOR_PUSH: Claude` → Claude gör en normal fast-forward-push av
    exakt de granskade committarna och verifierar varje remote-HEAD med
    `git ls-remote`. Claude skapar därefter en sista, avgränsad skills-commit
    med pushkvittot i session/handoff/index, pushar även den och verifierar
    den slutliga skills-remote-HEAD:en på nytt. Ett pushkvitto får alltså inte
    lämnas som enbart lokal commit. Ingen ytterligare fråga till Robert krävs
    inom kedjan.
    Kedjan ska däremot stoppa med `CHANGES_REQUIRED` eller `BLOCKED` om tester
    faller, diffen innehåller orelaterade filer, HEAD inte är den granskade,
    remote har flyttats, en merge/rebase skulle behövas eller scope har
    ändrats. Force-push, reset, konfliktlösning genom överskrivning och
    aktivering av andra tariffer är aldrig automatiskt tillåtna.
12. Rollfördelningen får inte beskrivas tvetydigt:
    **Codex är granskare/godkännare och pushar aldrig; Claude är implementatör
    och ensam pushverkställare; `agent-bridge` är endast signaltransport och
    gör inga repoändringar.** Relevanta loggar använder fälten
    `approved_by: Codex`, `executed_by: Claude` och
    `dispatched_by: agent-bridge`. Formuleringen att "Codex pushade" är alltid
    fel; korrekt formulering är att Codex godkände och Claude verkställde.
13. Ett sessions-ID ska vara globalt unikt i `index.md`. Bryggan får inte
    dispatcha en översta post vars ID förekommer mer än en gång i den
    committade indexfilen. En historisk dubblett rättas med en daterad
    rättelsepost, aldrig genom att tyst skriva om äldre sessionsinnehåll.

## Körbar agentbrygga

Den maskinläsbara kedjan kan köras av
[`automation/agent-bridge.zsh`](automation/agent-bridge.zsh). Bryggan väntar
på en ny, committad toppost i `index.md` och anropar `codex exec` eller
`claude --print` beroende på signal. Den är seriell, har at-most-once-låsning
och stoppar fail-closed vid fel eller om den anropade assistenten inte
skriver en ny signal. Driftinstruktioner och säkerhetsgränser finns i
[`automation/README.md`](automation/README.md).

Konversationsloggar är historik och samarbetsunderlag. Kod, konfiguration, avtal, mätdata och beslutad teknisk dokumentation är fortfarande primära källor för hur Ellen faktiskt fungerar.

## Namngivning och status

Sessions-ID använder formatet `ÅÅÅÅ-MM-DD-NNN`. Filnamn använder datum och ett kort beskrivande namn med gemener och bindestreck.

Tillåtna statusvärden:

- `active` – sessionen pågår eller väntar på nästa naturliga steg.
- `completed` – sessionens uttryckliga uppgift är avslutad.
- `blocked` – arbetet kan inte fortsätta utan ny information eller extern förändring.
- `archived` – sessionen bevaras endast som historik.
