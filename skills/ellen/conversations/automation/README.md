# Agentbrygga för Ellen

`agent-bridge.zsh` gör den maskinläsbara kedjan i
`conversations/README.md` körbar. Den följer den översta, committade raden i
`conversations/index.md` och anropar nästa lokala CLI:

| Signal | Anrop |
| --- | --- |
| `REVIEW_READY: Codex` | `codex exec` |
| `ACTIVATION_READY: Codex` | `codex exec` |
| `BLOCKED: Codex` | `codex exec` |
| `BLOCKED` | `codex exec` (bakåtkompatibel säkerhetsväg) |
| `APPROVED_FOR_IMPLEMENTATION: Claude` | `claude --print` |
| `CHANGES_REQUIRED: Claude` | `claude --print` |
| `APPROVED_FOR_ACTIVATION: Claude` | `claude --print` |
| `APPROVED_FOR_PUSH: Claude` | `claude --print` |

Bryggan är seriell: nästa assistent startas först när föregående CLI-anrop
har avslutats och skrivit en ny indexpost. Den kräver att signalen är ren
och finns i `HEAD`, använder ett singletonlås och markerar signalen som
övertagen före anrop. Vid CLI-fel, oförändrat sessions-ID eller annan
avvikelse stoppar den i stället för att försöka mutera samma steg igen.
`HUP`, `INT` och `TERM` avslutar bevakaren och låter `EXIT`-städningen ta
bort singletonlåset; signalhanteraren får aldrig fortsätta poll-loopen utan
lås.
Sessions-ID:t i den översta signalen måste också förekomma exakt en gång i den
committade indexfilen; en dubblett stoppar kedjan fail-closed.

En implementatör som behöver ett tekniskt beslut ska skriva
`BLOCKED: Codex`, inte en mottagarlös `BLOCKED`. Bryggan routar även den
äldre bara markören till Codex för att inte tappa redan skapade signaler.

Rollerna är fasta:

- **Codex granskar och godkänner. Codex pushar aldrig.**
- **Claude implementerar och är den enda pushverkställaren** efter en uttrycklig
  `APPROVED_FOR_PUSH: Claude`-signal.
- **agent-bridge är endast signaltransport** och gör inga repoändringar själv.

Loggar ska därför använda `approved_by: Codex`, `executed_by: Claude` och
`dispatched_by: agent-bridge` när respektive roll har deltagit. Formuleringen
"Codex pushade" är alltid fel. Efter en godkänd push ska Claude även pusha ett
avgränsat skills-kvitto med sessions-/handoff-/indexbokföringen och verifiera
den slutliga remote-HEAD:en, så att inget pushkvitto lämnas endast lokalt.

Runtimefiler lagras utanför arbetskopian:

- state: `<skills-repot>/.git/ellen-agent-bridge.state`;
- lås: `<skills-repot>/.git/ellen-agent-bridge.lock`;
- logg: `<skills-repot>/.git/ellen-agent-bridge.log`.

Kommandon från Ellen-mappen:

```sh
zsh conversations/automation/agent-bridge.zsh status
zsh conversations/automation/agent-bridge.zsh selftest
zsh conversations/automation/agent-bridge.zsh seed
zsh conversations/automation/agent-bridge.zsh once
zsh conversations/automation/agent-bridge.zsh run
```

`seed` markerar den nuvarande översta posten utan att anropa någon. Detta
ska göras när en assistent redan arbetar med det aktuella steget, så att
jobbet inte dubbleras. `run` pollar som standard var 15:e sekund; intervallet
kan ändras med `ELLEN_BRIDGE_INTERVAL_SECONDS`.

Varje Claude-anrop får ett nytt UUID med `--session-id`, körs med
`--no-session-persistence` och får hela uppdraget som ett explicit
promptargument. Det hindrar tidigare sessioner och bakgrundsnotiser från att
tas för den nya signalen. Anropet använder dessutom
`--output-format stream-json` och filtrerar strömmen med `jq --unbuffered`.
`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0` gör att huvudkörningen väntar tills
delegerade bakgrundsagenter verkligen är klara i stället för att avbryta dem
efter klientens tiominutersgräns.
Claude-prompten kräver dessutom att huvudkörningen själv väntar in, granskar
och sammanför delegerat arbete och därefter committar nästa indexsignal. Den
får inte avsluta med enbart beskedet att en bakgrundsagent senare ska återuppta
arbetet.
Runtime-loggen visar därför startens tilldelade sessions-ID,
`CLAUDE_TOOL start` när Claude börjar använda ett verktyg, eventuella
`CLAUDE_UPDATE`-texter och ett avslutande `CLAUDE_RESULT`, utan att dumpa
verktygsparametrar eller hela verktygsresultat. Följ aktiviteten med:

```sh
tail -f "$(git rev-parse --show-toplevel)/.git/ellen-agent-bridge.log"
```

Bryggan ger inte någon assistent större mandat än protokollet. Codex får
aldrig pusha. Claude får endast pusha efter `APPROVED_FOR_PUSH: Claude`, och
båda klienterna instrueras att stoppa vid ändrade HEAD:ar, orelaterade
diffar eller andra brutna grindar. Force-push och destruktiva
återställningar är fortsatt förbjudna.

Detta är en lokal runtimebrygga, inte en tjänst som överlever om datorn
stängs av. För automatisk start efter omstart kan samma script senare
registreras som en användarägd `launchd`-tjänst efter separat kontroll av
loggrotation och återstartspolicy.
