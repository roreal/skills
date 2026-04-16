Detta dokument beskriver hur konfigurering av enkey Gateway UG61, UG65 och UG71 går till
Generellt: För varje ändring måste du klicka på "Spara" för att ändringarna skall träda i kraft.
1. Fråga efter IP-adressen till Gateways webbgränssnitt.
Logga in med Username: "admin" och Password: "password"
Välj Extern antenn
2. Fråga efter affärsmöjlighetsnummer, t ex "A10067"
3. Byt lösenord från password till affärsmöjlighetsnummer+666673 i exemplet ovan skall då lösenordet vara "A10067666673"
4. Byt DNS för trådlöst nätverk från 192.168.1.XXX till 192.168.2.XXX.
5. Kontrollera och byt ev fast nätverk till DHCP
6. Gå till System - General Settings - System time och ställ in rätt tidszon "1 Sweden(Stockholm)" samt NTP Server Address: "sth1.ntp.se", Bocka i Enable NTP Server
7. Gå till System - Events - Events Settings och bocka för alla Record-bockar
8. Ta reda på Gatewayens serienummer.
9. Fråga vad det är för Kontraktsnummer, t ex "C10003".
10. Gå till Networks Server - Applications /#networkserver/applications
klicka på "+"
Sätt "Name" till "C10003-UG65-SN6221D4178971" där C10003 är kontraktsnummer, UG65 är gateway typ och N6221D4178971 är serienummer som föregås av "SN".
11. Sätt description till "Enkey MQTT"
Klicka på "+"
Välj "MQTT" i droplistan
12. Fråga efter Broker Address, t ex "p300-arcturus-transhub.enkey.io"
13. Ange Broker Adress enligt 12. ovan. Broker Port: 44883
Bocka i User Credentials
14. Be användaren fylla i Username och lösenord.
15. I Uplink data Topic: Lägg in samma som punkt 10. ovan
16. i Downlink data Topic: Lägg in "ug65/downlink/$deveui"
17. Spara och kontrollera att du får Status "Connected"
18. Gå till Network server device ../#networkserver/device
klicka på "Add".
19. Fråga i vilken mapp krypteringsnycklarna finns.
20. Öppna filerna 